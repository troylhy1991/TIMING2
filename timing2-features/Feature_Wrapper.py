import os
from feature_worker import generate_cell_pool
from feature_worker import generate_combined_feat_table

import multiprocessing as mp

def TIMING_Features(Data_DIR, Dataset_Name, Dataset_Output, Dataset_Blocks, Dataset_Frames, CORE_NUMBER):
    
    # Step 1: Create folders to organize the feature files
    os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Output,'features','1_Well_Pool'))
    os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Output,'features','2_Cell_Pool'))
    
    # Step 2: Calculate Features
    Dataset_Output_Path = os.path.join(Data_DIR, Dataset_Name, Dataset_Output) + '\\'

    parameters = []
    
    for BID in Dataset_Blocks:
        #print("Processing Features of " + BID + "......")
        #generate_well_pool(Dataset_Output_Path, BID)
        fnames = os.listdir(Dataset_Output_Path + BID + '\\label_img\\')
        Well_Number = len(fnames)/2
        for Well_ID in range(1, int(Well_Number+1)):
            temp = []
            temp.append(Data_DIR)
            temp.append(Dataset_Name)
            temp.append(Dataset_Output)
            temp.append(Dataset_Output_Path)
            temp.append(BID)
            temp.append(Well_ID)
            temp.append(Dataset_Frames)
            parameters.append(temp)
            #generate_cell_pool(Data_DIR, Dataset_Name, Dataset_Output, Dataset_Output_Path, BID, Well_ID, Dataset_Frames)
            
    p = mp.Pool(processes=CORE_NUMBER)
    for parameter in parameters:
        p.apply_async(generate_cell_pool, args=(parameter[0], parameter[1],parameter[2],parameter[3],parameter[4],parameter[5],parameter[6],))
    p.close()
    p.join()
            
    # Step 3: Generate the Combined feature Table Table_Exp.txt
    generate_combined_feat_table(Data_DIR, Dataset_Name, Dataset_Output, Dataset_Blocks, Dataset_Frames) 
    