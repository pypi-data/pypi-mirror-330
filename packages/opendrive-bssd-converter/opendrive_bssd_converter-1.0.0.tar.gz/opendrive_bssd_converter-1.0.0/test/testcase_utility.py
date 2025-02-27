import unittest
from pandas.testing import assert_frame_equal
import pandas as pd
from pathlib import Path
from lxml import etree
import xml.etree.ElementTree as ET


from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from integrate_BSSD_into_OpenDRIVE.utility.check_for_separated_BSSD_lane import criterion_1_check_innermost_BSSD_lanes
from integrate_BSSD_into_OpenDRIVE.utility.check_for_separated_BSSD_lane import criterion_2_check_crossability_of_lane_borders
from integrate_BSSD_into_OpenDRIVE.utility.access_BSSD_user_data_element import access_BSSD_user_data_element
from integrate_BSSD_into_OpenDRIVE.utility.classify_BSSD_lane_borders import criterion_1_neighbour_lanes
from integrate_BSSD_into_OpenDRIVE.utility.classify_BSSD_lane_borders import criterion_2_objects
from integrate_BSSD_into_OpenDRIVE.utility.find_OpenDRIVE_lane import find_OpenDRIVE_lane
from integrate_BSSD_into_OpenDRIVE.utility.collect_object_data import collect_object_data
from integrate_BSSD_into_OpenDRIVE.utility.check_relation_OpenDRIVE_BSSD_lane import check_relation_OpenDRIVE_BSSD_lane


