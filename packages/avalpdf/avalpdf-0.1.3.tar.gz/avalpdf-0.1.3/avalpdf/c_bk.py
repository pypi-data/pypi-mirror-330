#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
import sys
from pdfixsdk import *
import ctypes
from typing import Dict, List, Tuple
import tempfile
import urllib.request
import urllib.parse

# ANSI color codes
COLOR_GREEN = '\033[32;1m'    # P tags (verde brillante)
COLOR_RED = '\033[38;5;204m'  # Headings (rosa chiaro)
COLOR_ORANGE = '\033[33;1m'   # Figures (arancione brillante)
COLOR_PURPLE = '\033[35;1m'   # Tables (viola brillante)
COLOR_BLUE = '\033[34;1m'     # Lists (blu brillante)
COLOR_RESET = '\033[0m'       # Reset color

def pdf_to_json(pdf_path):
    """Convert PDF to JSON using PDFix SDK"""
    pdfix = GetPdfix()
    doc = pdfix.OpenDoc(pdf_path, "")
    
    if doc is None:
        raise Exception("Failed to open PDF document")
    
    # Prepare PDF to JSON conversion params
    params = PdfJsonParams()
    params.flags = (kJsonExportStructTree | kJsonExportDocInfo | kJsonExportText)
    
    # Convert to JSON
    json_conv = doc.CreateJsonConversion()
    json_conv.SetParams(params)
    
    # Extract data to stream
    mem_stm = pdfix.CreateMemStream()
    json_conv.SaveToStream(mem_stm)
    
    # Read memory stream into bytearray
    sz = mem_stm.GetSize()
    data = bytearray(sz)
    raw_data = (ctypes.c_ubyte * sz).from_buffer(data)
    mem_stm.Read(0, raw_data, len(raw_data))
    
    # Cleanup
    mem_stm.Destroy()
    doc.Close()
    
    return json.loads(data.decode("utf-8"))

def extract_content(element, level=0):
    results = []
    
    # Skip if element is not a dictionary
    if not isinstance(element, dict):
        return results
        
    tag_type = element.get('S', '')
    
    try:
        # Gestione speciale per tag Part
        if tag_type == 'Part':
            if 'K' in element and isinstance(element.get('K'), list):
                for child in element.get('K', []):
                    if isinstance(child, dict):
                        nested_results = extract_content(child, level)
                        results.extend(nested_results)
            return results
            
        if tag_type and tag_type != 'Document':
            content = []
            child_elements = []
            
            # Crea l'elemento base solo con il tag
            element_dict = {"tag": tag_type}
            
            if tag_type == 'Figure':
                alt_text = element.get('Alt', '')
                element_dict["text"] = alt_text if alt_text else ""
                results.append(element_dict)
                return results
                
            elif tag_type == 'Table':
                table_content = {
                    'headers': [],
                    'rows': []
                }
                
                # Miglioriamo l'estrazione di tabelle per gestire correttamente intestazioni di riga e colonna
                if 'K' in element:
                    # Prima passiamo per determinare il numero di colonne e righe
                    max_cols = 0
                    thead_rows = []
                    tbody_rows = []
                    
                    # Separa le righe di intestazione e corpo
                    for section in element['K']:
                        if section.get('S') == 'THead':
                            for row in section.get('K', []):
                                if row.get('S') == 'TR':
                                    thead_rows.append(row)
                        elif section.get('S') == 'TBody':
                            for row in section.get('K', []):
                                if row.get('S') == 'TR':
                                    tbody_rows.append(row)
                    
                    # Processa le righe di intestazione
                    for row in thead_rows:
                        header_row = []
                        for cell in row.get('K', []):
                            cell_content = process_table_cell(cell)
                            header_row.extend(cell_content)
                        if header_row:
                            table_content['headers'].append(header_row)
                            max_cols = max(max_cols, len(header_row))
                    
                    # Processa le righe di corpo
                    for row in tbody_rows:
                        data_row = []
                        has_row_header = False
                        row_header = None
                        
                        # Cerca prima un'intestazione di riga
                        for cell in row.get('K', []):
                            if cell.get('S') == 'TH':
                                has_row_header = True
                                cell_content = process_table_cell(cell)
                                if cell_content:
                                    row_header = cell_content[0]
                                break
                        
                        # Processa tutte le celle
                        for cell in row.get('K', []):
                            cell_content = process_table_cell(cell)
                            # Se è un'intestazione di riga, aggiungiamola con un indicatore
                            if cell.get('S') == 'TH' and has_row_header:
                                cell_content[0]['isRowHeader'] = True
                            data_row.extend(cell_content)
                        
                        if data_row:
                            table_content['rows'].append(data_row)
                
                results.append({
                    "tag": "Table",
                    "content": table_content
                })
            
            elif tag_type == 'Sect':
                # Estrai il contenuto direttamente dal Sect
                element_dict["text"] = ""  # Inizializza text vuoto
                
                if 'K' in element:
                    for child in element['K']:
                        child_results = extract_content(child, level + 1)
                        if child_results:
                            child_elements.extend(child_results)
                
                if child_elements:
                    element_dict["children"] = child_elements
                results.append(element_dict)
                
            elif tag_type == 'L':
                items = []
                is_ordered = False
                
                if 'K' in element:
                    for item in element.get('K', []):
                        if item.get('S') == 'LI':
                            # Estrai separatamente label e corpo dell'elemento lista
                            label = ""
                            body_text = []
                            
                            for li_child in item.get('K', []):
                                if li_child.get('S') == 'Lbl':
                                    # Estrai il bullet/numero
                                    for k in li_child.get('K', []):
                                        if isinstance(k, dict) and 'Content' in k:
                                            for content_item in k['Content']:
                                                if content_item.get('Type') == 'Text':
                                                    label += content_item.get('Text', '').strip()
                                    if label.replace('.', '').isdigit():
                                        is_ordered = True
                                        
                                elif li_child.get('S') == 'LBody':
                                    # Estrai il testo del corpo ricorsivamente preservando spazi
                                    def process_list_body(element):
                                        if isinstance(element, dict):
                                            if 'Content' in element:
                                                for content_item in element['Content']:
                                                    if content_item.get('Type') == 'Text':
                                                        text = content_item.get('Text', '')
                                                        # Aggiungi il testo senza strip() per preservare gli spazi
                                                        body_text.append(text)
                                            elif 'K' in element:
                                                for child in element['K']:
                                                    process_list_body(child)
                                    
                                    for p in li_child.get('K', []):
                                        process_list_body(p)
                                                                
                            # Combina label e body preservando gli spazi corretti
                            full_text = ''.join(body_text).strip()
                            if label and full_text:
                                items.append(f"{label} {full_text}")
                            elif full_text:
                                items.append(full_text)
                            elif label:
                                items.append(label)

                if items:
                    results.append({
                        "tag": "L",
                        "ordered": is_ordered,
                        "items": items
                    })
                return results

            else:
                # Process children first to collect nested elements
                if 'K' in element:
                    for child in element.get('K', []):
                        if not isinstance(child, dict):
                            continue
                            
                        if 'Content' in child:
                            try:
                                text_fragments = extract_text_content(child.get('Content', []))
                                if text_fragments:
                                    content.extend(text_fragments)
                            except (KeyError, AttributeError):
                                continue
                        else:
                            nested_results = extract_content(child, level + 1)
                            child_elements.extend(nested_results)
                
                # Create element with text and children
                text = ''.join(content)
                
                if text or text == '':  # Include empty strings
                    element_dict["text"] = text
                if child_elements:
                    element_dict["children"] = child_elements
                    
                results.append(element_dict)
        
        # Process siblings for Document tag
        elif 'K' in element and isinstance(element.get('K'), list):
            for child in element.get('K', []):
                if isinstance(child, dict):
                    nested_results = extract_content(child, level + 1)
                    results.extend(nested_results)
                    
    except Exception as e:
        print(f"Warning: Error processing element: {str(e)}", file=sys.stderr)
        
    return results

