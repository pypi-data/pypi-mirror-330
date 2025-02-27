import xml.etree.ElementTree as ET
from pathlib import Path
from tqdm import tqdm
from importlib_resources import files as resources_files

from integrate_BSSD_into_OpenDRIVE.utility.access_BSSD_user_data_element import access_BSSD_user_data_element


def step_7_create_minimal_behavior_space_structure(OpenDRIVE_element):
    """
    This function executes Step 7 of BSSD-Integration into OpenDRIVE.
    In every created BSSD-<lane>-element a minimal structure of the BSSD-Behavior-Space is inserted.
    This minimal structure is imported from the file "minimal_structure_BSSD_behavior_space.xml".
    It consists of the parent-elements <behaviorAlong> and <behaviorAgainst>, which include the four subelements representing the four 
    behavioral attributes of the BSSD

    Parameters
    ----------
    OpenDRIVE_element : etree.ElementTree.Element
        Element for the xodr-file --> Needed for modifying the xodr-file

    Returns
    -------
    OpenDRIVE_element :etree.ElementTree.Element
        Modified OpenDRIVE_element

    """
    
    #Filename of XML-file with minimal structure of BSSD-BehaviorSpace
    filename_xml_minimal_structure = 'minimal_structure_BSSD_behavior_space.xml'
    
    #Path to XML-file with minimal structure of BSSD-BehaviorSpace
    filepath_xml_minimal_structure = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath(filename_xml_minimal_structure)
    
    print('Importing minimal structure from "' + filename_xml_minimal_structure + '" ...\n')
    
    #Import XML-file (xml.etree.ElementTree)
    tree_xml = ET.parse(filepath_xml_minimal_structure)

    #Access root-element of imported XML-file (<minimalStructure>-element --> contains elements <behaviorAlong> and <behaviorAgainst>)
    root_element_minimal_structure = tree_xml.getroot()
    
    #MODIFY XML-TREE
    print('Insert minimal structure in BSSD-lanes...\n')
    inserted_minimal_structures = 0
    
    #Iteration through all <road>-elements of imported xodr-file to create elements for behaviorSpace in every BSSD-lane
    for road_element in tqdm(OpenDRIVE_element.findall('road')):
        
        #Check if current road includes at least one drivable lane
        if road_element.find('lanes').find('userData') != None:
            
            #Access <userData>-element with BSSD-segments (there might be other <userData>-elements existing)
            user_data_element = access_BSSD_user_data_element(road_element)
            
            #Access created <segment>-elements in current road 
            segment_elements_current_road = user_data_element.findall('segment')
            
            #Iteration through all <segment>-elements in current road to access <lane>-elements in the segments
            for segment_element in segment_elements_current_road:
                
                #Iteration through all BSSD-<lane>-elements in current segment
                for lane_element in segment_element.iter('lane'):

                    #Create subelements <behaviorAlong> and <behaviorAgainst> in every lane
                    #(Have to be created separately as the usage of the elements from XML with minimal structure leads to elements which are
                    #linked to each other)
                    behaviorAlong_element = ET.SubElement(lane_element, 'behaviorAlong')
                    behaviorAgainst_element = ET.SubElement(lane_element, 'behaviorAgainst')
                    
                    #Insert minimal structure of BSSD-Behavior-Space into BSSD-<lane>-element
                    # --> Iterate through all subelements (<boundary>, <speed> etc.) of minimal structure and append them to <behaviorAlong>
                    for subelement in root_element_minimal_structure.find('behaviorAlong'):
                        behaviorAlong_element.append(subelement)

                    #--> Iterate through all subelements (<boundar>, <speed> etc.) of minimal structure and append them to <behaviorAgainst>
                    for subelement in root_element_minimal_structure.find('behaviorAgainst'):
                        behaviorAgainst_element.append(subelement)
                    
                    inserted_minimal_structures = inserted_minimal_structures + 1
    
    print()

    #User output
    if inserted_minimal_structures  == 1:
        print('Inserted minimal structure in ' + str(inserted_minimal_structures) + ' BSSD-lane')
    else:
        print('Inserted minimal structure in ' + str(inserted_minimal_structures) + ' BSSD-lanes')
    
    return OpenDRIVE_element
    
    