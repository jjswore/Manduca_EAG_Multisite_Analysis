import os
from EAG_SIngleChannel_DataProcessing_Library import csv_plot
# Path to the parent directory
parent_directory = '/Users/joshswore/Manduca/Multi_Channel_Analysis/EAG_Waves/Normalized/NoFilt/DATA/'

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
            csv_plot(file_path,n[0],f'/Users/joshswore/Manduca/Single_Channel_Analysis/EAG_Waves/Normalized/NoFilt/EAG_Plots/')