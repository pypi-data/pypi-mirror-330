import bisect
import pandas as pd

def find_OpenDRIVE_lane(s_coordinate, t_coordinate, road_id, OpenDRIVE_object):
    """
    This function finds the OpenDRIVE-lane in which a defined point of a road in the OpenDRIVE-map (s-,t-coordinate & road_id) is located.
    Beyond that the distance in t-direction to the left and right border of the lane inside which the point is located is returned.
    
    If the point is not located inside a OpenDRIVE-lane the function returns None
    
    This function is used to to assert objects in the OpenDRIVE-map to BSSD-lane borders.

    Parameters
    ----------
    s_coordinate : float
        s-coordinate of the point (reference line system)
    t_coordinate : float
        t-coordinate of the point (reference line system)
    road_id : int
        id of the road where the point is located
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map

    Returns
    -------
    laneSection_s : float
        s-coordinate of laneSection where the point is located (None if point is located outside of the road)
    lane_id : int
        id of lane in which the point is located (None if point is located outside of a lane)
    delta_t_right : float
        distance in t-direction from point to right border of lane inside which point is located (None if point is located outside of a lane)
    delta_t_left : float
        distance in t-dircetion from point to left border of lane inside which point is located (None if point is located outside of a lane)
    """

    #Return values (default to None, if point is not located in a lane/in the road --> Can be outside of defined area)
    laneSection_s = None
    lane_id = None
    delta_t_right = None
    delta_t_left = None
    
    #Get object of road in which the point is located
    road_object = OpenDRIVE_object.getRoad(road_id)
    
    #Get length of road to check if s-coordinate is valid
    road_length = road_object.length
    
    #Return None if s-coordinate is higher than length of the road
    if s_coordinate>road_length:
        return laneSection_s, lane_id, delta_t_right, delta_t_left
    #Return None if s-coordinate is below zero 
    if s_coordinate < 0:
        return laneSection_s, lane_id, delta_t_right, delta_t_left
        
    #Get lanes object of road (Element <lanes>)
    lanes_object = road_object.lanes
    
    #Get all laneSections in the road of interest to find the laneSection which is valid at the s-coordinate at the point of interest
    list_laneSections_road = []
    for laneSection_object in lanes_object.lane_sections:
        list_laneSections_road.append(laneSection_object.sPos)
      
    #Get object of laneSection which is valid at the s-coordinate of the point
    index_laneSection_s = bisect.bisect_right(list_laneSections_road, s_coordinate) - 1
    laneSection_object = lanes_object.lane_sections[index_laneSection_s]
    #Get s-coordinate of laneSection which is valid at the s-coordinate of the point
    laneSection_s = laneSection_object.sPos
    
    ##Get offset of center lane and reference line (<laneOffset>)
    #List for storing s-coordinates of all <laneOffset>-elements which are defined in the road of interest
    list_laneOffsets = []
    
    #Append s-coordinates of all <laneOffset>-elements which are defined in the road of interest to list
    for laneOffset_object in lanes_object.laneOffsets:
        list_laneOffsets.append(laneOffset_object.start_pos)
    
    #If no <laneOffset>-elements exist in current road, there is no offset between reference line and center lane
    if len(list_laneOffsets)==0:
        t_center_lane = 0.0
    else:
        
        #Get s-coordinate of laneOffset which is valid at the s-coordinate of the point
        index_laneOffset_s = bisect.bisect_right(list_laneOffsets, s_coordinate) - 1
        
        #Check if there is no laneOffset defined at the s-coordinate of the point of interest
        #--> no offset between reference line and center lane
        if index_laneOffset_s < 0:
            t_center_lane = 0.0
        
        #If there is a laneOffset defined at the s-coordinate of the point of interest, calculate this laneOffset            
        else:
             
            laneOffset_s =  list_laneOffsets[index_laneOffset_s]
            
            #Get object of <laneOffset>-element valid at the s-coordinate of the point
            laneOffset_object = lanes_object.laneOffsets[index_laneOffset_s]
            
            #Get polynomial coefficients a, b, c and d describing the laneOffset at a defined s-coordinate
            #offset (ds) = a + b*ds + c*ds² + d*ds³
            coefficients_laneOffset = laneOffset_object.polynomial_coefficients
            a_laneOffset = coefficients_laneOffset[0]
            b_laneOffset = coefficients_laneOffset[1]
            c_laneOffset = coefficients_laneOffset[2]
            d_laneOffset = coefficients_laneOffset[3]
            
            #Get variable ds for calculating the laneOffset at the s-coordinate of the point
            #--> s-range from begin of <laneOffset>-element to s-coordinate of the point
            ds = s_coordinate - laneOffset_s
            
            #Calculate offset between reference line and center lane at s-coordinate of point
            #(= t-coordinate of center lane at s-coordinate of point)
            t_center_lane = a_laneOffset + b_laneOffset*ds + c_laneOffset*ds*ds + d_laneOffset*ds*ds*ds
    
    ##Calculate width of OpenDRIVE-lanes at point of interest
    #Create DataFrame which stores the width of all OpenDRIVE-lanes at the point of interest
    df_width_lanes = pd.DataFrame(columns = ['lane_id', 'width_at_point'])

    #Create DataFrame which stores the t-coordinate of the outer border of all OpenDRIVE-lanes at the point of interest 
    #Only necessary if lane width is defined with <border>-elements
    df_border_lanes = pd.DataFrame(columns = ['lane_id', 't_outer_border'])
    
    #Iterate through all lanes of laneSection to calculate the width of each lane at the s-coordinate of the point 
    for lane_object in laneSection_object.allLanes:
        lane_id = lane_object.id
        
        #Skip center lane --> Has no width
        if lane_id == 0:
            continue
        
        #Check if width of lane is defined with <width>-element (usally the case)
        if lane_object.has_border_record == False:
            
            #List for storing absolute s-coordinates of all <width>-elements which are defined in the current lane
            list_laneWidths = []
        
            #Iterate through all <width>-elements of current lane
            for lane_width_object in lane_object.widths:
                #Store absolute s-coordinate of <width>-element (= sOffset + s-coordinate of laneSection) in list
                list_laneWidths.append(lane_width_object.start_offset + laneSection_s)
                
            #Get s-coordinate of <width>-element which is valid at the s-coordinate of the point
            index_laneWidth_s = bisect.bisect_right(list_laneWidths, s_coordinate) - 1
            laneWidth_s =  list_laneWidths[index_laneWidth_s]
            
            #Get object of <width>-element valid at the s-coordinate of the point
            lane_width_object = lane_object.widths[index_laneWidth_s]
            
            #Get polynomial coefficients a, b, c and d describing the lane width at a defined s-coordinate
            #Width (ds) = a + b*ds + c*ds² + d*ds³
            coefficients_laneWidth = lane_width_object.polynomial_coefficients
            
            a_lane_width = coefficients_laneWidth[0]
            b_lane_width = coefficients_laneWidth[1]
            c_lane_width = coefficients_laneWidth[2]
            d_lane_width = coefficients_laneWidth[3]
            
            #Get variable ds for calculating the lane width  at the s-coordinate of the point
            #--> s-range from begin of <width>-element to s-coordinate of the point
            ds = s_coordinate - laneWidth_s
            
            #Calculate width of current lane at s-coordinate of point
            width_at_point = a_lane_width + b_lane_width*ds + c_lane_width*ds*ds + d_lane_width*ds*ds*ds
            
            #Append width of current lane to DataFrame
            df_width_lanes = df_width_lanes.append({'lane_id': lane_id, 'width_at_point': width_at_point}, ignore_index=True)
            
        #If width of lane is not defined by <width>-element it is defined by <border>-element --> Width is defined by outer t-coordinate of lane   
        else:
            
            #List for storing absolute s-coordinates of all <border>-elements which are defined in the current lane
            list_laneBorders = []
            
            #Iterate through all <border>-elements of current lane
            for lane_border_object in lane_object.borders:
                
                #Store absolute s-coordinate of <border>-element (= sOffset + s-coordinate of laneSection) in list
                list_laneBorders.append(lane_border_object.start_offset + laneSection_s)
                
            #Get s-coordinate of <border>-element which is valid at the s-coordinate of the point
            index_border_s = bisect.bisect_right(list_laneBorders, s_coordinate) - 1
            border_s =  list_laneBorders[index_border_s]
            
            #Get object of <border>-element valid at the s-coordinate of the point
            lane_border_object = lane_object.borders[index_border_s]
            
            #Get polynomial coefficients a, b, c and d describing the lane width at a defined s-coordinate
            #t_border (ds) = a + b*ds + c*ds² + d*ds³
            coefficients_laneBorder = lane_border_object.polynomial_coefficients
            
            a_lane_border = coefficients_laneBorder[0]
            b_lane_border = coefficients_laneBorder[1]
            c_lane_border = coefficients_laneBorder[2]
            d_lane_border = coefficients_laneBorder[3]
            
            #Get variable ds for calculating the t-coordinate of the outer border of the current lane at the s-coordinate of the point
            #--> s-range from begin of <border>-element to s-coordinate of the point
            ds = s_coordinate - border_s
            
            #Calculate t-coordinate of outer border of current lane at s-coordinate of point
            t_outer_border = a_lane_border + b_lane_border*ds + c_lane_border*ds*ds + d_lane_border*ds*ds*ds
            
            #Append t-coordinate of outer border of current lane to DataFrame
            df_border_lanes = df_border_lanes.append({'lane_id': lane_id, 't_outer_border': t_outer_border}, ignore_index=True)
    
    
    #Check if width of lanes is defined with <width>-elements (usally the case)
    if len(df_width_lanes)>0:
        
        #Function calculating the t-coordinates of the right and left border of every lane based on the <width>-Elements
        df_right_left_border_lanes = iterate_df_width_or_border(df_width_lanes, t_center_lane)
        
    elif len(df_border_lanes)>0:
        #Function calculating the t-coordinates of the right and left border of every lane based on the <border>-Elements
        df_right_left_border_lanes = iterate_df_width_or_border(df_border_lanes, t_center_lane)
            
        
    #Iterate through right/left borders of lanes in laneSection of interest to find the lane where the point of interest is located
    for index, lane_id in enumerate(df_right_left_border_lanes.loc[:, 'lane_id']):
        
        #Get t-coordinate of right and left border of current lane
        t_right_border_current_lane = df_right_left_border_lanes.loc[index, 't_right_border']
        t_left_border_current_lane = df_right_left_border_lanes.loc[index, 't_left_border']
        
        #Point of interest is located in the current lane if the t-coordinate of the point is higher than the t-coordinate of the right border
        #but lower than the t-coordinate of the left border 
        #If the point is exactly on a border between two lanes, it is assigned to the lane with the lower id as the lanes are sorted ascending in 
        #df_right_left_border_lanes
        if (t_coordinate >= t_right_border_current_lane) and (t_coordinate <= t_left_border_current_lane):
            
            #Get distance in t-direction from point of interest to right and left border of the lane
            delta_t_right = t_coordinate - t_right_border_current_lane
            delta_t_left = t_left_border_current_lane - t_coordinate
            
            delta_t_right = round(delta_t_right, 2)
            delta_t_left = round(delta_t_left, 2)
            
            return laneSection_s, int(lane_id), delta_t_right, delta_t_left
        
    #If no matching lane could be found, the point of interest is located outside of the road 
    #--> No lane defined at point of interest
    return laneSection_s, None, delta_t_right, delta_t_left
    
