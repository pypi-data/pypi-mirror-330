import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path
from lxml import etree
from unittest import mock

from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_extract_segments_automatically import A_3_extract_segments_automatically
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_1_segments_by_changing_number_of_drivable_lanes import A_3_1_segments_by_changing_number_of_drivable_lanes
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_2_segments_by_starting_and_ending_drivable_lanes import A_3_2_segments_by_starting_and_ending_drivable_lanes
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_3_segments_by_speed_limit import A_3_3_segments_by_speed_limit
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_4_segments_by_static_signals import A_3_4_segments_by_static_signals
from integrate_BSSD_into_OpenDRIVE.algorithms.A_3_5_segments_by_dynamic_signals import A_3_5_segments_by_dynamic_signals

class TestcaseExtractSegmentsAutomatically(unittest.TestCase):
    """
    TESTCASE A.03: Tests the function A_3_extract_segments_automatically.py. This includes:
        - Test 1: Checks whether BSSD-segments are extracted correctly based on rule 1: A new segment has to be defined when the total number 
          of drivable lanes changes from one laneSection to the next laneSection
              --> Executing subfunction A_3_1_segments_by_changing_number_of_drivable_lanes.py
        - Test 2: Checks whether BSSD-segments are extracted correctly based on rule 2: A new segment has to be defined when a drivable lane
          starts/ends and a preceding/succeeding lane section is existing
              --> Test 2 Consists of three tests with three different scenes which test subfunctionalities of rule 2
              --> Executing subfunction A_3_2_segments_by_starting_and_ending_drivable_lanes.py
        - Test 3: Checks whether BSSD-segments are extracted correctly based on rule 3: If the speed limit for a drivable lane
          changes, a new segment has to be defined
              --> Executing subfunction A_3_3_segments_by_speed_limit.py
        - Test 4: Checks whether BSSD-segments are extracted correctly based on rule 4: If there is a traffic sign or a road-marking,
          which affects a BSSD behavioral attribute, a new segment is defined
              --> Test 4 consists of two tests which represent the same test but with different user-inputs ("y" and "n")
              --> Executing subfunction A_3_4_segments_by_static_signals.py
        - Test 5: Checks whether BSSD-segments are extracted correctly based on rule 5:
            If there is a traffic light or another dynamic signal, a new segment is defined
            --> Executing subfunction A_3_5_segments_by_dynamic_signals.py
        - Test 6: Checks whether BSSD-segments are extracted correctly based on all rules for extracting new segments
              --> Executing overall function A_3_extract_segments_automatically.py
    """
    
        
    def test_1_extract_segments_automatically_rule_1(self):
        """
        Test 1: Checks whether BSSD-segments are extracted correctly based on rule 1: A new segment has to be defined when the total number 
          of drivable lanes changes from one lane section to the next lane section
                        
        As input data a xodr-file is used which covers the following scenarios:
            - Change in number of drivable lanes from one laneSection to succeeding laneSection
            - No change in number of drivable lanes from one laneSection to succeeding laneSection
            - No drivable lanes in a suceeding laneSection
            - No drivable lanes in two preceding laneSection
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_lane_data
        
        df_lane_data = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
    
                    #Start of road 0
                    #laneSection 0.0
                    #New road with two laneSections
        lane_data =[[0,    0.0,   1, 'driving', -1],
                    [0,    0.0,   2,  'sidewalk', -1],
                    [0,    0.0,  -1, 'driving', -1],
                    [0,    0.0,  -2,  'sidewalk', -1],
                    #laneSection 40.21
                    #Change to a laneSection with additional lane, which is not-drivable --> No new segment necessary
                    [0,  40.21,   1, 'driving', -1],
                    [0,  40.21,   2, 'sidewalk', -1],
                    [0,  40.21,  -1, 'driving', -1],
                    [0,  40.21,  -2, 'sidewalk', -1],
                    [0,  40.21,  -3, 'sidewalk', -1],
                    #Start of road 2
                    #laneSection 0.0
                    [2,    0.0,   1, 'driving', -1],
                    [2,    0.0,   2,  'sidewalk', -1],
                    [2,    0.0,  -1, 'driving', -1],
                    [2,    0.0,  -2,  'sidewalk', -1],
                    #laneSection 31.35
                    #Reduction of number of drivable lanes by one --> New segment necessary
                    [2,  31.35,   1, 'driving', -1],
                    [2,  31.35,   2, 'sidewalk', -1],
                    [2,  31.35,  -1,  'sidewalk', -1],
                    #laneSection 54.52
                    #Change to a laneSection with no drivable lane --> s_end of segment has to be defined
                    [2,  54.52,   1, 'sidewalk', -1],
                    [2,  54.52,  -1, 'sidewalk', -1],
                    #laneSection 61.0
                    #laneSection with no drivable lane 
                    [2,  60.0,   1, 'sidewalk', -1],
                    [2,  60.0,  -1, 'sidewalk', -1],
                    [2,  60.0,  -2, 'sidewalk', -1],
                    #laneSection 80.47
                    #laneSection with one drivable lane --> Check if new segment is defined although number of drivable lanes of previous 
                    #laneSection with drivable lanes (31.35) has also one drivable lane
                    [2,  80.47,   1, 'sidewalk', -1],
                    [2,  80.47,  -1, 'driving', -1]]
    
        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data):
            df_lane_data = df_lane_data.append({'road_id': lane_data[index][0],
                                                'laneSection_s': lane_data[index][1],
                                                'lane_id': lane_data[index][2],
                                                'lane_type': lane_data[index][3],
                                                'junction_id': lane_data[index][4]}, ignore_index=True)
          
        ##2. df_lane_data_drivable_lanes
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
        #Contains all drivable lanes of lane_data
        
                                    #Start of road 0
                                    #laneSection 0.0
                                    #New road with two laneSections
        lane_data_drivable_lanes =[ [0,    0.0,   1, 'driving', -1],
                                    [0,    0.0,  -1, 'driving', -1],
                                    #laneSection 40.21
                                    #Change to a laneSection with additional lane, which is not-drivable
                                    [0,  40.21,   1, 'driving', -1],
                                    [0,  40.21,  -1, 'driving', -1],
                                    #Start of road 2
                                    #laneSection 0.0
                                    [2,    0.0,   1, 'driving', -1],
                                    [2,    0.0,  -1, 'driving', -1],
                                    #laneSection 31.35
                                    #Reduction of number of drivable lanes by one
                                    [2,  31.35,   1, 'driving', -1],
                                    #laneSection 80.47
                                    #laneSection with one drivable lane --> Check if new segment is defined although number of drivable lanes of previous 
                                    #laneSection with drivable lanes (31.35) has also one drivable lane
                                    [2,  80.47,  -1, 'driving', -1]]
    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_segments_automatic, roads_laneSections_equal_segments = A_3_1_segments_by_changing_number_of_drivable_lanes(df_lane_data,
                                                                                                        df_lane_data_drivable_lanes)
                                                                                                                       
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. df_segments_automatic
        
        df_segments_automatic_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments which should be created based on input df_lane_data
                                       #Start of road 0
                                       #Has only one segment as number of drivable lanes is constant
        segments_automatic_expected = [[0,   0.0,  None],
                                       #Start of road 2
                                       [2,   0.0,  None],
                                       #Segment 31.35 due to change in number of drivable lane
                                       #s_end = 54.52 due to a laneSection at 54.52 which has no drivable lanes
                                       [2, 31.35, 54.52],
                                       #Segment 80.47 due to lane section which has drivable lanes
                                       [2, 80.47,  None]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic_expected):
            df_segments_automatic_expected = df_segments_automatic_expected.append({'road_id': segments_automatic_expected[index][0],
                                                                                    'segment_s_start': segments_automatic_expected[index][1],
                                                                                    'segment_s_end': segments_automatic_expected[index][2]},
                                                                                     ignore_index=True)
        #Convert values in column "road_id" to int 
        df_segments_automatic_expected['road_id']=df_segments_automatic_expected['road_id'].convert_dtypes()
        
        ##2. roads_laneSections_equal_segments
        
        #List is empty as there is no road where every laneSection lead to the definition of a segment
        roads_laneSections_equal_segments_expected = []
        
        #Check if real result is equal to expected result
        assert_frame_equal(df_segments_automatic_expected, df_segments_automatic)
        self.assertListEqual(roads_laneSections_equal_segments_expected, roads_laneSections_equal_segments)
        
    def test_2_extract_segments_automatically_rule_2_scene_1(self):
        """
        Test 2: Checks whether BSSD-segments are extracted correctly based on rule 2: A new segment has to be defined when a drivable lane
                starts/ends and a preceding/succeeding lane section is existing
                
        Scene 1: Three laneSections with three drivable lanes each. In the laneSection in the middle one drivable lanes starts & one drivable 
        lane ends --> Extraction of two new segments necessary (rule 2) as rule 1 is not fulfilled (the number of drivable lanes doesn't change in
                                                                                                    in the laneSections)
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_03_2_scene_1'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.6', filename_xodr +'.xodr')

        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        ##2. df_lane_data
        df_lane_data = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe

                    #Start of road 0
                    #laneSection 0.0 (3 drivable lanes)
        lane_data =[[1,    0.0,   1, 'driving', -1],
                    [1,    0.0,   2, 'driving', -1],
                    [1,    0.0,   3, 'sidewalk', -1],
                    [1,    0.0,  -1, 'driving', -1],
                    [1,    0.0,  -2, 'sidewalk', -1],
                    #laneSection 25.0 (3 drivable lanes), includes one lane which starts at the beginning of this laneSection (leads to a
                    #segment at 25.0) and one lane which ends at the end of this lane section (leads to a segment at 75.0 --> succeeding laneSection)
                    [1,   25.0,   1, 'driving', -1],
                    [1,   25.0,   2, 'sidewalk', -1],
                    [1,   25.0,   3, 'sidewalk', -1],
                    [1,   25.0,  -1, 'driving', -1],
                    [1,   25.0,  -2, 'driving', -1],
                    [1,   25.0,  -3, 'sidewalk', -1],
                    #laneSection 75.0 (3 drivable lanes)
                    [1,   75.0,   1, 'driving', -1],
                    [1,   75.0,   2, 'sidewalk', -1],
                    [1,   75.0,  -1, 'driving', -1],
                    [1,   75.0,  -2, 'driving', -1],
                    [1,   75.0,  -3, 'sidewalk', -1]]

        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data):
            df_lane_data = df_lane_data.append({'road_id': lane_data[index][0],
                                                'laneSection_s': lane_data[index][1],
                                                'lane_id': lane_data[index][2],
                                                'lane_type': lane_data[index][3],
                                                'junction_id': lane_data[index][4]}, ignore_index=True)
          
        ##3. df_lane_data_drivable_lanes
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
        #Contains all drivable lanes of lane_data
        
                                    #Start of road 0
                                    #laneSection 0.0 (3 drivable lanes)
        lane_data_drivable_lanes =[ [1,    0.0,   1, 'driving', -1],
                                    [1,    0.0,   2, 'driving', -1],
                                    [1,    0.0,  -1, 'driving', -1],
                                    #laneSection 25.0 (3 drivable lanes)
                                    [1,   25.0,   1, 'driving', -1],
                                    [1,   25.0,  -1, 'driving', -1],
                                    [1,   25.0,  -2, 'driving', -1],
                                    #laneSection 75.0 (3 drivable lanes)
                                    [1,   75.0,   1, 'driving', -1],
                                    [1,   75.0,  -1, 'driving', -1],
                                    [1,   75.0,  -2, 'driving', -1]]

        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
            
        ##4. df_segments_automatic
        
        df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments which should be created based on rule 1
                              #Start of road 0
                              #Segment 0.0 --> Based on first laneSection in the road with a drivable lane
        segments_automatic = [[1,   0.0,  None]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic):
            df_segments_automatic = df_segments_automatic.append({'road_id': segments_automatic[index][0],
                                                                'segment_s_start': segments_automatic[index][1],
                                                                'segment_s_end': segments_automatic[index][2]},
                                                                 ignore_index=True)
        
        ##5. roads_laneSections_equal_segments
        
        #List is empty as there is no road where every laneSection lead to the definition of a segment
        roads_laneSections_equal_segments = []
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_segments_automatic = A_3_2_segments_by_starting_and_ending_drivable_lanes(df_lane_data, df_lane_data_drivable_lanes,
                                                                                     df_segments_automatic, roads_laneSections_equal_segments,
                                                                                     OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. df_segments_automatic
        
        df_segments_automatic_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments which should be created based on input df_lane_data
                                       #Start of road 0
                                       #Segment 0.0
        segments_automatic_expected = [[1,   0.0,  None],
                                       #Segment 25.0, due to drivable lane starting in laneSection 25.0
                                       [1,  25.0,  None],
                                       #Segment 75.0, due to drivable lane ending in preceding laneSection 25.0
                                       [1,  75.0,  None]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic_expected):
            df_segments_automatic_expected = df_segments_automatic_expected.append({'road_id': segments_automatic_expected[index][0],
                                                                                    'segment_s_start': segments_automatic_expected[index][1],
                                                                                    'segment_s_end': segments_automatic_expected[index][2]},
                                                                                     ignore_index=True)
            
        #Convert values in column "road_id" to int 
        df_segments_automatic_expected['road_id']=df_segments_automatic_expected['road_id'].convert_dtypes()

        #Check if real result is equal to expected result
        assert_frame_equal(df_segments_automatic_expected, df_segments_automatic)
       
    def test_2_extract_segments_automatically_rule_2_scene_2(self):
        """
        Test 2: Checks whether BSSD-segments are extracted correctly based on rule 2: A new segment has to be defined when a drivable lane
                starts/ends and a preceding/succeeding lane section is existing
                
        Scene 2: Contains three laneSections. Two laneSections with three drivable lanes each. The laneSection in the middle has
        four drivable lanes. In the laneSection in the middle one drivable lanes starts & one drivable lane ends 
        
        --> Extraction of two new segments based on rule 2 not necessary (although one drivable lanes starts & one drivable 
        lane ends in the middle laneSection) as rule 1 already fulfilled (the number of drivable lanes changes between the laneSections)
        --> Check whether segments are not created twice, because both rules are fulfilled
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object 
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_03_2_scene_2'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.6', filename_xodr +'.xodr')

        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        ##2. df_lane_data
        df_lane_data = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe

                    #Start of road 0
                    #laneSection 0.0 (3 drivable lanes)
        lane_data =[[1,    0.0,   1, 'driving', -1],
                    [1,    0.0,   2, 'driving', -1],
                    [1,    0.0,   3, 'sidewalk', -1],
                    [1,    0.0,  -1, 'driving', -1],
                    [1,    0.0,  -2, 'sidewalk', -1],
                    #laneSection 25.0 (4 drivable lanes), includes one lane which starts at the beginning of this laneSection (leads to a
                    #segment at 25.0) and one lane which ends at the end of this lane section (leads to a segment at 75.0 --> succeeding laneSection)
                    [1,   25.0,   1, 'driving', -1],
                    [1,   25.0,   2, 'driving', -1],
                    [1,   25.0,   3, 'sidewalk', -1],
                    [1,   25.0,  -1, 'driving', -1],
                    [1,   25.0,  -2, 'driving', -1],
                    [1,   25.0,  -3, 'sidewalk', -1],
                    #laneSection 75.0 (3 drivable lanes)
                    [1,   75.0,   1, 'driving', -1],
                    [1,   75.0,   2, 'sidewalk', -1],
                    [1,   75.0,  -1, 'driving', -1],
                    [1,   75.0,  -2, 'driving', -1],
                    [1,   75.0,  -3, 'sidewalk', -1]]

        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data):
            df_lane_data = df_lane_data.append({'road_id': lane_data[index][0],
                                                'laneSection_s': lane_data[index][1],
                                                'lane_id': lane_data[index][2],
                                                'lane_type': lane_data[index][3],
                                                'junction_id': lane_data[index][4]}, ignore_index=True)
          
        ##3. df_lane_data_drivable_lanes
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
        #Contains all drivable lanes of lane_data
        
                                    #Start of road 0
                                    #laneSection 0.0 (3 drivable lanes)
        lane_data_drivable_lanes =[ [1,    0.0,   1, 'driving', -1],
                                    [1,    0.0,   2, 'driving', -1],
                                    [1,    0.0,  -1, 'driving', -1],
                                    #laneSection 25.0 (4 drivable lanes)
                                    [1,   25.0,   1, 'driving', -1],
                                    [1,   25.0,   2, 'driving', -1],
                                    [1,   25.0,  -1, 'driving', -1],
                                    [1,   25.0,  -2, 'driving', -1],
                                    #laneSection 75.0 (3 drivable lanes)
                                    [1,   75.0,   1, 'driving', -1],
                                    [1,   75.0,  -1, 'driving', -1],
                                    [1,   75.0,  -2, 'driving', -1]]

        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
            
        ##4. df_segments_automatic
        
        df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments created based on rule 1
        
                            #Start of road 0
                            #Segment 0.0
        segments_automatic= [[1,   0.0,  None],
                            #Segment 25.0, due to change in number of drivable lanes (rule 1)
                            [1,  25.0,  None],
                            #Segment 75.0, due to change in number of drivable lanes (rule 1)
                            [1,  75.0,  None]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic):
            df_segments_automatic = df_segments_automatic.append({'road_id': segments_automatic[index][0],
                                                                'segment_s_start': segments_automatic[index][1],
                                                                'segment_s_end': segments_automatic[index][2]},
                                                                 ignore_index=True)
        
        ##5. roads_laneSections_equal_segments
        
        #List contains road 1 as all laneSections in this road lead to the definition of a segment
        roads_laneSections_equal_segments = [1]
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_segments_automatic = A_3_2_segments_by_starting_and_ending_drivable_lanes(df_lane_data, df_lane_data_drivable_lanes,
                                                                                     df_segments_automatic, roads_laneSections_equal_segments,
                                                                                     OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. df_segments_automatic
        
        df_segments_automatic_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments which should be created based on rule 2
        #--> Equal to input as already all possible segments were extracted by rule 1
                                       #Start of road 0
                                       #Segment 0.0
        segments_automatic_expected = [[1,   0.0,  None],
                                       #Segment 25.0, due to change in number of drivable lanes from laneSection 0.0 (rule 1)
                                       [1,  25.0,  None],
                                       #Segment 25.0, due to change in number of drivable lanes from laneSection 25.0 (rule 1)
                                       [1,  75.0,  None]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic_expected):
            df_segments_automatic_expected = df_segments_automatic_expected.append({'road_id': segments_automatic_expected[index][0],
                                                                                    'segment_s_start': segments_automatic_expected[index][1],
                                                                                    'segment_s_end': segments_automatic_expected[index][2]},
                                                                                     ignore_index=True)
        #Convert values in column "road_id" to int 
        df_segments_automatic_expected['road_id']=df_segments_automatic_expected['road_id'].convert_dtypes()
        

        #Check if real result is equal to expected result
        assert_frame_equal(df_segments_automatic_expected, df_segments_automatic)
        
    def test_2_extract_segments_automatically_rule_2_scene_3(self):
        """
        Test 2: Checks whether BSSD-segments are extracted correctly based on rule 2: A new segment has to be defined when a drivable lane
                starts/ends and a preceding/succeeding lane section is existing
                
        Scene 3: Three laneSections. The first two laneSections have three drivable lanes each. The last laneSection has no drivable lane.
        In the laneSection in the middle one drivable lanes starts & one drivable lane ends
        --> Extraction of one segment by rule 1 as the number of drivable lanes changes from middle to last laneSection
        --> Extraction of one segment by rule 2 as one drivable lane starts in the laneSection in the middle
        
        --> It is checked whether s_end-coordinate of the second segment is extracted correctly based on the laneSection with
        no drivable lanes --> Both Rules define this s_end-coordinate (Rule 1 & Rule 2) --> Checked whether not defined twice
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_03_2_scene_3'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.6', filename_xodr +'.xodr')

        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        ##2. df_lane_data
        df_lane_data = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe

                    #Start of road 0
                    #laneSection 0.0 (3 drivable lanes)
        lane_data =[[1,    0.0,   1, 'driving', -1],
                    [1,    0.0,   2, 'driving', -1],
                    [1,    0.0,   3, 'sidewalk', -1],
                    [1,    0.0,  -1, 'driving', -1],
                    [1,    0.0,  -2, 'sidewalk', -1],
                    #laneSection 25.0 (3 drivable lanes), includes one lane which starts at the beginning of this laneSection (leads to a
                    #segment at 25.0). Includes also one lane which ends at the end of this laneSection --> Doesn't lead to a new segment as 
                    #succeeding laneSection has no drivable lanes
                    [1,   25.0,   1, 'driving', -1],
                    [1,   25.0,   2, 'sidewalk', -1],
                    [1,   25.0,   3, 'sidewalk', -1],
                    [1,   25.0,  -1, 'driving', -1],
                    [1,   25.0,  -2, 'driving', -1],
                    [1,   25.0,  -3, 'sidewalk', -1],
                    #laneSection 75.0 (0 drivable lanes)
                    [1,   75.0,   1, 'sidewalk', -1],
                    [1,   75.0,   2, 'sidewalk', -1],
                    [1,   75.0,  -1, 'sidewalk', -1],
                    [1,   75.0,  -2, 'sidewalk', -1],
                    [1,   75.0,  -3, 'sidewalk', -1]]

        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data):
            df_lane_data = df_lane_data.append({'road_id': lane_data[index][0],
                                                'laneSection_s': lane_data[index][1],
                                                'lane_id': lane_data[index][2],
                                                'lane_type': lane_data[index][3],
                                                'junction_id': lane_data[index][4]}, ignore_index=True)
          
        ##3. df_lane_data_drivable_lanes
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
        #Contains all drivable lanes of lane_data
        
                                    #Start of road 0
                                    #laneSection 0.0 (3 drivable lanes)
        lane_data_drivable_lanes =[ [1,    0.0,   1, 'driving', -1],
                                    [1,    0.0,   2, 'driving', -1],
                                    [1,    0.0,  -1, 'driving', -1],
                                    #laneSection 25.0 (3 drivable lanes)
                                    [1,   25.0,   1, 'driving', -1],
                                    [1,   25.0,  -1, 'driving', -1],
                                    [1,   25.0,  -2, 'driving', -1]]

        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
            
        
        ##4. df_segments_automatic
        
        df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments created based on rule 1
        
                            #Start of road 0
                            #Segment 0.0 --> Has a defined end at s=75.0 as there is a laneSection with no drivable lanes
        segments_automatic= [[1,   0.0,  75.0]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic):
            df_segments_automatic = df_segments_automatic.append({'road_id': segments_automatic[index][0],
                                                                'segment_s_start': segments_automatic[index][1],
                                                                'segment_s_end': segments_automatic[index][2]},
                                                                 ignore_index=True)
        
        ##5. roads_laneSections_equal_segments
        
        #List is empty as there is no road where every laneSection lead to the definition of a segment
        roads_laneSections_equal_segments = []
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_segments_automatic = A_3_2_segments_by_starting_and_ending_drivable_lanes(df_lane_data, df_lane_data_drivable_lanes,
                                                                                     df_segments_automatic, roads_laneSections_equal_segments,
                                                                                     OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. df_segments_automatic
        
        df_segments_automatic_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments which should be created based on rule 2
                                       #Start of road 0
                                       #Segment 0.0
        segments_automatic_expected = [[1,   0.0,  None],
                                       #Segment 25.0, due to drivable lane starting in laneSection 25.0
                                       #s_end due to laneSection 75.0 having no drivable lane
                                       [1,  25.0,  75.0]]
                                       
                                        
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic_expected):
            df_segments_automatic_expected = df_segments_automatic_expected.append({'road_id': segments_automatic_expected[index][0],
                                                                                    'segment_s_start': segments_automatic_expected[index][1],
                                                                                    'segment_s_end': segments_automatic_expected[index][2]},
                                                                                     ignore_index=True)
        #Convert values in column "road_id" to int 
        df_segments_automatic_expected['road_id']=df_segments_automatic_expected['road_id'].convert_dtypes()
        

        #Check if real result is equal to expected result
        assert_frame_equal(df_segments_automatic_expected, df_segments_automatic)
        
    def test_3_extract_segments_automatically_rule_3(self):
        """
        Test 3: Checks whether BSSD-segments are extracted correctly based on rule 3:
            If the speed limit for a drivable lane changes, a new segment has to be defined
                
        Scene: Three laneSections. The first laneSection has no drivable lanes. The other two laneSection have three drivable lanes each
        with several changes in <speed>-attribute --> See Testcase_A_03_3_scene.png

        
        --> It is checked whether the segments are extracted correctly based on the <speed>-elements
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_03_3'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        ##2. df_lane_data
        df_lane_data = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe

                    #Start of road 0
                    #laneSection 0.0 (No drivable lanes)
        lane_data =[[0,    0.0,   1, 'sidewalk', -1],
                    [0,    0.0,   2, 'sidewalk', -1],
                    [0,    0.0,  -1, 'sidewalk', -1],
                    [0,    0.0,  -2, 'sidewalk', -1],
                    #laneSection 21.79 (3 drivable lanes)
                    [0,  21.79,   1, 'driving', -1],
                    [0,  21.79,  -1, 'driving', -1],
                    [0,  21.79,  -2, 'driving', -1],
                    #laneSection 69.63 (3 drivable lanes)
                    [0,  69.63,   1, 'driving', -1],
                    [0,  69.63,   2, 'sidewalk', -1],
                    [0,  69.63,  -1, 'driving', -1],
                    [0,  69.63,  -2, 'driving', -1]]

        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data):
            df_lane_data = df_lane_data.append({'road_id': lane_data[index][0],
                                                'laneSection_s': lane_data[index][1],
                                                'lane_id': lane_data[index][2],
                                                'lane_type': lane_data[index][3],
                                                'junction_id': lane_data[index][4]}, ignore_index=True)
          
        ##3. df_lane_data_drivable_lanes
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
        #Contains all drivable lanes of lane_data
        
                                    #Start of road 0
        lane_data_drivable_lanes =[ #laneSection 21.79 (3 drivable lanes)
                                    [0,  21.79,   1, 'driving', -1],
                                    [0,  21.79,  -1, 'driving', -1],
                                    [0,  21.79,  -2, 'driving', -1],
                                    #laneSection 69.63 (3 drivable lanes)
                                    [0,  69.63,   1, 'driving', -1],
                                    [0,  69.63,  -1, 'driving', -1],
                                    [0,  69.63,  -2, 'driving', -1]]

        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
            
        
        ##4. df_segments_automatic
        
        df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments created based on rule 1 & 2
                            #Start of road 0
                            #Segment 21.79, due to change in number of drivable lanes (rule 1)
        segments_automatic= [[0,   21.79, None]]
                                       
                                     
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic):
            df_segments_automatic = df_segments_automatic.append({'road_id': segments_automatic[index][0],
                                                                'segment_s_start': segments_automatic[index][1],
                                                                'segment_s_end': segments_automatic[index][2]},
                                                                 ignore_index=True)
        

        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_segments_automatic, df_speed_limits = A_3_3_segments_by_speed_limit(df_lane_data, df_lane_data_drivable_lanes,
                                                                               df_segments_automatic, OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        
        ##1. df_speed_limits
        
        df_speed_limits_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'sOffset', 'speed_max', 'unit'])
        
        #list to fill DataFrame
        #<speed>-elements in input file, which should be added to df_speed_limits
        
                                 #Start of road 0
                                 #laneSection 0.0 has no drivable lanes --> speed limit not of interest
                                 #laneSection 21.79
                                 #lane 1 has speed limit 50 km/h at sOffset = 29.58
        speed_limits_expected = [[0,   21.79,  1, 29.58, float(50), 'km/h'],
                                 #lane -1 has speed limit 50 km/h at sOffset = 0.0
                                 [0,   21.79, -1,   0.0, float(50), 'km/h'],
                                 #lane -2 has no defined speed limit 
                                 
                                 #laneSection 69.63
                                 #lane 1 has speed limit 70 km/h at sOffset = 0.0 and speed limit 80 km/h at sOffset = 32.27
                                 [0,   69.63,  1,   0.0, float(70), 'km/h'],
                                 [0,   69.63,  1, 32.27, float(80), 'km/h'],
                                 #lane -1 has speed limit 50 km/h at sOffset = 0.0 and speed limit 50 km/h at sOffset = 44.92 (defined twice)
                                 [0,   69.63, -1,   0.0, float(50), 'km/h'],
                                 [0,   69.63, -1, 44.92, float(50), 'km/h'],
                                 #lane -2 has speed limit 60 km/h at sOffset = 0.0
                                 [0,   69.63, -2,   0.0, float(60), 'km/h']]
                                 
                                 

        #Paste list with data into DataFrame
        for index, element in enumerate(speed_limits_expected):
            df_speed_limits_expected = df_speed_limits_expected.append({'road_id': speed_limits_expected[index][0],
                                                                        'laneSection_s': speed_limits_expected[index][1],
                                                                        'lane_id': speed_limits_expected[index][2],
                                                                        'sOffset': speed_limits_expected[index][3],
                                                                        'speed_max': speed_limits_expected[index][4],
                                                                        'unit': speed_limits_expected[index][5]},
                                                                         ignore_index=True)
        
        ##2. df_segments_automatic
        
        df_segments_automatic_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments which should be created based on rule 3
                                       #Start of road 0
                                       #Segment 21.79, due to change in number of drivable lanes (rule 1)
        segments_automatic_expected = [[0,   21.79,  None],
                                       #Segment 51.37, due to speed limit in lane 1, laneSection 21.79
                                       [0,   51.37,  None],
                                       #Segment 69.63, due to change in speed limit (lanes 1 and -2) from laneSection 29.57 to laneSection 69.63
                                       [0,   69.63,  None],
                                       #Segment 101.9, due to change in speed limit during lane 1, laneSection 69.63
                                       [0,   101.9,  None]]

        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic_expected):
            df_segments_automatic_expected = df_segments_automatic_expected.append({'road_id': segments_automatic_expected[index][0],
                                                                                    'segment_s_start': segments_automatic_expected[index][1],
                                                                                    'segment_s_end': segments_automatic_expected[index][2]},
                                                                                     ignore_index=True)
            
        #Convert values in column "road_id" to int 
        df_segments_automatic_expected['road_id']=df_segments_automatic_expected['road_id'].convert_dtypes()
        
        #Check if real result is equal to expected result
        assert_frame_equal(df_segments_automatic_expected, df_segments_automatic)
        assert_frame_equal(df_speed_limits_expected, df_speed_limits)
        
    @mock.patch('builtins.input', create=True)
    def test_4_extract_segments_automatically_rule_4_1(self, mocked_input):
        """
        Test 4: Checks whether BSSD-segments are extracted correctly based on rule 4:
            If there is a traffic sign or a road-marking, which affects a BSSD behavioral attribute, a new segment is defined
                
        Scene: There exist several traffic signs, which affect BSSD, don't affect BSSD or are placed in a BSSD definition gap. In addition there is
        one <signalReference>-Element which is linked to a <signal>-Element
        --> See Testcase_A_03_4_scene.png

        --> It is checked whether the segments are extracted correctly based on the <signal>- and <signalReference>-elements
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_03_4'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
          
        ##2. df_lane_data_drivable_lanes
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
        #Contains all drivable lanes of lane_data
        
                                    #road 0
                                    #laneSection 0.0
        lane_data_drivable_lanes =[ [0,    0.0,  -1, 'driving', -1],
                                    #Start of road 1
                                    #laneSection 28.72 (2 drivable lanes)
                                    [1,  28.72,   1, 'driving', -1],
                                    [1,  28.72,  -1, 'driving', -1],
                                    #laneSection 119.25 (2 drivable lanes)
                                    [1, 119.25,   1, 'driving', -1],
                                    [1, 119.25,  -1, 'driving', -1],
                                    #Road 5
                                    [5,    0.0,   1, 'driving', -1],
                                    [5,    0.0,  -1, 'driving', -1],
                                    #Roads in Junction 6
                                    #Road 7
                                    [7,    0.0,  -1, 'driving',  6],
                                    #Road 10
                                    [10,   0.0,   1, 'driving',  6],
                                    #Road 16
                                    [16,   0.0,   1, 'driving',  6],
                                    #Road 17
                                    [17,   0.0,  -1, 'driving',  6]]


        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
            
        
        ##3. df_segments_automatic
        
        df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments created based on rule 1,2 & 3
                            
                             #road 0
        segments_automatic= [[0,     0.0,  None],
                             #Start of road 1
                             #Segment 28.72, due to change in number of drivable lanes (rule 1)
                             #Has a defined end as the succeeding laneSection has no drivable lanes (BSSD definition gap)
                             [1,   28.72, 92.39],
                             #Segment 119.25 due to change in number of drivable lanes (rule 1)
                             [1,  119.25, None],
                             #road 5
                             [5,     0.0,  None],
                             #road 7
                             [7,     0.0,  None],
                             #road 10
                             [10,    0.0,  None],
                             #road 16
                             [16,    0.0,  None],
                             #road 17
                             [17,    0.0,  None]]
                                       
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic):
            df_segments_automatic = df_segments_automatic.append({'road_id': segments_automatic[index][0],
                                                                'segment_s_start': segments_automatic[index][1],
                                                                'segment_s_end': segments_automatic[index][2]},
                                                                 ignore_index=True)
            
        ##4. Simulating user input 
        
        #Input "n" means that <signal>-elements with no defined "country"-attributes are not considered as <signal>-elements which
        #represent traffic signs and road markings from Germany
        mocked_input.side_effect = ['n']
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_segments_automatic, file_contains_dynamic_signals = A_3_4_segments_by_static_signals(df_lane_data_drivable_lanes, df_segments_automatic,
                                                                                                OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results

        ##1. df_segments_automatic
        
        df_segments_automatic_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments which should be created based on rule 4
        #5 traffic signs in imported xodr should not lead to a BSSD-segment as they are defined in a BSSD definition gap,
        #affect BSSD or don't affect BSSD
        
        segments_automatic_expected= [  [0,     0.0,  None],
                                        #Start of road 1
                                        #Segment 28.72, due to change in number of drivable lanes (rule 1)
                                        #Has a defined end as the succeeding laneSection has no drivable lanes (BSSD definition gap)
                                        [1,   28.72,  None],
                                        #Segment 51.37, due to traffic sign at s=80.02, which affects BSSD (rule 4)
                                        [1,   80.02, 92.39],
                                        #Segment 119.25 due to change in number of drivable lanes (rule 1)
                                        [1,  119.25, None],
                                        #road 5
                                        [5,     0.0,  None],
                                        #road 7
                                        [7,     0.0,  None],
                                        #segment 8.02 due to traffic sign at s=8.02
                                        [7,    8.02,  None],
                                        #road 10
                                        [10,    0.0,  None],
                                        #road 16
                                        [16,    0.0,  None],
                                        #road 17
                                        [17,    0.0,  None],
                                        #segment 7.58 due to link to traffic sign at s=7.58 (Element <signalReference>)
                                        [17,   7.58,  None]]

        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic_expected):
            df_segments_automatic_expected = df_segments_automatic_expected.append({'road_id': segments_automatic_expected[index][0],
                                                                                    'segment_s_start': segments_automatic_expected[index][1],
                                                                                    'segment_s_end': segments_automatic_expected[index][2]},
                                                                                     ignore_index=True)
        #Convert values in column "road_id" to int 
        df_segments_automatic_expected['road_id']=df_segments_automatic_expected['road_id'].convert_dtypes()
        
        #2. file_contains_dynamic_signals
        
        #OpenDRIVE-file contains no <signal>-elements with attribute dynamic="yes"
        file_contains_dynamic_signals_expected = False

        #Check if real result is equal to expected result
        assert_frame_equal(df_segments_automatic_expected, df_segments_automatic)
        self.assertEqual(file_contains_dynamic_signals_expected, file_contains_dynamic_signals)
        
    @mock.patch('builtins.input', create=True)
    def test_4_extract_segments_automatically_rule_4_2(self, mocked_input):
        """
        Test 4: Checks whether BSSD-segments are extracted correctly based on rule 4:
            If there is a traffic sign or a road-marking, which affects a BSSD behavioral attribute, a new segment is defined
                
        Scene: There exist several traffic signs, which affect BSSD, don't affect BSSD or are placed in a BSSD definition gap. In addition there is
        one <signalReference>-Element which is linked to a <signal>-Element
        --> See Testcase_A_03_4_scene.png

        --> It is checked whether the segments are extracted correctly based on the <signal>- and <signalReference>-elements
        
        --> In difference to "test_4_extract_segments_automatically_rule_4_1", the user input is "y" when asking whether
        <signal>-elements with no defined "country"-attributes are considered as <signal>-elements which represent traffic signs
        and road markings from Germany. --> Due to that one additional segment is extracted as the input OpenDRIVE-file contains one
        <signal>-element which represents a traffic sign from Germany but has no defined "country"-attribute
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_03_4'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
          
        ##2. df_lane_data_drivable_lanes
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
        #Contains all drivable lanes of lane_data
        
                                    #road 0
                                    #laneSection 0.0
        lane_data_drivable_lanes =[ [0,    0.0,  -1, 'driving', -1],
                                    #Start of road 1
                                    #laneSection 28.72 (2 drivable lanes)
                                    [1,  28.72,   1, 'driving', -1],
                                    [1,  28.72,  -1, 'driving', -1],
                                    #laneSection 119.25 (2 drivable lanes)
                                    [1, 119.25,   1, 'driving', -1],
                                    [1, 119.25,  -1, 'driving', -1],
                                    #Road 5
                                    [5,    0.0,   1, 'driving', -1],
                                    [5,    0.0,  -1, 'driving', -1],
                                    #Roads in Junction 6
                                    #Road 7
                                    [7,    0.0,  -1, 'driving',  6],
                                    #Road 10
                                    [10,   0.0,   1, 'driving',  6],
                                    #Road 16
                                    [16,   0.0,   1, 'driving',  6],
                                    #Road 17
                                    [17,   0.0,  -1, 'driving',  6]]


        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
            
        
        ##3. df_segments_automatic
        
        df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments created based on rule 1,2 & 3
                            
                             #road 0
        segments_automatic= [[0,     0.0,  None],
                             #Start of road 1
                             #Segment 28.72, due to change in number of drivable lanes (rule 1)
                             #Has a defined end as the succeeding laneSection has no drivable lanes (BSSD definition gap)
                             [1,   28.72, 92.39],
                             #Segment 119.25 due to change in number of drivable lanes (rule 1)
                             [1,  119.25, None],
                             #road 5
                             [5,     0.0,  None],
                             #road 7
                             [7,     0.0,  None],
                             #road 10
                             [10,    0.0,  None],
                             #road 16
                             [16,    0.0,  None],
                             #road 17
                             [17,    0.0,  None]]
                                       
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic):
            df_segments_automatic = df_segments_automatic.append({'road_id': segments_automatic[index][0],
                                                                'segment_s_start': segments_automatic[index][1],
                                                                'segment_s_end': segments_automatic[index][2]},
                                                                 ignore_index=True)
            
        ##4. Simulating user input 
        
        #Input "n" means that <signal>-elements with no defined "country"-attributes are not considered as <signal>-elements which
        #represent traffic signs and road markings from Germany
        mocked_input.side_effect = ['y']
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_segments_automatic, file_contains_dynamic_signals = A_3_4_segments_by_static_signals(df_lane_data_drivable_lanes, df_segments_automatic,
                                                                                                OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results

        ##1. df_segments_automatic
        
        df_segments_automatic_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments which should be created based on rule 4
        #5 traffic signs in imported xodr should not lead to a BSSD-segment as they are defined in a BSSD definition gap,
        #affect BSSD or don't affect BSSD
        
        segments_automatic_expected= [  [0,     0.0,  None],
                                        #Start of road 1
                                        #Segment 28.72, due to change in number of drivable lanes (rule 1)
                                        #Has a defined end as the succeeding laneSection has no drivable lanes (BSSD definition gap)
                                        [1,   28.72,  None],
                                        #Segment 55.6 due to traffic sign at s=34.04, which represents a traffic sign from Germany but has no
                                        #defined "country"-attribute --> Considered anyway as input above is "y"
                                        [1,    55.6,  None],
                                        #Segment 51.37, due to traffic sign at s=80.02, which affects BSSD (rule 4)
                                        [1,   80.02, 92.39],
                                        #Segment 119.25 due to change in number of drivable lanes (rule 1)
                                        [1,  119.25, None],
                                        #road 5
                                        [5,     0.0,  None],
                                        #road 7
                                        [7,     0.0,  None],
                                        #segment 8.02 due to traffic sign at s=8.02
                                        [7,    8.02,  None],
                                        #road 10
                                        [10,    0.0,  None],
                                        #road 16
                                        [16,    0.0,  None],
                                        #road 17
                                        [17,    0.0,  None],
                                        #segment 7.58 due to link to traffic sign at s=7.58 (Element <signalReference>)
                                        [17,   7.58,  None]]

        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic_expected):
            df_segments_automatic_expected = df_segments_automatic_expected.append({'road_id': segments_automatic_expected[index][0],
                                                                                    'segment_s_start': segments_automatic_expected[index][1],
                                                                                    'segment_s_end': segments_automatic_expected[index][2]},
                                                                                     ignore_index=True)
        #Convert values in column "road_id" to int 
        df_segments_automatic_expected['road_id']=df_segments_automatic_expected['road_id'].convert_dtypes()
        
        #2. file_contains_dynamic_signals
        
        #OpenDRIVE-file contains no <signal>-elements with attribute dynamic="yes"
        file_contains_dynamic_signals_expected = False

        #Check if real result is equal to expected result
        assert_frame_equal(df_segments_automatic_expected, df_segments_automatic)
        self.assertEqual(file_contains_dynamic_signals_expected, file_contains_dynamic_signals)
    

    def test_5_extract_segments_automatically_rule_5(self):
        """
        Test 5: Checks whether BSSD-segments are extracted correctly based on rule 5:
            If there is a traffic light or another dynamic signal, a new segment is defined
                
        Scene: There is one traffic sign with BSSD relevance (rule 4) and two traffic lights (rule 5). One traffic light is valid for two roads
        --> Use of element <signalReference>
        --> See Testcase_A_03_5_scene.png

        
        --> It is checked whether the segments are extracted correctly based on the <signal>- and <signalReference>-elements
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_A_03_5'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
          
        ##2. df_lane_data_drivable_lanes
        df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
        #Contains all drivable lanes of lane_data
                                            
                                     #Start of road 0
                                     #laneSection 0.0
        lane_data_drivable_lanes =[ [0,    0.0,  -1, 'driving', -1],
                                    #Start of road 1 (two drivable lanes)
                                    [1,  0.0,   1, 'driving', -1],
                                    [1,  0.0,  -1, 'driving', -1],
                                    #Road 2
                                    [2,    0.0,   1, 'driving', -1],
                                    [2,    0.0,  -1, 'driving', -1],
                                    #Roads in Junction 6
                                    #Road 4
                                    [4,    0.0,  -1, 'driving',  3],
                                    #Road 10
                                    [10,   0.0,   1, 'driving',  3],
                                    #Road 11
                                    [11,   0.0,   1, 'driving',  3]]


        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
            
        
        ##3. df_segments_automatic
        
        df_segments_automatic = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments created based on rule 1,2, 3 & 4
                              
                              #Road 0
        segments_automatic= [[0,     0.0,  None],
                             #Start of road 1
                             #Segment 0.0, due to change in number of drivable lanes (rule 1)
                             [1,   0.0, None],
                             #Segment 60.26, due to traffic sign with BSSD relevance (rule 4)
                             [1, 60.26, None],
                             #road 2
                             [2,     0.0,  None],
                             #road 4
                             [4,     0.0,  None],
                             #road 10
                             [10,    0.0,  None],
                             #road 11
                             [11,    0.0,  None]]
                             
                                       
        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic):
            df_segments_automatic = df_segments_automatic.append({'road_id': segments_automatic[index][0],
                                                                'segment_s_start': segments_automatic[index][1],
                                                                'segment_s_end': segments_automatic[index][2]},
                                                                 ignore_index=True)
            
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_segments_automatic = A_3_5_segments_by_dynamic_signals(df_lane_data_drivable_lanes, df_segments_automatic, OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results

        ##1. df_segments_automatic
        
        df_segments_automatic_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
        
        #list to fill DataFrame
        #Segments which should be created based on rule 5

        
        segments_automatic_expected=[[0,     0.0,  None],
                                     #Start of road 1
                                     #Segment 0.0, due to change in number of drivable lanes (rule 1)
                                     [1,   0.0, None],
                                     #Segment 32.48, due to traffic light (rule 5)
                                     [1, 32.48, None],
                                     #Segment 60.26, due to traffic sign with BSSD relevance (rule 4)
                                     [1, 60.26, None],
                                     #road 2
                                     [2,     0.0,  None],
                                     #road 4
                                     [4,     0.0,  None],
                                     #Segment 6.19 due to traffic light <signal>-element (rule 5)
                                     [4,    6.19,  None],
                                     #road 10
                                     [10,    0.0,  None],
                                     #road 11
                                     [11,    0.0,  None],
                                     #Segment 7.25 due to link to traffic light (rule 5) (element <signalReference>)
                                     [11,    7.25,  None]]

        #Paste list with data into DataFrame
        for index, element in enumerate(segments_automatic_expected):
            df_segments_automatic_expected = df_segments_automatic_expected.append({'road_id': segments_automatic_expected[index][0],
                                                                                    'segment_s_start': segments_automatic_expected[index][1],
                                                                                    'segment_s_end': segments_automatic_expected[index][2]},
                                                                                     ignore_index=True)
        
        #Convert values in column "road_id" to int 
        df_segments_automatic_expected['road_id']=df_segments_automatic_expected['road_id'].convert_dtypes()
        
        #Check if real result is equal to expected result
        assert_frame_equal(df_segments_automatic_expected, df_segments_automatic)
    
    def test_6_extract_segments_automatically_rules_combined(self):
    
       """
       Test 6: Checks whether BSSD-segments are extracted correctly based on all rules for extracting new segments
      
               
       Scene: Five laneSections. The first and last lane laneSection have no drivable lanes each. The other laneSections 
       have three drivable lanes each.
       --> With the laneSections and the drivable/not-drivable lanes rule 1 and rule 2 for extracting new segments are checked
       
       Beyond that, the OpenDRIVE-lanes have several changes in <speed>-element to check the correct application of rule 3.
       Furthermore, there are some static <signal>-Elements in the scene which check the correct application of rule 4
       Beyond that, there is one dynamic <signal>-element representing a traffic light to check the correct application of rule 5
       
       --> See Testcase_A_03_overall_scene.png

       
       """
    
       #### 1. ARRANGE
       #-----------------------------------------------------------------------
       
       ##1. OpenDRIVE_object
       
       #Filename of xodr which represents the input data
       filename_xodr = 'testcase_A_03'
       
       #Filepath to xodr
       filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

       #Read in xodr-file (lxml)
       tree_xodr = etree.parse(str(filepath_xodr))
       
       #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
       OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
       
         
       ##2. df_lane_data
       df_lane_data = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
       
       #list to fill Dataframe

                   #Start of road 0
                   #laneSection 0.0 (No drivable lanes)
       lane_data =[[0,    0.0,   1, 'sidewalk', -1],
                   [0,    0.0,   2, 'sidewalk', -1],
                   [0,    0.0,  -1, 'sidewalk', -1],
                   [0,    0.0,  -2, 'sidewalk', -1],
                   [0,    0.0,  -3, 'sidewalk', -1],
                   #laneSection 21.79 (3 drivable lanes)
                   [0,  21.79,   1, 'driving', -1],
                   [0,  21.79,  -1, 'driving', -1],
                   [0,  21.79,  -2, 'driving', -1],
                   [0,  21.79,  -3, 'sidewalk', -1],
                   #laneSection 69.63 (3 drivable lanes)
                   [0,  69.63,   1, 'driving', -1],
                   [0,  69.63,   2, 'sidewalk', -1],
                   [0,  69.63,  -1, 'driving', -1],
                   [0,  69.63,  -2, 'driving', -1],
                   [0,  69.63,  -3, 'sidewalk', -1],
                   #laneSection 162.02 (3 drivable lanes)
                   [0, 162.02,   1, 'driving', -1],
                   [0, 162.02,   2, 'driving', -1],
                   [0, 162.02,  -1, 'driving', -1],
                   [0, 162.02,  -2, 'sidewalk', -1],
                   #laneSection 206.45 (No drivable lanes)
                   [0, 206.45,   1, 'sidewalk', -1],
                   [0, 206.45,   2, 'sidewalk', -1],
                   [0, 206.45,  -1, 'sidewalk', -1],
                   [0, 206.45,  -2, 'sidewalk', -1],
                   [0, 206.45,  -3, 'sidewalk', -1]]
                   
       
       #Paste list with data into DataFrame
       for index, element in enumerate(lane_data):
           df_lane_data = df_lane_data.append({'road_id': lane_data[index][0],
                                               'laneSection_s': lane_data[index][1],
                                               'lane_id': lane_data[index][2],
                                               'lane_type': lane_data[index][3],
                                               'junction_id': lane_data[index][4]}, ignore_index=True)
         
       ##3. df_lane_data_drivable_lanes
       df_lane_data_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
       
       #list to fill Dataframe
       #Contains all drivable lanes of lane_data
       
                                   #Start of road 0
                                   #laneSection 21.79 (3 drivable lanes)
       lane_data_drivable_lanes =[ [0,  21.79,   1, 'driving', -1],
                                   [0,  21.79,  -1, 'driving', -1],
                                   [0,  21.79,  -2, 'driving', -1],
                                   #laneSection 69.63 (3 drivable lanes)
                                   [0,  69.63,   1, 'driving', -1],
                                   [0,  69.63,  -1, 'driving', -1],
                                   [0,  69.63,  -2, 'driving', -1],
                                   #laneSection 162.02 (3 drivable lanes)
                                   [0, 162.02,   1, 'driving', -1],
                                   [0, 162.02,   2, 'driving', -1],
                                   [0, 162.02,  -1, 'driving', -1]]

       #Paste list with data into DataFrame
       for index, element in enumerate(lane_data_drivable_lanes):
           df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                           'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                           'lane_id': lane_data_drivable_lanes[index][2],
                                                                           'lane_type': lane_data_drivable_lanes[index][3],
                                                                           'junction_id': lane_data_drivable_lanes[index][4]},
                                                                            ignore_index=True)
    
        
       #### 2. ACT
       #-----------------------------------------------------------------------
       df_segments_automatic, df_speed_limits = A_3_extract_segments_automatically(df_lane_data, df_lane_data_drivable_lanes, OpenDRIVE_object)
       
        
       #### 3. ASSERT
       #-----------------------------------------------------------------------
       
       #Create expected results
       
       ##1. df_segments_automatic
       
       df_segments_automatic_expected = pd.DataFrame(columns = ['road_id', 'segment_s_start', 'segment_s_end'])
       
       #list to fill DataFrame
       #Segments which should be created based on all rules for new segments
       
                                        #Start of road 0
                                        #Segment 21.79, due to change in number of drivable lanes (rule 1)
       segments_automatic_expected = [  [0,   21.79,  None],
                                        #Segment 28.57, due to traffic light (rule 5)
                                        [0,   28.57,  None],
                                        #Segment 51.37, due to speed limit in lane 1, laneSection 21.79 (rule 3)
                                        [0,   51.37,  None],
                                        #Segment 69.63, due to change in speed limit (lanes 1 and -2) from laneSection 29.57 
                                        #to laneSection 69.63 (rule 3)
                                        [0,   69.63,  None],
                                        #Segment 101.9, due to change in speed limit during lane 1, laneSection 69.63 (rule 3)
                                        [0,   101.9,  None],
                                        #Segment 162.02, due to starting/ending drivable lane (rule 2)
                                        [0,  162.02,  None],
                                        #Segment 183.03, due to <signal>-Element with relevance for BSSD at s=183.08 (rule 4)
                                        #Has a defined s_end at s=206.45 due to laneSection with no drivable lanes
                                        [0,  183.03,  206.45]]
                                        
                                      
       #Paste list with data into DataFrame
       for index, element in enumerate(segments_automatic_expected):
           df_segments_automatic_expected = df_segments_automatic_expected.append({'road_id': segments_automatic_expected[index][0],
                                                                                   'segment_s_start': segments_automatic_expected[index][1],
                                                                                   'segment_s_end': segments_automatic_expected[index][2]},
                                                                                    ignore_index=True)
       
        #Convert values in column "road_id" to int 
       df_segments_automatic_expected['road_id']=df_segments_automatic_expected['road_id'].convert_dtypes()    
    
        
       
        ##2. df_speed_limits
       
       df_speed_limits_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'sOffset', 'speed_max', 'unit'])
       
       #list to fill DataFrame
       #<speed>-elements in input file, which should be added to df_speed_limits
       
                                #Start of road 0
                                #laneSection 0.0 has no drivable lanes --> speed limit not of interest
                                #laneSection 21.79
                                #lane 1 has speed limit 50 km/h at sOffset = 29.58
       speed_limits_expected = [[0,   21.79,  1, 29.58, float(50), 'km/h'],
                                #lane -1 has speed limit 50 km/h at sOffset = 0.0
                                [0,   21.79, -1,   0.0, float(50), 'km/h'],
                                #lane -2 has no defined speed limit 
                                
                                #laneSection 69.63
                                #lane 1 has speed limit 70 km/h at sOffset = 0.0 and speed limit 80 km/h at sOffset = 32.27
                                [0,   69.63,  1,   0.0, float(70), 'km/h'],
                                [0,   69.63,  1, 32.27, float(80), 'km/h'],
                                #lane -1 has speed limit 50 km/h at sOffset = 0.0 and speed limit 50 km/h at sOffset = 44.92 (defined twice)
                                [0,   69.63, -1,   0.0, float(50), 'km/h'],
                                [0,   69.63, -1, 44.92, float(50), 'km/h'],
                                #lane -2 has speed limit 60 km/h at sOffset = 0.0
                                [0,   69.63, -2,   0.0, float(60), 'km/h']]
       
                                #No speed limits in laneSections 162.02 and 206.45
                                
                            
       #Paste list with data into DataFrame
       for index, element in enumerate(speed_limits_expected):
           df_speed_limits_expected = df_speed_limits_expected.append({'road_id': speed_limits_expected[index][0],
                                                                       'laneSection_s': speed_limits_expected[index][1],
                                                                       'lane_id': speed_limits_expected[index][2],
                                                                       'sOffset': speed_limits_expected[index][3],
                                                                       'speed_max': speed_limits_expected[index][4],
                                                                       'unit': speed_limits_expected[index][5]},
                                                                        ignore_index=True)    
   
    
       #Check if real result is equal to expected result
       assert_frame_equal(df_segments_automatic_expected, df_segments_automatic)
       assert_frame_equal(df_speed_limits_expected, df_speed_limits)
       
if __name__ == '__main__':
    unittest.main()
        
        
        