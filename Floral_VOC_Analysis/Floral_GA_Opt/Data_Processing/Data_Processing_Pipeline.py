from EAG_DataProcessing_Library import *

def run():
    D = '/Users/joshswore/Manduca/Multi_Channel_Data'

    s = '/Users/joshswore/Manduca/Multi_Channel_Analysis/'

    #process_data(D, savedir=f'{s}/Raw/Butter.1_6/',
    #             Norm=False, Smoothen=False, LOG=False,Butter=[.1, 6], B_filt=True, RETURN='SAVE')

    process_data(D, savedir=f'{s}/Normalized/NoFilt/',
    Norm='YY', Smoothen=False, LOG=False, Butter=[.1, 6, 1], B_filt=False, RETURN='SAVE')

run()