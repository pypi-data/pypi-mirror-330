import pandas as pd
from tqdm import tqdm
import bisect
from rich.console import Console
console = Console(highlight=False)

def A_3_4_segments_by_static_signals(df_lane_data_drivable_lanes, df_segments_automatic, OpenDRIVE_object):
    """
    This function extracts BSSD-segments (<segment>-elements) automatically based on rule 4:
        If there is a traffic sign, which affects a BSSD behavioral attribute, a new segment is defined
        
    --> Traffic signs are represented by:
        - <signal>-elements, which are static (attribute dynamic="no")
        - <signalReference>-elements which are linked to a static <signal>-element
        
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
        DataFrame which contains the automatically extracted segments based on rule 4. For every segment a start-s-coordinate is given. 
        If the segments ends before the next segment in the road or before the end of the road a end-s-coordinate is given.
    file_contains_dynamic_signals: Boolean
        Variable to store whether OpenDRIVE-file contains a dynamic signal (e.g. traffic light etc.).
        Is set to "True" when a dynamic signal is in the OpenDRIVE-file.
        If no dynamic signal is included in OpenDRIVE-file, rule 5 (segmenty_by_dynamic_signals.py) doesn't need to be executed
    """
    
    #Import inside function necessary as otherwise a circular import would result
    from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_extract_segments_automatically import paste_segment
    
    print('4. Extracting segments by traffic signs...\n')
    
    
    #List contains all traffic signs of StVO ("Verkehrszeichen") that affect a BSSD behavioral attribute
    #A traffic sign is represented by a number which is defined in the StVO
    #(see e.g. https://de.wikipedia.org/wiki/Bildtafel_der_Verkehrszeichen_in_der_Bundesrepublik_Deutschland_von_2013_bis_2017)
    
    #First number is the StVO-main-number
    #Second number is the StVO-subnumber
    #e.g. speed limits have the main number 274, the subnumber (e.g. 50) specifies the speed limit (e.g. 50 km/h)
    #If only certain subtypes of the traffic sign affect BSSD they are specified in the second number
    #If all subtypes of the traffic sign affect BSSD, it is set to "None"
    list_StVO_BSSD = [["201", None],
                      ["205", None],
                      ["206", None],
                      ["208", None],
                      ["215", None],
                      ["220", None],
                      ["222", None],
                      ["223", None],
                      ["237", None],
                      ["238", None],
                      ["239", None],
                      ["240", None],
                      ["241", None],
                      ["242", None],
                      ["244", None],
                      ["245", None],
                      ["250", None],
                      ["251", None],
                      ["257", "55"],
                      ["260", None],
                      ["262", None],
                      ["263", None],
                      ["264", None],
                      ["265", None],
                      ["267", None],
                      ["268", None],
                      ["269", None],
                      ["270.1", None],
                      ["270.2", None],
                      ["274", None],
                      ["274.1", None],
                      ["274.2", None],
                      ["276", None],
                      ["277.1", None],
                      ["278", None],
                      ["279", None],
                      ["280", None],
                      ["281", None],
                      ["281.1", None],
                      ["282", None],
                      ["293", None],
                      ["294", None],
                      ["295", None],
                      ["296", None],
                      ["298", None],
                      ["301", None],
                      ["306", None],
                      ["308", None],
                      ["310", None],
                      ["311", None],
                      ["325.1", None],
                      ["325.2", None],
                      ["330.1", None],
                      ["330.2", None],
                      ["331.1", None],
                      ["331.2", None],
                      ["340", None],
                      ["341", None],
                      ["342", None],
                      ["720", None]]
    
    #Static <signal>-elements can contain an attribute "country", which contains the country code of the signal (ISO 3166-1, alpha-2 codes)
    #This attribute is used to get only signals which represent traffic signs from Germany (country code = "DE")
    #To allow also other country-codes for Germany, this list contains all possible values of the "country"-attribute, which are according
    #to ISO 3166-1 or which aren't according to ISO 3166-1, but imply that Germany is meant
    country_attribute_accept_germany = ['DE', 'De', 'de', 'DEU', 'Deu', 'deu', 'GER', 'Ger', 'ger', 'Germany', 'germany', 'Deutschland',
                                        'deutschland']

    #Variable for storing the number of segments before executing this function to know how many segments have been added based on this function
    number_segments_before = len(df_segments_automatic)

    #Execute function for analyzing attribute "country" of the static <signal>-elements in the imported OpenDRIVE-file.
    #Depending on that, a user input is required or not
    number_signals_no_country, number_signals_germany, number_signals_other_country = analyze_signal_elements(df_lane_data_drivable_lanes,
                                                                                                              country_attribute_accept_germany,
                                                                                                              OpenDRIVE_object)

    #If there exist static <signal>-elements with no defined "country"-attribute, the user is asked whether these <signal>-elements
    #should be considered as static <signal>-elements which represent traffic signs from Germany
    if (number_signals_no_country)>0:
        print('Should static <signal>-elements which have no defined "country"-attribute be considered like their country-attribute is representing Germany? [y/n]')
        print('--> Their relevance for BSSD will be checked anyway\n')
        while True:
            input_empty_country_attribute = input('Input: ')
            print()
            
            #If answer is "yes", <signal>-elements with no defined "country"-attributes are considered as <signal>-elements which represent
            #traffic signs from Germany
            if input_empty_country_attribute == 'y' or input_empty_country_attribute=='Y' or input_empty_country_attribute == 'yes' or input_empty_country_attribute == 'Yes':
                
                not_consider_empty_country_attribute = True
                
                break
            
            #If answer is "no", <signal>-elements with no defined "country"-attributes are not considered as <signal>-elements which
            #represent traffic signs from Germany
            elif input_empty_country_attribute == 'n' or input_empty_country_attribute=='N' or input_empty_country_attribute == 'no' or input_empty_country_attribute == 'No':
                not_consider_empty_country_attribute = False
                break
            
            #No valid input
            else:
                print('[bold red]"' + input_empty_country_attribute + '" is no valid input. Please enter "y" or "n".\n[bold red]')
                continue
            
    #Consider "country"-attribute if there are no static <signal>-elements which have no defined "country"-attribute
    else:
        not_consider_empty_country_attribute = False
        
    
    #1. STATIC <SIGNAL>-ELEMENTS
    #Create segments based on traffic signs in static <signal>-elements
    #-------------------------------------------------------------------------------------
    
    print('4.1 Static <signal>-elements...\n')
    
    #Create list to store the id's of all static <signal>-elements with relevance for BSSD (id of <signal> is unique in whole file)
    #--> Needed for creating segments based on <signalReference>-elements
    list_static_signals_BSSD_relevant = []
        
    #Create variable to store whether OpenDRIVE-file contains a dynamic signal (e.g. traffic light etc.)
    #If no dynamic signal is included in OpenDRIVE-file, rule 5 (segmenty_by_dynamic_signals.py) doesn't need to be executed
    file_contains_dynamic_signals = False
    
    #Iteration through all roads with drivable lanes to automatically extract segments by traffic signs
    for road_id in tqdm(df_lane_data_drivable_lanes['road_id'].unique()):
        
        #Convert road_id to int as pd.unique() returns float values
        road_id = int(road_id)
        
        #Road object of current road
        road_object = OpenDRIVE_object.getRoad(road_id)
        
        #Iterate through all <signal>-elements of current road to extract segments
        for signal_object in road_object.signals:
            
            #Skip all <signals> with attribute dynamic="yes" as they represent traffic lights etc. (no traffic sign)
            #--> These elements are handled in rule 5 (segmenty_by_dynamic_signals.py)
            if signal_object.dynamic=='yes':
                file_contains_dynamic_signals = True
                continue
            
            #Access country code of signal (ISO 3166-1, alpha-2 codes) to get only signals which represent traffic signs
            #from Germany (country code = "DE")
            country_code_signal = signal_object.country
            
            #Check country-code of <signal>-elements depending on user input
            #If <signal>-elements with no defined "country"-attribute should be considered as they are not from Germany,
            #skip all <signal>-elements with a "country"-attribute not representing Germany (see country_attribute_accept_germany)
            if not_consider_empty_country_attribute==False:
                
                #Skip all <signal>-elements that don't represent a traffic sign from Germany (see country_attribute_accept_germany)
                if (country_code_signal in country_attribute_accept_germany)==False:
                    continue
            
            #If <signal>-elements with no defined "country"-attribute should be considered as they are from Germany,
            #skip all <signal>-elements with a "country"-attribute which is not empty and 
            #which does not represent Germany (see country_attribute_accept_germany)
            else:
                
                #skip all <signal>-elements with a "country"-attribute which is not empty ("None") and 
                #which does not represent Germany (see country_attribute_accept_germany)
                if ((country_code_signal in country_attribute_accept_germany)==False) and (country_code_signal!='None') \
                    and (len(country_code_signal)>0):
                    continue
            
            #Get type and subtype attributes of <signal>-element to check if the traffic signs has relevance for BSSD
            signal_type = signal_object.type
            signal_subtype = signal_object.subtype
            
            #Add segment only if signal has relevance for BSSD (see list "list_StVO_BSSD")
            if ([signal_type, None] in list_StVO_BSSD) or ([signal_type, signal_subtype] in list_StVO_BSSD):
                  
                #Append id of current <signal>-element to list of <signals> with BSSD-relevance
                list_static_signals_BSSD_relevant.append(signal_object.id)
            
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
    
    #Get number of extracted segments based on static <signal>-elements
    number_of_extracted_segments = len(df_segments_automatic)-number_segments_before
    
    print()
    
    #User output
    if number_of_extracted_segments==1:
        print('Extracted ' + str(number_of_extracted_segments) + ' segment\n')
    else:
        print('Extracted ' + str(number_of_extracted_segments) + ' segments\n')
    
    #2. STATIC <SIGNALREFERENCE>-ELEMENTS
    #Create segments based on traffic signs linked in static <signalReference>-elements
    #-------------------------------------------------------------------------------------
    
    #Variable for storing the number of segments before executing this function to know how many segments have been added based on this function
    number_segments_before = len(df_segments_automatic)
    
    #Create segments based on <signalReference>-elements linked to a static <signal>-element
    print('4.2 Static <signalReference>-elements...\n')
    
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
            
            #Check if <signal>-element linked in current <signalReference>-element has relevance for BSSD (list_static_signals_BSSD_relevant)
            #Skip <signalReference>-element if it is linked to a <signal>-element with no BSSD-relevance
            if (id_signalReference in list_static_signals_BSSD_relevant)==False:
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
        
        
    return df_segments_automatic, file_contains_dynamic_signals
        
        
        
