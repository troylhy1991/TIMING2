import os

# Step 1: create conda env for TIMING2-pipeline
command = 'conda create --yes --name TIMING2-pipeline python=3.5'
os.system(command)



# Step 2: create conda env for TIMING2-board
command = 'conda create --yes --name TIMING2-board python=2.7'
os.system(command)


# Step 3: create the C:\\timing2-temp folder
command = 'mkdir C:\\timing2-temp'
os.system(command)