def process_table_cell(cell):
    """Process table cell content recursively"""
    results = []
    
    if not isinstance(cell, dict):
        return [{"tag": "P", "text": ""}]
        
    cell_type = cell.get('S', '')
    
    if cell_type in ['TD', 'TH']:
        has_content = False
        cell_result = {"tag": "P", "text": ""}
        
        # Aggiungiamo un indicatore per le celle di intestazione
        if cell_type == 'TH':
            cell_result["isHeader"] = True
        
        for k in cell.get('K', []):
            # Process nested elements
            if isinstance(k, dict):
                tag = k.get('S', '')
                if tag:
                    if tag == 'Figure':
                        # Special handling for Figure tags
                        content = {
                            "tag": "Figure",
                            "text": k.get('Alt', '') or ""
                        }
                        results.append(content)
                        has_content = True
                    else:
                        content = {"tag": tag}
                        
                        # Extract text content and nested elements
                        if 'K' in k:
                            text_fragments = []
                            nested_elements = []
                            
                            for child in k['K']:
                                if isinstance(child, dict):
                                    child_tag = child.get('S', '')
                                    if child_tag == 'Figure':
                                        # Handle nested figures
                                        nested_elements.append({
                                            "tag": "Figure",
                                            "text": child.get('Alt', '') or ""
                                        })
                                        has_content = True
                                    elif child_tag == 'Span' or child_tag == 'Link':
                                        # Handle special tags with nested content
                                        span_content = []
                                        span_children = []
                                        
                                        # Process Span's content and children
                                        for span_child in child.get('K', []):
                                            if isinstance(span_child, dict):
                                                if 'Content' in span_child:
                                                    span_texts = extract_text_content(span_child['Content'])
                                                    if span_texts:
                                                        span_content.extend(span_texts)
                                                else:
                                                    # Recursively process deeper nested elements
                                                    child_results = extract_content(span_child)
                                                    if child_results:
                                                        span_children.extend(child_results)
                                        
                                        span_text = ''.join(span_content)
                                        span_element = {
                                            "tag": child_tag,
                                            "text": span_text
                                        }
                                        
                                        if span_children:
                                            span_element["children"] = span_children
                                            
                                        nested_elements.append(span_element)
                                        has_content = True
                                    elif 'Content' in child:
                                        fragments = extract_text_content(child['Content'])
                                        text_fragments.extend(fragments)
                                    else:
                                        # Recursively process nested structures
                                        child_results = process_table_cell(child)
                                        nested_elements.extend(child_results)
                            
                            if text_fragments:
                                content["text"] = ''.join(text_fragments)
                                has_content = True
                            else:
                                content["text"] = ""
                                
                            if nested_elements:
                                content["children"] = nested_elements
                                has_content = True
                                
                        # Preserviamo l'informazione se è un'intestazione
                        if cell_type == 'TH':
                            content["isHeader"] = True
                            
                        results.append(content)
        
        # Se non è stato trovato alcun contenuto, aggiungi un elemento P vuoto (con flag se è header)
        if not results:
            if cell_type == 'TH':
                cell_result["isHeader"] = True
            results.append(cell_result)
    
    return results

def extract_text_content(content_list):
    """Extract text content from Content list"""
    text_fragments = []
    for content_item in content_list:
        if content_item.get('Type') == 'Text':
            # Add text exactly as is, without stripping
            text_fragments.append(content_item.get('Text', ''))
    return text_fragments

def extract_list_item_text(item):
    """Helper function to extract text from list items safely"""
    try:
        if item.get('S') != 'LI':
            return None

        bullet = ""
        text_fragments = []
        
        # Extract bullet and text from LI structure
        for child in item.get('K', []):
            if child.get('S') == 'Lbl':
                # Extract bullet point
                for k in child.get('K', []):
                    if isinstance(k, dict) and 'Content' in k:
                        for content_item in k['Content']:
                            if content_item.get('Type') == 'Text':
                                bullet = content_item.get('Text', '').strip()
                                
            elif child.get('S') == 'LBody':
                # Process each paragraph in LBody
                for p in child.get('K', []):
                    if isinstance(p, dict):
                        if p.get('S') == 'P':
                            # Process paragraph content preserving spaces
                            for k in p.get('K', []):
                                if isinstance(k, dict):
                                    if 'Content' in k:
                                        # Add each text fragment, including spaces
                                        for content_item in k['Content']:
                                            if content_item.get('Type') == 'Text':
                                                text_fragments.append(content_item.get('Text', ''))
                                    elif k.get('S') in ['Span', 'Link']:
                                        for span_k in k.get('K', []):
                                            if isinstance(span_k, dict) and 'Content' in span_k:
                                                for content_item in span_k['Content']:
                                                    if content_item.get('Type') == 'Text':
                                                        text_fragments.append(content_item.get('Text', ''))

        # Join all text fragments directly, preserving spaces
        text = ''.join(text_fragments).strip()
        
        # Handle different list marker formats
        if bullet:
            if bullet in ['•', '-', '*']:  # Common bullet points
                return f"{bullet} {text}" if text else bullet
            elif bullet.isdigit() or bullet.rstrip('.').isdigit():  # Numbered lists
                return f"{bullet} {text}" if text else bullet
            else:  # Other markers
                return f"{bullet} {text}" if text else bullet
        
        return text if text else None
                
    except Exception as e:
        print(f"Warning: Error extracting list item text: {str(e)}", file=sys.stderr)
        
    return None

def create_simplified_json(pdf_json, results):
    """Create simplified JSON including metadata from full JSON"""
    metadata_fields = [
        "creation_date", "mod_date", "author", "title", "subject",
        "keywords", "producer", "creator", "standard", "lang",
        "num_pages", "tagged"
    ]
    
    simplified = {
        "metadata": {
            field: pdf_json.get(field, "") for field in metadata_fields
        },
        "content": results
    }
    return simplified

