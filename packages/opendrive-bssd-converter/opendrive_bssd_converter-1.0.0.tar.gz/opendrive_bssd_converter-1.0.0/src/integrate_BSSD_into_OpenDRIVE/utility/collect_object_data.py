import pandas as pd
from tqdm import tqdm
import math

from integrate_BSSD_into_OpenDRIVE.utility.find_OpenDRIVE_lane import find_OpenDRIVE_lane

def collect_object_data(OpenDRIVE_object):
    """
    This function parses all objects in the imported OpenDRIVE-file and creates a DataFrame containing certain data about every object that doesn't
    fulfill the following conditions:
        - Object that are placed in a height that is not of interest for motor vehicles (Maximum height = 4m --> see StVO §22, Absatz 2)
        - Objects that are not placed on the road (s-, and t-coordinate)
        - If object is <repeat>-element, it has to represent only one object (attribute "distance"=0)
        
    --> Conditions match to all objects which are not of interest for analyzing crossability of BSSD-lane borders
    (function "classify_BSSD_lane_borders")
    
    In this function, an object is an object represented by an <object>- or a <repeat>-element.
    Therefore it is itereted through all <object>-elements and in every <object>-element through all <repeat>-elements
    --> Only if the element fulfills the mentioned conditions it is added to the DataFrame
    
    Parameters
    ----------
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map

    Returns
    -------
    df_object_data : DataFrame
        DataFrame containing information about all objects which are represented by <object> and <repeat>-elements which don't fulfill the following
        conditions:
            - Object that are placed in a height that is not of interest for motor vehicles (Maximum height = 4m --> see StVO §22, Absatz 2 )
            - Objects that are not placed on the road (s-, and t-coordinate)
            - If object is <repeat>-element, it has to represent only one object (attribute "distance"=0)
    
    """
    
    #Create DataFrame to store data for objects in the imported OpenDRIVE-file
    #Column repeat contains True or False depending on whether object is represented by an <object>- (False) or an <repeat>-element (True)
    #Columns s_origin & t_origin store s- and t-coordinate of origin of local coordinate system (u, v, z) of object
    #Columns delta_t_left, delta_t_right store distance of objects origin to left/right border of lane in which the origin of the object is located
    #Columns s_min, s_max store the extent of the object in s-direction
    df_object_data = pd.DataFrame(columns = ['object_id', 'repeat', 'type','road_id', 'laneSection_s', 'lane_id', 's_origin', 't_origin', 'delta_t_left', 
                                             'delta_t_right', 's_min', 's_max'])
    
    #Maximum height of a motor vehicle (in m)
    #Currently set to 4 m as maximum height of motor vehicle + load is 4 m according to StVO §22, Absatz 2
    maximum_height_motor_vehicle = 4
    
    print('Analyzing objects in imported OpenDRIVE-file...\n')
    
    ##1. <OBJECT>-ELEMENTS
    
    #Iterate through all roads in OpenDRIVE-object to get all objects in every road
    for road_object in tqdm(OpenDRIVE_object.roads):
        
        #Get id of current road
        road_id = road_object.id
        
        #Iterate through all <object>-elements in current road to collect data of <object>-elements and subordinated <repeat>-elements
        for object_object in tqdm(road_object.objects, leave=False):
            
            #Variable to store information whether current <object>-element should be stored in df_object_data
            #--> All objects that fulfill the conditions mentioned above are stored in the DataFrame
            include_in_df = True
            
            #Get s- and t-coordinate of origin of object
            object_s_origin = object_object.s
            object_t_origin = object_object.t
                        
            #Call function to calculate the minimum and maximum s-coordinate, and the minimum and maximum h-coordinate of the extend of the object
            object_s_min, object_s_max, object_h_min, object_h_max = object_calculate_s_min_s_max_h_min_h_max(object_object)
            
            #Check if origin of object is defined in h-direction 
            #Case 1: origin of object is defined in h-direction --> Check for minimum height of object (h_min)
            if object_h_min!=None:
                
                #Check if minimum height is greater than maximum height of a motor vehicle 
                #If yes, skip this object as it is in a height not relevant for a motor vehicle
                #For loop is still executed to process all <repeat>-elements which are defined within current <object>-element
                if object_h_min > maximum_height_motor_vehicle:
                    include_in_df = False
                                   
            #Get id of current object
            object_id = object_object.id
            
            #Get type of current object (For information purposes)
            object_type = object_object.type
            
            #Locate object inside current road (function find_OpenDRIVE_lane)
            laneSection_s, lane_id, delta_t_right, delta_t_left = find_OpenDRIVE_lane(object_s_origin, object_t_origin, road_id, OpenDRIVE_object)
            
            #Consider object only if it is located inside the road (--> Located in a lane)
            #For loop is still executed to process all <repeat>-elements which are defined within current <object>-element
            if lane_id == None:
                include_in_df = False
            
            #Paste data of current <object>-element only if it fulfills all contions mentioned at the beginning of the function
            if include_in_df==True:
                    
                #Append data of <object>-element to overall DataFrame
                df_object_data = df_object_data.append({'object_id': object_id, 'repeat': False, 'type': object_type, 'road_id': road_id, 'laneSection_s': laneSection_s, 'lane_id': lane_id,
                                                        's_origin': round(object_s_origin, 2), 't_origin': round(object_t_origin, 2),
                                                        'delta_t_left': delta_t_left, 'delta_t_right': delta_t_right,
                                                        's_min': round(object_s_min, 2), 's_max': round(object_s_max, 2)},
                                                       ignore_index=True)
            
            ##2. <REPEAT>-ELEMENTS
            
            #Iterate through all <repeat>-elements of current <object>-elements to collect data 
            for repeat_object in object_object.repeats:
                
                #Skip all <repeat>-elements that represent more than one object (Have an attribute "distance" which is not zero)
                #--> These objects are not of interest as they cannot lead to a not crossable border
                if repeat_object.distance != 0:
                    continue
                
                #Get zOffset and height of object (average value between start and end value) for checking minimum height of object
                repeat_object_z_Offset = (repeat_object.zOffsetStart + repeat_object.zOffsetEnd)*0.5
                
                #Check if minimum height is greater than maximum height of a motor vehicle 
                #If yes, skip this object as it is in a height not relevant for a motor vehicle
                if repeat_object_z_Offset > maximum_height_motor_vehicle:
                    continue
                
                #Get s- and t-coordinate of origin of object (= center of object)
                #Center of object in s-direction is s-coordinate + 0.5*length --> s-coordinate of <repeat>-object is the starting point of the object
                repeat_object_s_origin = repeat_object.s + 0.5*repeat_object.length
                #Center of object in t-direction is average value of tStart and tEnd coordinate
                repeat_object_t_origin = (repeat_object.tStart + repeat_object.tEnd)*0.5
                
                #Locate object inside current road (function find_OpenDRIVE_lane)
                laneSection_s, lane_id, delta_t_right, delta_t_left = find_OpenDRIVE_lane(repeat_object_s_origin, repeat_object_t_origin,
                                                                                          road_id, OpenDRIVE_object)     
                                
                #Skip object if it is located outside the road (--> Not located in a lane)
                if lane_id == None:
                    continue
                
                #Get minimum and maximum s-coordinate of object
                #Minimum s-coordinate is attribute "s" --> Contains starting s-coordinate 
                repeat_object_s_min = repeat_object.s
                #Maxmium s-coordinate is attribue "s" + attribut "length"
                repeat_object_s_max = repeat_object.s + repeat_object.length
                
                #Append data of <repeat>-element to overall DataFrame
                df_object_data = df_object_data.append({'object_id': object_id, 'repeat': True, 'type': object_type, 'road_id': road_id,
                                                        'laneSection_s': laneSection_s, 'lane_id': lane_id,
                                                        's_origin': round(repeat_object_s_origin, 2),
                                                        't_origin': round(repeat_object_t_origin, 2), 'delta_t_left': delta_t_left,
                                                        'delta_t_right': delta_t_right, 's_min': round(repeat_object_s_min, 2),
                                                        's_max': round(repeat_object_s_max, 2)},
                                                       ignore_index=True)
                    
    print()
    
    #User output
    if len(df_object_data)==1:
        
        print('Found ' + str(len(df_object_data)) + ' object in imported OpenDRIVE-file which is of interest for crossability of BSSD-lane borders\n')
    else:
        print('Found ' + str(len(df_object_data)) + ' objects in imported OpenDRIVE-file which are of interest for crossability of BSSD-lane borders\n')
        
    return df_object_data
                
