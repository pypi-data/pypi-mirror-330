import pandas as pd
import numpy as np
import bisect
from tqdm import tqdm
from rich.console import Console

from integrate_BSSD_into_OpenDRIVE.utility.collect_object_data import collect_object_data
from integrate_BSSD_into_OpenDRIVE.utility.check_relation_OpenDRIVE_BSSD_lane import check_relation_OpenDRIVE_BSSD_lane

def classify_BSSD_lane_borders(df_lane_data, df_BSSD_lanes, df_segments, df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_object):
    """
    This function classifies the right and left border of all BSSD-lanes into crossable or not-crossable.
    This is done based on two criterions which are executed in two consecutive substeps:
        - Criterion 1: Classification based on neighbouring lanes 
            --> "Every border of a BSSD-lane is crossable if there is a neighbouring BSSD- or OpenDRIVE-lane existing, which is not of type
            "none" or "curb"".
        - Criterion 2: Classification based on objects in the imported OpenDRIVE-file
            --> "The border of a BSSD-lane is not crossable if there is an object/multiple objects in this BSSD-lane 
            defined throughout the whole s-range of this BSSD-lane"
            
     Parameters
     ----------
     df_lane_data : DataFrame
         DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file
     df_BSSD_lanes : DataFrame
         DataFrame containing all created BSSD-lanes. For every BSSD-lane the object for the first laneSection overlapping.
     df_segments : DataFrame
         DataFrame which contains all created BSSD-segments. 
         For every segment a start-s-coordinate is given. If the segments ends before the next segment in the road 
         or before the end of the road a end-s-coordinate is given.
     df_link_BSSD_lanes_with_OpenDRIVE_lanes : DataFrame
         DataFrame for storing information about link of BSSD-lanes to OpenDRIVE-lanes.
         For every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row is defined
     OpenDRIVE_object : elements.opendrive.OpenDRIVE
         Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map

     Returns
     -------
     df_BSSD_lanes_borders_crossable : DataFrame
         DataFrame to store for every BSSD-lane the information whether the right/left border is crossable or not-crossable.
         If the right/left border is crossable, the column "crossable_right"/"crossable_left" is set to "True".
         If the right/left border is not crossable, the column "crossable_right"/"crossable_left" is set to "False".
         --> Created based on criterion 1 and criterion 2       
    """
    
    console = Console(highlight=False)
    console.rule(style='None')
    print('Preprocessing: Classify borders of BSSD-lanes as crossable/not crossable: \n')
    
    #Execute function for criterion 1
    df_BSSD_lanes_borders_crossable = criterion_1_neighbour_lanes(df_BSSD_lanes)
    
    #Execute function for criterion 2
    df_BSSD_lanes_borders_crossable = criterion_2_objects(df_lane_data, df_BSSD_lanes, df_segments, df_link_BSSD_lanes_with_OpenDRIVE_lanes,
                                                          df_BSSD_lanes_borders_crossable, OpenDRIVE_object)
    
    console.rule(style='None')
    
    return df_BSSD_lanes_borders_crossable

