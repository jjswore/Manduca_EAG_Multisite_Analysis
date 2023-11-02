from GA_Butter_Library import *
from EAG_PCA import EAG_PCA
from Plot_PCA import Plot_PCA
import os
#==========================================================================================
#Run the GA
print('beginning Optimization')
start = time.time()

data='/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized_Extracted_Waves/' \
     'Quality_Controlled_Data/_QC_T_0.5_reduced.csv'
odors = 'ylangylang|limonene|benzylalcohol|lemonoil'
Oabreve = 'YLimBaLo'
concentration = '1k'
SaveDir=f'/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized_Extracted_Waves/GA_Butter_Optimized/' \
        f'FDR_Fitness/{Oabreve}/'

print('checking if Save Directory exists')
if not os.path.exists(SaveDir):
    os.makedirs(SaveDir)

data_df = pd.read_csv(data, index_col=0)

DF=data_df[data_df['concentration'].str.contains(concentration)]
DF=DF[DF['label'].str.contains(odors)]
print('first split')
print(DF['label'].unique())
train_features, test_features, train_labels, test_labels =TT_Split(DF, .5)
Training_data = pd.concat([train_features, train_labels], axis=1)
Test_data = pd.concat([test_features, test_labels], axis=1)
Training_data.to_csv(f'{SaveDir}{Oabreve}_trainingDF.csv')
Test_data.to_csv(f'{SaveDir}{Oabreve}_testingDF.csv')
# Get the indices of the train_features DataFrame
train_indices = train_features.index
# Select the corresponding rows from the LLL_df
train_labels_df = DF.iloc[:,-3:].loc[train_indices]
# Concatenate train_features and train_labels_df
df = pd.concat([train_features, train_labels_df], axis=1)

params, statistics=main(data=df, POPULATION_SIZE=100, TOURNAMENT_SIZE=3, CROSS_PROB=.5, MUT_PROB=.25, G=150)

CH1 = DF.iloc[:,:9000]
CH2 = DF.iloc[:,9000:]
#META = df.iloc[:,-3:]
#CH1 = pd.concat([CH1,META], axis=1)

CH1buttered_df = apply_filter_to_dataframe(dataframe=CH1.iloc[:, :-3],
                                           lowcut=params['lowcut_c1'],
                                           highcut=params['highcut_c1'],
                                           order=params['order_c1'])

CH2buttered_df = apply_filter_to_dataframe(dataframe=CH2.iloc[:, :-3],
                                           lowcut=params['lowcut_c2'],
                                           highcut=params['highcut_c2'],
                                           order=params['order_c2'])

buttered_df = pd.concat([CH1buttered_df,CH2buttered_df], axis=1)

print('here are the parameters:', params)
print(' here are the statistics:', statistics)

end = time.time()
total_time = end - start
print("\n"+ str(total_time))

STATSDF=pd.DataFrame(statistics)
BDF = pd.concat([buttered_df, DF.iloc[:,-3:]], axis=1)
PDF = pd.DataFrame.from_dict(params, orient='index').T


PDF.to_csv(f'{SaveDir}/{Oabreve}_BestParams.csv')
BDF.to_csv(f'{SaveDir}{Oabreve}_finalDF.csv')
STATSDF.to_csv(f'{SaveDir}{Oabreve}_STATS.csv')
print('Computing PC')
EAG_PCA(BDF,SaveDir,concentration,odors, Oabreve)
Plot_PCA(DATADIR=f'{SaveDir}/PCA/',ODENOTE=Oabreve,CONC=concentration,ODORS=odors,TITLE='')
print('the entire code has finished')

## from here I need to decide how I will proceed... Do I reprocess my data? no I think I return the best
## data frame right?
