from Manduca_Multisite_EAG_Analysis.Disease_VOC_Analysis.Data_Processing.EAG_DataProcessing_Library import *

DIR= '/Cov_Health_GAopt/ButterworthOptimized_for_interclassvariance/Butterworth_Filtered_Data/'
all_df = pd.read_csv(f'{DIR}Cov_health_QC1000_finalDF.csv', index_col=0)
ThreshList = [.5,1]
for t in ThreshList:
    print(f"begining quality control at threshold of {t}")
    final = FFT_LSTSQ_QC(all_df, t)
    final_T = pd.DataFrame(final.T.dropna(axis=0))

    filename = f"_QC_T_{str(t)}.csv"
    outdir=f"{DIR}"
    #outdir = outdir.replace('Processed_Data/Official', 'Quality_Controlled_Data')
    print(outdir)
    print(os.path.exists(outdir))

    if os.path.exists(outdir)==False:
        print('making directory...')
        os.makedirs(outdir)
        print('directory made')

    filename = os.path.join(outdir, filename)
    final_T.to_csv(filename)