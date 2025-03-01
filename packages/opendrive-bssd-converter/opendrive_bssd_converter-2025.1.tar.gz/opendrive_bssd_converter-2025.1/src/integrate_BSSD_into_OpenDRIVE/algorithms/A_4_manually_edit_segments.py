import pandas as pd
pd.options.mode.chained_assignment = None
from rich.console import Console
from rich import print
from rich.markdown import Markdown

from integrate_BSSD_into_OpenDRIVE.utility.print_table import print_table

console = Console(highlight=False)

def A_4_manually_edit_segments(df_segments_automatic, OpenDRIVE_object):
    """
    This function allows the user to manually edit the automatically found segments (see A_3_extract_segments_automatically.py).
    On the one hand additional segments can be created. On the other created segments can be removed if the segmentation by the preceding algorithm
    results in errors (may be the case when creating segments based on <signal>-elements).
    
    A segment is added/removed by typing in the s-coordinate where the segment should start/starts.


    Parameters
    ----------
    df_segments_automatic : DataFrame
        DataFrame which contains the automatically extracted segments from "A_3_extract_segments_automatically.py".
        For every segment a start-s-coordinate is given. If the segments ends before the next segment in the road 
        or before the end of the road a end-s-coordinate is given.
    OpenDRIVE_object : elements.opendrive.OpenDRIVE
        Object representing the root-<OpenDRIVE>-element of xodr-file

    Returns
    -------
    df_segments : DataFrame
        DataFrame which contains the manually edited segments. 
        For every segment a start-s-coordinate is given. If the segments ends before the next segment in the road 
        or before the end of the road a end-s-coordinate is given.
        Based on this DataFrame <segment>-elements are created.

    """
    
    
    console.print('Starting routine for manually editing BSSD-segments...\n')
    console.print('This routine can be aborted by typing "break" every time a console input is necessary. The changes until the abortion will be stored.\n')
    
    #Creating copy of df_segments_automatic --> df_segments includes the manually edited segments
    df_segments = df_segments_automatic
    
    #Iterate through all roads where a segment automatically has been created (--> Every road that contains at least one drivable lane)
    for road_id in df_segments_automatic['road_id'].unique():
        
        #Convert road_id to int as pd.unique() returns float values
        road_id = int(road_id)
        
        #Road object of current road
        road_object = OpenDRIVE_object.getRoad(road_id)
        
        #Get length of current road (necessary for validating inputs for new segments)
        road_length = road_object.length
        
        #Provide additional information if road is located inside a junction
        #Case: Road outside a junction
        if  road_object.junction == None:
            console.print('Road with id ' + str(road_id) + '\n', style='bold red')
        
        #Case: Road inside a junction
        else:
            console.print('Road with id ' + str(road_id) + ' (part of junction ' + str(road_object.junction.id) + ')\n', style='bold red')
        
        #1. Manually add Segments
        #--------------------------------------------------------------------------------
        console.print('1. Add segments\n ', style='bold yellow')
        
        #Variable for controlling the following while-True-loop
        continue_loop = True
        
        while True:

            #Break loop based on variable "continue_loop"
            if continue_loop == False:
                break
        
            #Access all created segments in the current road
            df_created_segments_current_road = df_segments[df_segments['road_id']==road_id]
            #Reset index
            df_created_segments_current_road = df_created_segments_current_road.reset_index(drop=True)
            
            #Create DataFrame with renamed columns for better user output
            df_created_segments_current_road_user_output = df_created_segments_current_road.rename(columns={'segment_s_start': 's_start', 'segment_s_end': 's_end'})
            df_created_segments_current_road_user_output['s_start'] = df_created_segments_current_road_user_output['s_start'].round(2)
            df_created_segments_current_road_user_output['s_end'] = df_created_segments_current_road_user_output['s_end'].round(2)
            
            #Change nan-values in attribute s_end for user output to "-"
            for index, s_end_element in enumerate(df_created_segments_current_road_user_output.loc[:, 's_end']):
                
                #Change nan to "-"
                if pd.isnull(s_end_element)==True:
                    df_created_segments_current_road_user_output.loc[index, 's_end'] = "-"
            
            #User output
            console.print('The following BSSD-segments will be created in road ' + str(road_id) + ' (length = ' + str(round(road_object.length, 2)) + '):\n ')

            #Display table in console with function "print_table" (Uses package rich)
            print_table(df_created_segments_current_road_user_output[['s_start', 's_end']], False, '')
            
            console.print('You have the following options:\nType in...')
            print(Markdown('* One s-coordinate for adding a segment (valid until next segment or end of road) at this s-coordinate of the road, e.g. "25.0"'))
            print(Markdown('* "c" to continue with removing segments in the current road'))
            print(Markdown('* "break" to abort editing segments. All changes until now will be stored'))
            
                    
            #Execute loop until valid user input (one valid s-coordinate) is given
            while True:
                
                #Get user input
                print()
                input_add_segments = input('Input: ')
                console.print()
                
                #Analyze user input
                
                #Abort execution when input is 'break' and return DataFrame
                if input_add_segments == 'break':

                    return df_segments
                
                else:
                    
                    #Input of a s-coordinate given (if input is valid)    
                    if input_add_segments != 'c':
                        
                        #Check validity of input and get s-coordinate of input
                        return_value, input_s_start = validate_input_add(input_add_segments, road_length, df_created_segments_current_road)
                        if return_value==False:
                            continue
                        
                        #Iterate through created segments in current road to paste new segment in correct place 
                        for index, current_s_start in enumerate(df_created_segments_current_road.loc[:, 'segment_s_start']):
                            
                            #Check if a succeeding segment in current road exists
                            if index < (len(df_created_segments_current_road)-1):
                                
                                #s_start of succeeding segment
                                s_start_next_segment = df_created_segments_current_road.loc[index+1, 'segment_s_start']
                                
                                #If input value of s_start is greater than the current s_start-value and lower than s_start of suceeding 
                                #segment, the new segment has to be pasted after the current segment
                                if (input_s_start > current_s_start) and (input_s_start < s_start_next_segment):
                                    
                                    #Get index of current segment in df_segments (for-loop iterates through df_created_segments_current_road)
                                    index_df_segments = df_segments[(df_segments['road_id']==road_id) & \
                                                                    (df_segments['segment_s_start']==current_s_start)].index.values.astype(int)[0]
                                    
                                    #Call function to paste new segment after current segment in df_segments
                                    df_segments = paste_segment(df_segments, index_df_segments, road_id, input_s_start)
                                     
                                    break
                                
                            
                            #No succeeding segment in current road existing
                            #--> Segment is pasted after current segment
                            else:
                                
                                #Get index of current segment in df_segments (for-loop iterates through df_created_segments_current_road)
                                index_df_segments = df_segments[(df_segments['road_id']==road_id) & \
                                                                (df_segments['segment_s_start']==current_s_start)].index.values.astype(int)[0]
                                
                                #Call function to paste new segment after current segment
                                df_segments = paste_segment(df_segments, index_df_segments, road_id, input_s_start)
                                break
                            
                        #Break inner while-True-loop                                
                        break
                    
                    #User input "c" to continue with next road
                    else:
                        #Break outer while-True-loop
                        continue_loop = False
                        #Break inner while-True-loop
                        break
        
        
        df_segments = df_segments.reset_index(drop=True)
        
        #2. Remove segments
        #-----------------------------------------------------------------------------------------
        console.print('2. Remove segments\n ', style='bold yellow')
        
        #Variable for controlling the following while-True-loop
        continue_loop = True
        
        while True:

            #Break loop based on variable "continue_loop"
            if continue_loop == False:
                break
        
            #Access all created segments in the current road
            df_created_segments_current_road = df_segments[df_segments['road_id']==road_id]
            
            #No removing of segment possible if only one segment is defined in current road
            if len(df_created_segments_current_road)==1:
                print('No removing of additional segments possible as road contains only one segment.\n')
                break
                
            
            #Create DataFrame with renamed columns for better user output
            df_created_segments_current_road_user_output = df_created_segments_current_road.rename(columns={'segment_s_start': 's_start', 'segment_s_end': 's_end'})
            df_created_segments_current_road_user_output = df_created_segments_current_road_user_output.reset_index(drop=True)
            df_created_segments_current_road_user_output['s_start'] = df_created_segments_current_road_user_output['s_start'].round(2)
            df_created_segments_current_road_user_output['s_end'] = df_created_segments_current_road_user_output['s_end'].round(2)
            
            #Change nan-values in attribute s_end for user output to "-"
            for index, s_end_element in enumerate(df_created_segments_current_road_user_output.loc[:, 's_end']):
                
                #Change nan to "-"
                if pd.isnull(s_end_element)==True:
                    df_created_segments_current_road_user_output.loc[index, 's_end'] = "-"
            
            #User output
            console.print('The following BSSD-segments will be created in road ' + str(road_id) + ' (length = ' + str(round(road_object.length, 2)) + '):\n ')

            #Display table in console with function "print_table" (Uses package rich)
            print_table(df_created_segments_current_road_user_output[['s_start', 's_end']], False, '')
            
            console.print('You have the following options:\nType in...')
            print(Markdown('* One s-coordinate of a segment for removing this segment'))
            print(Markdown('* "c" to continue with adding segments in the next road'))
            print(Markdown('* "break" to abort editing segments. All changes until now will be stored'))
            
                    
            #Execute loop until valid user input (one valid s-coordinate) is given
            while True:
                
                #Get user input
                print()
                input_remove_segments = input('Input: ')
                console.print()
                
                #Analyze user input
                
                #Abort execution when input is 'break' and return DataFrame
                if input_remove_segments == 'break':

                    return df_segments
                
                else:
                    
                    #Input of a s-coordinate given (if input is valid)    
                    if input_remove_segments != 'c':
                                               
                        #Check validity of input and get s-coordinate of input
                        return_value, input_s_start = validate_input_remove(input_remove_segments, df_created_segments_current_road)
                        if return_value==False:
                            continue
                        
                        
                        #Iterate through created segments in current road to find segment to be removed
                        for index_loop, current_s_start in enumerate(df_created_segments_current_road.loc[:, 'segment_s_start']):
                            
                            #Check if current segment is the segment to be removed
                            if round(current_s_start, 2)==round(input_s_start, 2):
                            
                                
                                #Get index of segment to be removed in df_segments
                                index_df_segments = df_created_segments_current_road.index[index_loop]
                            
                                #Check if segment to be removed has a defined s_end-coordinate
                                current_s_end = df_created_segments_current_road.loc[index_df_segments, 'segment_s_end']
                                
                                #Case 1: Segment to be removed has a defined s_end coordinate
                                if pd.isnull(current_s_end)==False:
                                    
                                    #Transfer s_end of segment to be removed to preceding segment (if existing)
                                    if index_loop >0:
                                        
                                        #Check if preceding segment has no defined s_end-coordinate
                                        #Only then s_end can be transferred to the preceding segment
                                        if pd.isnull(df_segments.loc[index_df_segments-1, 'segment_s_end'])==True:
                                        
                                            #Set s_end of preceding segment to value of s_end of segment to be removed
                                            df_segments.loc[index_df_segments-1, 'segment_s_end']=current_s_end
                                    
                                    
 
                                #Remove segment from df_segments
                                df_segments = df_segments.drop(index_df_segments)
                                df_segments = df_segments.reset_index(drop=True)
                                console.print('Removed segment with s_start = ' + str(input_s_start) + '\n')
                                break

                            
                        #Break inner while-True-loop                                
                        break
                    
                    #User input "c" to continue with next road
                    else:
                        #Break outer while-True-loop
                        continue_loop = False
                        #Break inner while-True-loop
                        break
        
        
    
    return df_segments


