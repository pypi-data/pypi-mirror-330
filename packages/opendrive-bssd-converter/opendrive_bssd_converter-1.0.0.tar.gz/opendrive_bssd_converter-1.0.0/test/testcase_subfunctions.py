import unittest
from pandas.testing import assert_frame_equal
import pandas as pd
from pathlib import Path
from lxml import etree
import numpy as np

from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from integrate_BSSD_into_OpenDRIVE.algorithms import A_1_find_drivable_lanes
from integrate_BSSD_into_OpenDRIVE.algorithms import A_2_manually_edit_drivable_lanes
from integrate_BSSD_into_OpenDRIVE.algorithms import A_4_manually_edit_segments
from integrate_BSSD_into_OpenDRIVE.algorithms import A_3_extract_segments_automatically

from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_extract_segments_automatically import check_for_succeeding_lane_section_with_no_drivable_lanes
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_4_segments_by_static_signals import check_signal_s_coordinate
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_4_segments_by_static_signals import analyze_signal_elements
from integrate_BSSD_into_OpenDRIVE.algorithms.A_7_1_extract_speed_attribute import set_identical_speed_attribute
from integrate_BSSD_into_OpenDRIVE.algorithms.A_7_1_extract_speed_attribute import set_speed_attribute_based_on_other_side

from integrate_BSSD_into_OpenDRIVE.utility.collect_object_data import calculate_extend_in_s_direction, calculate_extend_in_h_direction
from integrate_BSSD_into_OpenDRIVE.utility.classify_BSSD_lane_borders import set_shared_borders_not_crossable

