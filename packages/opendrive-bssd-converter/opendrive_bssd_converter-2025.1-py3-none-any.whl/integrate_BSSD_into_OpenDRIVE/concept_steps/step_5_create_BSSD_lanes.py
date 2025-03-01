import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm

from integrate_BSSD_into_OpenDRIVE.algorithms.A_5_find_overlappings_segments_laneSections import A_5_find_overlappings_segments_laneSections
from integrate_BSSD_into_OpenDRIVE.utility.access_BSSD_user_data_element import access_BSSD_user_data_element


def step_5_create_BSSD_lanes(df_segments, df_lane_data_drivable_lanes, OpenDRIVE_element, OpenDRIVE_object):
    """
    This function executes Step 5 of BSSD-Integration into OpenDRIVE.
    In every created BSSD-segment (see step 3) the BSSD-<lane>-elements are created. The BSSD-<lane>-elements are created based on the 
    OpenDRIVE-<lane>-elements which are defined in the first laneSection that overlaps with the BSSD-segment (seen by the s-range of the 
    laneSections and the BSSD-segments).
    
    The function A_5_find_overlappings_segments_laneSections.py finds all laneSections that overlap with the BSSD-segments.
    For every BSSD-Segment the first overlapping laneSection is chosen. Based on the id's of the OpenDRIVE-lanes in this laneSection,
    the id's of the BSSD-<lane>-elements in this segment are chosen.


    Parameters
    ----------
    df_segments : DataFrame
        DataFrame which contains all created BSSD-segments. 
    df_lane_data_drivable_lanes : DataFrame
        DataFrame which contains all lanes that represent a drivable OpenDRIVE-lane
    OpenDRIVE_element : etree.ElementTree.Element
        Element for the xodr-file --> Needed for modifying the xodr-file
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map

    Returns
    -------
    df_overlappings_segments_laneSections : DataFrame
        DataFrame which contains per segment one row for every laneSection that overlaps to this segment
    df_BSSD_lanes : DataFrame
        DataFrame containing all created BSSD-lanes. For every BSSD-lane the object for the first laneSection overlapping
        to the segment which contains this BSSD-lane is stored (--> Necessary for the succeeding step 6 of the concept)
    OpenDRIVE_element : etree.ElementTree.Element
        Modified OpenDRIVE_element
        
    """

    
    print()
    print('Searching for overlappings between created BSSD-segments and existing laneSections ...\n')
    
    #Function to find for every created BSSD-Segment the laneSections which overlap to this BSSD-Segment.
    df_overlappings_segments_laneSections = A_5_find_overlappings_segments_laneSections(df_segments, df_lane_data_drivable_lanes, OpenDRIVE_object)
    print()
        
    #DataFrame containing all created BSSD-lanes. For every BSSD-lane the object for the first laneSection overlapping
    #to the segment which contains this BSSD-lane is stored (--> Necessary for the succeeding step 6 of the concept)
    df_BSSD_lanes = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_object_s_min'])           
    
    
    #MODIFY XML-TREE
    print('Creating <lane> elements...\n')
    
    created_lane_elements = 0
    
    #Iteration through all <road>-elements of imported xodr-file to create <lane>-elements in every segment
    for road_element in tqdm(OpenDRIVE_element.findall('road')):
        
        #id of current <road>-element
        road_id = int(road_element.get('id'))
        
        #Check if current road includes at least one drivable lane
        if road_element.find('lanes').find('userData') != None:
            
            #Access <userData>-element with BSSD-segments (there might be other <userData>-elements existing)
            user_data_element = access_BSSD_user_data_element(road_element)
            
            #Access created <segment>-elements in current road 
            segment_elements_current_road = user_data_element.findall('segment')
            
            #Iteration through all <segment>-elements in current road to access <right>- and <left>-elements in the segments and create
            #<lane>-elements underneath
            for segment_element in segment_elements_current_road:
                
                #s-coordinate of current segment
                segment_s = float(segment_element.get('sStart'))
                
                #DataFrame which contains only laneSections overlapping with the current segment
                df_overlappings_current_segment = \
                    df_overlappings_segments_laneSections[ (df_overlappings_segments_laneSections['road_id']==road_id) & \
                                                          (round(df_overlappings_segments_laneSections['segment_s'], 3)==round(segment_s, 3))]  
                
                #Sort laneSections overlapping with current segment by s-coordinate
                df_overlappings_current_segment = df_overlappings_current_segment.sort_values(['laneSection_s'])
                df_overlappings_current_segment = df_overlappings_current_segment.reset_index(drop=True)
                
                #Get first laneSection overlapping to current segment
                laneSection_object_s_min = df_overlappings_current_segment.loc[0, 'laneSection_object']
                
                #Get s-coordinate of frist laneSection overlapping with current segment
                s_laneSection_min = laneSection_object_s_min.sPos
                
                #Create list which contains id's of all lanes in first overlapping laneSection
                list_lanes = []
                for lane_object in laneSection_object_s_min.allLanes:
                    
                    #Add all lanes to list with id's of lanes except for center lane (id=0 --> Not modelled in BSSD)
                    if lane_object.id!=0:
                        
                        list_lanes.append(lane_object.id)
                    
                #Sort list in ascending order to enable continous id's in modified xodr-file
                list_lanes.sort()
                
                #Iterate through all OpenDRIVE-lanes in first overlapping laneSection to create a BSSD-lane for every drivable OpenDRIVE-lane
                #in this laneSection
                for lane_id in list_lanes:
                    
                    #Access object for current OpenDRIVE-lane
                    lane_object = laneSection_object_s_min.getLane(lane_id)
                    
                    #Check if current lane is a drivable lane --> Only then it has to be modelled in BSSD
                    if len(df_lane_data_drivable_lanes[(df_lane_data_drivable_lanes['road_id']==road_id)\
                                                & (round(df_lane_data_drivable_lanes['laneSection_s'], 3)==round(s_laneSection_min, 3))\
                                                & (df_lane_data_drivable_lanes['lane_id']==lane_id)])>0:
                        
                        #Check if current OpenDRIVE-lane is defined on the right or left side of the road 
                        #Case 1: Current OpenDRIVE-lane defined on the right side (id < 0)
                        if lane_id < 0:
                            
                            #Access element <right> in current segment
                            right_element = segment_element.find('right')
                            
                            #Create subelement <lane> with id equally to id of <lane>-Element in first laneSection overlapping with the current
                            #segment
                            ET.SubElement(right_element, 'lane', attrib={'id': str(lane_id)})
                        
                        #Case 2: Current OpenDRIVE-lane defined on the left side (id > 0) --> id 0 was excluded before
                        else:
                            
                            #Access element <left> in current segment
                            left_element = segment_element.find('left')
                            
                            #Create subelement <lane> with id equally to id of <lane>-Element in first laneSection overlapping with the current
                            #segment
                            ET.SubElement(left_element, 'lane', attrib={'id': str(lane_id)})
                                
                            
                        #Append data of current lane to df_BSSD_lanes
                        df_BSSD_lanes = df_BSSD_lanes.append({'road_id': road_id, 'segment_s': segment_s, 'lane_id_BSSD': lane_id,
                                                    'laneSection_object_s_min': laneSection_object_s_min}, ignore_index=True)
                        
                        created_lane_elements = created_lane_elements + 1
                            
                    
    print()
    
    #User output
    if created_lane_elements  == 1:
        print('Created ' + str(created_lane_elements) + ' <lane> element')
    else:
        print('Created ' + str(created_lane_elements) + ' <lane> elements')
    
    return df_overlappings_segments_laneSections, df_BSSD_lanes, OpenDRIVE_element
    
    