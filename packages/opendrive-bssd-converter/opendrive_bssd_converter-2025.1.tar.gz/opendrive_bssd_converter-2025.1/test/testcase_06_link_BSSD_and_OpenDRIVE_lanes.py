import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path
from lxml import etree
import xml.etree.ElementTree as ET

from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_6_link_BSSD_and_OpenDRIVE_lanes import step_6_link_BSSD_and_OpenDRIVE_lanes
from utility.convert_xml_to_string_list import convert_xml_to_string_list

class TestcaseLinkBssdAndOpenDriveLanes(unittest.TestCase):
    """
    TESTCASE 06: Tests the function step_6_link_BSSD_and_OpenDRIVE_lanes.py. This includes:
        - Test 1: Checks for every created BSSD-<lane>-element if an element <assignLaneOpenDRIVE> is created, which contains
        <linkedLane>-elements which are representative for one OpenDRIVE-<lane>-element which is defined during the s-range of the
        BSSD-<lane>-element
    """
    
    def test_link_BSSD_and_OpenDRIVE_lanes(self):
        """
        Test 1: Checks for every created BSSD-<lane>-element if an element <assignLaneOpenDRIVE> is created, which contains
        <linkedLane>-elements which are representative for one OpenDRIVE-<lane>-element which is defined during the s-range of the
        BSSD-<lane>-element
        
        As input data a xodr-file is used which consists of one road with three laneSections. As there are only changes in the number 
        of non-drivable lanes, only one segment is extracted automatically. One additional segment is added by user input.
        As the id's of the drivable OpenDRIVE-lanes change due to the change in the number of non-drivable lanes, it can be checked whether
        the link of the BSSD-lanes to the corresponding OpenDRIVE-lanes is correctly.
        
        --> Same input data as for testcase_A_06_search_linked_OpenDRIVE_lanes.py

        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##For every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row is defined
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_06'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.6', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr = ET.parse(filepath_xodr)

        #Access root-element of imported xodr-file
        OpenDRIVE_element = tree_xodr.getroot()
        
        #Get laneSection_objects from imported OpenDRIVE_object
        laneSection_object_0_0 = OpenDRIVE_object.getRoad(1).lanes.lane_sections[0]
        laneSection_object_25_0 = OpenDRIVE_object.getRoad(1).lanes.lane_sections[1]
        laneSection_object_75_0 = OpenDRIVE_object.getRoad(1).lanes.lane_sections[2]
        
        ##1. df_overlappings_segments_laneSections
        
        df_overlappings_segments_laneSections = pd.DataFrame(columns = ['road_id', 'segment_s', 'laneSection_s', 'laneSection_object'])
        
        #list to fill DataFrame
        #overlappings of BSSD-segments and lane sections
                                            #Start of road 1
                                            #segment 0.0, overlaps with laneSections 0.0 and 25.0
        overlappings_segments_laneSections =[[1,   0.0, 0.0,  laneSection_object_0_0],
                                             [1,   0.0, 25.0, laneSection_object_25_0],
                                             #segment 50.0 (created by user input), overlaps with laneSections 20.0 and 75.0
                                             [1,  50.0,  25.0, laneSection_object_25_0],
                                             [1,  50.0,  75.0, laneSection_object_75_0]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(overlappings_segments_laneSections):
            df_overlappings_segments_laneSections = df_overlappings_segments_laneSections.append(
                                                                        {'road_id': overlappings_segments_laneSections[index][0],
                                                                        'segment_s': overlappings_segments_laneSections[index][1],
                                                                        'laneSection_s': overlappings_segments_laneSections[index][2],
                                                                        'laneSection_object': overlappings_segments_laneSections[index][3]},
                                                                         ignore_index=True)
        
          
        ##2. df_BSSD_lanes
        
        df_BSSD_lanes = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_object_s_min'])
        
        #list to fill DataFrame
        #Contains all created BSSD-lanes and the first laneSection overlapping to the segment which contains the BSSD-lane
        
                    #Start of road 1
                    #segment 0.0 has two BSSD-lanes --> id's are chosen based on laneSection 0.0
        BSSD_lanes=[[1,   0.0, -2,  laneSection_object_0_0],
                    [1,   0.0,  3,  laneSection_object_0_0],
                    #segment 50.0 has two BSSD-lanes --> id's are chosen based on laneSection 25.0
                    [1,  50.0, -3,  laneSection_object_25_0],
                    [1,  50.0,  3,  laneSection_object_25_0]]
        
        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_lanes):
            df_BSSD_lanes = df_BSSD_lanes.append(
                                                {'road_id': BSSD_lanes[index][0],
                                                'segment_s': BSSD_lanes[index][1],
                                                'lane_id_BSSD': BSSD_lanes[index][2],
                                                'laneSection_object_s_min': BSSD_lanes[index][3]},
                                                 ignore_index=True)

        
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_element = step_6_link_BSSD_and_OpenDRIVE_lanes(df_overlappings_segments_laneSections,
                                                                                                          df_BSSD_lanes, OpenDRIVE_element)  
        
        #Convert resulting OpenDRIVE_element to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_string = convert_xml_to_string_list(OpenDRIVE_element) 
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. OpenDRIVE_element
        
        #Filename of xodr which contains the expected result (Insertion of BSSD-<lane>-elements based on first lane section overlapping with BSSD-Segment
        filename_xodr_expected = 'testcase_06_expected'
        
        #Filepath to valid xodr with version 1.4
        filepath_xodr_expected = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.6', filename_xodr_expected +'.xodr')
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr_expected = ET.parse(filepath_xodr_expected)
        
        #Access root-element of imported xodr-file
        OpenDRIVE_element_expected = tree_xodr_expected.getroot()
        
        #Convert OpenDRIVE_element_expected to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_expected_string = convert_xml_to_string_list(OpenDRIVE_element_expected)
        
        ##2. df_link_BSSD_lanes_with_OpenDRIVE_lanes
        
        #Contains for every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row 
        df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected = pd.DataFrame(columns =
                                                                        ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_s',
                                                                         'lane_id_OpenDRIVE'])
        
        #list to fill DataFrame
        #Contains all created BSSD-lanes 
                                                        #Start of road 1
                                                        #segment 0.0 has two BSSD-lanes that overlap with two lane sections each
                                                        #BSSD-lane -2
        link_BSSD_lanes_with_OpenDRIVE_lanes_expected =[[1,   0.0, -2,  0.0, -2],
                                                        [1,   0.0, -2, 25.0, -3],
                                                        #BSSD-lane 3
                                                        [1,   0.0,  3,  0.0,  3],
                                                        [1,   0.0,  3, 25.0,  3],
                                                        #segment 50.0 has two BSSD-lanes that overlap with two lane sections each
                                                        #BSSD-lane -3
                                                        [1,  50.0, -3, 25.0, -3],
                                                        [1,  50.0, -3, 75.0, -3],
                                                        #BSSD-lane 3
                                                        [1,  50.0,  3, 25.0,  3],
                                                        [1,  50.0,  3, 75.0,  2]]

        
        #Paste list with data into DataFrame
        for index, element in enumerate(link_BSSD_lanes_with_OpenDRIVE_lanes_expected):
            df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected = df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected.append(
                                                                {'road_id': link_BSSD_lanes_with_OpenDRIVE_lanes_expected[index][0],
                                                                'segment_s': link_BSSD_lanes_with_OpenDRIVE_lanes_expected[index][1],
                                                                'lane_id_BSSD': link_BSSD_lanes_with_OpenDRIVE_lanes_expected[index][2],
                                                                'laneSection_s': link_BSSD_lanes_with_OpenDRIVE_lanes_expected[index][3],
                                                                'lane_id_OpenDRIVE': link_BSSD_lanes_with_OpenDRIVE_lanes_expected[index][4]},
                                                                 ignore_index=True)
    
        #Check if real result is equal to expected result
        assert_frame_equal(df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected, df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected)
        self.assertListEqual(OpenDRIVE_element_expected_string, OpenDRIVE_element_string)
        
    
if __name__ == '__main__':
    unittest.main()
        
        
        