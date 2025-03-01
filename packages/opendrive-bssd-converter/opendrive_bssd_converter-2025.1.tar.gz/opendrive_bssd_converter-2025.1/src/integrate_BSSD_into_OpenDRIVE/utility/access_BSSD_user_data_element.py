def access_BSSD_user_data_element(road_element):
    """
    This function returns the <userData>-element in a <road>-element of an OpenDRIVE-file that contains the BSSD-segments
    --> There might be other <userData>-elements existing in a <road>-element that do not include the BSSD-data

    Parameters
    ----------
    road_element : etree.ElementTree.Element
       <road>-element which contains the userData-element(s)

    Returns
    -------
    user_data_element : etree.ElementTree.Element
        Correct <userData>-element

    """
    
    #Check whether multiple <userData>-elements are existing in <lanes>-element of imported <road>-element (May be the case if imported xodr
    #already contains <userData>-elements
    #Case 1: Multiple <userData>-elements exist --> Search for <userData>-element with attribute "BSSD"
    if len(road_element.find('lanes').findall('userData'))>1:
        for curr_user_data_element in road_element.find('lanes').findall('userData'):
            if (curr_user_data_element.get('code')=='BSSD') & (curr_user_data_element.get('value')=='BSSD_segments'):
                user_data_element = curr_user_data_element
                break
    
    #Case 2: Only one <userData>-elements exists --> No search for right <userData>-element necessary
    else:
    
        #Access created <userData>-element in current road (exists only once per road)
        user_data_element = road_element.find('lanes').find('userData')
        
    return user_data_element
        
