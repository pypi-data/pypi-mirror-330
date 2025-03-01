import xml.etree.ElementTree as ET
import pandas as pd
pd.options.mode.chained_assignment = None
from tqdm import tqdm
from rich.console import Console
console = Console(highlight=False)


from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_extract_segments_automatically import A_3_extract_segments_automatically
from integrate_BSSD_into_OpenDRIVE.algorithms.A_4_manually_edit_segments import A_4_manually_edit_segments
from integrate_BSSD_into_OpenDRIVE.utility.access_BSSD_user_data_element import access_BSSD_user_data_element

def step_3_create_BSSD_segments(df_lane_data, df_lane_data_drivable_lanes, OpenDRIVE_element, OpenDRIVE_object):
    """
    This function executes Step 3 of BSSD-Integration into OpenDRIVE.
    In every road that contains at least one drivable lanes the BSSD-segments are created. One BSSD-segment is represented by a <segment>-element.
    To define which BSSD-Segments are created, two substeps are executed:
        1. Function "A_3_extract_segments_automatically.py": Automatic extraction of segments based on information from imported OpenDRIVE-file
        2. Function "A_4_manually_edit_segments.py": Manual editing (Adding & Removing) of segments by giving a s-coordinate as input
        
        
    Parameters
    ----------
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file.
    df_lane_data_drivable_lanes : DataFrame
        Subset of df_lane_data, which only contains lanes that represent a drivable OpenDRIVE-lane
    OpenDRIVE_element : etree.ElementTree.Element
        Element for the xodr-file --> Needed for modifying the xodr-file
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map
        
    Returns
    -------
    df_segments : DataFrame
        DataFrame which contains all created BSSD-segments. 
        For every segment a start-s-coordinate is given. If the segments ends before the next segment in the road 
        or before the end of the road, a defined end-s-coordinate is given (BSSD definition gap).
    df_speed_limits : DataFrame
        DataFrame which contains one row for every <speed>-element (defined in the OpenDRIVE-<lane>-elements)
        which is defined in the imported OpenDRIVE-file for a drivable lane
    OpenDRIVE_element : etree.ElementTree.Element
        Modified OpenDRIVE_element
   
    """
    
    #SUBSTEP 1: Automatic extraction of segments based on information from imported OpenDRIVE-file
    print()
    print('Automatic extraction of BSSD-segments...\n')
    df_segments_automatic, df_speed_limits = A_3_extract_segments_automatically(df_lane_data, df_lane_data_drivable_lanes, OpenDRIVE_object)
    
    #SUBSTEP 2: Manual editing (adding/removing) of segments      
    #Console output
    number_segments = len(df_segments_automatic)
    number_roads = df_segments_automatic['road_id'].nunique()
    
    print()
    #Singular or Plural in console output depending on number of roads
    if number_segments == 1:
        print(str(number_segments) + ' BSSD-segment has been found in ' + str(number_roads) + ' road\n')
    elif (number_segments > 1) & (number_roads == 1):
        print(str(number_segments) + ' BSSD-segments have been found in ' + str(number_roads) + ' road\n')
    else:
        print(str(number_segments) + ' BSSD-segments have been found in ' + str(number_roads) + ' roads\n')
    print('Do you want to edit the found segments manually? [y/n]\n')
    
    while True:
        input_manually_add_segments = input('Input: ')
        print()
        
        #Manual editing of segments is desired
        if input_manually_add_segments == 'y' or input_manually_add_segments=='Y' or input_manually_add_segments == 'yes' or input_manually_add_segments == 'Yes':
            
            #Call function to edit segments manually
            df_segments = A_4_manually_edit_segments(df_segments_automatic, OpenDRIVE_object)
            
            break
        
        #No manual editing of segments desired
        elif input_manually_add_segments == 'n' or input_manually_add_segments=='N' or input_manually_add_segments == 'no' or input_manually_add_segments == 'No':
            #Create segments based only on automatic extraction of segments
            df_segments = df_segments_automatic
            break
        #No valid input
        else:
            console.print('[bold red]"' + input_manually_add_segments + '" is no valid input. Please enter "y" or "n".[/bold red]')
            continue
         
    
    #MODIFY XML-TREE
    
    print('Creating <segment> elements...\n')
    created_segment_elements = 0
    
    #Iteration through all <road>-elements of imported xodr-file to create <segment>-element in every road which contains at least one drivable lane
    for road_element in tqdm(OpenDRIVE_element.findall('road')):
        
        #id of current <road>-element
        road_id = int(road_element.get('id'))
        
        #Check if current road includes at least one drivable lane
        if road_element.find('lanes').find('userData') != None:
                
            #Access <userData>-element with BSSD-segments (there might be other <userData>-elements existing)
            user_data_element = access_BSSD_user_data_element(road_element)
            
            #Get only part of df_segments for current road to create <segment>-elements
            df_segments_current_road = df_segments[df_segments['road_id']==road_id]
            df_segments_current_road = df_segments_current_road.reset_index(drop=True)

            
            #Create <segment>-elements for every s-coordinate in df_segments_current_road
            for index, segment in enumerate(df_segments_current_road.loc[:, 'segment_s_start']):
                
                
                #Check if current segment has a defined end-s-coordinate 
                #--> Is set when there is an area in a road where no segment is defined (BSSD definition gap)
                #If no end-s-coordinate is defined, only the attribute "segment_s_start" is set 
                if pd.isnull(df_segments_current_road.loc[index, 'segment_s_end'])==True:
                    #Numbers are stored in xodr according to IEEE 754 (--> 17 significant decimal digits)
                    ET.SubElement(user_data_element, 'segment', attrib={'sStart': "{:.16e}".format(segment)})
                    created_segment_elements = created_segment_elements + 1
               
                #If an end-s-coordinate is defined, both attributes "segment_s_start" and "s_end" are set 
                else:
                    #Numbers are stored in xodr according to IEEE 754 (--> 17 significant decimal digits)
                    ET.SubElement(user_data_element, 'segment', attrib={'sStart': "{:.16e}".format(segment), 
                                                                        'sEnd': "{:.16e}".format(df_segments_current_road.loc[index, 
                                                                                                                               'segment_s_end'])})
                    created_segment_elements = created_segment_elements + 1
                
                
    print()

    #User output
    if created_segment_elements  == 1:
        print('Created ' + str(created_segment_elements) + ' <segment> element')
    else:
        print('Created ' + str(created_segment_elements) + ' <segment> elements')
    
    return df_segments, df_speed_limits, OpenDRIVE_element