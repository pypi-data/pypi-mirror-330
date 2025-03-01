import unittest
from pathlib import Path
from lxml import etree
import pandas as pd
from pandas.testing import assert_frame_equal

from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from integrate_BSSD_into_OpenDRIVE.algorithms.A_1_find_drivable_lanes import A_1_find_drivable_lanes


class TestcaseFindDrivableLanes(unittest.TestCase):
    """
    TESTCASE A.01: Tests the function A_1_find_drivable_lanes.py. This includes:
        - Test 1: Check whether <lane>-elements of imported xodr-file are grouped correctly into drivable and not drivable lanes
        (depending on attribute "type" of <lane>-element and depending on neighbour lanes in case of type="biking")
        - Test 2: Check whether <lane>-elements with type-attribute "biking" are grouped correctly into drivable and not drivable lanes
        depending on neighbour lanes --> A biking lane is considered as drivable if at least one of the neighbour lanes (if existing) is drivable.
        
    """
    
    def test_1_search_drivable_lanes(self):
        """
        Test 1: Check whether <lane>-elements of imported xodr-file are grouped correctly into drivable and not drivable lanes
        (depending on attribute "type" of <lane>-element and depending on neighbour lanes in case of type="biking").
        
        The imported xodr file contains lanes of every possible lane-type (OpenDRIVE 1.7) in different roads and different lane sections
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_01_1'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_lane_data, df_lane_data_drivable_lanes, df_lane_data_not_drivable_lanes = A_1_find_drivable_lanes(OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. df_lane_data
        
        df_lane_data_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                              #Start of road 0
                              #laneSection 0.0
        lane_data_expected = [[0,   0.0,  1,        'driving', -1],
                              [0,   0.0,  2,           'exit', -1],
                              [0,   0.0,  3,        'offRamp', -1],
                              [0,   0.0,  4,         'onRamp', -1],
                              [0,   0.0,  5,         'biking', -1],
                              [0,   0.0,  6,           'none', -1],
                              [0,   0.0, -1,        'driving', -1],
                              [0,   0.0, -2,           'tram', -1],
                              [0,   0.0, -3,           'rail', -1],
                              [0,   0.0, -4,          'entry', -1],
                              #laneSection 20.15
                              [0, 20.15,  1,        'driving', -1],
                              [0, 20.15,  2,            'bus', -1],
                              [0, 20.15,  3,  'bidirectional', -1],
                              [0, 20.15,  4, 'connectingRamp', -1],
                              [0, 20.15,  5,         'median', -1],
                              [0, 20.15, -1,        'mwyExit', -1],
                              [0, 20.15, -2,           'taxi', -1],
                              [0, 20.15, -3,            'HOV', -1],
                              [0, 20.15, -4,       'mwyEntry', -1],
                              #Start of road 2
                              #laneSection 0.0
                              [2,   0.0,  1,        'driving', -1],
                              [2,   0.0,  2,         'border', -1],
                              [2,   0.0,  3,     'restricted', -1],
                              [2,   0.0,  4,        'parking', -1],
                              [2,   0.0,  5,           'stop', -1],
                              [2,   0.0,  6,      'roadWorks', -1],
                              [2,   0.0, -1,        'driving', -1],
                              [2,   0.0, -2,       'shoulder', -1],
                              [2,   0.0, -3,           'curb', -1],
                              [2,   0.0, -4,       'sidewalk', -1]]
    
        
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
                                             #Start of road 0
                                             #laneSection 0.0
        lane_data_drivable_lanes_expected =[[0,   0.0,  1,        'driving', -1],
                                            [0,   0.0,  2,           'exit', -1],
                                            [0,   0.0,  3,        'offRamp', -1],
                                            [0,   0.0,  4,         'onRamp', -1],
                                            [0,   0.0,  5,         'biking', -1],
                                            [0,   0.0, -1,        'driving', -1],
                                            [0,   0.0, -2,           'tram', -1],
                                            [0,   0.0, -3,           'rail', -1],
                                            [0,   0.0, -4,          'entry', -1],
                                            #laneSection 20.15
                                            [0, 20.15,  1,        'driving', -1],
                                            [0, 20.15,  2,            'bus', -1],
                                            [0, 20.15,  3,  'bidirectional', -1],
                                            [0, 20.15,  4, 'connectingRamp', -1],
                                            [0, 20.15, -1,        'mwyExit', -1],
                                            [0, 20.15, -2,           'taxi', -1],
                                            [0, 20.15, -3,            'HOV', -1],
                                            [0, 20.15, -4,       'mwyEntry', -1],
                                            #Start of road 2
                                            #laneSection 0.0
                                            [2,   0.0,  1,        'driving', -1],
                                            [2,   0.0,  2,         'border', -1],
                                            [2,   0.0,  3,     'restricted', -1],
                                            [2,   0.0,  4,        'parking', -1],
                                            [2,   0.0,  5,           'stop', -1],
                                            [2,   0.0,  6,      'roadWorks', -1],
                                            [2,   0.0, -1,        'driving', -1]]
                                            
        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes_expected):
            df_lane_data_drivable_lanes_expected = df_lane_data_drivable_lanes_expected.append(
                                                                                    {'road_id': lane_data_drivable_lanes_expected[index][0],
                                                                                    'laneSection_s': lane_data_drivable_lanes_expected[index][1],
                                                                                    'lane_id': lane_data_drivable_lanes_expected[index][2],
                                                                                    'lane_type': lane_data_drivable_lanes_expected[index][3],
                                                                                    'junction_id': lane_data_drivable_lanes_expected[index][4]},
                                                                                     ignore_index=True)

       
        
        ##3. df_lane_data_not_drivable_lanes
                
        df_lane_data_not_drivable_lanes_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                                                  #Start of Road 0
                                                  #laneSection 0.0
        lane_data_not_drivable_lanes_expected =  [[0,   0.0,  6,           'none', -1],
                                                  #laneSection 20.15
                                                  [0, 20.15,  5,         'median', -1],
                                                  #Start of Road 2
                                                  #laneSection 0.0
                                                  [2,   0.0, -2,       'shoulder', -1],
                                                  [2,   0.0, -3,           'curb', -1],
                                                  [2,   0.0, -4,       'sidewalk', -1]]
                                                  
    
        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_not_drivable_lanes_expected):
            df_lane_data_not_drivable_lanes_expected = df_lane_data_not_drivable_lanes_expected.append(
                                                                                {'road_id': lane_data_not_drivable_lanes_expected[index][0],
                                                                                 'laneSection_s': lane_data_not_drivable_lanes_expected[index][1],
                                                                                  'lane_id': lane_data_not_drivable_lanes_expected[index][2],
                                                                                  'lane_type': lane_data_not_drivable_lanes_expected[index][3],
                                                                                  'junction_id': lane_data_not_drivable_lanes_expected[index][4]},
                                                                                  ignore_index=True)


        #Check if real result is equal to expected result
        assert_frame_equal(df_lane_data_expected, df_lane_data)
        assert_frame_equal(df_lane_data_drivable_lanes_expected, df_lane_data_drivable_lanes)
        assert_frame_equal(df_lane_data_not_drivable_lanes_expected, df_lane_data_not_drivable_lanes)
        
    def test_2_search_drivable_biking_lanes(self):
        """
        Test 2: Check whether <lane>-elements with type-attribute "biking" are grouped correctly into drivable and not drivable lanes
        depending on neighbour lanes --> A biking lane is considered as drivable if at least one of the neighbour lanes (if existing) is drivable.
        
        The imported xodr file contains drivable and not drivable biking lanes --> see Testcase_A_01_2_scene.png
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_01_2'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_lane_data, df_lane_data_drivable_lanes, df_lane_data_not_drivable_lanes = A_1_find_drivable_lanes(OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. df_lane_data
        
        df_lane_data_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                              #Start of road 0
                              #laneSection 0.0
        lane_data_expected = [[0,   0.0,  1,        'driving', -1],
                              [0,   0.0,  2,         'biking', -1],
                              [0,   0.0, -1,        'driving', -1],
                              [0,   0.0, -2,       'sidewalk', -1],
                              [0,   0.0, -3,         'biking', -1],
                              [0,   0.0, -4,       'sidewalk', -1],
                              #Start of road 1
                              #laneSection 0.0
                              [1,   0.0,  1,        'driving', -1],
                              [1,   0.0, -1,         'biking', -1]]
    
        
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
                                              #Start of road 0
                                              #laneSection 0.0
        lane_data_drivable_lanes_expected =[  [0,   0.0,  1,        'driving', -1],
                                              #lane 2 is drivable as neighbour lane 1 is drivable
                                              [0,   0.0,  2,         'biking', -1],
                                              [0,   0.0, -1,        'driving', -1],
                                              #Start of road 1
                                              #laneSection 0.0
                                              [1,   0.0,  1,        'driving', -1],
                                              #lane -1 is drivable as neighbour-lane 1 is drivable
                                              [1,   0.0, -1,         'biking', -1]]
        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes_expected):
            df_lane_data_drivable_lanes_expected = df_lane_data_drivable_lanes_expected.append(
                                                                                    {'road_id': lane_data_drivable_lanes_expected[index][0],
                                                                                    'laneSection_s': lane_data_drivable_lanes_expected[index][1],
                                                                                    'lane_id': lane_data_drivable_lanes_expected[index][2],
                                                                                    'lane_type': lane_data_drivable_lanes_expected[index][3],
                                                                                    'junction_id': lane_data_drivable_lanes_expected[index][4]},
                                                                                     ignore_index=True)

       
        
        ##3. df_lane_data_not_drivable_lanes
                
        df_lane_data_not_drivable_lanes_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                                                  #Start of Road 0
                                                  #laneSection 0.0
        lane_data_not_drivable_lanes_expected =  [[0,   0.0, -2,       'sidewalk', -1],
                                                  #lane -3 is not drivable as neighbour lanes -2 and -4 are not drivable
                                                  [0,   0.0, -3,         'biking', -1],
                                                  [0,   0.0, -4,       'sidewalk', -1]]

    
        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_not_drivable_lanes_expected):
            df_lane_data_not_drivable_lanes_expected = df_lane_data_not_drivable_lanes_expected.append(
                                                                                {'road_id': lane_data_not_drivable_lanes_expected[index][0],
                                                                                 'laneSection_s': lane_data_not_drivable_lanes_expected[index][1],
                                                                                  'lane_id': lane_data_not_drivable_lanes_expected[index][2],
                                                                                  'lane_type': lane_data_not_drivable_lanes_expected[index][3],
                                                                                  'junction_id': lane_data_not_drivable_lanes_expected[index][4]},
                                                                                  ignore_index=True)


        #Check if real result is equal to expected result
        assert_frame_equal(df_lane_data_expected, df_lane_data)
        assert_frame_equal(df_lane_data_drivable_lanes_expected, df_lane_data_drivable_lanes)
        assert_frame_equal(df_lane_data_not_drivable_lanes_expected, df_lane_data_not_drivable_lanes)
        
    
if __name__ == '__main__':
    unittest.main()
        
        
        