def object_calculate_s_min_s_max_h_min_h_max(object_object):
    """
    This function calculates the minimum and maximum s-coordinate, and the minimum and maximum h-coordinate of the extend of an object.
    This is done by transforming the extend of the object from the local coordinate system into the reference coordinate system and adding
    the extend in s- respectively h-coordinates to the origin of the object in s- respectively h-coordinate.
    """
    
    #Get s-coordinate of origin of object
    object_s_origin = object_object.s
    
    #Get z-coordinate of origin to check height of object
    object_z_Offset = object_object.zOffset
    
    #Get dimensions of object as float to check if object is defined as cuboid (length, width, height), as cylinder (radius, height)
    #or as point object
    object_length = transform_dimensions_to_float(object_object.length)
    object_width = transform_dimensions_to_float(object_object.width)
    object_height = transform_dimensions_to_float(object_object.height)
    object_radius = transform_dimensions_to_float(object_object.radius)
    
    #Get rotation angles of object (rotation of local coordinate system to reference coordinate system)
    object_heading = transform_dimensions_to_float(object_object.hdg)
    gamma = object_heading
    object_pitch = transform_dimensions_to_float(object_object.pitch)
    beta = object_pitch
    object_roll = transform_dimensions_to_float(object_object.roll)
    alpha = object_roll
    
    #Case 1: Cuboid --> Object has no defined radius and at least one dimension of length, width or height is defined
    if ((object_length>0) or (object_width>0) or (object_height>0)) and (object_radius==0):
        
        #Get minimum and maximum coordinates of object in local coordinate system (u, v, z)
        #Origin of local coordinate system is in center of object --> Minimum and maximum coordinate are half of length, width, height
        u_min = -0.5*object_length
        u_max = 0.5*object_length
        
        v_min = -0.5*object_width
        v_max = 0.5*object_width
        
        z_min = -0.5*object_height
        z_max = 0.5*object_height
        
        #Call function to get extend of object in s-coordinates
        s_extend_min, s_extend_max = calculate_extend_in_s_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha, beta, gamma)
        
        #Extend in h-coordinates only of interest if height of origin is specified
        if object_z_Offset!='None':
            
            #Call function to get extend of object in h-coordinate
            h_extend_min, h_extend_max = calculate_extend_in_h_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha, beta, gamma)
        
    #Case 2: Cylinder --> Object has a defined radius
    elif (object_radius>0):
        
        #Get minimum and maximum coordinates of object in local coordinate system (u, v, z)
        #Origin of local coordinate system is in center of object
        u_min = -object_radius
        u_max = object_radius
        
        v_min = -object_radius
        v_max = object_radius
        
        z_min = -0.5*object_height
        z_max = 0.5*object_height
        
        #Call function to get extend of object in s-coordinate
        s_extend_min, s_extend_max = calculate_extend_in_s_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha, beta, gamma)
        
        #Extend in h-coordinates only of interest if height of origin is specified
        if object_z_Offset!='None':
            
            #Call function to get extend of object in h-coordinate
            h_extend_min, h_extend_max = calculate_extend_in_h_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha, beta, gamma)
        
    #Case 3: Point object --> Object has no extend
    else:
        
        s_extend_min = 0
        s_extend_max = 0
        
        h_extend_min = 0
        h_extend_max = 0
        
    #Minimum/Maximum s-coordinate of object can be calculated from origin of object and extend of object in s-direction
    s_min = object_s_origin + s_extend_min
    s_max = object_s_origin + s_extend_max

    #Extend in h-coordinates only of interest if height of origin is specified
    if object_z_Offset!='None':
        #Minimum/Maximum h-coordinate of object can be calculated from origin of object and extend of object in h-direction
        h_min = float(object_z_Offset)+h_extend_min
        h_max = float(object_z_Offset)+h_extend_max
    else:
        #If no height of origin is defined, return None for extend in h-direction
        h_min = None 
        h_max = None
    
    return s_min, s_max, h_min, h_max
       
        
