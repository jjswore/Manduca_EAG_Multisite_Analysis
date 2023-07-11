import time
from Manduca_Multisite_EAG_Analysis.Floral_VOC_Analysis.Floral_GA_Opt.Classification.GA_ButterCLF_Library import *

start = time.time()

filepath ='/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Quality_Controlled_Data/NoFilter/YY_Normalized/Both_Channels/_QC_T_1000.csv'

LLL_df = pd.read_csv(filepath, index_col=0)
print('first split')
train_features, test_features, train_labels, test_labels =TT_Split(LLL_df)
# Get the indices of the train_features DataFrame
train_indices = train_features.index
# Select the corresponding rows from the LLL_df
train_labels_df = LLL_df.iloc[:,-3:].loc[train_indices]
# Concatenate train_features and train_labels_df
df = pd.concat([train_features, train_labels_df], axis=1)
params,statistics=main(data=df, POPULATION_SIZE=1000, TOURNAMENT_SIZE=3, CROSS_PROB=.5, MUT_PROB=.15, G=20)

print('here are the parameters:', params)
print(' here are the statistics:', statistics)

end = time.time()
total_time = end - start
print("\n"+ str(total_time))

STATSDF=pd.DataFrame(statistics)
PDF=pd.DataFrame(params)

PDF.to_csv('Cov_health_QC1_BestParams.csv')
STATSDF.to_csv('Cov_health_Q1_STATS')


