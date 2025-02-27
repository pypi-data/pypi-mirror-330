from rich.console import Console
from rich import print
from rich.markdown import Markdown

from integrate_BSSD_into_OpenDRIVE.utility.print_table import print_table

console = Console(highlight=False)

def A_2_manually_edit_drivable_lanes(df_lane_data, df_lane_data_drivable_lanes, df_lane_data_not_drivable_lanes):
    """
    This function allows the user to manually edit the automatically found drivable lanes (see A_1_find_drivable_lanes.py).
    On the one hand additional lanes (not marked as drivable lanes by A_1_find_drivable_lanes.py) can be added to the list of drivable lanes.
    On the other hand lanes can be removed from the list of drivable lanes.
    
    
    Parameters
    ----------
    df_lane_data : DataFrame
        DataFrame which contains information about the type of the single OpenDRIVE-lanes in imported xodr-file (result of A_1_find_drivable_lanes.py)
    df_lane_data_drivable_lanes : DataFrame
        DataFrame which contains information about all lanes that represent a drivable OpenDRIVE-lane (result of A_1_find_drivable_lanes.py)
    df_lane_data_not_drivable_lanes : DataFrame
        DataFrame which contains information about all lanes that don't represent a drivable OpenDRIVE-lane (result of A_1_find_drivable_lanes.py)

    Returns
    -------
    df_lane_data_drivable_lanes : DataFrame
        Modified DataFrame with information about all drivable lanes.
    df_lane_data_not_drivable_lanes : DataFrame
        Modified DataFrame with information about all lanes that are not drivable.

    """
          
    
    console.print('Starting routine for manually editing the found drivable lanes...\n')
    console.print('This routine can be aborted by typing "break" every time a console input is necessary. The changes until the abortion will be stored.\n')
    

    #Iterate through all roads of OpenDRIVE-file for manually adding/deleting found drivable lanes
    for road_id in df_lane_data['road_id'].unique():
        
        #Get junction_id of current road (is None if road is not inside a junction)
        junction_id = df_lane_data[df_lane_data['road_id']==road_id].reset_index(drop=True).loc[0, 'junction_id']
        
        #Provide additional information if road is located inside a junction
        #Case: Road outside a junction
        if junction_id == -1:
            console.print('Road with id ' + str(road_id) + '\n', style='bold red')
        
        #Case: Road inside a junction
        else:
            console.print('Road with id ' + str(road_id) + ' (part of junction ' + str(junction_id) + ')\n', style='bold red')
        
       
        #1. Mark additional lanes as drivable lanes
        #--------------------------------------------------------------------------------
        console.print('1. Mark additional lanes as drivable:\n ', style='bold yellow')
        
        #Access all lanes that were marked as drivable lanes for the current road
        drivable_lanes = df_lane_data_drivable_lanes[df_lane_data_drivable_lanes['road_id']==road_id]
        drivable_lanes['laneSection_s'] = drivable_lanes['laneSection_s'].round(2)
        drivable_lanes = drivable_lanes[['laneSection_s', 'lane_id', 'lane_type']]
        
        #Check whether there were marked any lanes as drivable
        if drivable_lanes.empty==False:
            console.print('The following lanes were marked as drivable lanes:\n ')
            
            #Display table in console with function "print_table" (Uses package rich)
            print_table(drivable_lanes, False, '')
        else:
            console.print('No lanes were marked as drivable lanes\n')
        
        #Access all lanes that were not marked as drivable lanes for the current road
        not_drivable_lanes = df_lane_data_not_drivable_lanes[df_lane_data_not_drivable_lanes['road_id']==road_id]
        not_drivable_lanes['laneSection_s'] = not_drivable_lanes['laneSection_s'].round(2)
        not_drivable_lanes = not_drivable_lanes[['laneSection_s', 'lane_id', 'lane_type']]
        
        
        #Check whether there are any lanes to add
        if not_drivable_lanes.empty == False:
            
            #Get index of first element to get offset to zero --> Indices are referenced to zero for better usability
            index_offset = not_drivable_lanes.index[0]
            
            #Reset index for better usability
            not_drivable_lanes = not_drivable_lanes.reset_index(drop=True)
            
            print()
            console.print('You can add the following lanes to the list of drivable lanes:\n')
            
            #Display table in console with function "print_table" (Uses package rich)
            print_table(not_drivable_lanes, True, 'bold yellow')
                        
            print()
            console.print('You have the following options:')
            print(Markdown('* Add one/multiple lanes by typing the indices (left column of list above) of all lanes to be added, separated by a comma in a list (e.g. type in "0, 2, 4" for adding lanes in the indices 0, 2 and 4)'))
            print(Markdown('* Type in "c" if you do not want to add additional lanes\n'))
            print(Markdown('* Type in "break" to abort editing the drivable lanes. All changes until now will be stored'))

            #Execute loop until valid user input is given
            while True:
                
                #Get user input
                print()
                input_add_lanes = input('Input: ')
                console.print()
                
                #Analyze user input
                #Abort execution when input is 'break' and return DataFrames
                if input_add_lanes == 'break':
                    return df_lane_data_drivable_lanes, df_lane_data_not_drivable_lanes
        
                else:
                    #Specific lanes were given as input (if input is valid)
                    if input_add_lanes != 'c':
                        
                        
                        #Check validity of input and get indices of input
                        return_value, indices_lanes_add = validate_input(input_add_lanes, not_drivable_lanes)
                        if return_value==False:
                            continue
                        
                        #Add offset to indices to get "true" index
                        indices_lanes_add = [index+index_offset for index in indices_lanes_add]
                        
                        #Add lanes specified in input to DataFrame with drivable lanes
                        for index in indices_lanes_add:
                                                        
                            lane_to_add = df_lane_data_not_drivable_lanes.iloc[[index]]
                            #Add lanes from input to DataFrame with drivable lanes
                            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append(lane_to_add, ignore_index=True)
                            console.print('Added lane with id ' + str(df_lane_data_not_drivable_lanes.loc[index, 'lane_id']) + ', laneSection ' + str(df_lane_data_not_drivable_lanes.loc[int(index), 'laneSection_s']) + ' successfully to list of drivable lanes\n')
                            #Sort in added lanes
                            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.sort_values(['road_id', 'laneSection_s', 'lane_id'])
                            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.reset_index(drop=True)
                            
                            
                        #Delete lanes from input from DataFrame with not drivable lanes
                        df_lane_data_not_drivable_lanes = df_lane_data_not_drivable_lanes.drop(indices_lanes_add)
                        df_lane_data_not_drivable_lanes = df_lane_data_not_drivable_lanes.reset_index(drop=True)
                        
                    break
            
        #All lanes already marked as drivable lanes
        else:
            console.print('All lanes are already marked as drivable lanes\n')
        
        #2. Remove lanes from list of drivable lanes
        #-----------------------------------------------------------------------------------------
        console.print('2. Remove lanes from list of drivable lanes:\n ', style='bold yellow')
        
        #Access all lanes that are currently marked as drivable lanes in current road
        drivable_lanes = df_lane_data_drivable_lanes[df_lane_data_drivable_lanes['road_id']==road_id]
        drivable_lanes['laneSection_s'] = drivable_lanes['laneSection_s'].round(2)
        drivable_lanes = drivable_lanes[['laneSection_s', 'lane_id', 'lane_type']]

        
        #Check whether there are any lanes to delete
        if drivable_lanes.empty==False:
            
                    
            #Get index of first element to get offset to zero --> Indices are referenced to zero for better usability
            index_offset = drivable_lanes.index[0]
            
            #Reset index for better usability
            drivable_lanes = drivable_lanes.reset_index(drop=True)
            
            console.print('The following lanes are currently marked as drivable lanes:\n ')
            
            #Display table in console with function "print_table" (Uses package rich)
            print_table(drivable_lanes, True, 'bold yellow')
            
            print()
            console.print('You have the following options: \n')
            console.print(Markdown('* Remove one/multiple lanes by typing the indices (left column of list above) of all lanes to be removed, separated by a comma in a list (e.g. type in "0, 2, 4" for adding lanes in the indices 0, 2 and 4)'))
            console.print(Markdown('* Type in "c" if you do not want remove additional lanes'))
            console.print(Markdown('* Type in "break" to abort editing the drivable lanes. All changes until now will be stored'))

            #Execute loop until valid user input is given
            while True:
                
                #Get user input
                print()
                input_remove_lanes = input('Input: ')
                console.print()
                
                #Analyze user input
                #Abort execution of when input is 'break' and return DataFrames
                if input_remove_lanes == 'break':
                    return df_lane_data_drivable_lanes, df_lane_data_not_drivable_lanes
        
                else:
                    #Specific lanes were given as input (if input is valid)
                    if input_remove_lanes != 'c':
                        
                        
                        #Check validity of input and get indices of input
                        return_value, indices_lanes_remove = validate_input(input_remove_lanes, drivable_lanes)
                        if return_value==False:
                            continue

                        #Add offset to indices to get "true" index
                        indices_lanes_remove = [index+index_offset for index in indices_lanes_remove]
                        
                        #Add lanes from input to DataFrame with not drivable lanes
                        for index in indices_lanes_remove:
                            
                            lane_to_add = df_lane_data_drivable_lanes.iloc[[index]]
                            #Add lanes from input to DataFrame with not drivable lanes
                            df_lane_data_not_drivable_lanes = df_lane_data_not_drivable_lanes.append(lane_to_add, ignore_index=True)
                            #Sort in added lanes
                            df_lane_data_not_drivable_lanes = df_lane_data_not_drivable_lanes.sort_values(['road_id', 'laneSection_s', 'lane_id'])
                            df_lane_data_not_drivable_lanes = df_lane_data_not_drivable_lanes.reset_index(drop=True)
                            
                            console.print('Removed lane with id ' + str(df_lane_data_drivable_lanes.loc[index, 'lane_id']) + ', laneSection ' + str(df_lane_data_drivable_lanes.loc[int(index), 'laneSection_s']) + ' successfully from list of drivable lanes\n')
                        
                        #Delete lanes from input from DataFrame with drivable lanes
                        df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.drop(indices_lanes_remove)
                        df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.reset_index(drop=True)
                    break

        else:
            console.print('No lanes are currently marked as drivable lanes\n')
    
    return df_lane_data_drivable_lanes, df_lane_data_not_drivable_lanes


