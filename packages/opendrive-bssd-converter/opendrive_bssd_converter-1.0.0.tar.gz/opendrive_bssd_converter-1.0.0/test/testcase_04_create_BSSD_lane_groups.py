import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

from integrate_BSSD_into_OpenDRIVE.concept_steps.step_4_create_BSSD_lane_groups import step_4_create_BSSD_lane_groups
from utility.convert_xml_to_string_list import convert_xml_to_string_list


class TestcaseCreateBssdLaneGroups(unittest.TestCase):
    """
    TESTCASE 04: Tests the function step_4_create_BSSD_lane_groups.py. This includes:
        - Test 1: Check whether below every <segment>-element one element <right> and one element <left> (lane-groupings) is created correctly 
    """

    def test_create_BSSD_lane_groups(self):
        """
        Test 1: Check whether below every <segment>-element one element <right> and one element <left> (lane-groupings) is created correctly 
        
        As input data a xodr-file with two roads containing one laneSection each is used.
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_element
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_04'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr = ET.parse(filepath_xodr)

        #Access root-element of imported xodr-file
        OpenDRIVE_element = tree_xodr.getroot()
        
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        OpenDRIVE_element = step_4_create_BSSD_lane_groups(OpenDRIVE_element)

        #Convert resulting OpenDRIVE_element to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_string = convert_xml_to_string_list(OpenDRIVE_element)        

        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. OpenDRIVE_element
        
        #Filename of xodr which contains the expected result (Insertion of one element <right> and one element <left>  below every 
        #<segment>-element)
        filename_xodr_expected = 'testcase_04_expected'
        
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
        
        
        