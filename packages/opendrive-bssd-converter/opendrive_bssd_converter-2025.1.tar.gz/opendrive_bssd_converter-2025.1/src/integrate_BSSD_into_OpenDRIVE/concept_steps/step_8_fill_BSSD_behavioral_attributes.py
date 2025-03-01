import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm

from integrate_BSSD_into_OpenDRIVE.utility.access_BSSD_user_data_element import access_BSSD_user_data_element
from integrate_BSSD_into_OpenDRIVE.algorithms.A_7_extract_behavioral_attributes_automatically import A_7_extract_behavioral_attributes_automatically

def step_8_fill_BSSD_behavioral_attributes(df_lane_data, df_BSSD_lanes, df_link_BSSD_lanes_with_OpenDRIVE_lanes, df_speed_limits, df_segments,
                                           driving_direction, OpenDRIVE_element, OpenDRIVE_object):
    """
    This function executes Step 8 of BSSD-Integration into OpenDRIVE. For every BSSD-lane it is tried to extract the values of the BSSD behavioral
    attributes based on the information with BSSD-relevance included in the imported OpenDRIVE-file and insert the extracted values in the minimal 
    structure for the BSSD behavior space (see step 7: step_7_create_minimal_behavior_space_structure.py).
    
    In the current version of this tool the following behavioral attributes are extracted:
        1. speed
        

    Parameters
    ----------
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file.
    df_BSSD_lanes : DataFrame
        DataFrame containing all created BSSD-lanes. For every BSSD-lane the object for the first laneSection overlapping
    df_link_BSSD_lanes_with_OpenDRIVE_lanes : DataFrame
        DataFrame for storing information about link of BSSD-lanes to OpenDRIVE-lanes.
        For every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row is defined
    df_speed_limits : DataFrame
        DataFrame which contains one row for every <speed>-element (defined in the OpenDRIVE-<lane>-elements)
        which is defined in the imported OpenDRIVE-file for a drivable lane
    df_segments : DataFrame
        DataFrame which contains all created BSSD-segments. 
        For every segment a start-s-coordinate is given. If the segments ends before the next segment in the road 
        or before the end of the road a end-s-coordinate is given.
    driving_direction : String
        Driving direction of scenery in imported OpenDRIVE-file. Is either 'RHT' (Right hand traffic) or 'LHT' (Left hand traffic)
        If no driving direction is defined, it is set as default to 'RHT'
    OpenDRIVE_element : etree.ElementTree.Element
        Element for the xodr-file --> Needed for modifying the xodr-file
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map

    Returns
    -------
    OpenDRIVE_element : etree.ElementTree.Element
        Modified OpenDRIVE_element

    """
    
    print('Automatic extraction of behavioral attributes...\n')
    
    #Execute function for extracting BSSD behavioral attributes automatically based on the informations contained in the imported OpenDRIVE-file
    df_BSSD_speed_attribute = A_7_extract_behavioral_attributes_automatically(df_lane_data, df_BSSD_lanes, df_link_BSSD_lanes_with_OpenDRIVE_lanes,
                                                                              df_speed_limits, df_segments, driving_direction, OpenDRIVE_object)
    print()
    
    #MODIFY XML-TREE
    print('Insert found values of behavioral attribute "speed" in BSSD <speed> elements...\n')
    filled_speed_elements = 0
    
    #Iteration through all <road>-elements of imported xodr-file to insert values of behavioral attributes in every BSSD-lane
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
                    
                    #Access elements <behaviorAlong> and <behaviorAgainst>
                    behaviorAlong_element = lane_element.find('behaviorAlong')
                    behaviorAgainst_element = lane_element.find('behaviorAgainst')
                    
                    #1. Fill behavioral attribute "speed"
                    
                    #Get values of BSSD "speed" attribute for current BSSD-lane
                    df_BSSD_speed_attribute_current_lane = df_BSSD_speed_attribute[
                                                            (df_BSSD_speed_attribute['road_id']==road_id) \
                                                            & (round(df_BSSD_speed_attribute['segment_s'], 3) == round(segment_s, 3)) \
                                                            & (df_BSSD_speed_attribute['lane_id_BSSD']==lane_id)]
                    df_BSSD_speed_attribute_current_lane = df_BSSD_speed_attribute_current_lane.reset_index(drop=True)
                    
                    
                    #Acess <speed>-elements in elements <behaviorAlong> and <behaviorAgainst>
                    speed_element_behavior_along = behaviorAlong_element.find('speed')
                    speed_element_behavior_against = behaviorAgainst_element.find('speed')
                    
                    #Get values for BSSD attribute speed along/against reference direction for current BSSD-lane
                    speed_behavior_along = df_BSSD_speed_attribute_current_lane.loc[0, 'speed_behavior_along']
                    speed_behavior_against = df_BSSD_speed_attribute_current_lane.loc[0, 'speed_behavior_against']
                    
                    #Check if the BSSD attribute speed could be extracted in the current lane along reference direction
                    #If yes, insert the value of the BSSD behavioral attribute speed in the xodr-file
                    if pd.isnull(speed_behavior_along)==False:
                        
                        #Remove "old" <speed>-element (without value for attribute "max") and 
                        behaviorAlong_element.remove(speed_element_behavior_along)
                        
                        #Create a new <speed>-element (with the filled value for attribute "max")
                        #Numbers are stored in xodr according to IEEE 754 (--> 17 significant decimal digits)
                        ET.SubElement(behaviorAlong_element, 'speed', attrib={'max': "{:.16e}".format(speed_behavior_along)})
                        
                        filled_speed_elements = filled_speed_elements + 1

                      
                    #Check if the BSSD attribute speed could be extracted in the current lane against reference direction
                    #If yes, insert the value of the BSSD behavioral attribute speed in the xodr-file
                    if pd.isnull(speed_behavior_against)==False:
                        
                        #Remove "old" <speed>-element (without value for attribute "max")
                        behaviorAgainst_element.remove(speed_element_behavior_against)
                        
                        #Create a new <speed>-element (with the filled value for attribute "max")
                        #Numbers are stored in xodr according to IEEE 754 (--> 17 significant decimal digits)
                        ET.SubElement(behaviorAgainst_element, 'speed', attrib={'max': "{:.16e}".format(speed_behavior_against)})
                        
                        filled_speed_elements = filled_speed_elements + 1

    print()

    #User output
    if filled_speed_elements == 1:
        print('Inserted value of behavioral attribute "speed" in ' + str(filled_speed_elements) + ' BSSD <speed> element')
    else:
        print('Inserted value of behavioral attribute "speed" in ' + str(filled_speed_elements) + ' BSSD <speed> elements')
    
    return OpenDRIVE_element





    
    