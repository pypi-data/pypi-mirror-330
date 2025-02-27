import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path
from lxml import etree
import xml.etree.ElementTree as ET

from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_5_create_BSSD_lanes import step_5_create_BSSD_lanes
from utility.convert_xml_to_string_list import convert_xml_to_string_list

class TestcaseCreateBssdLanes(unittest.TestCase):
    """
    TESTCASE A.05: Tests the function step_5_create_BSSD_lanes.py. This includes:
        - Test 1: Checks for every BSSD-segment if <lane>-elements are created correctly based on <lane>-elements of first laneSection whose
         s-range overlaps with the s-range of the BSSD-segment

    """
    

    def test_create_BSSD_lanes(self):
        """
        Test 1: Checks for every BSSD-segment if <lane>-elements are created correctly based on <lane>-elements of first laneSection whose
         s-range overlaps with the s-range of the BSSD-segment
        
        As input data a xodr-file is used which consists of one road with four laneSections. Three laneSections contain drivable lanes.
        There are three BSSD-segments defined. One segment at s=0.0, which was extracted automatically from the laneSections, one segment at 
        s=60.0 which was created manually and one segment at s=145.75, which was extracted automatically from the laneSections.

        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_05'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        ##2. OpenDRIVE_element
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr = ET.parse(filepath_xodr)

        #Access root-element of imported xodr-file
        OpenDRIVE_element = tree_xodr.getroot()
        
        ##3. df_lane_data_drivable_lanes
        
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
        #Contains all drivable lanes of input xodr
                                    #Start of road 0
                                    #laneSection 0.0
        lane_data_drivable_lanes = [[0,    0.0,   1, 'driving', -1],
                                    [0,    0.0,  -1, 'driving', -1],
                                    #laneSection 56.05
                                    [0,  56.05,   1, 'driving', -1],
                                    [0,  56.05,  -1, 'driving', -1],
                                    #laneSection 145.75
                                    [0, 145.75,   2, 'driving', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
        
        ##4. df_segments
        
        #Contains all automatically extracted segments and all manually created segments
        df_segments = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        
                    #Start of road 0
                    #segment 0.0 --> overlaps with laneSection 0.0 and 56.05
        segments = [[0,   0.0,  None],
                    #segment at 60.0 --> user defined, ends at 98.13 as there begins a laneSection which contains no drivable lanes
                    [0,  60.0, 98.13],
                    #segment 145.75 --> overlaps with laneSection 145.75
                    [0,  145.75, None]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(segments):
            df_segments = df_segments.append({'road_id': segments[index][0],
                                            'segment_s_start': segments[index][1],
                                            'segment_s_end': segments[index][2]},
                                             ignore_index=True)
        
        #### 2. ACT
        #-----------------------------------------------------------------------

        df_overlappings_segments_laneSections, df_BSSD_lanes, OpenDRIVE_element = step_5_create_BSSD_lanes(df_segments, df_lane_data_drivable_lanes,
                                                                                            OpenDRIVE_element, OpenDRIVE_object) 
        
        #Convert resulting OpenDRIVE_element to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_string = convert_xml_to_string_list(OpenDRIVE_element) 
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. OpenDRIVE_element
        
        #Filename of xodr which contains the expected result (Insertion of BSSD-<lane>-elements based on first lane section overlapping with BSSD-Segment
        filename_xodr_expected = 'testcase_05_expected'
        
        #Filepath to xodr
        filepath_xodr_expected = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr_expected +'.xodr')
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr_expected = ET.parse(filepath_xodr_expected)
        
        #Access root-element of imported xodr-file
        OpenDRIVE_element_expected = tree_xodr_expected.getroot()
        
        #Convert OpenDRIVE_element_expected to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_expected_string = convert_xml_to_string_list(OpenDRIVE_element_expected)  
        
        ##2. df_overlappings_segments_laneSections
        
        #Get laneSection_objects from imported OpenDRIVE_object (needed for creating an expected version of df_overlappings_segments_laneSections)
        laneSection_object_0_0 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[0]
        laneSection_object_56_05 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[1]
        laneSection_object_145_75 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[3]
        
        df_overlappings_segments_laneSections_expected = pd.DataFrame(columns = ['road_id', 'segment_s', 'laneSection_s', 'laneSection_object'])
        
        #list to fill DataFrame
        #overlappings of BSSD-segments and lane sections
        
                                                       #Start of road 0
                                                       #segment 0.0, overlaps with laneSections 0.0 and 56.05
        overlappings_segments_laneSections_expected = [[0,   0.0, 0.0,  laneSection_object_0_0],
                                                       [0,   0.0, 56.05, laneSection_object_56_05],
                                                       #segment 60.0, overlaps with laneSection 56.05
                                                       [0,  60.0,  56.05, laneSection_object_56_05],
                                                       #segment 145.75, overlaps with laneSection 145.75
                                                       [0, 145.75, 145.75, laneSection_object_145_75]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(overlappings_segments_laneSections_expected):
            df_overlappings_segments_laneSections_expected = df_overlappings_segments_laneSections_expected.append(
                                                                            {'road_id': overlappings_segments_laneSections_expected[index][0],
                                                                            'segment_s': overlappings_segments_laneSections_expected[index][1],
                                                                            'laneSection_s': overlappings_segments_laneSections_expected[index][2],
                                                                            'laneSection_object': overlappings_segments_laneSections_expected[index][3]},
                                                                             ignore_index=True)
    
        ##3. df_BSSD_lanes
        
        df_BSSD_lanes_expected = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_object_s_min'])
        
        #list to fill DataFrame
        #Contains all created BSSD-lanes and the first laneSection overlapping to the segment which contains the BSSD-lane
                                #Start of road 0
                                #segment 0.0 has two BSSD-lanes --> id's are chosen based on laneSection 0.0
        BSSD_lanes_expected = [ [0,   0.0, -1,  laneSection_object_0_0],
                                [0,   0.0,  1,  laneSection_object_0_0],
                                #segment 60.0 has two BSSD-lanes --> id's are chosen based on laneSection 56.05
                                [0,  60.0, -1,  laneSection_object_56_05],
                                [0,  60.0,  1,  laneSection_object_56_05],
                                #segment 145.75 has one BSSD-lane --> id is chosen based on laneSection 145.75
                                [0, 145.75,  2,  laneSection_object_145_75]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_lanes_expected):
            df_BSSD_lanes_expected = df_BSSD_lanes_expected.append(
                                                                {'road_id': BSSD_lanes_expected[index][0],
                                                                'segment_s': BSSD_lanes_expected[index][1],
                                                                'lane_id_BSSD': BSSD_lanes_expected[index][2],
                                                                'laneSection_object_s_min': BSSD_lanes_expected[index][3]},
                                                                 ignore_index=True)
        
        #Check if real result is equal to expected result
        assert_frame_equal(df_overlappings_segments_laneSections_expected, df_overlappings_segments_laneSections)
        assert_frame_equal(df_BSSD_lanes_expected, df_BSSD_lanes)
        self.assertListEqual(OpenDRIVE_element_expected_string, OpenDRIVE_element_string)
    
if __name__ == '__main__':
    unittest.main()
        
        
        