def validate_input_add(input_add_segments, road_length, df_created_segments_current_road):
    """
    This function validates the user input in the variable "input_add_segments" (Adding segments). 
    The function returns a boolean depending on whether the input is valid or not.
    Additionaly the function returns the number given in the input as float value (list_number_elements)

    An input is generally valid if only one positive number (= the s-coordinate) is given as input. 
    The number can have a decimal point --> "25" but also "25.0" would be a valid input
    
    Besides this, the s-coordinate in the input has to fulfill the following conditions to be valid
        - It has to be below the length of the current road
        - It has to differ from s-coordinates of existing segments
        - It has to be in an area where drivable lanes are defined (Not drivable areas only exist if a segment has a defined s_end-value)

    """
    
    #Function for creating list with single elements of user input (e.g. comma, numbers) 
    #--> deleting spaces and joining characters belonging to one number together
    #--> Is used as a basis for validating the user input
    list_elements_input = get_elements_input(input_add_segments)
    
    
    #List for analyzing the numbers given in the input
    list_number_elements = []
    
    #Iterate through elements of user input to add all numbers to list_number_elements
    for element in list_elements_input:
        
        #Check for valid input (Just numbers are accepted)
        if (element.isnumeric()==True or isfloat(element) == True):
        
            #Check if element is a number or a float
            # If yes, append it to list_number_elements to analyze the numbers given as input
            if (element.isnumeric()==True or isfloat(element) == True):
                list_number_elements.append(float(element))
            
        else:
            console.print('[bold red]Wrong input format. Only one positive number (with optional decimal point) is accepted.\n[/bold red]')
            return False, list_number_elements
    
    #Analyze the number(s) in the input:
    
    #Check for more than one number 
    if len(list_number_elements)>1:
        console.print("[bold red]Wrong input. More than one number was given as input.\n[/bold red]")
        return False, list_number_elements
    
    #Check for empty list --> No number in input
    if len(list_number_elements)==0:
        console.print("[bold red]Wrong input. No number was given as input.\n[/bold red]")
        return False, list_number_elements
    
    
    #Store input of s-coordinate for start of BSSD-segment
    input_s_start = list_number_elements[0]
    
    #Check for a s_start higher than length of the current road (not possible)
    if round(input_s_start, 2) >= round(road_length, 2):
        console.print('[bold red]Wrong input. s_start (s = ' + str(input_s_start) +  ') is higher or equal to length of current road (s = ' + str(round(road_length, 2)) + ')\n[/bold red]')
        return False, input_s_start
        
    #Iterate through segments of current road to check if s-coordinate of input already exists as s_start or s_end of an existing segment
    for index, current_s_start in enumerate(df_created_segments_current_road.loc[:, 'segment_s_start']):
        
        #Check for identical s_start
        #Round to two digits. Rounding needed to cut off numerical errors for comparison of two float values
        if round(input_s_start, 2) == round(current_s_start, 2):
            console.print('[bold red]Wrong input. A segment with s_start = ' + str(input_s_start) + ' already exists\n[/bold red]' )
            return False, input_s_start
        
        #Check if s_end of current segment is defined
        if df_created_segments_current_road.loc[index, 'segment_s_end']!= None:
            
            #Check for identical s_end
            #Round to two digits. Rounding needed to cut off numerical errors for comparison of two float values
            if round(input_s_start, 2) == round(df_created_segments_current_road.loc[index, 'segment_s_end'], 2):
                console.print('[bold red]Wrong input. There is a segment with s_end = ' + str(input_s_start) + '. No adding of a new segment at this s-coordinate possible\n[/bold red]' )
                return False, input_s_start
        
    #Iterate through segments of current road to check if segment from user input is defined in an area of the road where at least one
    #drivable lane is existing
    for index, current_s_start in enumerate(df_created_segments_current_road.loc[:, 'segment_s_start']):
        
        #Get first segment in current road to check if there are no drivable lanes at the beginning of the road
        if index == 0:
            #Check for a non drivable area of the road at the beginning of the road (--> First segment starts at s > 0)
            if round(current_s_start,2) > 0:
                
                #Check if segment from input is located in non drivable area
                if input_s_start < current_s_start:
                    console.print('[bold red]Wrong input. A segment can not be defined at s_start = ' + str(input_s_start) + ' as no drivable lane exists at this s-coordinate of the road\n[/bold red]')
                    return False, input_s_start
        
        #Check for segments with a defined end to check if new segment is located in an area of the road with no drivable lanes      
        if (pd.isnull(df_created_segments_current_road.loc[index, 'segment_s_end'])==False):
             
            #s_end of current segment
            current_s_end = df_created_segments_current_road.loc[index, 'segment_s_end']
            
            #Check if a succeeding segment is existing
            if index < (len(df_created_segments_current_road)-1):
                
                #s_start of suceeding segment
                next_s_start = df_created_segments_current_road.loc[index+1, 'segment_s_start']
                
                #Check if new segment is defined in between s_end of current segment and s_start of suceeding segment
                #-->In this area no drivable lane is defined --> No segment possible
                if (input_s_start > current_s_end) and (input_s_start < next_s_start):
                    console.print('[bold red]Wrong input. A segment can not be defined at s_start = ' + str(input_s_start) + ' as no drivable lane exists at this s-coordinate of the road\n[/bold red]')
                    return False, input_s_start
            
            #No succeeding segment existing
            else:
                
                #Check if new segment is defined behind s_end of the current segment (last segment of the road)
                #-->In this area no drivable lane is defined --> No segment possible
                if input_s_start > current_s_end:
                    console.print('[bold red]Wrong input. A segment can not be defined at s_start = ' + str(input_s_start) + ' as no drivable lane exists at this s-coordinate of the road\n[/bold red]')
                    return False, input_s_start

        
    #Return True if no exception occured --> Input is valid
    #Return input_s_start, which contains the valid s-coordinate from the user input where a segment should be created
    return True, input_s_start