def check_signal_s_coordinate(s_signal, road_id, df_segments_automatic, road_object):
    """
    This function checks for the s-coordinate where a signal is defined (variable "s_signal"):
        a. If a segment has already been defined for this s-coordinate
        b. If the s-coordinate of the signal is in a BSSD definition gap (no drivable lanes existing at this s-coordinate)
        c. If the s-coordinate of the signal is higher than the length of the road
        d. If the s-coordinate of the signal is lower than zero (physically not possible)
        
    --> If one of the four conditions above is fulfilled, the function returns False --> No segment definition at s-coordinate of signal
    --> If no of the four conditions above is fulfilled, the function returns True --> A segment can be defined at s-coordinate of signal
    """
    
    #Get df_segments_automatic only for current road
    df_segments_automatic_current_road = df_segments_automatic[df_segments_automatic['road_id']==road_id]
    df_segments_automatic_current_road = df_segments_automatic_current_road.reset_index(drop=True)
    
    #Get all extracted segments in the current road
    segments_current_road = pd.unique(df_segments_automatic_current_road['segment_s_start'])
    segments_current_road = segments_current_road.tolist()
    segments_current_road.sort()
    
    #Check if a segment has already been defined for the s-coordinate of the signal
    #If yes, the signal can be skipped
    if (s_signal in segments_current_road) == True:
        return False
    
    #Check if currend road has a BSSD definition gap at the beginning (= first segment does start at s>0)
    #If yes, it has to be checked whether the signal is in this first definition gap
    if df_segments_automatic_current_road.loc[0, 'segment_s_start']>0:
        
        #Skip signal if it is defined for a s-coordinate that is in a BSSD definition gap
        if s_signal < df_segments_automatic_current_road.loc[0, 'segment_s_start']:
            return False
    
    #Get index of segment, which has the highest s_start coordinate which is below the s-coordinate of the signal
    index_segment_below = bisect.bisect_right(df_segments_automatic_current_road.loc[:, 'segment_s_start'], s_signal) - 1
    
    #Check if segment with highest s_start coordinate which is below the s-coordinate of the signal, has a defined s_end
    #If yes, it has to be checked whether the signal is defined in a BSSD definition gap
    if pd.isnull(df_segments_automatic_current_road.loc[index_segment_below, 'segment_s_end'])==False:
        
        #Skip signal if it is defined for a s-coordinate that is in a BSSD definition gap
        if s_signal >= df_segments_automatic_current_road.loc[index_segment_below, 'segment_s_end']:
            return False
        
    #Check if s-coordinate of signal is higher than length of the road (wrongly defined)
    if s_signal > road_object.length:
        return False
    
    #Check if s-coordinate of signal is lower than zero (physically not possible)
    if s_signal < 0:
        return False
        
    return True

