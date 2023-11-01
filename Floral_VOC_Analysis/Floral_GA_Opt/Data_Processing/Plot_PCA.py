import pandas as pd
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

def Plot_PCA(DATADIR, ODENOTE, ODORS, CONC, TITLE):
    # set the data to be loaded and set a save location
    Odenotation = ODENOTE
    Concentration = CONC
    TITLE = TITLE
    DIR = f'{DATADIR}'

    PCA_df = f'{DIR}/{Odenotation}_PCA.csv'
    PCA_obj = f'{DIR}/{Odenotation}_PCA.pickle'
    SaveDir = f'{DIR}/'

    # make sure the folder for saving exists
    if not os.path.exists(SaveDir):
        os.makedirs(SaveDir)

    # open the PCA_DF into a dataframe
    data_df = pd.read_csv(PCA_df, index_col=0)
    DF = data_df[data_df['concentration'].str.contains(CONC)]
    print(DF)
    PCA_DF = DF[DF['label'].str.contains(ODORS)]
    print(PCA_DF['label'])
    # open the pickle file
    pca_obj = open(PCA_obj, 'rb')
    PCAobj = pickle.load(pca_obj)
    pca_obj.close()

    text_x_pos = 0.4 * len(PCAobj.explained_variance_ratio_[:100])
    # For y-axis: set the position a bit (e.g., 5%) above the maximum value
    text_y_pos = .4 * max(PCAobj.explained_variance_ratio_[:100])

    # Plot the explained variance
    plt.scatter(range(100), PCAobj.explained_variance_ratio_[:100], color='brown')
    plt.title('PCA Explained Variance')
    plt.ylabel('Explained Variance (%)')
    plt.xlabel('Principal Component')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.text(text_x_pos, text_y_pos, f'Explained Variance of First 2 PC\'s:{round(sum(PCAobj.explained_variance_ratio_[:2]), 2)}')
    plt.savefig(f'{SaveDir}{Odenotation}_ExplainedVariance.jpg')
    plt.savefig(f'{SaveDir}{Odenotation}_ExplainedVariance.svg')
    plt.show()

    # Plot Results
    # ============================================================================================

    plt.figure()
    plt.figure(figsize=(10, 10))
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=14)
    plt.xlabel('Principal Component - 1', fontsize=20)
    plt.ylabel('Principal Component - 2', fontsize=20)
    plt.title(TITLE, fontsize=20)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)


    # Create a dictionary mapping labels to colors

    colors = plt.cm.Paired(np.linspace(0, 1, 8))
    label_color_dict = {
        'limonene': colors[0],
        'lemonoil': colors[1],
        'ylangylang': colors[2],
        'roseoil': colors[3],
        'benzylalcohol': colors[4],
        '1octen3ol': colors[5],
        'benzaldehyde': colors[6],
        'linalool': colors[7]
    }
    # Assuming you have 8 unique labels in Targets
    Targets = list(PCA_DF['label'].unique())

    plotted_labels = []  # List to keep track of labels we have plotted

    for target in Targets:
        color = label_color_dict.get(target)  # fetch color from the dictionary
        if color is None:
            continue
        indicesToKeep = (PCA_DF['label']) == target
        plt.scatter(PCA_DF.loc[indicesToKeep, 'PC 1']
                    , PCA_DF.loc[indicesToKeep, 'PC 2'], c=[color], edgecolors='black', s=60, label=target)
        plotted_labels.append(target)

    plt.legend(plotted_labels)

    plt.savefig(f'{SaveDir}{Odenotation}_PCA.jpg')
    plt.savefig(f'{SaveDir}{Odenotation}_PCA.svg')
    plt.show()