def validate_input_remove(input_remove_segment, df_created_segments_current_road):
    """
    This function validates the user input in the variable "input_remove_segment" (Removing segments). 
    The function returns a boolean depending on whether the input is valid or not.
    Additionaly the function returns the number given in the input as float value (list_number_elements)

    An input is generally valid if only one positive number (= the s-coordinate) is given as input. 
    The number can have a decimal point --> "25" but also "25.0" would be a valid input
    
    Besides this, the s-coordinate in the input has to be the s-coordinate of an already existing segment.

    """
    
    #Function for creating list with single elements of user input (e.g. comma, numbers) 
    #--> deleting spaces and joining characters belonging to one number together
    #--> Is used as a basis for validating the user input
    list_elements_input = get_elements_input(input_remove_segment)
    
    
    #List for analyzing the numbers given in the input
    list_number_elements = []
    
    #Iterate through elements of user input to add all numbers to list_number_elements
    for element in list_elements_input:
        
        #Check for valid input (Just numbers are accepted)
        if (element.isnumeric()==True or isfloat(element) == True):
        
            #Check if element is a number or a float
            # If yes, append it to list_number_elements to analyze the numbers given as input
            if (element.isnumeric()==True or isfloat(element) == True):
                list_number_elements.append(float(element))
            
        else:
            console.print('[bold red]Wrong input format. Only one positive number (with optional decimal point) is accepted.\n[/bold red]')
            return False, list_number_elements
    
    #Analyze the number(s) in the input:
    
    #Check for more than one number 
    if len(list_number_elements)>1:
        console.print("[bold red]Wrong input. More than one number was given as input.\n[/bold red]")
        return False, list_number_elements
    
    #Check for empty list --> No number in input
    if len(list_number_elements)==0:
        console.print("[bold red]Wrong input. No number was given as input.\n[/bold red]")
        return False, list_number_elements
      
    
    #Store input of s-coordinate for start of BSSD-segment
    input_s_start = list_number_elements[0]
    
        
    #Iterate through segments of current road to check if s-coordinate of input is identical to s-coordinate of an already existing segment
    for index, current_s_start in enumerate(df_created_segments_current_road.loc[:, 'segment_s_start']):
        
        #Check for identical s_start
        #Round to two digits. Rounding needed to cut off numerical errors for comparison of two float values
        if round(input_s_start, 2) == round(current_s_start, 2):
            
            #No removing of first segment in a road possible
            if index == 0:
                console.print('[bold red]Wrong input. Removing of first segment of the road (s_start = ' + str(current_s_start) + ') not possible \n[/bold red]' )
                return False, input_s_start
            
            #Valid input if input is equal to s_start of an already existing segment
            else:
                
                return True, input_s_start
    
    #If preceding for-loop couldn't find a segment with a s-start equal to the input, the input contains an invalid s-coordinate
    console.print('[bold red]Wrong input. A segment with s_start = ' + str(input_s_start) + ' does not exist\n[/bold red]' )
    return False, input_s_start


