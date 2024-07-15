import os

"""
Renames MEI files in the current directory to remove the "NEW" prefix.

This script iterates over all files in the current directory, checks if the
file is an MEI file with the "NEW" prefixb and renames it to remove the "NEW" prefix.
"""

for filename in os.listdir("."):
    # Check if the file is an MEI file with the "NEW" prefix
    if filename.endswith("NEW.mei"):
        # Create a new filename without the "NEW" prefix
        new_filename = filename.replace("NEW", "")
        
        # Rename the file
        os.rename(filename, new_filename)