def transform_dimensions_to_float(dimension):
    """
    This function transforms a dimension of an object_object (length, width, height, radius), which is stored as a string in the
    object_object, to a float value. If the dimension is not defined, it is set to 0.0
    """
    
    if (dimension!='None' and (float(dimension)!=0)):
        dimension = float(dimension)
    else:
        dimension = 0.0
        
    return dimension

def calculate_extend_in_s_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha, beta, gamma):
    """
    This function calculates the extend of an object in the s-coordinate based on the extend of the object in the local coordinate system 
    u, v, z and the rotation between the local coordinate system and the reference coordinate system (heading: gamma, pitch: beta, roll: alpha)
    """
    
    #Function to calculate the s-coordinate from one point in local coordinate system (u, v, z) 
    f = lambda u, v, z, alpha, beta, gamma: u*math.cos(beta)*math.cos(gamma) - \
                                            v*(math.cos(alpha)*math.sin(gamma)-math.cos(gamma)*math.sin(alpha)*math.sin(beta)) +\
                                            z*(math.sin(alpha)*math.sin(gamma)+math.cos(alpha)*math.cos(gamma)*math.sin(beta))
    
    #Calculate s-coordinates of corner points of cuboid
    s_1 = f(u_max, v_max, z_max, alpha, beta, gamma)
    s_2 = f(u_max, v_max, z_min, alpha, beta, gamma)
    s_3 = f(u_max, v_min, z_max, alpha, beta, gamma)
    s_4 = f(u_max, v_min, z_min, alpha, beta, gamma)
    s_5 = f(u_min, v_max, z_max, alpha, beta, gamma)
    s_6 = f(u_min, v_max, z_min, alpha, beta, gamma)
    s_7 = f(u_min, v_min, z_max, alpha, beta, gamma)
    s_8 = f(u_min, v_min, z_min, alpha, beta, gamma)
    
    s_corner_points = [s_1, s_2, s_3, s_4, s_5, s_6, s_7, s_8]
    
    #Minimum and maximum s-coordinate of object is corner with minimum and corner maximum s-coordinate
    s_extend_min = min(s_corner_points)
    s_extend_max = max(s_corner_points)
    
    s_extend_min = round(s_extend_min, 2)
    s_extend_max = round(s_extend_max, 2)
    
    return s_extend_min, s_extend_max


