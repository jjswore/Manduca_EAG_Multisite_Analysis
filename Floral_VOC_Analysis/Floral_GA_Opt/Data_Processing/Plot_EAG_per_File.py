import os
from EAG_DataProcessing_Library import csv_plot
# Path to the parent directory


parent_directory = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized/NoFilt/Data/ChannelSum/'
Save_Dir = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized/NoFilt/EAG_Plots/ChannelSum/'

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
            csv_plot(file_path,n[0],ylim=[-2.5,2.5],SDir=Save_Dir)

parent_directory = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized/NoFilt/Data/BothChannels/'
Save_Dir = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized/NoFilt/EAG_Plots/BothChannels/'

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
            csv_plot(file_path,n[0],ylim=[-1.5,1.5],SDir=Save_Dir)


parent_directory = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Raw/NoFilt/Data/ChannelSum/'
Save_Dir = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Raw/NoFilt/EAG_Plots/ChannelSum/'

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
            csv_plot(file_path,n[0],ylim=[-250,100],SDir=Save_Dir)

parent_directory = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Raw/NoFilt/Data/BothChannels/'
Save_Dir = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Raw/NoFilt/EAG_Plots/BothChannels/'

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
            csv_plot(file_path,n[0],ylim=[-250,100],SDir=Save_Dir)



