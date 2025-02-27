import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path
from lxml import etree

from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from integrate_BSSD_into_OpenDRIVE.algorithms.A_7_1_extract_speed_attribute import A_7_1_extract_speed_attribute

class TestcaseExtractBehavioralAttributesAutomatically(unittest.TestCase):
    """
    TESTCASE A.07: Tests the function A_7_extract_behavioral_attributes_automatically.py. This includes:
        - Test 1: Checks for every defined BSSD-lane whether the BSSD attribute "speed" is extracted correctly along/against reference direction
                  based on the defined <speed>-Elements in the drivable OpenDRIVE-lanes
            
    """
    
    def test_1_extract_speed_attribute(self):
        """
        Test 1: Checks for every defined BSSD-lane whether the BSSD attribute "speed" is extracted correctly along/against reference direction based
        on the defined <speed>-Elements in the drivable OpenDRIVE-lanes
        
        As input data a xodr-file is used which consists of two roads with a total amount of five segments.
        There are several different cases where the BSSD "speed" attribute is equal along and against driving direction (one way road, separation
        of driving directions) and several cases where the BSSD "speed" attribute against the driving direction is extracted from the other side 
        of the road.
        
        --> see Testcase_A_07_1_scene.png
        
        The test is executed with RHT as well as with LHT. 

        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_07_1'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        
        ##2. df_lane_data
        
        df_lane_data = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #Contains one row per OpenDRIVE-lane
        #list to fill Dataframe
                    #Start of road 0 
                    #laneSection 0.0
        lane_data =[[0,   0.0,  1, 'sidewalk', -1],
                    [0,   0.0, -1, 'driving', -1],
                    [0,   0.0, -2, 'driving', -1],
                    #laneSection 34.58
                    [0, 39.42,  1, 'bidirectional', -1],
                    [0, 39.42,  2, 'sidewalk', -1],
                    [0, 39.42, -1, 'driving', -1],
                    [0, 39.42, -2, 'driving', -1],
                    #laneSection 69.71
                    [0,112.52,  1, 'driving', -1],
                    [0,112.52,  2, 'sidewalk', -1],
                    [0,112.52, -1, 'sidewalk', -1],
                    [0,112.52, -2, 'driving', -1],
                    [0,112.52, -3, 'sidewalk', -1],
                    #Start of road 3
                    #laneSection 0.0
                    [4,   0.0,  1, 'driving', -1],
                    [4,   0.0,  2, 'sidewalk', -1],
                    [4,   0.0, -1, 'driving', -1],
                    [4,   0.0, -2, 'driving', -1],
                    #laneSection 25.12
                    [4, 36.22,  1, 'driving', -1],
                    [4, 36.22, -1, 'driving', -1],
                    [4, 36.22, -2, 'driving', -1]]

    
        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data):
            df_lane_data = df_lane_data.append({'road_id': lane_data[index][0],
                                                'laneSection_s': lane_data[index][1],
                                                'lane_id': lane_data[index][2],
                                                'lane_type': lane_data[index][3],
                                                'junction_id': lane_data[index][4]}, ignore_index=True)
            
        ##3. df_segments        
        df_segments = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        segments =[ [0,   0.0,  None],
                    [0, 39.42,  None],
                    [0,112.52,  None],
                    [4,   0.0,  None],
                    [4, 36.22,  None]]
                                 
        #Paste list with data into DataFrame
        for index, element in enumerate(segments):
            df_segments = df_segments.append({'road_id': segments[index][0],
                                            'segment_s_start': segments[index][1],
                                            'segment_s_end': segments[index][2]},
                                             ignore_index=True)
                
            
        ##4. df_BSSD_lanes
        
        #Get laneSection_objects from imported OpenDRIVE_object
        laneSection_object_0_0_road_0 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[0]
        laneSection_object_39_42 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[1]
        laneSection_object_112_52 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[2]
        
        laneSection_object_0_0_road_4 = OpenDRIVE_object.getRoad(4).lanes.lane_sections[0]
        laneSection_object_36_22 = OpenDRIVE_object.getRoad(4).lanes.lane_sections[1]
        
        df_BSSD_lanes = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_object_s_min'])
        
        #list to fill DataFrame
        #Contains all created BSSD-lanes and the first laneSection overlapping to the segment which contains the BSSD-lane
        
                    #Start of road 0
                    #segment 0.0
        BSSD_lanes=[[0,   0.0, -2,  laneSection_object_0_0_road_0],
                    [0,   0.0, -1,  laneSection_object_0_0_road_0],
                    #segment 39.42
                    [0, 39.42, -2,  laneSection_object_39_42],
                    [0, 39.42, -1,  laneSection_object_39_42],
                    [0, 39.42,  1,  laneSection_object_39_42],
                    #segment 112.52
                    [0,112.52, -2,  laneSection_object_112_52],
                    [0,112.52,  1,  laneSection_object_112_52],
                    #road 4
                    #segment 0.0
                    [4,   0.0, -2,  laneSection_object_0_0_road_4],
                    [4,   0.0, -1,  laneSection_object_0_0_road_4],
                    [4,   0.0,  1,  laneSection_object_0_0_road_4],
                    #segment 36.22
                    [4, 36.22, -2,  laneSection_object_36_22],
                    [4, 36.22, -1,  laneSection_object_36_22],
                    [4, 36.22,  1,  laneSection_object_36_22]]
                
                    
        
        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_lanes):
            df_BSSD_lanes = df_BSSD_lanes.append(
                                                {'road_id': BSSD_lanes[index][0],
                                                'segment_s': BSSD_lanes[index][1],
                                                'lane_id_BSSD': BSSD_lanes[index][2],
                                                'laneSection_object_s_min': BSSD_lanes[index][3]},
                                                 ignore_index=True)
            
            
            
        ##4. df_link_BSSD_lanes_with_OpenDRIVE_lanes

        df_link_BSSD_lanes_with_OpenDRIVE_lanes= pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_s',
                                                                         'lane_id_OpenDRIVE'])
        
        #list to fill DataFrame
        #Contains for every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row 
        
                                                #road 0
                                                #segment 0.0
        link_BSSD_lanes_with_OpenDRIVE_lanes = [[0,   0.0, -2,  0.0, -2],
                                                [0,   0.0, -1,  0.0, -1],
                                                #segment 39.42 
                                                [0, 39.42, -2, 39.42, -2],
                                                [0, 39.42, -1, 39.42, -1],
                                                [0, 39.42,  1, 39.42,  1],
                                                #segment 112.52
                                                [0, 112.52, -2, 112.52, -2],
                                                [0, 112.52,  1, 112.52,  1],
                                                #road 4
                                                #segment 0.0
                                                [4,   0.0, -2, 0.0, -2],
                                                [4,   0.0, -1, 0.0, -1],
                                                [4,   0.0,  1, 0.0,  1],
                                                #segment 36.22
                                                [4, 36.22, -2, 36.22, -2],
                                                [4, 36.22, -1, 36.22, -1],
                                                [4, 36.22,  1, 36.22,  1]]
                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(link_BSSD_lanes_with_OpenDRIVE_lanes):
            df_link_BSSD_lanes_with_OpenDRIVE_lanes = df_link_BSSD_lanes_with_OpenDRIVE_lanes.append(
                                                                {'road_id': link_BSSD_lanes_with_OpenDRIVE_lanes[index][0],
                                                                'segment_s': link_BSSD_lanes_with_OpenDRIVE_lanes[index][1],
                                                                'lane_id_BSSD': link_BSSD_lanes_with_OpenDRIVE_lanes[index][2],
                                                                'laneSection_s': link_BSSD_lanes_with_OpenDRIVE_lanes[index][3],
                                                                'lane_id_OpenDRIVE': link_BSSD_lanes_with_OpenDRIVE_lanes[index][4]},
                                                                 ignore_index=True)
            
            
        ##5. df_speed_limits
        #One row for every <speed>-element in a drivable OpenDRIVE-lane
        
        df_speed_limits = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'sOffset', 'speed_max', 'unit'])
        
        #list to fill DataFrame
        
                        #Start of road 0
                        #segment 0.0
        speed_limits =[ [0,   0.0, -1,  0.0, 50.0, 'km/h'],
                        [0,   0.0, -2,  0.0, 60.0, 'km/h'],
                        #segment 39.42 
                        [0, 39.42,  1,  0.0, 30.0, 'km/h'],
                        [0, 39.42, -1,  0.0, 50.0, 'km/h'],
                        [0, 39.42, -2,  0.0, 60.0, 'km/h'],
                        #segment 112.52
                        [0,112.52,  1,  0.0, 30.0, 'km/h'],
                        [0,112.52, -2,  0.0, 60.0, 'km/h'],
                        #road 4
                        #segment 0.0
                        [4,   0.0, -2,  0.0, 60.0, 'km/h'],
                        #segment 36.22
                        [4, 36.22,  1,  0.0, 30.0, 'km/h'],
                        [4, 36.22, -1,  0.0, 50.0, 'km/h'],
                        [4, 36.22, -2,  0.0, 60.0, 'km/h']]
        
        
        #Paste list with data into DataFrame
        for index, element in enumerate(speed_limits):
            df_speed_limits = df_speed_limits.append({'road_id': speed_limits[index][0],
                                                    'laneSection_s': speed_limits[index][1],
                                                    'lane_id': speed_limits[index][2],
                                                    'sOffset': speed_limits[index][3],
                                                    'speed_max': speed_limits[index][4],
                                                    'unit': speed_limits[index][5]},
                                                     ignore_index=True)
            
        ##6. driving_direction
        driving_direction_RHT = 'RHT'
        driving_direction_LHT = 'LHT'
            
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        #Result for RHT
        df_BSSD_speed_attribute_RHT = A_7_1_extract_speed_attribute(df_lane_data, df_BSSD_lanes, df_link_BSSD_lanes_with_OpenDRIVE_lanes,
                                                                df_speed_limits, df_segments, driving_direction_RHT, OpenDRIVE_object)
        
        #Result for LHT
        df_BSSD_speed_attribute_LHT = A_7_1_extract_speed_attribute(df_lane_data, df_BSSD_lanes, df_link_BSSD_lanes_with_OpenDRIVE_lanes,
                                                                df_speed_limits, df_segments, driving_direction_LHT, OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected result
        
        ##1. df_BSSD_speed_attribute
        
        #1.1 RHT

        df_BSSD_speed_attribute_RHT_expected = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute for every BSSD-lane (behaviorAlong and behaviorAgainst)
        
                                        #road 0
                                        #segment 0.0
        BSSD_speed_attribute_RHT_expected =[[0,   0.0, -2, 60.0, 60.0],
                                            [0,   0.0, -1, 50.0, 50.0],
                                            #segment 39.42 
                                            [0, 39.42, -2, 60.0, 30.0],
                                            [0, 39.42, -1, 50.0, 30.0],
                                            [0, 39.42,  1, 30.0, 30.0],
                                            #segment 112.52
                                            [0, 112.52, -2, 60.0, 60.0],
                                            [0, 112.52,  1, 30.0, 30.0],
                                            #road 4
                                            #segment 0.0
                                            [4,  0.0, -2, 60.0, None],
                                            [4,  0.0, -1, None, None],
                                            [4,  0.0,  1, 60.0, None],
                                            #segment 36.22
                                            [4, 36.22, -2, 60.0, 60.0],
                                            [4, 36.22, -1, 50.0, 30.0],
                                            [4, 36.22,  1, 50.0, 30.0]]
                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_RHT_expected):
            df_BSSD_speed_attribute_RHT_expected = df_BSSD_speed_attribute_RHT_expected.append(
                                                                {'road_id': BSSD_speed_attribute_RHT_expected[index][0],
                                                                'segment_s': BSSD_speed_attribute_RHT_expected[index][1],
                                                                'lane_id_BSSD': BSSD_speed_attribute_RHT_expected[index][2],
                                                                'speed_behavior_along': BSSD_speed_attribute_RHT_expected[index][3],
                                                                'speed_behavior_against': BSSD_speed_attribute_RHT_expected[index][4]},
                                                                 ignore_index=True)
            
        #Convert values in columns "road_id", "lane_id_BSSD" to int 
        df_BSSD_speed_attribute_RHT_expected['road_id']=df_BSSD_speed_attribute_RHT_expected['road_id'].convert_dtypes()
        df_BSSD_speed_attribute_RHT_expected['lane_id_BSSD']=df_BSSD_speed_attribute_RHT_expected['lane_id_BSSD'].convert_dtypes()
        
        #1.2 LHT

        df_BSSD_speed_attribute_LHT_expected = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'speed_behavior_along',
                                                                       'speed_behavior_against'])
        
        #list to fill DataFrame
        #Contains the BSSD speed-attribute (behaviorAlong and behaviorAgainst)
        
                                            #road 0
                                            #segment 0.0
        BSSD_speed_attribute_LHT_expected =[[0,   0.0, -2, 60.0, 60.0],
                                            [0,   0.0, -1, 50.0, 50.0],
                                            #segment 39.42 
                                            [0, 39.42, -2, 30.0, 60.0],
                                            [0, 39.42, -1, 30.0, 50.0],
                                            [0, 39.42,  1, 30.0, 30.0],
                                            #segment 112.52
                                            [0, 112.52, -2, 60.0, 60.0],
                                            [0, 112.52,  1, 30.0, 30.0],
                                            #road 4
                                            #segment 0.0
                                            [4,   0.0, -2, None, 60.0],
                                            [4,   0.0, -1, None, None],
                                            [4,   0.0,  1, None, 60.0],
                                            #segment 36.22
                                            [4, 36.22, -2, 60.0, 60.0],
                                            [4, 36.22, -1, 30.0, 50.0],
                                            [4, 36.22,  1, 30.0, 50.0]]
                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_speed_attribute_LHT_expected):
            df_BSSD_speed_attribute_LHT_expected = df_BSSD_speed_attribute_LHT_expected.append(
                                                                {'road_id': BSSD_speed_attribute_LHT_expected[index][0],
                                                                'segment_s': BSSD_speed_attribute_LHT_expected[index][1],
                                                                'lane_id_BSSD': BSSD_speed_attribute_LHT_expected[index][2],
                                                                'speed_behavior_along': BSSD_speed_attribute_LHT_expected[index][3],
                                                                'speed_behavior_against': BSSD_speed_attribute_LHT_expected[index][4]},
                                                                 ignore_index=True)
            
        #Convert values in columns "road_id", "lane_id_BSSD" to int 
        df_BSSD_speed_attribute_LHT_expected['road_id']=df_BSSD_speed_attribute_LHT_expected['road_id'].convert_dtypes()
        df_BSSD_speed_attribute_LHT_expected['lane_id_BSSD']=df_BSSD_speed_attribute_LHT_expected['lane_id_BSSD'].convert_dtypes()
        
        
        
        #Check if real result is equal to expected result
        assert_frame_equal(df_BSSD_speed_attribute_RHT_expected, df_BSSD_speed_attribute_RHT)
        assert_frame_equal(df_BSSD_speed_attribute_LHT_expected, df_BSSD_speed_attribute_LHT)
    
if __name__ == '__main__':
    unittest.main()
        
        
        