class TescasetSubfunctions(unittest.TestCase):
    """
    TESTCASE SUBFUNCTIONS: Tests all help functions which are used throughout BSSD-integration into OpenDRIVE.
    A subfunction is a function which fulfills a minor task when executing a function representing 
    a concept step (folder "concept_steps"), an algorithm (folder "algorithms") or an utility function (folder "utility")
    
    This Testcase includes:
        - Test 1: Tests the function "get_elements_input" used in the algorithm "A_2_manually_edit_drivable_lanes"
        - Test 2: Tests the function "get_elements_input" used in the algorithm "A_4_manually_edit_segments"
        - Test 3: Tests the function "check_for_succeeding_lane_section_with_no_drivable_lanes" used in the algorithm 
                  "A_3_extract_segments_automatically".
        - Test 4: Tests the function "paste_segment" used in the algorithm "A_3_extract_segments_automatically".
        - Test 5: Tests the function "paste_segment" used in the algorithm "A_4_manually_edit_segments".
        - Test 6: Tests the function "check_if_biking_is_drivable" used in the algorithm "A_1_find_drivable_lanes"
        - Test 7: Tests the function "check_signal_s_coordinate" used in the algorithm "A_3_4_segments_by_static_signals".
        - Test 8: Tests the function "test_9_analyze_signal_elements" used in the algorithm "A_3_4_segments_by_static_signals". 
        - Test 9: Tests the functions "calculate_extend_in_s_direction" and "calculate_extend_in_h_direction" used in the utility function
                   "collect_object_data"
        - Test 10: Tests the function "set_shared_borders_not_crossable" used in the utitlity function "classify_BSSD_lane_borders"
        - Test 11: Tests the function "set_identical_speed_attribute" used in the algorithm "A_7_1_extract_speed_attribute"
        - Test 12: Tests the function "set_speed_attribute_based_on_other_side" used in the algorithm "A_7_1_extract_speed_attribute"
    """

    def test_1_get_elements_input_manually_edit_drivable_lanes(self):
        """
        Test 1: Tests the function "get_elements_input" used in the algorithm "A_2_manually_edit_drivable_lanes". This function gets a user input
                for adding drivable/non-drivable lanes as input and creates a list containing the single elements of the user input.
                In this context, an element is generally a character from the passed user input. 
                There are two exceptions from this:
                    - Spaces are deleted
                    - Characters which are digits and belonging to one Number are joined to one element 
                        --> e.g. Characters "2" and "5" would result in one element "25"
                        
                This function serves as a basis for validating the user input (function validate_input_add).
                
                It is checked whether for a given input, the single elements of the input are included correct in the list, which represents
                the output
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. given_input
        
        #Input-data represents indices for lanes to add/remove to/from the list of drivable lanes
        input_1 = '1, 3'
        input_2 = '10, 4'
        input_3 = '10.5, 6'
        input_4 = '1 5; 3'
        input_5 = 'wrong, 10'
                
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        list_elements_input_1 = A_2_manually_edit_drivable_lanes.get_elements_input(input_1)
        list_elements_input_2 = A_2_manually_edit_drivable_lanes.get_elements_input(input_2)
        list_elements_input_3 = A_2_manually_edit_drivable_lanes.get_elements_input(input_3)
        list_elements_input_4 = A_2_manually_edit_drivable_lanes.get_elements_input(input_4)
        list_elements_input_5 = A_2_manually_edit_drivable_lanes.get_elements_input(input_5)
               

        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. list_elements_input
        
        #Spaces are deleted from input and digits belongig to one number are joined together
        list_elements_input_1_expected=['1', ',', '3']
        list_elements_input_2_expected=['10', ',', '4']
        list_elements_input_3_expected=['10', '.', '5', ',', '6']
        list_elements_input_4_expected=['1', '5', ';', '3']
        list_elements_input_5_expected=['w', 'r', 'o', 'n', 'g', ',', '10']
        
 
        #Check if test_result is equal to expected result
        self.assertListEqual(list_elements_input_1_expected, list_elements_input_1)
        self.assertListEqual(list_elements_input_2_expected, list_elements_input_2)
        self.assertListEqual(list_elements_input_3_expected, list_elements_input_3)
        self.assertListEqual(list_elements_input_4_expected, list_elements_input_4)
        self.assertListEqual(list_elements_input_5_expected, list_elements_input_5)

    def test_2_get_elements_input_manually_add_segments(self):
        """
        Test 2: Tests the function "get_elements_input" used in the algorithm "A_4_manually_edit_segments". This function gets a user input
                for adding a segment at a certain s-coordinate and creates a list containing the single elements of the user input.
                In this context, an element is generally a character from the passed user input. 
                There are two exceptions from this:
                    - Spaces are deleted
                    - Characters which are digits and belonging to one Number are joined to one element 
                        --> e.g. Characters "2", "5", ".", "0" would result in one element "25.0"
                        
                This function serves as a basis for validating the user input (function validate_input_add).
                
                It is checked whether for a given input, the single elements of the input are included correct in the list, which represents
                the output
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. input_add_segments
        
        #Input-data represents a s-coordinate of a segment to be added 
        input_1 = '25'
        input_2 = '20.531'
        input_3 = '105.61    50'
        input_4 = '10; 60'
        input_5 = '.5'
        input_6 = 'wrong, 10'
                
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        list_elements_input_1 = A_4_manually_edit_segments.get_elements_input(input_1)
        list_elements_input_2 = A_4_manually_edit_segments.get_elements_input(input_2)
        list_elements_input_3 = A_4_manually_edit_segments.get_elements_input(input_3)
        list_elements_input_4 = A_4_manually_edit_segments.get_elements_input(input_4)
        list_elements_input_5 = A_4_manually_edit_segments.get_elements_input(input_5)
        list_elements_input_6 = A_4_manually_edit_segments.get_elements_input(input_6)

        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. list_elements_input
        
        #Spaces are deleted from input and digits belongig to one number are joined together
        list_elements_input_1_expected=['25']
        list_elements_input_2_expected=['20.531']
        list_elements_input_3_expected=['105.61', '50']
        list_elements_input_4_expected=['10', ';', '60']
        list_elements_input_5_expected=['.', '5']
        list_elements_input_6_expected=['w', 'r', 'o', 'n', 'g', ',', '10']
        
 
        #Check if test_result is equal to expected result
        self.assertListEqual(list_elements_input_1_expected, list_elements_input_1)
        self.assertListEqual(list_elements_input_2_expected, list_elements_input_2)
        self.assertListEqual(list_elements_input_3_expected, list_elements_input_3)
        self.assertListEqual(list_elements_input_4_expected, list_elements_input_4)
        self.assertListEqual(list_elements_input_5_expected, list_elements_input_5)
        self.assertListEqual(list_elements_input_6_expected, list_elements_input_6)
        
    def test_3_check_for_succeeding_lane_section_with_no_drivable_lanes(self):
        """
        Test 3: Tests the function "check_for_succeeding_lane_section_with_no_drivable_lanes" used in the algorithm 
                "A_3_extract_segments_automatically".
                This function checks for a laneSection (s_laneSection) whether there is a suceeding laneSection which doesn't contain
                any drivable lanes. This function is necessary to know whether a s_end-attribute has to be specified for a segment extracted
                by the existing laneSections.
                
                It is checked whether for given laneSections with drivable lanes, given laneSections with no drivable lanes and a certain
                laneSection with drivable lanes, the output is correct
                --> Correct output = True/False depending on whether the suceeding laneSection has no drivable lanes or not.
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. laneSections_all_lanes
        
        #s-coordiantes of all laneSections in a road
        laneSections_all_lanes = [0.0, 10.35, 80.1, 306.0]
        
        ##2. laneSections_drivable_lanes
        
        #s-coordiantes of all laneSections that contain at least one drivable lane
        laneSections_drivable_lanes = [0.0, 10.35, 306.0]
        
        ##3. s_laneSection

        #s-coordinate of laneSection for which should be checked whether it has a succeeding laneSection with no drivable lanes
        
        #Has no suceeding laneSection with no drivable lanes --> False
        s_laneSection_1 = 0.0
        #Has a suceeding laneSection with no drivable lanes --> True
        s_laneSection_2 = 10.35
        #Has no suceeding laneSection with no drivable lanes --> False
        s_laneSection_3 = 306.0
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        return_value_1 = check_for_succeeding_lane_section_with_no_drivable_lanes(s_laneSection_1, laneSections_drivable_lanes,
                                                                                         laneSections_all_lanes)
        return_value_2 = check_for_succeeding_lane_section_with_no_drivable_lanes(s_laneSection_2, laneSections_drivable_lanes,
                                                                                        laneSections_all_lanes)
        return_value_3 = check_for_succeeding_lane_section_with_no_drivable_lanes(s_laneSection_3, laneSections_drivable_lanes,
                                                                                         laneSections_all_lanes)

        #### 3. ASSERT
        #-----------------------------------------------------------------------
 
        #Check if test_result is equal to expected result
        self.assertFalse(return_value_1)
        self.assertTrue(return_value_2)
        self.assertFalse(return_value_3)
        
    def test_4_paste_segment_extract_segments_automatically(self):
        """
        Test 4: Tests the function "paste_segment" used in the algorithm "A_3_extract_segments_automatically".
                This function pastes a new segment (given road_id, s_start and s_end) into df_segments_automatic at the correct position.        
                
                It is checked whether a certain segment is pasted correctly into df_segments_automatic.
                Correct means:
                    - At the right index in the DataFrame (sorted by s_start-coordinates of segments)
                    - potentially taking over s_end from another existing segment if s_start of new segment is higher than s_start of other
                      segment and s_start is lower than s_end of other segment
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_segments_automatic
        
        #df_segments_automatic        
        df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments automatically extracted 
                             #Road 0
                             #Segment 0.0
        segments_automatic =[[0,   0.0,  None],
                             #Segment 30.0
                             [0,  30.0,  None],
                             #Segment 50.0, has a defined s_end
                             [0,  50.0,  80.0],
                             #Segment 110.0
                             [0, 110.0,  None],
                             #Segment 130.0, has a defined end
                             [0, 130.0, 150.0],
                             #Road 1
                             #Segment 0.0
                             [1,   0.0, None],
                             #Road 2
                             #Segment 30.0 (--> No drivable lanes from 0.0 to 30.0)
                             [2,  30.0, None],
                             #Segment 50.25
                             [2, 50.25, None]]
                             
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic):
            df_segments_automatic = df_segments_automatic.append({'road_id': segments_automatic[index][0],
                                                                'segment_s_start': segments_automatic[index][1],
                                                                'segment_s_end': segments_automatic[index][2]},
                                                                 ignore_index=True)
        
        ##2. Different input values to test function (road_id, s_start, s_end)
        
        
        #Pasting of "normal" segment with no defined s_end
        road_id_1 = 0
        s_start_1 = 40.0
        s_end_1 = None
        
        #Pasting of "normal" segment with no defined s_end 
        road_id_2 = 0
        s_start_2 = 60.0
        s_end_2 = None
        
        #Pasting of segment with defined s_end which is already included in df_segments_automatic
        road_id_3 = 0
        s_start_3 = 140.0
        s_end_3 = 150.0
        
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        df_segments_automatic_1 = A_3_extract_segments_automatically.paste_segment(df_segments_automatic, road_id_1, s_start_1, s_end_1)
        df_segments_automatic_2 = A_3_extract_segments_automatically.paste_segment(df_segments_automatic, road_id_2, s_start_2, s_end_2)
        df_segments_automatic_3 = A_3_extract_segments_automatically.paste_segment(df_segments_automatic, road_id_3, s_start_3, s_end_3)


        #### 3. ASSERT
        #-----------------------------------------------------------------------
            
        #Create expected result
        
        ##1. df_segments_automatic
        
        #df_segments_automatic_1
        df_segments_automatic_expected_1 = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments automatically extracted 
                                         #Road 0
                                         #Segment 0.0
        segments_automatic_expected_1 =[[0,   0.0,  None],
                                         #Segment 30.0
                                         [0,  30.0,  None],
                                         #Pasting segment 40.0 with no defined s_end
                                         [0,  40.0,  None],
                                         #Segment 50.0, has a defined s_end
                                         [0,  50.0,  80.0],
                                         #Segment 110.0
                                         [0, 110.0,  None],
                                         #Segment 130.0, has a defined end
                                         [0, 130.0, 150.0],
                                         #Road 1
                                         #Segment 0.0
                                         [1,   0.0, None],
                                         #Road 2
                                         #Segment 30.0 (--> No drivable lanes from 0.0 to 30.0)
                                         [2,  30.0, None],
                                         #Segment 50.25
                                         [2, 50.25, None]]
                             
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic_expected_1):
            df_segments_automatic_expected_1 = df_segments_automatic_expected_1.append({'road_id': segments_automatic_expected_1[index][0],
                                                                                'segment_s_start': segments_automatic_expected_1[index][1],
                                                                                'segment_s_end': segments_automatic_expected_1[index][2]},
                                                                                 ignore_index=True)
            
        
        #df_segments_automatic_2       
        df_segments_automatic_expected_2 = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments automatically extracted 
                                         #Road 0
                                         #Segment 0.0
        segments_automatic_expected_2 =[[0,   0.0,  None],
                                         #Segment 30.0
                                         [0,  30.0,  None],
                                         #Segment 50.0, has a defined s_end
                                         [0,  50.0,  None],
                                         #Pasting of segment 60.0 which takes over s_end from segment 50.0
                                         [0,  60.0,  80.0],
                                         #Segment 110.0
                                         [0, 110.0,  None],
                                         #Segment 130.0, has a defined end
                                         [0, 130.0, 150.0],
                                         #Road 1
                                         #Segment 0.0
                                         [1,   0.0, None],
                                         #Road 2
                                         #Segment 30.0 (--> No drivable lanes from 0.0 to 30.0)
                                         [2,  30.0, None],
                                         #Segment 50.25
                                         [2, 50.25, None]]
                             
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic_expected_2):
            df_segments_automatic_expected_2 = df_segments_automatic_expected_2.append({'road_id': segments_automatic_expected_2[index][0],
                                                                                'segment_s_start': segments_automatic_expected_2[index][1],
                                                                                'segment_s_end': segments_automatic_expected_2[index][2]},
                                                                                 ignore_index=True)
            
        #df_segments_automatic_3   
        df_segments_automatic_expected_3 = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments automatically extracted 
                                         #Road 0
                                         #Segment 0.0
        segments_automatic_expected_3 =[[0,   0.0,  None],
                                         #Segment 30.0
                                         [0,  30.0,  None],
                                         #Segment 50.0, has a defined s_end
                                         [0,  50.0,  80.0],
                                         #Segment 110.0
                                         [0, 110.0,  None],
                                         #Segment 130.0, has no defined end
                                         [0, 130.0, None],
                                         #Pasting of new segment with defined s_end
                                         [0, 140.0, 150.0],
                                         #Road 1
                                         #Segment 0.0
                                         [1,   0.0, None],
                                         #Road 2
                                         #Segment 30.0 (--> No drivable lanes from 0.0 to 30.0)
                                         [2,  30.0, None],
                                         #Segment 50.25
                                         [2, 50.25, None]]
                             
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic_expected_3):
            df_segments_automatic_expected_3 = df_segments_automatic_expected_3.append({'road_id': segments_automatic_expected_3[index][0],
                                                                                'segment_s_start': segments_automatic_expected_3[index][1],
                                                                                'segment_s_end': segments_automatic_expected_3[index][2]},
                                                                                 ignore_index=True)
    
        #Check if test_result is equal to expected result
        assert_frame_equal(df_segments_automatic_expected_1, df_segments_automatic_1)
        assert_frame_equal(df_segments_automatic_expected_2, df_segments_automatic_2)
        assert_frame_equal(df_segments_automatic_expected_3, df_segments_automatic_3)
        
    def test_5_paste_segment_manually_add_segments(self):
        """
        Test 5: Tests the function "paste_segment" used in the algorithm "A_4_manually_edit_segments".
                This function pastes a new segment (given road_id and s-coordinate) given by a user input into df_segments at the passed index        
                
                It is checked whether a certain segment is pasted correctly into df_segments_automatic.
                Correct means:
                    - At the right index in the DataFrame (sorted by s_start-coordinates of segments)
                    - potentially taking over s_end from another existing segment if s_start of new segment is higher than s_start of other
                      segment and s_start is lower than s_end of other segment
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_segments 
        
        df_segments = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments created
                    #Road 0
                    #Segment 0.0
        segments =[[0,   0.0,  None],
                    #Segment 30.0
                    [0,  30.0,  None],
                    #Segment 50.0, has a defined s_end
                    [0,  50.0,  80.0],
                    #Segment 110.0
                    [0, 110.0,  None],
                    #Segment 130.0, has a defined end
                    [0, 130.0, 150.0],
                    #Road 1
                    #Segment 0.0
                    [1,   0.0, None],
                    #Road 2
                    #Segment 30.0 (--> No drivable lanes from 0.0 to 30.0)
                    [2,  30.0, None],
                    #Segment 50.25
                    [2, 50.25, None]]
                             
        #Paste list with data into DataFrame
        for index, element in enumerate(segments):
            df_segments = df_segments.append({'road_id': segments[index][0],
                                            'segment_s_start': segments[index][1],
                                            'segment_s_end': segments[index][2]},
                                             ignore_index=True)
        
        ##2. Different input values to test function (road_id, input_s_start, index)
        
        #Pasting of segment at s=40.0
        road_id_1 = 0
        input_s_start_1 = 40.0
        index_1 = 1
        
        ##Pasting of segment at s=60.0 --> Has to take over s_end from preceding segment
        road_id_2 = 0
        input_s_start_2 = 60.0
        index_2 = 2
        
        
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        df_segments_1 = A_4_manually_edit_segments.paste_segment(df_segments, index_1, road_id_1, input_s_start_1)
        df_segments_2 = A_4_manually_edit_segments.paste_segment(df_segments, index_2, road_id_2, input_s_start_2)


        #### 3. ASSERT
        #-----------------------------------------------------------------------
            
        #Create expected result
        
        ##df_segments
        
        #df_segments_1
        df_segments_expected_1 = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments after pasting new segment 
                                #Road 0
                                #Segment 0.0
        segments_expected_1 =[  [0,   0.0,  None],
                                #Segment 30.0
                                [0,  30.0,  None],
                                #Pasting segment 40.0 with no defined s_end
                                [0,  40.0,  None],
                                #Segment 50.0, has a defined s_end
                                [0,  50.0,  80.0],
                                #Segment 110.0
                                [0, 110.0,  None],
                                #Segment 130.0, has a defined end
                                [0, 130.0, 150.0],
                                #Road 1
                                #Segment 0.0
                                [1,   0.0, None],
                                #Road 2
                                #Segment 30.0 (--> No drivable lanes from 0.0 to 30.0)
                                [2,  30.0, None],
                                #Segment 50.25
                                [2, 50.25, None]]
                             
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_expected_1):
            df_segments_expected_1 = df_segments_expected_1.append({'road_id': segments_expected_1[index][0],
                                                                    'segment_s_start': segments_expected_1[index][1],
                                                                    'segment_s_end': segments_expected_1[index][2]},
                                                                     ignore_index=True)
            
            
            
        
        #df_segments_2       
        #Create expected result
        #df_segments_automatic_1
        df_segments_expected_2 = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments after pasting new segment 
                                #Road 0
                                #Segment 0.0
        segments_expected_2 =[  [0,   0.0,  None],
                                #Segment 30.0
                                [0,  30.0,  None],
                                #Segment 50.0, has no defined end anymore as s_end was taken over by segment 60.0
                                [0,  50.0,  None],
                                #Segment 60.0, takes over s_end from segment 50.0
                                [0,  60.0,  80.0],
                                #Segment 110.0
                                [0, 110.0,  None],
                                #Segment 130.0, has a defined end
                                [0, 130.0, 150.0],
                                #Road 1
                                #Segment 0.0
                                [1,   0.0, None],
                                #Road 2
                                #Segment 30.0 (--> No drivable lanes from 0.0 to 30.0)
                                [2,  30.0, None],
                                #Segment 50.25
                                [2, 50.25, None]]
                             
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_expected_2):
            df_segments_expected_2 = df_segments_expected_2.append({'road_id': segments_expected_2[index][0],
                                                                    'segment_s_start': segments_expected_2[index][1],
                                                                    'segment_s_end': segments_expected_2[index][2]},
                                                                     ignore_index=True)
    
        #Check if test_result is equal to expected result
        assert_frame_equal(df_segments_expected_1, df_segments_1)
        assert_frame_equal(df_segments_expected_2, df_segments_2)   
        
        
        
    def test_6_check_if_biking_is_drivable(self):
        """
        Test 6: Tests the function "check_if_biking_is_drivable" used in the algorithm "A_1_find_drivable_lanes".
            
                
                This function checks for a certain lane (lane_id, laneSection_object) with attribute type="biking", if this lane is a drivable or a
                not drivable lane. A biking lane is considered as drivable if at least one of the neighbour lanes (if existing) is drivable.
                
                If the biking lane is drivable, the function returns True. If the biking lane is not drivable, the function returns False
                                    
                The input scenario contains drivable and not drivable biking lanes 
                --> Equal to testcase_A_01_2.xodr --> see Testcase_A_01_2_scene.png
                
                It is checked whether based on the input scenario the biking lanes are classified correctly as drivable/not drivable.
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. laneSection_object
        
        #Filename of xodr which contains the input scenario (Same scenario as testcase_A_01_2.xodr)
        filename_xodr = 'testcase_biking_drivable'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        #Get laneSection_objects from imported OpenDRIVE_object
        laneSection_object_road_0 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[0]
        laneSection_object_road_1 = OpenDRIVE_object.getRoad(1).lanes.lane_sections[0]
        
        ##2. lane_id
        
        #Lane id's of biking lanes in imported scenario
        
        #lane 2, road 0
        lane_id_1 = 2
        #lane -3, road 0
        lane_id_2 = -3
        #lane -1, road 1
        lane_id_3 = -1
        
        ##3. dict_lane_types
        
        #Dictionary defines whether an OpenDRIVE-lane of a certain type represents a drivable lane (Value 'yes' --> modelled in BSSD) 
        #or not a drivable lane (Value 'no' --> not modelled in BSSD)
        dict_lane_types = {'shoulder':      'yes',
                           'border':        'yes',
                           'driving':       'yes',
                           'stop':          'yes',
                           'none':          'no',
                           'restricted':    'yes',
                           'parking':       'yes',
                           'median':        'no',
                           'biking':        'no',
                           'sidewalk':      'no',
                           'curb':          'no',
                           'exit':          'yes',
                           'entry':         'yes',
                           'onRamp':        'yes',
                           'offRamp':       'yes',
                           'connectingRamp':'yes',
                           'bidirectional': 'yes',
                           'roadWorks':     'yes',
                           'tram':          'yes',
                           'rail':          'yes',
                           'bus':           'yes',
                           'taxi':          'yes',
                           'HOV':           'yes',
                           'mwyEntry':      'yes',
                           'mwyExit':       'yes',
                           'special1':      'yes',
                           'special2':      'yes',
                           'special3':      'yes'}
        
        #### 2. ACT
        #-----------------------------------------------------------------------

        return_value_1 = A_1_find_drivable_lanes.check_if_biking_is_drivable(lane_id_1, laneSection_object_road_0, dict_lane_types)
        return_value_2 = A_1_find_drivable_lanes.check_if_biking_is_drivable(lane_id_2, laneSection_object_road_0, dict_lane_types)
        return_value_3 = A_1_find_drivable_lanes.check_if_biking_is_drivable(lane_id_3, laneSection_object_road_1, dict_lane_types)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
    
        #Check if real result is equal to expected result
        #lane 2, road 0 has a drivable lane as neighbour --> drivable
        self.assertTrue(return_value_1)
        #lane -3, road 0 has no drivable lane as neighbour --> not drivable
        self.assertFalse(return_value_2)
        #lane -1, road 1 has a drivable lane as neighbour --> drivable
        self.assertTrue(return_value_3)
        
    
    def test_7_check_signal_s_coordinate(self):
        """
        Test 7: Tests the function "check_signal_s_coordinate" used in the algorithm "A_3_4_segments_by_static_signals".
        
        This function checks for the s-coordinate where a BSSD-relevant signal is defined (variable "s_signal") if there is the creation 
        of a BSSD-segment possible --> Depends on various conditions (e.g. if there is a drivable lane defined at this s-coordinate)

        Scene: One road with several signals:
            - One signal is defined at a negative s-coordinate --> No segment definition possible
            - One Signal with a s-coordinate in a BSSD definition gap --> No segment creation possible
            - One Signal with a s-coordinate where adrivable lane is defined --> Segment creation possible
            - One Signal with a s-coordinate higher than length of the road --> No segment creation possible
        
        --> It is checked whether the signals are accepted/denied correctly
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. road_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_check_signal_s_coordinate'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        road_object = OpenDRIVE_object.getRoad(0)
        
                   
        ##2. df_segments_automatic
        
        df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
                            #Start of road 0
                            #Segment 21.99
        segments_automatic= [[0,   21.99, None]]
                                       
                                     
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic):
            df_segments_automatic = df_segments_automatic.append({'road_id': segments_automatic[index][0],
                                                                'segment_s_start': segments_automatic[index][1],
                                                                'segment_s_end': segments_automatic[index][2]},
                                                                 ignore_index=True)
            
            
        ##3. road_id 
        #id of road which contains the signals
        road_id = 0
        
        ##4. s_signal
        
        #Signal with negative s-coordinate --> No segment creation possible
        s_signal_1 = -1.43
        #Signal with s-coordinate in BSSD definition gap --> No segment creation possible
        s_signal_2 = 5.54
        #Signal with s-coordinate where drivable lane is defined --> Segment creation possible
        s_signal_3 = 51.64
        #Signal with s-coordinate higher than length of the road --> No segment creation possible
        s_signal_4 = 101.28
    
        #### 2. ACT
        #-----------------------------------------------------------------------
        return_value_1 = check_signal_s_coordinate(s_signal_1, road_id, df_segments_automatic, road_object)
        return_value_2 = check_signal_s_coordinate(s_signal_2, road_id, df_segments_automatic, road_object)
        return_value_3 = check_signal_s_coordinate(s_signal_3, road_id, df_segments_automatic, road_object)
        return_value_4 = check_signal_s_coordinate(s_signal_4, road_id, df_segments_automatic, road_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        
        #Check if real result is equal to expected result
        
        #Signal with negative s-coordinate --> No segment creation possible
        self.assertFalse(return_value_1)
        #Signal with s-coordinate in BSSD definition gap --> No segment creation possible
        self.assertFalse(return_value_2)
        #Signal with s-coordinate where drivable lane is defined --> Segment creation possible
        self.assertTrue(return_value_3)
        #Signal with s-coordinate higher than length of the road --> No segment creation possible
        self.assertFalse(return_value_4)
        
    
    def test_8_analyze_signal_elements(self):
        """
        Test 8: Tests the function "test_9_analyze_signal_elements" used in the algorithm "A_3_4_segments_by_static_signals".
        
        This function analyzes the attribute "country" of the static <signal>-elements in the imported OpenDRIVE-file.
        It counts the number of static <signal>-elements that:
            - have no/an empty "country"-attribute --> variable number_signals_no_country
            - have a "country"-attribute representing Germany (see list country_attribute_accept_germany) --> variable number_signals_germany
            - have a "country"-attribute representing another country than Germany --> variable number_signals_other_country
            
        Scene: There exist several traffic signs, which affect BSSD, don't affect BSSD or are placed in a BSSD definition gap. In addition there is
        one <signalReference>-Element which is linked to a <signal>-Element
        --> See Testcase_A_03_4_scene.png

        Scene: One road + one junction with several signals from germany, another country than germany, and with no defined "country"-attribute:
        --> Same scene as for test_4_extract_segments_automatically_rule_4_2 from testcase_A_03_extract_segments_automatically.py
        --> See Testcase_A_03_4_scene.png
            
            
        --> It is checked whether the signals are counted correctly depending on their country-attribute
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_analyze_signal_elements'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        ##2. df_lane_data_drivable_lanes
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
        #Contains all drivable lanes of lane_data
        
                                    #road 0
                                    #laneSection 0.0
        lane_data_drivable_lanes =[ [0,    0.0,  -1, 'driving', -1],
                                    #Start of road 1
                                    #laneSection 28.72 (2 drivable lanes)
                                    [1,  28.72,   1, 'driving', -1],
                                    [1,  28.72,  -1, 'driving', -1],
                                    #laneSection 119.25 (2 drivable lanes)
                                    [1, 119.25,   1, 'driving', -1],
                                    [1, 119.25,  -1, 'driving', -1],
                                    #Road 5
                                    [5,    0.0,   1, 'driving', -1],
                                    [5,    0.0,  -1, 'driving', -1],
                                    #Roads in Junction 6
                                    #Road 7
                                    [7,    0.0,  -1, 'driving',  6],
                                    #Road 10
                                    [10,   0.0,   1, 'driving',  6],
                                    #Road 16
                                    [16,   0.0,   1, 'driving',  6],
                                    #Road 17
                                    [17,   0.0,  -1, 'driving',  6]]


        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
                   
        ##3. country_attribute_accept_germany
        
        #Static <signal>-elements can contain an attribute "country", which contains the country code of the signal (ISO 3166-1, alpha-2 codes)
        #This attribute is used to get only signals which represent traffic signs/road markings from Germany (country code = "DE")
        #To allow also other country-codes, this list contains all possible values of the "country"-attribute, which are according to ISO 3166-1 or
        #which aren't according to ISO 3166-1, but imply that Germany is meant
        country_attribute_accept_germany = ['DE', 'De', 'de', 'DEU', 'Deu', 'deu', 'GER', 'Ger', 'ger', 'Germany', 'germany', 'Deutschland',
                                            'deutschland']
        
    
        #### 2. ACT
        #-----------------------------------------------------------------------
        #Execute function for analyzing attribute "country" of the static <signal>-elements in the imported OpenDRIVE-file.
        #Depending on that, a user input is required or not
        number_signals_no_country, number_signals_germany, number_signals_other_country = analyze_signal_elements(df_lane_data_drivable_lanes,
                                                                                                                  country_attribute_accept_germany,
                                                                                                                  OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected result
        
        #Imported scene contains one <signal> with attribute "country = US"
        number_signals_no_country_expected = 1
        #Imported scene contains six <signals> with attribute "country = DE"
        number_signals_germany_expected = 6
        #Imported scene contains on <signal> with no defined attribute "country"
        number_signals_other_country_expected = 1
        
        #Check if real result is equal to expected result
        self.assertEqual(number_signals_no_country_expected, number_signals_no_country)
        self.assertEqual(number_signals_germany_expected, number_signals_germany)
        self.assertEqual(number_signals_other_country_expected, number_signals_other_country)
        
    
    def test_9_calculate_extend_in_s_h_direction (self):
        """
        Test 9: Tests the functions "calculate_extend_in_s_direction" and "calculate_extend_in_h_direction" used in the utility function
                "collect_object_data"
                                
                These functions calculate the extend of an object in the s-/h-coordinate based on the extend of the object in the local coordinate system 
                u, v, z and the rotation between the local coordinate system and the reference coordinate system (heading: gamma, pitch: beta, roll: alpha)
                
                As input data one object with dimensions length 1.2m, width 0.8 m, height 0.6 m is chosen.
                It is checked for different rotation angles of the object if the extend in s- and h-direction is calculated right
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. object data (Object has length of 1.2m, width of 0.8 m, height of 0.6 m)
        u_min = -0.6
        u_max = 0.6
        
        v_min = -0.4
        v_max = 0.4
        
        z_min = -0.3
        z_max = 0.3
        
        ##2. object rotation (alpha = roll, beta = pitch, gamma = heading)
        
        #1. object with no rotation
        alpha_1 = 0
        beta_1 = 0
        gamma_1 = 0
        
        #2. object with 90° rotation around u-axis (roll)
        alpha_2 = np.deg2rad(90)
        beta_2 = 0
        gamma_2 = 0
        
        #3. object with 90° rotation around v-axis (pitch)
        alpha_3 = 0
        beta_3 = np.deg2rad(90)
        gamma_3 = 0
        
        #4. object with 90° rotation around z-axis (heading)
        alpha_4 = 0
        beta_4 = 0
        gamma_4 = np.deg2rad(90)
        
        #5. object with 50° rotation around all axes
        alpha_5 = np.deg2rad(50)
        beta_5 = np.deg2rad(50)
        gamma_5 = np.deg2rad(50)
        
                    
                
        #### 2. ACT
        #-----------------------------------------------------------------------
                
        s_extend_min_1, s_extend_max_1 = calculate_extend_in_s_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha_1, beta_1, gamma_1)
        h_extend_min_1, h_extend_max_1 = calculate_extend_in_h_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha_1, beta_1, gamma_1)
        
        s_extend_min_2, s_extend_max_2 = calculate_extend_in_s_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha_2, beta_2, gamma_2)
        h_extend_min_2, h_extend_max_2 = calculate_extend_in_h_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha_2, beta_2, gamma_2)
        
        s_extend_min_3, s_extend_max_3 = calculate_extend_in_s_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha_3, beta_3, gamma_3)
        h_extend_min_3, h_extend_max_3 = calculate_extend_in_h_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha_3, beta_3, gamma_3)
        
        s_extend_min_4, s_extend_max_4 = calculate_extend_in_s_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha_4, beta_4, gamma_4)
        h_extend_min_4, h_extend_max_4 = calculate_extend_in_h_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha_4, beta_4, gamma_4)
        
        s_extend_min_5, s_extend_max_5 = calculate_extend_in_s_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha_5, beta_5, gamma_5)
        h_extend_min_5, h_extend_max_5 = calculate_extend_in_h_direction(u_max, v_max, z_max, u_min, v_min, z_min, alpha_5, beta_5, gamma_5)

        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        ##1. Extend of objects
        
        #1. object with no rotation --> reference coordinate system is equal to local coordinate system
        s_extend_min_1_expected = -0.6
        s_extend_max_1_expected = 0.6
        
        h_extend_min_1_expected = -0.3
        h_extend_max_1_expected = 0.3
        
        #2. object with 90° rotation around u-axis (roll)
        #s-coordinate equal to u-coordinates
        s_extend_min_2_expected = -0.6
        s_extend_max_2_expected = 0.6
        
        #h-coordinates equal to v-coordinates
        h_extend_min_2_expected = -0.4
        h_extend_max_2_expected = 0.4
        
        #3. object with 90° rotation around v-axis (pitch)
        #s-coordinate equal to z-coordinates
        s_extend_min_3_expected = -0.3
        s_extend_max_3_expected = 0.3
        
        #h-coordinates equal to negative u-coordinates
        h_extend_min_3_expected = -0.6
        h_extend_max_3_expected = 0.6
        
        #4. object with 90° rotation around z-axis (heading)
        #s-coordinate equal to negative v-coordinates
        s_extend_min_4_expected = -0.4
        s_extend_max_4_expected = 0.4
        
        #h-coordinates equal to z-coordinates
        h_extend_min_4_expected = -0.3
        h_extend_max_4_expected = 0.3
        
        #5. object with 50° rotation around all axes
        #s-coordinate
        s_extend_min_5_expected = -0.56
        s_extend_max_5_expected = 0.56
        
        #h-coordinates 
        h_extend_min_5_expected = -0.78
        h_extend_max_5_expected = 0.78
        
        
    
        #Check if test_result is equal to expected result
        self.assertEqual(s_extend_min_1_expected, s_extend_min_1)
        self.assertEqual(s_extend_max_1_expected, s_extend_max_1)
        self.assertEqual(h_extend_min_1_expected, h_extend_min_1)
        self.assertEqual(h_extend_max_1_expected, h_extend_max_1)
        
        self.assertEqual(s_extend_min_2_expected, s_extend_min_2)
        self.assertEqual(s_extend_max_2_expected, s_extend_max_2)
        self.assertEqual(h_extend_min_2_expected, h_extend_min_2)
        self.assertEqual(h_extend_max_2_expected, h_extend_max_2)
        
        self.assertEqual(s_extend_min_3_expected, s_extend_min_3)
        self.assertEqual(s_extend_max_3_expected, s_extend_max_3)
        self.assertEqual(h_extend_min_3_expected, h_extend_min_3)
        self.assertEqual(h_extend_max_3_expected, h_extend_max_3)
        
        self.assertEqual(s_extend_min_4_expected, s_extend_min_4)
        self.assertEqual(s_extend_max_4_expected, s_extend_max_4)
        self.assertEqual(h_extend_min_4_expected, h_extend_min_4)
        self.assertEqual(h_extend_max_4_expected, h_extend_max_4)
        
        self.assertEqual(s_extend_min_5_expected, s_extend_min_5)
        self.assertEqual(s_extend_max_5_expected, s_extend_max_5)
        self.assertEqual(h_extend_min_5_expected, h_extend_min_5)
        self.assertEqual(h_extend_max_5_expected, h_extend_max_5)
        
    
    def test_10_set_shared_borders_not_crossable(self):
        """
        Test 10: Tests the function "set_shared_borders_not_crossable" used in the utitlity function "classify_BSSD_lane_borders"
        
        This function goes through all BSSD-lanes where the right or left border was classified as not crossable. As this right/left border is the 
        left/right border of the right/left neighbour lane, the attribute not crossable has also to be set in the neighbour lane (One border is
        always shared by two lanes, except for outer lanes)
        
        In the input scenario there are two roads with several not crossable borders (due to objects) 
    
        It is checked whether for all not crossable borders the identical border in the neighbour BSSD-lane is also set to not crossable
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_BSSD_lanes_borders_crossable
        #--> Classification of lane borders as crossable/not-crossable based on criterion 1 & criterion 2 (befor setting shared borders to the 
        #identical value for crossability)
        
        df_BSSD_lanes_borders_crossable = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'crossable_left', 'crossable_right'])
        
        #list to fill DataFrame
        
                                        #Start of road 0
                                        #segment 0.0
                                        #Left border of -1 is not crossable
        BSSD_lanes_borders_crossable =[ [0,   0.0, -1,  False, True],
                                        [0,   0.0,  1,  True, True],
                                        #segment 20.0 
                                        [0,  20.0, -1,  True, True],
                                        #Right and left border of 1 is not crossable
                                        [0,  20.0,  1,  False, False],
                                        [0,  20.0,  2,  True, True],
                                        #road 1
                                        #segment 0.0
                                        [1,   0.0, -2,  True, True],
                                        [1,   0.0, -1, False, False],
                                        #Right and left border of -1 is not crossable
                                        [1,   0.0,  1,  True,  True]]
        
        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_lanes_borders_crossable):
            df_BSSD_lanes_borders_crossable = df_BSSD_lanes_borders_crossable.append(
                                            {'road_id': BSSD_lanes_borders_crossable[index][0],
                                            'segment_s': BSSD_lanes_borders_crossable[index][1],
                                            'lane_id_BSSD': BSSD_lanes_borders_crossable[index][2],
                                            'crossable_left': BSSD_lanes_borders_crossable[index][3],
                                            'crossable_right': BSSD_lanes_borders_crossable[index][4]},
                                             ignore_index=True)
            
        ##2. number_changed_border
        #Number of borders changed to not crossable based on objects (criterion 2)
        number_changed_border = 5
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_BSSD_lanes_borders_crossable, number_changed_border = set_shared_borders_not_crossable(df_BSSD_lanes_borders_crossable,
                                                                                                  number_changed_border)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected result
        
        ##1. df_BSSD_lanes_borders_crossable
        #--> Classification of lane borders as crossable/not-crossable based on criterion 1 & criterion 2
        
        df_BSSD_lanes_borders_crossable_expected = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'crossable_left',
                                                                           'crossable_right'])
        
        #list to fill DataFrame
        
                                                #Start of road 0
                                                #segment 0.0
                                                #Left border of -1 is not crossable --> Right border of 1 also not crossable
        BSSD_lanes_borders_crossable_expected =[[0,   0.0, -1,  False, True],
                                                [0,   0.0,  1,  True, False],
                                                #segment 20.0 
                                                [0,  20.0, -1,  False, True],
                                                #Right and left border of 1 is not crossable --> Right Border of 2 not crossable, left border of
                                                #1 not crossable
                                                [0,  20.0,  1,  False, False],
                                                [0,  20.0,  2,  True, False],
                                                #road 1
                                                #segment 0.0
                                                [1,   0.0, -2, False, True],
                                                [1,   0.0, -1, False, False],
                                                #Right and left border of -1 is not crossable --> Right border of 1 not crossable,
                                                #Left border of -2 is not crossable
                                                [1,   0.0,  1,  True, False]]
        
        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_lanes_borders_crossable_expected):
            df_BSSD_lanes_borders_crossable_expected = df_BSSD_lanes_borders_crossable_expected.append(
                                            {'road_id': BSSD_lanes_borders_crossable_expected[index][0],
                                            'segment_s': BSSD_lanes_borders_crossable_expected[index][1],
                                            'lane_id_BSSD': BSSD_lanes_borders_crossable_expected[index][2],
                                            'crossable_left': BSSD_lanes_borders_crossable_expected[index][3],
                                            'crossable_right': BSSD_lanes_borders_crossable_expected[index][4]},
                                             ignore_index=True)
            
        ##2. number_changed_border
        #Number of borders changed to not crossable based on objects (criterion 2 + function to set identical borders to identical values)
        number_changed_border_expected = 10
        
        #Check if real result is equal to expected result
        assert_frame_equal(df_BSSD_lanes_borders_crossable_expected, df_BSSD_lanes_borders_crossable)
        self.assertEqual(number_changed_border_expected, number_changed_border)
        
        
    def test_11_set_identical_speed_attribute(self):
        """
        Test 11: Tests the function "set_identical_speed_attribute" used in the algorithm "A_7_1_extract_speed_attribute"
        
        This function sets for a defined BSSD-lane in df_BSSD_speed_attribute (index_BSSD_lane) the speed attribute for the direction against the
        driving direction to the same value as along the driving direction.
        
        It is checked whether the speed limit is set correctly to an identical value
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_BSSD_speed_attribute
            
        
        ##Define df_BSSD_speed_attribute for three BSSD-lanes
        
        df_BSSD_speed_attribute_1 = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute for every BSSD-lane (behaviorAlong and behaviorAgainst)
        
        BSSD_speed_attribute_1 =[   [0,   0.0, -1, 50.0, None],
                                    [0,   0.0,  1, None, 60.0],
                                    [0,   0.0,  2, 30.0, 30.0]]

                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_1):
            df_BSSD_speed_attribute_1 = df_BSSD_speed_attribute_1.append(
                                                                    {'road_id': BSSD_speed_attribute_1[index][0],
                                                                    'segment_s': BSSD_speed_attribute_1[index][1],
                                                                    'lane_id_BSSD': BSSD_speed_attribute_1[index][2],
                                                                    'speed_behavior_along': BSSD_speed_attribute_1[index][3],
                                                                    'speed_behavior_against': BSSD_speed_attribute_1[index][4]},
                                                                     ignore_index=True)
            
        df_BSSD_speed_attribute_2 = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute for every BSSD-lane (behaviorAlong and behaviorAgainst)
        

        BSSD_speed_attribute_2 =[ [0,   0.0, -1, 50.0, None],
                                [0,   0.0,  1, None, 60.0],
                                [0,   0.0,  2, 30.0, 30.0]]
                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_2):
            df_BSSD_speed_attribute_2 = df_BSSD_speed_attribute_2.append(
                                                                    {'road_id': BSSD_speed_attribute_2[index][0],
                                                                    'segment_s': BSSD_speed_attribute_2[index][1],
                                                                    'lane_id_BSSD': BSSD_speed_attribute_2[index][2],
                                                                    'speed_behavior_along': BSSD_speed_attribute_2[index][3],
                                                                    'speed_behavior_against': BSSD_speed_attribute_2[index][4]},
                                                                     ignore_index=True) 
            
        df_BSSD_speed_attribute_3 = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute for every BSSD-lane (behaviorAlong and behaviorAgainst)
        

        BSSD_speed_attribute_3 =[ [0,   0.0, -1, 50.0, None],
                                [0,   0.0,  1, None, 60.0],
                                [0,   0.0,  2, 30.0, 30.0]]
                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_3):
            df_BSSD_speed_attribute_3 = df_BSSD_speed_attribute_3.append(
                                                                    {'road_id': BSSD_speed_attribute_3[index][0],
                                                                    'segment_s': BSSD_speed_attribute_3[index][1],
                                                                    'lane_id_BSSD': BSSD_speed_attribute_3[index][2],
                                                                    'speed_behavior_along': BSSD_speed_attribute_3[index][3],
                                                                    'speed_behavior_against': BSSD_speed_attribute_3[index][4]},
                                                                     ignore_index=True)
            
            
        #Speed attributes for three BSSD-lanes  
        #1. BSSD-lane with id -1
        speed_behavior_along_1 = 50.0
        speed_behavior_against_1 = None
        index_BSSD_lane_1 = 0
        
        #2. BSSD-lane with id 1
        speed_behavior_along_2 = None
        speed_behavior_against_2 = 60.0
        index_BSSD_lane_2 = 1
        
        #3. BSSD-lane with id 2
        speed_behavior_along_3 = 30.0
        speed_behavior_against_3 = 30.0
        index_BSSD_lane_3 = 2
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        df_BSSD_speed_attribute_1 = set_identical_speed_attribute(speed_behavior_along_1, speed_behavior_against_1, df_BSSD_speed_attribute_1,
                                                                index_BSSD_lane_1)
        
        df_BSSD_speed_attribute_2 = set_identical_speed_attribute(speed_behavior_along_2, speed_behavior_against_2, df_BSSD_speed_attribute_2,
                                                                index_BSSD_lane_2)
        
        df_BSSD_speed_attribute_3 = set_identical_speed_attribute(speed_behavior_along_3, speed_behavior_against_3, df_BSSD_speed_attribute_3,
                                                                index_BSSD_lane_3)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected result
        
        ##1. df_BSSD_speed_attribute
        
        #1.1 lane with id -1
        
        df_BSSD_speed_attribute_expected_1 = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute for every BSSD-lane(behaviorAlong and behaviorAgainst)

                                            #Identical speed value for BSSD-lane -1
        BSSD_speed_attribute_expected_1 = [[0,   0.0, -1, 50.0, 50.0],
                                           [0,   0.0,  1, None, 60.0],
                                           [0,   0.0,  2, 30.0, 30.0]]                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_expected_1):
            df_BSSD_speed_attribute_expected_1 = df_BSSD_speed_attribute_expected_1.append(
                                                                {'road_id': BSSD_speed_attribute_expected_1[index][0],
                                                                'segment_s': BSSD_speed_attribute_expected_1[index][1],
                                                                'lane_id_BSSD': BSSD_speed_attribute_expected_1[index][2],
                                                                'speed_behavior_along': BSSD_speed_attribute_expected_1[index][3],
                                                                'speed_behavior_against': BSSD_speed_attribute_expected_1[index][4]},
                                                                 ignore_index=True)
        
        #1.2 lane with id 1
        
        df_BSSD_speed_attribute_expected_2 = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute for every BSSD-lane (behaviorAlong and behaviorAgainst)


        BSSD_speed_attribute_expected_2 = [[0,   0.0, -1, 50.0, None],
                                           #Identical speed value for BSSD-lane 1
                                           [0,   0.0,  1, 60.0, 60.0],
                                           [0,   0.0,  2, 30.0, 30.0]]                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_expected_2):
            df_BSSD_speed_attribute_expected_2 = df_BSSD_speed_attribute_expected_2.append(
                                                                {'road_id': BSSD_speed_attribute_expected_2[index][0],
                                                                'segment_s': BSSD_speed_attribute_expected_2[index][1],
                                                                'lane_id_BSSD': BSSD_speed_attribute_expected_2[index][2],
                                                                'speed_behavior_along': BSSD_speed_attribute_expected_2[index][3],
                                                                'speed_behavior_against': BSSD_speed_attribute_expected_2[index][4]},
                                                                 ignore_index=True)
        
        
        #1.3 lane with id 2
        
        df_BSSD_speed_attribute_expected_3 = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute for every BSSD-lane (behaviorAlong and behaviorAgainst)

        BSSD_speed_attribute_expected_3 = [[0,   0.0, -1, 50.0, None],
                                           [0,   0.0,  1, None, 60.0],
                                           #Identical speed value for BSSD-lane 2
                                           [0,   0.0,  2, 30.0, 30.0]]                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_expected_3):
            df_BSSD_speed_attribute_expected_3 = df_BSSD_speed_attribute_expected_3.append(
                                                                {'road_id': BSSD_speed_attribute_expected_3[index][0],
                                                                'segment_s': BSSD_speed_attribute_expected_3[index][1],
                                                                'lane_id_BSSD': BSSD_speed_attribute_expected_3[index][2],
                                                                'speed_behavior_along': BSSD_speed_attribute_expected_3[index][3],
                                                                'speed_behavior_against': BSSD_speed_attribute_expected_3[index][4]},
                                                                 ignore_index=True)
        
        #Check if real result is equal to expected result
        assert_frame_equal(df_BSSD_speed_attribute_expected_1, df_BSSD_speed_attribute_1)
        assert_frame_equal(df_BSSD_speed_attribute_expected_2, df_BSSD_speed_attribute_2)
        assert_frame_equal(df_BSSD_speed_attribute_expected_3, df_BSSD_speed_attribute_3)
        
        
    def test_12_set_speed_attribute_based_on_other_side(self):
        """
        Test 12: Tests the function "set_speed_attribute_based_on_other_side" used in the algorithm "A_7_1_extract_speed_attribute"
        
        This function sets for a defined BSSD-lane in df_BSSD_speed_attribute (road_id, segment_s, lane_id_BSSD, index_BSSD_lane)
        the speed attribute for the direction against the driving direction to the value of the speed attribute of the innermost BSSD-lane on the other side of the road,
        where a speed attribute along driving direction has been defined.
        
        As input scenario there are several BSSD-lanes where a speed attribute along driving direction could be extracted as well as 
        BSSD-lanes where a speed attribute along driving direction could not be extracted.
        It is checked whether the speed attribute against driving direction is set correctly based on the above rule.
        
        The test is executed for RHT and LHT.
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_BSSD_speed_attribute
            
        
        ##Define df_BSSD_speed_attribute for three BSSD-lanes
        
        #1.1 RHT
        df_BSSD_speed_attribute_RHT = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute for every BSSD-lane (behaviorAlong and behaviorAgainst)
        
                                    #Segment 0.0
        BSSD_speed_attribute_RHT =[ [0,   0.0, -1, None, None],
                                    [0,   0.0, -2, None, None],
                                    [0,   0.0,  1, None, 50.0],
                                    [0,   0.0,  2, None, 40.0],
                                    #Segment 20.0
                                    [0,  20.0, -1, 50.0, None],
                                    [0,  20.0, -2, 60.0, None],
                                    [0,  20.0,  1, None, None],
                                    [0,  20.0,  2, None, None],
                                    #Segment 40.0
                                    [0,  40.0, -1, None, None],
                                    [0,  40.0, -2, 60.0, None],
                                    [0,  40.0,  1, None, 50.0],
                                    [0,  40.0,  2, None, 40.0],
                                    #Segment 60.0
                                    [0,  60.0, -1, 50.0, None],
                                    [0,  60.0, -2, 60.0, None],
                                    [0,  60.0,  1, None, None],
                                    [0,  60.0,  2, None, 40.0]]
                                                    
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_RHT):
            df_BSSD_speed_attribute_RHT = df_BSSD_speed_attribute_RHT.append(
                                                                    {'road_id': BSSD_speed_attribute_RHT[index][0],
                                                                    'segment_s': BSSD_speed_attribute_RHT[index][1],
                                                                    'lane_id_BSSD': BSSD_speed_attribute_RHT[index][2],
                                                                    'speed_behavior_along': BSSD_speed_attribute_RHT[index][3],
                                                                    'speed_behavior_against': BSSD_speed_attribute_RHT[index][4]},
                                                                     ignore_index=True)
        #1.2 LHT
        df_BSSD_speed_attribute_LHT = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute for every BSSD-lane (behaviorAlong and behaviorAgainst)
        
                                #Segment 0.0
        BSSD_speed_attribute_LHT =[ [0,   0.0, -1, None, None],
                                    [0,   0.0, -2, None, None],
                                    [0,   0.0,  1, 50.0, None],
                                    [0,   0.0,  2, 40.0, None],
                                    #Segment 20.0
                                    [0,  20.0, -1, None, 50.0],
                                    [0,  20.0, -2, None, 60.0],
                                    [0,  20.0,  1, None, None],
                                    [0,  20.0,  2, None, None],
                                    #Segment 40.0
                                    [0,  40.0, -1, None, None],
                                    [0,  40.0, -2, None, 60.0],
                                    [0,  40.0,  1, 50.0, None],
                                    [0,  40.0,  2, 40.0, None],
                                    #Segment 60.0
                                    [0,  60.0, -1, None, 50.0],
                                    [0,  60.0, -2, None, 60.0],
                                    [0,  60.0,  1, None, None],
                                    [0,  60.0,  2, 40.0, None]]
                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_LHT):
            df_BSSD_speed_attribute_LHT = df_BSSD_speed_attribute_LHT.append(
                                                                    {'road_id': BSSD_speed_attribute_LHT[index][0],
                                                                    'segment_s': BSSD_speed_attribute_LHT[index][1],
                                                                    'lane_id_BSSD': BSSD_speed_attribute_LHT[index][2],
                                                                    'speed_behavior_along': BSSD_speed_attribute_LHT[index][3],
                                                                    'speed_behavior_against': BSSD_speed_attribute_LHT[index][4]},
                                                                     ignore_index=True)
       
            
        ##2. road_id
        road_id = 0
    
        
        ##3. driving_direction
        driving_direction_RHT = 'RHT'
        driving_direction_LHT = 'LHT'
        

        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        #1. RHT
        for index_BSSD_lane, lane_id_BSSD in enumerate(df_BSSD_speed_attribute_RHT.loc[:, 'lane_id_BSSD']):
            segment_s = df_BSSD_speed_attribute_RHT.loc[index_BSSD_lane, 'segment_s']
            if lane_id_BSSD < 0:
                side_current_BSSD_lane = 'right'
            else:
                side_current_BSSD_lane = 'left'
        
            df_BSSD_speed_attribute_RHT = set_speed_attribute_based_on_other_side(road_id, segment_s, lane_id_BSSD, index_BSSD_lane,
                                                                              side_current_BSSD_lane,
                                                                            driving_direction_RHT, df_BSSD_speed_attribute_RHT)
  
        #2. LHT
        for index_BSSD_lane, lane_id_BSSD in enumerate(df_BSSD_speed_attribute_LHT.loc[:, 'lane_id_BSSD']):
            segment_s = df_BSSD_speed_attribute_LHT.loc[index_BSSD_lane, 'segment_s']
            if lane_id_BSSD < 0:
                side_current_BSSD_lane = 'right'
            else:
                side_current_BSSD_lane = 'left'
        
            df_BSSD_speed_attribute_LHT = set_speed_attribute_based_on_other_side(road_id, segment_s, lane_id_BSSD, index_BSSD_lane,
                                                                              side_current_BSSD_lane,
                                                                            driving_direction_LHT, df_BSSD_speed_attribute_LHT)
                                                                 
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected result
        
        ##1. df_BSSD_speed_attribute
        
        #1.1 RHT
        
        
        df_BSSD_speed_attribute_RHT_expected = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute for every BSSD-lane (behaviorAlong and behaviorAgainst)

        #speed attribute against the driving direction is the speed attribute (if defined) of the innermost BSSD-lane with opposite driving
        #direction
                                        #segment 0.0
        BSSD_speed_attribute_RHT_expected =[[0,   0.0, -1, None, 50.0],
                                            [0,   0.0, -2, None, 50.0],
                                            [0,   0.0,  1, None, 50.0],
                                            [0,   0.0,  2, None, 40.0],
                                            #Segment 20.0
                                            [0,  20.0, -1, 50.0, None],
                                            [0,  20.0, -2, 60.0, None],
                                            [0,  20.0,  1, 50.0, None],
                                            [0,  20.0,  2, 50.0, None],
                                            #Segment 40.0
                                            [0,  40.0, -1, None, 50.0],
                                            [0,  40.0, -2, 60.0, 50.0],
                                            [0,  40.0,  1, 60.0, 50.0],
                                            [0,  40.0,  2, 60.0, 40.0],
                                            #Segment 60.0
                                            [0,  60.0, -1, 50.0, 40.0],
                                            [0,  60.0, -2, 60.0, 40.0],
                                            [0,  60.0,  1, 50.0, None],
                                            [0,  60.0,  2, 50.0, 40.0]]                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_RHT_expected):
            df_BSSD_speed_attribute_RHT_expected = df_BSSD_speed_attribute_RHT_expected.append(
                                                                {'road_id': BSSD_speed_attribute_RHT_expected[index][0],
                                                                'segment_s': BSSD_speed_attribute_RHT_expected[index][1],
                                                                'lane_id_BSSD': BSSD_speed_attribute_RHT_expected[index][2],
                                                                'speed_behavior_along': BSSD_speed_attribute_RHT_expected[index][3],
                                                                'speed_behavior_against': BSSD_speed_attribute_RHT_expected[index][4]},
                                                                 ignore_index=True)
        
        
        #2.2 LHT
        
        df_BSSD_speed_attribute_LHT_expected = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute for every BSSD-lane (behaviorAlong and behaviorAgainst)

        #speed attribute against the driving direction is the speed attribute (if defined) of the innermost BSSD-lane with opposite driving
        #direction
                                        #segment 0.0
        BSSD_speed_attribute_LHT_expected =[[0,   0.0, -1, 50.0, None],
                                            [0,   0.0, -2, 50.0, None],
                                            [0,   0.0,  1, 50.0, None],
                                            [0,   0.0,  2, 40.0, None],
                                            #Segment 20.0
                                            [0,  20.0, -1, None, 50.0],
                                            [0,  20.0, -2, None, 60.0],
                                            [0,  20.0,  1, None, 50.0],
                                            [0,  20.0,  2, None, 50.0],
                                            #Segment 40.0
                                            [0,  40.0, -1, 50.0, None],
                                            [0,  40.0, -2, 50.0, 60.0],
                                            [0,  40.0,  1, 50.0, 60.0],
                                            [0,  40.0,  2, 40.0, 60.0],
                                            #Segment 60.0
                                            [0,  60.0, -1, 40.0, 50.0],
                                            [0,  60.0, -2, 40.0, 60.0],
                                            [0,  60.0,  1, None, 50.0],
                                            [0,  60.0,  2, 40.0, 50.0]]                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_LHT_expected):
            df_BSSD_speed_attribute_LHT_expected = df_BSSD_speed_attribute_LHT_expected.append(
                                                                {'road_id': BSSD_speed_attribute_LHT_expected[index][0],
                                                                'segment_s': BSSD_speed_attribute_LHT_expected[index][1],
                                                                'lane_id_BSSD': BSSD_speed_attribute_LHT_expected[index][2],
                                                                'speed_behavior_along': BSSD_speed_attribute_LHT_expected[index][3],
                                                                'speed_behavior_against': BSSD_speed_attribute_LHT_expected[index][4]},
                                                                 ignore_index=True)
        
        
        #Check if real result is equal to expected result
        assert_frame_equal(df_BSSD_speed_attribute_RHT_expected, df_BSSD_speed_attribute_RHT)
        assert_frame_equal(df_BSSD_speed_attribute_LHT_expected, df_BSSD_speed_attribute_LHT)
        
if __name__ == '__main__':

    unittest.main()
        