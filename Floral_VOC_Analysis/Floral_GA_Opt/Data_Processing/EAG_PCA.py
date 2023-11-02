import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pickle
import os

def EAG_PCA(DATA, SAVEDIR, CONC, ODORS, OD):
    concentration = CONC
    odors = ODORS
    odenote = OD
    data = DATA
    SaveDir = f'{SAVEDIR}PCA/'

    if not os.path.exists(SaveDir):
        os.makedirs(SaveDir)

    if isinstance(data, str):
        # Additional check to see if it ends with '.csv' if needed
        if data.endswith('.csv'):
            DF = pd.read_csv(data, index_col=0)
        else:
            print("String provided is not a path to a CSV file.")
            return

        # If data is already a dataframe
    elif isinstance(data, pd.DataFrame):
        DF = DATA

    else:
        print("Unsupported data format.")
        return
    # load our data frame into the program


    All_DF = DF[DF['concentration'].str.contains(concentration)]
    All_DF = All_DF[All_DF['label'].str.contains(odors)]
    # convert the data frame into a usable format for scaling
    All_DF2 = All_DF.iloc[:, :-3].convert_dtypes(float).astype(float)

    # scale the data to calculate the principal componenets
    All_DF_Scaled = pd.DataFrame(StandardScaler().fit_transform(All_DF2),
                                 columns=All_DF2.columns,
                                 index=All_DF2.index)
    # set the PCA parameters
    PCA_set = PCA(n_components=100)

    All_DF_PCAResults = PCA_set.fit_transform(All_DF_Scaled)
    print(PCA_set.explained_variance_ratio_)
    # Save our PCA object
    reader = open(f'{SaveDir}{odenote}_PCA.pickle', 'wb')
    pickle.dump(obj=PCA_set, file=reader)
    reader.close()
    All_DF_PCA_DF = pd.DataFrame(data=All_DF_PCAResults, index=All_DF_Scaled.index)

    for x, y in zip(range(100), range(1, 101)):
        All_DF_PCA_DF.rename({x: f'PC {y}'}, axis=1, inplace=True)


    All_DF_PCA_DF = pd.concat([All_DF_PCA_DF,All_DF.iloc[:,-3:]], axis=1 )
    print(All_DF_PCA_DF.columns)
    All_DF_PCA_DF.to_csv(f'{SaveDir}{odenote}_PCA.csv')
    return All_DF_PCA_DF, PCA_set

#=========================================================================================================
'''data='/Users/joshswore/Manduca/MultiChannel/WildType/Floral/Quality_Controlled_Data/No_Filter/YY_Normalized/Both_Channels/_QC_T_1.csv'
odors = 'lemonoil|limonene|linalool'
Odenote = 'LLL'
concentration = '1k'
SaveDir='/Users/joshswore/Manduca/TEST/'
EAG_PCA(DATA=data,SAVEDIR=SaveDir,CONC=concentration,ODORS=odors,OD=Odenote)'''

'''concentration = '1k'
odors = 'linalool|limonene|lemonoil'#|1octen3ol|benzaldehyde|roseoil'#|ylangylang|benzylalcohol'
odenote = 'LLL'
data = '/Users/joshswore/Manduca/Single_Channel_Analysis/DataFrames/Normalized/GA_Butter_Optimized/IntraVarMinimized/LLL_finalDF.csv'
SaveDir = f'/Users/joshswore/Manduca/Single_Channel_Analysis/DataFrames/Normalized/GA_Butter_Optimized/IntraVarMinimized/PCA/'


if not os.path.exists(SaveDir):
    os.makedirs(SaveDir)

#load our data frame into the program
DF = pd.read_csv(data, index_col=0)

All_DF=DF[DF['concentration'].str.contains(concentration)]
All_DF=All_DF[All_DF['label'].str.contains(odors)]
#convert the data frame into a usable format for scaling
All_DF2=All_DF.iloc[:,:5001].convert_dtypes(float).astype(float)

#scale the data to calculate the principal componenets
All_DF_Scaled=pd.DataFrame(StandardScaler().fit_transform(All_DF2),
                                   columns = All_DF2.columns,
                                   index=All_DF2.index)
#set the PCA parameters
PCA_set=PCA(n_components=100)

All_DF_PCAResults=PCA_set.fit_transform(All_DF_Scaled)
print(PCA_set.explained_variance_ratio_)
#Save our PCA object
reader=open(f'{SaveDir}{odenote}_PCA.pickle','wb')
pickle.dump(obj=PCA_set,file=reader)
reader.close()
All_DF_PCA_DF = pd.DataFrame(data = All_DF_PCAResults, index=All_DF_Scaled.index)

for x,y in zip(range(100), range(1,101)):
    All_DF_PCA_DF.rename({x: f'PC {y}'},axis=1, inplace=True)

All_DF_PCA_DF=pd.concat([All_DF_PCA_DF, All_DF.iloc[:,-2:]], axis=1)
All_DF_PCA_DF.to_csv(f'{SaveDir}{odenote}_PCA.csv')'''
