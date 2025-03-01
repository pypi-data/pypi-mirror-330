import unittest
from unittest import mock
import pandas as pd
from pandas.testing import assert_frame_equal

from integrate_BSSD_into_OpenDRIVE.algorithms.A_2_manually_edit_drivable_lanes import A_2_manually_edit_drivable_lanes
from integrate_BSSD_into_OpenDRIVE.algorithms.A_2_manually_edit_drivable_lanes import validate_input


class TestcaseAddDrivableLanes(unittest.TestCase):
    """
    TESTCASE A.02.1: Tests the function of adding drivable lanes manually in A_2_manually_edit_drivable_lanes.py. This includes:
        - Test 1: Check whether one not-drivable lane is added correctly to the list of drivable lanes depending on user input.
        - Test 2: Check whether multiple not-drivable lanes are added correctly to the list of drivable lanes depending on user input.
        - Test 3: Check whether valid/invalid user input is recognized as valid/not valid when adding not drivable lanes to list of drivable lanes
    
    """
    
    @mock.patch('builtins.input', create=True)
    def test_add_one_drivable_lane(self, mocked_input):
        """
        Test 1: Check whether one not-drivable lane is added correctly to the list of drivable lanes depending on user input.
        As input data one road with two lane sections that contain multiple drivable lanes and multiple not-drivable lanes is used
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_lane_data
        df_lane_data = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                    #Start of road 0
                    #laneSection 0.0
        lane_data =[[0,    0.0,   1, 'driving', -1],
                    [0,    0.0,   2, 'driving', -1],
                    [0,    0.0,  -1,  'sidewalk', -1],
                    #laneSection 20.0
                    [0,   20.0,   1, 'driving', -1],
                    [0,   20.0,   2, 'sidewalk', -1],
                    [0,   20.0,  -1,  'sidewalk', -1]]
    
        
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
                                    #Start of road 0
                                    #laneSection 0.0
        lane_data_drivable_lanes = [[0,    0.0,   1, 'driving', -1],
                                    [0,    0.0,   2, 'driving', -1],
                                    #laneSection 20.0
                                    [0,   20.0,   1, 'driving', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
        
        ##3. df_lane_data_not_drivable_lanes
        df_lane_data_not_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                                        #Start of road 0
                                        #laneSection 0.0        
        lane_data_not_drivable_lanes = [[0,    0.0,  -1,  'sidewalk', -1],
                                        #laneSection 20.0
                                        [0,   20.0,   2,  'sidewalk', -1],
                                        [0,   20.0,  -1,  'sidewalk', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_not_drivable_lanes):
            df_lane_data_not_drivable_lanes = df_lane_data_not_drivable_lanes.append({'road_id': lane_data_not_drivable_lanes[index][0],
                                                                                    'laneSection_s': lane_data_not_drivable_lanes[index][1],
                                                                                    'lane_id': lane_data_not_drivable_lanes[index][2],
                                                                                    'lane_type': lane_data_not_drivable_lanes[index][3],
                                                                                    'junction_id': lane_data_not_drivable_lanes[index][4]},
                                                                                     ignore_index=True)
        
        ##4. Simulating user input 
        
        #Input "0" adds the lane with the index 0 in df_lane_data_not_drivable_lanes to the list of drivable lanes
        #Input "c" means that no drivable lane should be marked as not-drivable lane
        mocked_input.side_effect = ['0', 'c']
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_lane_data_drivable_lanes, df_lane_data_not_drivable_lanes = A_2_manually_edit_drivable_lanes(df_lane_data,
                                                                                                    df_lane_data_drivable_lanes, 
                                                                                                    df_lane_data_not_drivable_lanes)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        
        ##1. df_lane_data_drivable_lanes

        df_lane_data_drivable_lanes_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                                              #Start of road 0
                                              #laneSection 0.0
                                              #Lane -1 added to list of drivable lanes
        lane_data_drivable_lanes_expected = [ [0,    0.0,  -1,  'sidewalk', -1],
                                              [0,    0.0,   1, 'driving', -1],
                                              [0,    0.0,   2, 'driving', -1],
                                              #laneSection 20.0
                                              [0,   20.0,   1, 'driving', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes_expected):
            df_lane_data_drivable_lanes_expected = df_lane_data_drivable_lanes_expected.append(
                                                                            {'road_id': lane_data_drivable_lanes_expected[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes_expected[index][1],
                                                                            'lane_id': lane_data_drivable_lanes_expected[index][2],
                                                                            'lane_type': lane_data_drivable_lanes_expected[index][3],
                                                                            'junction_id': lane_data_drivable_lanes_expected[index][4]},
                                                                             ignore_index=True)
        
        ##2. df_lane_data_not_drivable_lanes
        
        df_lane_data_not_drivable_lanes_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                                                #Start of road 0
                                                #laneSection 20.0
        lane_data_not_drivable_lanes_expected = [[0,   20.0,   2,  'sidewalk', -1],
                                                 [0,   20.0,  -1,  'sidewalk', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_not_drivable_lanes_expected):
            df_lane_data_not_drivable_lanes_expected = df_lane_data_not_drivable_lanes_expected.append(
                                                                            {'road_id': lane_data_not_drivable_lanes_expected[index][0],
                                                                            'laneSection_s': lane_data_not_drivable_lanes_expected[index][1],
                                                                            'lane_id': lane_data_not_drivable_lanes_expected[index][2],
                                                                            'lane_type': lane_data_not_drivable_lanes_expected[index][3],
                                                                            'junction_id': lane_data_not_drivable_lanes_expected[index][4]},
                                                                             ignore_index=True)
                

        #Check if test_result is equal to expected result (= True)
        assert_frame_equal(df_lane_data_drivable_lanes_expected, df_lane_data_drivable_lanes)
        assert_frame_equal(df_lane_data_not_drivable_lanes_expected, df_lane_data_not_drivable_lanes)
     
    @mock.patch('builtins.input', create=True)
    def test_add_multiple_drivable_lane(self, mocked_input):
        """
        Test 2: Check whether multiple not-drivable lanes are added correctly to the list of drivable lanes depending on user input.
        As input data one road with two lane sections that contain multiple drivable lanes and multiple not-drivable lanes is used
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        ##1. df_lane_data
        df_lane_data = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                    #Start of road 0
                    #laneSection 0.0
        lane_data =[[0,    0.0,   1, 'driving', -1],
                    [0,    0.0,   2, 'driving', -1],
                    [0,    0.0,  -1,  'sidewalk', -1],
                    #laneSection 20.0
                    [0,   20.0,   1, 'driving', -1],
                    [0,   20.0,   2, 'sidewalk', -1],
                    [0,   20.0,  -1,  'sidewalk', -1]]
    
        
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
                                    #Start of road 0
                                    #laneSection 0.0
        lane_data_drivable_lanes = [[0,    0.0,   1, 'driving', -1],
                                    [0,    0.0,   2, 'driving', -1],
                                    #laneSection 20.0
                                    [0,   20.0,   1, 'driving', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes):
            df_lane_data_drivable_lanes = df_lane_data_drivable_lanes.append({'road_id': lane_data_drivable_lanes[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes[index][1],
                                                                            'lane_id': lane_data_drivable_lanes[index][2],
                                                                            'lane_type': lane_data_drivable_lanes[index][3],
                                                                            'junction_id': lane_data_drivable_lanes[index][4]},
                                                                             ignore_index=True)
        
        ##3. df_lane_data_not_drivable_lanes
        df_lane_data_not_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                                        #Start of road 0
                                        #laneSection 0.0        
        lane_data_not_drivable_lanes = [[0,    0.0,  -1,  'sidewalk', -1],
                                        #laneSection 20.0
                                        [0,   20.0,   2,  'sidewalk', -1],
                                        [0,   20.0,  -1,  'sidewalk', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_not_drivable_lanes):
            df_lane_data_not_drivable_lanes = df_lane_data_not_drivable_lanes.append({'road_id': lane_data_not_drivable_lanes[index][0],
                                                                                    'laneSection_s': lane_data_not_drivable_lanes[index][1],
                                                                                    'lane_id': lane_data_not_drivable_lanes[index][2],
                                                                                    'lane_type': lane_data_not_drivable_lanes[index][3],
                                                                                    'junction_id': lane_data_not_drivable_lanes[index][4]},
                                                                                     ignore_index=True)
        
        
        ##4. Simulating user input 
        
        #Input "0, 2" adds the lanes in the indices 0 and 2 in df_lane_data_not_drivable_lanes to the list of drivable lanes
        #Input "c" means that no drivable lane should be marked as not-drivable lane
        mocked_input.side_effect = ['0, 2', 'c']
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        df_lane_data_drivable_lanes, df_lane_data_not_drivable_lanes = A_2_manually_edit_drivable_lanes(df_lane_data,
                                                                                                    df_lane_data_drivable_lanes, 
                                                                                                    df_lane_data_not_drivable_lanes)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Create expected results
        
        
        ##1. df_lane_data_drivable_lanes

        df_lane_data_drivable_lanes_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                                              #Start of road 0
                                              #laneSection 0.0
                                              #Added lane -1 to list of drivable lanes
        lane_data_drivable_lanes_expected = [ [0,    0.0,  -1,  'sidewalk', -1],
                                              [0,    0.0,   1, 'driving', -1],
                                              [0,    0.0,   2, 'driving', -1],
                                              #laneSection 20.0
                                              #Added lane -1 to list of drivable lanes
                                              [0,   20.0,  -1,  'sidewalk', -1],
                                              [0,   20.0,   1, 'driving', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_drivable_lanes_expected):
            df_lane_data_drivable_lanes_expected = df_lane_data_drivable_lanes_expected.append(
                                                                            {'road_id': lane_data_drivable_lanes_expected[index][0],
                                                                            'laneSection_s': lane_data_drivable_lanes_expected[index][1],
                                                                            'lane_id': lane_data_drivable_lanes_expected[index][2],
                                                                            'lane_type': lane_data_drivable_lanes_expected[index][3],
                                                                            'junction_id': lane_data_drivable_lanes_expected[index][4]},
                                                                             ignore_index=True)
        
        ##2. df_lane_data_not_drivable_lanes
        
        df_lane_data_not_drivable_lanes_expected = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
    
        #list to fill Dataframe
                                                #Start of road 0
                                                #laneSection 20.0
        lane_data_not_drivable_lanes_expected = [[0,   20.0,  2,  'sidewalk', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_not_drivable_lanes_expected):
            df_lane_data_not_drivable_lanes_expected = df_lane_data_not_drivable_lanes_expected.append(
                                                                            {'road_id': lane_data_not_drivable_lanes_expected[index][0],
                                                                            'laneSection_s': lane_data_not_drivable_lanes_expected[index][1],
                                                                            'lane_id': lane_data_not_drivable_lanes_expected[index][2],
                                                                            'lane_type': lane_data_not_drivable_lanes_expected[index][3],
                                                                            'junction_id': lane_data_not_drivable_lanes_expected[index][4]},
                                                                             ignore_index=True)

        #Check if test_result is equal to expected result (= True)
        assert_frame_equal(df_lane_data_drivable_lanes_expected, df_lane_data_drivable_lanes)
        assert_frame_equal(df_lane_data_not_drivable_lanes_expected, df_lane_data_not_drivable_lanes)
        

    def test_validate_input(self):
        """
        Test 3: Checks whether valid/invalid user input is recognized as valid/not valid when adding not drivable lanes to list of
        drivable lanes (Function "validate_input" from A_2_manually_edit_drivable_lanes.py)
        
        The following valid input cases are checked:
            - One correct index 
            - Two correct indices 
            - Two correct indices with different order and no space at one position
        
        The following invalid input cases are checked:
            - One wrong index
            - One correct and one false index 
            - Identical indices 
            - Wrong input format (no numbers separated by comma )
            - Wrong input format (empty input)
            
        As input data one road with two laneSections with not-drivable lanes is used
        """
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
       
        ## 1. df_lane_data_not_drivable_lanes --> Input of indices of this DataFrame to add to the list of drivable lanes
        df_lane_data_not_drivable_lanes = pd.DataFrame(columns = ['road_id', 'laneSection_s', 'lane_id', 'lane_type', 'junction_id'])
        
        #list to fill Dataframe
                                        #Start of road 0
                                        #laneSection 0.0
        lane_data_not_drivable_lanes = [[0,    0.0,  -1,  'sidewalk', -1],
                                        #laneSection 20.0
                                        [0,   20.0,   2,  'sidewalk', -1],
                                        [0,   20.0,  -1,  'sidewalk', -1]]

    
        #Paste list with data into DataFrame
        for index, element in enumerate(lane_data_not_drivable_lanes):
            df_lane_data_not_drivable_lanes = df_lane_data_not_drivable_lanes.append({'road_id': lane_data_not_drivable_lanes[index][0],
                                                                                    'laneSection_s': lane_data_not_drivable_lanes[index][1],
                                                                                    'lane_id': lane_data_not_drivable_lanes[index][2],
                                                                                    'lane_type': lane_data_not_drivable_lanes[index][3],
                                                                                    'junction_id': lane_data_not_drivable_lanes[index][4]},
                                                                                     ignore_index=True)
        
        ##2. Provide inputs
        
        #Provide valid inputs
        
        #One correct index
        input_valid_1 = '0'
        #Two correct indices
        input_valid_2 = '0, 2'
        #Three correct indices with different order and no space at one position
        input_valid_3 = '2,0, 1'
        
        #Provide invalid inputs
        
        #One wrong index
        input_invalid_1 = '5012'
        #One correct and one false index 
        input_invalid_2 = '1, 1532'
        #Identical indices 
        input_invalid_3 = '1, 1'
        #Wrong input format (no numbers separated by comma )
        input_invalid_3 = '1. 2'
        #Wrong input format (no numbers separated by comma )
        input_invalid_4 = '1; 0'
        #Wrong input format (empty input)
        input_invalid_5 = ''
        
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        return_input_valid_1, list_number_elements = validate_input(input_valid_1, df_lane_data_not_drivable_lanes)
        return_input_valid_2, list_number_elements = validate_input(input_valid_2, df_lane_data_not_drivable_lanes)
        return_input_valid_3, list_number_elements = validate_input(input_valid_3, df_lane_data_not_drivable_lanes)
        
        return_input_invalid_1, list_number_elements = validate_input(input_invalid_1, df_lane_data_not_drivable_lanes)
        return_input_invalid_2, list_number_elements = validate_input(input_invalid_2, df_lane_data_not_drivable_lanes)
        return_input_invalid_3, list_number_elements = validate_input(input_invalid_3, df_lane_data_not_drivable_lanes)
        return_input_invalid_4, list_number_elements = validate_input(input_invalid_4, df_lane_data_not_drivable_lanes)
        return_input_invalid_5, list_number_elements = validate_input(input_invalid_5, df_lane_data_not_drivable_lanes)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        
        #Check if returned values are equal to expected result (True or False depending on input)
        self.assertTrue(return_input_valid_1)
        self.assertTrue(return_input_valid_2)
        self.assertTrue(return_input_valid_3)
        
        self.assertFalse(return_input_invalid_1)
        self.assertFalse(return_input_invalid_2)
        self.assertFalse(return_input_invalid_3)
        self.assertFalse(return_input_invalid_4)
        self.assertFalse(return_input_invalid_5)
    
if __name__ == '__main__':
    unittest.main()
        
        
        