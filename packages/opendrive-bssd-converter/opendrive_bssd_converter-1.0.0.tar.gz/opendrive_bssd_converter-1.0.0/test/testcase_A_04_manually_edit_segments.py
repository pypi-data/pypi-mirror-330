import unittest
from unittest import mock
from pathlib import Path
from lxml import etree
import pandas as pd
from pandas.testing import assert_frame_equal

from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from integrate_BSSD_into_OpenDRIVE.algorithms.A_4_manually_edit_segments import A_4_manually_edit_segments
from integrate_BSSD_into_OpenDRIVE.algorithms.A_4_manually_edit_segments import validate_input_add
from integrate_BSSD_into_OpenDRIVE.algorithms.A_4_manually_edit_segments import validate_input_remove


class TestcaseManuallyEditSegments(unittest.TestCase):
    """
    TESTCASE A.04: Tests the function A_4_manually_edit_segments.py. This includes:
        - Test 1: Check whether segments given in an user input are correctly added to the list of segments in df_segments
        - Test 2: Check if valid/invalid user input when adding segments is recognized as valid/invalid
        - Test 3: Check whether segments given in an user input are correctly removed from the list of segments in df_segments
        - Test 4: Check if valid/invalid user input for removing a segment in a road is recognized as valid/invalid
    """
    
    @mock.patch('builtins.input', create=True)
    def test_1_manually_add_segments(self, mocked_input):
        """
        Test 1: Check whether segments given in an user input are correctly added to the list of segments in df_segments.
        The following two cases are checked:
            - Adding a segment at a s-coordinate which is in the definition area of a segment with no defined s-end-coordinate
            - Adding a segment at a s-coordinate which is in the definition area of a segment with a defined s-end-coordinate
        
        As input data one road with three laneSections is used. The middle laneSection contains no drivable lanes (Only sidewalk).

        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_04_1'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        ##2. df_segments_automatic        
        df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments automatically extracted
        segments_automatic =[[0,   0.0,  29.97],
                             [0,  62.18,  None]]
                             
    
        
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic):
            df_segments_automatic = df_segments_automatic.append({'road_id': segments_automatic[index][0],
                                                                'segment_s_start': segments_automatic[index][1],
                                                                'segment_s_end': segments_automatic[index][2]},
                                                                 ignore_index=True)
         
        ##3. Simulating user input 
        
        #Input "80.25" adds a segment with s-coordinate 80.25 and no defined end in df_segments_automatic
        #Input "20" adds a segment with s-coordinate 20.0 and a defined end at 29.97 in df_segments_automatic
        #Input "break" means that no additional segment should be added (or removed) for this road
        mocked_input.side_effect = ['80.25', '20', 'break']
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_segments = A_4_manually_edit_segments(df_segments_automatic, OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        
        ##1. df_segments        
        df_segments_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments based on input df_segments_automatic
        segments_expected =[[0,   0.0,  None],
                            [0,  20.0, 29.97],
                            [0, 62.18,  None],
                            [0, 80.25,  None],]
                                 
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_expected):
            df_segments_expected = df_segments_expected.append({'road_id': segments_expected[index][0],
                                                                'segment_s_start': segments_expected[index][1],
                                                                'segment_s_end': segments_expected[index][2]},
                                                                 ignore_index=True)
                
        #Check if test_result is equal to expected result (= True)
        assert_frame_equal(df_segments_expected, df_segments)
     
    

    def test_2_validate_input_add(self):
        """
        Test 2: Check if valid/invalid user input for adding a segment in a road is recognized as valid/invalid.
        As input data a road with three existing segments is chosen. One segment has a defined s-end-coordinate, two segments have no
        defined s-end-coordinate
        
        The following valid input cases are checked:
            - Correct s-coordinate without decimal point
            - Correct s-coordinate with decimal point
        
        The following invalid input cases are checked:
            - Multiple s-coordinates
            - Empty input 
            - s-coordinate higher than length of road
            - s-coordinate equal to length of road
            - s-coordinate equal to existing segment 
            - s-coordinate equal to defined end of existing segment
            - s-coordinate in area where no segment is defined'

        """
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_created_segments_current_road --> Contains all created segments for one road
        df_created_segments_current_road = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #List with created segments in one road 
        created_segments_current_road =[[0,   0.0,  40.0],
                                        [0,   75.0,  None],
                                        [0,   90.0,  None]]
                             
        #Paste list with data into DataFrame
        for index, element in enumerate(created_segments_current_road):
            df_created_segments_current_road = df_created_segments_current_road.append({'road_id': created_segments_current_road[index][0],
                                                                                        'segment_s_start': created_segments_current_road[index][1],
                                                                                        'segment_s_end': created_segments_current_road[index][2]},
                                                                                         ignore_index=True)
       
        ##2. Define length of road for which user input for adding segments is used
        road_length = 100.0
        
        ##3. User inputs
        
        #Provide valid inputs
        
        #correct s-coordinate without decimal point
        input_valid_1 = '20'
        #correct s-coordinate with decimal point
        input_valid_2 = '20.25'

        
        #Provide invalid inputs
        
        #Multiple s-coordinates
        input_invalid_1 = '20, 30'
        #Empty input 
        input_invalid_2 = ''
        #s-coordinate higher than length of road
        input_invalid_3 = '1500'
        #s-coordinate equal to length of road
        input_invalid_4 = '100.0'
        #s-coordinate equal to existing segment 
        input_invalid_5 = '75.0'
        #s-coordinate equal to defined end of existing segment
        input_invalid_6 = '40.0'
        #s-coordinate in area where no segment is defined
        input_invalid_7 = '50.0'
        
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        return_input_valid_1, input_s_start = validate_input_add(input_valid_1, road_length, df_created_segments_current_road)
        return_input_valid_2, input_s_start = validate_input_add(input_valid_2, road_length, df_created_segments_current_road)
        
        return_input_invalid_1, input_s_start = validate_input_add(input_invalid_1, road_length, df_created_segments_current_road)
        return_input_invalid_2, input_s_start = validate_input_add(input_invalid_2, road_length, df_created_segments_current_road)
        return_input_invalid_3, input_s_start = validate_input_add(input_invalid_3, road_length, df_created_segments_current_road)
        return_input_invalid_4, input_s_start = validate_input_add(input_invalid_4, road_length, df_created_segments_current_road)
        return_input_invalid_5, input_s_start = validate_input_add(input_invalid_5, road_length, df_created_segments_current_road)
        return_input_invalid_6, input_s_start = validate_input_add(input_invalid_6, road_length, df_created_segments_current_road)
        return_input_invalid_7, input_s_start = validate_input_add(input_invalid_7, road_length, df_created_segments_current_road)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
    
        #Check if returned values are equal to expected result (True or False depending on input)
        self.assertTrue(return_input_valid_1)
        self.assertTrue(return_input_valid_2)

        self.assertFalse(return_input_invalid_1)
        self.assertFalse(return_input_invalid_2)
        self.assertFalse(return_input_invalid_3)
        self.assertFalse(return_input_invalid_4)
        self.assertFalse(return_input_invalid_5)
        self.assertFalse(return_input_invalid_6)
        
    @mock.patch('builtins.input', create=True)
    def test_3_manually_remove_segments(self, mocked_input):
        """
        Test 3: Check whether segments given in an user input are correctly removed from the list of segments in df_segments.
                
        The following two cases are checked:
            - Removing a segment with no defined s-end coordinate
            - Removing a segment with a defined s-end-coordinate
        
        As input data one road with four laneSections is used. Two laneSections contain no drivable lanes (Only sidewalk).

        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_04_2'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        ##2. df_segments_automatic        
        df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments automatically extracted
        segments_automatic =[[0,   0.0,  56.05],
                             [0,  98.13, 145.75]]
                             
    
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic):
            df_segments_automatic = df_segments_automatic.append({'road_id': segments_automatic[index][0],
                                                                'segment_s_start': segments_automatic[index][1],
                                                                'segment_s_end': segments_automatic[index][2]},
                                                                 ignore_index=True)
         
        ##3. Simulating user input 
        
        #Input before "c" adds segments (s=30.0, 120.0, 15.0) 
        #Input after "c" removes segments (s=15.0, 30.0, 98.13, 120.0) 
        #Input "break" means that no additional segment should be removed for this road
        mocked_input.side_effect = ['30.0', '120.0', '15.0', 'c', '15.0', '30.0', '98.13', '120.0', 'break']
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_segments = A_4_manually_edit_segments(df_segments_automatic, OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        
        ##1. df_segments        
        df_segments_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #All segments except for segment 0.0 were removed by user input
        segments_expected =[[0,   0.0,  56.05]]
                            
                                 
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_expected):
            df_segments_expected = df_segments_expected.append({'road_id': segments_expected[index][0],
                                                                'segment_s_start': segments_expected[index][1],
                                                                'segment_s_end': segments_expected[index][2]},
                                                                 ignore_index=True)
                
        #Check if test_result is equal to expected result (= True)
        assert_frame_equal(df_segments_expected, df_segments)
        
    def test_4_validate_input_remove(self):
        """
        Test 4: Check if valid/invalid user input for removing a segment in a road is recognized as valid/invalid.
        As input data a road with three existing segments is chosen. One segment has a defined s-end-coordinate, two segments have no
        defined s-end-coordinate
        
        The following valid input cases are checked:
            - Correct s-coordinate without decimal point
            - Correct s-coordinate with decimal point
        
        The following invalid input cases are checked:
            - Multiple s-coordinates
            - Empty input 
            - s-coordinate of first segment (can't be removed)
            - s-coordinate of a segment which doesn't exist
            - wrong input format (No number, negative number)

        """
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_created_segments_current_road --> Contains all created segments for one road
        df_created_segments_current_road = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #List with created segments in one road 
        created_segments_current_road =[[0,   0.0,  40.0],
                                        [0,   75.0,  None],
                                        [0,   90.0,  None]]
                             
        #Paste list with data into DataFrame
        for index, element in enumerate(created_segments_current_road):
            df_created_segments_current_road = df_created_segments_current_road.append({'road_id': created_segments_current_road[index][0],
                                                                                        'segment_s_start': created_segments_current_road[index][1],
                                                                                        'segment_s_end': created_segments_current_road[index][2]},
                                                                                         ignore_index=True)
       
        
        ##2. User inputs
        
        #Provide valid inputs
        
        #correct s-coordinate without decimal point
        input_valid_1 = '75'
        #correct s-coordinate with decimal point
        input_valid_2 = '90.0'

        #Provide invalid inputs
        
        #Multiple s-coordinates
        input_invalid_1 = '20, 30'
        #Empty input 
        input_invalid_2 = ''
        #s-coordinate of first segment (can't be removed)
        input_invalid_3 = '0.0'
        #s-coordinate of a segment which doesn't exist 
        input_invalid_4 = '100.0'
        #Wrong input format 
        input_invalid_5 = 'a'
        #Wrong input format 
        input_invalid_6 = '-3'
        
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        return_input_valid_1, input_s_start = validate_input_remove(input_valid_1, df_created_segments_current_road)
        return_input_valid_2, input_s_start = validate_input_remove(input_valid_2, df_created_segments_current_road)
        
        return_input_invalid_1, input_s_start = validate_input_remove(input_invalid_1, df_created_segments_current_road)
        return_input_invalid_2, input_s_start = validate_input_remove(input_invalid_2, df_created_segments_current_road)
        return_input_invalid_3, input_s_start = validate_input_remove(input_invalid_3, df_created_segments_current_road)
        return_input_invalid_4, input_s_start = validate_input_remove(input_invalid_4, df_created_segments_current_road)
        return_input_invalid_5, input_s_start = validate_input_remove(input_invalid_5, df_created_segments_current_road)
        return_input_invalid_6, input_s_start = validate_input_remove(input_invalid_6, df_created_segments_current_road)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
    
        #Check if returned values are equal to expected result (True or False depending on input)
        self.assertTrue(return_input_valid_1)
        self.assertTrue(return_input_valid_2)

        self.assertFalse(return_input_invalid_1)
        self.assertFalse(return_input_invalid_2)
        self.assertFalse(return_input_invalid_3)
        self.assertFalse(return_input_invalid_4)
        self.assertFalse(return_input_invalid_5)
        self.assertFalse(return_input_invalid_6)
        
if __name__ == '__main__':
    unittest.main()
        
        
        