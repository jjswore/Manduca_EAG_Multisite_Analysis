import pandas as pd
import pickle
from Manduca_Multisite_EAG_Analysis.Disease_VOC_Analysis.Classification.EAG_Classifier_Library import RF_Testing, SVM_Testing
import os

def RFmodel(concentrations, classifier, data, odor, PosL, repeats):
    """
    Trains and evaluates a Random Forest classifier on the provided dataset for each concentration of a given odor.

    Args:
        concentrations (list): A list of concentrations of the odor to be analyzed.
        data (pd.DataFrame): A pandas DataFrame containing the training data.
        odor (str): The name of the odor being analyzed.

    Returns:
        list: A nested list containing the classification performance metrics for each iteration of the Random Forest classifier
            for each concentration of the given odor.
    """
    results = []
    for conc in [concentrations]:
        print(f"Building Random Forest for {odor} at {conc} concentration")
        results.append([RF_Testing(data=data, classifier=classifier, concentration=conc, odors=odor, P=PosL)
                        for _ in range(repeats)])
        print(f"Finished analysis for {odor} at {conc} concentration")
    return results

def SVMmodel(concentrations, classifier, data, odor, PosL, repeats):
    """
    Trains and evaluates a Support Vector Machine classifier on the provided dataset for each concentration of a given odor.

    Args:
        concentrations (list): A list of concentrations of the odor to be analyzed.
        data (pd.DataFrame): A pandas DataFrame containing the training data.
        odor (str): The name of the odor being analyzed.

    Returns:
        list: A nested list containing the classification performance metrics for each iteration of the Support Vector Machine classifier
            for each concentration of the given odor.
    """
    results = []
    for conc in [concentrations]:
        print(f"Building SVM for {odor} at {conc} concentration")
        results.append([SVM_Testing(data=data, classifier=classifier, concentration=conc, odors=odor, P=PosL)
                        for _ in range(repeats)])
        print(f"Finished analysis for {odor} at {conc} concentration")
    return results

def pickle_Saver(savedir,ext,data):
    if not os.path.isdir(savedir):
        os.makedirs(savedir)
    reader=open(f'{savedir}{ext}.pickle','wb')
    pickle.dump(obj=data,file=reader)
    reader.close()



f='PCs/QC_T_1_IntAlign_cov_health_pcas.csv'
datadir= '/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Quality_Controlled_Data/ButterLC1_HC5_O2/YY_Normalized_Smoothened/Both_Channels/Intensity_Aligned_Data/'
Save_Directory=f'{datadir}Classifier_Results/'
if not os.path.exists(Save_Directory):
    os.makedirs(Save_Directory)
PCA_DF = pd.read_csv(f'{datadir}{f}', index_col=0)

with open(f'{datadir}classifiers/QC_T_1_IntAlign_rf_BestCLF_YYnorm.pickle', 'rb') as f:
    RF_CLF = pickle.load(f)

with open(f'{datadir}classifiers/QC_T_1_IntAlign_svm_BestCLF_YYnorm.pickle', 'rb') as f:
    SVM_CLF = pickle.load(f)

print(f'beginng Classification of Intensity Aligned Data')
print(f'beginning SVM on {f}...')
SVM_Results=SVMmodel(concentrations='cov1', classifier=SVM_CLF, data=[PCA_DF],odor='artcov1|healthy1k|healthy100k',PosL='artcov1', repeats=100)
pickle_Saver(savedir=Save_Directory,ext='IntAlign_QC1_SVM_Results',data=SVM_Results)

print(f'beginning Random Forest on {f}...')
RF_results=RFmodel(concentrations='cov1', classifier=RF_CLF, data=[PCA_DF],odor='artcov1|healthy1k|healthy100k',PosL='artcov1', repeats=100)
pickle_Saver(savedir=Save_Directory,ext='IntAlign_QC1_RF_Results',data=RF_results)