def criterion_1_neighbour_lanes(df_BSSD_lanes):
    """
    This function classifies the right and left border of all BSSD-lanes into crossable or not-crossable based on criterion 1:
    "Every border of a BSSD-lane is crossable if there is a neighbouring BSSD- or OpenDRIVE-lane existing, which is not of type "none" or "curb"".

    Parameters
    ----------
    df_BSSD_lanes : DataFrame
        DataFrame containing all created BSSD-lanes. For every BSSD-lane the object for the first laneSection overlapping is stored

    Returns
    -------
    df_BSSD_lanes_borders_crossable : DataFrame
        DataFrame to store for every BSSD-lane the information whether the right/left border is crossable or not-crossable.
        If the right/left border is crossable, the column "crossable_right"/"crossable_left" is set to "True".
        If the right/left border is not crossable, the column "crossable_right"/"crossable_left" is set to "False".
        
    """
    
    print('1. Crossability based on neighbour lanes...\n')
    
    #Create DataFrame to store for every BSSD-lane the information whether the right/left border is crossable or not-crossable
    df_BSSD_lanes_borders_crossable = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'crossable_left', 'crossable_right'])
    
    #Defined types of OpenDRIVE-lanes which definitely lead to a not-crossable border
    lane_types_not_crossable=['none', 'curb']
    
    #Manually creating index for succeeding for-loop (Necessary to realize visualiziation with tqdm)
    index_BSSD_lane = 0
    
    #Iteration through all BSSD lanes (df_BSSD_lanes) to classify the right and left border of every BSSD-lane into crossable/not-crossable
    for lane_id_BSSD in tqdm(df_BSSD_lanes.loc[:, 'lane_id_BSSD']):
        
        #road_id of current BSSD-lane
        road_id = df_BSSD_lanes.loc[index_BSSD_lane, 'road_id']
        
        #s-coordinate of segment of current BSSD-lane
        segment_s = df_BSSD_lanes.loc[index_BSSD_lane, 'segment_s']
                
        #Get object of laneSection which is defined at the beginning of the current BSSD-segment
        laneSection_object_s_min = df_BSSD_lanes.loc[index_BSSD_lane, 'laneSection_object_s_min']
        
        ##1. Classify right border 
        
        #Get lane object of right neighbour OpenDRIVE-lane
        right_lane_neighbour_object = laneSection_object_s_min.getLane(lane_id_BSSD-1)
        
        #Check if there is a right neighbour lane existing
        if right_lane_neighbour_object != None:
            
            #Check if id of right neighbour lane is zero (center lane --> No "real" existing lane)
            #Case 1: Right neighbour lane has id 0
            if right_lane_neighbour_object.id == 0:
                
                #If neighbour lane is center lane go to next right lane 
                right_lane_neighbour_object = laneSection_object_s_min.getLane(lane_id_BSSD-2)
                    

        #Check again if right neighbour lane is None (if lane right of center lane is not existing)
        if right_lane_neighbour_object!=None:           
            
            #If right neighbour lane is existing, check type-attribute of this neighbour lane
            type_right_neighbour_lane = right_lane_neighbour_object.type
            
            #Classify right border as not crossable if neighbour lane is of type "none" or "curb"
            if type_right_neighbour_lane in lane_types_not_crossable:
                right_border_crossable = False
            #Classify right border as crossable if neighbour lane is not of type "none" or "curb"
            else:
                right_border_crossable = True
        
        #Classify right border as not crossable if there is no neighbour lane existing
        else:
            right_border_crossable = False
            
        ##2. Classify left border 
        
        #Get lane object of left neighbour lane
        left_lane_neighbour_object = laneSection_object_s_min.getLane(lane_id_BSSD+1)
        
        #Check if there is a left neighbour lane existing
        if left_lane_neighbour_object != None:
            
            #Check if id of left neighbour lane is zero (center lane --> No "real" existing lane)
            #Case 1: Left neighbour lane has id 0
            if left_lane_neighbour_object.id == 0:
                
                #Get lane objects of left neighbour lane
                left_lane_neighbour_object = laneSection_object_s_min.getLane(lane_id_BSSD+2)
                
        #Check again if left neighbour lane is None (if lane left of center lane is not existing)
        if left_lane_neighbour_object!=None:           
               
            #If left neighbour lane is existing, check type-attribute of this neighbour lane
            type_left_neighbour_lane = left_lane_neighbour_object.type
            
            #Classify left border as not crossable if neighbour lane is of type "none" or "curb"
            if type_left_neighbour_lane in lane_types_not_crossable:
                left_border_crossable = False
                
            #Classify left border as crossable if neighbour lane is not of type "none" or "curb"
            else:
                left_border_crossable = True
        
        #Classify left border as not crossable if there is no neighbour lane existing
        else:
            left_border_crossable = False
            
        #Append data of BSSD-lane to overall DataFrame
        df_BSSD_lanes_borders_crossable = df_BSSD_lanes_borders_crossable.append({'road_id': road_id, 'segment_s': segment_s,
                                                                                  'lane_id_BSSD': lane_id_BSSD,
                                                                                  'crossable_left': left_border_crossable,
                                                                                  'crossable_right': right_border_crossable}, ignore_index=True)
        index_BSSD_lane = index_BSSD_lane + 1
    
   
    #Total number of BSSD-lane borders (every BSSD-lane has a right and a left border)
    number_borders = len(df_BSSD_lanes_borders_crossable)*2
    
    #Number of borders which were classified as not crossable (For user output)
    number_not_crossable_left = len(df_BSSD_lanes_borders_crossable[df_BSSD_lanes_borders_crossable['crossable_left']==False])
    number_not_crossable_right = len(df_BSSD_lanes_borders_crossable[df_BSSD_lanes_borders_crossable['crossable_right']==False])
    
    number_not_crossable = number_not_crossable_left + number_not_crossable_right
    
    #User output: Number of borders which were classified as crossable
    number_crossable = number_borders - number_not_crossable
    
    print()
    #User output
    #Singular or Plural in console output
    if (number_crossable == 1) & (number_not_crossable == 1):
        print('Classified ' + str(number_crossable) + ' BSSD-lane border as crossable, ' + str(number_not_crossable) + ' BSSD-lane border as not crossable')
    elif (number_crossable > 1) & (number_not_crossable == 1):
        print('Classified ' + str(number_crossable) + ' BSSD-lane borders as crossable, ' + str(number_not_crossable) + ' BSSD-lane border as not crossable')
    elif (number_crossable == 1) & (number_not_crossable > 1):
        print('Classified ' + str(number_crossable) + ' BSSD-lane border as crossable, ' + str(number_not_crossable) + ' BSSD-lane borders as not crossable')
    else:
        print('Classified ' + str(number_crossable) + ' BSSD-lane borders as crossable, ' + str(number_not_crossable) + ' BSSD-lane borders as not crossable')
    
    return df_BSSD_lanes_borders_crossable

