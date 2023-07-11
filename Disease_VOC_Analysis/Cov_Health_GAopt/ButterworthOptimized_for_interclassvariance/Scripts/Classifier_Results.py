from Manduca_Multisite_EAG_Analysis.Disease_VOC_Analysis.Data_Visualization.Classifier_Results_Library import *


root='/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Quality_Controlled_Data/'
IDIR='ButterLC1_HC4.1_O2/YY_Normalized_Smoothened/Both_Channels/Intensity_Aligned_Data/Classifier_Results/'
SDIR='ButterLC1_HC4.1_O2/YY_Normalized_Smoothened/Both_Channels/Solenoid_Aligned_Data/Classifier_Results/'

IntSVM='IntAlign_QC1_SVM_Results.pickle'
IntRF='IntAlign_QC1_RF_Results.pickle'
SolSVM='SolAlign_QC1_SVM_Results.pickle'
SolRF='SolAlign_QC1_RF_Results.pickle'



SVM_intensity_aligned = pickle_to_DF(f'{root}{IDIR}{IntSVM}')
RF_intensity_aligned = pickle_to_DF(f'{root}{IDIR}{IntRF}')
SVM_solenoid_centered = pickle_to_DF(f'{root}{SDIR}{SolSVM}')
RF_solenoid_centered = pickle_to_DF(f'{root}{SDIR}{SolRF}')

names=['Intensity Aligned SVM', 'Intensity Aligned RF', 'Solenoid Aligned SVM', 'Solenoid Aligned RF']

df=pd.concat([SVM_intensity_aligned['accuracy_score'],RF_intensity_aligned['accuracy_score'],
              SVM_solenoid_centered['accuracy_score'],RF_solenoid_centered['accuracy_score'],],axis=1,keys=names)

ViPlot(df,'Classifier Results',3,None)
plt.show()
#plot_CM(RF_intensity_aligned['confusion_matrix'],RF_intensity_aligned['labels'],LABELS=,title=)

#plt.show()








