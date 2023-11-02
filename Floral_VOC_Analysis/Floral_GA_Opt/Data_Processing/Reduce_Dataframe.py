import pandas as pd

#reduce the dataframe to include only the first 5 seconds of each channel and every other sampled point
#this will reduce both noise and the computational time it takes for the GA to finish and training of
#the classifier model
DF = pd.read_csv('/Users/joshswore/Manduca/Multi_Channel_Analysis/'
            'Normalized_Extracted_Waves/Quality_Controlled_Data/'
            '_QC_T_0.5.csv', index_col=0)
CH1 = DF.iloc[:,:5001:2]
CH2 = DF.iloc[:,9000:14001: 2]

DF_Final = pd.concat([CH1, CH2, DF.iloc[:,-3:]],axis=1)
DF_Final.to_csv('/Users/joshswore/Manduca/Multi_Channel_Analysis/'
            'Normalized_Extracted_Waves/Quality_Controlled_Data/'
            '_QC_T_0.5_reduced.csv')