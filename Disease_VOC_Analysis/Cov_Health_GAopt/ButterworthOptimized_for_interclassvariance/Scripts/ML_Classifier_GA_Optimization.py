from Manduca_Multisite_EAG_Analysis.Disease_VOC_Analysis.Classification.EAG_Classifier_Library import *
from sklearn_genetic import GASearchCV
from sklearn_genetic.space import Categorical, Integer, Continuous
from sklearn_genetic.callbacks import ConsecutiveStopping
from sklearn import svm

    # Create parameter grid
SVM_param_grid = {
        "C": Continuous(.01,10),
        "degree": Continuous(0,1),
        "gamma": Continuous(0,1),
        "coef0": Continuous(0,1)}

RF_param_grid = {
        "n_estimators":Categorical([10]),
        "max_features": Categorical(['sqrt','log2']),
        "max_depth": Integer(10,120),
        "min_samples_split": Integer(2,20),
        'max_leaf_nodes':Integer(10,600),
        "min_samples_leaf": Integer(1,20),
        "max_samples": Continuous(0,1),
        "bootstrap":Categorical([True])}
def SVM_GASearch(train_features,train_labels, params, concentration, odors):
    """
    Perform a grid search to optimize SVM hyperparameters.

    Args:
    - data (List[pd.DataFrame]): A list of pandas dataframes, each containing the data to be analyzed
    - concentration (str): The concentration of the odor stimuli to be analyzed
    - odors (str): The label of the odor stimuli to be analyzed
    - P (str): The positive class label for computing recall score

    Returns:
    - clf (svm.SVC): The optimized SVM classifier
    - gbp (Dict[str, Any]): The best set of hyperparameters found by grid search
    - gbs (float): The best score found by grid search
    """
    #params = {
        #"kernel": Categorical(['rbf']),
        #"C": Continuous(0.1, 1),
        #"degree": Continuous(0, 1),
        #"gamma": Continuous(0, 3),
        #"coef0": Continuous(1, 4)}

    # Concatenate data into a single dataframe
    #Analysis_data = pd.concat([data], axis=1)

    # Filter data based on concentration and odor label
    #data_df = Analysis_data[(Analysis_data['concentration'].str.contains(concentration)) &
                            #(#Analysis_data['label'].str.contains(odors))]

    # Split data into train and test sets
    #print('Splitting data...')
    #train_features, test_features, train_labels, test_labels = TT_Split(data_df, .8)
    print('setting GA search')
    GA = GASearchCV(estimator=svm.SVC(kernel='rbf'), cv=10, param_grid=params, population_size=750, generations=200,
                    n_jobs=-1, verbose=True, scoring='accuracy', mutation_probability=.3, tournament_size=3)
    print('begining search')
    callback= ConsecutiveStopping(25,metric='fitness')
    GA.fit(train_features,train_labels,callback)

    gbp= GA.best_params_
    gbs=GA.best_score_
    gbe=GA.best_estimator_
    print(gbp,gbs,gbe)
    return gbp,gbs,gbe

def RF_GASearch(train_features,train_labels, params, concentration, odors):
    """
    Perform a grid search to optimize RandomForest hyperparameters.

    Args:
    - data (List[pd.DataFrame]): A list of pandas dataframes, each containing the data to be analyzed
    - concentration (str): The concentration of the odor stimuli to be analyzed
    - odors (str): The label of the odor stimuli to be analyzed

    Returns:
    - clf (RandomForestClassifier): The optimized RandomForest classifier
    - gbp (Dict[str, Any]): The best set of hyperparameters found by grid search
    - gbs (float): The best score found by grid search
    """

    # Concatenate data into a single dataframe
    #Analysis_data = pd.concat([data], axis=1)

    # Filter data based on concentration and odor label
    #data_df = Analysis_data[(Analysis_data['concentration'].str.contains(concentration)) &
                            #(Analysis_data['label'].str.contains(odors))]

    # Split data into train and test sets
    #print('Splitting data...')
    #train_features, test_features, train_labels, test_labels = TT_Split(data_df, .8)
    print('setting GA search')
    GA = GASearchCV(estimator=RandomForestClassifier(), cv=10, param_grid=params, population_size=750, generations=200,
                    n_jobs=-1, verbose=True, scoring='accuracy', mutation_probability=.3, tournament_size=3)
    print('begining search')
    callback= ConsecutiveStopping(25,metric='fitness')
    GA.fit(train_features,train_labels,callback)

    gbp= GA.best_params_ #these are the best performing parameters
    gbs=GA.best_score_
    gbe=GA.best_estimator_ # Estimator that was chosen by the search, i.e. estimator which gave highest score on the left out data ie the classifier
    print(gbp,gbs,gbe)
    return gbp,gbs,gbe