def print_formatted_content(element, level=0):
    """Stampa il contenuto in modo leggibile con indentazione"""
    indent = "  " * level
    
    tag = element.get('tag', '')
    text = element.get('text', '')
    children = element.get('children', [])

    # Gestione speciale per P con figura annidata
    if tag == 'P' and len(children) == 1 and children[0].get('tag') == 'Figure':
        figure = children[0]
        print(f"{indent}{COLOR_GREEN}[P]{COLOR_RESET} > {COLOR_ORANGE}[Figure]{COLOR_RESET} {figure.get('text', '')}")
        return

    # Gestione speciale per P o H con Span/Link annidati - stampa su un'unica riga
    if (tag == 'P' or tag.startswith('H')) and children:
        child_spans = [c for c in children if c.get('tag') in ['Span', 'Link']]
        if child_spans:
            # Formatta il tag principale
            if tag == 'P':
                tag_str = f"{COLOR_GREEN}[{tag}]{COLOR_RESET}"
            elif tag.startswith('H'):
                tag_str = f"{COLOR_RED}[{tag}]{COLOR_RESET}"
            else:
                tag_str = f"[{tag}]"
                
            # Formatta ogni span/link con > sulla stessa riga
            spans_output = []
            for child in child_spans:
                child_tag = child.get('tag')
                child_text = child.get('text', '')
                if child_tag == 'Span':
                    spans_output.append(f"> [Span] {child_text}")
                elif child_tag == 'Link':
                    spans_output.append(f"> [Link] {child_text}")
            
            # Stampa l'elemento principale e i suoi figli span/link sulla stessa riga
            print(f"{indent}{tag_str} {' '.join(spans_output)}")
            
            # Stampa gli altri figli che non sono Span/Link
            other_children = [c for c in children if c.get('tag') not in ['Span', 'Link']]
            for child in other_children:
                print_formatted_content(child, level + 1)
                
            return

    # Gestione tabelle migliorata con indicazione di TH e TD
    if tag == 'Table':
        print(f"{indent}{COLOR_PURPLE}[Table]{COLOR_RESET}")
        table_content = element.get('content', {})
        
        # Ottieni le intestazioni e le righe per calcolare la larghezza di colonna ottimale
        headers = table_content.get('headers', [])
        rows = table_content.get('rows', [])
        
        # Calcola la larghezza massima per ogni colonna
        all_rows = headers + rows
        max_columns = max([len(row) for row in all_rows]) if all_rows else 0
        column_widths = [0] * max_columns
        
        # Determina la larghezza ideale per ogni colonna basata sul contenuto
        for row in all_rows:
            for i, cell in enumerate(row):
                if i < max_columns:  # Evita errori di indice
                    if isinstance(cell, dict):
                        # Calcola la lunghezza del testo visualizzato senza i codici ANSI
                        text = cell.get('text', '').strip()
                        text_length = len(text)
                        
                        # Aggiungi una lunghezza extra per indicatori di TH/TD e tag annidati
                        cell_type_tag = "[TH] > " if cell.get('isHeader', False) or cell.get('isRowHeader', False) else "[TD] > "
                        tag_length = len(cell_type_tag) + 5  # [TH] > [P] è più lungo di [P]
                        total_length = text_length + tag_length
                        
                        column_widths[i] = max(column_widths[i], min(total_length, 50))  # Limita a 50 caratteri per leggibilità
        
        # Funzione per stampare una riga formattata con larghezze colonne
        def print_table_row(row, is_header_row=False):
            cells = []
            for i, cell in enumerate(row):
                if isinstance(cell, dict):
                    # Prepara il contenuto della cella con formattazione migliorata
                    is_header = cell.get('isHeader', False) or cell.get('isRowHeader', False) or is_header_row
                    
                    # Mostra sempre il tag TH o TD appropriato
                    cell_type_tag = f"{COLOR_RED}[TH]{COLOR_RESET} > " if is_header else f"[TD] > "
                    cell_content = format_cell_content_with_type(cell, show_cell_type=False).strip()
                    
                    # Combina il tag di cella con il contenuto
                    if cell_content:
                        content = f"{cell_type_tag}{cell_content}"
                    else:
                        content = f"{cell_type_tag}{COLOR_GREEN}[Empty]{COLOR_RESET}"
                    
                    # Aggiungi padding e tronca se necessario
                    width = column_widths[i] if i < len(column_widths) else 15
                    # Non consideriamo i codici ANSI nel calcolo della lunghezza
                    visible_length = len(content.replace(COLOR_GREEN, "").replace(COLOR_RED, "").
                                         replace(COLOR_ORANGE, "").replace(COLOR_PURPLE, "").
                                         replace(COLOR_BLUE, "").replace(COLOR_RESET, ""))
                    
                    # Spazio aggiuntivo per i codici di colore
                    color_padding = len(content) - visible_length
                    padded_content = content.ljust(width + color_padding)
                    
                    cells.append(padded_content)
            
            if cells:
                print(f"{indent}    | " + " | ".join(cells) + " |")
            
        # Stampa le intestazioni di colonna
        if headers:
            print(f"{indent}  {COLOR_PURPLE}[Headers]{COLOR_RESET}")
            for row in headers:
                print_table_row(row, True)
            # Aggiungi un separatore visivo tra intestazioni e dati
            separator = []
            for width in column_widths:
                separator.append("-" * width)
            print(f"{indent}    +-" + "-+-".join(separator) + "-+")
        
        # Stampa le righe di dati, evidenziando le intestazioni di riga
        if rows:
            print(f"{indent}  {COLOR_PURPLE}[Rows]{COLOR_RESET}")
            for row in rows:
                print_table_row(row)
        
        return

    # Handle other elements
    if tag == 'Figure':
        print(f"{indent}{COLOR_ORANGE}[Figure]{COLOR_RESET} {text}")
        if children:  # Process any nested elements
            for child in children:
                print_formatted_content(child, level + 1)
        return
    elif tag == 'L':
        list_type = f"{COLOR_BLUE}[ORDERED LIST]{COLOR_RESET}" if element.get('ordered', False) else f"{COLOR_BLUE}[UNORDERED LIST]{COLOR_RESET}"
        print(f"{indent}{list_type}")
        if element.get('items'):
            if element.get('ordered', False):
                for i, item in enumerate(element.get('items'), 1):
                    if not item.startswith(str(i)):
                        print(f"{indent}  {i}. {item}")
                    else:
                        print(f"{indent}  {item}")
            else:
                for item in element.get('items'):
                    print(f"{indent}  {item}")
        return
    elif tag == 'P':
        tag_str = f"{COLOR_GREEN}[{tag}]{COLOR_RESET}"
    elif tag.startswith('H'):
        tag_str = f"{COLOR_RED}[{tag}]{COLOR_RESET}"
    else:
        tag_str = f"[{tag}]"

    # Print current element
    if text.strip():
        print(f"{indent}{tag_str} {text}")
    elif tag != 'Sect':  # Non stampare elementi Sect vuoti
        print(f"{indent}{tag_str}")
            
    # Print children
    if children:
        for child in children:
            print_formatted_content(child, level + 1)

def format_cell_content_with_type(element, level=0, show_cell_type=True) -> str:
    """Format cell content recursively including cell type (TH/TD) and nested elements"""
    if not isinstance(element, dict):
        return ""
        
    tag = element.get('tag', '')
    text = element.get('text', '').strip()
    children = element.get('children', [])
    is_header = element.get('isHeader', False) or element.get('isRowHeader', False)
    
    parts = []
    
    # Aggiungi il tag di tipo cella (TH o TD) se richiesto
    if show_cell_type:
        if is_header:
            parts.append(f"{COLOR_RED}[TH]{COLOR_RESET} > ")
        else:
            parts.append("[TD] > ")
    
    # Casi speciali per elementi annidati
    if tag == 'P' and len(children) == 1 and children[0].get('tag') == 'Figure':
        # Per P con una sola figura annidata, mostra entrambi i tag
        figure = children[0]
        figure_part = f"{COLOR_GREEN}[P]{COLOR_RESET} > {COLOR_ORANGE}[Figure]{COLOR_RESET} {figure.get('text', '')}"
        parts.append(figure_part)
        return ''.join(parts)
    
    # Aggiungi il tag dell'elemento
    if tag == 'Figure':
        parts.append(f"{COLOR_ORANGE}[{tag}]{COLOR_RESET}")
    elif tag.startswith('H'):
        parts.append(f"{COLOR_RED}[{tag}]{COLOR_RESET}")
    elif tag == 'P':
        parts.append(f"{COLOR_GREEN}[{tag}]{COLOR_RESET}")
    else:
        parts.append(f"[{tag}]")
    
    # Aggiungi il testo dell'elemento
    if text:
        parts.append(text)
    
    # Gestione speciale per tag annidati
    if children:
        # Handle Span in P or H tags - use > syntax
        child_spans = [c for c in children if c.get('tag') in ['Span', 'Link']]
        if child_spans:
            for child in child_spans:
                child_tag = child.get('tag')
                child_text = child.get('text', '').strip() 
                if child_text:
                    parts.append(f"> [{child_tag}] {child_text}")
        
        # For other nested elements, add a compact representation
        other_children = [c for c in children if c.get('tag') not in ['Span', 'Link']]
        if other_children:
            nested_tags = [f"+{c.get('tag')}" for c in other_children]
            if nested_tags:
                parts.append(f"[{' '.join(nested_tags)}]")
    
    return ' '.join(parts)

# Modifica la funzione di formato celle originale per utilizzare la nuova versione
def format_cell_content(element, level=0) -> str:
    return format_cell_content_with_type(element, level, show_cell_type=True)

def is_only_whitespace(text: str) -> bool:
    """Helper function to check if text contains only whitespace characters"""
    return bool(text and all(c in ' \t\n\r' for c in text))

def is_element_empty(element: Dict) -> bool:
    """Verifica ricorsivamente se un elemento e tutti i suoi contenuti sono vuoti"""
    if not isinstance(element, dict):
        return True
        
    # Controlla il testo diretto
    has_text = bool(element.get('text', '').strip())
    if has_text:
        return False
        
    # Controlla se è un'immagine (tag Figure)
    if element.get('tag') == 'Figure':
        return False
        
    # Controlla i figli ricorsivamente, compresi gli Span
    children = element.get('children', [])
    if children:
        return all(is_element_empty(child) for child in children)
        
    # Se non ci sono né testo diretto né figli, l'elemento è vuoto
    return True

