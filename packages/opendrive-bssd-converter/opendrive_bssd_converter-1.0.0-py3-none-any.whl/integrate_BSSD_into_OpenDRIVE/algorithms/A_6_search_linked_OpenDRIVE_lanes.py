import pandas as pd
from tqdm import tqdm

def A_6_search_linked_OpenDRIVE_lanes(df_overlappings_segments_laneSections, df_BSSD_lanes):
    """
    This function searches for all BSSD-lanes the linked OpenDRIVE-lanes.
    --> During the s-range of a BSSD-lane multiple OpenDRIVE-lanes may be defined as BSSD-segments and laneSections may have different borders.
    To link the BSSD- and the OpenDRIVE-lanes a structure is built into the xodr-file (Element <assignLaneOpenDRIVE>).
    This function is the basis for creating this structure as it creates a DataFrame which contains for every BSSD-lanes 
    the linked OpenDRIVE-lanes.

    Parameters
    ----------
    df_overlappings_segments_laneSections : DataFrame
        DataFrame which contains one row for every laneSection that overlaps a certain segment.
    df_BSSD_lanes : DataFrame
        DataFrame for storing all created BSSD-lanes

    Returns
    -------
    df_link_BSSD_lanes_with_OpenDRIVE_lanes : DataFrame
        DataFrame for storing information about link of BSSD-lanes to OpenDRIVE-lanes.
        For every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row is defined

    """
    
    #Create DataFrame for storing information about link of BSSD-lanes to OpenDRIVE-lanes
    #For every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row is defined
    df_link_BSSD_lanes_with_OpenDRIVE_lanes = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_s', 'lane_id_OpenDRIVE'])

    #Iteration through every road, which contains at least one BSSD-segment 
    for road_id in tqdm(df_overlappings_segments_laneSections['road_id'].unique()):
        
        #DataFrame which contains only information about the segments in the current road
        df_BSSD_lanes_current_road = df_BSSD_lanes[df_BSSD_lanes['road_id']==road_id]
        df_BSSD_lanes_current_road = df_BSSD_lanes_current_road.reset_index(drop=True)
        
        #Iteration through all segments in the current road to access the BSSD-lanes in the segments
        for segment_s in df_BSSD_lanes_current_road.loc[:, 'segment_s'].unique():
            
            #DataFrame which contains only information about all lanes in the current segment
            df_BSSD_lanes_current_segment = df_BSSD_lanes_current_road[df_BSSD_lanes_current_road['segment_s']==segment_s]
            df_BSSD_lanes_current_segment = df_BSSD_lanes_current_segment.reset_index(drop=True)
        
            #Create DataFrame which contains only laneSections overlapping with the current segment
            df_overlappings_current_segment = \
                df_overlappings_segments_laneSections[ (df_overlappings_segments_laneSections['road_id']==road_id) & \
                                                      (df_overlappings_segments_laneSections['segment_s']==segment_s)]  
            df_overlappings_current_segment = df_overlappings_current_segment.reset_index(drop=True)
            
            #Iteration through all BSSD-lanes in current segment to create link to OpenDRIVE-lanes for every BSSD-lane
            for index, lane_id_BSSD in enumerate(df_BSSD_lanes_current_segment.loc[:, 'lane_id_BSSD']):
                
                #Iteration through all laneSections which overlap to the current BSSD-Segment--> For every overlapping laneSection, a lane-Link has 
                #to be defined
                for index_2, laneSection_s in enumerate(df_overlappings_current_segment.loc[:, 'laneSection_s']):
                    
                    #Search for first overlapping laneSection -->iId of OpenDRIVE-lane is equal to id of BSSD-lane
                    if index_2==0:
                        
                        #Get the object of the first laneSection overlapping with current BSSD-lane (--> is stored in df_BSSD_lanes_current_segment)
                        first_laneSection_object = df_BSSD_lanes_current_segment.loc[index, 'laneSection_object_s_min']
                        
                        #Get object for the equivalent OpenDRIVE-lane in the first overlapping laneSection (id's are equally)
                        first_lane_object = first_laneSection_object.getLane(lane_id_BSSD)
                        
                        #Get s-coordinate of first laneSection overlapping with current BSSD-lane
                        s_first_laneSection = first_laneSection_object.sPos
                        
                        #Append data of first OpenDRIVE-lane overlapping with current BSSD-lane to overall DataFrame
                        df_link_BSSD_lanes_with_OpenDRIVE_lanes = df_link_BSSD_lanes_with_OpenDRIVE_lanes.append({'road_id': road_id,
                                                                                                                  'segment_s': segment_s,
                                                                                                                  'lane_id_BSSD': lane_id_BSSD,
                                                                                                                  'laneSection_s': s_first_laneSection,
                                                                                                                  'lane_id_OpenDRIVE': lane_id_BSSD},
                                                                                                                  ignore_index=True)
                        
                        #Check if a suceeding OpenDRIVE-lane exists
                        #If yes, store the id of the succeeding OpenDRIVE-lane to find it in the succeeding laneSection
                        if first_lane_object.link.successorId!=None:
                            id_succeeding_lane = first_lane_object.link.successorId
                        #If no, there is no succeeding overlapping laneSection    
                        else:
                            break
                        
                    #Not the first overlapping laneSection
                    else:
                        
                        #Get the object of the current laneSection
                        lane_section_object = df_overlappings_current_segment.loc[index_2, 'laneSection_object']
                        
                        #Get the object of the OpenDRIVE-lane in the current laneSection which is equivalent to the current BSSD-lane
                        lane_object = lane_section_object.getLane(id_succeeding_lane)
                        
                        #Append data of OpenDRIVE-lane overlapping with current BSSD-lane to overall DataFrame
                        df_link_BSSD_lanes_with_OpenDRIVE_lanes = df_link_BSSD_lanes_with_OpenDRIVE_lanes.append({'road_id': road_id,
                                                                                                                  'segment_s': segment_s,
                                                                                                                  'lane_id_BSSD': lane_id_BSSD,
                                                                                                                  'laneSection_s': laneSection_s,
                                                                                                                  'lane_id_OpenDRIVE': lane_object.id},
                                                                                                                  ignore_index=True)
                        
                        #Check if a suceeding OpenDRIVE-lane exists
                        #If yes, store the id of the succeeding OpenDRIVE-lane to find it in the succeeding laneSection
                        if lane_object.link.successorId!=None:
                            id_succeeding_lane = lane_object.link.successorId
                        #If no, there is no succeeding overlapping laneSection    
                        else:
                            break
    
    #Convert values in columns "road_id", "lane_id_BSSD" and "lane_id_OpenDRIVE" to int 
    df_link_BSSD_lanes_with_OpenDRIVE_lanes['road_id']=df_link_BSSD_lanes_with_OpenDRIVE_lanes['road_id'].convert_dtypes()
    df_link_BSSD_lanes_with_OpenDRIVE_lanes['lane_id_BSSD']=df_link_BSSD_lanes_with_OpenDRIVE_lanes['lane_id_BSSD'].convert_dtypes()
    df_link_BSSD_lanes_with_OpenDRIVE_lanes['lane_id_OpenDRIVE']=df_link_BSSD_lanes_with_OpenDRIVE_lanes['lane_id_OpenDRIVE'].convert_dtypes()
    
    
    number_BSSD_lanes = len(df_BSSD_lanes)
    number_links = len(df_link_BSSD_lanes_with_OpenDRIVE_lanes)
    
    print()
    
    #User output
    #Singular or Plural in console output
    if number_links == 1:
        print('Linked ' + str(number_links) + ' OpenDRIVE-lane to ' + str(number_BSSD_lanes) + ' BSSD-lane')
    elif (number_links > 1) & (number_BSSD_lanes == 1):
        print('Linked ' + str(number_links) + ' OpenDRIVE-lanes to ' + str(number_BSSD_lanes) + ' BSSD-lane')
    else:
        print('Linked ' + str(number_links) + ' OpenDRIVE-lanes to ' + str(number_BSSD_lanes) + ' BSSD-lanes')
    
    return df_link_BSSD_lanes_with_OpenDRIVE_lanes