def calculate_extend_in_h_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha, beta, gamma):
    """
    This function calculates the extend of an object in the h-coordinate based on the extend of the object in the local coordinate system 
    u, v, z and the rotation between the local coordinate system and the reference coordinate system (heading: gamma, pitch: beta, roll: alpha)
    """
    
    #Function to calculate the h-coordinate from one point in local coordinate system (u, v, z) 
    f = lambda u, v, z, alpha, beta, gamma: -u*math.sin(beta) + v*math.cos(beta)*math.sin(alpha) + z*math.cos(alpha)*math.cos(beta) 
    
    #Calculate h-coordinates of corner points of cuboid
    h_1 = f(u_max, v_max, z_max, alpha, beta, gamma)
    h_2 = f(u_max, v_max, z_min, alpha, beta, gamma)
    h_3 = f(u_max, v_min, z_max, alpha, beta, gamma)
    h_4 = f(u_max, v_min, z_min, alpha, beta, gamma)
    h_5 = f(u_min, v_max, z_max, alpha, beta, gamma)
    h_6 = f(u_min, v_max, z_min, alpha, beta, gamma)
    h_7 = f(u_min, v_min, z_max, alpha, beta, gamma)
    h_8 = f(u_min, v_min, z_min, alpha, beta, gamma)
    
    h_corner_points = [h_1, h_2, h_3, h_4, h_5, h_6, h_7, h_8]
    
    #Minimum and maximum h-coordinate of object is corner with minimum and corner maximum h-coordinate
    h_extend_min = min(h_corner_points)
    h_extend_max = max(h_corner_points)
    
    h_extend_min = round(h_extend_min, 2)
    h_extend_max = round(h_extend_max, 2)
    
    return h_extend_min, h_extend_max
                   