def get_elements_input(input_add_segments):
    """
    This function creates a list which contains the single elements of the user input in the variable "input_add_segments"/"input_remove_segments".
    In this context, an element is generally a character from the passed user input. 
    There are two exceptions from this:
        - Spaces are deleted
        - Characters which are digits and belonging to one Number are joined to one element 
            --> e.g. Characters "2", "5", ".", "0" would result in one element "25.0"
    """
    
    #List for storing single elements (e.g. comma, numbers) of input_add_segments 
    #--> deleting spaces and joining characters belonging to one number together
    list_elements_input = []
    #Variable for building a number out of multiple succeeding characters which contain a number
    number = None
    
    #Iteration through characters of passed input to store single elements of input in list_elements_input
    for i, char in enumerate(input_add_segments):
        
        #Skip spaces
        if char == ' ':
            continue
        
        #Check if character is a number
        elif char.isnumeric()==True:
            
            #Check if last character was a number
            #Case last character is no number
            if number == None:
                number = char
                
                #Check if a succeeding char exists in input_add_segments 
                if i<(len(input_add_segments)-1):
                    
                    #Check if succeeding char is not a number and not a decimal point "." (float value)
                    #If yes then current number is complete and can be added as an element to list
                    if input_add_segments[i+1].isnumeric()==False and input_add_segments[i+1]!=".":
                        list_elements_input.append(number)
                        number = None
                        
                #If no succeeding char exists, number is complete and can be added as an element to list
                else:
                    list_elements_input.append(number)
                continue
            
            #Case last character is a number
            else:
                #If last character was a number, the current character is added to the number
                number = number + char
                
                #Check if succeeding char is not a number --> If yes then current number is complete and can be added as an element to list 
                if i<(len(input_add_segments)-1):
                    
                    #Check if succeeding char is not a number and no decimal point "." (float value)
                    if input_add_segments[i+1].isnumeric()==False and input_add_segments[i+1]!=".":
                        list_elements_input.append(number)
                        number = None
                #If no succeeding char exists, number is complete and can be added as an element to list
                else:
                    list_elements_input.append(number)
                continue
        
        #Check if character is a decimal point "."
        elif char==".":
            #Check if last character was a number
            #Case last character is no number
            if number == None:
                list_elements_input.append(char)
            else:
                
                #Check if a succeeding char exists in input_add_segments 
                if i<(len(input_add_segments)-1):
                    
                    #Check if succeeding char is not a number
                    #If yes then current number and the decimal point "." are added as separate elements to the list
                    if input_add_segments[i+1].isnumeric()==False:
                        list_elements_input.append(number)
                        list_elements_input.append(char)
                        number = None
                    #If no, the decimal point is added to the number
                    else:
                        #If last character was a number, the current character is added to the number
                        number = number + char
                else:
                    #No suceeding char exists --> Current number and the decimal point "." are added as separate elements to the list 
                    list_elements_input.append(number)
                    list_elements_input.append(char)
                    
        #Add every character that is not a space or a number as a separate element to list
        else:
            list_elements_input.append(char)
    
    return list_elements_input

