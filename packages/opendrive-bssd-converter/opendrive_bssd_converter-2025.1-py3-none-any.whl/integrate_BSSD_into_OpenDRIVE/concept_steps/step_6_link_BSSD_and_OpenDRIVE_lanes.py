import xml.etree.ElementTree as ET
from tqdm import tqdm

from integrate_BSSD_into_OpenDRIVE.algorithms.A_6_search_linked_OpenDRIVE_lanes import A_6_search_linked_OpenDRIVE_lanes
from integrate_BSSD_into_OpenDRIVE.utility.access_BSSD_user_data_element import access_BSSD_user_data_element

def step_6_link_BSSD_and_OpenDRIVE_lanes(df_overlappings_segments_laneSections, df_BSSD_lanes, OpenDRIVE_element):
    """
    This function executes Step 6 of BSSD-Integration into OpenDRIVE.
    In every created BSSD-<lane>-element an element <assignLaneOpenDRIVE> is created. This element is necessary to have a unique link of a
    BSSD-lane to an OpenDRIVE-lane for a certain s-coordinate.
    The element <assignLaneOpenDRIVE> has at least one subelement <linkedLane>. Every element <linkedLane> is representative for one OpenDRIVE-
    <lane>-element which is defined during the s-range of the BSSD-<lane>-element.
    
    To realize this, the function A_6_search_linked_OpenDRIVE_lanes.py is executed.
    This function searches for all BSSD-lanes the linked OpenDRIVE-lanes and returns them in a DataFrame. Based on this DataFrame, the 
    elements desribed above are created.
    

    Parameters
    ----------       
    df_overlappings_segments_laneSections : DataFrame
        DataFrame which contains per segment one row for every laneSection that overlaps to this segment
    df_BSSD_lanes : DataFrame
        DataFrame for storing all created BSSD-lanes
    OpenDRIVE_element : etree.ElementTree.Element
        Element for the xodr-file --> Needed for modifying the xodr-file

    Returns
    -------
    df_link_BSSD_lanes_with_OpenDRIVE_lanes : DataFrame
        DataFrame for storing information about link of BSSD-lanes to OpenDRIVE-lanes.
        For every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row is defined
    OpenDRIVE_element : etree.ElementTree.Element
        Modified OpenDRIVE_element

    """
    
    
    print()
    print('Search for links between created BSSD-lanes and existing OpenDRIVE-lanes ...\n')
    
    #Execute function for searching the OpenDRIVE-lanes, which are linked to the created BSSD-lanes
    df_link_BSSD_lanes_with_OpenDRIVE_lanes = A_6_search_linked_OpenDRIVE_lanes(df_overlappings_segments_laneSections, df_BSSD_lanes)
    print()
    
    
    #MODIFY XML-TREE
    print('Creating <linkedLane> elements...\n')
    created_linkedLane_elements = 0 
    
    #Iteration through all <road>-elements of imported xodr-file to create <assignLaneOpenDRIVE>-elements in every BSSD-lane
    for road_element in tqdm(OpenDRIVE_element.findall('road')):
        
        #id of current <road>-element
        road_id = int(road_element.get('id'))
        
        #Check if current road includes at least one drivable lane
        if road_element.find('lanes').find('userData') != None:
            
            #Access <userData>-element with BSSD-segments (there might be other <userData>-elements existing)
            user_data_element = access_BSSD_user_data_element(road_element)
            
            #Access created <segment>-elements in current road 
            segment_elements_current_road = user_data_element.findall('segment')
            
            #Iteration through all <segment>-elements in current road to access <lane>-elements in the segments
            for segment_element in segment_elements_current_road:
                
                #s-coordinate of current segment
                segment_s = float(segment_element.get('sStart'))

                #Iteration through all BSSD-<lane>-elements in current segment
                for lane_element in segment_element.iter('lane'):
                    
                    #id of current BSSD-lane
                    lane_id = int(lane_element.get('id'))
                    
                    #Create subelement <assignLaneOpenDRIVE> in every BSSD-<lane>-element
                    ET.SubElement(lane_element, 'assignLaneOpenDRIVE')

                    
                    #Access OpenDRIVE-lanes which overlap to the current BSSD-lane
                    df_link_current_BSSD_lane = df_link_BSSD_lanes_with_OpenDRIVE_lanes[(df_link_BSSD_lanes_with_OpenDRIVE_lanes['road_id']==road_id)\
                                                & (round(df_link_BSSD_lanes_with_OpenDRIVE_lanes['segment_s'], 3)==round(segment_s, 3))\
                                                & (df_link_BSSD_lanes_with_OpenDRIVE_lanes['lane_id_BSSD']==lane_id)]
                    df_link_current_BSSD_lane = df_link_current_BSSD_lane.reset_index(drop=True)
                    
                    #Access created <assignLaneOpenDRIVE>-element
                    assignLaneOpenDRIVE_element = lane_element.find('assignLaneOpenDRIVE')
                    
                    #Iterate through all OpenDRIVE-lanes which overlap to the current BSSD-lane to create a <linkedLane> element for
                    #every overlapping OpenDRIVE-lane
                    for index, lane_id_OpenDRIVE in enumerate(df_link_current_BSSD_lane.loc[:, 'lane_id_OpenDRIVE']):
                        
                        #Create subelement <linkedLane> for every link of a BSSD-lane to an OpenDRIVE-lane 
                        ET.SubElement(assignLaneOpenDRIVE_element, 'linkedLane', attrib={'sLaneSection': "{:.16e}".format(df_link_current_BSSD_lane.loc[index, 'laneSection_s']), 
                                                                                         'id': str(int(lane_id_OpenDRIVE))})
                    
                    #console output depending on the number of linked OpenDRIVE-lane
                    number_of_links = len(df_link_current_BSSD_lane)
                    
                    created_linkedLane_elements = created_linkedLane_elements + number_of_links

    print()

    #User output
    if created_linkedLane_elements  == 1:
        print('Created ' + str(created_linkedLane_elements) + ' <linkedLane> element')
    else:
        print('Created ' + str(created_linkedLane_elements) + ' <linkedLane> elements')    

    return df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_element
