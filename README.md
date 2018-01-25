
# What is TIMING?
TIMING is the acronym for Time-lapse Imaging Microscopy in Nanowell Grids. It is a high-throughput single-cell imaging and image processing protocol developed and maintained by [Single-Cell Lab](http://singlecell.chee.uh.edu/), [Farsight Group](http://www.farsight-toolkit.org/wiki/Main_Page) and [STIM Laboratory](http://stim.ee.uh.edu/) at University of Houston, Houston, Texas.

In TIMING, we put cells in controlled microenvironment, nanowells. The nanowells have the size of 50 um by 50 um, and in one nanowell, there are usually less than 10 cells in total. Different cells are stained with different fluorescent bio-markers. We do 4D imaging (X,Y,w,t) of the cells and analyze their interactions.

![Nanowell Slides](https://github.com/troylhy1991/TIMING2/blob/master/appendix/Slides.JPG)

The nanowells are fabricated on PDMS slides and in one slide there are approximately 100,000 nanowells. Automatic analysis of huge amount of imaging data is necessary. We build a image processing and analysis pipeline to achieve this. The pipeline contains following steps:
  * Image preprocessing, including spectral unmixing, background subtraction and contrast enhancement
  * Cell Segmentation
  * Cell Tracking
  * Cell Feature Calculation

![](https://github.com/troylhy1991/TIMING2/blob/master/appendix/TIMING.JPG)

TIMING could boost immunotherapy. For example, we use TIMING to quantify the killing efficacy of CAR T-cells (Chimeric Antigen Receptor T Cell, a geneticlly modified human T cell) and implement the optimal reprogrammed CAR T-cell for a specific patient.

For more details, see our previous [Bioinformatics paper](https://academic.oup.com/bioinformatics/article/31/19/3189/212047)

# How about TIMING2?
TIMING2 is all about the updates and improvements of TIMING pipeline, the software part of the whole TIMING protocol. Compared with TIMING pipeline, we have the following key improvements:

(1) A unified TIMING2-pipeline wrapped up in Jupyter Notebook, where user can run different steps easily;

(2) Updated Modules, TIMING2-pipeline have several modules in TIMING pipeline updated, which are faster, easier and more robust
    
 * [EZ_Unmixer](https://github.com/troylhy1991/EZ_Unmixer), we use an interactive tool EZ_Unmixer to calculate the spectral leakage ratio \lambda, and do linear subtraction with \lambda using the pipeline;
    
 * Nanowell detection and cropping using faster r-cnn, a more robust nanowell detection module using state-of-art object detector based on convolutional neural networks; fully automatic and no input parameter configuration;

<p align="center">
  <img src="https://github.com/troylhy1991/TIMING2/blob/master/appendix/faster-rcnn.JPG" width="400">
</p>

 * GPU-accelerated Cell segmentation module
    
(3) New Modules, TIMING2 has several new modules which is not included in TIMING,
    
 * Cell death detection without fluorescent cell death marker, using convolutional neural networks based image classifier, TIMING2 is able to detect cell death with 87% accuracy by looking at phase contrast channel;
    
 * TIMING2-board, a visualization and re-editing system
 
![TIMING2-board](https://github.com/troylhy1991/TIMING2/blob/master/appendix/TIMING2-board.JPG)    

(4) Cross-Platform compatibility

<p align="center">
  <img src="https://github.com/troylhy1991/TIMING2/blob/master/appendix/Platform.jpg" width="400">
</p>

# Requirements:

* 64-bit computer with at least 2GHz processor running Windows, Linux or Mac
* CUDA-enabled GPU, memory >= 4 GB recommended
* Hard drive storage >= 2TB, solid-state hard drive strongly recommended

# Installation:

(1) Download this repository and put the folder say C:\Users\TIMING2\

(2) Download auxiliary modules, and copy the folders to C:\Users\TIMING2\

 * [timing2-crop](https://drive.google.com/open?id=1JF5EzTBGnQCUoflwbl9hmdB-1xd-6TII)
 
 * [timing2-seg](https://drive.google.com/open?id=1wZuUeq0VIsF-GQw5F5OoMAe0iFbnwQe9)
 
(3) Download and install [Anaconda](https://www.anaconda.com/download/?lang=en-us)

(4) Create the environments for TIMING2-pipeline and TIMING2-board, open Anaconda Prompt, change to TIMING2 home directory C:\Users\TIMING2\, and type python setup_env.py

(5) Set up TIMING2-pipeline, in the prompt, type activate TIMING2-pipeline, and then type python setup_timing2_pipeline.py

(6) Open another Anaconda Prompt, change to TIMING2 home directory, type activate TIMING2-board, and then type python setup_timing2_board.py (independent from step 5)

(7) Have a cup of coffee, will be ready in several minutes.

# Usage:

(1) Download the [TEST Dataset](https://drive.google.com/open?id=1SAnS3vMh7EpoRCJpZkm2d-t1bji1uvyj), and put it in the folder, say C:\Users\TIMING2_Datasets_Raw\; also, make another directory for the results C:\Users\TIMING2_Datasets_Results\;

(2) Run [TIMING2-pipeline Jupyter Notebook](https://github.com/troylhy1991/TIMING2/blob/master/TIMING_II_PIPELINE_DEMO_Updated_1.ipynb), make sure to change the following parameters to run the test:
 
 * CORE_NUMBER = # of CORES available on your machine
 
 * TIMING_II_Home = "C:\\Users\\TIMING2\\"
 
 * Data_Raw_DIR = "C:\\Users\\TIMING2_Datasets_Raw\\"
 
 * Data_DIR = "C:\\Users\\TIMING2_Datasets_Results\\"
 
 (3) Visualize the results; Open a new Anaconda Prompt, activate the visualization and editing environment by typing activate TIMING2-
board, change directory to typing cd C:\\Users\\TIMING2\\timing2-viewer\\2.0\\. Start the visualization system typing python TIMING_Main.py, and you will see a small widget window popping up.
 
# Contact:
 Hengyang Lu: hlu9@uh.edu
