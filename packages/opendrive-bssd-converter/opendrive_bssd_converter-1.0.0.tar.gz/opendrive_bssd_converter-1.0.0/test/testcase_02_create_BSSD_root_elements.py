import unittest
from unittest import mock
from pathlib import Path
from lxml import etree
import xml.etree.ElementTree as ET
import pandas as pd
from pandas.testing import assert_frame_equal


from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_2_create_BSSD_root_elements import step_2_create_BSSD_root_elements
from utility.convert_xml_to_string_list import convert_xml_to_string_list


class TestcaseCreateBssdRootElements(unittest.TestCase):
    """
    TESTCASE 02: Tests the function step_2_create_BSSD_root_elements.py. This includes:
        - Test 1: Check whether a <userData>-elements is inserted in every <road>-element that contains at least one drivable lane.
           
    """

    @mock.patch('builtins.input', create=True)
    def test_create_BSSD_root_elements(self, mocked_input):
        """
        Test 1: Check whether a <userData>-element is inserted in every <road>-element that contains at least one drivable lane.
        
        As input data a xodr-file with two roads is used. One road contains drivable and not-
        drivable lanes. The other road only contains not-drivable lanes. It has to be checked if only an 
        <userData>-element is created in the road which has drivable lanes.
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_02'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        ##2. OpenDRIVE_element
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr = ET.parse(filepath_xodr)

        #Access root-element of imported xodr-file
        OpenDRIVE_element = tree_xodr.getroot()
        
        ##3. Simulating user input 
        
        #Input "n" skips the routine for manually adding/deleting drivable lanes
        #--> Here not necessary as this function is tested separately (testcase_A_02_1_manually_add_drivable_lanes.py and
        #                                                              testcase_A_02_2_manually_delete_drivable_lanes.py)
        mocked_input.side_effect = ['n']
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_lane_data, df_lane_data_drivable_lanes, OpenDRIVE_element = step_2_create_BSSD_root_elements(OpenDRIVE_element, OpenDRIVE_object)

        #Convert resulting OpenDRIVE_element to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_string = convert_xml_to_string_list(OpenDRIVE_element)        

        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. df_lane_data
        
        df_lane_data_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                              #Start of road 0 (contains drivable and not drivable lanes)
                              #laneSection 0.0
        lane_data_expected = [[0,   0.0,  1, 'driving', -1],
                              [0,   0.0,  2, 'sidewalk', -1],
                              [0,   0.0, -1, 'driving', -1],
                              [0,   0.0, -2, 'sidewalk', -1],
                              #Start of road 1 (contains only not-drivable lanes)
                              #laneSection 0.0
                              [1,   0.0,  1, 'biking', -1],
                              [1,   0.0,  2, 'sidewalk', -1],
                              [1,   0.0, -1, 'biking', -1],
                              [1,   0.0, -2, 'sidewalk', -1]]
    
        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_expected):
            df_lane_data_expected = df_lane_data_expected.append({'road_id': lane_data_expected[index][0],
                                                                  'laneSection_s': lane_data_expected[index][1],
                                                                  'lane_id': lane_data_expected[index][2],
                                                                  'lane_type': lane_data_expected[index][3],
                                                                  'junction_id': lane_data_expected[index][4]}, ignore_index=True)
    
        ##2. df_lane_data_drivable_lanes
        
        df_lane_data_drivable_lanes_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                                              #Start of road 0 (contains drivable and not drivable lanes)
                                              #laneSection 0.0
        lane_data_drivable_lanes_expected = [ [0,   0.0,  1, 'driving', -1],
                                              [0,   0.0, -1, 'driving', -1]]
        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes_expected):
            df_lane_data_drivable_lanes_expected = df_lane_data_drivable_lanes_expected.append(
                                                                                    {'road_id': lane_data_drivable_lanes_expected[index][0],
                                                                                    'laneSection_s': lane_data_drivable_lanes_expected[index][1],
                                                                                    'lane_id': lane_data_drivable_lanes_expected[index][2],
                                                                                    'lane_type': lane_data_drivable_lanes_expected[index][3],
                                                                                    'junction_id': lane_data_drivable_lanes_expected[index][4]},
                                                                                     ignore_index=True)
        
        ##3. OpenDRIVE_element
        
        #Filename of xodr which contains the expected result (Insertion of element <userData> in road 0 and no insertion of element <userData>
        #in road 1 as it contains no drivable lane)
        filename_xodr_expected = 'testcase_02_expected'
        
        #Filepath to xodr
        filepath_xodr_expected = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr_expected +'.xodr')

        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr_expected = ET.parse(filepath_xodr_expected)
        
        #Access root-element of imported xodr-file
        OpenDRIVE_element_expected = tree_xodr_expected.getroot()
        
        #Convert OpenDRIVE_element_expected to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_expected_string = convert_xml_to_string_list(OpenDRIVE_element_expected)  
        
        #Check if test_result is equal to expected result
        assert_frame_equal(df_lane_data_expected, df_lane_data)
        assert_frame_equal(df_lane_data_drivable_lanes_expected, df_lane_data_drivable_lanes)
        self.assertListEqual(OpenDRIVE_element_expected_string, OpenDRIVE_element_string)
    
    
if __name__ == '__main__':

    unittest.main()
        
        
        