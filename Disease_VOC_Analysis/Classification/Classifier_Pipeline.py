from EAG_Classifier_Library import *
import os

DIR='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/ButterLC1_HC3/YY_Normalized/Both_Channels/'
DirList = os.listdir(DIR)
print(f'beginng Classification of YY_Normalized channels subtracted Data')
for f in DirList:
    if f.endswith('.csv'):
        print(f)
        All_df = pd.read_csv(f'{DIR}{f}' , index_col=0)

        All_df= All_df[All_df['concentration'].str.contains('1k')]
        All_df= All_df[All_df['label'].str.contains('linalool|limonene|lemonoil')]

        CH1=All_df.iloc[:,:9000]
        CH2=All_df.iloc[:,9000:-3]
        Ch_List=[All_df.iloc[:,:-3]]
        Ch_Name_list=['Both Channels']

        for ch,chn in zip(Ch_List,Ch_Name_list):
            PCA_DF, PCA_M, Scaled_Data = PCA_Constructor(ch,10)
            PCA_DF=pd.concat([PCA_DF,All_df.iloc[:,-3:]],axis=1)
            PCA_Results=[PCA_DF,PCA_M, Scaled_Data]
            Dlabs=['PCA_DF','PCA_M','Scaled_Data']
            n = f.split('.csv')[0]
            Save_Directory = f'{DIR}ClassifierResults/{chn}10PCs/test{n}/'
            for d,l in zip(PCA_Results,Dlabs):
                pickle_Saver(Save_Directory,f'{chn}{l}',d)

            print(f'beginning Logistic Regression on {f}...')
            LR_Results=LRmodel(concentrations='1k',data=[PCA_DF],odor='linalool|limonene|lemonoil',PosL='lemonoil', repeats=100)
            pickle_Saver(savedir=Save_Directory,ext='LogR_Results',data=LR_Results)

            print(f'beginning SVM on {f}...')
            SVM_Results=SVMmodel(concentrations='1k',data=[PCA_DF],odor='linalool|limonene|lemonoil',PosL='lemonoil', repeats=100)
            pickle_Saver(savedir=Save_Directory,ext='SVM_Results',data=SVM_Results)

            print(f'beginning Random Forest on {f}...')
            RF_results=RFmodel(concentrations='1k',data=[PCA_DF],odor='linalool|limonene|lemonoil',PosL='lemonoil', repeats=100)
            pickle_Saver(savedir=Save_Directory,ext='RF_Results',data=RF_results)

DIR='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/ButterLC1_HC3/YY_Normalized_Smoothened/Both_Channels/'
DirList = os.listdir(DIR)
print(f'beginng Classification of YY_Normalized channels subtracted Data')
for f in DirList:
    if f.endswith('.csv'):
        print(f)
        All_df = pd.read_csv(f'{DIR}{f}' , index_col=0)

        All_df= All_df[All_df['concentration'].str.contains('1k')]
        All_df= All_df[All_df['label'].str.contains('linalool|limonene|lemonoil')]

        CH1=All_df.iloc[:,:9000]
        CH2=All_df.iloc[:,9000:-3]
        Ch_List=[All_df.iloc[:,:-3]]
        Ch_Name_list=['Both Channels']

        for ch,chn in zip(Ch_List,Ch_Name_list):
            PCA_DF, PCA_M, Scaled_Data = PCA_Constructor(ch,10)
            PCA_DF=pd.concat([PCA_DF,All_df.iloc[:,-3:]],axis=1)
            PCA_Results=[PCA_DF,PCA_M, Scaled_Data]
            Dlabs=['PCA_DF','PCA_M','Scaled_Data']
            n = f.split('.csv')[0]
            Save_Directory = f'{DIR}ClassifierResults/{chn}10PCs/{n}/'
            for d,l in zip(PCA_Results,Dlabs):
                pickle_Saver(Save_Directory,f'{chn}{l}',d)

            print(f'beginning Logistic Regression on {f}...')
            LR_Results=LRmodel(concentrations='1k',data=[PCA_DF],odor='linalool|limonene|lemonoil',PosL='lemonoil', repeats=100)
            pickle_Saver(savedir=Save_Directory,ext='LogR_Results',data=LR_Results)

            print(f'beginning SVM on {f}...')
            SVM_Results=SVMmodel(concentrations='1k',data=[PCA_DF],odor='linalool|limonene|lemonoil',PosL='lemonoil', repeats=100)
            pickle_Saver(savedir=Save_Directory,ext='SVM_Results',data=SVM_Results)

            print(f'beginning Random Forest on {f}...')
            RF_results=RFmodel(concentrations='1k',data=[PCA_DF],odor='linalool|limonene|lemonoil',PosL='lemonoil', repeats=100)
            pickle_Saver(savedir=Save_Directory,ext='RF_Results',data=RF_results)
