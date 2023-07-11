import time
from Manduca_Multisite_EAG_Analysis.Disease_VOC_Analysis.Classification.GA_ButterCLF_Library import *

start = time.time()

LLL_df = pd.read_csv('LLL_QC_T_1.csv', index_col=0)
train_features, test_features, train_labels, test_labels =TT_Split(LLL_df)
# Get the indices of the train_features DataFrame
train_indices = train_features.index
# Select the corresponding rows from the LLL_df
train_labels_df = LLL_df.iloc[:,-3:].loc[train_indices]
# Concatenate train_features and train_labels_df
df = pd.concat([train_features, train_labels_df], axis=1)
params,statistics=main(data=df, POPULATION_SIZE=500, TOURNAMENT_SIZE=3, CROSS_PROB=.5, MUT_PROB=.25, G=20)

print('here are the parameters:', params)
print(' here are the statistics:', statistics)

end = time.time()
total_time = end - start
print("\n"+ str(total_time))

STATSDF=pd.DataFrame(statistics)
PDF=pd.DataFrame(params)

PDF.to_csv('LLL_QC1_BestParams.csv')
STATSDF.to_csv('LLL_Q1_STATS')
