from EAG_Classifier_Library import *
import pandas as pd
import os

OdAbrev='YLimBaLo'
Odors ='ylangylang|limonene|benzylalcohol|lemonoil'
#read in
PCA_DF = pd.read_csv(f'/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized_Extracted_Waves/'
                     f'GA_Butter_Optimized/FDR_Fitness/{OdAbrev}/PCA/{OdAbrev}_PCA.csv',index_col=0)

TeDF = pd.read_csv(f'/Users/joshswore/Manduca/Multi_Channel_Analysis/Normalized_Extracted_Waves/'
                   f'GA_Butter_Optimized/FDR_Fitness/{OdAbrev}/{OdAbrev}_testingDF.csv',index_col=0)

Test_PCA_DF = PCA_DF.loc[PCA_DF.index.intersection(TeDF.index)]

#TeDF = pd.concat([TeDF.iloc[:,::5], Test_PCA_DF.iloc[:,-3:]], axis=1)

#PCA_DF.drop(columns='label.1',inplace=True)
Save_Directory = f'/Users/joshswore/Manduca/Multi_Channel_Analysis/Classifier_Results/{OdAbrev}/FDR_Fitness/PCs/'
if not os.path.exists(Save_Directory):
    os.makedirs(Save_Directory)

#Test_PCA_DF=pd.concat([Test_PCA_DF.iloc[:,:5],Test_PCA_DF.iloc[:,-3:]], axis=1)
print(f'begining Classification of YY_Normalized channels summed Data')

#data to input can be time series data or PCs Usin PC's we can expect training to occur faster since there are fewer "features"

print(f'beginning SVM...')
SVM_Results=SVMmodel(concentrations='1k',data=[Test_PCA_DF],odor=Odors,PosL='limonene', repeats=100)
pickle_Saver(savedir=Save_Directory,ext='SVM_Results',data=SVM_Results)

#print(f'beginning Random Forest')
#RF_results=RFmodel(concentrations='1k',data=[Test_PCA_DF],odor=Odors,PosL='limonene', repeats=100)
#pickle_Saver(savedir=Save_Directory,ext='RF_Results',data=RF_results)