#Function to check for correct user input (only numbers separated by comma)
def validate_input(given_input, df):
    """
    This function validates a user input (variable "given_input") --> In general only numbers seperated by comma are accepted.
    Beyond that the number has to be an index valid in passed DataFrame.
    
    Function returns True or False dependening on whether user input is valid or not.
    Additionaly the function returns the list list_number_elements, which includes all numbers of the user input
    """
    
    #Function for creating list with single elements of user input (e.g. comma, numbers) 
    #--> deleting spaces and joining characters belonging to one number together
    #--> Is used as a basis for validating the user input
    list_elements_input = get_elements_input(given_input)
    
    #List for analyzing the numbers given in the input
    list_number_elements = []
    
    #Iterate through elements of user input to add all numbers to list_number_elements
    for element in list_elements_input:
        
        #Check for valid input (only numbers and commas allowed)
        if (element.isnumeric()==True) or (element == ','):
            
            #Check if element is a number
            if element.isnumeric()==True:
                list_number_elements.append(element)
                
        else:
            console.print('[bold red]Wrong input format. Only positive numbers separated by commas are accepted.\n[/bold red]')
            return False, list_number_elements
    
    #Convert numbers in list_number_elements from string to int
    list_number_elements = list(map(int, list_number_elements))
    
    #Check if no number is included in input
    if len(list_number_elements) == 0:
        console.print('[bold red]Wrong input. No number was given as input\n[/bold red]')
        return False, list_number_elements
    
    #Check if double values exist
    if len(list_number_elements)>len(set(list_number_elements)):
        console.print('[bold red]Wrong input. At least one value is included twice in your input.\n[/bold red]')
        return False, list_number_elements
    
    #Iterate through numbers of user input (result of preceeding for-loop) to check for validity of the numbers
    for element in list_number_elements:
        
        #Accept numbers only if existing in passed DataFrame
        if (int(element) in df.index) == False:
            console.print('[bold red]Wrong input number. Index ' + str(element) + ' is not included in list above.\n[/bold red]')
            return False, list_number_elements
        
        
    return True, list_number_elements

