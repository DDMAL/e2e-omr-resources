import lxml.etree as ET

# Register the MEI namespace with the prefix "mei"
#ET.register_namespace("", "http://www.music-encoding.org/ns/mei")

def main(filename):
    """
    Modifies an MEI file by updating the octave values of nc elements
    based on the presence of a clef element with shape="C".

    Parameters:
    filename (str): The path to the MEI file to be modified

    Returns:
    None

    The function parses the MEI file, iterates over its elements, and
    checks for clef elements with shape="C". When such an element is found,
    it sets a flag to True. Then, it iterates over the nc elements and
    increments their octave values by 1 if the flag is True. Finally,
    it writes the modified XML tree to a new file with the same name
    but with "NEW" appended.
    """
    # Parse the XML file using ElementTree
    tree = ET.parse(filename)
    root = tree.getroot()

    # Initialize a flag to track whether we've found a clef element with shape="C"
    flag = False

    # Iterate over all elements in the XML tree
    for child in root.iter("*"):
        child.tag = ET.QName(child).localname
        # Check if the current element is a clef element
        if child.tag.endswith("clef"):
            # Reset the flag
            flag = False
            
            # Check if the "shape" attribute has the value "C"
            # If so, set flag to True and add or update the "oct" attribute to "4"
            for attr, value in child.attrib.items():
                
                if attr.endswith("shape") and value == "C":
                    flag = True                   
                    child.attrib["dis"] = "8"
                    child.attrib["dis.place"] = "above"
                    
                    break

        # Check if the current element is an nc element
        if child.tag.endswith("nc"):
            
            for attr, value in child.attrib.items():
                
                # Increment the oct value by 1 if flag is true
                if attr.endswith("oct") and flag:    
                    oct = int(value) + 1
                    child.attrib[attr] = str(oct)
                    break


    # Create a new ElementTree instance with the modified root element
    new_tree = ET.ElementTree(root)

    # Write the modified XML tree to a new file with the same name but with "NEW" appended
    new_tree.write(filename[:-4] + "NEW.mei", encoding="utf8", xml_declaration=True)
