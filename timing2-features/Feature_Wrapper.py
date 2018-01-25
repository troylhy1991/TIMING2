import os
from feature_worker import generate_cell_pool
from feature_worker import generate_combined_feat_table

def TIMING_Features(Data_DIR, Dataset_Name, Dataset_Output, Dataset_Blocks, Dataset_Frames):
    
    # Step 1: Create folders to organize the feature files
    os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Output,'features','1_Well_Pool'))
    os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Output,'features','2_Cell_Pool'))
    
    # Step 2: Calculate Features
    Dataset_Output_Path = os.path.join(Data_DIR, Dataset_Name, Dataset_Output) + '\\'

    for BID in Dataset_Blocks:
        #print("Processing Features of " + BID + "......")
        #generate_well_pool(Dataset_Output_Path, BID)
        fnames = os.listdir(Dataset_Output_Path + BID + '\\label_img\\')
        Well_Number = len(fnames)/2
        for Well_ID in range(1, int(Well_Number+1)):
            generate_cell_pool(Data_DIR, Dataset_Name, Dataset_Output, Dataset_Output_Path, BID, Well_ID, Dataset_Frames)
            
    # Step 3: Generate the Combined feature Table Table_Exp.txt
    generate_combined_feat_table(Data_DIR, Dataset_Name, Dataset_Output, Dataset_Blocks, Dataset_Frames) 
    