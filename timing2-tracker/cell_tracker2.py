from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import os
import numpy as np


import pims
import skimage
from skimage import measure, io

from itertools import permutations



class TIMING_Cell_Tracker2:
    def __init__(self, input_folder, output_folder, t, series, count):
        self.frames = pims.ImageSequence(input_folder, process_func=None)
        self.t = t
        self.series = series
        self.cell_count = count
        self.output_folder = output_folder
        (w,h) = self.frames[0].shape
        self.frames_output = np.zeros(shape=(t,w,h), dtype=np.uint8)


        self.regions_0 = []
        self.regions_1 = []

        
    def run_cell_tracker(self):
        
        if self.cell_count == 1:
            self.frames_output = self.frames
            self.write_track_img()
            
        if self.cell_count > 1:
            for t in range(self.t-1):
                if series[t] > 0:
                    self.LAP(t)
            self.write_track_img()
        
    
    def LAP(self, t):
    
        ### STEP-1 Get Cell-ASSOCIATION-MATRIX(CAM)
        CAM = np.zeros((self.cell_count, self.cell_count))       
        
        state_1_predict = self.predict_next_state(t)
        state_1 = self.get_next_state(t)
        
        
        ### trace back and get effective record for each cell
        missing_cells = [1 for i in range(self.cell_count)]
        t0 = t
        
        for i in range(self.cell_count):
            if state_1_predict[i][2] > 0:
                missing_cells[i] = 0
                
        while sum(missing_cells) > 0 and t0 > 0:
            t0 = t0 -1
            state_0_predict = self.predict_next_state(t0)
            
            for i in range(self.cell_count):
                if state_1_predict[i][2] == 0:
                    if state_0_predict[i][2] > 0:
                        missing_cells[i] =0
                        state_1_predict[i] = state_0_predict[i]
            
            
        ### Calculate the cost MATRIX
        for i in range(self.cell_count):
            for j in range(self.cell_count):
                if state_1_predict[i][2]>0 and state_1[j][2]>0:
                    dx = state_1_predict[i][0] - state_1[j][0]
                    dy = state_1_predict[i][1] - state_1[j][1]
                    CAM[i][j] = -(dx*dx + dy*dy)
                else:
                    CAM[i][j] = -160000
                    
                    
        ### STEP-2 PARSE CAM to GET ASSO
        ASSO = self.PAS(CAM)
        
        
        ### STEP-3 UPDATE frames_output
        for i in range(self.cell_count):
            self.output_frames[t+1][self.frames[t+1] == ASSO[i]] = i + 1
    
    
    def get_detected_cell_current(self, t, N):
        try:
            self.region_0 = skimage.measure.regionprops(self.frames_output[t], intensity_image=self.frames_output[t])  
            minr, minc, maxr, maxc = self.regions_0[N-1].bbox
            xc = (minc+maxc)/2.0
            yc = (minr+maxr)/2.0
            w = maxc - minc
            h = maxr - minr
            
            if w < 4 or h < 4:
                zc = 0
            else:
                zc = 1
            
            return [xc, yc, zc]
            
        except:
            return [0,0,0]
        
        
    def get_detected_cell_next(self, t, N):
        try:
            self.region_1 = skimage.measure.regionprops(self.frames[t], intensity_image=self.frames[t])
            minr, minc, maxr, maxc = self.regions_1[N-1].bbox
            xc = (minc+maxc)/2.0
            yc = (minr+maxr)/2.0
            w = maxc - minc
            h = maxr - minr
            
            if w < 4 or h < 4:
                zc = 0
            else:
                zc = 1
            
            return [xc, yc, zc]
            
        except:
            return [0,0,0]        
        
        
    def get_current_state(self, t):
        state_0 = []
        for N in range(self.cell_count):
            temp = self.get_detected_cell_current(t,N)
            state_0.append(temp)
            
        return state_0
        
        
    def get_current_speed(self, t):
        speed_0 = []
        if t == 0:
            for N in range(self.cell_count):
                temp = [0,0]
                speed_0.append(temp)
            
        if t > 0:   ##### This could result problems
            for N in range(self.cell_count):
                temp1 = self.get_detected_cell_current(t,N)
                temp0 = self.get_detected_cell_current(t-1,N)
                if temp1[2] > 0 and temp0[2] > 0:
                    vx = temp1[0] - temp1[0]
                    vy = temp1[1] - temp1[1]
                else:
                    vx = 0
                    vy = 0
                speed_0.append([vx, vy])
            
        return speed_0            
        
        
    def get_next_state(self, t):
        state_1 = []
        for N in range(self.cell_count):
            temp = self.get_detected_cell_next(t, N)
            state_1.append(temp)
        
        return state_1        
            
        
    def predict_next_state(self, t):
        '''
        the simplest prediction of next state is to add the position with speed*decay(0.5)
        '''
        state_0 = self.get_current_state(t)
        speed_0 = self.get_current_speed(t)
        
        state_1_predict = np.array(state_0)
        
        for N in range(self.cell_count):
            state_1_predict[N][0] += speed_0[N][0]*0.5
            state_1_predict[N][1] += speed_0[N][1]*0.5
            
        return state_1_predict
        
        
        
    def PAS(self, PAA):
        '''
        Generate the track mapping results based on Patch Association Array (PAA)
        Input:  PAA A1  A2  A3
                C1  p11 p12 p13
                C2  p21 p22 p23
                C3  p31 p32 p33
        Output:
            ASSO: [0,2,1]' which means 0-->0, 1-->2, 2-->1
        '''
        n = PAA.shape[0]
        temp = range(n)

        perms = list(permutations(temp))
        scores = []
        for perm in perms:
            score = 0
            for i in range(n):
                score += PAA[i, perm[i]]
            scores.append(score)

        index = np.argmax(scores)

        return np.array(perms[index])


    def write_track_img(self):
        for t in range(0, self.t):
            fname = self.output_folder.split('\\')[-1] + '_t' + str(t+1) + '.tif'
            full_fname = self.output_folder + '\\' + fname
            io.imsave(full_fname, self.frames_output[t])

