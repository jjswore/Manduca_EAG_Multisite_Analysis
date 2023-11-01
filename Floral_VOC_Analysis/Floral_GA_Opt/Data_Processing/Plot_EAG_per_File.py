import os
from EAG_DataProcessing_Library import csv_plot
# Path to the parent directory
parent_directory = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized/NoFilt/Data/'
Save_Dir = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized/NoFilt/EAG_Plots/'

if not os.path.exists(Save_Dir):
    os.makedirs(Save_Dir)
# Use os.walk to go through each directory and subdirectory
for dirpath, dirnames, filenames in os.walk(parent_directory):
    for file in filenames:
        # Full path to the file
        file_path = os.path.join(dirpath, file)

        # Process the file
        # Add your logic here
        print(file_path)
        print(dirpath)
        if file.endswith('.csv'):
            n = file.split('.')
            csv_plot(file_path,n[0],Save_Dir)