def criterion_2_objects(df_lane_data, df_BSSD_lanes, df_segments, df_link_BSSD_lanes_with_OpenDRIVE_lanes, df_BSSD_lanes_borders_crossable,
                        OpenDRIVE_object):
    """
    This function modifies the crossability of the right/left border of all BSSD-lanes based on criterion 2:
    "The border of a BSSD-lane is not crossable if there is an object/multiple objects in this BSSD-lane 
    defined throughout the whole s-range of this BSSD-lane"

    Parameters
    ----------
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file
    df_BSSD_lanes : DataFrame
        DataFrame containing all created BSSD-lanes. For every BSSD-lane the object for the first laneSection overlapping.
    df_segments : DataFrame
        DataFrame which contains all created BSSD-segments. 
        For every segment a start-s-coordinate is given. If the segments ends before the next segment in the road 
        or before the end of the road a end-s-coordinate is given.
    df_link_BSSD_lanes_with_OpenDRIVE_lanes : DataFrame
        DataFrame for storing information about link of BSSD-lanes to OpenDRIVE-lanes.
        For every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row is defined
     df_BSSD_lanes_borders_crossable : DataFrame
         DataFrame to store for every BSSD-lane the information whether the right/left border is crossable or not-crossable.
         If the right/left border is crossable, the column "crossable_right"/"crossable_left" is set to "True".
         If the right/left border is not crossable, the column "crossable_right"/"crossable_left" is set to "False".
         --> Created based on criterion 1
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map

    Returns
    -------
    df_BSSD_lanes_borders_crossable : DataFrame
        Modified version based on criterion 2

    """
    
    print()
    print('2. Crossability based on objects...\n')
        
    #Execute function to collect data about all objects in imported OpenDRIVE-file which are of interest for crossability of lane borders
    df_object_data = collect_object_data(OpenDRIVE_object)
    
    #Skip execution of function if there were no objects found in the OpenDRIVE-file which are located inside a OpenDRIVE-lane
    if len(df_object_data)==0:
        return df_BSSD_lanes_borders_crossable
    
    #Define maximum distance for which an object should be linked to a BSSD-lane border
    #--> e.g. 0.5 means that all objects, whose origin is < 0.5 m in t-direction away from the border of the corresponding BSSD-lane, are linked to
    #the border of this BSSD-lane
    maximum_distance_border = 0.5
    
    print('Check if found objects lead to not crossable BSSD-lane borders...\n')

    #Variable to count how many borders have been set to not crossable based on objects
    number_changed_border = 0

    #Manually creating index for succeeding for-loop (Necessary to realize visualiziation with tqdm)
    index_segment = 0

    #Iteration through all BSSD segments (df_BSSD_segments) to classify borders of BSSD-lanes based on objects as not-crossable
    #--> DataFrame df_BSSD_lanes_borders_crossable of criterion 1 is edited
    for segment_s_start in tqdm(df_segments.loc[:, 'segment_s_start']):
    
        #road_id of current BSSD-segment
        road_id = df_segments.loc[index_segment, 'road_id']
        
        ##Find s_end of current segment
        
        #Get subset of df_segments for current road to check the s-coordinate until which the segment is defined
        df_segments_current_road = df_segments[df_segments['road_id']==road_id]
        df_segments_current_road = df_segments_current_road.reset_index(drop=True)
        
        #Check if current segment has a succeeding BSSD definition gap (Column 'segment_s_end' is defined)
        #Case 1: Current segment has no suceeding BSSD definiton gap
        if pd.isnull(df_segments.loc[index_segment, 'segment_s_end']):
            
            #Find index of closest s_start which is higher than segment_s_start 
            index_succeeding_segment =  bisect.bisect_right(df_segments_current_road.loc[:, 'segment_s_start'], segment_s_start)
            
            #Check if current segment is the the last segment in the current road
            #Case 1: Current segment is last segment in current road
            if (len(df_segments_current_road)-1)<index_succeeding_segment:
                
                #s-end coordinate of current segment is equal to length of the road
                segment_s_end = round(OpenDRIVE_object.getRoad(road_id).length, 3)
                
            else:
                #s-end coordinate of current segment is equal s-start coordinate of succeeding segment in current road
                segment_s_end = df_segments.loc[index_segment+1, 'segment_s_start']
                                                 
            
        #Case 2: Current segment has a suceeding BSSD definiton gap   
        else:
            #s-end coordinate of current segment is s-coordinate of beginning of BSSD definiton gap
            segment_s_end = df_segments.loc[index_segment, 'segment_s_end']
            
        
        #Get all BSSD-lanes which are defined in the current BSSD-segment
        df_BSSD_lanes_current_segment = df_BSSD_lanes[(df_BSSD_lanes['road_id']==road_id) & \
                                                     (round(df_BSSD_lanes['segment_s'], 3)==round(segment_s_start, 3))]
        df_BSSD_lanes_current_segment = df_BSSD_lanes_current_segment.reset_index(drop=True)

        #Get subset of df_object_data for current road
        df_object_data_current_road = df_object_data[(df_object_data['road_id']==road_id)]                               
        df_object_data_current_road = df_object_data_current_road.reset_index(drop=True)
        
        #Create empty DataFrame which will be filled with data for all objects which are defined in the current BSSD-segment
        df_object_data_current_BSSD_segment = df_object_data[0:0]
        
        #Iterate through all objects in current road to filter all objects which are defined in the s-range of the current BSSD-segment
        for index_2, s_min in enumerate(df_object_data_current_road.loc[:, 's_min']):
            #Get s_max coordinate of current object
            s_max = df_object_data_current_road.loc[index_2, 's_max']
            
            #Check if current segment (segment_s_start, segment_s_end) and current object (s_min, s_max) overlap 
            #If yes append data of current object to DataFrame df_object_data_current_BSSD_segment
            if max(segment_s_start, s_min) <= min(segment_s_end, s_max):
                
                df_object_data_current_BSSD_segment =  pd.concat([df_object_data_current_BSSD_segment, df_object_data_current_road.loc[[index_2]]])
                
        df_object_data_current_BSSD_segment = df_object_data_current_BSSD_segment.reset_index(drop=True)
            
        
        #Iterate through all BSSD-lanes of current segment to check crossability of lane borders based on objects
        for lane_id_BSSD in df_BSSD_lanes_current_segment.loc[:, 'lane_id_BSSD']:
            
            #Create empty DataFrame which will be filled with data for all objects which are defined in the current BSSD-lane
            df_object_data_current_BSSD_lane = df_object_data[0:0]
            
            #Iterate through all objects defined in the current segment to filter all objects
            #which are defined in current BSSD-lane
            for index_2, laneSection_s_object in enumerate(df_object_data_current_BSSD_segment.loc[:, 'laneSection_s']):
                
                #Get id of OpenDRIVE-lane in which origin of object is located 
                OpenDRIVE_lane_id_object = df_object_data_current_BSSD_segment.loc[index_2, 'lane_id']
                
                #Check if current object has a origin in an OpenDRIVE-lane which is related to the current BSSD-lane
                #(function "check_relation_OpenDRIVE_BSSD_lane") --> In this context "related" means that the OpenDRIVE-lane:
                    #a. Directly overlaps to the BSSD-lane (see df_link_BSSD_lanes_with_OpenDRIVE_lanes)
                    #or
                    #b. Is connected via the elements <predecessor>/<successor> to an OpenDRIVE-lane which directly overlaps to the BSSD-lane
                #If current object is in an OpenDRIVE-lane which is related to current BSSD-lane, append data of current object to DataFrame for
                #all objects which are defined in the current BSSD-lane
                if check_relation_OpenDRIVE_BSSD_lane([road_id, laneSection_s_object, OpenDRIVE_lane_id_object], [road_id, segment_s_start, lane_id_BSSD],
                                                   df_lane_data, df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_object)==True:
                   df_object_data_current_BSSD_lane = pd.concat([df_object_data_current_BSSD_lane, df_object_data_current_BSSD_segment.loc[[index_2]]])
                                                                
            df_object_data_current_BSSD_lane = df_object_data_current_BSSD_lane.reset_index(drop=True)
            
            
            #Choose discretisation of s-coordinate (in m) for checking crossability of lane border
            #e.g. 0.2 means that every 20 cm it is checked whether an object is defined at the right/left border of the current BSSD-lane
            #If at every discretisation point an object is defined, the lane border is classified as not crossable
            discretisation_s = 0.2
            
            #Get all objects in the current BSSD-lane which are relevant for the crossability of the left lane border.
            #This includes all objects that have a distance to the left border < maximum_distance_border
            df_objects_left = df_object_data_current_BSSD_lane[df_object_data_current_BSSD_lane['delta_t_left']<maximum_distance_border]
            df_objects_left = df_objects_left.reset_index(drop=True)
            
            #Variable to set that left border is crossable (True)/not crossable (False)
            crossable_left = False
                        
            #Get all objects in the current BSSD-lane which are relevant for the crossability of the right lane border.
            #This includes all objects that have a distance to the right border < maximum_distance_border
            df_objects_right = df_object_data_current_BSSD_lane[df_object_data_current_BSSD_lane['delta_t_right']<maximum_distance_border]
            df_objects_right = df_objects_right.reset_index(drop=True)
            
            #Variable to set that right border is crossable (True)/not crossable (False)
            crossable_right = False
            
            #Continue with next object, if object is not linked to any border (right or left)
            if (len(df_objects_left)==0) and (len(df_objects_right)==0):
                continue
            
            #Iterate through s-range of segment with discretisation chosen in "discretisation_s" to check for every s-coordinate whether an
            #object is defined on the left/right side
            for s in np.arange(segment_s_start+discretisation_s, segment_s_end-discretisation_s, discretisation_s):
                
                #Check s-coordinate for left border only if there are any objects on the left side of the border and if the crossability is set to
                #not crossable by now
                if (len(df_objects_left)>0) and (crossable_left==False):
                
                    #Check for the current s-coordinate if there is an object which is defined at this s-coordinate on the left side
                    df_check_object_left = df_objects_left[(df_objects_left['s_min']<=s) & (df_objects_left['s_max']>=s)]
                    
                    #If there is no object defined at this s-coordinate on the left side, set left border to crossable
                    if len(df_check_object_left)==0:
                        crossable_left = True
                
                #Check s-coordinate for right border only if there are any objects on the right side of the border and if the crossability is set to
                #not crossable by now
                if (len(df_objects_right)>0) and (crossable_right==False):
                
                    #Check for the current s-coordinate if there is an object which is defined at this s-coordinate on the right side
                    df_check_object_right = df_objects_right[(df_objects_right['s_min']<=s) & (df_objects_right['s_max']>=s)]
                    
                    #If there is no object defined at this s-coordinate on the left side, set right border to crossable
                    if len(df_check_object_right)==0:
                        crossable_right = True
                        
            #Get index of entry for current BSSD-lane in df_BSSD_lanes_borders_crossable
            index_df_lanes_borders_crossable = df_BSSD_lanes_borders_crossable[(df_BSSD_lanes_borders_crossable['road_id']==road_id) & \
                                                (round(df_BSSD_lanes_borders_crossable['segment_s'], 3)==round(segment_s_start, 3)) & \
                                                (df_BSSD_lanes_borders_crossable['lane_id_BSSD']==lane_id_BSSD)].index.values.astype(int)[0]
                
            
            #Check if there are objects defined in the left/right side and if they lead to a not crossable left/right border (preceding for-loop)
            if (len(df_objects_left)>0) and (crossable_left==False):
                
                #Modify values for crossability of left/right border of current BSSD-lane in df_BSSD_lanes_borders_crossable
                df_BSSD_lanes_borders_crossable.loc[index_df_lanes_borders_crossable, 'crossable_left']=crossable_left
                number_changed_border = number_changed_border + 1 
                
            if (len(df_objects_right)>0) and (crossable_right==False):
                
                #Modify values for crossability of left/right border of current BSSD-lane in df_BSSD_lanes_borders_crossable
                df_BSSD_lanes_borders_crossable.loc[index_df_lanes_borders_crossable, 'crossable_right']=crossable_right
                number_changed_border = number_changed_border + 1
                
                
        index_segment = index_segment +1
    
    #Go through all BSSD-lanes where the right or left border was classified as not crossable. As this right/left border is the 
    #left/right border of the right/left neighbour lane, the attribute not crossable has also to be set in the neighbour lane (One border is always
    #shared by two lanes, except for outer lanes) --> function "set_shared_borders_not_crossable"                                       
    df_BSSD_lanes_borders_crossable, number_changed_border = set_shared_borders_not_crossable(df_BSSD_lanes_borders_crossable, number_changed_border)
    
    print()
    
    #User output
    if number_changed_border==1:
        print(str(number_changed_border) + ' BSSD-lane border was changed to not crossable\n')
    else:
        print(str(number_changed_border) + ' BSSD-lane borders were changed to not crossable\n')
    
    return df_BSSD_lanes_borders_crossable

