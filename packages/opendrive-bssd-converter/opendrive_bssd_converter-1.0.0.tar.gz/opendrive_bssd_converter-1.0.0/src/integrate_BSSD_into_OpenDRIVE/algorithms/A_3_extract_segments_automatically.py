import pandas as pd
import bisect

from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_1_segments_by_changing_number_of_drivable_lanes import A_3_1_segments_by_changing_number_of_drivable_lanes
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_2_segments_by_starting_and_ending_drivable_lanes import A_3_2_segments_by_starting_and_ending_drivable_lanes
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_3_segments_by_speed_limit import A_3_3_segments_by_speed_limit
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_4_segments_by_static_signals import A_3_4_segments_by_static_signals
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_5_segments_by_dynamic_signals import A_3_5_segments_by_dynamic_signals

def A_3_extract_segments_automatically(df_lane_data, df_lane_data_drivable_lanes, OpenDRIVE_object):
    """
    This function extracts BSSD-segments (<segment>-elements) automatically based on informations in the imported OpenDRIVE-file.
    The BSSD-segments are extracted based on different rules, which are applied in consecutive steps:
        1. If the number of drivable lanes changes from one laneSection to the next laneSection, a new segment has to 
           be defined.
        2. If a drivable lane starts/ends in a laneSection that has a preceding/succeeding laneSection, a new segment has to be defined 
           for the s-coordinate of this laneSection/the s-coordinate of the succeeding laneSection
        3. If the speed limit for a drivable lane changes, a new segment has to be defined
        4. If there is a traffic sign, which affects a BSSD behavioral attribute, a new segment is defined
        5. If there is a traffic light or another dynamic signal, a new segment is defined
           
    For every rule a separate subfunction is defined, which extracts the segments based on this rule:
        Rule 1: A_3_1_segments_by_changing_number_of_drivable_lanes.py
        Rule 2: A_3_2_segments_by_starting_and_ending_drivable_lanes.py
        Rule 3: A_3_3_segments_by_speed_limit.py
        Rule 4: A_3_4_segments_by_static_signals.py
        Rule 5: A_3_5_segments_by_dynamic_signals.py
        

    Parameters
    ----------
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported
        xodr-file
    df_lane_data_drivable_lanes : DataFrame
        DataFrame which contains information about all lanes that represent a drivable OpenDRIVE-lane 
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map

    Returns
    -------
    df_segments_automatic : DataFrame
        DataFrame which contains the automatically extracted segments. For every segment a start-s-coordinate is given. 
        If the segments ends before the next segment in the road or before the end of the road a end-s-coordinate is given.
    df_speed_limits : DataFrame
        DataFrame which contains one row for every <speed>-element (defined in the OpenDRIVE-<lane>-elements)
        which is defined in the imported OpenDRIVE-file for a drivable lane
    """
    

    #Execute subfunction for extracting segments by Rule 1
    df_segments_automatic, roads_laneSections_equal_segments = A_3_1_segments_by_changing_number_of_drivable_lanes(df_lane_data,
                                                                                                                   df_lane_data_drivable_lanes)
                                                                                                                   
    #Execute subfunction for extracting segments by Rule 2
    df_segments_automatic = A_3_2_segments_by_starting_and_ending_drivable_lanes(df_lane_data, df_lane_data_drivable_lanes,
                                                                                 df_segments_automatic, roads_laneSections_equal_segments,
                                                                                 OpenDRIVE_object)
    
    #Execute subfunction for extracting segments by Rule 3
    df_segments_automatic, df_speed_limits = A_3_3_segments_by_speed_limit(df_lane_data, df_lane_data_drivable_lanes, df_segments_automatic,
                                                                           OpenDRIVE_object)
    #Execute subfunction for extracting segments by Rule 4
    df_segments_automatic, file_contains_dynamic_signals = A_3_4_segments_by_static_signals(df_lane_data_drivable_lanes, df_segments_automatic,
                                                                                            OpenDRIVE_object)
    
    #Check if imported OpenDRIVE-file contains any dynamic <signal>-elements
    #If imported OpenDRIVE-file contains no dynamic <signal>-elements, execution of rule 5 can be skipped
    if file_contains_dynamic_signals==True:
        
        #Execute subfunction for extracting segments by Rule 5
        df_segments_automatic = A_3_5_segments_by_dynamic_signals(df_lane_data_drivable_lanes, df_segments_automatic, OpenDRIVE_object)
                                                                  
    
    return df_segments_automatic, df_speed_limits

