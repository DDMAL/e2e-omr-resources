import os
import xml.etree.ElementTree as ET

def update_clef_line(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mei"):
                file_path = os.path.join(root, file)
                tree = ET.parse(file_path)
                root_element = tree.getroot()
                
                # Find all staffDef elements and update clef.line
                for staff_def in root_element.findall(".//{http://www.music-encoding.org/ns/mei}staffDef"):
                    if staff_def.get("clef.line") == "3":
                        staff_def.set("clef.line", "4")
                
                # Write the updated XML back to the file
                tree.write(file_path, encoding='utf-8', xml_declaration=True)

# Update the directory path as needed
directory_path = "/Users/kyriebouressa/Documents/e2e-omr-resources/resulting_mei_files/MS73/Ready for Neon"
update_clef_line(directory_path)
