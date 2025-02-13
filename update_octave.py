import xml.etree.ElementTree as ET
import re

def register_namespace():
    # Register the default MEI namespace
    ET.register_namespace('', 'http://www.music-encoding.org/ns/mei')

def get_original_header(file_path):
    # Read the first few lines to get the XML declaration and processing instructions; MEI header
    with open(file_path, 'r', encoding='utf-8') as f: #keep empty lines
        header_lines = []
        for line in f:
            header_lines.append(line)
            if '</mei>' in line: #stop reading after mei element
                break
        return header_lines

def get_mei_version(file_path):
    # Get the MEI version from the MEI header/og MEI attribute
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'meiversion="([^"]+)"', content)
        return match.group(1) if match else "5.0" #default if nothing is found

def write_with_original_format(tree, file_path, original_headers, mei_version):
    root = tree.getroot()
    root.set('meiversion', mei_version)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(original_headers)

        # Write the XML tree to a string first
        xml_string = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
        f.write(xml_string)  # Then write the string to the file

def update_clef_line(file_path):
    register_namespace()  # Register namespace before parsing
    # get original headers and mei version
    original_headers = get_original_header(file_path)
    mei_version = get_mei_version(file_path)

    tree = ET.parse(file_path)
    root_element = tree.getroot()
    in_c_clef = False
    changes_made = 0
    
    for elem in root_element.iter():
        if elem.tag == '{http://www.music-encoding.org/ns/mei}clef': #might as well be precise, instead of '('}clef'):' :D
            if elem.get('shape') == 'C':
                in_c_clef = True
                elem_id = elem.get('xml:id') or elem.get('facs', 'Unknown location')
                print("Found C clef at {}".format(elem_id))
            else:
                in_c_clef = False
        
        if in_c_clef and elem.get('oct'):
            current_oct = int(elem.get('oct'))
            elem.set('oct', str(current_oct + 1))
            changes_made += 1
            elem_id = elem.get('xml:id') or elem.get('facs', 'Unknown location')
            print("Updated octave from {} to {} at {}".format(current_oct, current_oct + 1, elem_id))

    print("\nTotal octave changes made: {}".format(changes_made))
    write_with_original_format(tree, file_path + '.updated', original_headers, mei_version)

file_path = "/Users/ekaterina/Documents/e2e-omr-resources/resulting_mei_files/Einsiedeln/reviewed_once/CH-E_611_100r.mei"
update_clef_line(file_path)