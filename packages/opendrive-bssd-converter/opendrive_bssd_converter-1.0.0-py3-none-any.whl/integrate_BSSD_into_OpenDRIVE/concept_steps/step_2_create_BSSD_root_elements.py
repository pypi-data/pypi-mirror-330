import xml.etree.ElementTree as ET
from tqdm import tqdm
from rich.console import Console
console = Console(highlight=False)

from integrate_BSSD_into_OpenDRIVE.algorithms.A_1_find_drivable_lanes import A_1_find_drivable_lanes
from integrate_BSSD_into_OpenDRIVE.algorithms.A_2_manually_edit_drivable_lanes import A_2_manually_edit_drivable_lanes


def step_2_create_BSSD_root_elements(OpenDRIVE_element, OpenDRIVE_object):
    """
    This function executes Step 2 of BSSD-Integration into OpenDRIVE.
    In every road that contains at least one lane that represent a lane that is modelled in BSSD, a <userData>-element is created to 
    store the BSSD-information for this road. All lanes that are part of roadway (German: 'Fahrbahn') are modelled in BSSD.
    These lanes will be called "drivable lanes" in the following.
    
    To find out which lanes in the imported OpenDRIVE-file are "drivable" two substeps are executed:
        1. Function "A_1_find_drivable_lanes.py": Automatic search of drivable lanes based on the attribute 'type' of the OpenDRIVE-<lane>-element
        2. Function "A_2_manually_edit_drivable_lanes.py": Provides the possibilty to manually edit the found drivable lanes.
        
    Parameters
    ----------
    OpenDRIVE_element : etree.ElementTree.Element
        Element for the xodr-file --> Needed for modifying the xodr-file
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map
        
    Returns
    -------
    OpenDRIVE_element : etree.ElementTree.Element
        Modified OpenDRIVE_element
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file.
    df_lane_data_drivable_lanes : DataFrame
        Subset of df_lane_data, which only contains lanes that represent a drivable OpenDRIVE-lane
    
    """
    
    #SUBSTEP 1: Function to automatically find drivable lanes within OpenDRIVE-file to create a <userData>-element in every road 
    #which contains at least one drivable lane
    print('Analyzing OpenDRIVE-file for drivable lanes...\n')
    df_lane_data, df_lane_data_drivable_lanes, df_lane_data_not_drivable_lanes = A_1_find_drivable_lanes(OpenDRIVE_object)

    #Console output
    percentage_drivable_lanes = 100 * (len(df_lane_data_drivable_lanes)/len(df_lane_data))
    percentage_drivable_lanes = round(percentage_drivable_lanes)
    
    #Get number of roads, laneSections and lanes in imported xodr for console output
    number_roads = df_lane_data['road_id'].nunique()
    number_laneSections = len(df_lane_data.drop_duplicates(['road_id', 'laneSection_s']))
    number_lanes = len(df_lane_data)
    
    #Console output depending whether only one road/laneSection/lane exists or not
    if number_roads  == 1:
        string_number_roads = str(number_roads) + ' road'
    else:
        string_number_roads = str(number_roads) + ' roads'
    
    if number_laneSections  == 1:
        string_number_laneSections = str(number_laneSections) + ' lane section'
    else:
        string_number_laneSections = str(number_laneSections) + ' lane sections'
        
    if number_lanes  == 1:
        string_number_lanes = str(number_lanes) + ' lane'
    else:
        string_number_lanes = str(number_lanes) + ' lanes'
    
    print()
    print('OpenDRIVE-file contains ' + string_number_roads + ', ' + string_number_laneSections + ' and ' + 
          string_number_lanes + '\n')
    print(str(percentage_drivable_lanes) + ' % of all lanes were marked as drivable lanes. All these lanes will be modelled within BSSD\n')
    print('Do you want to edit the found drivable lanes manually? [y/n]\n')

    #SUBSTEP 2: Get user input to check whether drivable lanes should be edited manually
    while True:
        input_manually_edit_lanes = input('Input: ')
        print()
        
        #Manual editing of drivable lanes is desired
        if input_manually_edit_lanes == 'y' or input_manually_edit_lanes=='Y' or input_manually_edit_lanes == 'yes' or input_manually_edit_lanes == 'Yes':
            
            #Manually add/remove drivable lanes from list of automatically foung drivable lanes
            df_lane_data_drivable_lanes, df_lane_data_not_drivable_lanes = A_2_manually_edit_drivable_lanes(df_lane_data,
                                                                                                        df_lane_data_drivable_lanes, 
                                                                                                        df_lane_data_not_drivable_lanes)
            break
        
        #No manual editing of drivable lanes desired
        elif input_manually_edit_lanes == 'n' or input_manually_edit_lanes=='N' or input_manually_edit_lanes == 'no' or input_manually_edit_lanes == 'No':
            break
        #No valid input
        else:
            console.print('[bold red]"' + input_manually_edit_lanes + '" is no valid input. Please enter "y" or "n".[/bold red]')
            continue

    
    #MODIFY XML-TREE
    print('Creating <userData> elements...\n')
    created_user_data_elements = 0
    
    #Iteration through all <road>-elements of imported xodr-file to create <userData>-element in every road which contains at least one drivable lane
    for road_element in tqdm(OpenDRIVE_element.findall('road')):
        #id of current <road>-element
        road_id = int(road_element.get('id'))
        
        #Check if current road includes at least one drivable lane
        if any(df_lane_data_drivable_lanes.road_id == road_id) == True:
            
            #<lanes>-element of current <road>-element --> To create <userData>-element for current road
            lanes_element = road_element.find('lanes')
            
            #Create <userData>-elements with attributes "code" and "value" (obligatory accoring to XML-schema of OpenDRIVE)
            ET.SubElement(lanes_element, 'userData', attrib={'code': 'BSSD', 'value': 'BSSD_segments'})
            created_user_data_elements = created_user_data_elements + 1
    
    print()
    
    #User output
    if created_user_data_elements  == 1:
        print('Created element <userData> in ' + str(created_user_data_elements) + ' road')
    else:
        print('Created element <userData> in ' + str(created_user_data_elements) + ' roads')
        
    
    return df_lane_data, df_lane_data_drivable_lanes, OpenDRIVE_element