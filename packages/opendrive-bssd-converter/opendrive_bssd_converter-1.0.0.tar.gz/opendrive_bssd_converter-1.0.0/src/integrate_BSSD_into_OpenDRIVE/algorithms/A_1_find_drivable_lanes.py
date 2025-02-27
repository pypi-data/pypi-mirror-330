import pandas as pd
from tqdm import tqdm

def A_1_find_drivable_lanes(OpenDRIVE_object):
    """
    The main purpose of this function is to find all lanes in an existing OpenDRIVE-file that represent a lane that is modelled in BSSD. 
    All lanes that are part of roadway (German: 'Fahrbahn') are modelled in BSSD. These lanes will be called "drivable lanes" in the following.
    For automatic extraction whether a lane is drivable  or not, the attribute 'type' of the OpenDRIVE-<lane>-element is used.
    The 'type'-attribute describes the main purpose of a lane.
    
    This function divides all lanes included in an OpenDRIVE-file into two groups: 
        - One group includes all lanes that are drivable
        - The other group includes all lanes that are not drivable

    

    Parameters
    ----------
    OpenDRIVE_object : elements.opendrive.OpenDRIVE 
    (opendriveparser from TUM https://gitlab.lrz.de/tum-cps/commonroad-scenario-designer/-/tree/main/crdesigner/map_conversion/opendrive/opendrive_parser)
        Object representing the root-<OpenDRIVE>-element of xodr-file.

    Returns
    -------
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file.
    df_lane_data_drivable_lanes : DataFrame
        Subset of df_lane_data, which only contains lanes that represent a drivable OpenDRIVE-lane
    df_lane_data_not_drivable_lanes : DataFrame
        Subset of df_lane_data, which only contains lanes that don't represent a drivable OpenDRIVE-lane.

    """
    
    #Dictionary that contains all possible values of attribute 'type' of OpenDRIVE-<lane>-element 
    #Dictionary defines whether an OpenDRIVE-lane of a certain type represents a drivable lane (Value 'yes' --> modelled in BSSD) 
    #or not a drivable lane (Value 'no' --> not modelled in BSSD)
    dict_lane_types = {'shoulder':      'no',
                       'border':        'yes',
                       'driving':       'yes',
                       'stop':          'yes',
                       'none':          'no',
                       'restricted':    'yes',
                       'parking':       'yes',
                       'median':        'no',
                       'biking':        'no',
                       'sidewalk':      'no',
                       'curb':          'no',
                       'exit':          'yes',
                       'entry':         'yes',
                       'onRamp':        'yes',
                       'offRamp':       'yes',
                       'connectingRamp':'yes',
                       'bidirectional': 'yes',
                       'roadWorks':     'yes',
                       'tram':          'yes',
                       'rail':          'yes',
                       'bus':           'yes',
                       'taxi':          'yes',
                       'HOV':           'yes',
                       'mwyEntry':      'yes',
                       'mwyExit':       'yes',
                       'special1':      'yes',
                       'special2':      'yes',
                       'special3':      'yes'}

    #Create DataFrame to store information for all OpenDRIVE-<lane>-elements
    df_lane_data = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
    
    # Create DataFrame which contains only data for drivable OpenDRIVE-<lane>-elements (Subset of df_lane_data)
    df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
    
    # Create DataFrame which contains only data for not drivable OpenDRIVE-<lane>-elements (Subset of df_lane_data)
    df_lane_data_not_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])


    #Iteration through all road-objects of imported OpenDRIVE-object to extract drivable lanes of this road
    for road_object in tqdm(OpenDRIVE_object.roads):
        
        #id of current road-object
        road_id = road_object.id

        #lanes-object of current road-object --> To access laneSection-objects of current road
        lanes_object = road_object.lanes
        
        #Iteration through all laneSection-objects 
        for laneSection_object in lanes_object.lane_sections:
            
            #s-coordinate of current laneSection-object
            laneSection_s = laneSection_object.sPos
            
            #Iteration through all lane-objects of current laneSection-object to extract data of lanes in current laneSection
            for lane_object in laneSection_object.allLanes:
                
                #id of current lane-object
                lane_id = lane_object.id
               
                #Skip center lane of OpenDRIVE (has always id = 0) as center lane has infinitesimal physical dimensions --> No "real" lane
                if lane_id == 0:
                    continue
                
                #type-attribute of current lane-object
                lane_type = lane_object.type
                
                #junction-object of current road-object (Is None if lane is not inside a junction)
                junction_object = road_object.junction
                
                #Get id of junction (id is set to -1 if road is not inside a junction)
                if junction_object == None:
                    junction_id = -1
                else:
                    junction_id = junction_object.id
                
                #Data of current lane-object to append to overall DataFrame
                data_current_lane = {'road_id': road_id, 'laneSection_s': laneSection_s, 'lane_id': lane_id, 'lane_type': lane_type,
                                     'junction_id': junction_id}
                
                #Append data to overall DataFrame
                df_lane_data = df_lane_data.append(data_current_lane, ignore_index=True)
                
                
                #Special case: Biking lanes
                #Drivable/not-drivable depending on neighbour-lanes
                if lane_type == 'biking':
                    
                    #Check for drivable/not-drivable with function "check_if_biking_is_drivable"
                    # --> If one of the neighbour-lanes of the biking-lane is drivable, the biking lane is also considered as drivable 
                    #Case 1: biking lane is drivable
                    if check_if_biking_is_drivable(lane_id, laneSection_object, dict_lane_types)==True:

                        df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append(data_current_lane, ignore_index=True)
                    #Case 2: biking lane is not drivable
                    else:

                        df_lane_data_not_drivable_lanes = df_lane_data_not_drivable_lanes.append(data_current_lane, ignore_index=True)
                    
                #No biking lane --> drivable/not-drivable only depending on "type"-attribute
                else:
                    
                    #Check whether current lane represents a drivable lane to append it to the right DataFrame
                    #Case: Current lane represents a drivable lane
                    if dict_lane_types[lane_type] == 'yes':

                        df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append(data_current_lane, ignore_index=True)
                    #Case: Current lane doesn't represent a drivable lane
                    else:

                        df_lane_data_not_drivable_lanes = df_lane_data_not_drivable_lanes.append(data_current_lane, ignore_index=True)

            
    return df_lane_data, df_lane_data_drivable_lanes, df_lane_data_not_drivable_lanes