def isfloat(num):
#Check if input (variable "num") is a float
    try:
        float(num)
        return True
    
    except ValueError:
        return False
   

def insert_row(row_number, df, row_value):
    # Function to insert a row in a dataframe at a given position
    
    # Slice the upper half of the dataframe
    df1 = df[0:row_number]
  
    # Store the result of lower half of the dataframe
    df2 = df[row_number:]
  
    # Insert the row in the upper half dataframe
    df1.loc[row_number]=row_value
  
    # Concat the two dataframes
    df_result = pd.concat([df1, df2])
  
    # Reassign the index labels
    df_result.index = [*range(df_result.shape[0])]
  
    # Return the updated dataframe
    return df_result

def paste_segment(df_segments, index, road_id, input_s_start):
    """
    This function pastes a new segment (given road_id and s-coordinate) into df_segments at the passed index
    """
    
    #Check if current segment at position index (segment after which new segment is pasted) has a defined end
    #If no, the new segment can be pasted without modifications
    if pd.isnull(df_segments.loc[index, 'segment_s_end'])==True:
        
        #Values of new segment
        data_new_segment = [road_id, input_s_start, None]
        
        #Paste new segment into list of segments
        df_segments = insert_row(index+1, df_segments, data_new_segment)
        
        console.print('Added new segment with s_start = ' + str(input_s_start) + '\n')

    #If yes, the segment might be pasted with modifications
    else:
        #Case 1: s_start of new segment is higher than s_end of current segment
        #--> New segment can be pasted after current segment without modifications
        if input_s_start > df_segments.loc[index, 'segment_s_end']:
            #Values of new segment
            data_new_segment = [road_id, input_s_start, None]
            
            #Paste new segment into list of segments
            df_segments = insert_row(index+1, df_segments, data_new_segment)
            
            console.print('Added new segment with s_start = ' + str(input_s_start) + '\n')

        
        #Case 2: s_start of new segment is lower than s_end of current segment
        #--> New segment is pasted after current segment and takes the s_end-value from current segment
        else:
            #s_end of current segment --> Transfered to new segment
            current_s_end = df_segments.loc[index, 'segment_s_end']
            
            #Values of new segment (includes s_end of current segment)
            data_new_segment = [road_id, input_s_start, current_s_end]
            
            #s_end of current segment is set to None
            df_segments.loc[index, 'segment_s_end'] = None
            
            #Paste new segment into list of segments
            df_segments = insert_row(index+1, df_segments, data_new_segment)
            
            console.print('Added new segment with s_start = ' + str(input_s_start) + '\n')
    
    return df_segments