#Load data to classify
datadir='/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Quality_Controlled_Data/ButterLC1_HC4.1_O2/YY_Normalized_Smoothened/Both_Channels/'
savedir='/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Quality_Controlled_Data/ButterLC1_HC4.1_O2/YY_Normalized_Smoothened/Both_Channels/Intensity_Aligned_Data/'
classdir='classifiers/'
df = pd.read_csv(f'{datadir}_QC_T_1.csv', index_col=0)
CH1 = df.iloc[:,:9001]
CH1 = pd.concat([CH1,df.iloc[:,-3:]], axis=1)
CH2 = df.iloc[:,9001:]

#CH1df = intensity_alignment(CH1)
#CH2df = intensity_alignment(CH2)

#Save the classifier, score and parameters
CH1.to_csv(f'{savedir}/Channel_Seperations/CH1__QC_T_1_IntAlign_TimeSeries_YYNormSmooth.csv')
CH2.to_csv(f'{savedir}/Channel_Seperations/CH2__QC_T_1_IntAlign_TimeSeries_YYNormSmooth.csv')

SolAlign_df = pd.concat([CH1.iloc[:,:-3],CH2],axis=1)

C1_cov_healthy_df = CH1[(CH1['label'].str.contains('artcov1|healthy1k|healthy100k'))]
C2_cov_healthy_df = CH2[(CH2['label'].str.contains('artcov1|healthy1k|healthy100k'))]
intensity_aligned_cov_health_df = SolAlign_df[(SolAlign_df['label'].str.contains('artcov1|healthy1k|healthy100k'))]

C1cov_healthy_pcas, _, _= PCA_Constructor(C1_cov_healthy_df,PC=10)
C2cov_healthy_pcas, _, _= PCA_Constructor(C2_cov_healthy_df,PC=10)
intensity_aligned_cov_health_pcas,_,_=PCA_Constructor(intensity_aligned_cov_health_df,PC=10)

C1cov_healthy_pcas = pd.concat([C1cov_healthy_pcas,C1_cov_healthy_df.iloc[:,-3:]], axis=1)
C2cov_healthy_pcas = pd.concat([C2cov_healthy_pcas,C2_cov_healthy_df.iloc[:,-3:]], axis=1)
intensity_aligned_cov_health_pcas = pd.concat([intensity_aligned_cov_health_pcas,intensity_aligned_cov_health_df.iloc[:,-3:]],axis=1)

C1cov_healthy_pcas.to_csv(f'{savedir}PCs/C1cov_QC_T_1_YYNormSmooth_IntAlign_healthy_pcas.csv')
C2cov_healthy_pcas.to_csv(f'{savedir}PCs/C2cov_QC_T_1_YYNormSmooth_IntAlign_healthy_pcas.csv')
intensity_aligned_cov_health_pcas.to_csv(f'{savedir}PCs/QC_T_1_IntAlign_cov_health_pcas.csv')

#Analysis_data = pd.concat([data], axis=1)

# Filter data based on concentration and odor label
data_df = intensity_aligned_cov_health_pcas[(intensity_aligned_cov_health_pcas['concentration'].str.contains('cov1')) &
                        (intensity_aligned_cov_health_pcas['label'].str.contains('artcov1|healthy1k|healthy100k'))]

# Split data into train and test sets
print('Splitting data...')
train_features, test_features, train_labels, test_labels = TT_Split(data_df, .8)

svm_bp, svm_bs, svm_bclf = SVM_GASearch(train_features,train_labels, SVM_param_grid, 'cov1','artcov1|healthy1k|healthy100k')
rf_bp, rf_bs, rf_bclf =RF_GASearch(train_features,train_labels, RF_param_grid, 'cov1', 'artcov1|healthy1k|healthy100k')

pickle_Saver(savedir=savedir+classdir,ext='QC_T_1_IntAlign_svm_BestParams_YYNormSmooth',data=svm_bp)
pickle_Saver(savedir=savedir+classdir,ext='QC_T_1_IntAlign_svm_BestCLF_YYNormSmooth',data=svm_bclf)
pickle_Saver(savedir=savedir+classdir,ext='QC_T_1_IntAlign_rf_BestParams_YYNormSmooth',data=rf_bp)
pickle_Saver(savedir=savedir+classdir,ext='QC_T_1_IntAlign_rf_BestCLF_YYNormSmooth',data=rf_bclf)