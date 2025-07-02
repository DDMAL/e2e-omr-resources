import xml.etree.ElementTree as ET
import re

def register_namespace():
    ET.register_namespace('', 'http://www.music-encoding.org/ns/mei')

def get_original_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        header_lines = []
        for _ in range(3):  # Get XML declaration and schema declarations only
            line = f.readline()
            if line.strip():
                header_lines.append(line)
        return header_lines

def get_mei_version(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'meiversion="([^"]+)"', content)
        return match.group(1) if match else "5.0"

def write_with_original_format(tree, file_path, original_headers, mei_version):
    root = tree.getroot()
    root.set('meiversion', mei_version)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        # Write XML and schema declarations
        for header in original_headers:
            f.write(header)
            
        # Write the modified tree, but format the mei element opening properly so it doesn't repeat itself again. more. and more. and more.
        xml_string = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
        # Replace the mei element opening to match original formatting
        xml_string = xml_string.replace('<mei', '<mei\n    ')
        f.write(xml_string)

def update_clef_line(file_path):
    register_namespace()
    original_headers = get_original_header(file_path)
    mei_version = get_mei_version(file_path)

    tree = ET.parse(file_path)
    root_element = tree.getroot()
    in_c_clef = False
    changes_made = 0

    ns = '{http://www.music-encoding.org/ns/mei}'
    
    # Find all layer elements
    for layer in root_element.findall(f'.//{ns}layer'):
        in_c_clef = False
        
        # Process each element in order
        for elem in layer.iter():
            if elem.tag == f'{ns}clef':
                if elem.get('shape') == 'C':
                    in_c_clef = True
                    print(f"Found C clef at {elem.get('xml:id') or elem.get('facs', 'Unknown location')}")
                else:
                    in_c_clef = False
            
            if in_c_clef and elem.tag == f'{ns}nc' and elem.get('oct'):
                current_oct = int(elem.get('oct'))
                elem.set('oct', str(current_oct + 1))
                changes_made += 1
                print(f"Updated octave from {current_oct} to {current_oct + 1} at {elem.get('xml:id')}")

    print(f"\nTotal octave changes made: {changes_made}")
    write_with_original_format(tree, file_path + '.updated', original_headers, mei_version)

file_path = "/Users/ekaterina/Documents/e2e-omr-resources/resulting_mei_files/Einsiedeln/reviewed_once/CH-E_611_100v.mei"
update_clef_line(file_path)