def check_relation_OpenDRIVE_BSSD_lane(data_OpenDRIVE_lane, data_BSSD_lane, df_lane_data,
                                       df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_object):
    """
    This function checks if an OpenDRIVE-lane is related to a BSSD-lane. In this context "related" means that the OpenDRIVE-lane
        a. directly overlaps to the BSSD-lane (see df_link_BSSD_lanes_with_OpenDRIVE_lanes)
        
        or
        
        b. is connected via the elements <predecessor>/<successor> to an OpenDRIVE-lane which directly overlaps to the BSSD-lane
        
    This function is used to check whether an object is relevant for the crossability of a certain BSSD-lane border.
    The function returns True if the OpenDRIVE-lane is related to the BSSD-lane. Otherwise the function returns False

    Parameters
    ----------
    data_OpenDRIVE_lane : list
        Contains the data to identify the OpenDRIVE-lane: [road_id_OpenDRIVE, laneSection_s, lane_id_OpenDRIVE]
    data_BSSD_lane : list
        Contains the data to identify the BSSD--lane: [road_id_BSSD, segment_s, lane_id_BSSD]
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file.
    df_link_BSSD_lanes_with_OpenDRIVE_lanes : DataFrame
        DataFrame for storing information about link of BSSD-lanes to OpenDRIVE-lanes.
        For every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row is defined
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map

    Returns
    -------
    True/False: True if the OpenDRIVE-lane is related to the BSSD-lane. Otherwise False

    """
    
    #Get data of OpenDRIVE-lane: road_id, laneSection, OpenDRIVE_lane_id    
    road_id_OpenDRIVE = data_OpenDRIVE_lane[0]
    laneSection_s = data_OpenDRIVE_lane[1]
    lane_id_OpenDRIVE = data_OpenDRIVE_lane[2]
    
    #Get data of BSSD-lane: road_id, segment, BSSD_lane_id    
    road_id_BSSD = data_BSSD_lane[0]
    segment_s = data_BSSD_lane[1]
    lane_id_BSSD = data_BSSD_lane[2]
    
    #Check if the OpenDRIVE-lane is located in the same road like the BSSD-lane --> If not, the two lanes are not related
    if road_id_OpenDRIVE!=road_id_BSSD:
        return False
    
    #Get all OpenDRIVE-lanes which overlap to the BSSD-lane
    df_linked_OpenDRIVE_lanes_BSSD_lane = df_link_BSSD_lanes_with_OpenDRIVE_lanes[\
                                                      (df_link_BSSD_lanes_with_OpenDRIVE_lanes['road_id']==road_id_BSSD)&\
                                                      (round(df_link_BSSD_lanes_with_OpenDRIVE_lanes['segment_s'], 3)==round(segment_s, 3))&\
                                                      (df_link_BSSD_lanes_with_OpenDRIVE_lanes['lane_id_BSSD']==lane_id_BSSD)]
    df_linked_OpenDRIVE_lanes_BSSD_lane = df_linked_OpenDRIVE_lanes_BSSD_lane.reset_index(drop=True)
    
    
    ##1. CHECK CONDITION A: OpenDRIVE-lane directly overlaps to BSSD-lane
    
    #Check if OpenDRIVE-lane directly overlaps to the BSSD-lane --> Therefore get subset of df_linked_OpenDRIVE_lanes_BSSD_lane which contains only
    #the BSSD and the OpenDRIVE-lane --> This df has either one entry if the OpenDRIVE- and the BSSD-lane are directly overlapping or no entry
    #if they do not overlap directly
    df_check_direct_linkage = df_linked_OpenDRIVE_lanes_BSSD_lane[\
                                                    (round(df_linked_OpenDRIVE_lanes_BSSD_lane['laneSection_s'], 3)==round(laneSection_s, 3))&\
                                                    (df_linked_OpenDRIVE_lanes_BSSD_lane['lane_id_OpenDRIVE']==lane_id_OpenDRIVE)]
   
    #If length of DataFrame is > 0, the OpenDRIVE-lane overlaps to the BSSD-lane --> They are related to each other
    if len(df_check_direct_linkage)>0:
        return True
    
    ##2. CHECK CONDTION B: OpenDRIVE-lane is connected via the elements <predecessor>/<successor> to an OpenDRIVE-lane which directly overlaps
    #to the BSSD-lane
    
    #Get subset of df_lane_data which only contains the road of interest
    df_lane_data_road = df_lane_data[df_lane_data['road_id']==road_id_OpenDRIVE]
    df_lane_data_road = df_lane_data_road.reset_index(drop=True)
    
    #Check if OpenDRIVE-lane is defined before or after BSSD-lane
    #Case 1: OpenDRIVE-lane is defined before BSSD-lane
    if laneSection_s < segment_s:
        
        #Get first laneSection overlapping to BSSD-lane
        first_overlapping_laneSection = df_linked_OpenDRIVE_lanes_BSSD_lane.loc[0, 'laneSection_s']
        
        #Get list of all laneSections in the road of interest which have an s-coordinate equal/below to s-coordinate of 
        #first laneSection overlapping to BSSD-lane
        list_laneSections_below = df_lane_data_road[round(df_lane_data_road['laneSection_s'], 3)<=round(first_overlapping_laneSection, 3)]\
                                    ['laneSection_s'].unique().tolist()
        #Sort laneSections descending
        list_laneSections_below.sort(reverse=True)
              
        #Iterate through the OpenDRIVE-lanes linked in the <predecessor>-element of the preceding OpenDRIVE-lane --> For every OpenDRIVE-lane it is 
        #checked whether it is equal to the OpenDRIVE-lane of interest
                                      
        #Get lane_id of first OpenDRIVE-lane overlapping with the BSSD-lane --> Is the starting OpenDRIVE-lane 
        curr_OpenDRIVE_lane_id = df_linked_OpenDRIVE_lanes_BSSD_lane.loc[0, 'lane_id_OpenDRIVE']
        
        #Start iteration
        for s_curr_laneSection in list_laneSections_below:
            
            #Check if current OpenDRIVE-lane is the OpenDRIVE-lane of interest
            #If yes, return True --> OpenDRIVE-lane and BSSD-lane are related to each other
            if (round(s_curr_laneSection, 3)==round(laneSection_s, 3)) and (curr_OpenDRIVE_lane_id==lane_id_OpenDRIVE):
                return True
            
            #Get object for current OpenDRIVE-lane
            lane_object_current_OpenDRIVE_lane = OpenDRIVE_object.getRoad(road_id_OpenDRIVE).lanes.getLaneSection(s_curr_laneSection).\
                                                        getLane(curr_OpenDRIVE_lane_id)
                                                        
            #If current OpenDRIVE-lane has no predecessor, the OpenDRIVE-lane of interest is not related to the BSSD-lane
            if lane_object_current_OpenDRIVE_lane.link.predecessorId==None:
                return False        
            
            #Set for next iteration the id linked in predecessor to id of current OpenDRIVE-lane
            curr_OpenDRIVE_lane_id = lane_object_current_OpenDRIVE_lane.link.predecessorId
            
        #If OpenDRIVE-lane of interest was not found, return False
        return False
    
    #Case 2: OpenDRIVE-lane is defined after BSSD-lane
    else:
        
        #Get last laneSection overlapping to BSSD-lane
        last_overlapping_laneSection = df_linked_OpenDRIVE_lanes_BSSD_lane.loc[len(df_linked_OpenDRIVE_lanes_BSSD_lane)-1, 'laneSection_s']
                
        #Get list of all laneSections in the road of interest which have an s-coordinate equal/higher to s-coordinate of
        #the last laneSection overlapping to BSSD-lane
        list_laneSections_above = df_lane_data_road[round(df_lane_data_road['laneSection_s'], 3)>=round(last_overlapping_laneSection, 3)]\
                                    ['laneSection_s'].unique().tolist()
              
        #Iterate through the OpenDRIVE-lanes linked in the <successor>-element of the preceding OpenDRIVE-lane --> For every OpenDRIVE-lane it is 
        #checked whether it is equal to the OpenDRIVE-lane of interest
                                      
        #Get lane_id of last OpenDRIVE-lane overlapping with the BSSD-lane --> Is the starting OpenDRIVE-lane 
        curr_OpenDRIVE_lane_id = df_linked_OpenDRIVE_lanes_BSSD_lane.loc[len(df_linked_OpenDRIVE_lanes_BSSD_lane)-1, 'lane_id_OpenDRIVE']
        
        #Start iteration
        for s_curr_laneSection in list_laneSections_above:
            
            #Check if current OpenDRIVE-lane is the OpenDRIVE-lane of interest
            #If yes, return True --> OpenDRIVE-lane and BSSD-lane are related to each other
            if (round(s_curr_laneSection, 3)==round(laneSection_s, 3)) and (curr_OpenDRIVE_lane_id==lane_id_OpenDRIVE):
                return True
            
            #Get object for current OpenDRIVE-lane
            lane_object_current_OpenDRIVE_lane = OpenDRIVE_object.getRoad(road_id_OpenDRIVE).lanes.getLaneSection(s_curr_laneSection).\
                                                        getLane(curr_OpenDRIVE_lane_id)
                                                        
            #If current OpenDRIVE-lane has no successor, the OpenDRIVE-lane of interest is not related to the BSSD-lane
            if lane_object_current_OpenDRIVE_lane.link.successorId==None:
                return False        
            
            #Set for next iteration the id linked in successor to id of current OpenDRIVE-lane
            curr_OpenDRIVE_lane_id = lane_object_current_OpenDRIVE_lane.link.successorId
            
        #If OpenDRIVE-lane of interest was not found, return False
        return False
        