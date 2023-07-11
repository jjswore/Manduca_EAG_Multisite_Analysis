from Manduca_Multisite_EAG_Analysis.Disease_VOC_Analysis.Classification.EAG_Classifier_Library import *
from sklearn_genetic import GASearchCV
from sklearn_genetic.space import Categorical, Continuous
from sklearn_genetic.callbacks import ConsecutiveStopping
from sklearn import svm

LogR_param_grid = {
        "C": Continuous(.01,20),
        "fit_intercept": Categorical([True,False]),
        "solver": Categorical(['liblinear']),
        "penalty": Categorical(['l2'])}



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
        "max_depth": Continuous(10,120),
        "min_samples_split": Continuous(0,20),
        'max_leaf_nodes':Continuous(10,600),
        "min_samples_leaf": Continuous(1,20),
        "max_samples": Continuous(0,1),
        "bootstrap":Categorical([True,False])}



def SVM_GASearch(data, concentration, odors):
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
    SVM_param_grid = {
        "kernel": Categorical(['rbf']),
        "C": Continuous(0.1, 1),
        "degree": Continuous(0, 1),
        "gamma": Continuous(0, 3),
        "coef0": Continuous(1, 4)}

    # Concatenate data into a single dataframe
    Analysis_data = pd.concat(data, axis=1)

    # Filter data based on concentration and odor label
    data_df = Analysis_data[(Analysis_data['concentration'].str.contains(concentration)) &
                            (Analysis_data['label'].str.contains(odors))]

    # Split data into train and test sets
    print('Splitting data...')
    train_features, test_features, train_labels, test_labels = TT_Split(data_df, .7)
    print('setting GA search')
    GA = GASearchCV(estimator=svm.SVC(), cv=15, param_grid=SVM_param_grid, population_size=1000, generations=10,
                    n_jobs=-1, verbose=True, scoring='accuracy', mutation_probability=.3, tournament_size=100)
    print('begining search')
    callback= ConsecutiveStopping(10,metric='fitness')
    GA.fit(train_features,train_labels,callback)

    gbp= GA.best_params_
    gbs=GA.best_score_
    gbe=GA.best_estimator_
    print(gbp,gbs,gbe)
    return gbp,gbs,gbe

def RandomForest_GASearch(data, concentration, odors):
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

    RF_param_grid = {
        "n_estimators": Categorical([10]),
        "max_features": Categorical(['sqrt', 'log2']),
        "max_depth": Continuous(10, 120),
        "min_samples_split": Continuous(0, 20),
        'max_leaf_nodes': Continuous(10, 600),
        "min_samples_leaf": Continuous(1, 20),
        "max_samples": Continuous(0, 1),
        "bootstrap": Categorical([True, False])}

    # Concatenate data into a single dataframe
    Analysis_data = pd.concat(data, axis=1)

    # Filter data based on concentration and odor label
    data_df = Analysis_data[(Analysis_data['concentration'].str.contains(concentration)) &
                            (Analysis_data['label'].str.contains(odors))]

    # Split data into train and test sets
    print('Splitting data...')
    train_features, test_features, train_labels, test_labels = TT_Split(data_df, .7)
    print('setting GA search')
    GA = GASearchCV(estimator=RandomForestClassifier(), cv=15, param_grid=RF_param_grid, population_size=1000, generations=10,
                    n_jobs=-1, verbose=True, scoring='accuracy', mutation_probability=.3, tournament_size=100)
    print('begining search')
    callback= ConsecutiveStopping(10,metric='fitness')
    GA.fit(train_features,train_labels,callback)

    gbp= GA.best_params_
    gbs=GA.best_score_
    gbe=GA.best_estimator_
    print(gbp,gbs,gbe)
    return gbp,gbs,gbe



PCAS = pd.read_pickle('/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/ButterLC1_HC3/YY_Normalized/Both_Channels/ClassifierResults/CH210PCs/_QC_T_1/CH2PCA_DF.pickle')

SVM_GASearch([PCAS],'1k','lemonoil|limonene|linalool')