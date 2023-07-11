from Manduca_Multisite_EAG_Analysis.Disease_VOC_Analysis.Classification.EAG_Classifier_Library import *
from sklearn_genetic import GASearchCV
from sklearn_genetic.space import Categorical, Integer, Continuous
from sklearn_genetic.callbacks import ConsecutiveStopping
from sklearn import svm

    # Create parameter grid
SVM_param_grid = {
        "kernel": Categorical(['rbf', 'linear']),
        "C": Continuous(.01,20),
        "degree": Continuous(0,1),
        "gamma": Continuous(0,1),
        "coef0": Continuous(0,1)}

RF_param_grid = {
        "n_estimators":Categorical([10]),
        "max_features": Categorical(['sqrt','log2']),
        "max_depth": Integer(10,120),
        "min_samples_split": Integer(0,20),
        'max_leaf_nodes':Integer(10,600),
        "min_samples_leaf": Integer(1,20),
        "max_samples": Continuous(0,1),
        "bootstrap":Categorical([True])}
def SVM_GASearch(data, params, concentration, odors):
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
    Analysis_data = pd.concat([data], axis=1)

    # Filter data based on concentration and odor label
    data_df = Analysis_data[(Analysis_data['concentration'].str.contains(concentration)) &
                            (Analysis_data['label'].str.contains(odors))]

    # Split data into train and test sets
    print('Splitting data...')
    train_features, test_features, train_labels, test_labels = TT_Split(data_df, .8)
    print('setting GA search')
    GA = GASearchCV(estimator=svm.SVC(), cv=10, param_grid=params, population_size=100, generations=200,
                    n_jobs=-1, verbose=True, scoring='accuracy', mutation_probability=.3, tournament_size=3)
    print('begining search')
    callback= ConsecutiveStopping(10,metric='fitness')
    GA.fit(train_features,train_labels,callback)

    gbp= GA.best_params_
    gbs=GA.best_score_
    gbe=GA.best_estimator_
    print(gbp,gbs,gbe)
    return gbp,gbs,gbe

def RF_GASearch(data, params, concentration, odors):
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
    Analysis_data = pd.concat([data], axis=1)

    # Filter data based on concentration and odor label
    data_df = Analysis_data[(Analysis_data['concentration'].str.contains(concentration)) &
                            (Analysis_data['label'].str.contains(odors))]

    # Split data into train and test sets
    print('Splitting data...')
    train_features, test_features, train_labels, test_labels = TT_Split(data_df, .8)
    print('setting GA search')
    GA = GASearchCV(estimator=RandomForestClassifier(), cv=10, param_grid=params, population_size=100, generations=200,
                    n_jobs=-1, verbose=True, scoring='accuracy', mutation_probability=.3, tournament_size=3)
    print('begining search')
    callback= ConsecutiveStopping(10,metric='fitness')
    GA.fit(train_features,train_labels,callback)

    gbp= GA.best_params_ #these are the best performing parameters
    gbs=GA.best_score_
    gbe=GA.best_estimator_ # Estimator that was chosen by the search, i.e. estimator which gave highest score on the left out data ie the classifier
    print(gbp,gbs,gbe)
    return gbp,gbs,gbe

#Load data to classify

df = pd.read_csv('Cov_health_QC1_finalDF.csv', index_col=0)

#Save the classifier, score and parameters
#Use the

#PCAS = pd.read_pickle('/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/ButterLC1_HC3/YY_Normalized/Both_Channels/ClassifierResults/CH210PCs/_QC_T_1/CH2PCA_DF.pickle')
from Manduca_Multisite_EAG_Analysis.Disease_VOC_Analysis.Classification.EAG_Classifier_Library import PCA_Constructor, pickle_Saver
#PCAs = PCA_Constructor(df, PC=10)

cov_healthy_df = df[(df['label'].str.contains('artcov1|healthy1k|healthy100k'))]
cov_healthy_pcas, _, _= PCA_Constructor(cov_healthy_df,PC=10)

cov_healthy_pcas = pd.concat([cov_healthy_pcas,cov_healthy_df.iloc[:,-3:]], axis=1)

svm_bp, svm_bs, svm_bclf = SVM_GASearch(cov_healthy_pcas, SVM_param_grid, 'cov1','artcov1|healthy1k|healthy100k')
rf_bp, rf_bs, rf_bclf =RF_GASearch(cov_healthy_pcas, RF_param_grid, 'cov1', 'artcov1|healthy1k|healthy100k')

pickle_Saver(savedir='Intensity_Aligned_CLF_Opt/',ext='svm_BestParams',data=svm_bp)
pickle_Saver(savedir='Intensity_Aligned_CLF_Opt/',ext='svm_BestCLF',data=svm_bclf)
pickle_Saver(savedir='Intensity_Aligned_CLF_Opt/',ext='rf_BestParams',data=rf_bp)
pickle_Saver(savedir='Intensity_Aligned_CLF_Opt/',ext='rf_BestCLF',data=rf_bclf)