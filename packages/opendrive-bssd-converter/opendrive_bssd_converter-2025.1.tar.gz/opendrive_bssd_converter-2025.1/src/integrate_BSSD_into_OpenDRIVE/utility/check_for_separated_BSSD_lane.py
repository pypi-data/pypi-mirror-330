def check_for_separated_BSSD_lane(road_id, segment_s, lane_id_BSSD, df_BSSD_lanes, df_BSSD_lanes_borders_crossable):
    """
    This function checks for a BSSD-lane if it is separated from the BSSD-lanes on the other side of the road (opposite driving direction).
    Depending on whether the BSSD-lane is separated from the other side, the the speed limit against the driving direction
    is equal to the speed limit along the driving direction or it is equal to a speed limit from a BSSD-lane from the other side of the road.
    
    There are two criterions for checking the separation:
        1. Check innermost BSSD-lanes: If there is a not-drivable lane between the innermost BSSD-lanes in the segment of the BSSD-lane,
            the BSSD-lane is separated from the BSSD-lanes on the other side of the road.
        2. Check the crossability of the borders of the BSSD-lane: If there is a not crossable border of a BSSD-lane, which is located inwards to
            the BSSD-lane and on the same side of the road, the BSSD-lane is separated from the BSSD-lanes on the other side of the road.

        --> Each criterion is executed in a separate function: 
            1. "criterion_1_check_innermost_BSSD_lanes"
            2. "criterion_2_check_crossability_of_lane_borders"
            
    Each function returns True if the criterion is fulfilled (= BSSD-lane is separated from other side of the road) or False
    if the criterion is not fulfilled (= BSSD-lane is not separated from other side of the road)
    --> If at least one of the two criterions returns True, the BSSD-lane is considered as separated from the other side of the road

    Parameters
    ----------
    road_id : int
        id of the road which contains the BSSD-lane
    segment_s : float
        s-coordinate of the segment which contains the BSSD-lane
    lane_id_BSSD : int
        id of the BSSD-lane for which the separation from the other side of the road should be checked
    df_BSSD_lanes : DataFrame
        DataFrame containing all created BSSD-lanes. For every BSSD-lane the object for the first laneSection overlapping is stored
    df_BSSD_lanes_borders_crossable : DataFrame
        DataFrame to store for every BSSD-lane the information whether the right/left border is crossable or not-crossable.
        If the right/left border is crossable, the column "crossable_right"/"crossable_left" is set to "True".
        If the right/left border is not crossable, the column "crossable_right"/"crossable_left" is set to "False".

    Returns
    -------
    bool
        True/False: True if the BSSD-lane is separated from other side of the road, False if not

    """
    
    #Check for criterion 1 --> If this criterion is fulfilled, return True --> BSSD-lane is considered as separated from the other side of the road
    if criterion_1_check_innermost_BSSD_lanes(road_id, segment_s, df_BSSD_lanes)==True:
        return True
    #If criterion 1 is not fulfilled, check for criterion 2 --> If this criterion is fulfilled, return True
    #--> BSSD-lane is considered as separated from the other side of the road
    elif criterion_2_check_crossability_of_lane_borders(road_id, segment_s, lane_id_BSSD, df_BSSD_lanes_borders_crossable)==True:
        return True
    #If both criterions are not fulfilled, return False --> BSSD-lane is not considered as separated from the other side of the road
    else:
        return False

def criterion_1_check_innermost_BSSD_lanes(road_id, segment_s, df_BSSD_lanes):
    """
    This function executes criterion 1 for checking whether a BSSD-lane separated from the BSSD-lanes on the other side of the road.
    
    Criterion 1 is defined as: If there is a not-drivable lane between the innermost BSSD-lanes in the segment of the BSSD-lane, the BSSD-lane is
        separated from the BSSD-lanes on the other side of the road.
    
    --> This can be checked by looking at the id-values of the BSSD-lanes in the passed BSSD-segment --> If there exist no BSSD-lanes
    with id 1 or -1 it is sure that a not-drivable lane exists between the innermost BSSD-lanes

    Parameters
    ----------
    road_id : int
        id of road that contains the BSSD-segment
    segment_s : float
        s-coordinate of start of BSSD-segment which should be checked
    df_BSSD_lanes : DataFrame
        DataFrame containing all created BSSD-lanes.

    Returns
    -------
    bool
        True if criterion is fulfilled --> BSSD-lane is considered as separated from the other side of the road
        False if criterion is not fulfilled --> BSSD-lane is not considered as separated from the other side of the road

    """
    
    #Get all BSSD-lanes in the current BSSD-Segment
    df_BSSD_lanes_current_segment = df_BSSD_lanes[(df_BSSD_lanes['road_id']==road_id) & (round(df_BSSD_lanes['segment_s'], 3) == round(segment_s, 3))]
    df_BSSD_lanes_current_segment = df_BSSD_lanes_current_segment.reset_index(drop=True)
    list_BSSD_lanes_current_segment = df_BSSD_lanes_current_segment.loc[:,'lane_id_BSSD'].tolist()
    
    #Check if there is no BSSD-lane with id 1 or no BSSD-lane with id -1
    #If yes, it is sure that there is a not drivable lane between the innermost BSSD-lanes --> BSSD-lane is separated from the other side of the
    #road (This function will only be executed for roads which have both driving directions --> Special case one way road is already considered)
    if ((-1 in list_BSSD_lanes_current_segment) == False) or ((1 in list_BSSD_lanes_current_segment) == False):
        return True
    #If no, the BSSD-lane is not separated from the other side of the road
    else:
        return False
    
