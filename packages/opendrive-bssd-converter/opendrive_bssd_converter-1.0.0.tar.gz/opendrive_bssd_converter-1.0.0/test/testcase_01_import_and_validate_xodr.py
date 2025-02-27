import unittest
from pathlib import Path
from lxml import etree
from importlib_resources import files as resources_files

from integrate_BSSD_into_OpenDRIVE.concept_steps.step_1_import_and_validate_xodr import validate_against_OpenDRIVE_version


class TestcaseImportValidateXODR(unittest.TestCase):
    """
    TESTCASE 01: Check whether a valid/invalid xodr of versions 1.4/1.5/1.6/1.7 is recognized as valid/invalid by 
    step 1 of BSSD integration into OpenDRIVE (Importing and validating OpenDRIVE-file).
    
    This includes:
        - Test 1: Check whether valid xodr of version 1.4 is recognized as valid
        - Test 2: Check whether invalid xodr of version 1.4 is recognized as invalid
        - Test 3: Check whether valid xodr of version 1.5 is recognized as valid
        - Test 4: Check whether invalid xodr of version 1.5 is recognized as invalid
        - Test 5: Check whether valid xodr of version 1.6 is recognized as valid
        - Test 6: Check whether invalid xodr of version 1.6 is recognized as invalid
        - Test 7: Check whether valid xodr of version 1.7 is recognized as valid
        - Test 8: Check whether invalid xodr of version 1.7 is recognized as invalid
    """
       
    def test_validate_valid_xodr_1_4(self):
        """
        Test 1: Check whether valid xodr of version 1.4 is recognized as valid. The input xodr consists of one road with two lanes.
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        #Filename of valid xodr
        filename_xodr = 'testcase_01_valid_1_4'
        
        #Filepath to valid xodr with version 1.4
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')

        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Filepath to xsd-file for OpenDRIVE 1.4
        filepath_xsd_1_4 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('OpenDRIVE_1.4H_Schema_Files.xsd')
        #Read in OpenDRIVE-schema-file (lxml)
        tree_OpenDRIVE_schema_1_4 = etree.parse(str(filepath_xsd_1_4))
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        #Get result of function to validate OpenDRIVE against xsd --> Returns True or False 
        test_result = validate_against_OpenDRIVE_version(tree_xodr, tree_OpenDRIVE_schema_1_4)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Check if test_result is equal to expected result (= True)
        self.assertTrue(test_result, 'The valid OpenDRIVE-file "' + filename_xodr + '.xodr", Version 1.4 was marked as invalid')
     
    def test_validate_invalid_xodr_1_4(self):
        """
        Test 2: Check whether invalid xodr of version 1.4 is recognized as invalid. The input xodr consists of one road with two lanes. One <lane>-
        element has no attribute "id"
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        #Filename of valid xodr
        filename_xodr = 'testcase_01_invalid_1_4'
        
        #Filepath to invalid xodr with version 1.4
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.4', filename_xodr +'.xodr')
       
        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Filepath to xsd-file for OpenDRIVE 1.4
        filepath_xsd_1_4 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('OpenDRIVE_1.4H_Schema_Files.xsd')
        #Read in OpenDRIVE-schema-file (lxml)
        tree_OpenDRIVE_schema_1_4 = etree.parse(str(filepath_xsd_1_4))
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        #Get result of function to validate OpenDRIVE against xsd --> Returns True or False 
        test_result = validate_against_OpenDRIVE_version(tree_xodr, tree_OpenDRIVE_schema_1_4)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Check if test_result is equal to expected result (= False)
        self.assertFalse(test_result, 'The invalid OpenDRIVE-file "' + filename_xodr + '.xodr", Version 1.4 was marked as valid')
      
    def test_validate_valid_xodr_1_5(self):
        """
        Test 3: Check whether valid xodr of version 1.5 is recognized as valid. The input xodr consists of one road with two lanes.
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        #Filename of valid xodr
        filename_xodr = 'testcase_01_valid_1_5'
        
        #Filepath to valid xodr with version 1.5
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.5', filename_xodr +'.xodr')
        
        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Filepath to xsd-file for OpenDRIVE 1.5
        filepath_xsd_1_5 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('OpenDRIVE_1.5_Schema_Files.xsd')
        #Read in OpenDRIVE-schema-file (lxml)
        tree_OpenDRIVE_schema_1_5 = etree.parse(str(filepath_xsd_1_5))
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        #Get result of function to validate OpenDRIVE against xsd --> Returns True or False 
        test_result = validate_against_OpenDRIVE_version(tree_xodr, tree_OpenDRIVE_schema_1_5)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Check if test_result is equal to expected result (= True)
        self.assertTrue(test_result, 'The valid OpenDRIVE-file "' + filename_xodr + '.xodr", Version 1.5 was marked as invalid')
        
    #Testcase 4: Validate an invalid xodr with version 1.5
    def test_validate_invalid_xodr_1_5(self):
        """
        Test 4: Check whether invalid xodr of version 1.5 is recognized as invalid. The input xodr consists of one road with two lanes. One <lane>-
        element has no attribute "id"
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        #Filename of invalid xodr
        filename_xodr = 'testcase_01_invalid_1_5'
        
        #Filepath to valid xodr with version 1.5
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.5', filename_xodr +'.xodr')
                    
        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Filepath to xsd-file for OpenDRIVE 1.5
        filepath_xsd_1_5 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('OpenDRIVE_1.5_Schema_Files.xsd')
        
        #Read in OpenDRIVE-schema-file (lxml)
        tree_OpenDRIVE_schema_1_5 = etree.parse(str(filepath_xsd_1_5))
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        #Get result of function to validate OpenDRIVE against xsd --> Returns True or False 
        test_result = validate_against_OpenDRIVE_version(tree_xodr, tree_OpenDRIVE_schema_1_5)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Check if test_result is equal to expected result (= False)
        self.assertFalse(test_result, 'The invalid OpenDRIVE-file "' + filename_xodr + '.xodr", Version 1.5 was marked as valid')
        

    def test_validate_valid_xodr_1_6(self):
        """
        Test 5: Check whether valid xodr of version 1.6 is recognized as valid. The input xodr is the example file "Ex_Pedestrian_Crossing.xodr"
        from the official OpenDRIVE-specification (Version 1.6).
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        #Filename of valid xodr
        filename_xodr = 'testcase_01_valid_1_6'
        
        #Filepath to valid xodr with version 1.6
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.6', filename_xodr +'.xodr')
        
        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Filepath to xsd-file for OpenDRIVE 1.7 --> Schema for version 1.6 doesn't work properly --> But schema for version 1.7 can be used
        filepath_xsd_1_6 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('opendrive_17_core.xsd')
        #Read in OpenDRIVE-schema-file (lxml)
        tree_OpenDRIVE_schema_1_6 = etree.parse(str(filepath_xsd_1_6))
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        #Get result of function to validate OpenDRIVE against xsd --> Returns True or False 
        test_result = validate_against_OpenDRIVE_version(tree_xodr, tree_OpenDRIVE_schema_1_6)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Check if test_result is equal to expected result (= True)
        self.assertTrue(test_result, 'The valid OpenDRIVE-file "' + filename_xodr + '.xodr", Version 1.6 was marked as invalid')
        

    def test_validate_invalid_xodr_1_6(self):
        """
        Test 6: Check whether invalid xodr of version 1.6 is recognized as invalid. The input xodr is a modified version of 
        the example file "Ex_Pedestrian_Crossing.xodr" from the official OpenDRIVE-specification (Version 1.6).
        One <lane>-element has no attribute "id"
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        #Filename of invalid xodr
        filename_xodr = 'testcase_01_invalid_1_6'
        
        #Filepath to valid xodr with version 1.6
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.6', filename_xodr +'.xodr')
                    
        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Filepath to xsd-file for OpenDRIVE 1.7 --> Schema for version 1.6 doesn't work properly --> But schema for version 1.7 can be used
        filepath_xsd_1_6 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('opendrive_17_core.xsd')
        
        #Read in OpenDRIVE-schema-file (lxml)
        tree_OpenDRIVE_schema_1_6 = etree.parse(str(filepath_xsd_1_6))
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        #Get result of function to validate OpenDRIVE against xsd --> Returns True or False 
        test_result = validate_against_OpenDRIVE_version(tree_xodr, tree_OpenDRIVE_schema_1_6)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Check if test_result is equal to expected result (= False)
        self.assertFalse(test_result, 'The invalid OpenDRIVE-file "' + filename_xodr + '.xodr", Version 1.6 was marked as valid')
      
    
    def test_validate_valid_xodr_1_7(self):
        """
        Test 7: Check whether valid xodr of version 1.7 is recognized as valid. The input xodr is the example file "Ex_Pedestrian_Crossing.xodr"
        from the official OpenDRIVE-specification (Version 1.7).
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        #Filename of valid xodr
        filename_xodr = 'testcase_01_valid_1_7'
        
        #Filepath to valid xodr with version 1.7
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.7', filename_xodr +'.xodr')
        
        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Filepath to xsd-file for OpenDRIVE 1.7
        filepath_xsd_1_7 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('opendrive_17_core.xsd')
        #Read in OpenDRIVE-schema-file (lxml)
        tree_OpenDRIVE_schema_1_7 = etree.parse(str(filepath_xsd_1_7))
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        #Get result of function to validate OpenDRIVE against xsd --> Returns True or False 
        test_result = validate_against_OpenDRIVE_version(tree_xodr, tree_OpenDRIVE_schema_1_7)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Check if test_result is equal to expected result (= True)
        self.assertTrue(test_result, 'The valid OpenDRIVE-file "' + filename_xodr + '.xodr", Version 1.7 was marked as invalid')
        

    def test_validate_invalid_xodr_1_7(self):
        """
        Test 8: Check whether invalid xodr of version 1.7 is recognized as invalid. The input xodr is a modified version of 
        the example file "Ex_Pedestrian_Crossing.xodr" from the official OpenDRIVE-specification (Version 1.7).
        One <lane>-element has no attribute "id"
        """
        
        #### 1. ARRANGE
        #-----------------------------------------------------------------------
        
        #Filename of invalid xodr
        filename_xodr = 'testcase_01_invalid_1_7'
        
        #Filepath to valid xodr with version 1.7
        filepath_xodr = Path.joinpath(Path(__file__).parent, 'test_data', 'xodr_files', '1.7', filename_xodr +'.xodr')
                    
        #Read in xodr-file (lxml)
        tree_xodr = etree.parse(str(filepath_xodr))
        
        #Filepath to xsd-file for OpenDRIVE 1.7
        filepath_xsd_1_7 = resources_files('integrate_BSSD_into_OpenDRIVE.data').joinpath('opendrive_17_core.xsd')
        
        #Read in OpenDRIVE-schema-file (lxml)
        tree_OpenDRIVE_schema_1_7 = etree.parse(str(filepath_xsd_1_7))
        
        #### 2. ACT
        #-----------------------------------------------------------------------
        
        #Get result of function to validate OpenDRIVE against xsd --> Returns True or False 
        test_result = validate_against_OpenDRIVE_version(tree_xodr, tree_OpenDRIVE_schema_1_7)
        
        #### 3. ASSERT
        #-----------------------------------------------------------------------
        
        #Check if test_result is equal to expected result (= False)
        self.assertFalse(test_result, 'The invalid OpenDRIVE-file "' + filename_xodr + '.xodr", Version 1.7 was marked as valid')
    
if __name__ == '__main__':
    unittest.main()
        
        
        