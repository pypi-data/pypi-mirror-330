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


class TestcaseOverall(unittest.TestCase):
    """
    TESTCASE OVERALL: Tests the whole implementation (all concept steps) with one exemplary OpenDRIVE-file
    """

    @mock.patch('builtins.input', create=True)    
    def test_overall(self, mocked_input):
        """
        Test 1: Tests the whole implementation (all concept steps) with one exemplary OpenDRIVE-file.
        
        The exemplary OpenDRIVE-file is a scene which consists of one T-junction (three roads and one junction).
        The scenery was built in Roadrunner in a way that as much funtionalities as possible of the implementation are tested.
        Due to that this scenery can be seen as a combination of all sceneries which where used in the tests for the single functionalities of the
        implementation.
        
        TODO Bild mit Szenerie verlinken
        --> See 

        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. filepath_xodr
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_overall'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

        
        ##2. Simulating user input 
                                    
                                    #Manually editing drivable lanes (for testing purposes)
        mocked_input.side_effect = ['y',
                                    #Proceed to road 1
                                    'c',
                                    #Mark one not drivable lane as drivable
                                    '4',
                                    #Mark the same lane again as not drivable
                                    '2',
                                    #Stop routine for manually editing drivable lanes
                                    'break',
                                    #Manually add segments
                                    'y',
                                    #Add all segments that are not extracted automatically
                                    #road 1
                                    '2.68',
                                    '17.34',
                                    '43.65',
                                    '76.19',
                                    '80.59',
                                    '92.72',
                                    'c',
                                    #No removing of segments
                                    'c',
                                    #road 9,
                                    '137.76',
                                    '176.44',
                                    #Dummy segment to test removing of segments
                                    '10.16',
                                    'c',
                                    '10.16',
                                    #road 23 & all roads in junction 29 --> No manual creation of segments necessary
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
        filename_xodr_expected = 'testcase_overall_expected'
        
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
        
        
        