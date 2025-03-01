import pandas as pd
from tqdm import tqdm


def A_3_1_segments_by_changing_number_of_drivable_lanes(df_lane_data, df_lane_data_drivable_lanes):
    """
    This function extracts BSSD-segments (<segment>-elements) automatically based on rule 1:
        
        If the number of drivable lanes changes from one laneSection to the next laneSection, a new segment has to 
        be defined.
    

    Parameters
    ----------
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file
    df_lane_data_drivable_lanes : DataFrame
        DataFrame which contains information about all lanes that represent a drivable OpenDRIVE-lane 

    Returns
    -------
    df_segments_automatic : DataFrame
        DataFrame which contains the automatically extracted segments based on rule 1. For every segment a start-s-coordinate is given. 
        If the segments ends before the next segment in the road or before the end of the road a end-s-coordinate is given.
    roads_laneSections_equal_segments : list
        List to insert id's of all roads where for every laneSection a segment has been extracted.
        If this is the case, rule 2 can be skipped for these roads --> Optimization of computing time

    """
    
    #Import inside function necessary as otherwise a circular import would result
    from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_extract_segments_automatically import check_for_succeeding_lane_section_with_no_drivable_lanes
    
    #Create DataFrame to store information about segments to be created 
    #Start-s-coordinate (s_start) of a segment has to be specified always. 
    #End-s-coordinate (s_end) has to be specified only if there is no succeeding segment and the road is defined further (BSSD definition gap)
    df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
    
    #Create list to insert id's of all roads where for every laneSection a segment has been extracted
    #If this is the case, execution of rule 2 can be skipped --> Optimization of computing time
    roads_laneSections_equal_segments = []

    print('1. Extracting segments by change in number of drivable lanes...\n')
    #Iteration through all roads with at least one drivable lane to automatically extract segments by existing laneSections 
    #of OpenDRIVE-file
    for road_id in tqdm(df_lane_data_drivable_lanes['road_id'].unique()):
                
        #Access all drivable lanes for the current road
        drivable_lanes_current_road = df_lane_data_drivable_lanes[df_lane_data_drivable_lanes['road_id']==road_id]
            
        #Get all laneSections in current road that contain at least one drivable lane
        laneSections_drivable_lanes = pd.unique(drivable_lanes_current_road['laneSection_s'])
        laneSections_drivable_lanes = laneSections_drivable_lanes.tolist()
        laneSections_drivable_lanes.sort()
        
        #Access all lanes for the current road to check whether there are laneSections with no drivable lanes
        all_lanes_current_road = df_lane_data[df_lane_data['road_id']==road_id]
        
        #Get all laneSections in current road 
        laneSections_all_lanes = pd.unique(all_lanes_current_road['laneSection_s'])
        laneSections_all_lanes = laneSections_all_lanes.tolist()
        laneSections_all_lanes.sort()
        
        #Variable for storing number of drivable lanes in previous laneSection to detect changes in number of drivable lanes
        number_drivable_lanes_previous_laneSection = None
        
        #Iteration through laneSections with at least one drivable lane
        for s_laneSection in laneSections_drivable_lanes:
            
            #drivable lanes in current laneSection
            drivable_lanes_current_laneSection = drivable_lanes_current_road[drivable_lanes_current_road['laneSection_s']==s_laneSection]
            
            #Number of drivable lanes in current laneSection 
            number_drivable_lanes = len(drivable_lanes_current_laneSection)
            
            #No previous laneSection existing --> means that current laneSection is the first laneSection with at least one drivable lane
            #-->A segment always has to start at this s-position
            if number_drivable_lanes_previous_laneSection == None:
                
                #Check if suceeding laneSection has no drivable lanes
                #If no, segment will get no "s_end"-attribute
                if check_for_succeeding_lane_section_with_no_drivable_lanes(s_laneSection, laneSections_drivable_lanes,
                                                                            laneSections_all_lanes)==False:
                    df_segments_automatic = df_segments_automatic.append({'road_id': road_id, 'segment_s_start': s_laneSection,
                                                                          'segment_s_end': None}, ignore_index=True)
                    
                    number_drivable_lanes_previous_laneSection = number_drivable_lanes
                
                #If yes, "s_end"-attribute has to be specified
                else:
                    #s-coordinate where succeeding laneSection with no drivable lanes starts is end-s-coordinate of current laneSection
                    s_end = laneSections_all_lanes[laneSections_all_lanes.index(s_laneSection)+1]
                    
                    df_segments_automatic = df_segments_automatic.append({'road_id': road_id, 'segment_s_start': s_laneSection,
                                                                          'segment_s_end': s_end}, ignore_index=True)
                    
                    number_drivable_lanes_previous_laneSection = None
                    
            #Previous laneSection existing
            else:
                #Check if number of drivable lanes has changed in comparison to previous laneSection, 
                #If yes, a segment has to start at this s-coordinate
                if number_drivable_lanes != number_drivable_lanes_previous_laneSection:
                   
                    #Check if suceeding laneSection has no drivable lanes
                    #If no, segment will get no "s_end"-attribute
                    if check_for_succeeding_lane_section_with_no_drivable_lanes(s_laneSection, laneSections_drivable_lanes,
                                                                                laneSections_all_lanes)==False:
                        df_segments_automatic = df_segments_automatic.append({'road_id': road_id, 'segment_s_start': s_laneSection,
                                                                              'segment_s_end': None}, ignore_index=True)
                        
                        number_drivable_lanes_previous_laneSection = number_drivable_lanes
                        
                    #If yes, "s_end"-attribute has to be specified
                    else:
                        #s-coordinate where succeeding laneSection with no drivable lanes starts is end-s-coordinate of current laneSection
                        s_end = laneSections_all_lanes[laneSections_all_lanes.index(s_laneSection)+1]
                        
                        df_segments_automatic = df_segments_automatic.append({'road_id': road_id, 'segment_s_start': s_laneSection,
                                                                              'segment_s_end': s_end}, ignore_index=True)
                        
                        number_drivable_lanes_previous_laneSection = None
                
                #If no, it is not sure that a segment starts at this s-coordinate
                #But it has to be checked if there is a succeeding laneSection with no drivable lane as then s_end has to be defined for last
                #defined segment
                else:
                    #Check if suceeding laneSection has no drivable lanes
                    if check_for_succeeding_lane_section_with_no_drivable_lanes(s_laneSection, laneSections_drivable_lanes,
                                                                                laneSections_all_lanes)==True:
                        
                        #s-coordinate where succeeding laneSection with no drivable lanes starts is end-s-coordinate of current laneSection
                        s_end = laneSections_all_lanes[laneSections_all_lanes.index(s_laneSection)+1]
                        #The last defined segment has a defined s_end at the s-coordinate where the laneSection with no drivable lanes starts
                        df_segments_automatic.loc[len(df_segments_automatic)-1, 'segment_s_end']=s_end
                        
                        #Set number of drivable lanes of previous laneSection to None so that a segment is created at first laneSection 
                        #with drivable lanes after laneSection with no drivable lanes
                        number_drivable_lanes_previous_laneSection = None
        
        #Get all extracted segments in the current road to check if application of Rule 2 is necessary
        segments_current_road = pd.unique(df_segments_automatic[df_segments_automatic['road_id']==road_id]['segment_s_start'])
        segments_current_road = segments_current_road.tolist()
        segments_current_road.sort()  
        
        #If all laneSections in current road have lead to a new segment due to rule 1, no application of rule 2 for this road is necessary 
        if laneSections_all_lanes == segments_current_road:
            roads_laneSections_equal_segments.append(road_id)
        
    #Convert values in column "road_id" to int 
    df_segments_automatic['road_id']=df_segments_automatic['road_id'].convert_dtypes()
    
    print()
    #User output: Number of created segments based on this function
    if len(df_segments_automatic)==1:
        print('Extracted ' + str(len(df_segments_automatic)) + ' segment\n')
    else:
        print('Extracted ' + str(len(df_segments_automatic)) + ' segments\n')
    
    
    return df_segments_automatic, roads_laneSections_equal_segments