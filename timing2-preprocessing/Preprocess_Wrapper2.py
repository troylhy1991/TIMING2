import os,sys
import helper

import multiprocessing as mp

sys.path.append("../timing2-seg/")
from seg_worker import worker


def TIMING_Preprocess_Clip_Enhance(min_clip_value, max_clip_value, min_pixel_value, max_pixel_value,TIMING_II_HOME, Data_Raw_DIR, Data_DIR, Dataset_Name, Dataset_Input, Dataset_Output, Dataset_Blocks, clip_enhance_tuple, channel_dict, channel_naming_dict, CORE_NUMBER):
    ### Define some internal parameters, legacy issue
    root_path = Data_Raw_DIR + '\\'
    save_root_path = Data_DIR + '\\'
    data_id = Dataset_Name
    out_path = save_root_path + data_id + '\\IN\\'
    #range_blocks = range(1,len(Dataset_Blocks)+1)
    range_blocks = [int(x[1:4]) for x in Dataset_Blocks]

    exe_path = TIMING_II_HOME + 'timing2-preprocessing\\'
    data_path = root_path + data_id + '\\'
    block_list = Dataset_Blocks

    ### Enhance Channel
    commandsGlobal = []
    for block_dir in block_list:
        filename_dict = {}
        for ch in clip_enhance_tuple:
            filename_dict[ch] = block_dir +'CH'+ channel_naming_dict[ch]+'.tif'
        ##### Channel Image Enhancement #######################################################
        bg_prefix = 'bg_'
        runChannelEnhancement = 1
        if runChannelEnhancement:
            for ch in clip_enhance_tuple:
                temp = []
                temp.append(os.path.join(exe_path,'rescale_clip'))
                temp.append( os.path.join(out_path,block_dir,bg_prefix + filename_dict[ch]) )
                temp.append( os.path.join(out_path,block_dir,bg_prefix + filename_dict[ch]) )
                temp.append(str(min_pixel_value))
                temp.append(str(max_pixel_value))
                temp.append(str(min_clip_value))
                temp.append(str(max_clip_value))
                temp = " ".join(temp)
                commandsGlobal.append(temp)

    p = mp.Pool(processes=CORE_NUMBER)

    for command in commandsGlobal:
        p.apply_async(worker, args=(command, ))
    p.close()
    p.join()