def get_elements_input(given_input):
    """
    This function creates a list which contains the single elements of the user input in the variable "given_input".
    In this context, an element is generally a character from the passed user input. 
    There are two exceptions from this:
        - Spaces are deleted
        - Characters which are digits and belonging to one Number are joined to one element 
            --> e.g. Characters "2" and "5" would result in one element "25"
    """
    
    #List for storing single elements (e.g. comma, numbers) of given_input 
    list_elements_input = []
    
    #Variable for building a number out of multiple succeeding characters which contain a number
    number = None
    
    #Iteration through characters of passed input to store single elements of input in list_elements_input
    for i, char in enumerate(given_input):
        
        #Skip spaces
        if char == ' ':
            continue
        
        #Check if character is a number
        elif char.isnumeric()==True:
            
            #Check if last character was a number
            #Case last character is no number
            if number == None:
                number = char
                
                #Check if a succeeding character exists in given_input 
                if i<(len(given_input)-1):
                    
                    #Check if succeeding character is not a number 
                    #If yes then current number is complete and can be added as an element to list
                    if given_input[i+1].isnumeric()==False:
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
                
                #Check if succeeding character is not a number --> If yes then current number is complete and can be added as an element to list 
                if i<(len(given_input)-1):
                    
                    #Check if succeeding character is not a number
                    if given_input[i+1].isnumeric()==False:
                        list_elements_input.append(number)
                        number = None
                #If no succeeding character exists, number is complete and can be added as an element to list
                else:
                    list_elements_input.append(number)
                continue
        
        #Add every character that is not a space or a number as a separate element to list
        else:
            list_elements_input.append(char)
    
    return list_elements_input