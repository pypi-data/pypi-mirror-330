import xml.etree.ElementTree as ET
from lxml import etree
from pathlib import Path
import sys
from rich.console import Console
from importlib_resources import files as resources_files

console = Console(highlight=False)

from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive


def step_1_import_and_validate_xodr(filepath_xodr):
    """
    This function executes step 1 of BSSD-Integration into OpenDRIVE. 
    The OpenDRIVE-file specified in "filepath_xodr" first is validated for the OpenDRIVE-versions 1.4, 1.5, 1.6 and 1.7.
    If the file is valid, it is stored as an OpenDRIVE-object (usage of opendriveparser from TUM (v0.3)
                                                               https://gitlab.lrz.de/tum-cps/commonroad-scenario-designer/-/tree/main/crdesigner/map_conversion/opendrive/opendrive_parser)
    and it is stored as an xml ElementTree to allow modification to the xodr-file.
    
    Parameters
    ----------
    filepath_xodr : pathlib.Path
        Full Path to the xodr-file


    Returns
    -------
    OpenDRIVE_element : etree.ElementTree.Element
        Element for the xodr-file --> Needed for modifying the xodr-file
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map
    driving_direction : String
        Driving direction of scenery in imported OpenDRIVE-file. Is either 'RHT' (Right hand traffic) or 'LHT' (Left hand traffic)
        If no driving direction is defined, it is set as default to 'RHT'
    """
    
    #get filename of xodr-file from imported filepath
    filename_xodr = filepath_xodr.name
        
    #Import xodr-file (lxml) --> Needed for opendriveparser TUM and validation of xodr
    tree_xodr = etree.parse(str(filepath_xodr))
    
    #Get paths to schema-files of different OpenDRIVE-versions from package resources
    schema_1_4 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('OpenDRIVE_1.4H_Schema_Files.xsd')
    schema_1_5 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('OpenDRIVE_1.5_Schema_Files.xsd')
    schema_1_6 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('opendrive_16_core.xsd')
    schema_1_7 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('opendrive_17_core.xsd')
    
                      
    #Read in OpenDRIVE-schema-files 
    OpenDRIVE_1_4_schema_doc = etree.parse(str(schema_1_4))
    OpenDRIVE_1_5_schema_doc = etree.parse(str(schema_1_5))
    OpenDRIVE_1_6_schema_doc = etree.parse(str(schema_1_6))
    OpenDRIVE_1_7_schema_doc = etree.parse(str(schema_1_7))
    
     
    #Check for validity of xodr-file
    print('Validating imported OpenDRIVE-file "' + filename_xodr + '"...\n')
    if ((validate_against_OpenDRIVE_version(tree_xodr, OpenDRIVE_1_4_schema_doc)==False) and \
       (validate_against_OpenDRIVE_version(tree_xodr, OpenDRIVE_1_5_schema_doc)==False) and \
       (validate_against_OpenDRIVE_version(tree_xodr, OpenDRIVE_1_6_schema_doc)==False) and \
       (validate_against_OpenDRIVE_version(tree_xodr, OpenDRIVE_1_7_schema_doc)==False)) == True :
        print('Imported OpenDRIVE-File "' + filename_xodr + '" is not valid for OpenDRIVE-versions 1.4, 1.5, 1.6 and 1.7\n')
        print('Due to that the correct functionality of the BSSD-integration into the imported xodr can not be guaranteed\n')
        print('Do you wish to continue nevertheless? [y/n]\n')
        
        #If xodr-file is not valid, ask for execution of tool
        while True:
            input_continue = input('Input: ')
            print()
            
            #Continuing is desired
            if input_continue == 'y' or input_continue=='Y' or input_continue == 'yes' or input_continue == 'Yes':
                break
            #Continuing is not desired 
            elif input_continue == 'n' or input_continue=='N' or input_continue == 'no' or input_continue == 'No':
                print('Aborting BSSD-integration into OpenDRIVE...\n')
                sys.exit()
            #No valid input
            else:
                console.print('[bold red]"' + input_continue + '" is no valid input. Please enter "y" or "n".\n[/bold red]')
                continue
        

    #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
    #https://gitlab.lrz.de/tum-cps/commonroad-scenario-designer/-/tree/main/crdesigner/map_conversion/opendrive/opendrive_parser
    OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())

    #Find OpenDRIVE-Version of imported file for console output
    header_object = OpenDRIVE_object.header
    OpenDRIVE_version = header_object.revMajor + '.' + header_object.revMinor

    #Import xodr-file (xml.etree.ElementTree)
    tree_xodr = ET.parse(filepath_xodr)

    #Access root-element of imported xodr-file
    OpenDRIVE_element = tree_xodr.getroot()
    
    #Console output
    print('Succesfully imported OpenDRIVE-file "' + filename_xodr + '" with Version ' + OpenDRIVE_version + '\n')
    
    #Set driving direction as default to Right-Hand-Traffic (RHT)
    #If LHT is desired (and not included in xodr-file), set this variable to 'LHT'
    driving_direction='RHT'
    
    #Iteration through all <road>-elements of imported xodr-file to check if a driving direction (RHT/LHT) has been defined 
    for road_element in OpenDRIVE_element.findall('road'):
        
        #Search for the first <road>-element which has a defined driving direction RHT/LHT 
        #If a road with RHT/LHT is found, this is set as the default driving direction for the whole OpenDRIVE-file
        if road_element.get('rule') == 'RHT':
            break
        elif road_element.get('rule') == 'LHT':
            driving_direction = 'LHT'
            break
    
            
    return OpenDRIVE_element, OpenDRIVE_object, driving_direction
           

def validate_against_OpenDRIVE_version(tree_xodr, schema_doc):
    """
    This function validates a given xodr-file (included in "tree_xodr") against a given xml-schema (included in "schema_doc")
    """
    
    #Create validator
    schema = etree.XMLSchema(schema_doc)
    
    #Execute validation
    validation_result = schema.validate(tree_xodr)
    
    return validation_result
    
    