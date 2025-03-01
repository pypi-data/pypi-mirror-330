import pandas as pd
from tqdm import tqdm
import bisect

from integrate_BSSD_into_OpenDRIVE.utility.classify_BSSD_lane_borders import classify_BSSD_lane_borders
from integrate_BSSD_into_OpenDRIVE.utility.check_for_separated_BSSD_lane import check_for_separated_BSSD_lane


def A_7_1_extract_speed_attribute(df_lane_data, df_BSSD_lanes, df_link_BSSD_lanes_with_OpenDRIVE_lanes, df_speed_limits, df_segments, driving_direction, 
                                  OpenDRIVE_object):
    """
    This function extracts the BSSD behavioral attribute "speed" based on the speed limits defined in the imported OpenDRIVE-file.
    The basis for this is "df_speed_limits" which contains all <speed>-elements, which are defined for the OpenDRIVE-lanes.
    
    The function is divided in two main parts:
        1. Extraction of the speed attribute along the driving direction of the BSSD-lanes
            --> For every BSSD-lane the first overlapping OpenDRIVE-lane is used. If there is a speed-limit defined in this OpenDRIVE-lane
            at the whole s-range of the BSSD-lane, this speed limit can be used for the BSSD attribute speed along the driving direction of
            the BSSD-lane.
        2. Extraction of the speed attribute against the driving direction of the BSSD-lanes
            --> The value of the speed attribute against the driving direction depends on whether there are drivable lanes on the other side of 
            the road and whether the other side of the road is separated. Depending on that the speed limit
            against the driving direction is equal to the speed limit along the driving direction or it is equal to a speed limit from a BSSD-lane
            from the other side of the road
    
    
    Parameters
    ----------
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file.
    df_BSSD_lanes : DataFrame
        DataFrame containing all created BSSD-lanes. For every BSSD-lane the object for the first laneSection overlapping is stored
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

    Returns
    -------
    df_BSSD_speed_attribute : DataFrame
        DataFrame storing information about BSSD speed attribute of BSSD-lanes. For every BSSD-lane the value for speed for behaviorAlong and 
        behaviorAgainst is stored (even if the value couldn't be extracted).
    
    """

    
    #Create DataFrame to store information about BSSD speed attribute of BSSD-lanes
    #Columns 'speed_behavior_along'/'speed_behavior_against' contain the value of the attribute "max" for the behavioral attribute 'speed'
    #in/against reference direction
    #If no data can be extracted automatically from the OpenDRIVE-file the value for is set to None
    df_BSSD_speed_attribute = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along', 'speed_behavior_against'])
    
    print('1. Extracting behavioral attribute "speed"...\n')
    
    #-------------------------------------------------------------------------------
    #1. SPEED LIMIT ALONG DRIVING DIRECTION
    print('1.1 Extracting behavioral attribute "speed" along driving direction...\n')
    
    #Manually create index for succeeding for-loop (Necessary to realize visualiziation with tqdm)
    index_BSSD_lane = 0
    
    #Iteration through all BSSD lanes (df_BSSD_lanes) to automatically extract the speed-attribute along driving direction for the BSSD-lanes
    for lane_id_BSSD in tqdm(df_BSSD_lanes.loc[:, 'lane_id_BSSD']):
        
        #Variables for storing BSSD behavioral attribute speed in reference direction for current BSSD-lane
        speed_behavior_along = None
        #Variables for storing BSSD behavioral attribute speed against reference direction for current BSSD-lane
        speed_behavior_against = None
        
        #road_id of current BSSD-lane
        road_id = df_BSSD_lanes.loc[index_BSSD_lane, 'road_id']
        
        #s-coordinate of segment of current BSSD-lane
        segment_s = df_BSSD_lanes.loc[index_BSSD_lane, 'segment_s']
        
        #Access all OpenDRIVE-lanes overlapping with the current BSSD-lane (df_link_BSSD_lanes_with_OpenDRIVE_lanes)
        #The aim is to find the first overlapping OpenDRIVE-lane --> For this lane it is checked whether a speed limit is defined
        df_overlapping_OpenDRIVE_lanes_current_BSSD_lane = df_link_BSSD_lanes_with_OpenDRIVE_lanes[
                                                            (df_link_BSSD_lanes_with_OpenDRIVE_lanes['road_id']==road_id) \
                                                            & (round(df_link_BSSD_lanes_with_OpenDRIVE_lanes['segment_s'], 3) == round(segment_s, 3)) \
                                                            & (df_link_BSSD_lanes_with_OpenDRIVE_lanes['lane_id_BSSD']==lane_id_BSSD)]
        df_overlapping_OpenDRIVE_lanes_current_BSSD_lane = df_overlapping_OpenDRIVE_lanes_current_BSSD_lane.reset_index(drop=True)
            
        #Get index of row which contains the first OpenDRIVE-lane which overlaps with the current BSSD-lane
        index_first_overlapping_laneSection = df_overlapping_OpenDRIVE_lanes_current_BSSD_lane['laneSection_s'].idxmin()
        
        #Get laneSection and lane_id of first OpenDRIVE-lane overlapping with the current BSSD-lane to check for speed limits
        laneSection_first_overlapping_lane = df_overlapping_OpenDRIVE_lanes_current_BSSD_lane.loc[index_first_overlapping_laneSection,
                                                                                                  'laneSection_s']
        lane_id_first_overlapping_lane = int(df_overlapping_OpenDRIVE_lanes_current_BSSD_lane.loc[index_first_overlapping_laneSection,
                                                                                                  'lane_id_OpenDRIVE'])
        
        #Get all speed limits which are defined for the first overlapping OpenDRIVE-lane to extract BSSD attribute speed
        df_speed_limits_first_overlapping_lane = df_speed_limits[(df_speed_limits['road_id']==road_id) \
                                            & (round(df_speed_limits['laneSection_s'], 3) == round(laneSection_first_overlapping_lane, 3)) \
                                            & (df_speed_limits['lane_id']==lane_id_first_overlapping_lane)]
        df_speed_limits_first_overlapping_lane = df_speed_limits_first_overlapping_lane.reset_index(drop=True)
        
        #Check if a speed limit has been defined for first overlapping OpenDRIVE-lane
        #--> If no speed limit has been defined for first overlapping OpenDRIVE-lane, no BSSD speed attribute can be extracted along driving direction
        
        #Case: A speed limit has been defined for first overlapping OpenDRIVE-lane
        if len(df_speed_limits_first_overlapping_lane) > 0:
            
            #Get list which contains all speed limits of first overlapping OpenDRIVE_lane with absolute s-values
            #(= s-coordinate of laneSection + sOffset of speed limit)
            list_speed_limits_absolute_s_values = df_speed_limits_first_overlapping_lane['laneSection_s'] + \
                                                  df_speed_limits_first_overlapping_lane['sOffset']
            
            #Find index of speed limit which is valid in the BSSD-lane (= speed limit with highest sOffset lower/equal to segment_s)
            index_speed_limit_valid =  bisect.bisect_right(list_speed_limits_absolute_s_values, segment_s) - 1
            
            #If index is below 0, no speed limit is valid for the current BSSD-lane
            # --> If s-coordinate of the first speed limit defined for the first overlapping OpenDRIVE-lane is higher than s-coordinate
            #of current segment, no speed limit is defined for the current BSSD-lane
            
            #Case: Index is >=0 --> speed limit is valid for the current BSSD-lane
            if index_speed_limit_valid >= 0:
                
                #Get speed limit which is valid in the BSSD-lane in driving direction
                speed_limit_in_driving_direction = df_speed_limits_first_overlapping_lane.loc[index_speed_limit_valid, 'speed_max']
                
                #Check if OpenDRIVE-file is based on RHT or LHT (to know whether behaviorAlong or behaviorAgainst is the driving direction)
                #Case 1: RHT
                if driving_direction=='RHT':
                    
                    #Check if BSSD-lane belongs to right or left side of the road
                    #If lane-id < 0: Right side of the road
                    if lane_id_BSSD < 0:
                        
                        #Combination of RHT and right side of the road means that driving direction is along reference direction --> behaviorAlong
                        speed_behavior_along = speed_limit_in_driving_direction
                    
                    #If lane-id > 0: Left side of the road
                    else:
                    
                        #Combination of RHT and left side of the road means that driving direction is against reference direction --> behaviorAgainst
                        speed_behavior_against = speed_limit_in_driving_direction
                
                #Case 2: LHT     
                else:
                    
                    #Check if BSSD-lane belongs to right or left side of the road
                    #If lane-id < 0: Right side of the road
                    if lane_id_BSSD < 0:
                        
                        #Combination of LHT and right side of the road means that driving direction is against reference direction --> behaviorAgainst
                        speed_behavior_against = speed_limit_in_driving_direction
                        
                    #If lane-id > 0: Left side of the road
                    else:
                        
                        #Combination of LHT and left side of the road means that driving direction is is along reference direction --> behaviorAlong
                        speed_behavior_along = speed_limit_in_driving_direction
                        
                
                ##Special case: OpenDRIVE-lanes with attribute "type" = 'bidirectional' --> Lane is driven in both directions
                #--> Speed limit is identical for both driving directions
                #Get object of first overlapping OpenDRIVE-lane to check the "type"-attribute of this lane
                lane_object_first_overlapping_lane = OpenDRIVE_object.getRoad(road_id).lanes.getLaneSection(laneSection_first_overlapping_lane).\
                                                    getLane(lane_id_first_overlapping_lane)
                                                  
                #Set speed limit for both driving directions if BSSD-lane is represented by an OpenDRIVE-lane which is bidirectional
                if lane_object_first_overlapping_lane.type=='bidirectional':
                    speed_behavior_along = speed_limit_in_driving_direction
                    speed_behavior_against = speed_limit_in_driving_direction
                
                
            
        #Append values for BSSD speed attribute in current BSSD-lane to df_BSSD_speed_attribute (even if values are None)
        df_BSSD_speed_attribute = df_BSSD_speed_attribute.append({'road_id': road_id, 'segment_s': segment_s, 'lane_id_BSSD': lane_id_BSSD,
                                                                  'speed_behavior_along': speed_behavior_along, 
                                                                  'speed_behavior_against': speed_behavior_against}, ignore_index=True) 
        
        index_BSSD_lane = index_BSSD_lane + 1
            
    
    #Get number of found speed attributes along driving direction
    if driving_direction == 'RHT':
        
        df_along_driving_direction = df_BSSD_speed_attribute[( (df_BSSD_speed_attribute['lane_id_BSSD']<0) & \
                                                             (pd.isnull(df_BSSD_speed_attribute['speed_behavior_along'])==False) ) \
                                                             | ( (df_BSSD_speed_attribute['lane_id_BSSD']>0) & \
                                                             (pd.isnull(df_BSSD_speed_attribute['speed_behavior_against'])==False) )]
        
        number_found_speed_attributes_along_driving_direction = len(df_along_driving_direction)
    else:
        
        df_along_driving_direction = df_BSSD_speed_attribute[( (df_BSSD_speed_attribute['lane_id_BSSD']<0) & \
                                                             (pd.isnull(df_BSSD_speed_attribute['speed_behavior_against'])==False) ) \
                                                             | ( (df_BSSD_speed_attribute['lane_id_BSSD']>0) & \
                                                             (pd.isnull(df_BSSD_speed_attribute['speed_behavior_along'])==False) )]
        
        number_found_speed_attributes_along_driving_direction = len(df_along_driving_direction)
    
    print()
    
    #User output
    if number_found_speed_attributes_along_driving_direction==1:
        print('Extracted behavioral attribute "speed" along driving direction for ' + str(number_found_speed_attributes_along_driving_direction) +\
              ' BSSD-lane\n')
    else:
        print('Extracted behavioral attribute "speed" along driving direction for ' + str(number_found_speed_attributes_along_driving_direction) +\
              ' BSSD-lanes\n')
    
    #If no value for the speed attribute could be found, skip execution of second step (Extraction of attribute speed against driving direction)
    if number_found_speed_attributes_along_driving_direction == 0:
        
        #Convert values in columns "road_id", "lane_id_BSSD" to int 
        df_BSSD_speed_attribute['road_id']=df_BSSD_speed_attribute['road_id'].convert_dtypes()
        df_BSSD_speed_attribute['lane_id_BSSD']=df_BSSD_speed_attribute['lane_id_BSSD'].convert_dtypes()
        
        return df_BSSD_speed_attribute
    
    #-------------------------------------------------------------------------------
    #2. SPEED LIMIT AGAINST DRIVING DIRECTION
    
    #Preprocessing: Execute function to classify for every BSSD-lane the right and left border as crossable/not-crossable.
    #This is done on the one hand based on the type of the neighbouring lanes and on the other hand based on the objects in the OpenDRIVE-file
    #The informations about the crossability of the borders of a BSSD-lane are needed to define the behavioral attribute "speed" against the driving
    #direction
    df_BSSD_lanes_borders_crossable = classify_BSSD_lane_borders(df_lane_data, df_BSSD_lanes, df_segments, df_link_BSSD_lanes_with_OpenDRIVE_lanes,
                                                                 OpenDRIVE_object)
    
    print()
    print('1.2 Extracting behavioral attribute "speed" against driving direction...\n')
    
    #Manually creating index for succeeding for-loop (Necessary to realize visualiziation with tqdm)
    index_BSSD_lane = 0
    
    #Iteration through all BSSD lanes (df_BSSD_speed_attribute) to automatically extract
    #the speed-attribute against driving direction
    for lane_id_BSSD in tqdm(df_BSSD_speed_attribute.loc[:, 'lane_id_BSSD']):
        
        #road_id of current BSSD-lane
        road_id = df_BSSD_speed_attribute.loc[index_BSSD_lane, 'road_id']
        
        #s-coordinate of segment of current BSSD-lane
        segment_s = df_BSSD_speed_attribute.loc[index_BSSD_lane, 'segment_s']
        
        #Get value for speed attribute which was extracted before (along driving direction)
        speed_behavior_along = df_BSSD_speed_attribute.loc[index_BSSD_lane, 'speed_behavior_along']
        speed_behavior_against = df_BSSD_speed_attribute.loc[index_BSSD_lane, 'speed_behavior_against']
        
        #Check for special case that speed attribute is already extracted for both driving directions (Only the case if BSSD-lane is linked to 
        #an OpenDRIVE-lane of type "bidirectional") --> Current BSSD-lane can be skipped as speed for both directions is already extracted
        if (pd.isnull(speed_behavior_along)==False) and (pd.isnull(speed_behavior_against)==False):
            index_BSSD_lane = index_BSSD_lane + 1
            continue
        
        #Get side of the road where current BSSD-lane is defined
        #If id of BSSD-lane is < 0, lane is on the right side of the road
        if lane_id_BSSD < 0:
            
            #Store information about side of current BSSD-lane
            side_current_BSSD_lane = 'right'
            
            #Get all BSSD-lane which are defined in the current segment for the other side of the road (In this case, the left side)
            df_BSSD_lanes_other_side = df_BSSD_lanes[(df_BSSD_lanes['road_id']==road_id) \
                                                & (round(df_BSSD_lanes['segment_s'], 3) == round(segment_s, 3)) \
                                                & (df_BSSD_lanes['lane_id_BSSD']>0)]
            df_BSSD_lanes_other_side = df_BSSD_lanes_other_side.reset_index(drop=True)
                
            
        ##If id of BSSD-lane is > 0 (zero not possible), lane is on the left side of the road
        else:
            
            #Store information about side of current BSSD-lane
            side_current_BSSD_lane = 'left'
            
            #Get all BSSD-lane which are defined in the current segment for the other side of the road (In this case, the right side)
            df_BSSD_lanes_other_side = df_BSSD_lanes[(df_BSSD_lanes['road_id']==road_id) \
                                                & (round(df_BSSD_lanes['segment_s'], 3) == round(segment_s, 3)) \
                                                & (df_BSSD_lanes['lane_id_BSSD']<0)]
            df_BSSD_lanes_other_side = df_BSSD_lanes_other_side.reset_index(drop=True)    
            
        #Check if no BSSD-lanes are defined for the other side of the road (= One way road, dt.: "Einbahnstraße")
        #If yes, only one driving direction exists/contains drivable lanes --> behavior attribute "speed" in current BSSD-lane 
        #is identical in both driving directions
        if len(df_BSSD_lanes_other_side)==0:
            
            #Set speed attribute identical for both driving directions in current BSSD-lane 
            df_BSSD_speed_attribute = set_identical_speed_attribute(speed_behavior_along, speed_behavior_against, df_BSSD_speed_attribute,
                                                                    index_BSSD_lane)
            
            index_BSSD_lane = index_BSSD_lane + 1

            
        #If BSSD-lanes are defined for both sides of the road in the current segment, it has to be checked whether the current BSSD-lane is 
        #separated from the BSSD-lanes on the other side of the road (opposite driving direction)
        else:
            
            #Check if the current BSSD-lane is separated from the BSSD-lanes on the other side of the road
            #(function "check_for_separated_BSSD_lane")
            #If yes, behavior attribute "speed" in current BSSD-lane is identical in both driving directions (see case one way road)
            if check_for_separated_BSSD_lane(road_id, segment_s, lane_id_BSSD, df_BSSD_lanes, df_BSSD_lanes_borders_crossable)==True:
                
                #Set speed attribute identical for both driving directions in current BSSD-lane
                df_BSSD_speed_attribute = set_identical_speed_attribute(speed_behavior_along, speed_behavior_against, df_BSSD_speed_attribute,
                                                                        index_BSSD_lane)
                
                index_BSSD_lane = index_BSSD_lane + 1
                
            #If no, behavior attribute "speed" in current BSSD-lane against driving direction has to be extracted from the innermost BSSD-lane
            #on the other side of the road, where a speed attribute along driving direction has been defined
            else:
                
                #Execute function to set speed attribute of current BSSD-lane against driving direction based on speed-attribute of innermost
                #BSSD-lane on the other side of the road
                df_BSSD_speed_attribute = set_speed_attribute_based_on_other_side(road_id, segment_s,
                                                                                    lane_id_BSSD, index_BSSD_lane, side_current_BSSD_lane,
                                                                                    driving_direction, df_BSSD_speed_attribute)
    
                index_BSSD_lane = index_BSSD_lane + 1
    
    
    #Get number of found speed attributes against driving direction
    if driving_direction == 'RHT':
        
        df_against_driving_direction = df_BSSD_speed_attribute[( (df_BSSD_speed_attribute['lane_id_BSSD']<0) & \
                                                             (pd.isnull(df_BSSD_speed_attribute['speed_behavior_against'])==False) ) \
                                                             | ( (df_BSSD_speed_attribute['lane_id_BSSD']>0) & \
                                                             (pd.isnull(df_BSSD_speed_attribute['speed_behavior_along'])==False) )]
        
        number_found_speed_attributes_against_driving_direction = len(df_against_driving_direction)
    else:
        
        df_against_driving_direction = df_BSSD_speed_attribute[( (df_BSSD_speed_attribute['lane_id_BSSD']<0) & \
                                                             (pd.isnull(df_BSSD_speed_attribute['speed_behavior_along'])==False) ) \
                                                             | ( (df_BSSD_speed_attribute['lane_id_BSSD']>0) & \
                                                             (pd.isnull(df_BSSD_speed_attribute['speed_behavior_against'])==False) )]
        
        number_found_speed_attributes_against_driving_direction = len(df_against_driving_direction)
    
    print()
    
    #User output
    if number_found_speed_attributes_against_driving_direction==1:
        print('Extracted behavioral attribute "speed" against driving direction for ' + str(number_found_speed_attributes_against_driving_direction)\
              + ' BSSD-lane\n')
    else:
        print('Extracted behavioral attribute "speed" against driving direction for ' + str(number_found_speed_attributes_against_driving_direction)\
              + ' BSSD-lanes\n')
    
    #Convert values in columns "road_id", "lane_id_BSSD" to int 
    df_BSSD_speed_attribute['road_id']=df_BSSD_speed_attribute['road_id'].convert_dtypes()
    df_BSSD_speed_attribute['lane_id_BSSD']=df_BSSD_speed_attribute['lane_id_BSSD'].convert_dtypes()
    
    return df_BSSD_speed_attribute

    
