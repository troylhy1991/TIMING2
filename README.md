
## What is TIMING?
TIMING is the acronym for Time-lapse Imaging Microscopy in Nanowell Grids. It is a high-throughput single-cell imaging and image processing protocol developed and maintained by [Single-Cell Lab](http://singlecell.chee.uh.edu/) and [Farsight Group](http://www.farsight-toolkit.org/wiki/Main_Page) at University of Houston, Houston, Texas.

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

## How about TIMING2?
TIMING2 is all about the updates and improvements of TIMING pipeline, the software part of the whole TIMING protocol. Compared with TIMING pipeline, we have the following key improvements:

(1) A unified TIMING2-pipeline wrapped up in Jupyter Notebook, where user can run different steps easily;

(2) Updated Modules, TIMING2-pipeline have several modules in TIMING pipeline updated, which are faster, easier and more robust
    
 * [EZ_Unmixer](https://github.com/troylhy1991/EZ_Unmixer), we use an interactive tool EZ_Unmixer to calculate the spectral leakage ratio \lambda, and do linear subtraction with \lambda using the pipeline;
    
 * Nanowell detection and cropping using faster r-cnn, a more robust nanowell detection module using state-of-art object detector based on convolutional neural networks; fully automatic and no input parameter configuration;
    
![Faster R-CNN Nanowell](https://github.com/troylhy1991/TIMING2/blob/master/appendix/faster-rcnn.JPG)
    
 * GPU-accelerated Cell segmentation module
    
(3) New Modules, TIMING2 has several new modules which is not included in TIMING,
    
 * Cell death detection without fluorescent cell death marker, using convolutional neural networks based image classifier, TIMING2 is able to detect cell death with 87% accuracy by looking at phase contrast channel;
    
 * TIMING2-board, a visualization and re-editing system
 
![TIMING2-board](https://github.com/troylhy1991/TIMING2/blob/master/appendix/TIMING2-board.JPG)    

(4) Cross-Platform compatibility

![Cross Platform](https://github.com/troylhy1991/TIMING2/blob/master/appendix/Platform.jpg)  

## Requirements:


## Installation:


## Usage:


## Troubleshooting:


## Contact:
 Hengyang Lu: hlu9@uh.edu
