import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path
from lxml import etree

from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from integrate_BSSD_into_OpenDRIVE.algorithms.A_5_find_overlappings_segments_laneSections import A_5_find_overlappings_segments_laneSections

class TestcaseFindOverlappingsSegmentsLaneSections(unittest.TestCase):
    """
    TESTCASE A.05: Tests the function A_5_find_overlappings_segments_laneSections.py. This includes:
        - Test 1: Checks for every defined BSSD-segment whether all laneSections are found whose s-range overlaps to the
          s-range of the BSSD-segment 
    """
    

    def test_find_overlappings_segments_laneSections(self):
        """
        Test 1: Checks for every defined BSSD-segment whether all laneSections are found whose s-range overlaps to 
        the s-range of the BSSD-segment 
        
        As input data a xodr-file is used which consists of one road with three laneSections. Two laneSections contain drivable lanes.
        --> There are two BSSD-segments defined. One segment at s=0.0, which was extracted automatically from the laneSections,
        and one segment at s=30.0 which was created manually. 
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_05'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
          
        ##2. df_lane_data_drivable_lanes
        
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
        #Contains all drivable lanes in input xodr
                                    #Start of road 0
                                    #laneSection 0.0
        lane_data_drivable_lanes = [[0,    0.0,   1, 'driving', -1],
                                    [0,    0.0,  -1, 'driving', -1],
                                    #laneSection 24.3
                                    [0,   24.3,   1, 'driving', -1],
                                    [0,   24.3,  -1, 'driving', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
        
        ##3. df_segments
        #Contains all automatically extracted segments and all manually created segments
        df_segments = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        
                    #Start of road 0
                    #segment 0.0 --> overlaps with laneSection 0.0 and 24.3
        segments = [[0,   0.0,  None],
                    #segment at 30.0 --> user defined, ends at 57.95 as there begins a laneSection which contains no drivable lanes
                    [0,  30.0, 57.95]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(segments):
            df_segments = df_segments.append({'road_id': segments[index][0],
                                            'segment_s_start': segments[index][1],
                                            'segment_s_end': segments[index][2]},
                                             ignore_index=True)
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_overlappings_segments_laneSections = A_5_find_overlappings_segments_laneSections(df_segments, df_lane_data_drivable_lanes,
                                                                                        OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. df_overlappings_segments_laneSections
        
        df_overlappings_segments_laneSections_expected = pd.DataFrame(columns = ['road_id', 'segment_s', 'laneSection_s', 'laneSection_object'])
        
        #Get laneSection_objects from imported OpenDRIVE_object (needed for creating an expected version of df_overlappings_segments_laneSections)
        laneSection_object_0_0 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[0]
        laneSection_object_24_3 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[1]
        
        
        #list to fill DataFrame
        #overlappings of BSSD-segments and lane sections
                                                       #Start of road 0
                                                       #segment 0.0, overlaps with laneSections 0.0 and 24.3
        overlappings_segments_laneSections_expected = [[0,   0.0, 0.0,  laneSection_object_0_0],
                                                       [0,   0.0, 24.3, laneSection_object_24_3],
                                                       #segment 30.0, overlaps with laneSection 24.3
                                                       [0,  30.0,  24.3, laneSection_object_24_3]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(overlappings_segments_laneSections_expected):
            df_overlappings_segments_laneSections_expected = df_overlappings_segments_laneSections_expected.append(
                                                                            {'road_id': overlappings_segments_laneSections_expected[index][0],
                                                                            'segment_s': overlappings_segments_laneSections_expected[index][1],
                                                                            'laneSection_s': overlappings_segments_laneSections_expected[index][2],
                                                                            'laneSection_object': overlappings_segments_laneSections_expected[index][3]},
                                                                             ignore_index=True)
    
        #Check if real result is equal to expected result
        assert_frame_equal(df_overlappings_segments_laneSections_expected, df_overlappings_segments_laneSections)
        
    
if __name__ == '__main__':
    unittest.main()
        
        
        