def iterate_df_width_or_border(df_lanes_t_data, t_center_lane):
    """
    This function calculates a DataFrame containing the t-coordinates of the right and left border of every lane based on the <width>-
    or <border>-Elements which are defined at the point of interest.
    
    The data for the <width>- or <border>-elements is contained in the passed DataFrame "df_lanes_t_data":
        - In the case of <width>-elements (usually the case), the DataFrame df_lane_t_data is df_width_lanes
        - In the case of <border>-elements, the DataFrame df_lane_t_data is df_border_lanes
    """
    
    #Get subset of df_lanes_t_data which contains only the lanes on the right side (id < 0)
    df_lanes_t_data_right = df_lanes_t_data[df_lanes_t_data['lane_id']<0]
    #Sort values descending by id's (-1, -2, ...)
    df_lanes_t_data_right = df_lanes_t_data_right.sort_values(['lane_id'], ascending=False)
    df_lanes_t_data_right = df_lanes_t_data_right.reset_index(drop=True)
    
    #Get subset of df_lanes_t_data which contains only the lanes on the left side (id > 0)
    df_lanes_t_data_left = df_lanes_t_data[df_lanes_t_data['lane_id']>0]
    #Sort values ascending by id's (1, 2, ...)
    df_lanes_t_data_left = df_lanes_t_data_left.sort_values(['lane_id'])
    df_lanes_t_data_left = df_lanes_t_data_left.reset_index(drop=True)
    
    #Create DataFrame to store the t-coordinate of the right and left border of each lane
    df_right_left_border_lanes = pd.DataFrame(columns = ['lane_id', 't_left_border', 't_right_border'])
    
    #Check if passed DataFrame contains data for <width> or for <border>-elements
    #Case 1: Contains data for <width>-elements --> usually the case
    if df_lanes_t_data.columns[1]=='width_at_point':
        dataframe_contains = 'width'
        
    #Case 2: Contains data for <border>-elements
    else:
        dataframe_contains = 'border'
    
    #Iterate through lanes on the right side of the road (id<0) to calculate t-coordinates of right and left border of lanes
    for index, lane_id in enumerate(df_lanes_t_data_right.loc[:, 'lane_id']):
        
        #Case 1: Passed DataFrame contains data for <width>-elements
        if dataframe_contains == 'width':
        
            #Get width of current lane at s-coordinate of point of interest
            lane_width_current_lane = df_lanes_t_data_right.loc[index, 'width_at_point']
            
            #Special case: Lane with id -1 --> t_left_border = t_center_lane
            if lane_id == -1:
                t_left_border = t_center_lane
                #Right  border of current lane = Left border of current lane - width of current lane
                t_right_border = t_left_border - lane_width_current_lane
            else:
                #Right border of preceding lane = Left border of current lane
                t_left_border = t_right_border        
                
                #Right  border of current lane = Left border of current lane - width of current lane
                t_right_border = t_left_border - lane_width_current_lane
        
        #Case 2: Passed DataFrame contains data for <border>-elements
        else:
            
            #Get outer border of current lane at s-coordinate of point of interest
            lane_border_current_lane = df_lanes_t_data_right.loc[index, 't_outer_border']
            
            #Special case: Lane with id -1 --> t_left_border = t_center_lane = 0.0
            if lane_id == -1:
                #In the case of <border>-elements, the center lane is always at t=0.0 (No <laneOffset> possible)
                t_left_border = 0.0
                #Right border of current lane = t-coordinate of outer border of current lane
                t_right_border = lane_border_current_lane
            else:
                #Right border of preceding lane = Left border of current lane
                t_left_border = t_right_border        
                
                #Right border of current lane = t-coordinate of outer border of current lane
                t_right_border = lane_border_current_lane
            
        #Append data of current lane to DataFrame
        df_right_left_border_lanes = df_right_left_border_lanes.append({'lane_id': lane_id, 't_left_border': t_left_border,
                                                                        't_right_border': t_right_border}, ignore_index=True)
        
    #Iterate through lanes on the left  side of the road (id>0) to calculate t-coordinates of right and left border of lanes
    for index, lane_id in enumerate(df_lanes_t_data_left.loc[:, 'lane_id']):
        
        #Case 1: Passed DataFrame contains data for <width>-elements
        if dataframe_contains == 'width':
        
            #Get width of current lane at s-coordinate of point of interest
            lane_width_current_lane = df_lanes_t_data_left.loc[index, 'width_at_point']
            
            #Special case: Lane width id 1 --> t_right_border = t_center_lane
            if lane_id == 1:
                t_right_border = t_center_lane
                
                #Left border of current lane = right border of current lane + width of current lane
                t_left_border = t_right_border + lane_width_current_lane
            else:
                #Left border of preceding lane = right border of current lane
                t_right_border = t_left_border        
                
                #Left border of current lane = right border of current lane + width of current lane
                t_left_border = t_right_border + lane_width_current_lane
        
        #Case 2: Passed DataFrame contains data for <border>-elements     
        else:
            
            #Get border of current lane at s-coordinate of point of interest
            lane_border_current_lane = df_lanes_t_data_left.loc[index, 't_outer_border']
            
            #Special case: Lane with id -1 --> t_left_border = t_center_lane = 0.0
            if lane_id == 1:
                #In the case of <border>-elements, the center lane is always at t=0.0 (No <laneOffset> possible)
                t_right_border = 0.0
                
                #Left border of current lane = t-coordinate of outer border of current lane
                t_left_border = lane_border_current_lane
            else:
                #Left border of preceding lane = right border of current lane
                t_right_border = t_left_border        
                
                #Left border of current lane = t-coordinate of outer border of current lane
                t_left_border = lane_border_current_lane
        
        #Append data of current lane to DataFrame
        df_right_left_border_lanes = df_right_left_border_lanes.append({'lane_id': lane_id, 't_left_border': t_left_border,
                                                                        't_right_border': t_right_border}, ignore_index=True)
        
    #Sort df by lane_id
    df_right_left_border_lanes = df_right_left_border_lanes.sort_values(['lane_id'])
    df_right_left_border_lanes = df_right_left_border_lanes.reset_index(drop=True)
    
    return df_right_left_border_lanes
    