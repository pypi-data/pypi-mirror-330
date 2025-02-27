from tqdm import tqdm

from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_4_segments_by_static_signals import check_signal_s_coordinate

def A_3_5_segments_by_dynamic_signals(df_lane_data_drivable_lanes, df_segments_automatic, OpenDRIVE_object):
    """
    This function extracts BSSD-segments (<segment>-elements) automatically based on rule 5:
        If there is a traffic light or another dynamic signal, a new segment is defined
        
    --> Traffic lights and other dynamic signals are represented by <signal>-elements, which are dynamic (attribute dynamic="yes")
        
    Parameters
    ----------
    df_lane_data_drivable_lanes : DataFrame
        DataFrame which contains information about all lanes that represent a drivable OpenDRIVE-lane 
    df_segments_automatic : DataFrame
        DataFrame which contains the automatically extracted segments (result of execution of rule 1, rule 2 and rule 3)
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file --> Used for parsing the OpenDRIVE-Map

    Returns
    -------
    df_segments_automatic : DataFrame
        DataFrame which contains the automatically extracted segments based on rule 5. For every segment a start-s-coordinate is given. 
        If the segments ends before the next segment in the road or before the end of the road a end-s-coordinate is given.

    """
    
    #Import inside function necessary as otherwise a circular import would result
    from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_extract_segments_automatically import paste_segment
    
    print('5. Extracting segments by traffic lights and other dynamic signals...\n')
    
    #Variable for storing the number of segments before executing this function to know how many segments have been added based on dynamic
    #<signal>-elements
    number_segments_before = len(df_segments_automatic)
    
    #1. DYNAMIC <SIGNAL>-ELEMENTS
    #Create segments based on traffic lights and other dynamic signals in dynamic <signal>-elements
    #-------------------------------------------------------------------------------------
    
    print('5.1 Dynamic <signal>-elements...\n')
    
    #Create list to store the id of all dynamic <signal>-elements (id of <signal> is unique in whole file)
    #--> Needed for creating segments based on <signalReference>-elements
    list_dynamic_signals = []
   
    #Iteration through all roads with drivable lanes to automatically extract segments by traffic lights and other dynamic signals
    for road_id in tqdm(df_lane_data_drivable_lanes['road_id'].unique()):
        
        #Convert road_id to int as pd.unique() returns float values
        road_id = int(road_id)
        
        #Road object of current road
        road_object = OpenDRIVE_object.getRoad(road_id)
        
        #Iterate through all <signal>-elements of current road to extract segments
        for signal_object in road_object.signals:
            
            #Skip all <signals> with attribute dynamic="no" as they represent traffic signs
            #--> These elements were already handled in rule 4 (segmenty_by_static_signals.py)
            if signal_object.dynamic=='no':
                continue
            
            #Check if dynamic-attribute is set to "yes" --> Imported file may not fulfill the offical OpenDRIVE-specifications
            #May have other values than "yes" or "no" for attribute "dynamic"
            if signal_object.dynamic=='yes':
                
                #Append id of current <signal>-element to list of dynamic signal --> Needed for <signalReference>-elements
                list_dynamic_signals.append(signal_object.id)
                
                #Get s-coordinate of signal to check whether a segment has already been defined at this s-coordinate and to check if a drivable
                #lane exists at this s-coordinate
                s_signal = round(signal_object.s, 2)
                
                #Skip signal if a segment has already been defined at s-coordinate of signal or if s-coordinate of signal is defined in
                #a BSSD definition gap (Conditions are checked by function "check_signal_s_coordinate")
                if check_signal_s_coordinate(s_signal, road_id, df_segments_automatic, road_object)==False:
                    continue
                
                #Create segment at s-coordinate of signal
                df_segments_automatic = paste_segment(df_segments_automatic, road_id, s_signal, None)
        
    #Sort in added lanes
    df_segments_automatic = df_segments_automatic.sort_values(['road_id', 'segment_s_start'])
    df_segments_automatic = df_segments_automatic.reset_index(drop=True)
    
    #Get number of extracted segments based on dynamic <signal>-elements
    number_of_extracted_segments = len(df_segments_automatic)-number_segments_before
    
    print()
    #User output
    if number_of_extracted_segments==1:
        print('Extracted ' + str(number_of_extracted_segments) + ' segment\n')
    else:
        print('Extracted ' + str(number_of_extracted_segments) + ' segments\n')
            
    
    #2. DYNAMIC <SIGNALREFERENCE>-ELEMENTS
    #Create segments based on traffic lights and other dynamic signals linked in dynamic <signalReference>-elements
    #-------------------------------------------------------------------------------------
    
    #Variable for storing the number of segments before executing this function to know how many segments have been added based on dynamic
    #<signalReference>-elements
    number_segments_before = len(df_segments_automatic)
    
    #Create segments based on  <signalReference>-elements linked to a dynamic <signal>-element
    print('5.2 Dynamic <signalReference>-elements...\n')
    
    #Iteration through all roads with drivable lanes to automatically extract segments by traffic signs in <signalReference>-elements
    for road_id in tqdm(df_lane_data_drivable_lanes['road_id'].unique()):
        
        #Convert road_id to int as pd.unique() returns float values
        road_id = int(road_id)
        
        #Road object of current road
        road_object = OpenDRIVE_object.getRoad(road_id)
        
        #Iterate through all <signaReference>-elements of current road to extract segments
        for signalReference_object in road_object.signalReference:
            
            #Get id of <signal> which is linked in current <signalReference>-element
            id_signalReference = signalReference_object.id
            
            #Check if <signal>-element linked in current <signalReference>-element is a dynamic <signal>-element (list_dynamic_signals)
            #Skip <signalReference>-element if it is linked to a <signal>-element which is not dynamic
            if (id_signalReference in list_dynamic_signals)==False:
                continue
            
            #Get s-coordinate of <signalReference>-element --> s-Position where rule of linked <signal>-element takes effect
            s_signalReference = signalReference_object.s
            
            #Check s-coordinate of <signalReference> to check whether a segment has already been defined at this s-coordinate and to check if
            #a drivable lane exists at this s-coordinate
            if check_signal_s_coordinate(s_signalReference, road_id, df_segments_automatic, road_object)==False:
                continue
            
            #Create segment at s-coordinate of <signalReference>-element
            df_segments_automatic = paste_segment(df_segments_automatic, road_id, s_signalReference, None) 
                
                
    
    #Sort in added lanes
    df_segments_automatic = df_segments_automatic.sort_values(['road_id', 'segment_s_start'])
    df_segments_automatic = df_segments_automatic.reset_index(drop=True)
    
    #Convert values in column "road_id" to int 
    df_segments_automatic['road_id']=df_segments_automatic['road_id'].convert_dtypes()
    
    #Get number of extracted segments based on static <signalReference>-elements
    number_of_extracted_segments = len(df_segments_automatic)-number_segments_before
    
    print()
    
    #User output
    if number_of_extracted_segments==1:
        print('Extracted ' + str(number_of_extracted_segments) + ' segment\n')
    else:
        print('Extracted ' + str(number_of_extracted_segments) + ' segments\n')
    
    
    return df_segments_automatic
        