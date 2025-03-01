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


class TestcaseAutobahn9(unittest.TestCase):
    """
    TESTCASE AUTOBAHN 9: Tests the whole implementation (all concept steps) with one exemplary snippet of the
    xodr-file "2017-04-04_Testfeld_A9_Nord_offset".
    
    """

    @mock.patch('builtins.input', create=True)    
    def test_Autobahn_9(self, mocked_input):
        """
        Test 1: Tests the whole implementation (all concept steps) with one exemplary snippet of the
                xodr-file "2017-04-04_Testfeld_A9_Nord_offset".
        
        The snippet contains a scenery which is representative for a motorway. It consists of "normal" motorway sections with changes in speed limit
        and overtaking. Furthermore it contains one entry and one exit to the motorway.
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. filepath_xodr
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_Autobahn_9'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

        ##2. Simulating user input 
                                    
                                    #Manually editing drivable lanes 
        mocked_input.side_effect = ['y',
                                    #Mark all lanes with attribute type="shoulder" as drivable as they are part of the street in the imported 
                                    #xodr-file
                                    '0,1,2,3',
                                    'c',
                                    '0,1,2,3',
                                    'c',
                                    '0,1,2,3,4',
                                    'c',
                                    '0,1,2',
                                    'c',
                                    '0,1,2',
                                    'c',
                                    '0',
                                    'c',
                                    '0',
                                    'c',
                                    '0',
                                    'c',
                                    '0',
                                    'c',
                                    #Manually edit segments 
                                    'y',
                                    #Road 2002000
                                    #Add
                                    'c',
                                    #Remove
                                    '2633.52',
                                    '2634.15',
                                    '2819.39',
                                    '2819.92',
                                    '2912.33',
                                    '2913.39',
                                    'c',
                                    #Road 2003000
                                    #Add
                                    '40.65',
                                    '59.685165',
                                    '81.0',
                                    '285.688103',
                                    '286.0',
                                    '297.0',
                                    'c',
                                    #Remove
                                    '90.62',
                                    '90.69',
                                    '255.3',
                                    '255.98',
                                    'c',
                                    #Road 2004000
                                    #Add
                                    '42.2',
                                    'c',
                                    #Remove
                                    '465.62',
                                    '468.02',
                                    '667.87',
                                    '668.37',
                                    'c',
                                    #Road 2016000
                                    #Add
                                    '40.255439',
                                    'c',
                                    #Remove
                                    'c',
                                    #Road 2017000
                                    #Add
                                    '15.61',
                                    '20.5',
                                    '26.849178',
                                    'c',
                                    #Remove
                                    'c',
                                    #Road 3011020, 3011021, 3012020, 3012021
                                    'break']
                                    
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
        filename_xodr_expected = 'testcase_Autobahn_9_expected'
        
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
        
        
        