class TescaseUtility(unittest.TestCase):
    """
    TESTCASE UTILITY: Tests all utility functions which are used throughout BSSD-integration into OpenDRIVE (folder "utility").
    
    This Testcase includes:
        - Test 1: Tests the function "access_BSSD_user_data_element" used in all concept steps when accessing the created BSSD-<userData>-element
        - Test 2: Tests the function "criterion_1_neighbour_lanes" used in the utility function "classify_BSSD_lane_borders".
        - Test 3.1: Tests the function "find_OpenDRIVE_lane" used in the utility function "find_OpenDRIVE_lane" (input with <width>-element)
        - Test 3.2: Tests the function "find_OpenDRIVE_lane" used in the utility function "find_OpenDRIVE_lane" (input with <border>-element)
        - Test 4: Tests the function "collect_object_data" used in the utility function "collect_object_data"
        - Test 5: Tests the function "check_relation_OpenDRIVE_BSSD_lane" used in the utility function "check_relation_OpenDRIVE_BSSD_lane"      
        - Test 6: Tests the function "criterion_2_objects" used in the utility function "classify_BSSD_lane_borders".
        - Test 7: Tests the function "criterion_1_check_drivable_lanes" used in the utility function "check_for_separated_BSSD_lane"
        - Test 8: Tests the function "criterion_2_check_objects" used in the utility function "check_for_separated_BSSD_lane"
    """

    def test_1_access_BSSD_user_data_element(self):
        """
        Test 1: Tests the function "access_BSSD_user_data_element" used in all concept steps when accessing the created BSSD-<userData>-element
                
                This function returns the <userData>-element in a <road>-element that contains the BSSD-segments
                --> There might be other <userData>-elements existing in a <road>-element that do not include the BSSD-data
                    
                As input data a xodr is chosen which contains several <userData>-elements under the <road>-element
                It is checked whether the right <userData>-element (created by step 2 of BSSD-Integration) is found.
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. road_element
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_access_userData_element'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr = ET.parse(filepath_xodr)

        #Access root-element of imported xodr-file
        OpenDRIVE_element = tree_xodr.getroot()
        
        #Input xodr consits of one road only --> Get element for this road as input for function to test
        road_element = OpenDRIVE_element.findall('road')[0]
        
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        user_data_element  = access_BSSD_user_data_element(road_element)
      
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        ##1. user_data_element
        
        user_data_element_expected = ET.Element('userData', attrib={'code': 'BSSD', 'value': 'BSSD_segments'})
        
        #Check if test_result is equal to expected result (Tag and attributes of <userData>-Elements are identical)
        self.assertEqual(user_data_element_expected.tag, user_data_element.tag)
        self.assertEqual(user_data_element_expected.attrib, user_data_element.attrib)
        
    def test_2_classify_BSSD_lane_borders_criterion_1 (self):
        """
        Test 2: Tests the function "criterion_1_neighbour_lanes" used in the utility function "classify_BSSD_lane_borders".
                
                
                This function classifies the right and left border of all BSSD-lanes into crossable or not-crossable based on criterion 1:
                "Every border of a BSSD-lane is crossable if there is a neighbouring BSSD- or OpenDRIVE-lane existing
                which is not of type "none" or "curb"".
                                
                The input scenario contains three BSSD-lanes which have neighbouring lanes of different types and have no neighbouring lanes
                --> See testcase_classify_BSSD_lane_borders_crossable_criterion_1.png
            
                
                It is checked whether the right and left borders of the BSSD-lanes are classified correctly crossable/not-crossable 
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_BSSD_lanes
        
        ##Import OpenDRIVE_object as laneSection-objects are needed for input-data (df_BSSD_lanes)
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_classify_BSSD_lane_borders_criterion_1'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        #Get laneSection_objects from imported OpenDRIVE_object
        laneSection_object_road_0 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[0]
        laneSection_object_road_1 = OpenDRIVE_object.getRoad(1).lanes.lane_sections[0]
        
        df_BSSD_lanes = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_object_s_min'])
        
        #list to fill DataFrame
        #Contains all created BSSD-lanes and the first laneSection overlapping to the segment which contains the BSSD-lane
        
                    #Start of road 0
                    #segment 0.0 has two BSSD-lanes
        BSSD_lanes=[[0,   0.0, -2,  laneSection_object_road_0],
                    [0,   0.0,  1,  laneSection_object_road_0],
                    #Start of road 1
                    #segment 0.0 has one BSSD-lane
                    [1,   0.0,  1,  laneSection_object_road_1]]
        
        
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
        
        df_BSSD_lanes_borders_crossable = criterion_1_neighbour_lanes(df_BSSD_lanes)


        #### 3. ASSERT
        #-----------------------------------------------------------------------
               
        ##1. df_BSSD_lanes_borders_crossable_expected
        
        df_BSSD_lanes_borders_crossable_expected = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'crossable_left', 'crossable_right'])
        
        #list to fill DataFrame
        
                                                #Start of road 0
                                                #lane -2: Right neighbour lane is of type "sidewalk" (--> crossable)
                                                #left neighbour lane is of type "none" (--> Not crossable)
        BSSD_lanes_borders_crossable_expected =[[0,   0.0, -2,  False, True],
                                                #lane 1: Right neighbour lane is of type "none" (--> Not crossable)
                                                #Left neighbour lane is of type "curb" (--> not crosable)
                                                [0,   0.0,  1,   False, False],
                                                #Start of road 1
                                                #lane 1 has no neighbouring lanes --> Both borders are not crossable
                                                [1,   0.0,  1,  False, False]]
        
        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_lanes_borders_crossable_expected):
            df_BSSD_lanes_borders_crossable_expected = df_BSSD_lanes_borders_crossable_expected.append(
                                                {'road_id': BSSD_lanes_borders_crossable_expected[index][0],
                                                'segment_s': BSSD_lanes_borders_crossable_expected[index][1],
                                                'lane_id_BSSD': BSSD_lanes_borders_crossable_expected[index][2],
                                                'crossable_left': BSSD_lanes_borders_crossable_expected[index][3],
                                                'crossable_right': BSSD_lanes_borders_crossable_expected[index][4]},
                                                 ignore_index=True)
        
        
        
        #Check if test_result is equal to expected result
        assert_frame_equal(df_BSSD_lanes_borders_crossable_expected, df_BSSD_lanes_borders_crossable)
        
        
    def test_3_1_find_OpenDRIVE_lane_width (self):
        """
        Test 3.1: Tests the function "find_OpenDRIVE_lane" used in the utility function "find_OpenDRIVE_lane" (input with <width>-element) 
                        
                This function finds the OpenDRIVE-lane in which a defined point of a road in the OpenDRIVE-map (s-,t-coordinate & road_id) is
                located.
                    
                The input scenario contains a road with a laneOffset and lanes that have several changes in the defined width.
                The lane width in this scenario is defined by <width>-elements.
                
                For several points it is checked whether the right OpenDRIVE-lane is found and the correct distance of the defined point to
                the left & right border of the OpenDRIVE-lane is calculated.
                
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        ##Import OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_find_OpenDRIVE_lane_width'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        ##2. Input data of point of interest
        road_id = 0
        
        #Point 1 
        s_coordinate_1 = 122.0
        t_coordinate_1 = 1.2
        
        #Point 2 (inside lane -2, laneSection 72.96)
        s_coordinate_2 = 101.0
        t_coordinate_2 = -6.0
        
        #Point 3 (outside of road, t-coordinate to high)
        s_coordinate_3 = 101.0
        t_coordinate_3 = 50.0
        
        #Point 4 (outside of road, s-coordinate > length of road)
        s_coordinate_4 = 1200.0
        t_coordinate_4 = 0.0
                    
                
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        laneSection_s_1, lane_id_1, delta_t_right_1, delta_t_left_1 = find_OpenDRIVE_lane(s_coordinate_1, t_coordinate_1, road_id, OpenDRIVE_object)
        laneSection_s_2, lane_id_2, delta_t_right_2, delta_t_left_2 = find_OpenDRIVE_lane(s_coordinate_2, t_coordinate_2, road_id, OpenDRIVE_object)
        laneSection_s_3, lane_id_3, delta_t_right_3, delta_t_left_3 = find_OpenDRIVE_lane(s_coordinate_3, t_coordinate_3, road_id, OpenDRIVE_object)
        laneSection_s_4, lane_id_4, delta_t_right_4, delta_t_left_4 = find_OpenDRIVE_lane(s_coordinate_4, t_coordinate_4, road_id, OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected result
        #Calculated by hand (with elements <laneOffset> and <width>)
        
        #Point 1 (inside lane 1, laneSection 72.96)
        laneSection_s_1_expected = 72.96
        lane_id_1_expected = 1
        delta_t_right_1_expected = 1.78
        delta_t_left_1_expected = 1.99
        
        #Point 2 (inside lane -2, laneSection 72.96)
        laneSection_s_2_expected = 72.96
        lane_id_2_expected = -2
        delta_t_right_2_expected = 3.16
        delta_t_left_2_expected = 1.27
        
        #Point 3 (outside of road, t-coordinate to high)
        laneSection_s_3_expected = 72.96
        lane_id_3_expected = None
        delta_t_right_3_expected = None
        delta_t_left_3_expected = None
        
        #Point 4 (outside of road, s-coordinate > length of road)
        laneSection_s_4_expected = None
        lane_id_4_expected = None
        delta_t_right_4_expected = None
        delta_t_left_4_expected = None
        
        
        #Check if test_result is equal to expected result
        self.assertEqual(laneSection_s_1_expected, laneSection_s_1)
        self.assertEqual(lane_id_1_expected, lane_id_1)
        self.assertEqual(delta_t_right_1_expected, delta_t_right_1)
        self.assertEqual(delta_t_left_1_expected, delta_t_left_1)
        
        self.assertEqual(laneSection_s_2_expected, laneSection_s_2)
        self.assertEqual(lane_id_2_expected, lane_id_2)
        self.assertEqual(delta_t_right_2_expected, delta_t_right_2)
        self.assertEqual(delta_t_left_2_expected, delta_t_left_2)
        
        self.assertEqual(laneSection_s_3_expected, laneSection_s_3)
        self.assertEqual(lane_id_3_expected, lane_id_3)
        self.assertEqual(delta_t_right_3_expected, delta_t_right_3)
        self.assertEqual(delta_t_left_3_expected, delta_t_left_3)
        
        self.assertEqual(laneSection_s_4_expected, laneSection_s_4)
        self.assertEqual(lane_id_4_expected, lane_id_4)
        self.assertEqual(delta_t_right_4_expected, delta_t_right_4)
        self.assertEqual(delta_t_left_4_expected, delta_t_left_4)
        
        
    def test_3_2_find_OpenDRIVE_lane_border (self):
        """
        Test 3.2: Tests the function "find_OpenDRIVE_lane" used in the utility function "find_OpenDRIVE_lane" (input with <border>-element) 
                        
                This function finds the OpenDRIVE-lane in which a defined point of a road in the OpenDRIVE-map (s-,t-coordinate & road_id) is
                located.
                
                The input scenario contains a road with a lane that has several changes in the defined width.
                The lane width in this scenario is defined by <border>-elements.
                
                For several points it is checked whether the right OpenDRIVE-lane is found and the correct distance of the defined point to
                the left & right border of the OpenDRIVE-lane is calculated.
                
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        ##Import OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_find_OpenDRIVE_lane_border'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.7', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        ##2. Input data of point of interest
        road_id = 1
        
        #Point 1
        s_coordinate_1 = 61.0
        t_coordinate_1 = -3.7
                    
                
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        laneSection_s_1, lane_id_1, delta_t_right_1, delta_t_left_1 = find_OpenDRIVE_lane(s_coordinate_1, t_coordinate_1, road_id, OpenDRIVE_object)
        

        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected result
        #Calculated by hand (with elements <border>)
        
        #Point 1
        laneSection_s_1_expected = 50.0
        lane_id_1_expected = -2
        delta_t_right_1_expected = 1.92
        delta_t_left_1_expected = 0.13
        
        
        #Check if test_result is equal to expected result
        self.assertEqual(laneSection_s_1_expected, laneSection_s_1)
        self.assertEqual(lane_id_1_expected, lane_id_1)
        self.assertEqual(delta_t_right_1_expected, delta_t_right_1)
        self.assertEqual(delta_t_left_1_expected, delta_t_left_1)
        
    
    def test_4_collect_object_data (self):
        """
        Test 4: Tests the function "collect_object_data" used in the utility function "collect_object_data"
                                
                This function parses all objects in the imported OpenDRIVE-file and creates a DataFrame containing certain data about every object
                that doesn't fulfill the following conditions:
                    - Object that are placed in a height that is not of interest for motor vehicles (Maximum height = 4m --> see StVO §22, Absatz 2 )
                    - Objects that are not placed on the road (s-, and t-coordinate)
                    - If object is <repeat>-element, it has to represent only one object (attribute "distance"=0)
                    
                --> Conditions match to all objects which are not of interest for analyzing crossability of the border of a lane
                (function "classify_BSSD_lane_borders")
                                
                The input scenario 5 <object>-elements and 4 <repeat>-elements.         
                It is checked whether the right <object>/<repeat>-elements are skipped and if the right data is gathered about the
                remaining <object>/<repeat>-elements
                
                --> See testcase_collect_object_data.png
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        ##Import OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_collect_object_data'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
                    
                
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        df_object_data = collect_object_data(OpenDRIVE_object)


        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        ##1. df_object_data
        
        df_object_data_expected = pd.DataFrame(columns = ['object_id', 'repeat', 'type','road_id', 'laneSection_s', 'lane_id', 's_origin', 't_origin',
                                                          'delta_t_left', 'delta_t_right', 's_min', 's_max'])
        
        #list to fill DataFrame
        #Contains information about all objects which are of interest for crossability of lane borders
        
                                #Four  objects are contained in df_object_data as only they are of interest for crossability of lane borders
                                #Object represented by <object>-element with id = 2 (Has heading, pitch and roll defined)
        object_data_expected =[[2, False, 'None', 0, 0.0, -1, 1.98, -1.86, 1.86, 1.64,  1.32,  2.64],
                               #Object represented by <object>-element with id = 1
                               [1, False, 'None', 0, 0.0, -1, 35.7, -1.58, 1.58, 1.92, 35.41, 35.99],
                               #Object represented by <repeat>-element inside <object>-element with id = 1
                               [1,  True, 'None', 0, 0.0, -1,  7.34,  -2.5, 2.5,    1,   7.0, 7.69],
                               #Object represented by <object>-element with id = 5
                               [5, False, 'None', 0, 0.0,  1,42.86,  1.33, 2.17, 1.33,  42.51, 43.21]]
                                              
        
        #Paste list with data into DataFrame
        for index, element in enumerate(object_data_expected):
            df_object_data_expected = df_object_data_expected.append(
                                                {'object_id': object_data_expected[index][0], 'repeat': object_data_expected[index][1],
                                                 'type': object_data_expected[index][2],
                                                'road_id': object_data_expected[index][3], 'laneSection_s': object_data_expected[index][4],
                                                'lane_id': object_data_expected[index][5], 's_origin': object_data_expected[index][6],
                                                't_origin': object_data_expected[index][7], 'delta_t_left': object_data_expected[index][8],
                                                'delta_t_right': object_data_expected[index][9], 's_min': object_data_expected[index][10],
                                                's_max': object_data_expected[index][11]}, ignore_index=True)
        
        
        
        #Check if test_result is equal to expected result
        assert_frame_equal(df_object_data_expected, df_object_data)
        
        
    
    def test_5_check_relation_OpenDRIVE_BSSD_lane(self):
        """
        Test 5: Tests the function "check_relation_OpenDRIVE_BSSD_lane" used in the utility function "check_relation_OpenDRIVE_BSSD_lane"
        
        This function checks if an OpenDRIVE-lane is related to a BSSD-lane. In this context "related" means that the OpenDRIVE-lane:
            a. Directly overlaps to the BSSD-lane (see df_link_BSSD_lanes_with_OpenDRIVE_lanes)
            or
            b. Is connected via the elements <predecessor>/<successor> to an OpenDRIVE-lane which directly overlaps to the BSSD-lane
            
        The function returns True if the OpenDRIVE-lane is related to the BSSD-lane. Otherwise the function returns False
                
        As input data a xodr-file is used which consists of two roads with several laneSections. It is checked for different pairs of OpenDRIVE-lane
        and BSSD-lane if the classification is correctly "related" or "not related"
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_check_relation_OpenDRIVE_BSSD_lane'
        
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
        lane_data = [[0,   0.0,  1, 'driving', -1],
                    [0,   0.0,  2, 'sidewalk', -1],
                    [0,   0.0, -1, 'driving', -1],
                    [0,   0.0, -2, 'sidewalk', -1],
                    #Start of road 1 
                    #laneSection 0.0
                    [1,   0.0,  1, 'driving', -1],
                    [1,   0.0,  2, 'sidewalk', -1],
                    [1,   0.0, -1, 'driving', -1],
                    [1,   0.0, -2, 'sidewalk', -1],
                    #laneSection 24.29
                    [1, 24.29,  1, 'driving', -1],
                    [1, 24.29,  2, 'sidewalk', -1],
                    [1, 24.29, -1, 'driving', -1],
                    [1, 24.29, -2, 'driving', -1],
                    [1, 24.29, -3, 'sidewalk', -1],
                    #laneSection 45.78
                    [1, 45.78,  1, 'driving', -1],
                    [1, 45.78,  2, 'sidewalk', -1],
                    [1, 45.78,  3, 'sidewalk', -1],
                    [1, 45.78, -1, 'driving', -1],
                    [1, 45.78, -2, 'driving', -1],
                    [1, 45.78, -3, 'sidewalk', -1]]
    
        
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data):
            df_lane_data = df_lane_data.append({'road_id': lane_data[index][0],
                                                'laneSection_s': lane_data[index][1],
                                                'lane_id': lane_data[index][2],
                                                'lane_type': lane_data[index][3],
                                                'junction_id': lane_data[index][4]}, ignore_index=True)
            
            
            
        ##3. df_link_BSSD_lanes_with_OpenDRIVE_lanes

        df_link_BSSD_lanes_with_OpenDRIVE_lanes= pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_s',
                                                                         'lane_id_OpenDRIVE'])
        
        #list to fill DataFrame
        #Contains for every OpenDRIVE-lane that is defined within the s-range of a BSSD-lane a separate row 
        
                                                #Start of road 0
        link_BSSD_lanes_with_OpenDRIVE_lanes =[ [0,   0.0, -1,  0.0, -1],
                                                [0,   0.0,  1,  0.0,  1],
                                                #road 1
                                                [1,   0.0, -1,  0.0, -1],
                                                [1,   0.0,  1,  0.0,  1],
                                                [1, 24.29, -2, 24.29, -2],
                                                [1, 24.29, -2, 45.78, -2],
                                                [1, 24.29, -1, 24.29, -1],
                                                [1, 24.29, -1, 45.78, -1],
                                                [1, 24.29,  1, 24.29, 1],
                                                [1, 24.29,  1, 45.78, 1]]
                                                

        
        #Paste list with data into DataFrame
        for index, element in enumerate(link_BSSD_lanes_with_OpenDRIVE_lanes):
            df_link_BSSD_lanes_with_OpenDRIVE_lanes = df_link_BSSD_lanes_with_OpenDRIVE_lanes.append(
                                                                {'road_id': link_BSSD_lanes_with_OpenDRIVE_lanes[index][0],
                                                                'segment_s': link_BSSD_lanes_with_OpenDRIVE_lanes[index][1],
                                                                'lane_id_BSSD': link_BSSD_lanes_with_OpenDRIVE_lanes[index][2],
                                                                'laneSection_s': link_BSSD_lanes_with_OpenDRIVE_lanes[index][3],
                                                                'lane_id_OpenDRIVE': link_BSSD_lanes_with_OpenDRIVE_lanes[index][4]},
                                                                 ignore_index=True)
        
        
        ##4.data_BSSD_lane/data_OpenDRIVE_lane
        
        #1. OpenDRIVE-lane overlaps directly with BSSD-lane (see df_link_BSSD_lanes_with_OpenDRIVE_lanes)
        
        #Columns road_id, lanesection_s, lane_id_OpenDRIVE
        data_OpenDRIVE_lane_1 = [1, 45.78, -1]
        #Columns road_id, segment_s, lane_id_BSSD
        data_BSSD_lane_1 = [1, 24.29, -1]
        
        #2. OpenDRIVE-lane is related with BSSD-lane due to successor-element
        
        #Columns road_id, lanesection_s, lane_id_OpenDRIVE
        data_OpenDRIVE_lane_2 = [1, 45.78, -2]
        #Columns road_id, segment_s, lane_id_BSSD
        data_BSSD_lane_2 = [1, 0.0, -1]
        
        #3. OpenDRIVE-lane is related with BSSD-lane due to predecessor-element
        
        #Columns road_id, lanesection_s, lane_id_OpenDRIVE
        data_OpenDRIVE_lane_3 = [1, 0.0, -1]
        #Columns road_id, segment_s, lane_id_BSSD
        data_BSSD_lane_3 = [1, 24.29, -2]
        
        #4. OpenDRIVE-lane is not related with BSSD-lane (forward direction)
        
        #Columns road_id, lanesection_s, lane_id_OpenDRIVE
        data_OpenDRIVE_lane_4 = [1, 24.29, -1]
        #Columns road_id, segment_s, lane_id_BSSD
        data_BSSD_lane_4 = [1, 0.0, -1]
        
        #5. OpenDRIVE-lane is not related with BSSD-lane (backward direction)
        
        #Columns road_id, lanesection_s, lane_id_OpenDRIVE
        data_OpenDRIVE_lane_5 = [1, 0.0, -1]
        #Columns road_id, segment_s, lane_id_BSSD
        data_BSSD_lane_5 = [1, 24.29, -1]
       
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        return_value_1 = check_relation_OpenDRIVE_BSSD_lane(data_OpenDRIVE_lane_1, data_BSSD_lane_1, df_lane_data, 
                                                                                     df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_object)
        return_value_2 = check_relation_OpenDRIVE_BSSD_lane(data_OpenDRIVE_lane_2, data_BSSD_lane_2, df_lane_data, 
                                                                                     df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_object)
        return_value_3 = check_relation_OpenDRIVE_BSSD_lane(data_OpenDRIVE_lane_3, data_BSSD_lane_3, df_lane_data, 
                                                                                     df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_object)
        return_value_4 = check_relation_OpenDRIVE_BSSD_lane(data_OpenDRIVE_lane_4, data_BSSD_lane_4, df_lane_data, 
                                                                                     df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_object)
        return_value_5 = check_relation_OpenDRIVE_BSSD_lane(data_OpenDRIVE_lane_5, data_BSSD_lane_5, df_lane_data, 
                                                                                     df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Check if real result is equal to expected result
        self.assertTrue(return_value_1)
        self.assertTrue(return_value_2)
        self.assertTrue(return_value_3)
        self.assertFalse(return_value_4)
        self.assertFalse(return_value_5)
        
    def test_6_classify_BSSD_lane_borders_criterion_2(self):
        """
        Test 6: Tests the function "criterion_2_objects" used in the utility function "classify_BSSD_lane_borders"
        
        This function modifies the right/left border of all BSSD-lanes to not crossable based on criterion 2:
        "The border of a BSSD-lane is not crossable if there is an object/multiple objects in this BSSD-lane 
        defined throughout the whole s-range of this BSSD-lane"
        
        The input scenario contains two roads with:
            - three large objects which separate BSSD-lanes
            - multiple objects directly connected together --> Also one large "object" that separates BSSD-lanes
        
        --> See testcase_classify_BSSD_lane_borders_crossable_criterion_2.png
    
        It is checked whether the right and left borders of the BSSD-lanes which are separated by the objects are classified correctly
        as not-crossable 
        
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_classify_BSSD_lane_borders_criterion_2'
        
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
        lane_data = [[0,   0.0,  1, 'driving', -1],
                    [0,   0.0,  2, 'driving', -1],
                    [0,   0.0,  3, 'driving', -1],
                    [0,   0.0, -1, 'driving', -1],
                    [0,   0.0, -2, 'driving', -1],
                    [0,   0.0, -3, 'driving', -1],
                    #laneSection 34.58
                    [0, 34.58,  1, 'driving', -1],
                    [0, 34.58,  2, 'driving', -1],
                    [0, 34.58,  3, 'driving', -1],
                    [0, 34.58, -1, 'driving', -1],
                    [0, 34.58, -2, 'driving', -1],
                    #laneSection 69.71
                    [0, 69.71,  1, 'driving', -1],
                    [0, 69.71,  2, 'driving', -1],
                    [0, 69.71, -1, 'driving', -1],
                    [0, 69.71, -2, 'driving', -1],
                    #Start of road 3
                    #laneSection 0.0
                    [3,   0.0,  1, 'driving', -1],
                    [3,   0.0,  2, 'driving', -1],
                    [3,   0.0,  3,  'border', -1],
                    [3,   0.0,  4, 'sidewalk', -1],
                    [3,   0.0, -1, 'driving', -1],
                    [3,   0.0, -2, 'driving', -1],
                    #laneSection 25.12
                    [3, 25.12,  1, 'driving', -1],
                    [3, 25.12,  2, 'driving', -1],
                    [3, 25.12,  3,  'border', -1],
                    [3, 25.12,  4, 'sidewalk', -1],
                    [3, 25.12, -1, 'driving', -1]]

    
        
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
                    [0, 34.58,  None],
                    [0, 69.71,  None],
                    [3,   0.0,  None],
                    [3, 25.12,  None]]
                                 
        #Paste list with data into DataFrame
        for index, element in enumerate(segments):
            df_segments = df_segments.append({'road_id': segments[index][0],
                                            'segment_s_start': segments[index][1],
                                            'segment_s_end': segments[index][2]},
                                             ignore_index=True)
                
            
        ##4. df_BSSD_lanes
        
        #Get laneSection_objects from imported OpenDRIVE_object
        laneSection_object_0_0_road_0 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[0]
        laneSection_object_34_58 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[1]
        laneSection_object_69_71 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[2]
        
        laneSection_object_0_0_road_3 = OpenDRIVE_object.getRoad(3).lanes.lane_sections[0]
        laneSection_object_25_12 = OpenDRIVE_object.getRoad(3).lanes.lane_sections[1]
        
        df_BSSD_lanes = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_object_s_min'])
        
        #list to fill DataFrame
        #Contains all created BSSD-lanes and the first laneSection overlapping to the segment which contains the BSSD-lane
        
                    #Start of road 0
                    #segment 0.0 (six BSSD-lanes)
        BSSD_lanes=[[0,   0.0, -3,  laneSection_object_0_0_road_0],
                    [0,   0.0, -2,  laneSection_object_0_0_road_0],
                    [0,   0.0, -1,  laneSection_object_0_0_road_0],
                    [0,   0.0,  1,  laneSection_object_0_0_road_0],
                    [0,   0.0,  2,  laneSection_object_0_0_road_0],
                    [0,   0.0,  3,  laneSection_object_0_0_road_0],
                    #segment 34.58 (five BSSD-lanes)
                    [0, 34.58, -2,  laneSection_object_34_58],
                    [0, 34.58, -1,  laneSection_object_34_58],
                    [0, 34.58,  1,  laneSection_object_34_58],
                    [0, 34.58,  2,  laneSection_object_34_58],
                    [0, 34.58,  3,  laneSection_object_34_58],
                    #segment 69.71 (four BSSD-lanes)
                    [0, 69.71, -2,  laneSection_object_69_71],
                    [0, 69.71, -1,  laneSection_object_69_71],
                    [0, 69.71,  1,  laneSection_object_69_71],
                    [0, 69.71,  2,  laneSection_object_69_71],
                    #road 3
                    #segment 0.0 (five BSSD-lanes)
                    [3,   0.0, -2,  laneSection_object_0_0_road_3],
                    [3,   0.0, -1,  laneSection_object_0_0_road_3],
                    [3,   0.0,  1,  laneSection_object_0_0_road_3],
                    [3,   0.0,  2,  laneSection_object_0_0_road_3],
                    [3,   0.0,  3,  laneSection_object_0_0_road_3],
                    #segment 25.12 (four BSSD-lanes)
                    [3, 25.12, -1,  laneSection_object_25_12],
                    [3, 25.12,  1,  laneSection_object_25_12],
                    [3, 25.12,  2,  laneSection_object_25_12],
                    [3, 25.12,  3,  laneSection_object_25_12]]
                    
        
        
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
        link_BSSD_lanes_with_OpenDRIVE_lanes = [[0,   0.0, -3,  0.0, -3],
                                                [0,   0.0, -2,  0.0, -2],
                                                [0,   0.0, -1,  0.0, -1],
                                                [0,   0.0,  1,  0.0,  1],
                                                [0,   0.0,  2,  0.0,  2],
                                                [0,   0.0,  3,  0.0,  3],
                                                #segment 34.58 
                                                [0, 34.58, -2, 34.58, -2],
                                                [0, 34.58, -1, 34.58, -1],
                                                [0, 34.58,  1, 34.58,  1],
                                                [0, 34.58,  2, 34.58,  2],
                                                [0, 34.58,  3, 34.58,  3],
                                                #segment 69.71 
                                                [0, 69.71, -2, 69.71, -2],
                                                [0, 69.71, -1, 69.71, -1],
                                                [0, 69.71,  1, 69.71,  1],
                                                [0, 69.71,  2, 69.71,  2],
                                                #road 3
                                                #segment 0.0
                                                [3,   0.0, -2, 0.0, -2],
                                                [3,   0.0, -1, 0.0, -1],
                                                [3,   0.0,  1, 0.0,  1],
                                                [3,   0.0,  2, 0.0,  2],
                                                [3,   0.0,  3, 0.0,  3],
                                                #segment 25.12
                                                [3, 25.12, -1, 25.12, -1],
                                                [3, 25.12,  1, 25.12,  1],
                                                [3, 25.12,  2, 25.12,  2],
                                                [3, 25.12,  3, 25.12,  3]]
                                                    

        
        #Paste list with data into DataFrame
        for index, element in enumerate(link_BSSD_lanes_with_OpenDRIVE_lanes):
            df_link_BSSD_lanes_with_OpenDRIVE_lanes = df_link_BSSD_lanes_with_OpenDRIVE_lanes.append(
                                                                {'road_id': link_BSSD_lanes_with_OpenDRIVE_lanes[index][0],
                                                                'segment_s': link_BSSD_lanes_with_OpenDRIVE_lanes[index][1],
                                                                'lane_id_BSSD': link_BSSD_lanes_with_OpenDRIVE_lanes[index][2],
                                                                'laneSection_s': link_BSSD_lanes_with_OpenDRIVE_lanes[index][3],
                                                                'lane_id_OpenDRIVE': link_BSSD_lanes_with_OpenDRIVE_lanes[index][4]},
                                                                 ignore_index=True)
            
            
        ##5. df_BSSD_lanes_borders_crossable
        #--> Classification of lane borders as crossable/not-crossable based on criterion 1
        
        df_BSSD_lanes_borders_crossable = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'crossable_left', 'crossable_right'])
        
        #list to fill DataFrame
        
                                        #Start of road 0
                                        #segment 0.0
        BSSD_lanes_borders_crossable =[ [0,   0.0, -1,  True, True],
                                        [0,   0.0, -2,  True, True],
                                        [0,   0.0, -3,  True, False],
                                        [0,   0.0,  1,  True, True],
                                        [0,   0.0,  2,  True, True],
                                        [0,   0.0,  3, False, True],
                                        #segment 34.58 
                                        [0, 34.58, -1, True, True],
                                        [0, 34.58, -2, True, False],
                                        [0, 34.58,  1, True, True],
                                        [0, 34.58,  2, True, True],
                                        [0, 34.58,  3, False, True],
                                        #segment 69.71 
                                        [0, 69.71, -1, True, True],
                                        [0, 69.71, -2, True, False],
                                        [0, 69.71,  1, True, True],
                                        [0, 69.71,  2, False, True],
                                        #road 3
                                        #segment 0.0
                                        [3,   0.0, -1, True, True],
                                        [3,   0.0, -2, True, False],
                                        [3,   0.0,  1, True, True],
                                        [3,   0.0,  2, True, True],
                                        [3,   0.0,  3, True, True],
                                        #segment 25.12
                                        [3, 25.12, -1, True, False],
                                        [3, 25.12,  1, True, True],
                                        [3, 25.12,  2, True, True],
                                        [3, 25.12,  3, True, True]]
        
        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_lanes_borders_crossable):
            df_BSSD_lanes_borders_crossable = df_BSSD_lanes_borders_crossable.append(
                                            {'road_id': BSSD_lanes_borders_crossable[index][0],
                                            'segment_s': BSSD_lanes_borders_crossable[index][1],
                                            'lane_id_BSSD': BSSD_lanes_borders_crossable[index][2],
                                            'crossable_left': BSSD_lanes_borders_crossable[index][3],
                                            'crossable_right': BSSD_lanes_borders_crossable[index][4]},
                                             ignore_index=True)
            
       
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_BSSD_lanes_borders_crossable = criterion_2_objects(df_lane_data, df_BSSD_lanes, df_segments, df_link_BSSD_lanes_with_OpenDRIVE_lanes,
                                                              df_BSSD_lanes_borders_crossable, OpenDRIVE_object)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected result
        
        ##1. df_BSSD_lanes_borders_crossable
        #--> Classification of lane borders as crossable/not-crossable based on criterion 1 & criterion 2
        
        df_BSSD_lanes_borders_crossable_expected = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'crossable_left', 'crossable_right'])
        
        #list to fill DataFrame
        
                                                #Start of road 0
                                                #segment 0.0
        BSSD_lanes_borders_crossable_expected =[[0,   0.0, -3,  True, False],
                                                [0,   0.0, -2,  False, True],
                                                [0,   0.0, -1,  True, False],
                                                [0,   0.0,  1, False, True],
                                                [0,   0.0,  2,  True, False],
                                                [0,   0.0,  3, False, True],
                                                #segment 34.58 
                                                [0, 34.58, -2, False, False],
                                                [0, 34.58, -1, True, False],
                                                [0, 34.58,  1, False, True],
                                                [0, 34.58,  2, True, False],
                                                [0, 34.58,  3, False, True],
                                                #segment 69.71 
                                                [0, 69.71, -2, False, False],
                                                [0, 69.71, -1, True, False],
                                                [0, 69.71,  1, False, True],
                                                [0, 69.71,  2, False, False],
                                                #road 3
                                                #segment 0.0
                                                [3,   0.0, -2, True, False],
                                                [3,   0.0, -1, False, True],
                                                [3,   0.0,  1, True, False],
                                                [3,   0.0,  2, False, True],
                                                [3,   0.0,  3, False, False],
                                                #segment 25.12
                                                [3, 25.12, -1, True, False],
                                                [3, 25.12,  1, True, True],
                                                [3, 25.12,  2, False, True],
                                                [3, 25.12,  3, False, False]]
        
        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_lanes_borders_crossable_expected):
            df_BSSD_lanes_borders_crossable_expected = df_BSSD_lanes_borders_crossable_expected.append(
                                            {'road_id': BSSD_lanes_borders_crossable_expected[index][0],
                                            'segment_s': BSSD_lanes_borders_crossable_expected[index][1],
                                            'lane_id_BSSD': BSSD_lanes_borders_crossable_expected[index][2],
                                            'crossable_left': BSSD_lanes_borders_crossable_expected[index][3],
                                            'crossable_right': BSSD_lanes_borders_crossable_expected[index][4]},
                                             ignore_index=True)
        
        #Check if real result is equal to expected result
        assert_frame_equal(df_BSSD_lanes_borders_crossable_expected, df_BSSD_lanes_borders_crossable)
        
        
    def test_7_separated_BSSD_lane_criterion_1(self):
        """
        Test 7: Tests the function "criterion_1_check_drivable_lanes" used in the utility function "check_for_separated_BSSD_lane".
            
        This function executes criterion 1 for checking whether a BSSD-lane separated from the BSSD-lanes on the other side of the road
        (function "check_for_separated_BSSD_lane")
                                                                                                                                         .
        Criterion 1 is defined as: If there is a not-drivable lane between the innermost BSSD-lanes in the segment of the BSSD-lane, the BSSD-lane is
            separated from the BSSD-lanes on the other side of the road.        
        
                
        The input scenario contains two BSSD-segments. In one BSSD-segment the driving directions are not separated, in the other BSSD-segment
        the driving directions are separated.
        
        It is checked whether the BSSD-Segments are classified correctly as separated or not separated from the other side of the road.
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_BSSD_lanes
        
        ##Import OpenDRIVE_object as laneSection-objects are needed for input-data (df_BSSD_lanes)
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_check_for_separated_BSSD_lane_criterion_1'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        #Get laneSection_objects from imported OpenDRIVE_object
        laneSection_object_0_0 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[0]
        laneSection_object_71_62 = OpenDRIVE_object.getRoad(0).lanes.lane_sections[1]
        
        df_BSSD_lanes = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'laneSection_object_s_min'])
        
        #list to fill DataFrame
        #Contains all created BSSD-lanes and the first laneSection overlapping to the segment which contains the BSSD-lane
        
                    #Start of road 1
                    #segment 0.0 has two BSSD-lanes
        BSSD_lanes=[[0,   0.0, -1,  laneSection_object_0_0],
                    [0,   0.0,  1,  laneSection_object_0_0],
                    #segment 71_62 has three BSSD-lanes 
                    [0, 71.62, -3,  laneSection_object_71_62],
                    [0, 71.62, -2,  laneSection_object_71_62],
                    [0, 71.62,  1,  laneSection_object_71_62]]
        
        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_lanes):
            df_BSSD_lanes = df_BSSD_lanes.append(
                                                {'road_id': BSSD_lanes[index][0],
                                                'segment_s': BSSD_lanes[index][1],
                                                'lane_id_BSSD': BSSD_lanes[index][2],
                                                'laneSection_object_s_min': BSSD_lanes[index][3]},
                                                 ignore_index=True)
            
        ##2. road_id
        #Id of road which contains BSSD-Segment
        road_id = 0
        
        ##3. segment_s
        #s-coordinates of BSSD-segments for which separation to other side of the road should be checked
        segment_s_1 = 0.0
        segment_s_2 = 71.62
                
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        return_value_1 = criterion_1_check_innermost_BSSD_lanes(road_id, segment_s_1, df_BSSD_lanes)
        return_value_2 = criterion_1_check_innermost_BSSD_lanes(road_id, segment_s_2, df_BSSD_lanes)


        #### 3. ASSERT
        #-----------------------------------------------------------------------
               
        #Check if test_result is equal to expected result
        
        #First segment is not separated from other side of the road as innermost BSSD-lanes have the id's -1 and 1
        self.assertFalse(return_value_1)
        #Second segment is separated from other side of the road as there is a not drivable lane between the innermost BSSD-lanes
        self.assertTrue(return_value_2)
        
    def test_8_separated_BSSD_lane_criterion_2(self):
        """
        Test 8: Tests the function "criterion_2_check_crossability_of_lane_borders" used in the utility function "check_for_separated_BSSD_lane".
        
        This function executes criterion 2 for checking whether a BSSD-lane separated from the BSSD-lanes on the other side of the road.
        
        Criterion 2 is defined as: If there is a not crossable border of a BSSD-lane, which is located inwards to the
            BSSD-lane and on the same side of the road like the BSSD-lane, the BSSD-lane is separated from the BSSD-lanes on the other side of the
            road.
                
        The input scenario contains two BSSD-segments. In the first segment there is a not crossable border between two BSSD-lanes on the left
        side of the road, in the second segment there is a not crossable border between two BSSD-lanes on the right side of the road
                
        For every BSSD-lane it is checked whether it is classified correctly as separated/not separated from the other side of the road
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_BSSD_lanes_borders_crossable
        #--> Classification of lane borders as crossable/not-crossable
        
        df_BSSD_lanes_borders_crossable = pd.DataFrame(columns = ['road_id', 'segment_s', 'lane_id_BSSD', 'crossable_left', 'crossable_right'])
        
        #list to fill DataFrame
        
                                        #Start of road 0
                                        #segment 0.0
                                        #Right side, only lane -3 has right border which is not crossable
        BSSD_lanes_borders_crossable =[ [0,   0.0, -1,  True, True],
                                        [0,   0.0, -2,  True, True],
                                        [0,   0.0, -3,  True, False],
                                        #Left side, not crossable border between lane 1 and 2
                                        [0,   0.0,  1, False, True],
                                        [0,   0.0,  2,  True, False],
                                        [0,   0.0,  3, True, True],
                                        #segment 20.0
                                        #Right side, not crossable border between lane -2 and -3
                                        [0,  20.0, -1, True, True],
                                        [0,  20.0, -2, True, False],
                                        [0,  20.0, -3,  False, True],
                                        [0,  20.0, -4,  True, False],
                                        #Right side, only lane 3 has left border which is not crossable
                                        [0,  20.0,  1, True, True],
                                        [0,  20.0,  2, True, True],
                                        [0,  20.0,  3, False, True]]
        
        
        #Paste list with data into DataFrame
        for index, element in enumerate(BSSD_lanes_borders_crossable):
            df_BSSD_lanes_borders_crossable = df_BSSD_lanes_borders_crossable.append(
                                            {'road_id': BSSD_lanes_borders_crossable[index][0],
                                            'segment_s': BSSD_lanes_borders_crossable[index][1],
                                            'lane_id_BSSD': BSSD_lanes_borders_crossable[index][2],
                                            'crossable_left': BSSD_lanes_borders_crossable[index][3],
                                            'crossable_right': BSSD_lanes_borders_crossable[index][4]},
                                             ignore_index=True)
        
    
            
        ##All lanes are located in road with id 0
        road_id = 0       
                
        #### 2. ACT
        #-----------------------------------------------------------------------
        return_values = []
        
        #Execute function to test for every BSSD-lane in the input scenario
        for index, lane_id_BSSD in enumerate(df_BSSD_lanes_borders_crossable.loc[:, 'lane_id_BSSD']):
            
            segment_s = df_BSSD_lanes_borders_crossable.loc[index, 'segment_s']
            
            return_values.append(criterion_2_check_crossability_of_lane_borders(road_id, segment_s, lane_id_BSSD, df_BSSD_lanes_borders_crossable))
            

        #### 3. ASSERT
        #-----------------------------------------------------------------------
               
        #Check if test_result is equal to expected result
                                  #laneSection 0.0
                                  #Right side, all lanes are not separated
        return_values_expected = [False, False, False,
                                  #Left side, Lanes 2 and 3 are separeted 
                                  False, True, True,
                                  #laneSection 20.0
                                  #Right side, Lanes -3 and -4 are separated
                                  False, False, True, True,
                                  #Left side, all lanes are not separated 
                                  False, False, False]
        
                
        self.assertListEqual(return_values_expected, return_values)
        
    
if __name__ == '__main__':

    unittest.main()
        
        
        