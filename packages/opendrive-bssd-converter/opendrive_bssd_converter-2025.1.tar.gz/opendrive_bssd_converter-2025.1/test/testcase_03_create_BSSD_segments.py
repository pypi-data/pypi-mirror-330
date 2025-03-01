import unittest
from unittest import mock
from pathlib import Path
from lxml import etree
import xml.etree.ElementTree as ET
import pandas as pd
from pandas.testing import assert_frame_equal


from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive

from integrate_BSSD_into_OpenDRIVE.concept_steps.step_3_create_BSSD_segments import step_3_create_BSSD_segments
from utility.convert_xml_to_string_list import convert_xml_to_string_list


class TestcaseCreateBssdSegments(unittest.TestCase):
    """
    TESTCASE 03: Tests the function step_3_create_BSSD_segments.py. This includes:
        - Test 1: Check whether for every BSSD-segment in df_segments a <segment>-element is created correctly below the BSSD-<userData>-element
    """

    @mock.patch('builtins.input', create=True)
    def test_create_BSSD_segments(self, mocked_input):
        """
        Test 1: Check whether for every BSSD-segment in df_segments a <segment>-element is created correctly below the BSSD-<userData>-element
        
        As input data the same scenario as for testcase_A_04_manually_add_segments is used. It consists of one road with three laneSections.
        The middle laneSection contains no drivable lanes (Only sidewalk). To check whether <segment>-elements are only created below the 
        BSSD-<userData>-elements, the imported xodr contains a second <userData>-element, which does not belong to BSSD.
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_03'
        
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
        
        ##3. df_lane_data
        df_lane_data = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                    #Start of road 0
                    #laneSection 0.0
        lane_data =[[0,    0.0,   1, 'driving', -1],
                    [0,    0.0,  -1, 'driving', -1],
                    #laneSection 29.97
                    [0,  29.97,   1, 'sidewalk', -1],
                    [0,  29.97,   2, 'sidewalk', -1],
                    [0,  29.97,  -1, 'sidewalk', -1],
                    #laneSection 62.18
                    [0,  62.18,   1, 'driving', -1],
                    [0,  62.18,  -1, 'driving', -1]]
    
        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data):
            df_lane_data = df_lane_data.append({'road_id': lane_data[index][0],
                                                'laneSection_s': lane_data[index][1],
                                                'lane_id': lane_data[index][2],
                                                'lane_type': lane_data[index][3],
                                                'junction_id': lane_data[index][4]}, ignore_index=True)
          
        ##4. df_lane_data_drivable_lanes
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                                    #Start of road 0
                                    #laneSection 0.0
        lane_data_drivable_lanes =[ [0,    0.0,   1, 'driving', -1],
                                    [0,    0.0,  -1, 'driving', -1],
                                    #laneSection 62.18
                                    [0,  62.18,   1, 'driving', -1],
                                    [0,  62.18,  -1, 'driving', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
        
        ##5. Simulating user input 
        
        #Input "n" skips the routine for manually adding segments
        #--> Here not necessary as this function is tested separately (testcase_A_03_extract_segments_automatically.py)
        mocked_input.side_effect = ['n']
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_segments, df_speed_limits, OpenDRIVE_element = step_3_create_BSSD_segments(df_lane_data, df_lane_data_drivable_lanes,
                                                                                      OpenDRIVE_element, OpenDRIVE_object)

        #Convert resulting OpenDRIVE_element to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_string = convert_xml_to_string_list(OpenDRIVE_element)        


        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. OpenDRIVE_element
        
        #Filename of xodr which contains the expected result (Insertion of two elements <segment> in road 0 for the two segments at s=0.0 and s=62.18)
        filename_xodr_expected = 'testcase_03_expected'
        
        #Filepath to xodr
        filepath_xodr_expected = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr_expected +'.xodr')
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr_expected = ET.parse(filepath_xodr_expected)
        
        #Access root-element of imported xodr-file
        OpenDRIVE_element_expected = tree_xodr_expected.getroot()
        
        #Convert OpenDRIVE_element_expected to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_expected_string = convert_xml_to_string_list(OpenDRIVE_element_expected) 
        
        ##2. df_segments        
        df_segments_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments based on input df_segments_automatic
        segments_expected =[[0,   0.0,  29.97],
                            [0, 62.18,  None]]
        
        
                                 
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_expected):
            df_segments_expected = df_segments_expected.append({'road_id': segments_expected[index][0],
                                                                'segment_s_start': segments_expected[index][1],
                                                                'segment_s_end': segments_expected[index][2]},
                                                                 ignore_index=True)
        #Convert values in column "road_id" to int 
        df_segments_expected['road_id']=df_segments_expected['road_id'].convert_dtypes()
        
        #3. df_speed_limits

        df_speed_limits_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'sOffset', 'speed_max', 'unit'])
        
                                 #Start of road 0
                                 #All drivable lanes have speed-limit 40 mph
                                 #Speed limit of not drivable lanes not included in df_speed_limits
        speed_limits_expected = [[0,   0.0,  1, 0.0, float(40), 'mph'],
                                 [0,   0.0, -1, 0.0, float(40), 'mph'],
                                 [0, 62.18,  1, 0.0, float(40), 'mph'],
                                 [0, 62.18, -1, 0.0, float(40), 'mph']]
        
        #Paste list with data into DataFrame
        for index, element in enumerate(speed_limits_expected):
            df_speed_limits_expected = df_speed_limits_expected.append({'road_id': speed_limits_expected[index][0],
                                                                        'laneSection_s': speed_limits_expected[index][1],
                                                                        'lane_id': speed_limits_expected[index][2],
                                                                        'sOffset': speed_limits_expected[index][3],
                                                                        'speed_max': speed_limits_expected[index][4],
                                                                        'unit': speed_limits_expected[index][5]},
                                                                         ignore_index=True)
        
        #Check if test_result is equal to expected result
        self.assertListEqual(OpenDRIVE_element_expected_string, OpenDRIVE_element_string)
        assert_frame_equal(df_segments_expected, df_segments)
        assert_frame_equal(df_speed_limits_expected, df_speed_limits)
    
if __name__ == '__main__':

    unittest.main()
        
        
        