from integrate_BSSD_into_OpenDRIVE.algorithms.A_7_1_extract_speed_attribute import A_7_1_extract_speed_attribute


def A_7_extract_behavioral_attributes_automatically(df_lane_data, df_BSSD_lanes, df_link_BSSD_lanes_with_OpenDRIVE_lanes, df_speed_limits, df_segments, 
                                                    driving_direction, OpenDRIVE_object):
    """
    This function extracts BSSD behavioral attributes automatically based on the informations contained in the imported OpenDRIVE-file.
    This includes the following subfunctions, which are each representative for one behavioral attribute:
        1. Extraction of BSSD behavioral attribute "speed" based on the speed limits defined in the imported OpenDRIVE-file 
           --> subfunction A_7_1_extract_speed_attribute.py
        
        Extraction of other behavioral attributes could be added here
        ...

    Parameters
    ----------
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file.
    df_BSSD_lanes : DataFrame
        DataFrame containing all created BSSD-lanes. For every BSSD-lane the object for the first laneSection overlapping
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

    ##1.BEHAVIORAL ATTRIBUTE "SPEED"
    
    #Execute subfunction for extracting behvavioral attribute 'speed' in BSSD lanes 
    df_BSSD_speed_attribute = A_7_1_extract_speed_attribute(df_lane_data, df_BSSD_lanes, df_link_BSSD_lanes_with_OpenDRIVE_lanes, df_speed_limits,
                                                            df_segments, driving_direction, OpenDRIVE_object)
    
    ##Extraction of additional behavioral attributes could be added here...
                              

    return df_BSSD_speed_attribute                                                                                

    