'''data='/Users/joshswore/Manduca/Single_Channel_Analysis/Normalized_Exctracted_Waves/GA_Butter_Optimized/FDR_Fitness/RoLoLim/PCA'
odors = 'lemonoil|roseoil|limonene'
Odenote = 'RoLoLim'
concentration = '1k'
SaveDir='/Users/joshswore/Manduca/Single_Channel_Analysis/Normalized_Exctracted_Waves/' \
        'GA_Butter_Optimized/FDR_Fitness/RoLoLim/PCA'
Plot_PCA(DATADIR=data,ODENOTE=Odenote,CONC=concentration,ODORS=odors,TITLE=f'Rose Oil, Lemon Oil, Limonene \n Concentration 1:1000')'''

###########################################################################################################
#set the data to be loaded and set a save location
"""data='/Users/joshswore/Manduca/Single_Channel_Analysis/DataFrames/Normalized/GA_Butter_Optimized/FDR_Fitness/LLL_finalDF.csv'
odors = 'lemonoil|limonene|linalool'
Odenote = 'LLL'
concentration = '1k'
SaveDir='/Users/joshswore/Manduca/Single_Channel_Analysis/DataFrames/Normalized/GA_Butter_Optimized/FDR_Fitness/'
Plot_PCA(SaveDir,Odenote,concentration,'Lemon Oil, Limonene, Linalool')"""
"""Odenotation='LLL'
Concentration = '1:1k'
TITLE = 'Lemon Oil, Limonene, Linalool'
DIR='/Users/joshswore/Manduca/Single_Channel_Analysis/DataFrames/Normalized/GA_Butter_Optimized/FDR_Fitness/PCA/LLL/'


PCA_df = f'{DIR}/{Odenotation}_PCA.csv'
PCA_obj = f'{DIR}/{Odenotation}_PCA.pickle'
SaveDir = f'{DIR}/'

#make sure the folder for saving exists
if not os.path.exists(SaveDir):
    os.makedirs(SaveDir)

#open the PCA_DF into a dataframe
PCA_DF = pd.read_csv(PCA_df, index_col=0)

#open the pickle file
pca_obj = open(PCA_obj, 'rb')
PCAobj= pickle.load(pca_obj)
pca_obj.close()

#Plot the explained variance
plt.scatter(range(100), PCAobj.explained_variance_ratio_[:100],color='brown')
plt.title('PCA Explained Variance')
plt.ylabel('Explained Variance (%)')
plt.xlabel('Principal Component')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.text(40,.4, f'Explained Variance of First 2 PC\'s:{round(sum(PCAobj.explained_variance_ratio_[:2]),2)}')
plt.savefig(f'{SaveDir}{Odenotation}_ExplainedVariance.jpg')
plt.savefig(f'{SaveDir}{Odenotation}_ExplainedVariance.svg')
plt.show()

#Plot Results
#============================================================================================



plt.figure()
plt.figure(figsize=(10,10))
plt.xticks(fontsize=12)
plt.yticks(fontsize=14)
plt.xlabel('Principal Component - 1',fontsize=20)
plt.ylabel('Principal Component - 2',fontsize=20)
plt.title(f'{TITLE} \n at Concentration: {Concentration}',fontsize=20)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

#colors = ['steelblue', 'steelblue','steelblue', 'coral', 'coral', 'coral', 'darkseagreen', 'darkseagreen', 'darkseagreen']#, 'darkseagreen', 'darkseagreen', 'darkseagreen']
Targets = list((PCA_DF['label']).unique())
targets=  Targets

colors = ['limegreen','cyan', 'steelblue', 'brown', 'black',  'yellow','red']
for target, color in zip(targets,colors):
    indicesToKeep = (PCA_DF['label']) == target
    plt.scatter(PCA_DF.loc[indicesToKeep, 'PC 1']
               , PCA_DF.loc[indicesToKeep, 'PC 2'], c = color, edgecolors='black', s = 60)
plt.legend(targets)
plt.savefig(f'{SaveDir}{Odenotation}_PCA.jpg')
plt.savefig(f'{SaveDir}{Odenotation}_PCA.svg')
plt.show()"""