# This Object is used for generating the 1st stage training data set for Deep TIMING Prediction SystemError
# Author: Troy H. Lu
# Date: 04/04/2017
# 

import sys,os

import SimpleITK as sitk
import numpy as np
import random

from PyQt4.QtGui import *
from PyQt4.QtCore import *


		
class TIMING_DT_Sampler(QWidget):
	def __init__(self, dataPath, t_span, tag, E_feat, T_feat):
		super(TIMING_DT_Sampler, self).__init__()
		
		self.path = dataPath
		self.CART_path = 'CART_01'
		self.dataset = tag.dataset
		self.BID = tag.BID
		self.row = tag.R
		self.col = tag.C
		self.t = 1
		self.t_span = t_span
		self.E_Num = tag.E_Num
		self.T_Num = tag.T_Num
		
		self.E_feat = E_feat
		self.T_feat = T_feat
		
		self.setupUI()
		
	def setupUI(self):
	
		# Nanowell Information Display
		pad = "       "
		
		Info_1A = QLabel("Dataset ID       :")
		Info_1B = QLabel(self.dataset)
		H1 = QHBoxLayout()
		H1.addWidget(Info_1A)
		H1.addWidget(Info_1B)
		
		Info_2A = QLabel("Block ID           :")
		Info_2B = QLabel(pad + str(self.BID))
		H2 = QHBoxLayout()
		H2.addWidget(Info_2A)
		H2.addWidget(Info_2B)
		
		Info_3A = QLabel("Row                :")
		Info_3B = QLabel(pad + str(self.row))
		H3 = QHBoxLayout()
		H3.addWidget(Info_3A)
		H3.addWidget(Info_3B)
		
		Info_4A = QLabel("Column           :")
		Info_4B = QLabel(pad + str(self.col))
		H4 = QHBoxLayout()
		H4.addWidget(Info_4A)
		H4.addWidget(Info_4B)
		
		Info_5A = QLabel("# of Effectors :")
		Info_5B = QLabel(pad + str(self.E_Num))
		H5 = QHBoxLayout()
		H5.addWidget(Info_5A)
		H5.addWidget(Info_5B)
		
		Info_6A = QLabel("# of Targets   :")
		Info_6B = QLabel(pad + str(self.T_Num))
		H6 = QHBoxLayout()
		H6.addWidget(Info_6A)
		H6.addWidget(Info_6B)
	
	
	
	
		self.combo = QComboBox(self)
		self.combo.addItem('E1')
		self.combo.addItem('E2')
		self.combo.addItem('E3')
		self.combo.addItem('T1')
		self.combo.addItem('T2')
		self.combo.addItem('T3')
		
		death_tag = QLabel("Death Time 1: ")
		self.textbox = QLineEdit(self)
		
		death_tag2 = QLabel("Death Time 2: ")
		self.textbox2 = QLineEdit(self)
		
		self.button = QPushButton('Start Sampling', self)
		self.button.clicked.connect(self.buttonEvent)
		VBox = QVBoxLayout()
		HBox = QHBoxLayout()
		HBox.addWidget(death_tag)
		HBox.addWidget(self.textbox)
		HBox.addWidget(death_tag2)
		HBox.addWidget(self.textbox2)
		
		VBox.addLayout(H1)
		VBox.addLayout(H2)
		VBox.addLayout(H3)
		VBox.addLayout(H4)
		VBox.addLayout(H5)
		VBox.addLayout(H6)		
		VBox.addWidget(self.combo)
		VBox.addLayout(HBox)
		VBox.addWidget(self.button)
		
		self.setWindowTitle("Deep TIMING Sampler")
		self.setLayout(VBox)
		self.setFixedSize(350,450)
		self.show()

	def getImagePath(self, CH, t):
		path = self.path + "B" + str(self.BID).zfill(3) + "/crops_8bit_s/imgR"+str(self.row)+"C"+str(self.col)+"CH"+str(CH)+"/imgR"+str(self.row)+"C"+str(self.col)+"CH"+str(CH)+"_t"+str(t)+".tif"
		return path
	
	def getBGImagePath(self, CH, t):
		path = self.path + "B" + str(self.BID).zfill(3) + "/crops_8bit_s/imgR"+str(self.row)+"C"+str(self.col)+"CH"+str(CH)+"bg/imgR"+str(self.row)+"C"+str(self.col)+"CH"+str(CH)+"bg_t"+str(t)+".tif"
		return path
	
	def getLabelImagePath(self, CH, t):
		path = self.path + "B" + str(self.BID).zfill(3) +"/label_img/imgR"+str(self.row)+"C"+str(self.col)+"CH"+str(CH)+"label/imgR"+str(self.row)+"C"+str(self.col)+"CH"+str(CH)+"label_t"+str(t)+".tif"
		return path

	def read_stat_LOG(self):
		print "read stat LOG ..."
		filename = self.path + 'DT_Set/Stat_LOG.txt'
		f = open(filename,'r')
		stat_data = f.read()
		stat_data = stat_data.split('\n')
		
		line1 = stat_data[1].split('\t')
		line2 = stat_data[2].split('\t')
		
		E_P = int(line1[1])
		E_N = int(line1[2])
		T_P = int(line2[1])
		T_N = int(line2[2])
		
		return [E_P, E_N, T_P, T_N]
	
	def write_stat_LOG(self, E_P, E_N, T_P, T_N):
		print "write stat LOG ..."
		filename = self.path + 'DT_Set/Stat_LOG.txt'
		f = open(filename,'w')
		line1 = ['Stat', 'Death', 'No_Death']
		line1 = '\t'.join(line1) + '\n'
		
		line2 = ['E_Seq', str(E_P), str(E_N)]
		line2 = '\t'.join(line2) + '\n'
		
		line3 = ['T_Seq', str(T_P), str(T_N)]
		line3 = '\t'.join(line3) + '\n'
		
		f.writelines(line1)
		f.writelines(line2)
		f.writelines(line3)
		f.close()
		print "write stat LOG Done!"
	
	def write_MAP_LOG(self, cell_type, Item):
		print "write MAP LOG ..."
		# The headers Are like:
		# Sequence  # Dataset_Name   # UID  # Cell_ID  # t1    # t2   # t_death
		Header = ['#Sequence_ID','#Dataset','UID','Cell_ID','t1','t2','t_death']
		Header = '\t'.join(Header) + '\n'
		
		if cell_type == 'E':
			filename = self.path + 'DT_Set/MAP_E_LOG.txt'
		if cell_type == 'T':
			filename = self.path + 'DT_Set/MAP_T_LOG.txt'
		f = open(filename,'r')
		line1 = f.readline()
		f.close()
		line1 = line1.split('\t')
		if line1[0] != '#Sequence_ID':
			f = open(filename,'w')
			f.writelines(Header)
			f.close()
		
		# Make sure each element in Item is a string
		#line = '\t'.join(Item) + '\n'
		f = open(filename,'a')
		f.writelines(Item)
		f.close()
		print "write MAP LOG Done!"
	
	def query_MAP_LOG(self):
		print "query MAP LOG ..."
		
	def write_cell_number(self, N):
		filename = self.path + self.CART_path + '/Total_Cell_Number.txt'
		f = open(filename,'w')
		line = str(N)
		f.writelines(line)
		f.close()
	def get_cell_number(self):
		filename = self.path + self.CART_path + '/Total_Cell_Number.txt'
		if os.path.exists(filename):
			f = open(filename,'r')
			N = f.readline()
			f.close()	
			return int(N)
		else:
			return 0


	def buttonEvent(self):
		print "Sampling Button Event!"
		
		
		# get current information and write new cell number
		total_cell_number = self.get_cell_number()
		total_cell_number = total_cell_number + 1
		
		
		# which cell?
		cell_name = self.combo.currentText()
		if cell_name == 'E1':
			cell_type = 'E'
			cell_ID = 1
		if cell_name == 'E2':
			cell_type = 'E'
			cell_ID = 2
		if cell_name == 'E3':
			cell_type = 'E'
			cell_ID = 3
		if cell_name == 'T1':
			cell_type = 'T'
			cell_ID = 1
		if cell_name == 'T2':
			cell_type = 'T'
			cell_ID = 2
		if cell_name == 'T3':
			cell_type = 'T'
			cell_ID = 3		
		
		# when cell dies?
		t_death1 = int(self.textbox.text())
		t_death2 = int(self.textbox2.text())	
		pairs = [[1,t_death1],[t_death1,t_death2],[t_death2,self.t_span+1]]

		# dataset name
		str_dataset = str(self.dataset)
		# UID
		str_UID = str(self.BID)+str(self.row).zfill(2)+str(self.col).zfill(2)
		# Cell_ID
		str_cell_ID = str(cell_name)
		# N1
		str_N1 = str(t_death1 - 1)
		# N2
		str_N2 = str(t_death2 - t_death1)
		# N3			
		str_N3 = str(self.t_span + 1 - t_death2)
		
		# make directory, write txt file
		str_cell_ID = str(total_cell_number).zfill(6)
		cell_directory = self.path + self.CART_path +'/cell_' + str_cell_ID 

		os.mkdir(cell_directory)
		os.mkdir(cell_directory + '/1')
		os.mkdir(cell_directory + '/2')
		os.mkdir(cell_directory + '/3')
		
		Item = [str_dataset, str_UID, str(cell_name), str_N1, str_N2, str_N3]
		Item = '\t'.join(Item) + '\n'
		
		cell_info_filename = cell_directory + '/cell_info.txt'
		f = open(cell_info_filename,"w")
		f.writelines(Item)
		f.close()
		
		self.write_cell_number(total_cell_number)
		
		# for each pair do the following
		for i in range(0,3):
			frames = range(pairs[i][0], pairs[i][1])
			t1 = pairs[i][0]
			# for every sequence, need to generate the item list
			# sequence_ID
			if cell_type == 'E':
				# write images
				for t in frames:
					# get the bounding box plus [x,y,w,h]
					if cell_type == 'E':
						CH = 1
					# crop the patches
					label_temp = sitk.ReadImage(self.getLabelImagePath(CH,t))
					label_temp = sitk.GetArrayFromImage(label_temp)
					x1 = np.where(label_temp == cell_ID)[0].min()
					y1 = np.where(label_temp == cell_ID)[1].min()
					x2 = np.where(label_temp == cell_ID)[0].max()
					y2 = np.where(label_temp == cell_ID)[1].max()
					x_c = int((x1+x2)/2)
					y_c = int((y1+y2)/2)
						# the size of one patch is 51 by 51
					
					# write images [image, name, path]
					# CH0
					img_CH0 = sitk.ReadImage(self.getImagePath(0,t))
					img_CH0 = sitk.GetArrayFromImage(img_CH0)
					img_CH0_patch = img_CH0[x_c-25:x_c+25+1, y_c-25:y_c+25+1]
					img_CH0_patch = sitk.GetImageFromArray(img_CH0_patch)
					# CH1
					img_CH1 = sitk.ReadImage(self.getBGImagePath(1,t))
					img_CH1 = sitk.GetArrayFromImage(img_CH1)
					img_CH1_patch = img_CH1[x_c-25:x_c+25+1, y_c-25:y_c+25+1]
					img_CH1_patch = sitk.GetImageFromArray(img_CH1_patch)				
					# CH2
					img_CH2 = sitk.ReadImage(self.getBGImagePath(2,t))
					img_CH2 = sitk.GetArrayFromImage(img_CH2)
					img_CH2_patch = img_CH2[x_c-25:x_c+25+1, y_c-25:y_c+25+1]
					img_CH2_patch = sitk.GetImageFromArray(img_CH2_patch)				
					# CH3
					img_CH3 = sitk.ReadImage(self.getImagePath(3,t))
					img_CH3 = sitk.GetArrayFromImage(img_CH3)
					img_CH3_patch = img_CH3[x_c-25:x_c+25+1, y_c-25:y_c+25+1]
					img_CH3_patch = sitk.GetImageFromArray(img_CH3_patch)				
					# prepare the image path and name
					fname_CH0 = cell_directory + '/' + str(i+1) + '/CH0_' + str(t-t1+1).zfill(3) + '.tif'
					fname_CH1 = cell_directory + '/' + str(i+1) + '/CH1_' + str(t-t1+1).zfill(3) + '.tif'
					fname_CH2 = cell_directory + '/' + str(i+1) + '/CH2_' + str(t-t1+1).zfill(3) + '.tif'
					fname_CH3 = cell_directory + '/' + str(i+1) + '/CH3_' + str(t-t1+1).zfill(3) + '.tif'
					sitk.WriteImage(img_CH0_patch, fname_CH0)
					sitk.WriteImage(img_CH1_patch, fname_CH1)
					sitk.WriteImage(img_CH2_patch, fname_CH2)
					sitk.WriteImage(img_CH3_patch, fname_CH3)
					
		# write total_cell_counts
		self.write_cell_number(total_cell_number)
		
		print "Sampling Done!"
			
		


class Nanowell_Tag():
	def __init__(self):
		self.dataset = 'Dataset ID'
		self.BID = 1
		self.R = 1
		self.C = 1
		self.E_Num = 0
		self.T_Num = 0
		self.tSeek1 = 0
		self.TimInt = 0
		self.DInt = 0
		self.EDInt = 0
		
def main():
	app = QApplication(sys.argv)
	path = "C:\\Users\\Hengyang\\Desktop\\TIMING 1.0\\Dataset\\20160211_GR_01_CARTAR_M\\"
	BID = 1
	row = 3
	col = 1
	t = 1
	t_span = 72
	tag = Nanowell_Tag()
	Sampler = TIMING_DT_Sampler(path,t_span,tag)
	sys.exit(app.exec_())
	

if __name__ == '__main__':
	main()
		
		
		
		