def analyze_signal_elements(df_lane_data_drivable_lanes, country_attribute_accept_germany, OpenDRIVE_object):
    """
    This function analyzes the attribute "country" of the static <signal>-elements in the imported OpenDRIVE-file.
    It counts the number of static <signal>-elements that:
        - have no/an empty "country"-attribute --> variable number_signals_no_country
        - have a "country"-attribute representing Germany (see list country_attribute_accept_germany) --> variable number_signals_germany
        - have a "country"-attribute representing another country than Germany --> variable number_signals_other_country
        
    If there exist static <signal>-elements with no defined "country"-attribute, the user is asked whether these <signal>-elements
    should be considered as static <signal>-elements which represent traffic signs from Germany

    """
    
    #Variables for counting the number of static <signal>-elements in the three categories
    number_signals_no_country = 0
    number_signals_germany = 0
    number_signals_other_country = 0
    
    #Iteration through all roads with drivable lanes to analyze country-attribute of static signal-elements
    for road_id in df_lane_data_drivable_lanes['road_id'].unique():
        
        #Convert road_id to int as pd.unique() returns float values
        road_id = int(road_id)
        
        #Road object of current road
        road_object = OpenDRIVE_object.getRoad(road_id)
        
        #Iterate through all <signal>-elements of current road to extract segments
        for signal_object in road_object.signals:
            
            #Skip all <signals> with attribute dynamic="yes" as they represent traffic lights etc. (no traffic sign)
            #--> These elements are handled in rule 5 (segmenty_by_dynamic_signals.py)
            if signal_object.dynamic=='yes':
                continue
            
            #Access country code of signal (ISO 3166-1, alpha-2 codes) for user output
            country_code_signal = signal_object.country
            
            #Check for signals with country-code representing Germany
            if country_code_signal in country_attribute_accept_germany:
                   number_signals_germany = number_signals_germany + 1
                   
            #Check for signals which have a defined country-code, which is not representing Germany
            elif (country_code_signal!='None') and (len(country_code_signal)>0):
                number_signals_other_country = number_signals_other_country + 1
            
            #Signals which have no country-code (None or empty string)
            else:
                number_signals_no_country = number_signals_no_country + 1
                

    #Console output with singular/plural depending on number of found elements
    if number_signals_no_country  == 1:
        string_number_signals_no_country = str(number_signals_no_country) + ' static <signal>-element, which has no defined "country"-attribute\n'
    else:
        string_number_signals_no_country = str(number_signals_no_country) +  ' static <signal>-elements, which have no defined "country"-attribute\n'
    
    if number_signals_germany  == 1:
        string_number_signals_germany = str(number_signals_germany) + ' static <signal>-element from Germany\n'
    else:
        string_number_signals_germany = str(number_signals_germany) +  ' static <signal>-elements from Germany\n'
    
    if number_signals_other_country  == 1:
        string_number_signals_other_country = str(number_signals_other_country) + ' static <signal>-element from another country than Germany\n'
    else:
        string_number_signals_other_country = str(number_signals_other_country) + ' static <signal>-elements from another country than Germany\n'
        
    
    #Check if imported file contains any signals with an empty or not existing country code 
    #If yes, make a console output to ask if country attribute should be considered
    if number_signals_no_country > 0:
        print('Imported OpenDRIVE-file contains...\n')
        print('...' + string_number_signals_no_country)
        print('...' + string_number_signals_germany)
        print('...' + string_number_signals_other_country)
        
    return number_signals_no_country, number_signals_germany, number_signals_other_country
            
        