from rich.table import Table
from rich import box
from rich.console import Console

def print_table(df, show_index, style_index):
    """
    This function creates and prints a rich table (rich.table.Table) based on a Pandas DataFrame (df).
        
    Parameters
    ----------
    df : DataFrame
        DataFrame which should be printed
    show_index : boolean
        Set to True, if the index of the DataFrame should be printed as the first column
        Set to False, if the index of the DataFrame should not be printed 
    style_index : String
        Specify the style of the index-column
        (e.g. "bold yellow" for displaying in bold an yellow --> see https://rich.readthedocs.io/en/stable/style.html for details)

    Returns
    -------
    None
    
    """
    #Deactivate auto-highlighting
    console = Console(highlight=False)
    
    #Create rich table 
    table = Table(show_lines=True, box=box.HEAVY_HEAD)
    
    #Check if index of imported DataFrame should be displayed
    #Case 1: Index should be displayed in first column
    if show_index == True:
        
        #Create separate column for index
        table.add_column('index', justify='center', style=style_index, header_style=style_index)
        
        #Create a column for every column in the imported DataFrame
        for column in df.columns:
            table.add_column(str(column), justify='center')

        #Fill the table with the values from the imported DataFrame
        for index, value_list in enumerate(df.values.tolist()):
            row = [str(index)]
            row += [str(x) for x in value_list]
            table.add_row(*row)
            
        #Print rich Table    
        console.print(table, justify='center')
    
    #Case 2: Index shouldn't be displayed in first column    
    else:
            #Create a column for every column in the imported DataFrame
            for column in df.columns:
                table.add_column(str(column), justify='center')
            
            #Fill the table with the values from the imported DataFrame
            for index, value_list in enumerate(df.values.tolist()):
                row = []
                row += [str(x) for x in value_list]
                table.add_row(*row)
                
            #print rich Table   
            console.print(table, justify='center')