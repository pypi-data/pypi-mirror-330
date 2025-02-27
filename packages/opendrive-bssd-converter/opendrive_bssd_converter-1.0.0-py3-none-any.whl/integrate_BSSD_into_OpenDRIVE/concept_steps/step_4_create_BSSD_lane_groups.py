import xml.etree.ElementTree as ET
from tqdm import tqdm

from integrate_BSSD_into_OpenDRIVE.utility.access_BSSD_user_data_element import access_BSSD_user_data_element

def step_4_create_BSSD_lane_groups(OpenDRIVE_element):
    """
    This function creates the elements for the BSSD-lane-groups <right> and <left>.
    In every <segment>-element, one subelement <right> and one subelement <left> is created 
    (independent from whether there are actually <lane>-elements below the <right>- or the <left>-element)

    Parameters
    ----------
    OpenDRIVE_element : etree.ElementTree.Element
        Element for the xodr-file --> Needed for modifying the xodr-file

    Returns
    -------
    OpenDRIVE_element : etree.ElementTree.Element
        Modified OpenDRIVE_element

    """
    
    #MODIFY XML-TREE
    print('Creating BSSD lane group elements <right>/<left>...\n')
    
    created_lane_groupings = 0
    
    #Iteration through all <road>-elements of imported xodr-file to create <right> and <left>-elements in every segment
    for road_element in tqdm(OpenDRIVE_element.findall('road')):
                
        #Check if current road includes at least one drivable lane
        if road_element.find('lanes').find('userData') != None:
            
            #Access <userData>-element with BSSD-segments (there might be other <userData>-elements existing)
            user_data_element = access_BSSD_user_data_element(road_element)
            
            #Access created <segment>-elements in current road 
            segment_elements_current_road = user_data_element.findall('segment')
            
            #Iteration through all <segment>-elements in current road to create one <right>- and one <left>-element in the segments
            for segment_element in segment_elements_current_road:
                ET.SubElement(segment_element, 'right')
                ET.SubElement(segment_element, 'left')
                
                created_lane_groupings = created_lane_groupings + 2
                
                
    print()

    #User output
    if created_lane_groupings  == 1:
        print('Created ' + str(created_lane_groupings) + ' <right>/<left> element')
    else:
        print('Created ' + str(created_lane_groupings) + ' <right>/<left> elements')
    
    return OpenDRIVE_element
    