import os,sys
import helper

import multiprocessing as mp

sys.path.append("../timing2-seg/")
from seg_worker import worker

def TIMING_Preprocess_Mkdir(Data_DIR, Dataset_Name, Dataset_Input, Dataset_Output, Dataset_Blocks):
    ### Making the directory storing the preprocessed images
    os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name))
    os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Input))
    os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Input, 'Parameters'))

    for block in Dataset_Blocks:
        os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Input, block))

    ### Making the directory for output and temporary result
    os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Output))
    os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Output,'features'))

    for block in Dataset_Blocks:
        os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block))
        os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'crops_8bit_s'))
        os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'label_img'))
        os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'meta'))
        os.system('mkdir ' + os.path.join(Data_DIR, Dataset_Name, Dataset_Output, block,'temp'))

        


def TIMING_Preprocess_Stack(TIMING_II_HOME, Data_Raw_DIR, Data_DIR, Dataset_Name, Dataset_Input, Dataset_Output, Dataset_Blocks, stack_tuple, channel_dict, channel_naming_dict, microscope, CORE_NUMBER):
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

    num_of_time_decimals = 2
    num_of_block_decimals = 3
    file_list_path = os.path.join(save_root_path+data_id+'_FileList/')
    
    ### Stack the images
    helper.SaveFiles( data_path, save_root_path, data_id, range_blocks, out_path, stack_tuple, channel_dict, channel_naming_dict, microscope, num_of_time_decimals, num_of_block_decimals) 

    #t1 = time.time()
    commandsGlobal = []
    for block_dir in block_list:
        if not os.path.isdir(os.path.join(out_path,block_dir)):
            os.makedirs(os.path.join(out_path,block_dir))

        filename_dict = {}
        for ch in stack_tuple:
            filename_dict[ch] = block_dir +'CH'+channel_naming_dict[ch]+'.tif'

        #### Stack Image Data ####################################
        ompNumThreads = 1 #FIXME is giving an error when reading in parallel
        commands = []
        runImageToStack = 1
        if runImageToStack:
            #print('Stacking...')
            for ch in stack_tuple:
                temp = []
                temp.append(exe_path + 'image_to_stack')
                temp.append(os.path.join(file_list_path,'inputfnames_'+block_dir+ '_' +channel_naming_dict[ch]+'.txt'))
                temp.append(os.path.join(out_path,block_dir))
                temp.append(filename_dict[ch])
                temp.append( str(ompNumThreads) )

                temp = " ".join(temp)
                commandsGlobal.append(temp)

    p = mp.Pool(processes=CORE_NUMBER)
    for command in commandsGlobal:
        p.apply_async(worker, args=(command, ))
    p.close()
    p.join()
    #print("1-STACK TIME: " +str(time.time() - t1))

    
    
    
    
def TIMING_Preprocess_Unmix(domi, leak, unmix_ratio, TIMING_II_HOME, Data_Raw_DIR, Data_DIR, Dataset_Name, Dataset_Input, Dataset_Output, Dataset_Blocks, unmix_tuple, stack_tuple, channel_dict, channel_naming_dict, CORE_NUMBER):
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
    
    ### Unmixing Steps
    commandsGlobal = []
    for block_dir in block_list:
        filename_dict = {}
        for ch in stack_tuple:
            filename_dict[ch] = block_dir +'CH'+channel_naming_dict[ch]+'.tif'
      ###### spectral unmixing ############################################################
        ompNumThreads = 1
        umx_prefix = 'umx_'
        commands = []
        runUnmixing = 1
        if runUnmixing:
            temp = []
            temp.append( os.path.join(exe_path,'unmix') )
            temp.append( os.path.join(out_path,block_dir,filename_dict[unmix_tuple[domi]]) ) # dominant channel
            temp.append( os.path.join(out_path,block_dir,filename_dict[unmix_tuple[leak]]) ) # leaked channel
            temp.append( os.path.join(out_path,block_dir,umx_prefix + filename_dict[unmix_tuple[leak]]) ) # unmixed channel output
            temp.append( str(unmix_ratio) )

            temp = " ".join(temp)
            commandsGlobal.append(temp)


    p = mp.Pool(processes=CORE_NUMBER)

    for command in commandsGlobal:
        p.apply_async(worker, args=(command, ))
    p.close()
    p.join()
    
    
    
    
def TIMING_Preprocess_BackgroundSubtract(bg_param, TIMING_II_HOME, Data_Raw_DIR, Data_DIR, Dataset_Name, Dataset_Input, Dataset_Output, Dataset_Blocks, preprocess_tuple, stack_tuple, unmix_tuple_clean, channel_dict, channel_naming_dict, CORE_NUMBER):
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
    
    
    ### Background Noise Subtraction
    commandsGlobal = []
    for block_dir in block_list:
        filename_dict = {}
        for ch in stack_tuple:
            filename_dict[ch] = block_dir +'CH'+ channel_naming_dict[ch]+'.tif'
      ##### background subtraction ############################################################
        ompNumThreads = 1
        #bg_param = 40
        bg_prefix = 'bg_'
        umx_prefix = 'umx_'
        commands = []
        runBackgroundSubstraction = 1
        if runBackgroundSubstraction:
            for ch in preprocess_tuple:
                temp = []
                temp.append(os.path.join(exe_path,'background_subtraction'))
                if ch in unmix_tuple_clean:
                    temp.append( os.path.join(out_path,block_dir,umx_prefix + filename_dict[ch]) )
                else:
                    temp.append( os.path.join(out_path,block_dir,filename_dict[ch]) )
                temp.append( os.path.join(out_path,block_dir,bg_prefix + filename_dict[ch]) )
                temp.append( str(bg_param) )
                temp.append( str(ompNumThreads) )
                #print '\tbacksubs, cmd: '+" ".join(temp)

                #subprocess.call(temp)
                temp = " ".join(temp)
                commandsGlobal.append(temp)

    p = mp.Pool(processes=CORE_NUMBER)

    for command in commandsGlobal:
        p.apply_async(worker, args=(command, ))
    p.close()
    p.join()
    
    
    
    
def TIMING_Preprocess_Enhance(min_pixel_value, max_pixel_value,TIMING_II_HOME, Data_Raw_DIR, Data_DIR, Dataset_Name, Dataset_Input, Dataset_Output, Dataset_Blocks, enhance_tuple, channel_dict, channel_naming_dict, CORE_NUMBER):
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
        for ch in enhance_tuple:
            filename_dict[ch] = block_dir +'CH'+ channel_naming_dict[ch]+'.tif'
        ##### Channel Image Enhancement #######################################################
        bg_prefix = 'bg_'
        runChannelEnhancement = 1
        if runChannelEnhancement:
            for ch in enhance_tuple:
                temp = []
                temp.append(os.path.join(exe_path,'rescale'))
                temp.append( os.path.join(out_path,block_dir,bg_prefix + filename_dict[ch]) )
                temp.append( os.path.join(out_path,block_dir,bg_prefix + filename_dict[ch]) )
                temp.append(str(min_pixel_value))
                temp.append(str(max_pixel_value))
                temp = " ".join(temp)
                commandsGlobal.append(temp)

    p = mp.Pool(processes=CORE_NUMBER)

    for command in commandsGlobal:
        p.apply_async(worker, args=(command, ))
    p.close()
    p.join()
    
    
    