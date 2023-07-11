import pandas as pd

from Classifier_Results_Library import *

Butter='LC1_HC3'
QCThresh='1'
Process='YY_Normalized_Smoothened'



SVM_Difference=ClassifierResults(BASE='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/', BUTTER=Butter,
                      PROCESS=Process,CH='CH_Subtraction', QCTHRESH=QCThresh,Feature='10PCs', MODEL='SVM')
SVM_Sum=ClassifierResults(BASE='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/', BUTTER=Butter,
                      PROCESS=Process,CH='CH_Addition', QCTHRESH=QCThresh,Feature='10PCs', MODEL='SVM')
SVM_CH1=ClassifierResults(BASE='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/', BUTTER=Butter,
                      PROCESS=Process,CH='Both_Channels', QCTHRESH=QCThresh,Feature='CH110PCs', MODEL='SVM')
SVM_CH2=ClassifierResults(BASE='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/', BUTTER=Butter,
                      PROCESS=Process,CH='Both_Channels', QCTHRESH=QCThresh,Feature='CH210PCs', MODEL='SVM')
SVM_Both=ClassifierResults(BASE='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/', BUTTER=Butter,
                      PROCESS=Process,CH='Both_Channels', QCTHRESH=QCThresh,Feature='Both Channels10PCs', MODEL='SVM')

RF_Difference=ClassifierResults(BASE='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/', BUTTER=Butter,
                      PROCESS=Process,CH='CH_Subtraction', QCTHRESH=QCThresh,Feature='10PCs', MODEL='RF')
RF_Sum=ClassifierResults(BASE='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/', BUTTER=Butter,
                      PROCESS=Process,CH='CH_Addition', QCTHRESH=QCThresh,Feature='10PCs', MODEL='RF')
RF_CH1=ClassifierResults(BASE='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/', BUTTER=Butter,
                      PROCESS=Process,CH='Both_Channels', QCTHRESH=QCThresh,Feature='CH110PCs', MODEL='RF')
RF_CH2=ClassifierResults(BASE='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/', BUTTER=Butter,
                      PROCESS=Process,CH='Both_Channels', QCTHRESH=QCThresh,Feature='CH210PCs', MODEL='RF')
RF_Both=ClassifierResults(BASE='/Users/joshswore/Manduca/MultiChannel/Floral/Quality_Controlled_Data/', BUTTER=Butter,
                      PROCESS=Process,CH='Both_Channels', QCTHRESH=QCThresh,Feature='Both Channels10PCs', MODEL='RF')

names=['SVM_Difference','SVM_Sum','SVM_CH1','SVM_CH2', 'SVM_Both', 'RF_Difference','RF_Sum','RF_CH1','RF_CH2', 'RF_Both' ]

df=pd.concat([SVM_Difference['accuracy_score'],SVM_Sum['accuracy_score'],SVM_CH1['accuracy_score'],SVM_CH2['accuracy_score'],SVM_Both['accuracy_score'],
           RF_Difference['accuracy_score'], RF_Sum['accuracy_score'], RF_CH1['accuracy_score'], RF_CH2['accuracy_score'], RF_Both['accuracy_score']],axis=1,keys=names)

ViPlot(df,'Classifier Results',3,'/Users/joshswore/Desktop/QC_0.5_SVM_and_RF_results.svg')
plt.show()








