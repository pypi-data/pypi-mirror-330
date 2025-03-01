import pandas as pd
from tqdm import tqdm

def A_3_2_segments_by_starting_and_ending_drivable_lanes(df_lane_data, df_lane_data_drivable_lanes, df_segments_automatic,
                                                         roads_laneSections_equal_segments, OpenDRIVE_object):
    """
    This function extracts BSSD-segments (<segment>-elements) automatically based on rule 2:
        
        If a drivable lane starts/ends in a laneSection that has a preceding/succeeding laneSection, a new segment has to be defined 
        for the s-coordinate of this laneSection/the s-coordinate of the succeeding laneSection

    Parameters
    ----------
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file
    df_lane_data_drivable_lanes : DataFrame
        DataFrame which contains information about all lanes that represent a drivable OpenDRIVE-lane 
    df_segments_automatic : DataFrame
        DataFrame which contains the automatically extracted segments (result of execution of rule 1)
    roads_laneSections_equal_segments : list
        List containing id's of all roads where for every laneSection already segment has been extracted.
        If this is the case, execution of rule 2 can be skipped for these roads--> Optimization of computing time
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map

    Returns
    -------
    df_segments_automatic : DataFrame
        DataFrame which contains the automatically extracted segments based on rule 2. For every segment a start-s-coordinate is given. 
        If the segments ends before the next segment in the road or before the end of the road a end-s-coordinate is given.

    """
    
    #Import inside function necessary as otherwise a circular import would result
    from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_extract_segments_automatically import check_for_succeeding_lane_section_with_no_drivable_lanes
    from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_extract_segments_automatically import paste_segment
    
    print('2. Extracting segments by starting/ending drivable lanes...\n')
    
    #Variable for storing the number of segments before executing this function to know how many segments have been added based on this function
    number_segments_before = len(df_segments_automatic)
    
    #Iteration through all roads with at least one drivable lane to automatically extract segments by existing laneSections 
    #of OpenDRIVE-file
    for road_id in tqdm(df_lane_data_drivable_lanes['road_id'].unique()): 

        #Convert road_id to int as pd.unique() returns float values
        road_id = int(road_id)
        
        #Skip application of rule 2 for this road if already all laneSections in this road have lead to the extraction of a segment
        #--> In this case rule 2 won't find a new segment
        if (road_id in roads_laneSections_equal_segments)==True:
            continue
        
        #Road object of current road
        road_object = OpenDRIVE_object.getRoad(road_id)
        
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
        
        #Get all extracted segments in the current road
        segments_current_road = pd.unique(df_segments_automatic[df_segments_automatic['road_id']==road_id]['segment_s_start'])
        segments_current_road = segments_current_road.tolist()
        segments_current_road.sort()
        
        #Iterate through all laneSections with drivable lanes to check whether a segment has been extracted for this laneSection
        for index, s_laneSection in enumerate(laneSections_drivable_lanes):
            
            
            #drivable lanes in current laneSection
            drivable_lanes_current_laneSection = drivable_lanes_current_road[drivable_lanes_current_road['laneSection_s']==s_laneSection]
            drivable_lanes_current_laneSection = drivable_lanes_current_laneSection.reset_index(drop=True)
            
            
            #Get index of current laneSection in list with all laneSections of current road to access laneSection-object and 
            #to check whether a succeeding/preceding laneSection exists
            index_laneSection = laneSections_all_lanes.index(s_laneSection)
            
            #Get object for current laneSection
            laneSection_object = road_object.lanes.lane_sections[index_laneSection]
            
            #Iterate through all drivable lanes in current laneSection to check whether it has a succeeding/preceding lane in
            #succeeding/preceding laneSection (if existing)
            for lane_id in drivable_lanes_current_laneSection.loc[:, 'lane_id']:
                
                #Get object for current lane
                lane_object = laneSection_object.getLane(lane_id)
                
                #Skip roads that only contain one laneSection --> Have no succeeding/preceding laneSection
                if len(laneSections_all_lanes)==1:
                    break
                
                #Check if current lane has no preceding lane and a preceding laneSection is existing
                #If yes, a new segment has to be defined at the s-coordinate of current laneSection
                if (lane_object.link.predecessorId==None) & (index_laneSection > 0):
                    
                    #Check if segment has already been defined 
                    if (s_laneSection in segments_current_road) == False:
                    
                        #Check if suceeding laneSection has no drivable lanes
                        #If no, segment will get no "s_end"-attribute
                        if check_for_succeeding_lane_section_with_no_drivable_lanes(s_laneSection, laneSections_drivable_lanes,
                                                                                    laneSections_all_lanes)==False:

                            df_segments_automatic = paste_segment(df_segments_automatic, road_id, s_laneSection, None)
                            
                            segments_current_road.append(s_laneSection)
                            
                        #If yes, "s_end"-attribute has to be specified
                        else:
                            #s-start-coordinate of segment is s-coordinate of current laneSection
                            #s-coordinate where succeeding laneSection with no drivable lanes starts is end-s-coordinate of current laneSection
                            s_end = laneSections_all_lanes[laneSections_all_lanes.index(s_laneSection)+1]
                            
                            df_segments_automatic = paste_segment(df_segments_automatic, road_id, s_laneSection, s_end)
                            
                            segments_current_road.append(s_laneSection)
                            
                            
                #Check if current lane has no succeeding lane and a succeeding laneSection is existing
                #If yes, a new segment has to be defined at the s-coordinate of succeeding laneSection
                if (lane_object.link.successorId==None) & (index_laneSection < len(laneSections_all_lanes)-1):
                    
                    #s-coordinate of succeeding laneSection is s-start-coordinate of new segment
                    segment_s_start = laneSections_all_lanes[index_laneSection+1]
                    
                    #Add new segment only if succeeding laneSection contains at least one drivable lane
                    if (segment_s_start in laneSections_drivable_lanes)==True:
                    
                        #Check if segment has already been defined 
                        if (segment_s_start in segments_current_road) == False:
                            
                            #Check if suceeding laneSection of laneSection at segment_s_start has no drivable lanes
                            #If no, segment will get no "s_end"-attribute
                            if check_for_succeeding_lane_section_with_no_drivable_lanes(segment_s_start, laneSections_drivable_lanes,
                                                                                        laneSections_all_lanes)==False:
                                
                                df_segments_automatic = paste_segment(df_segments_automatic, road_id, segment_s_start, None)
                                
                                segments_current_road.append(segment_s_start)
                            
                            #If yes, "s_end"-attribute has to be specified
                            else:
                                #s-coordinate where succeeding laneSection with no drivable lanes starts is end-s-coordinate of current laneSection
                                s_end = laneSections_all_lanes[laneSections_all_lanes.index(segment_s_start)+1]
                                
                                df_segments_automatic = paste_segment(df_segments_automatic, road_id, segment_s_start, s_end)
                                
                                segments_current_road.append(s_laneSection)
                            
                        
    #Sort in added lanes
    df_segments_automatic = df_segments_automatic.sort_values(['road_id', 'segment_s_start'])
    df_segments_automatic = df_segments_automatic.reset_index(drop=True)
    
    #Convert values in column "road_id" to int 
    df_segments_automatic['road_id']=df_segments_automatic['road_id'].convert_dtypes()
    
    #Get number of extracted segments based on this function for user output
    number_of_extracted_segments = len(df_segments_automatic)-number_segments_before
    
    print()
    
    #User output
    if number_of_extracted_segments==1:
        print('Extracted ' + str(number_of_extracted_segments) + ' segment\n')
    else:
        print('Extracted ' + str(number_of_extracted_segments) + ' segments\n')
        
    return df_segments_automatic