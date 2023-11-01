import pandas as pd
from EAG_DataProcessing_Library import *

data = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized_Extracted_Waves/All_Odors.csv'
SaveDir = '/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized_Extracted_Waves/Quality_Controlled_Data/'
if not os.path.exists(SaveDir):
    print('making directory...')
    os.makedirs(SaveDir)
    print('directory made')


ThreshList=[.5,1,10]
all_df=pd.read_csv(data, index_col=0)
print(len(all_df.T))
for t in ThreshList:
        print(f"begining quality control at threshold of {t}")
        final = FFT_LSTSQ_QC(all_df, t)
        final_T = pd.DataFrame(final.T.dropna(axis=0))

        filename = f"_QC_T_{str(t)}.csv"

        final_T.to_csv(f'{SaveDir}{filename}')
