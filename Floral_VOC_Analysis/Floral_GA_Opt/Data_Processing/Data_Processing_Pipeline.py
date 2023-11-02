from EAG_DataProcessing_Library import *

def run():
    D = '/Users/joshswore/Manduca/Multi_Channel_Data'

    s = '/Users/joshswore/Manduca/Multi_Channel_Analysis/'

    process_data(D, savedir=f'{s}/Raw/NoFilt/Data/BothChannels/',
    Norm=False, Smoothen=False, LOG=False, SUM=False,Butter=[.1, 6, 1], B_filt=False, RETURN='SAVE')

    process_data(D, savedir=f'{s}/Raw/NoFilt/Data/ChannelSum/',
    Norm=False, Smoothen=False, LOG=False, SUM=True, Butter=[.1, 6, 1], B_filt=False, RETURN='SAVE')

    process_data(D, savedir=f'{s}/Normalized/NoFilt/Data/BothChannels/',
    Norm='YY', Smoothen=False, LOG=False, SUM=False, Butter=[.1, 6, 1], B_filt=False, RETURN='SAVE')

    process_data(D, savedir=f'{s}/Normalized/NoFilt/Data/ChannelSum/',
    Norm='YY', Smoothen=False, LOG=False,  SUM=True, Butter=[.1, 6, 1], B_filt=False, RETURN='SAVE')

run()