import os
import custupdate

"""
Updates MEI files in the current directory by incrementing octave values
based on the presence of a clef element with shape="C".

This script iterates over all files in the current directory, checks if the
file is an MEI file (not already updated) and updates it using the
octupdate module. It then prints a message indicating that the file
has been updated.
"""

for mefile in os.listdir("."):
    # Get the filename as a string
    filename = os.fsdecode(mefile)
    
    # Check if the file is an MEI file and not already updated
    if filename.endswith(".mei") and not filename.endswith("NEW.mei"):
        # Update the MEI file using the octupdate module
        custupdate.main(filename)       
        # Print a message indicating that the file has been updated
        print(filename + " has been updated")