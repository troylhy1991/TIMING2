import os
import multiprocessing as mp
from track_worker import track_worker

def TIMING_Tracker(Data_DIR, Dataset_Name, Dataset_Output, Dataset_Blocks, Dataset_Frames, CORE_NUMBER):
    # Step 1: Make directory for tracking results
    for block in Dataset_Blocks:
        bg_img_dir = os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'crops_8bit_s\\')
        temp_track_dir = os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'label_img\\')
        os.system('mkdir ' + temp_track_dir)
        folder_names = os.listdir(bg_img_dir)
        for folder_name in folder_names:
            if 'bg' in folder_name:
                os.system('mkdir '+ temp_track_dir + folder_name)
                
    # Step 2: Start the tracking session with parallel setup
    # Prepare the parameter list  
    parameters = []
    for block in Dataset_Blocks:
        temp_seg_dir = os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'temp\\segmentation\\')
        temp_track_dir = os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'label_img\\')

        # load the list of valid nanowells
        f = open(os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'meta\\valid_nanowell_ID.txt'))
        valid_nanowell_ID = f.readlines()[0].rstrip('\n').split('\t')
        valid_nanowell_ID = [int(i) for i in valid_nanowell_ID]
        f.close()

        for ID in valid_nanowell_ID:

            f = open(os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'meta\\cell_hist\\imgNo'+str(ID)+'bg.txt'))
            ET_count = f.readlines()
            f.close()
            E_count = int(ET_count[0].rstrip('\n').split('\t')[0])
            T_count = int(ET_count[1].rstrip('\n').split('\t')[0])

            if E_count != 0:

                folder_name = 'imgNo'+str(ID)+'CH1bg'

                f = open(os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'meta\\cell_count\\imgNo'+str(ID)+'CH1bg.txt'))
                E_series = f.readlines()
                f.close()
                E_series = E_series[0].rstrip('\n').split('\t')
                E_series = [int(i) for i in E_series]

                temp1 = temp_seg_dir + folder_name
                temp2 = temp_track_dir + folder_name
                temp3 = folder_name + '_t'
                temp4 = Dataset_Frames
                temp5 = E_series

                parameters.append([temp1, temp2, temp3, temp4, temp5])

            if T_count != 0:

                folder_name = 'imgNo'+str(ID)+'CH2bg'

                f = open(os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'meta\\cell_count\\imgNo'+str(ID)+'CH2bg.txt'))
                T_series = f.readlines()
                f.close()
                T_series = T_series[0].rstrip('\n').split('\t')
                T_series = [int(i) for i in T_series]

                temp1 = temp_seg_dir + folder_name
                temp2 = temp_track_dir + folder_name
                temp3 = folder_name + '_t'
                temp4 = Dataset_Frames
                temp5 = T_series

                parameters.append([temp1, temp2, temp3, temp4, temp5])

    #t1 = time.time()

    # Start the parallel threads
    p = mp.Pool(processes=CORE_NUMBER)
    for parameter in parameters:
        p.apply_async(track_worker, args=(parameter[0], parameter[1],parameter[2],parameter[3],parameter[4],))
    p.close()
    p.join()

    #print("CELL TRACKING TIME: " +str(time.time() - t1))