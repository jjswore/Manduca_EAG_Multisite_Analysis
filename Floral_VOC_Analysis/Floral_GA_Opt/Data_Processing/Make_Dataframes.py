from EAG_DataProcessing_Library import *

df = EAG_df_build('/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized/NoFilt/')
save = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized_Extracted_Waves/'
if not os.path.exists(save):
    os.makedirs(save)
df.to_csv(f'{save}All_Odors.csv')
