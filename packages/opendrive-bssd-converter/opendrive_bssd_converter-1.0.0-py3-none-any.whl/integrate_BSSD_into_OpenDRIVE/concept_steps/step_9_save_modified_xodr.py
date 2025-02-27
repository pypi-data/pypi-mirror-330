import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from pathlib import Path

def step_9_save_modified_xodr(OpenDRIVE_element, filepath_xodr):
    """
    This function executes Step 9 of BSSD-Integration into OpenDRIVE. The modified OpenDRIVE-element is saved as new OpenDRIVE-file.
    The new OpenDRIVE-file has the name of the original OpenDRIVE-file with the additonal ending "_BSSD"
    
    Parameters
    ----------
    OpenDRIVE_element : etree.ElementTree.Element
        Element for the modified xodr-file --> Is saved as .xodr-file
    filepath_xodr : pathlib.Path
        Full Path to the imported xodr-file --> Modified xodr-file is saved in the same location

    Returns
    -------
    None.

    """

    #Get path to folder which contains xodr-file
    path_xodr = filepath_xodr.parent
    
    #Path to folder for exporting modified xodr-file --> Modified file is stored in the same folder as the input file
    export_path_xodr = path_xodr

    #Filename of modified OpenDRIVE-file
    filename_export_xodr = str(filepath_xodr.stem) + '_BSSD.xodr'
    
    #Complete filepath for export of modified OpenDRIVE-file
    filepath_export_xodr = Path.joinpath(export_path_xodr, filename_export_xodr)
    
    print('Saving modified file...\n')    
    
    #Save modified xodr-file as "pretty-print" (human-friendly format) with module "minidom"
    pretty_print = lambda data: '\n'.join([line for line in parseString(data).toprettyxml(indent='\t').split('\n') if line.strip()])
    
    with open(filepath_export_xodr, 'w') as f:
        f.write(pretty_print(ET.tostring(OpenDRIVE_element)))
    
    print('Saved modified file as "' + filename_export_xodr + '" in directory "' + str(export_path_xodr) + '"\n')  
