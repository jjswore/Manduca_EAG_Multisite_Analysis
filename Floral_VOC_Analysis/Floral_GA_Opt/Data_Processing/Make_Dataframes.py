from EAG_DataProcessing_Library import *

def MakeDF(FILE, SAVEDIR):
    df = EAG_df_build(FILE)
    save = SAVEDIR
    if not os.path.exists(save):
        os.makedirs(save)
    df.to_csv(f'{save}All_Odors.csv')

DF=['/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized/NoFilt/Data/BothChannels/',
    '/Users/joshswore/Manduca/Multi_Channel_Analysis/Raw/NoFilt/Data/BothChannels/',
    '/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized/NoFilt/Data/ChannelSum/',
    '/Users/joshswore/Manduca/Multi_Channel_Analysis/Raw/NoFilt/Data/ChannelSum/']


SAVE=['/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized/DataFrames/BothChannels/',
     '/Users/joshswore/Manduca/Multi_Channel_Analysis/Raw/DataFrames/BothChannels/',
     '/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized/DataFrames/ChannelSum/',
     '/Users/joshswore/Manduca/Multi_Channel_Analysis/Raw/DataFrames/ChannelSum/']

for F,S in zip(DF,SAVE):
    MakeDF(F,S)

