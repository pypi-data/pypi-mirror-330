import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path
from lxml import etree

from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from integrate_BSSD_into_OpenDRIVE.algorithms.A_6_search_linked_OpenDRIVE_lanes import A_6_search_linked_OpenDRIVE_lanes

class TestcaseSearchLinkedOpenDriveLanes(unittest.TestCase):
    """
    TESTCASE A.06: Tests the function A_6_search_linked_OpenDRIVE_lanes.py. This includes:
        - Test 1: Checks for every defined BSSD-lane whether all OpenDRIVE-lanes that overlap to this BSSD-lane are found
    """
    
    def test_search_linked_OpenDRIVE_lanes(self):
        """
        Test 1: Checks for every defined BSSD-lane whether all OpenDRIVE-lanes that overlap to this BSSD-lane are found
        
        As input data a xodr-file is used which consists of one road with three laneSections. As there are only changes in the number 
        of non-drivable lanes, only one segment is extracted automatically. One additional segment is added by user input.
        As the id's of the drivable OpenDRIVE-lanes change due to the change in the number of non-drivable lanes, it can be checked whether
        the link of the BSSD-lanes to the corresponding OpenDRIVE-lanes is correctly.

        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##Import OpenDRIVE_object as laneSection-objects are needed for input-data (df_overlappings_segments_laneSections and df_BSSD_lanes)
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_06'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.6', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        
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
        df_link_BSSD_lanes_with_OpenDRIVE_lanes = A_6_search_linked_OpenDRIVE_lanes(df_overlappings_segments_laneSections, df_BSSD_lanes)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. df_link_BSSD_lanes_with_OpenDRIVE_lanes

        df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected = pd.DataFrame(columns =
                                                                        ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_s',
                                                                         'lane_id_OpenDRIVE'])
        
        #list to fill DataFrame
        #Contains for every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row 
        
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
        
    
        #Convert values in column "road_id", "lane_id_BSSD" and "lane_id_OpenDRIVE" to int 
        df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected['road_id']=df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected['road_id'].convert_dtypes()
        df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected['lane_id_BSSD']=df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected['lane_id_BSSD']\
                                                                                                                                .convert_dtypes()                                                              
        df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected['lane_id_OpenDRIVE']=df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected['lane_id_OpenDRIVE']\
                                                                                                                                .convert_dtypes()
        
        #Check if real result is equal to expected result
        assert_frame_equal(df_link_BSSD_lanes_with_OpenDRIVE_lanes_expected, df_link_BSSD_lanes_with_OpenDRIVE_lanes)
        
    
if __name__ == '__main__':
    unittest.main()
        
        
        