def set_identical_speed_attribute(speed_behavior_along, speed_behavior_against, df_BSSD_speed_attribute, index_BSSD_lane):
    """
    This function sets for a defined BSSD-lane in df_BSSD_speed_attribute (index_BSSD_lane) the speed attribute for the direction against the
    driving direction to the same value as along the driving direction.
    
    This is necessary in two cases:
        - If a road has only drivable lanes in one direction (= One way road, dt.: "Einbahnstraße")
        - If the two sides of the road are separated
    """
    
    #Check for which side of the road the speed attribute was extracted (If it was extracted for one side)
    
    #Case 1: Speed attribute was extracted for behaviorAlong direction
    #-->speed attribute for behaviorAgainst has to be set to the same value
    if pd.isnull(speed_behavior_against)==True:
        df_BSSD_speed_attribute.loc[index_BSSD_lane, 'speed_behavior_against']=speed_behavior_along
        
    #Case 2: Speed attribute was extracted for behaviorAgainst direction
    #-->speed attribute for behaviorAlong has to be set to the same value
    else:
        df_BSSD_speed_attribute.loc[index_BSSD_lane, 'speed_behavior_along']=speed_behavior_against
        
    return df_BSSD_speed_attribute

def set_speed_attribute_based_on_other_side(road_id, segment_s, lane_id_BSSD, index_BSSD_lane, side_current_BSSD_lane, driving_direction,
                                            df_BSSD_speed_attribute):
    """
    This function sets for a defined BSSD-lane in df_BSSD_speed_attribute (road_id, segment_s, lane_id_BSSD, index_BSSD_lane) the speed attribute
    for the direction against the driving direction to the value of the speed attribute of the innermost BSSD-lane on the other side of the road,
    where a speed attribute along driving direction has been defined.
    """
    
    #Check for which side of the road the current BSSD-lane is defined
    #--> Access all BSSD-lanes on the other side of the road (depending on right/left) for which a speed attribute could be extracted
    
    #Case 1: Current BSSD-lane is defined on the right side of the road
    if side_current_BSSD_lane == 'right':
        
        #Case 1: Current BSSD-lane on the right side of the road and RHT
        if driving_direction=='RHT':
        
            #Get all BSSD-lanes of the other side of the road for which a speed attribute along driving direction could be extracted
            df_BSSD_speed_attribute_other_side = df_BSSD_speed_attribute[(df_BSSD_speed_attribute['road_id']==road_id) \
                                                & (round(df_BSSD_speed_attribute['segment_s'], 3) == round(segment_s, 3)) \
                                                & (df_BSSD_speed_attribute['lane_id_BSSD']>0)\
                                                & (pd.isnull(df_BSSD_speed_attribute['speed_behavior_against'])==False)]
            df_BSSD_speed_attribute_other_side = df_BSSD_speed_attribute_other_side.reset_index(drop=True)
            
            #Check if at least in one BSSD-lane on the other side of the road a speed attribute could be extracted
            #If yes, set the speed attribute of the current BSSD-lane against driving direction to the value of 
            #the innermost BSSD-lane of the other side of the road, where a speed attribute along driving direction has be defined
            #If for no BSSD-lane on the other side of the road a speed attribute could be extracted,
            #no speed attribute can be set for current BSSD-lane against driving direction
            if len(df_BSSD_speed_attribute_other_side)>0:
                
                #Get index of innermost BSSD-lane of other side of the road (Has the smallest index as only positive id's exist)
                index_innermost_BSSD_lane_other_side = df_BSSD_speed_attribute_other_side['lane_id_BSSD'].idxmin()
                
                #--> speed behaviorAgainst in current BSSD-lane = speed behaviorAgainst in innermost BSSD-lane from other side of the road
                df_BSSD_speed_attribute.loc[index_BSSD_lane, 'speed_behavior_against']=df_BSSD_speed_attribute_other_side\
                                                                    .loc[index_innermost_BSSD_lane_other_side, 'speed_behavior_against']
                                                                                                                
        #Case 2: Current BSSD-lane on the right side of the road and LHT
        else:
        
            #Get all BSSD-lanes of the other side of the road for which a speed attribute along driving direction could be extracted
            df_BSSD_speed_attribute_other_side = df_BSSD_speed_attribute[(df_BSSD_speed_attribute['road_id']==road_id) \
                                                & (round(df_BSSD_speed_attribute['segment_s'], 3) == round(segment_s, 3)) \
                                                & (df_BSSD_speed_attribute['lane_id_BSSD']>0)\
                                                & (pd.isnull(df_BSSD_speed_attribute['speed_behavior_along'])==False)]
            df_BSSD_speed_attribute_other_side = df_BSSD_speed_attribute_other_side.reset_index(drop=True)
            
            #Check if at least in one BSSD-lane on the other side of the road a speed attribute could be extracted
            #If yes, set the speed attribute of the current BSSD-lane against driving direction to the value of 
            #the innermost BSSD-lane of the other side of the road, where a speed attribute along driving direction has be defined
            #If for no BSSD-lane on the other side of the road a speed attribute could be extracted,
            #no speed attribute can be set for current BSSD-lane against driving direction
            if len(df_BSSD_speed_attribute_other_side)>0:
                
                #Get index of innermost BSSD-lane of other side of the road (Has the smallest index as only positive id's exist)
                index_innermost_BSSD_lane_other_side = df_BSSD_speed_attribute_other_side['lane_id_BSSD'].idxmin()
                                    
                #--> speed behaviorAlong in current BSSD-lane = speed behaviorAlong in innermost BSSD-lane from other side of the road
                df_BSSD_speed_attribute.loc[index_BSSD_lane, 'speed_behavior_along']=df_BSSD_speed_attribute_other_side\
                                                                    .loc[index_innermost_BSSD_lane_other_side, 'speed_behavior_along']
                                                                           
    #Case 2: Current BSSD-lane is defined on the left side of the road
    else:
        
        #Case 1: Current BSSD-lane on the left side of the road and RHT
        if driving_direction=='RHT':
        
            #Get all BSSD-lanes of the other side of the road for which a speed attribute along driving direction could be extracted
            df_BSSD_speed_attribute_other_side = df_BSSD_speed_attribute[(df_BSSD_speed_attribute['road_id']==road_id) \
                                                & (round(df_BSSD_speed_attribute['segment_s'], 3) == round(segment_s, 3)) \
                                                & (df_BSSD_speed_attribute['lane_id_BSSD']<0)\
                                                & (pd.isnull(df_BSSD_speed_attribute['speed_behavior_along'])==False)]
            df_BSSD_speed_attribute_other_side = df_BSSD_speed_attribute_other_side.reset_index(drop=True)
            
            #Check if at least in one BSSD-lane on the other side of the road a speed attribute could be extracted
            #If yes, set the speed attribute of the current BSSD-lane against driving direction to the value of 
            #the innermost BSSD-lane of the other side of the road, where a speed attribute along driving direction has be defined
            #If for no BSSD-lane on the other side of the road a speed attribute could be extracted,
            #no speed attribute can be set for current BSSD-lane against driving direction
            if len(df_BSSD_speed_attribute_other_side)>0:
                
                #Get index of innermost BSSD-lane of other side of the road (Has the highest index as only negative id's exist)
                index_innermost_BSSD_lane_other_side = df_BSSD_speed_attribute_other_side['lane_id_BSSD'].idxmax()
            
                #--> speed behaviorAlong in current BSSD-lane = speed behaviorAlong in innermost BSSD-lane from other side of the road
                df_BSSD_speed_attribute.loc[index_BSSD_lane, 'speed_behavior_along']=df_BSSD_speed_attribute_other_side\
                                                                    .loc[index_innermost_BSSD_lane_other_side, 'speed_behavior_along']
                                                                    
        #Case 2: Current BSSD-lane on the left side of the road and LHT
        else:
        
            #Get all BSSD-lanes of the other side of the road for which a speed attribute along driving direction could be extracted
            df_BSSD_speed_attribute_other_side = df_BSSD_speed_attribute[(df_BSSD_speed_attribute['road_id']==road_id) \
                                                & (round(df_BSSD_speed_attribute['segment_s'], 3) == round(segment_s, 3)) \
                                                & (df_BSSD_speed_attribute['lane_id_BSSD']<0)\
                                                & (pd.isnull(df_BSSD_speed_attribute['speed_behavior_against'])==False)]
            df_BSSD_speed_attribute_other_side = df_BSSD_speed_attribute_other_side.reset_index(drop=True)
            
            #Check if at least in one BSSD-lane on the other side of the road a speed attribute could be extracted
            #If yes, set the speed attribute of the current BSSD-lane against driving direction to the value of 
            #the innermost BSSD-lane of the other side of the road, where a speed attribute along driving direction has be defined
            #If for no BSSD-lane on the other side of the road a speed attribute could be extracted,
            #no speed attribute can be set for current BSSD-lane against driving direction
            if len(df_BSSD_speed_attribute_other_side)>0:
                
                #Get index of innermost BSSD-lane of other side of the road (Has the highest index as only negative id's exist)
                index_innermost_BSSD_lane_other_side = df_BSSD_speed_attribute_other_side['lane_id_BSSD'].idxmax()
                
                #--> speed behaviorAgainst in current BSSD-lane = speed behaviorAgainst in innermost BSSD-lane from other side of the road
                df_BSSD_speed_attribute.loc[index_BSSD_lane, 'speed_behavior_against']=df_BSSD_speed_attribute_other_side\
                                                                    .loc[index_innermost_BSSD_lane_other_side, 'speed_behavior_against']
                                                                    
    return df_BSSD_speed_attribute
    
    
    
    