def check_if_biking_is_drivable(lane_id, laneSection_object, dict_lane_types):
    """
    This function checks for a certain lane (lane_id, laneSection_object) with attribute type="biking", if this lane is a drivable or a not drivable
    lane. A biking lane is considered as drivable if at least one of the neighbour lanes (if existing) is drivable.
    
    If the biking lane is drivable, the function returns True. If the biking lane is not drivable, the function returns False
    """
    
    #Get lane object of left neighbour lane
    left_lane_neighbour_object = laneSection_object.getLane(lane_id+1)
    
    #Check if there is a left neighbour lane existing
    if left_lane_neighbour_object != None:
        
        #Check if id of left neighbour lane is zero (center lane --> No "real" existing lane)
        #Case 1: Left neighbour lane has id 0
        if left_lane_neighbour_object.id == 0:
            
            #If neighbour lane is center lane go to next left lane (if existing)
            if laneSection_object.getLane(lane_id+2) != None:
                
                #Get lane objects of left neighbour lane
                left_lane_neighbour_object = laneSection_object.getLane(lane_id+2)
                
                type_left_neighbour_lane = left_lane_neighbour_object.type
                
                #Check if left neighbour lane is a drivable lane
                #If yes, mark current biking lane as drivable lane
                if dict_lane_types[type_left_neighbour_lane] == 'yes':
                    return True
        
        #Case 2: Left neighbour lane has not id 0        
        else:
            
            type_left_neighbour_lane = left_lane_neighbour_object.type

            #Check if left neighbour lane is a drivable lane
            #If yes, mark current biking lane as drivable lane
            if dict_lane_types[type_left_neighbour_lane] == 'yes':
                return True
        
        
    #Get lane object of right neighbour lane
    right_lane_neighbour_object = laneSection_object.getLane(lane_id-1)
    
    #Check if there is a right neighbour lane existing
    if right_lane_neighbour_object != None:
        
        #Check if id of right neighbour lane is zero (center lane --> No "real" existing lane)
        #Case 1: Right neighbour lane has id 0
        if right_lane_neighbour_object.id == 0:
            
            #If neighbour lane is center lane go to next right lane (if existing)
            if laneSection_object.getLane(lane_id-2) != None:
                
                #Get lane objects of right neighbour lane
                right_lane_neighbour_object = laneSection_object.getLane(lane_id-2)
                
                type_right_neighbour_lane = right_lane_neighbour_object.type
                
                #Check if right neighbour lane is a drivable lane
                #If yes, mark current biking lane as drivable lane
                if dict_lane_types[type_right_neighbour_lane] == 'yes':
                    return True
        
        #Case 2: Right neighbour lane has not id 0 
        else:
            
            type_right_neighbour_lane = right_lane_neighbour_object.type
            
            #Check if right neighbour lane is a drivable lane
            #If yes, mark current biking lane as drivable lane
            if dict_lane_types[type_right_neighbour_lane] == 'yes':
                return True
    
    #Return False if neighbouring lanes are not existing or not drivable
    return False
            
    
