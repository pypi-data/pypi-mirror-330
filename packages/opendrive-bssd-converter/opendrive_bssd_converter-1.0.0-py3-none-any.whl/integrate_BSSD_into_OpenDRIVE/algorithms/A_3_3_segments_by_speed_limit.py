import pandas as pd
from tqdm import tqdm

def A_3_3_segments_by_speed_limit(df_lane_data, df_lane_data_drivable_lanes, df_segments_automatic, OpenDRIVE_object):
    """
    This function extracts BSSD-segments (<segment>-elements) automatically based on rule 3:
        
        If the speed limit for a drivable lane changes, a new segment has to be defined

    Parameters
    ----------
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file
    df_lane_data_drivable_lanes : DataFrame
        DataFrame which contains information about all lanes that represent a drivable OpenDRIVE-lane 
    df_segments_automatic : DataFrame
        DataFrame which contains the automatically extracted segments (result of execution of rule 1 and rule 2)
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map

    Returns
    -------
    df_segments_automatic : DataFrame
        DataFrame which contains the automatically extracted segments based on rule 3. For every segment a start-s-coordinate is given. 
        If the segments ends before the next segment in the road or before the end of the road a end-s-coordinate is given.
    df_speed_limits : DataFrame
        DataFrame which contains one row for every <speed>-element (defined in the OpenDRIVE-<lane>-elements)
        which is defined in the imported OpenDRIVE-file for a drivable lane
        

    """
    
    #Import inside function necessary as otherwise a circular import would result
    from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_extract_segments_automatically import paste_segment
    
    
    #DataFrame for storing the data of the <speed>-elements, which are definied in the OpenDRIVE-<lane>-elements
    #For every <speed>-element a row is defined. The columns sOffset, speed_max and unit contain the s-coordinate from where the speed limit
    #is valid, the speed limit itself and the unit in which the speed limit is defined
    df_speed_limits = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'sOffset', 'speed_max', 'unit'])
    
    print('3. Extracting segments by speed limits for drivable lanes...\n')
    
    #Variable for storing the number of segments before executing this function to know how many segments have been added based on this function
    number_segments_before = len(df_segments_automatic)
    
    #Iteration through all roads with at least one drivable lane to automatically extract segments by speed limits of drivable lanes
    for road_id in tqdm(df_lane_data_drivable_lanes['road_id'].unique()):
        
        #Access all drivable lanes for the current road
        drivable_lanes_current_road = df_lane_data_drivable_lanes[df_lane_data_drivable_lanes['road_id']==road_id]
        
        #Convert road_id to int as pd.unique() returns float values
        road_id = int(road_id)
        
        #Road object of current road
        road_object = OpenDRIVE_object.getRoad(road_id)
        
        #Access all drivable lanes for the current road
        drivable_lanes_current_road = df_lane_data_drivable_lanes[df_lane_data_drivable_lanes['road_id']==road_id]
        
        #Get all laneSections in current road that contain at least one drivable lane
        laneSections_drivable_lanes = pd.unique(drivable_lanes_current_road['laneSection_s'])
        laneSections_drivable_lanes = laneSections_drivable_lanes.tolist()
        laneSections_drivable_lanes.sort()
        
        #Access all lanes for the current road 
        all_lanes_current_road = df_lane_data[df_lane_data['road_id']==road_id]
        
        #Get all laneSections in current road 
        laneSections_all_lanes = pd.unique(all_lanes_current_road['laneSection_s'])
        laneSections_all_lanes = laneSections_all_lanes.tolist()
        laneSections_all_lanes.sort()
        
        #Get all extracted segments in the current road
        segments_current_road = pd.unique(df_segments_automatic[df_segments_automatic['road_id']==road_id]['segment_s_start'])
        segments_current_road = segments_current_road.tolist()
        segments_current_road.sort()
        
        #Iterate through all laneSections with drivable lanes to iterate through all drivable lanes
        for index, s_laneSection in enumerate(laneSections_drivable_lanes):
            
            #drivable lanes in current laneSection
            drivable_lanes_current_laneSection = drivable_lanes_current_road[drivable_lanes_current_road['laneSection_s']==s_laneSection]
            drivable_lanes_current_laneSection = drivable_lanes_current_laneSection.reset_index(drop=True)
            
            #Get index of current laneSection in list with all laneSections of current road to access laneSection-object and 
            #to check whether a succeeding/preceding laneSection exists
            index_laneSection = laneSections_all_lanes.index(s_laneSection)
            
            #Get object for current laneSection
            laneSection_object = road_object.lanes.lane_sections[index_laneSection]
            
            #Iterate through all drivable lanes in current laneSection to iterate through all <speed>-elements of all drivable lanes
            for lane_id in drivable_lanes_current_laneSection.loc[:, 'lane_id']:
                
                #Get object for current lane
                lane_object = laneSection_object.getLane(lane_id)
                
                #Variable for storing speed limit of preceding <speed>-element in current lane --> Needed for comparing old with new value
                speed_max_preceding_speed_element = None
                
                #Iterate through all <speed>-elements in current lane to extract segments based on the speed limits 
                for index_speed, speed_object in enumerate(lane_object.speeds):
                    
                    speed_max_current_speed_object = speed_object.vMax
                    sOffset_current_speed_object =  speed_object.sOffset
                    
                    #Skip <speed>-element if speed limit is below zero (In some files value "-1" is used when no data is available)
                    if speed_max_current_speed_object<0:
                        speed_max_preceding_speed_element = None
                        continue
                    
                    #Append data of <speed>-element to df_speed_limits
                    df_speed_limits = df_speed_limits.append({'road_id': road_id, 'laneSection_s': s_laneSection, 'lane_id': lane_id,
                                                              'sOffset': sOffset_current_speed_object,
                                                              'speed_max': speed_max_current_speed_object,
                                                              'unit': speed_object.unit}, ignore_index=True)
                    
                                                
                    #If a new segment is defined based on current <speed>-element, the s-coordinate of new segment would be the sum 
                    #of s-coordinate of laneSection and sOffset of <speed>-Element
                    segment_s_start = s_laneSection + sOffset_current_speed_object
                    
                    #Check if current <speed>-element is the first <speed>-element in this lane
                    #If yes, it has to be checked whether there is a preceding speed-object with the same speed limit
                    if index_speed == 0:
                        
                        #If sOffset is >0 and <speed>-element is the first in this lane, there is no defined preceding speed limit
                        #--> New segment has to be defined as speed limit changes from undefined to a defined value
                        if sOffset_current_speed_object>0:
  
                            df_segments_automatic = paste_segment(df_segments_automatic, road_id, segment_s_start, None)
                            segments_current_road.append(segment_s_start)
                        
                        #If sOffset is 0, it has to be checked if a preceding lane is existing, which has a defined speed-limit
                        else:
                            
                            #Check for first <speed>-element in lane with sOffset=0 if a segment has already been defined for this s-coordinate
                            #If yes, the current lane can be skipped to improve computing time
                            if (segment_s_start in segments_current_road) == True:
                                speed_max_preceding_speed_element = speed_max_current_speed_object
                                continue
                            
                            #If current lane has no preceding lane, there is no defined preceding speed limit
                            #--> New segment has to be defined as speed limit changes from undefined to a defined value
                            if lane_object.link.predecessorId==None:
                                
                                df_segments_automatic = paste_segment(df_segments_automatic, road_id, segment_s_start, None)
                                segments_current_road.append(segment_s_start)
                                
                            else:
                                #Check if current laneSection is the first laneSection with drivable lanes in the current road
                                #If yes, there is no defined preceding speed limit
                                #--> New segment has to be defined as speed limit changes from undefined to a defined value
                                if index==0:
                                    df_segments_automatic = paste_segment(df_segments_automatic, road_id, segment_s_start, None)
                                    segments_current_road.append(segment_s_start)
                                    
                                #If no, it has to be checked whether a preceding defined speed limit is existing
                                else:
                                    
                                    lane_id_predecessor = lane_object.link.predecessorId
                                    
                                    #Get s-coordinate of preceding laneSection (contains lane, which is the predecessor of the current lane)
                                    s_preceding_lane_section = laneSections_all_lanes[index_laneSection -1]
                                    
                                    
                                    #Get all <speed>-elements of preceding lane
                                    df_speed_limit_preceding_lane = df_speed_limits[(df_speed_limits['road_id']==road_id)\
                                                        & (round(df_speed_limits['laneSection_s'], 3)==round(s_preceding_lane_section, 3))\
                                                        & (df_speed_limits['lane_id']==lane_id_predecessor)]
                                    df_speed_limit_preceding_lane = df_speed_limit_preceding_lane.reset_index(drop=True)
                                
                                
                                    #Check if preceding lane has any <speed>-elements
                                    #If no, a new segment has to be defined as speed limit changes from undefined to a defined value
                                    if len(df_speed_limit_preceding_lane)==0:
                                        df_segments_automatic = paste_segment(df_segments_automatic, road_id, segment_s_start, None)
                                        segments_current_road.append(segment_s_start)
                                        
                                    #If yes, it has to be checked whether the speed-limit has changed 
                                    else:
                                        #Get speed-limit of the last valid <speed>-element of preceding lane (Highest value for sOffset)
                                        speed_max_preceding_lane = df_speed_limit_preceding_lane.loc[df_speed_limit_preceding_lane['sOffset'].idxmax(), 'speed_max']
                                        
                                        #Create new segment if speed-limit has changed from preceding lane to current lane
                                        if round(speed_max_current_speed_object, 3)!=round(speed_max_preceding_lane, 3):
                                            df_segments_automatic = paste_segment(df_segments_automatic, road_id, segment_s_start, None)
                                            segments_current_road.append(segment_s_start)
                    
                    #Current <speed>-element is not the first <speed>-element in current lane
                    else:
                        
                        #Create new segment if speed-limit has changed from preceding <speed>-element to current lane-element
                        if round(speed_max_current_speed_object, 3)!=round(speed_max_preceding_speed_element, 3):
                            df_segments_automatic = paste_segment(df_segments_automatic, road_id, segment_s_start, None)
                            segments_current_road.append(segment_s_start)
                            
                    #Set speed limit of current <speed>-element as the "old" speed limit
                    speed_max_preceding_speed_element = speed_max_current_speed_object
                        
                                        
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
        
        
    return df_segments_automatic, df_speed_limits
        
        
        
        
        