def check_for_succeeding_lane_section_with_no_drivable_lanes(s_laneSection, laneSections_drivable_lanes, laneSections_all_lanes):
    """
    This function checks for a laneSection (s_laneSection) whether there is a suceeding laneSection which doesn't contain any drivable
    lanes. This is done by comparing all laneSections in the current road that contain at least one drivable lane 
    (variable "laneSections_drivable_lanes") with all laneSections in the current road (variable "laneSections_all_lanes")
    
    If there is a succeeding laneSection with no drivable lanes, the function returns "True". If not, the function returns "False".
    
    This function is necessary to detect BSSD definitions gaps (laneSection with no drivable lanes)
    
    """
    
    #Check if current laneSection is last laneSection in current road
    #If yes, there is no suceeding laneSection with no drivable lanes
    if s_laneSection == laneSections_all_lanes[len(laneSections_all_lanes)-1]:
        return False
    #If no, check drivable lanes in succeeding laneSection
    else:
        #Get index of current laneSection in list with only drivable lanes
        index_list_drivable_lanes = laneSections_drivable_lanes.index(s_laneSection)
        
        #Get index of current laneSection in list with all lanes
        index_list_all_lanes = laneSections_all_lanes.index(s_laneSection)
        
        #Check if current laneSection is the last laneSection with drivable lanes but not the last laneSection (in general) 
        #in the current road --> If yes, there is a suceeding laneSection with no drivable lanes
        if s_laneSection == laneSections_drivable_lanes[len(laneSections_drivable_lanes)-1]:
            return True
        else:
            #Check if succeeding laneSection in both lists is the same laneSection
            #If yes, there is a suceeding laneSection with drivable lanes
            if laneSections_drivable_lanes[index_list_drivable_lanes+1] == laneSections_all_lanes[index_list_all_lanes+1]:
                return False
            #If no, there is a suceeding laneSection with no drivable lanes
            else:
                return True

def paste_segment(df_segments_automatic, road_id, s_start, s_end):
    """
    This function pastes a new segment (given road_id, s_start and s_end) into df_segments_automatic at the correct position
    --> Needed every time a new segment is found by one of the algorithms for automatically extracting new segments
    """
    
    #Access all extracted segments for the current road
    df_segments_automatic_current_road = df_segments_automatic[df_segments_automatic['road_id']==road_id]
    df_segments_automatic_current_road = df_segments_automatic_current_road.reset_index(drop=True)
    
    #Append new segment to list of segments
    df_segments_automatic_current_road = df_segments_automatic_current_road.append({'road_id': road_id, 'segment_s_start': s_start,
                                                                                    'segment_s_end': s_end}, ignore_index=True)
    
    #Get all unique s_start-values in a list
    list_s_start = pd.unique(df_segments_automatic_current_road['segment_s_start'])
    list_s_start= list_s_start.tolist()
    list_s_start.sort()
    
    #Get all unique s_end-values in a list
    list_s_end = pd.unique(df_segments_automatic_current_road['segment_s_end'].dropna())
    list_s_end= list_s_end.tolist()
    list_s_end.sort()
    
    #Empty DataFrame to fill in s_start and s_end in a sorted order
    df_segments_automatic_current_road = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
    
    #Iterate through list_s_start to create segments for every s-start in df_segments_automatic_current_road
    for current_s_start in list_s_start:
        
        #Append segments to list of segments
        df_segments_automatic_current_road = df_segments_automatic_current_road.append({'road_id': road_id, 'segment_s_start': current_s_start,
                                                                                        'segment_s_end': None}, ignore_index=True)
    #Iterate through list_s_end to find segment with closest s_start for each s_end
    for current_s_end in list_s_end:
        
        #Find index of closest s_start which is lower than s_end 
        index_paste_s_end =  bisect.bisect_right(list_s_start, current_s_end) - 1
        
        #Paste value for s_end in matching segment
        df_segments_automatic_current_road.loc[index_paste_s_end, 'segment_s_end'] = current_s_end
        
    #Delete old data for segments in current road from DataFrame with segments
    df_segments_automatic = df_segments_automatic.drop(df_segments_automatic[df_segments_automatic.road_id == road_id].index)
    
    #Append new data for segments in current road to DataFrame with segments
    df_segments_automatic = df_segments_automatic.append(df_segments_automatic_current_road)
    
    #Sort in added data
    df_segments_automatic = df_segments_automatic.sort_values(['road_id', 'segment_s_start'])
    df_segments_automatic = df_segments_automatic.reset_index(drop=True)
    
    return df_segments_automatic