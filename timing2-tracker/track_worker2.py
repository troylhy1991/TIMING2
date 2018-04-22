import sys,os
sys.path.append('.')
from cell_tracker2 import TIMING_Cell_Tracker2

def track_worker2(input_path, output_path, prefix, t, series, count):
    Tracker = TIMING_Cell_Tracker2(os.path.join(input_path, prefix + '*.tif'), output_path, t, series, count)
    Tracker.run_cell_tracker()
    del Tracker