def criterion_2_check_crossability_of_lane_borders(road_id, segment_s, lane_id_BSSD, df_BSSD_lanes_borders_crossable):
    """
    This function executes criterion 2 for checking whether a BSSD-lane separated from the BSSD-lanes on the other side of the road.
    
    Criterion 2 is defined as: If there is a not crossable border of a BSSD-lane, which is located inwards to the
        BSSD-lane and on the same side of the road, the BSSD-lane is separated from the BSSD-lanes on the other side of the road.

    Parameters
    ----------
    road_id : int
        id of the road which contains the BSSD-lane
    segment_s : float
        s-coordinate of the segment which contains the BSSD-lane
    lane_id_BSSD : int
        id of the BSSD-lane for which the separation from the other side of the road should be checked
    df_BSSD_lanes_borders_crossable : DataFrame
        DataFrame to store for every BSSD-lane the information whether the right/left border is crossable or not-crossable.
        If the right/left border is crossable, the column "crossable_right"/"crossable_left" is set to "True".
        If the right/left border is not crossable, the column "crossable_right"/"crossable_left" is set to "False".

    Returns
    -------
    bool
        True if criterion is fulfilled --> BSSD-lane is considered as separated from the other side of the road
        False if criterion is not fulfilled --> BSSD-lane is not considered as separated from the other side of the road

    """
    
    #Check in which side of the road the BSSD-lane is defined to get the BSSD-lanes located inwards to the BSSD-lane on the same side of the road
    #Case 1: BSSD-lane is located on the right side of the road (id < 0)
    if lane_id_BSSD <0:
        
        #Get crossability of current BSSD-lane and all BSSD-lanes which are located inwards to the BSSD-lane but on the same side of the road
        df_BSSD_lanes_borders_crossable_inwards = df_BSSD_lanes_borders_crossable[(df_BSSD_lanes_borders_crossable['road_id']==road_id) &\
                                                              (round(df_BSSD_lanes_borders_crossable['segment_s'], 3) == round(segment_s, 3)) & \
                                                              (df_BSSD_lanes_borders_crossable['lane_id_BSSD']<0) & \
                                                              (df_BSSD_lanes_borders_crossable['lane_id_BSSD']>=lane_id_BSSD)] 
        df_BSSD_lanes_borders_crossable_inwards = df_BSSD_lanes_borders_crossable_inwards.reset_index(drop=True)
        
        #Check if there is a border which is located inwards to the current BSSD-lane and is not crossable
        #Check only left borders as they are always inward to current BSSD-lanes
        #Case 1: If yes, then criterion 2 is fulfilled. Thus, the BSSD-lane is separated from the BSSD-lanes on the other side of the road
        if any(df_BSSD_lanes_borders_crossable_inwards.crossable_left == False):
            return True
        #Case 2: If no, then criterion 2 is not fulfilled. Thus, the BSSD-lane is not separated from the BSSD-lanes on the other side of the road
        else:
            return False
        
    
    #Case 2: BSSD-lane is located on the left side of the road (id > 0)
    else:
        #Get crossability of of current BSSD-lane and all BSSD-lanes which are located inwards to the BSSD-lane but on the same side of the road
        df_BSSD_lanes_borders_crossable_inwards = df_BSSD_lanes_borders_crossable[(df_BSSD_lanes_borders_crossable['road_id']==road_id) &\
                                                              (round(df_BSSD_lanes_borders_crossable['segment_s'], 3) == round(segment_s, 3)) & \
                                                              (df_BSSD_lanes_borders_crossable['lane_id_BSSD']>0) & \
                                                              (df_BSSD_lanes_borders_crossable['lane_id_BSSD']<=lane_id_BSSD)] 
        df_BSSD_lanes_borders_crossable_inwards = df_BSSD_lanes_borders_crossable_inwards.reset_index(drop=True)
        
        #Check if there is a border which is located inwards to the current BSSD-lane and is not crossable
        #Check only right borders as they are always inward to current BSSD-lanes
        #Case 1: If yes, then criterion 2 is fulfilled. Thus, the BSSD-lane is separated from the BSSD-lanes on the other side of the road
        if any(df_BSSD_lanes_borders_crossable_inwards.crossable_right == False):
            return True
        #Case 2: If no, then criterion 2 is not fulfilled. Thus, the BSSD-lane is not separated from the BSSD-lanes on the other side of the road
        else:
            return False
