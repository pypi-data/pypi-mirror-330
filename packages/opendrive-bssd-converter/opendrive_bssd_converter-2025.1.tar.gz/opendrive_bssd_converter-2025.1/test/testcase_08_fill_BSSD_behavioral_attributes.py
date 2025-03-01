import unittest
import pandas as pd
from pathlib import Path
from lxml import etree
import xml.etree.ElementTree as ET

from integrate_BSSD_into_OpenDRIVE.opendrive_parser.parser import parse_opendrive
from utility.convert_xml_to_string_list import convert_xml_to_string_list
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_8_fill_BSSD_behavioral_attributes import step_8_fill_BSSD_behavioral_attributes

class TestcaseFillBssdBehavioralAttributes(unittest.TestCase):
    """
    TESTCASE A.08: Tests the function A_8_fill_BSSD_behavioral_attributes.py. This includes:
        - Test 1: Checks for every BSSD <speed>-element whether the extracted speed is inserted correctly along and against reference direction
            
    """
    
    def test_1_fill_BSSD_behavioral_attributes(self):
        """
        Test 1: Checks for every BSSD <speed>-element whether the extracted speed is inserted correctly along and against reference direction
        
        As input data a xodr-file is used which consists of two roads with a total amount of five segments.
        There are several different cases where the BSSD "speed" attribute is equal along and against driving direction (one way road, separation
        of driving directions) and several cases where the BSSD "speed" attribute against the driving direction is extracted from the other side 
        of the road.
        
        --> Same input data as for testcase_A_06_search_linked_OpenDRIVE_lanes.py --> see Testcase_A_07_1_scene.png
    
        The test is executed with RHT as well as with LHT.

        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. OpenDRIVE_object/OpenDRIVE_element
        
        #Filename of xodr which represents the input data
        filename_xodr = 'testcase_08'
        
        #Filepath to xodr
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
        
        #Import xodr-file (lxml) --> Needed for opendriveparser TUM
        tree_xodr = etree.parse(str(filepath_xodr))
        #Create object OpenDRIVE from root-element (Usage of opendriveparser from TUM)
        OpenDRIVE_object = parse_opendrive(tree_xodr.getroot())
        
        #Create two separate ElementTrees (for RHT and LHT)
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr_RHT = ET.parse(filepath_xodr)

        #Access root-element of imported xodr-file
        OpenDRIVE_element_RHT = tree_xodr_RHT.getroot()
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr_LHT = ET.parse(filepath_xodr)

        #Access root-element of imported xodr-file
        OpenDRIVE_element_LHT = tree_xodr_LHT.getroot()
        
        
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
        OpenDRIVE_element_RHT = step_8_fill_BSSD_behavioral_attributes(df_lane_data, df_BSSD_lanes, df_link_BSSD_lanes_with_OpenDRIVE_lanes,
                                                                                            df_speed_limits, df_segments, driving_direction_RHT, 
                                                                                            OpenDRIVE_element_RHT, OpenDRIVE_object)
        
        #Result for LHT
        OpenDRIVE_element_LHT = step_8_fill_BSSD_behavioral_attributes(df_lane_data, df_BSSD_lanes, df_link_BSSD_lanes_with_OpenDRIVE_lanes,
                                                                                            df_speed_limits, df_segments, driving_direction_LHT, 
                                                                                            OpenDRIVE_element_LHT, OpenDRIVE_object)
        
        #Convert resulting OpenDRIVE_element to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_RHT_string = convert_xml_to_string_list(OpenDRIVE_element_RHT) 
        OpenDRIVE_element_LHT_string = convert_xml_to_string_list(OpenDRIVE_element_LHT) 
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected result
        
        ##1.1 OpenDRIVE_element RHT
        
        #Filename of xodr which contains the expected result (<speed>-elements are filled according to speed limits in OpenDRIVE-file)
        filename_xodr_expected = 'testcase_08_expected_RHT'
        
        #Filepath to valid xodr with version 1.4
        filepath_xodr_expected = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr_expected +'.xodr')
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr_expected = ET.parse(filepath_xodr_expected)
        
        #Access root-element of imported xodr-file
        OpenDRIVE_element_RHT_expected = tree_xodr_expected.getroot()
        
        #Convert OpenDRIVE_element_expected to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_RHT_expected_string = convert_xml_to_string_list(OpenDRIVE_element_RHT_expected)
        
        ##1.1 OpenDRIVE_element LHT
        
        #Filename of xodr which contains the expected result (<speed>-elements are filled according to speed limits in OpenDRIVE-file)
        filename_xodr_expected = 'testcase_08_expected_LHT'
        
        #Filepath to valid xodr with version 1.4
        filepath_xodr_expected = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr_expected +'.xodr')
        
        #Import xodr-file (xml.etree.ElementTree)
        tree_xodr_expected = ET.parse(filepath_xodr_expected)
        
        #Access root-element of imported xodr-file
        OpenDRIVE_element_LHT_expected = tree_xodr_expected.getroot()
        
        #Convert OpenDRIVE_element_expected to a list of strings for assertion (Necessary to avoid problems with different
        #tabs, newlines and whitespaces when comparing the result with the expected result)
        OpenDRIVE_element_LHT_expected_string = convert_xml_to_string_list(OpenDRIVE_element_LHT_expected)
        
        
        #Check if real result is equal to expected result
        self.assertListEqual(OpenDRIVE_element_RHT_expected_string, OpenDRIVE_element_RHT_string)
        self.assertListEqual(OpenDRIVE_element_LHT_expected_string, OpenDRIVE_element_LHT_string)
    
if __name__ == '__main__':
    unittest.main()
        
        
        