import unittest
from unittest import mock
from pathlib import Path
import xml.etree.ElementTree as ET

from integrate_BSSD_into_OpenDRIVE.concept_steps.step_1_import_and_validate_xodr import step_1_import_and_validate_xodr
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_2_create_BSSD_root_elements import step_2_create_BSSD_root_elements
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_3_create_BSSD_segments import step_3_create_BSSD_segments
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_4_create_BSSD_lane_groups import step_4_create_BSSD_lane_groups
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_5_create_BSSD_lanes import step_5_create_BSSD_lanes
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_6_link_BSSD_and_OpenDRIVE_lanes import step_6_link_BSSD_and_OpenDRIVE_lanes
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_7_create_minimal_behavior_space_structure import step_7_create_minimal_behavior_space_structure
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_8_fill_BSSD_behavioral_attributes import step_8_fill_BSSD_behavioral_attributes

from utility.convert_xml_to_string_list import convert_xml_to_string_list


class TestcaseGriesheim(unittest.TestCase):
    """
    TESTCASE GRIESHEIM: Tests the whole implementation (all concept steps) with one exemplary snippet of the
    xodr-file "2021-09-29_1632_Conti_Griesheim_Gesamt_v1.4_offset".
    """

    @mock.patch('builtins.input', create=True)    
    def test_Griesheim(self, mocked_input):
        """
        Test 1: Tests the whole implementation (all concept steps) with one exemplary snippet of the
                xodr-file "2021-09-29_1632_Conti_Griesheim_Gesamt_v1.4_offset".
                
        The snippet contains a scenery which is representative for an urban X-junction. It consists of four roads leading to/from the junction
        and the junction itself.
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. filepath_xodr
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_Griesheim'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

        
        ##2. Simulating user input 
                                    
                                    #Manually editing drivable lanes 
        mocked_input.side_effect = ['y',
                                    #Some lanes with attribute 'border' are drivable, some lanes with attribute type="shoulder" are drivable 
                                    #xodr-file
                                    #Road 1019000
                                    'c',
                                    '1, 4, 6, 9, 11, 15, 17, 21, 23, 26',
                                    #Road 1031000
                                    '3',
                                    '0, 4, 5, 10, 11, 16, 17, 22',
                                    #Road 1015000
                                    'c',
                                    '0, 5',
                                    #Road 1030000
                                    'c',
                                    '0, 5, 6, 11, 12, 17, 18, 23, 24, 29, 30, 35',
                                    #Road 3055100
                                    'c',
                                    #Road 3055150
                                    'c',
                                    #Road 3055050
                                    'c',
                                    '0, 3, 6, 9, 12',
                                    #Road 3055300
                                    'c',
                                    '0, 3, 6, 9, 12, 15, 18, 21, 25, 29, 33',
                                    #Road 3055200
                                    'c',
                                    '0, 3, 7',
                                    #Road 3055250,
                                    'c', 
                                    '0, 3, 7, 11, 15',
                                    #Manually editing segments
                                    'y',
                                    #Road 1015000
                                    'c',
                                    #Road 1019000
                                    'c',
                                    'c',
                                    #Road 1030000
                                    '196.5525787117',
                                    'c',
                                    'c',
                                    #Road 1031000
                                    '76.7965626287',
                                    'c',
                                    '78.25',
                                    'c',
                                    #Road 3055050
                                    'c',
                                    '11.21',
                                    #Road 3055100
                                    'c',
                                    #Road 3055150
                                    'c',
                                    '2.92',
                                    '20.87',
                                    #Road 3055200
                                    'c',
                                    'c',
                                    #Road 3055250
                                    '18.6302099062',
                                    'c',
                                    'c',
                                    #Road 3055300
                                    'c',
                                    '3.23',
                                    'c']
                                    
        #### 2. ACT
        #-----------------------------------------------------------------------

        #Execute function for step 1
        OpenDRIVE_element, OpenDRIVE_object, driving_direction = step_1_import_and_validate_xodr(filepath_xodr)

        #Execute function for step 2
        df_lane_data, df_lane_data_drivable_lanes, OpenDRIVE_element = step_2_create_BSSD_root_elements(OpenDRIVE_element, OpenDRIVE_object)

        #Execute function for step 3
        df_segments, df_speed_limits, OpenDRIVE_element = step_3_create_BSSD_segments(df_lane_data, df_lane_data_drivable_lanes, OpenDRIVE_element,
                                                                                      OpenDRIVE_object)

        #Execute function for step 4
        OpenDRIVE_element = step_4_create_BSSD_lane_groups(OpenDRIVE_element)

        #Execute function for step 5
        df_overlappings_segments_laneSections, df_BSSD_lanes, OpenDRIVE_element = step_5_create_BSSD_lanes(df_segments, df_lane_data_drivable_lanes,
                                                                                            OpenDRIVE_element, OpenDRIVE_object) 

        #Execute function for step 6
        df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_element = step_6_link_BSSD_and_OpenDRIVE_lanes(df_overlappings_segments_laneSections,
                                                                                                          df_BSSD_lanes, OpenDRIVE_element)      

        #Execute function for step 7
        OpenDRIVE_element = step_7_create_minimal_behavior_space_structure(OpenDRIVE_element) 


        #Execute function for step 8
        OpenDRIVE_element = step_8_fill_BSSD_behavioral_attributes(df_lane_data, df_BSSD_lanes, df_link_BSSD_lanes_with_OpenDRIVE_lanes,
                                                                                            df_speed_limits, df_segments, driving_direction, 
                                                                                            OpenDRIVE_element, OpenDRIVE_object)
        
        #Convert resulting OpenDRIVE_element to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_string = convert_xml_to_string_list(OpenDRIVE_element)        


        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. OpenDRIVE_element
        
        #Filename of xodr which contains the expected result
        filename_xodr_expected = 'testcase_Griesheim_expected'
        
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
        self.assertListEqual(OpenDRIVE_element_expected_string, OpenDRIVE_element_string)
    
    
if __name__ == '__main__':

    unittest.main()
        
        
        