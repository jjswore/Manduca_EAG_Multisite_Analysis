import matplotlib.pyplot as plt
from Classifier_Results_Library import *

#

File_Dir='/Users/joshswore/Manduca/Multi_Channel_Analysis/Classifier_Results/LLL/FDR_Fitness/'
Save_Dir = f'{File_Dir}/Figures/'

if not os.path.exists(Save_Dir):
    os.makedirs(Save_Dir)

name_map = {
    'ylangylang': 'Ylang Ylang',
    'benzylalcohol': 'Benzylalcohol',
    'benzaldehyde': 'Benzaldehyde',
    '1octen3ol': '1-Octen-3-ol',
    'roseoil': 'Rose Oil',
    'lemonoil': 'Lemon Oil',
    'limonene': 'Limonene',
    'linalool': 'Linalool'
}

SVM_Results ='SVM_Results.pickle'
RF_Results = 'RF_Results.pickle'

SVM_DF = pickle_to_DF(f'{File_Dir}{SVM_Results}')
RF_DF = pickle_to_DF(f'{File_Dir}{RF_Results}')
print(SVM_DF['predicted_classes'][5])
labels = [name_map[label] for label in SVM_DF['predicted_classes'][0] if label in name_map]

print(len(labels))

names=['SVM Results', 'RF Results']

df=pd.concat([SVM_DF['accuracy_score'],RF_DF['accuracy_score'],
              SVM_DF['accuracy_score'],RF_DF['accuracy_score']],axis=1,keys=names)



SVM_CM = extract_CM(SVM_DF)

RF_CM = extract_CM(RF_DF)
#title='Lemon Oil, Limonene, 1-Octen-3-ol \n  Ylang Ylang, Benzylalcohol'
#', '.join(labels)
plot_CM(SVM_CM,labels,YROT=45, XROT=45, TITLE=None, SAVEDIR=f'{Save_Dir}SVM_')
plot_CM(RF_CM,labels,YROT=45, XROT=45, TITLE=None, SAVEDIR=f'{Save_Dir}RF_')

ViPlot(df,'Classifier Results',len(labels),SAVEDIR=Save_Dir)