def set_shared_borders_not_crossable(df_BSSD_lanes_borders_crossable, number_changed_border):
    """
    This function goes through all BSSD-lanes where the right or left border was classified as not crossable. As this right/left border is the 
    left/right border of the right/left neighbour lane, the attribute not crossable has also to be set in the neighbour lane (One border is always
    shared by two lanes, except for outer lanes)                                                                                                                              
    """
    
    #Sort BSSD-lanes ascending --> From outermost right lane (lowest id) to outermost left lane (highest id)
    df_BSSD_lanes_borders_crossable = df_BSSD_lanes_borders_crossable.sort_values(['road_id', 'segment_s', 'lane_id_BSSD'])
    df_BSSD_lanes_borders_crossable = df_BSSD_lanes_borders_crossable.reset_index(drop=True)
    
    #Get all BSSD-lanes which have at least one border which was classified as not crossable
    df_borders_not_crossable = df_BSSD_lanes_borders_crossable[(df_BSSD_lanes_borders_crossable['crossable_left']==False) \
                                                               | (df_BSSD_lanes_borders_crossable['crossable_right']==False)]
        
    #Iterate through all BSSD-lanes where at least one border is not crossable
    #--> Set for every border that is not crossable the same border in the neighbour lane as not crossable
    for index, lane_id_BSSD in enumerate(df_borders_not_crossable.loc[:, 'lane_id_BSSD']):
        
        #Get index of current entry in df_borders_not_crossable as the index in this df is not sorted
        #(--> to keep linkage with df_BSSD_lanes_borders_crossable)
        index_original_df = df_borders_not_crossable.index.values.astype(int)[index]
        
        #Get road and segment of current BSSD-lane
        road_id = df_borders_not_crossable.loc[index_original_df, 'road_id']
        segment_s = df_borders_not_crossable.loc[index_original_df, 'segment_s']
        
        #Get crossability of left and right border
        crossable_left =  df_borders_not_crossable.loc[index_original_df, 'crossable_left']
        crossable_right =  df_borders_not_crossable.loc[index_original_df, 'crossable_right']
        
        ##1.LEFT BORDER
        
        #Check if left border is not crossable and current BSSD-lane is not the last BSSD-lane in df_BSSD_lanes_borders_crossable
        #If yes, right border of left neighbour lane has also to be set to not-crossable
        if (crossable_left==False) and (index_original_df<(len(df_BSSD_lanes_borders_crossable)-1)):
            
            #Get data of succeeding lane in df_BSSD_lanes_borders_crossable (road_id, segment_s, lane_id_BSSD) to check whether this lane is the 
            #direct left neighbour of the current BSSD-lane (Higher index in df = direction left)
            road_id_left_neighbour = df_BSSD_lanes_borders_crossable.loc[index_original_df+1, 'road_id']
            segment_s_left_neighbour = df_BSSD_lanes_borders_crossable.loc[index_original_df+1, 'segment_s']
            lane_id_BSSD_left_neighbour = df_BSSD_lanes_borders_crossable.loc[index_original_df+1, 'lane_id_BSSD']
            
            #Check if succeeding BSSD-lane is in the same segment as the current BSSD-lane
            #If yes, check if this BSSD-lane is the direct left neighbour of current BSSD-lane
            if (road_id_left_neighbour==road_id) and (round(segment_s_left_neighbour, 3)==round(segment_s, 3)):
                
                #Special case: lane with id -1 --> Left neighbour lane has id which is +2 higher
                #If neighbour lane has id +1 set right border of this lane to not crossable
                if (lane_id_BSSD==-1) and (lane_id_BSSD_left_neighbour==1):
                    
                    df_BSSD_lanes_borders_crossable.loc[index_original_df+1, 'crossable_right']=False
                    number_changed_border = number_changed_border + 1
                    
                #Check if succeeding lane is direct left neighboour of current BSSD-lane --> Is the case if id is only +1 higher
                #If yes, set right border of this lane to not crossable
                if (lane_id_BSSD_left_neighbour == lane_id_BSSD+1):
                    
                    df_BSSD_lanes_borders_crossable.loc[index_original_df+1, 'crossable_right']=False
                    number_changed_border = number_changed_border + 1
                    
        ##2.RIGHT BORDER
        #Check if right border is not crossable and current BSSD-lane is not the first BSSD-lane in df_BSSD_lanes_borders_crossable
        #If yes, left border of right neighbour lane has also to be set to not-crossable
        if (crossable_right==False) and (index_original_df>0):
                    
            #Get data of preceding lane in df_BSSD_lanes_borders_crossable (road_id, segment_s, lane_id_BSSD) to check whether this lane is the 
            #direct right neighbour of the current BSSD-lane (Lower index in df = direction right)
            road_id_right_neighbour = df_BSSD_lanes_borders_crossable.loc[index_original_df-1, 'road_id']
            segment_s_right_neighbour = df_BSSD_lanes_borders_crossable.loc[index_original_df-1, 'segment_s']
            lane_id_BSSD_right_neighbour = df_BSSD_lanes_borders_crossable.loc[index_original_df-1, 'lane_id_BSSD']
            
            #Check if preceding BSSD-lane is in the same segment as the current BSSD-lane
            #If yes, check if this BSSD-lane is the direct right neighbour of current BSSD-lane
            if (road_id_right_neighbour==road_id) and (round(segment_s_right_neighbour, 3)==round(segment_s, 3)):
            
                #Special case: lane with id 1 --> Right neighbour lane has id which is -2 lower
                #If neighbour lane has id -1 set left border of this lane to not crossable
                if (lane_id_BSSD==1) and (lane_id_BSSD_right_neighbour==-1):
                    
                    df_BSSD_lanes_borders_crossable.loc[index_original_df-1, 'crossable_left']=False
                    number_changed_border = number_changed_border + 1
                    
                #Check if preceding lane is direct right neighboour of current BSSD-lane --> Is the case if id is only -1 lower
                #If yes, set left border of this lane to not crossable
                if (lane_id_BSSD_right_neighbour == lane_id_BSSD-1):
                    
                    df_BSSD_lanes_borders_crossable.loc[index_original_df-1, 'crossable_left']=False
                    number_changed_border = number_changed_border + 1
                    
    return df_BSSD_lanes_borders_crossable, number_changed_border