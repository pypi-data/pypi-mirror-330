from pathlib import Path
import easygui
import os
from rich import print
from rich.markdown import Markdown

from integrate_BSSD_into_OpenDRIVE.concept_steps.step_1_import_and_validate_xodr import step_1_import_and_validate_xodr
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_2_create_BSSD_root_elements import step_2_create_BSSD_root_elements
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_3_create_BSSD_segments import step_3_create_BSSD_segments
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_4_create_BSSD_lane_groups import step_4_create_BSSD_lane_groups
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_5_create_BSSD_lanes import step_5_create_BSSD_lanes
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_6_link_BSSD_and_OpenDRIVE_lanes import step_6_link_BSSD_and_OpenDRIVE_lanes
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_7_create_minimal_behavior_space_structure import step_7_create_minimal_behavior_space_structure
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_8_fill_BSSD_behavioral_attributes import step_8_fill_BSSD_behavioral_attributes
from integrate_BSSD_into_OpenDRIVE.concept_steps.step_9_save_modified_xodr import step_9_save_modified_xodr

##TOOL FOR INTEGRATING BSSD-DATA INTO AN EXISTING OpenDRIVE-FILE (VERSIONS 1.4, 1.5, 1.6, 1.7)
def main():
    #Select target file using easygui
    
    #Set current directory as default path where GUI of easygui should start
    default_path_easygui = str(Path.cwd().parent) + os.path.sep + '*.xodr'
    
    #Get filepath and open GUI at path specified in default_path_easygui with default file-type .xodr
    print()
    print('Choose a xodr-file which should be integrated with BSSD \n')
    filepath_xodr = easygui.fileopenbox(msg='Choose a xodr-file ', default = default_path_easygui)
    filepath_xodr = Path(filepath_xodr)


    #### STEP 1: Read in and validate OpenDRIVE-File
    #-------------------------------------------------------------------------------

    print(Markdown('# STEP 1: IMPORTING AND VALIDATING OpenDRIVE-FILE'))
    print()

    #Execute function for step 1
    OpenDRIVE_element, OpenDRIVE_object, driving_direction = step_1_import_and_validate_xodr(filepath_xodr)

    #### STEP 2: Create BSSD-root elements (<userData>)
    #-------------------------------------------------------------------------------
    print()
    print(Markdown('# STEP 2: CREATING BSSD-ROOT-ELEMENTS'))
    print()
    #Execute function for step 2
    df_lane_data, df_lane_data_drivable_lanes, OpenDRIVE_element = step_2_create_BSSD_root_elements(OpenDRIVE_element, OpenDRIVE_object)

    #### STEP 3: Create BSSD-segments
    #-------------------------------------------------------------------------------
    print()
    print(Markdown('# STEP 3: CREATING BSSD-SEGMENTS'))
    print()
    #Execute function for step 3
    df_segments, df_speed_limits, OpenDRIVE_element = step_3_create_BSSD_segments(df_lane_data, df_lane_data_drivable_lanes, OpenDRIVE_element,
                                                                                OpenDRIVE_object)

    #### STEP 4: Create BSSD-lane-groups
    #-------------------------------------------------------------------------------
    print()
    print(Markdown('# STEP 4: CREATING BSSD-LANE-GROUPS'))
    print()
    #Execute function for step 4
    OpenDRIVE_element = step_4_create_BSSD_lane_groups(OpenDRIVE_element)

    print()
    print(Markdown('# STEP 5: CREATING BSSD-LANES'))
    print()

    #Execute function for step 5
    df_overlappings_segments_laneSections, df_BSSD_lanes, OpenDRIVE_element = step_5_create_BSSD_lanes(df_segments, df_lane_data_drivable_lanes,
                                                                                        OpenDRIVE_element, OpenDRIVE_object) 

    #### STEP 6: Link BSSD- and OpenDRIVE-lanes
    #-------------------------------------------------------------------------------
    print()
    print(Markdown('# STEP 6: LINK BSSD- AND OpenDRIVE-LANES'))
    print()

    #Execute function for step 6
    df_link_BSSD_lanes_with_OpenDRIVE_lanes, OpenDRIVE_element = step_6_link_BSSD_and_OpenDRIVE_lanes(df_overlappings_segments_laneSections,
                                                                                                    df_BSSD_lanes, OpenDRIVE_element)      

    #### STEP 7: Create the minimal BSSD behavior space structure
    #-------------------------------------------------------------------------------
    print()            
    print(Markdown('# STEP 7: CREATE THE MINIMAL BSSD BEHAVIOR SPACE STRUCTURE'))
    print()

    #Execute function for step 7
    OpenDRIVE_element = step_7_create_minimal_behavior_space_structure(OpenDRIVE_element) 

    #### STEP 8: Fill BSSD behavioral attributes
    #-------------------------------------------------------------------------------
    print()
    print(Markdown('# STEP 8: FILL BSSD BEHAVIORAL ATTRIBUTES'))
    print()

    #Execute function for step 8
    OpenDRIVE_element = step_8_fill_BSSD_behavioral_attributes(df_lane_data, df_BSSD_lanes, df_link_BSSD_lanes_with_OpenDRIVE_lanes,
                                                                                        df_speed_limits, df_segments, driving_direction, 
                                                                                        OpenDRIVE_element, OpenDRIVE_object)

    #### STEP 9: Save modified xodr-file
    #-------------------------------------------------------------------------------
    print()
    print(Markdown('# STEP 9: SAVING MODIFIED OpenDRIVE-FILE'))
    print()

    #Execute function for step 9
    step_9_save_modified_xodr(OpenDRIVE_element, filepath_xodr)

# Execute main() function
if __name__ == '__main__':
    main()