class AccessibilityValidator:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.successes = []
        self.is_tagged = False
        
        self.check_weights = {
            'tagging': 35,          # Aumentato perché fondamentale
            'title': 20,           # Aumentato perché molto importante
            'language': 20,        # Aumentato perché molto importante
            'headings': 5,         # Ridotto perché un titolo vuoto è meno grave
            'alt_text': 4,         # Invariato
            'figures': 4,          # Invariato
            'tables': 4,           # Invariato
            'lists': 4,            # Invariato
            'empty_elements': 1,   # Ridotto al minimo perché meno importante
            'underlining': 1,      # Invariato
            'spacing': 1,          # Invariato
            'extra_spaces': 0.5,   # Ridotto perché poco rilevante
            'links': 0.5          # Ridotto perché poco rilevante
        }
        self.check_scores = {k: 0 for k in self.check_weights}
        self.empty_elements_count = {
            'paragraphs': 0,
            'table_cells': 0,
            'headings': 0,
            'spans': 0,
            'total': 0
        }

    def validate_metadata(self, metadata: Dict) -> None:
        # Check tagged status first
        tagged = metadata.get('tagged')
        if not tagged or tagged.lower() != 'true':
            self.issues.append("Document is not tagged")
            self.check_scores['tagging'] = 0
            self.is_tagged = False
        else:
            self.successes.append("Document is tagged")
            self.check_scores['tagging'] = 100
            self.is_tagged = True
            
        # Check title with clearer message
        if not metadata.get('title'):
            self.issues.append("Document metadata is missing title property")
            self.check_scores['title'] = 0
        else:
            self.successes.append("Document metadata includes title property")
            self.check_scores['title'] = 100
            
        # Check language
        lang = metadata.get('lang', '').lower()
        if not lang.startswith('it'):
            self.issues.append(f"Document language is not Italian (found: {lang})")
            self.check_scores['language'] = 0
        else:
            self.successes.append("Document language is Italian")
            self.check_scores['language'] = 100

    def validate_empty_elements(self, content: List) -> None:
        """Check for any empty elements in the document"""
        if not self.is_tagged:
            self.check_scores['empty_elements'] = 0
            return
            
        def check_element(element: Dict, path: str = "") -> None:
            tag = element.get('tag', '')
            text = element.get('text', '')
            children = element.get('children', [])
            
            current_path = f"{path}/{tag}" if path else tag
            
            # Check for empty content
            has_no_content = not text.strip() and not children
            if has_no_content:
                if tag == 'P':
                    self.empty_elements_count['paragraphs'] += 1
                    self.empty_elements_count['total'] += 1
                elif tag.startswith('H'):
                    self.empty_elements_count['headings'] += 1
                    self.empty_elements_count['total'] += 1
                elif tag == 'Span':
                    self.empty_elements_count['spans'] += 1
                    self.empty_elements_count['total'] += 1
                    
            # Special check for table cells
            if tag == 'Table':
                table_content = element.get('content', {})
                # Check both headers and rows
                for section in ['headers', 'rows']:
                    for row in table_content.get(section, []):
                        for cell in row:
                            if isinstance(cell, dict) and not cell.get('text', '').strip():
                                self.empty_elements_count['table_cells'] += 1
                                self.empty_elements_count['total'] += 1
            
            # Check children recursively
            for child in element.get('children', []):
                check_element(child, current_path)
                
        # Reset counters
        self.empty_elements_count = {k: 0 for k in self.empty_elements_count}
        
        # Check all elements
        for element in content:
            check_element(element)
            
        # ... rest of existing validate_empty_elements code ...

    def is_complex_alt_text(self, alt_text: str) -> tuple[bool, str]:
        """
        Verifica se l'alt text contiene pattern problematici
        Returns: (is_complex, reason)
        """
        import re
        
        # Verifica estensioni di file comuni
        file_ext_pattern = r'\.(png|jpe?g|gif|bmp|tiff?|pdf|docx?|xlsx?|pptx?)$'
        if re.search(file_ext_pattern, alt_text, re.IGNORECASE):
            return True, "contains file extension"

        # Verifica nomi file che contengono trattini, underscore o numeri
        complex_name_pattern = r'[-_][a-zA-Z0-9]+[-_0-9]*\.'
        if re.search(complex_name_pattern, alt_text):
            return True, "contains complex filename"
            
        # Verifica se contiene "File:" o "Image:" all'inizio
        if alt_text.startswith(("File:", "Image:")):
            return True, "starts with 'File:' or 'Image:'"

        return False, ""

    def validate_figures(self, content: List) -> None:
        """Validate figures and their alt text - checks recursively through all structures"""
        if not self.is_tagged:
            self.check_scores['figures'] = 0
            self.check_scores['alt_text'] = 0
            return
            
        figures = []
        figures_without_alt = []
        figures_with_complex_alt = []
        
        def check_figures_recursive(element: Dict, path: str = "", page_num: int = 1) -> None:
            # Check cambio pagina
            if 'Pg' in element:
                page_num = int(element['Pg'])
                
            # Process current element
            tag = element.get('tag', '')
            current_path = f"{path}/{tag}" if path else tag
            
            if tag == 'Figure':
                figure_num = len(figures) + 1
                figures.append((current_path, figure_num, page_num))
                alt_text = element.get('text', '').strip()
                if not alt_text:
                    figures_without_alt.append((current_path, figure_num, page_num))
                else:
                    is_complex, reason = self.is_complex_alt_text(alt_text)
                    if is_complex:
                        figures_with_complex_alt.append((current_path, alt_text, reason, figure_num, page_num))
            
            # Check children
            children = element.get('children', [])
            if children:
                for child in children:
                    check_figures_recursive(child, current_path, page_num)
                    
            # Special handling for table cells and other structured content
            if tag == 'Table':
                table_content = element.get('content', {})
                # Check headers
                for row in table_content.get('headers', []):
                    for cell in row:
                        check_figures_recursive(cell, f"{current_path}/header", page_num)
                # Check rows
                for row in table_content.get('rows', []):
                    for cell in row:
                        check_figures_recursive(cell, f"{current_path}/row", page_num)
        
        # Start recursive check
        for element in content:
            check_figures_recursive(element)
        
        # Update validation results
        if figures:
            if figures_without_alt:
                missing_figures = [f"Figure {num} (page {page})" for _, num, page in figures_without_alt]
                self.issues.append(f"Found {len(figures_without_alt)} figures without alt text: {', '.join(missing_figures)}")
                self.check_scores['figures'] = 50
            else:
                count = len(figures)
                self.successes.append(f"Found {count} figure{'' if count == 1 else 's'} with alternative text")
                self.check_scores['figures'] = 100

            if figures_with_complex_alt:
                for _, alt_text, reason, num, page in figures_with_complex_alt:
                    self.warnings.append(f"Figure {num} (page {page}) has problematic alt text ({reason}): '{alt_text}'")
                self.check_scores['alt_text'] = 50
            else:
                self.check_scores['alt_text'] = 100
        else:
            self.check_scores['figures'] = 0
            self.check_scores['alt_text'] = 0

    def validate_heading_structure(self, content: List) -> None:
        if not self.is_tagged:
            self.check_scores['headings'] = 0
            return
            
        headings = []
        empty_headings = []
        
        def collect_headings(element: Dict) -> None:
            tag = element.get('tag', '')
            if tag.startswith('H'):
                try:
                    level = int(tag[1:])
                    # Usa is_element_empty per verificare se il titolo è vuoto
                    if is_element_empty(element):
                        empty_headings.append(level)
                    else:
                        headings.append(level)
                except ValueError:
                    pass
            
            for child in element.get('children', []):
                collect_headings(child)
        
        for element in content:
            collect_headings(element)
        
        # Logica di scoring rivista per i titoli
        if empty_headings and not headings:
            # Se ci sono solo titoli vuoti, il punteggio deve essere molto basso
            self.issues.append(f"Found {len(empty_headings)} empty heading{'s' if len(empty_headings) > 1 else ''} (H{', H'.join(map(str, empty_headings))}) and no valid headings")
            self.check_scores['headings'] = 0
            return
        
        if empty_headings:
            # Se ci sono alcuni titoli vuoti ma anche titoli validi
            self.issues.append(f"Found {len(empty_headings)} empty heading{'s' if len(empty_headings) > 1 else ''} (H{', H'.join(map(str, empty_headings))})")
            self.check_scores['headings'] = 30  # Punteggio penalizzato ma non azzerato
            
        if not headings and not empty_headings:
            # Se non ci sono titoli affatto
            self.warnings.append("No headings found in document")
            self.check_scores['headings'] = 20
            return
            
        if headings:  # Verifichiamo la struttura solo se ci sono headings non vuoti
            # Controlla il livello del primo heading
            if headings[0] > 1:
                self.issues.append(f"First heading is H{headings[0]}, should be H1")
                self.check_scores['headings'] = max(self.check_scores['headings'], 40)
            
            # Controlla la gerarchia dei titoli
            prev_level = headings[0]
            hierarchy_issues = []
            
            for level in headings[1:]:  # Parti dal secondo titolo
                if level > prev_level + 1:
                    hierarchy_issues.append(f"H{prev_level} followed by H{level}")
                prev_level = level
            
            if hierarchy_issues:
                self.issues.append("Incorrect heading hierarchy: " + ", ".join(hierarchy_issues))
                self.check_scores['headings'] = max(self.check_scores['headings'], 50)
            
            if not any(issue for issue in self.issues if "heading" in issue.lower()):
                count = len(headings)
                self.successes.append(f"Found {count} heading{'s' if count > 1 else ''} with correct structure")
                self.check_scores['headings'] = 100

    def validate_tables(self, content: List) -> None:
        if not self.is_tagged:
            self.check_scores['tables'] = 0
            return
            
        tables = []
        tables_without_headers = []
        empty_tables = []
        tables_with_duplicate_headers = []
        tables_with_proper_headers = []
        tables_with_multiple_header_rows = []
        tables_without_data = []
        
        # Migliorata per rilevare intestazioni sia di riga che di colonna
        def is_table_completely_empty(headers, rows) -> bool:
            # Check if all headers are empty
            all_headers_empty = all(
                not (isinstance(cell, dict) and cell.get('text', '').strip() or
                     isinstance(cell, str) and cell.strip())
                for row in headers
                for cell in row
            )
            
            # Check if all rows are empty
            all_rows_empty = all(
                not (isinstance(cell, dict) and cell.get('text', '').strip() or
                     isinstance(cell, str) and cell.strip())
                for row in rows
                for cell in row
            )
            
            return all_headers_empty and all_rows_empty
        
        def has_duplicate_headers(headers) -> tuple[bool, list]:
            if not headers:
                return False, []
            
            header_texts = []
            duplicates = []
            
            for row in headers:
                row_texts = []
                for cell in row:
                    if isinstance(cell, dict):
                        text = cell.get('text', '').strip()
                    else:
                        text = str(cell).strip()
                    if text in row_texts:
                        duplicates.append(text)
                    row_texts.append(text)
                header_texts.extend(row_texts)
            
            return bool(duplicates), duplicates
        
        def is_element_empty(element: Dict) -> bool:
            """Verifica ricorsivamente se un elemento e tutti i suoi contenuti sono vuoti"""
            if not isinstance(element, dict):
                return True
                
            # Controlla il testo diretto
            has_text = bool(element.get('text', '').strip())
            if has_text:
                return False
                
            # Controlla se è un'immagine (tag Figure)
            if element.get('tag') == 'Figure':
                return False
                
            # Controlla contenuto tabella
            if element.get('tag') == 'Table':
                table_content = element.get('content', {})
                # Controlla headers e rows
                for section in ['headers', 'rows']:
                    for row in table_content.get(section, []):
                        for cell in row:
                            if not is_element_empty(cell):
                                return False
                return True
                
            # Controlla contenuto liste
            if element.get('tag') == 'L':
                items = element.get('items', [])
                return all(not item.strip() for item in items)
                
            # Controlla ricorsivamente i figli, compresi gli Span
            children = element.get('children', [])
            if children:
                return all(is_element_empty(child) for child in children)
                
            # Se non ci sono né testo diretto né figli, l'elemento è vuoto
            return True

        def is_cell_empty(cell: Dict) -> bool:
            """Controlla se una cella è completamente vuota"""
            return is_element_empty(cell)

        def count_empty_cells(table_content: Dict) -> tuple[int, List[str], List[str]]:
            """Conta le celle vuote e restituisce (count, locations, details)"""
            empty_cells = []
            empty_cells_details = []
            total_empty = 0
            
            def format_cell_content(cell):
                """Formatta i dettagli del contenuto di una cella vuota"""
                tags = []
                if isinstance(cell, dict):
                    tag = cell.get('tag', '')
                    if tag:
                        tags.append(f"{tag}")
                        if cell.get('children'):
                            for child in cell.get('children'):
                                child_tag = child.get('tag', '')
                                if child_tag:
                                    tags.append(f"{child_tag}")
                return f"[{' > '.join(tags)}]" if tags else "[empty]"
            
            # Check headers
            for i, row in enumerate(table_content.get('headers', [])):
                for j, cell in enumerate(row):
                    if is_cell_empty(cell):
                        total_empty += 1
                        location = f"header[{i}][{j}]"
                        empty_cells.append(location)
                        empty_cells_details.append(f"{location} {format_cell_content(cell)}")
            
            # Check data rows
            for i, row in enumerate(table_content.get('rows', [])):
                for j, cell in enumerate(row):
                    if is_cell_empty(cell):
                        total_empty += 1
                        location = f"row[{i}][{j}]"
                        empty_cells.append(location)
                        empty_cells_details.append(f"{location} {format_cell_content(cell)}")
            
            return total_empty, empty_cells, empty_cells_details

        def check_tables(element: Dict, path: str = "") -> None:
            tag = element.get('tag', '')
            
            if tag == 'Table':
                table_num = len(tables) + 1
                table_content = element.get('content', {})
                headers = table_content.get('headers', [])
                rows = table_content.get('rows', [])
                
                # Verifica se ci sono intestazioni di riga (celle con isHeader o isRowHeader = True)
                has_row_headers = any(
                    any(isinstance(cell, dict) and (cell.get('isHeader', False) or cell.get('isRowHeader', False)) 
                        for cell in row)
                    for row in rows
                )
                
                # First check if table is structurally empty
                if not headers and not rows:
                    empty_tables.append(f"Table {table_num}")
                    return
                # Then check if table has structure but all cells are empty
                elif is_table_completely_empty(headers, rows):
                    empty_tables.append(f"Table {table_num}")
                else:
                    tables.append(f"Table {table_num}")
                    
                    # Check if table has headers (ora considerando anche le intestazioni di riga)
                    if not headers and not has_row_headers:
                        tables_without_headers.append(f"Table {table_num}")
                    else:
                        # Check number of header rows
                        if len(headers) > 1:
                            tables_with_multiple_header_rows.append((f"Table {table_num}", len(headers)))
                        
                        # Check for duplicate headers
                        has_duplicates, duplicate_values = has_duplicate_headers(headers)
                        if has_duplicates:
                            tables_with_duplicate_headers.append((f"Table {table_num}", duplicate_values))
                        else:
                            tables_with_proper_headers.append(f"Table {table_num}")
                    
                    # Check if table has data rows
                    if not rows:
                        tables_without_data.append(f"Table {table_num}")
                
                # Check for empty cells with improved detection
                empty_count, empty_locations, empty_details = count_empty_cells(table_content)
                if empty_count > 0:
                    if empty_count == 1:
                        self.warnings.append(f"Table {table_num} has 1 empty cell at: {empty_details[0]}")
                    else:
                        self.warnings.append(f"Table {table_num} has {empty_count} empty cells at: {', '.join(empty_details)}")
            
            # Check children
            for child in element.get('children', []):
                check_tables(child)
        
        for element in content:
            check_tables(element)
        
        # Report issues and warnings
        if empty_tables:
            self.issues.append(f"Found empty tables: {', '.join(empty_tables)}")
        
        if tables:  # Solo se ci sono tabelle non vuote
            # Issues per tabelle senza header o senza dati
            if tables_without_headers:
                self.issues.append(f"Found tables without headers: {', '.join(tables_without_headers)}")
            if tables_without_data:
                self.issues.append(f"Found tables without data rows: {', '.join(tables_without_data)}")
            
            # Warning per tabelle con più righe di intestazione
            for table_id, num_rows in tables_with_multiple_header_rows:
                self.warnings.append(f"{table_id} has {num_rows} header rows, consider using a single header row")
            
            # Report successo per ogni tabella corretta individualmente
            for table_id in tables_with_proper_headers:
                if (not any(table_id == t[0] for t in tables_with_multiple_header_rows) and
                    table_id not in tables_without_data):
                    self.successes.append(f"{table_id} has proper header tags")
                
            # Warning per contenuti duplicati
            if tables_with_duplicate_headers:
                for table_id, duplicates in tables_with_duplicate_headers:
                    self.warnings.append(f"{table_id} has duplicate headers: {', '.join(duplicates)}")
        
        if not (empty_tables or tables_without_headers or tables_without_data):
            self.check_scores['tables'] = 100
        else:
            self.check_scores['tables'] = 50

    def validate_possible_unordered_lists(self, content: List) -> None:
        """Check for consecutive paragraphs starting with '-' that might be unordered lists"""
        if not self.is_tagged:
            self.check_scores['lists'] = 0
            return
            
        def find_consecutive_dash_paragraphs(elements: List, path: str = "") -> List[List[str]]:
            sequences = []
            current_sequence = []
            
            for element in elements:
                if element['tag'] == 'P':
                    text = element.get('text', '').strip()
                    if text.startswith('-'):
                        current_sequence.append(text)
                    else:
                        if len(current_sequence) >= 2:
                            sequences.append(current_sequence.copy())
                        current_sequence = []
                
                # Check children recursively
                if element.get('children'):
                    nested_sequences = find_consecutive_dash_paragraphs(element['children'])
                    sequences.extend(nested_sequences)
            
            # Add last sequence if it exists
            if len(current_sequence) >= 2:
                sequences.append(current_sequence)
                
            return sequences
        
        sequences = find_consecutive_dash_paragraphs(content)
        
        if sequences:
            for sequence in sequences:
                self.warnings.append(
                    f"Found sequence of {len(sequence)} paragraphs that might form an unordered list"
                )
            self.check_scores['lists'] = 50
        else:
            self.check_scores['lists'] = 100

    def validate_possible_ordered_lists(self, content: List) -> None:
        """Check for consecutive paragraphs starting with sequential numbers that might be ordered lists"""
        if not self.is_tagged:
            self.check_scores['lists'] = 0
            return
            
        def find_consecutive_numbered_paragraphs(elements: List, path: str = "") -> List[List[str]]:
            sequences = []
            current_sequence = []
            
            def extract_leading_number(text: str) -> tuple[bool, int]:
                """Extract leading number from text (handles formats like '1.', '1)', '1 ')"""
                import re
                match = re.match(r'^(\d+)[.). ]', text)
                if match:
                    return True, int(match.group(1))
                return False, 0
            
            for element in elements:
                current_path = f"{path}/{element['tag']}" if path else element['tag']
                
                if element['tag'] == 'P':
                    text = element.get('text', '').strip()
                    is_numbered, number = extract_leading_number(text)
                    
                    if is_numbered:
                        if not current_sequence or number == current_sequence[-1][2] + 1:
                            current_sequence.append((current_path, text, number))
                        else:
                            if len(current_sequence) >= 2:
                                sequences.append(current_sequence.copy())
                            current_sequence = []
                            if number == 1:
                                current_sequence.append((current_path, text, number))
                    else:
                        if len(current_sequence) >= 2:
                            sequences.append(current_sequence.copy())
                        current_sequence = []
                
                # Check children recursively
                if element.get('children'):
                    nested_sequences = find_consecutive_numbered_paragraphs(element.get('children'), current_path)
                    sequences.extend(nested_sequences)
            
            # Add last sequence if it exists
            if len(current_sequence) >= 2:
                sequences.append(current_sequence)
                
            return sequences
        
        sequences = find_consecutive_numbered_paragraphs(content)
        
        if sequences:
            for sequence in sequences:
                numbers = [str(p[2]) for p in sequence]
                self.warnings.append(
                    f"Found sequence of {len(numbers)} numbered paragraphs ({', '.join(numbers)}) that might form an ordered list"
                )
            self.check_scores['lists'] = 50
        else:
            self.check_scores['lists'] = 100

    def validate_misused_unordered_lists(self, content: List) -> None:
        """Check for unordered lists containing consecutive numbered items"""
        if not self.is_tagged:
            self.check_scores['lists'] = 0
            return
            
        def extract_leading_number(text: str) -> tuple[bool, int]:
            """Extract number from text even after bullet points"""
            import re
            # Prima rimuovi eventuali bullet points (•, -, *)
            text = re.sub(r'^[•\-*]\s*', '', text.strip())
            # Poi cerca il numero
            match = re.match(r'^(\d+)[.). ]', text)
            if match:
                return True, int(match.group(1))
            return False, 0
        
        def check_list_items(element: Dict, path: str = "") -> None:
            tag = element.get('tag', '')
            current_path = f"{path}/{tag}" if path else tag
            
            if tag == 'L' and not element.get('ordered', False):  # Solo liste non ordinate
                items = element.get('items', [])
                if items:
                    current_sequence = []
                    
                    for item in items:
                        is_numbered, number = extract_leading_number(item)
                        if is_numbered:
                            if not current_sequence or number == current_sequence[-1][1] + 1:
                                current_sequence.append((item, number))
                            else:
                                if len(current_sequence) >= 2:
                                    numbers = [str(item[1]) for item in current_sequence]
                                    self.warnings.append(
                                        f"Found consecutive items numbered {', '.join(numbers)} in unordered list at: {current_path}"
                                    )
                                current_sequence = [(item, number)] if number == 1 else []
                    
                    # Check last sequence
                    if len(current_sequence) >= 2:
                        numbers = [str(item[1]) for item in current_sequence]
                        self.warnings.append(
                            f"Found consecutive items numbered {', '.join(numbers)} in unordered list at: {current_path}"
                        )
            
            # Check children recursively
            for child in element.get('children', []):
                check_list_items(child, current_path)
        
        for element in content:
            check_list_items(element)
        
        if not any(self.warnings):
            self.check_scores['lists'] = 100
        else:
            self.check_scores['lists'] = 50

    def validate_excessive_underscores(self, content: List) -> None:
        """Check recursively for excessive consecutive underscores that might be used for underlining"""
        def check_underscores(text: str) -> tuple[bool, int]:
            """Returns (has_excessive_underscores, count)"""
            import re
            # Cerca sequenze di 4 o più underscore
            pattern = r'_{4,}'
            match = re.search(pattern, text)
            if match:
                return True, len(match.group(0))
            return False, 0
            
        def check_element(element: Dict, path: str = "") -> None:
            current_path = f"{path}/{element['tag']}" if path else element['tag']
            
            # Controlla il testo dell'elemento corrente
            if 'text' in element:
                text = element.get('text', '')
                has_underscores, count = check_underscores(text)
                if has_underscores:
                    self.warnings.append(f"Found {count} consecutive underscores in {current_path} - might be attempting to create underlining")
            
            # Controlla i figli
            for child in element.get('children', []):
                check_element(child, current_path)
            
            # Per le tabelle, controlla le celle
            if element.get('tag') == 'Table':
                table_content = element.get('content', {})
                # Controlla headers
                for i, row in enumerate(table_content.get('headers', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            has_underscores, count = check_underscores(text)
                            if has_underscores:
                                self.warnings.append(f"Found {count} consecutive underscores in {current_path}/header[{i}][{j}] - might be attempting to create underlining")
                
                # Controlla rows
                for i, row in enumerate(table_content.get('rows', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            has_underscores, count = check_underscores(text)
                            if has_underscores:
                                self.warnings.append(f"Found {count} consecutive underscores in {current_path}/row[{i}][{j}] - might be attempting to create underlining")
            
            # Per le liste, controlla gli items
            if element.get('tag') == 'L':
                for i, item in enumerate(element.get('items', [])):
                    has_underscores, count = check_underscores(item)
                    if has_underscores:
                        self.warnings.append(f"Found {count} consecutive underscores in {current_path}/item[{i}] - might be attempting to create underlining")
                
        for element in content:
            check_element(element)
        
        if not any(self.warnings):
            self.check_scores['underlining'] = 100
        else:
            self.check_scores['underlining'] = 50

    def validate_spaced_capitals(self, content: List) -> None:
        """Check for words written with spaced capital letters like 'C I T T À'"""
        import re
        
        def is_spaced_capitals(text: str) -> bool:
            # Trova sequenze di lettere maiuscole separate da spazi dove ogni lettera è isolata
            # Es: "C I T T À" match, "CITTÀ" no match, "DETERMINA NOMINA" no match
            pattern = r'(?:^|\s)([A-ZÀÈÌÒÙ](?:\s+[A-ZÀÈÌÒÙ]){2,})(?:\s|$)'
            matches = re.finditer(pattern, text)
            spaced_words = []
            
            for match in matches:
                # Verifica che non ci siano lettere consecutive senza spazio
                word = match.group(1)
                if all(c == ' ' or (c.isupper() and c.isalpha()) for c in word):
                    spaced_words.append(word.strip())
                    
            return spaced_words
            
        def check_element(element: Dict, path: str = "") -> None:
            current_path = f"{path}/{element['tag']}" if path else element['tag']
            
            # Controlla il testo dell'elemento corrente
            if 'text' in element:
                text = element.get('text', '')
                spaced_words = is_spaced_capitals(text)
                if spaced_words:
                    for word in spaced_words:
                        self.warnings.append(f"Found spaced capital letters in {current_path}: '{word}'")
            
            # Controlla i figli
            for child in element.get('children', []):
                check_element(child, current_path)
            
            # Per le tabelle, controlla le celle
            if element.get('tag') == 'Table':
                table_content = element.get('content', {})
                # Controlla headers
                for i, row in enumerate(table_content.get('headers', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            spaced_words = is_spaced_capitals(text)
                            if spaced_words:
                                for word in spaced_words:
                                    self.warnings.append(f"Found spaced capital letters in {current_path}/header[{i}][{j}]: '{word}'")
                
                # Controlla rows
                for i, row in enumerate(table_content.get('rows', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            spaced_words = is_spaced_capitals(text)
                            if spaced_words:
                                for word in spaced_words:
                                    self.warnings.append(f"Found spaced capital letters in {current_path}/row[{i}][{j}]: '{word}'")
            
            # Per le liste, controlla gli items
            if element.get('tag') == 'L':
                for i, item in enumerate(element.get('items', [])):
                    spaced_words = is_spaced_capitals(item)
                    if spaced_words:
                        for word in spaced_words:
                            self.warnings.append(f"Found spaced capital letters in {current_path}/item[{i}]: '{word}'")
                
        for element in content:
            check_element(element)
        
        if not any(self.warnings):
            self.check_scores['spacing'] = 100
        else:
            self.check_scores['spacing'] = 50

    def validate_extra_spaces(self, content: List) -> None:
        """Check for excessive spaces that might be used for layout purposes"""
        import re
        
        def check_spaces(text: str) -> List[tuple[str, int]]:
            """Returns list of (space_sequence, count) for suspicious spaces"""
            issues = []
            
            # Cerca sequenze di 3 o più spazi non a inizio/fine riga
            for match in re.finditer(r'(?<!^)\s{3,}(?!$)', text):
                space_seq = match.group()
                issues.append((space_seq, len(space_seq)))
            
            # Cerca tabulazioni multiple
            for match in re.finditer(r'\t{2,}', text):
                tab_seq = match.group()
                issues.append((tab_seq, len(tab_seq)))
            
            return issues
            
        def check_element(element: Dict, path: str = "") -> None:
            current_path = f"{path}/{element['tag']}" if path else element['tag']
            
            # Controlla il testo dell'elemento
            if 'text' in element:
                text = element.get('text', '')
                space_issues = check_spaces(text)
                if space_issues:
                    for space_seq, count in space_issues:
                        self.warnings.append(
                            f"Found {count} consecutive spaces in {current_path} - might be attempting layout with spaces"
                        )
            
            # Controlla i figli
            for child in element.get('children', []):
                check_element(child, current_path)
            
            # Controlli speciali per tabelle
            if element.get('tag') == 'Table':
                table_content = element.get('content', {})
                # Controlla headers
                for i, row in enumerate(table_content.get('headers', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            space_issues = check_spaces(text)
                            if space_issues:
                                for space_seq, count in space_issues:
                                    self.warnings.append(
                                        f"Found {count} consecutive spaces in {current_path}/header[{i}][{j}]"
                                    )
                
                # Controlla rows
                for i, row in enumerate(table_content.get('rows', [])):
                    for j, cell in enumerate(row):
                        if isinstance(cell, dict):
                            text = cell.get('text', '')
                            space_issues = check_spaces(text)
                            if space_issues:
                                for space_seq, count in space_issues:
                                    self.warnings.append(
                                        f"Found {count} consecutive spaces in {current_path}/row[{i}][{j}]"
                                    )
            
            # Controlli speciali per liste
            if element.get('tag') == 'L':
                for i, item in enumerate(element.get('items', [])):
                    space_issues = check_spaces(item)
                    if space_issues:
                        for space_seq, count in space_issues:
                            self.warnings.append(
                                f"Found {count} consecutive spaces in {current_path}/item[{i}]"
                            )
                
        for element in content:
            check_element(element)
        
        if not any(self.warnings):
            self.check_scores['extra_spaces'] = 100
        else:
            extra_spaces_count = sum(1 for w in self.warnings if "consecutive spaces" in w)
            if extra_spaces_count > 10:
                self.check_scores['extra_spaces'] = 0  # Molti problemi di spaziatura
            else:
                self.check_scores['extra_spaces'] = 50  # Alcuni problemi di spaziatura

    def validate_links(self, content: List) -> None:
        """Check for non-descriptive or raw URLs in links"""
        if not self.is_tagged:
            self.check_scores['links'] = 0
            return
            
        problematic_links = []
        
        def is_problematic_link(text: str) -> tuple[bool, str]:
            """Check if link text is problematic, excluding email addresses and institutional domains"""
            import re
            
            text = text.strip().lower()
            
            # Skip check for complete email addresses
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', text):
                return False, ""
                
            # Skip check for partial email/institutional domains
            if text.endswith(('.gov.it', '.comune.it', '.it.it', '.pec.it', 
                             'pec.comune.it', '@pec.comune.it', '@comune.it')):
                return False, ""
            
            # Common problematic patterns
            patterns = {
                r'^https?://': "starts with http:// or https://",
                r'^www\.': "starts with www.",
                r'^click here$|^here$|^link$': "non-descriptive text",
                r'^[0-9]+$': "contains only numbers"
            }
            
            for pattern, reason in patterns.items():
                if re.search(pattern, text):
                    return True, reason
                    
            return False, ""
            
        def check_links_recursive(element: Dict, path: str = "", page_num: int = 1) -> None:
            # Track page numbers
            if 'Pg' in element:
                page_num = int(element['Pg'])
                
            tag = element.get('tag', '')
            current_path = f"{path}/{tag}" if path else tag
            
            # Check if element is a link
            if tag == 'Link':
                link_text = element.get('text', '').strip()
                if link_text:
                    is_bad, reason = is_problematic_link(link_text)
                    if is_bad:
                        problematic_links.append((current_path, link_text, reason, page_num))
            
            # Check children recursively
            children = element.get('children', [])
            if children:
                for child in children:
                    check_links_recursive(child, current_path, page_num)
                    
            # Special handling for table cells
            if tag == 'Table':
                table_content = element.get('content', {})
                # Check headers
                for row in table_content.get('headers', []):
                    for cell in row:
                        check_links_recursive(cell, f"{current_path}/header", page_num)
                # Check rows
                for row in table_content.get('rows', []):
                    for cell in row:
                        check_links_recursive(cell, f"{current_path}/row", page_num)
        
        # Start recursive check
        for element in content:
            check_links_recursive(element)
            
        # Update validation results
        if problematic_links:
            for path, text, reason, page in problematic_links:
                self.warnings.append(f"Non-descriptive or raw URL link on page {page}: '{text}' ({reason})")
            self.check_scores['links'] = 50
        else:
            self.check_scores['links'] = 100

    def calculate_weighted_score(self) -> float:
        """Calcola il punteggio pesato di accessibilità"""
        # Se non ci sono issues né warnings, il punteggio è 100
        if not self.issues and not self.warnings and not any(value > 0 for value in self.empty_elements_count.values()):
            return 100.00
            
        # Altrimenti calcola il punteggio pesato
        total_weight = sum(self.check_weights.values())
        weighted_sum = sum(
            self.check_weights[check] * self.check_scores[check]
            for check in self.check_weights
        )
        return round(weighted_sum / total_weight, 2)

    def generate_json_report(self) -> Dict:
        return {
            "validation_results": {
                "issues": self.issues,
                "warnings": self.warnings,
                "successes": self.successes,
                "weighted_score": self.calculate_weighted_score(),
                "detailed_scores": {
                    check: score for check, score in self.check_scores.items()
                }
            }
        }

    def print_console_report(self) -> None:
        print("\n📖 Accessibility Validation Report\n")
        
        # Print empty elements count first
        print("🔍 Empty Elements Count:")
        print(f"  • Total empty elements: {self.empty_elements_count['total']}")
        if self.empty_elements_count['paragraphs'] > 0:
            print(f"  • Empty paragraphs: {self.empty_elements_count['paragraphs']}")
        if self.empty_elements_count['table_cells'] > 0:
            print(f"  • Empty table cells: {self.empty_elements_count['table_cells']}")
        if self.empty_elements_count['headings'] > 0:
            print(f"  • Empty headings: {self.empty_elements_count['headings']}")
        if self.empty_elements_count['spans'] > 0:
            print(f"  • Empty spans: {self.empty_elements_count['spans']}")
        print()
        
        if self.successes:
            print("✅ Successes:")
            for success in self.successes:
                print(f"  • {success}")
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.issues:
            print("\n❌ Issues:")
            for issue in self.issues:
                print(f"  • {issue}")
        
        # Print summary with weighted score
        total = len(self.successes) + len(self.warnings) + len(self.issues)
        weighted_score = self.calculate_weighted_score()
        
        print(f"\n📊 Summary:")
        print(f"  • Total checks: {total}")
        print(f"  • Successes: {len(self.successes)} ✅")
        print(f"  • Warnings: {len(self.warnings)} ⚠️")
        print(f"  • Issues: {len(self.issues)} ❌")
        print(f"  • Weighted Accessibility Score: {weighted_score}%")
        
        # Overall assessment
        if weighted_score >= 90:
            print("\n🎉 Excellent! Document has very good accessibility.")
        elif weighted_score >= 70:
            print("\n👍 Good! Document has decent accessibility but could be improved.")
        elif weighted_score >= 50:
            print("\n⚠️  Fair. Document needs accessibility improvements.")
        else:
            print("\n❌ Poor. Document has serious accessibility issues.")

def analyze_pdf(pdf_path: str, options: dict) -> None:
    """
    Analyze a PDF file with configurable outputs
    """
    try:
        # Setup output directory
        output_dir = Path(options['output_dir']) if options['output_dir'] else Path(pdf_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        pdf_name = Path(pdf_path).stem

        # Show conversion message only if saving JSON outputs
        if (options['save_full'] or options['save_simple']) and not options['quiet']:
            print("🔄 Converting PDF to JSON structure...", file=sys.stderr)
        
        # Convert PDF to JSON
        pdf_json = pdf_to_json(pdf_path)
        
        # Extract and simplify content
        if 'StructTreeRoot' not in pdf_json:
            if not options['quiet']:
                print("⚠️  Warning: No structure tree found in PDF", file=sys.stderr)
            results = []
        else:
            results = extract_content(pdf_json['StructTreeRoot'])
        
        # Create simplified JSON
        simplified_json = create_simplified_json(pdf_json, results)
        
        # Save full JSON if requested
        if options['save_full']:
            full_path = output_dir / f"{pdf_name}_full.json"
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(pdf_json, f, indent=2, ensure_ascii=False)
            if not options['quiet']:
                print(f"💾 Full JSON saved to: {full_path}")

        # Save simplified JSON if requested
        if options['save_simple']:
            simplified_path = output_dir / f"{pdf_name}_simplified.json"
            with open(simplified_path, 'w', encoding='utf-8') as f:
                json.dump(simplified_json, f, indent=2, ensure_ascii=False)
            if not options['quiet']:
                print(f"💾 Simplified JSON saved to: {simplified_path}")

        # Show document structure if requested
        if options['show_structure']:
            print("\n📄 Document Structure:")
            print("Note: Colors are used to highlight different tag types and do not indicate errors:")
            print(f"  {COLOR_GREEN}[P]{COLOR_RESET}: Paragraphs")
            print(f"  {COLOR_RED}[H1-H6]{COLOR_RESET}: Headings")
            print(f"  {COLOR_ORANGE}[Figure]{COLOR_RESET}: Images")
            print(f"  {COLOR_PURPLE}[Table]{COLOR_RESET}: Tables")
            print(f"  {COLOR_BLUE}[List]{COLOR_RESET}: Lists")
            print("-" * 40)
            for element in simplified_json.get('content', []):
                print_formatted_content(element)
            print("-" * 40)

        # Run validation if requested
        if options['save_report'] or options['show_validation']:
            if not options['quiet']:
                print("\n🔍 Running accessibility validation...")
            
            validator = AccessibilityValidator()
            validator.validate_metadata(simplified_json.get('metadata', {}))
            validator.validate_empty_elements(simplified_json.get('content', []))
            validator.validate_figures(simplified_json.get('content', []))
            validator.validate_heading_structure(simplified_json.get('content', []))
            validator.validate_tables(simplified_json.get('content', []))  # Add table validation
            validator.validate_possible_unordered_lists(simplified_json.get('content', []))  # Add this
            validator.validate_possible_ordered_lists(simplified_json.get('content', []))    # Add this
            validator.validate_misused_unordered_lists(simplified_json.get('content', []))  # Add this
            # Aggiungi i nuovi validatori
            validator.validate_excessive_underscores(simplified_json.get('content', []))
            validator.validate_spaced_capitals(simplified_json.get('content', []))
            validator.validate_extra_spaces(simplified_json.get('content', []))
            validator.validate_links(simplified_json.get('content', []))  # Add link validation
            
            # Show validation results if requested
            if options['show_validation']:
                validator.print_console_report()
            
            # Save validation report if requested
            if options['save_report']:
                report_path = output_dir / f"{pdf_name}_validation_report.json"
                with open(report_path, 'w', encoding='utf-8') as f:
                    json.dump(validator.generate_json_report(), f, indent=2)
                if not options['quiet']:
                    print(f"\n💾 Validation report saved to: {report_path}")
        
        if not options['quiet']:
            print("\n✨ Analysis complete!")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def download_pdf(url: str) -> Path:
    """Download a PDF file from URL and save it to a temporary file"""
    try:
        # Validate URL
        parsed = urllib.parse.urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError("Invalid URL")

        # Create temporary file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        tmp_path = Path(tmp.name)

        # Download file
        urllib.request.urlretrieve(url, tmp_path)
        
        return tmp_path

    except Exception as e:
        raise Exception(f"Failed to download PDF: {str(e)}")

def is_url(path: str) -> bool:
    """Check if the given path is a URL"""
    try:
        parsed = urllib.parse.urlparse(path)
        return all([parsed.scheme, parsed.netloc])
    except:
        return False

def main():
    parser = argparse.ArgumentParser(
        description='PDF Analysis Tool: Convert to JSON and validate accessibility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic usage (shows full analysis by default)
  avalpdf document.pdf
  
  Analyze remote PDF via URL
  avalpdf https://example.com/document.pdf
  
  Save reports to specific directory
  avalpdf document.pdf -o /path/to/output --report --simple
  
  Save all files without console output
  avalpdf document.pdf --full --simple --report --quiet
"""
    )
    
    parser.add_argument('input', help='Input PDF file or URL')
    parser.add_argument('--output-dir', '-o', help='Output directory for JSON files')
    
    # File output options
    parser.add_argument('--full', action='store_true', help='Save full JSON output')
    parser.add_argument('--simple', action='store_true', help='Save simplified JSON output')
    parser.add_argument('--report', action='store_true', help='Save validation report')
    
    # Display options
    parser.add_argument('--show-structure', action='store_true', help='Show document structure in console')
    parser.add_argument('--show-validation', action='store_true', help='Show validation results in console')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress all console output except errors')
    
    args = parser.parse_args()
    
    try:
        # Handle URL input
        if is_url(args.input):
            if not args.quiet:
                print("📥 Connecting to remote source...", file=sys.stderr)
            input_path = download_pdf(args.input)
            cleanup_needed = True
        else:
            # Handle local file
            input_path = Path(args.input)
            cleanup_needed = False

        if not input_path.is_file():
            print(f"❌ Error: Input file '{args.input}' does not exist", file=sys.stderr)
            sys.exit(1)
        
        # If no display options specified, enable both structure and validation display
        show_structure = args.show_structure
        show_validation = args.show_validation
        if not any([args.show_structure, args.show_validation, args.quiet]):
            show_structure = True
            show_validation = True
        
        # Prepare options dictionary
        options = {
            'output_dir': args.output_dir,
            'save_full': args.full,
            'save_simple': args.simple,
            'save_report': args.report,
            'show_structure': show_structure,
            'show_validation': show_validation,
            'quiet': args.quiet
        }
        
        analyze_pdf(str(input_path), options)

        # Cleanup temporary file if needed
        if cleanup_needed:
            input_path.unlink()
            
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

