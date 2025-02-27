import pandas as pd
from tqdm import tqdm

def A_5_find_overlappings_segments_laneSections(df_segments, df_lane_data_drivable_lanes, OpenDRIVE_object):
    """
    This function finds for every created BSSD-Segment the laneSections which overlap to this BSSD-Segment.
    Overlapping means in this context that the s-range of a segment intersects the s-range of a laneSection.

    Parameters
    ----------
    df_segments : DataFrame
        DataFrame which contains all created BSSD-segments.
    df_lane_data_drivable_lanes : DataFrame
        DataFrame that contains all lanes in the OpenDRIVE-file that represent a drivable OpenDRIVE-lane
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file

    Returns
    -------
    df_overlappings_segments_laneSections : DataFrame
        DataFrame which contains per segment one row for every laneSection that overlaps to this segment

    """
    
    #DataFrame to store the laneSections which overlap to a certain BSSD-Segment
    #columns "road_id" and "segment_s" are used to identify the segment
    #column "laneSection_s" includes the s_coordinate of the laneSection that overlaps to the segment
    #column "laneSection_object" includes the laneSection-object of the laneSection that overlaps to the segment
    df_overlappings_segments_laneSections = pd.DataFrame(columns = ['road_id', 'segment_s', 'laneSection_s', 'laneSection_object'])

    #Iteration through every road, which contains at least one BSSD-segment 
    for road_id in tqdm(df_segments['road_id'].unique()):
        
        #Get road-object of current road to access all laneSection-objects in current road
        road_object = OpenDRIVE_object.getRoad(int(road_id))
        
        #DataFrame which contains only information about the segments in the current road
        df_segments_current_road = df_segments[df_segments['road_id']==road_id]
        df_segments_current_road = df_segments_current_road.reset_index(drop=True)
        
        #Iteration through all segments of current road to find the corresponding laneSections which overlap to the BSSD-Segment
        for index, s_start_curr_segment in enumerate(df_segments_current_road.loc[:, 'segment_s_start']):
            
            #Check if current segment has a defined end (Attribute s_end) to get the s-coordinate where the segment ends
            #Case 1: Current segment has no defined end --> Segment ends where next segment starts/the road ends
            if pd.isnull(df_segments_current_road.loc[index, 'segment_s_end'])==True:
                
                #Check if a succeeding segment in current road is existing
                #Case 1: Succeeding segment existing
                if index < (len (df_segments_current_road)-1):
                    
                    #s-coordinate where segment ends is s-coordinate where succeeding segment starts
                    s_end_curr_segment = df_segments_current_road.loc[index+1, 'segment_s_start']
                    
                #Case 2: No suceeding segment existing --> segments ends at the end of the current road
                else:
                    
                    #s-coordinate where segment ends is the length of the road
                    s_end_curr_segment = road_object.length
                    
            #Case 2: Current segment has a defined end (Attribute s_end) 
            else:
                #s-coordinate where segment ends can be accessed directly from df_segments_current_road
                s_end_curr_segment = df_segments_current_road.loc[index, 'segment_s_end']
                
            #Variable to count how many laneSections overlap with the current BSSD-Segment
            number_overlappings_current_segment = 0
            
            #Iteration through laneSection-objects of current road to check for every laneSection whether it overlaps with the current segment
            for laneSection_object in road_object.lanes.lane_sections:
                
                #s-coordinate where current laneSection starts
                s_start_curr_laneSection = laneSection_object.sPos
                
                #Check if current laneSection contains at least one drivable lane
                #If not, skip this laneSection
                if any((df_lane_data_drivable_lanes.road_id == int(road_id)) & \
                       (round(df_lane_data_drivable_lanes.laneSection_s, 3) == round(s_start_curr_laneSection, 3))) == False:
                    continue
                
                #Check if there was already a laneSection found which overlaps to the current BSSD-Segment
                #If yes, add a tolerance of 1 cm to the s-start coordinate of the current laneSection to prevent that numerical errors lead to a
                #laneSection overlapping with two BSSD-Segments, which in reality only overlaps with one BSSD-Segment
                if number_overlappings_current_segment > 0:
                    s_start_curr_laneSection_with_tolerance = s_start_curr_laneSection + 0.01
                else:
                    s_start_curr_laneSection_with_tolerance = s_start_curr_laneSection
            
                #s-coordinate where current laneSection ends
                s_end_curr_laneSection = s_start_curr_laneSection + laneSection_object.length
                
                #Check if current segment and current laneSection overlap 
                #(No overlapping if start of segment/laneSection and end of laneSection/segment are equally)
                if max(s_start_curr_segment, s_start_curr_laneSection_with_tolerance)<\
                    min(s_end_curr_segment, s_end_curr_laneSection):
                    
                    #Append data of current laneSection to overall DataFrame df_overlappings_segments_laneSections
                    df_overlappings_segments_laneSections = df_overlappings_segments_laneSections.append({'road_id': int(road_id),
                                                                                                          'segment_s': s_start_curr_segment,
                                                                                                          'laneSection_s': s_start_curr_laneSection,
                                                                                                          'laneSection_object': laneSection_object},
                                                                                                         ignore_index=True)
                    
                    number_overlappings_current_segment = number_overlappings_current_segment + 1

    number_segments = len(df_segments)
    number_overlappings = len(df_overlappings_segments_laneSections)
    
    print()
    
    #User output
    #Singular or Plural in console output
    if number_overlappings == 1:
        print('Found ' + str(number_overlappings) + ' laneSection which overlaps with ' + str(number_segments) + ' BSSD-segment')
    elif (number_overlappings > 1) & (number_segments == 1):
        print('Found ' + str(number_overlappings) + ' laneSections which overlaps with ' + str(number_segments) + ' BSSD-segment')
    else:
        print('Found ' + str(number_overlappings) + ' laneSections which overlap with ' + str(number_segments) + ' BSSD-segments')
    
    return df_overlappings_segments_laneSections    