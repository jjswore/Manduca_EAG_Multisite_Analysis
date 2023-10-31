from EAG_DataProcessing_Library import *

def run():
    DirList = ['/Users/joshswore/Manduca/MultiChannel/Floral/Raw_Data/032223/',
               '/Users/joshswore/Manduca/MultiChannel/Floral/Raw_Data/032423/',
               '/Users/joshswore/Manduca/MultiChannel/Floral/Raw_Data/020623/',
               '/Users/joshswore/Manduca/MultiChannel/Floral/Raw_Data/012823/',
               '/Users/joshswore/Manduca/MultiChannel/Floral/Raw_Data/012623/',
               '/Users/joshswore/Manduca/MultiChannel/Floral/Raw_Data/012423/',
               '/Users/joshswore/Manduca/MultiChannel/Floral/Raw_Data/011923/',
               '/Users/joshswore/Manduca/MultiChannel/Floral/Raw_Data/11823/',
               '/Users/joshswore/Manduca/MultiChannel/Floral/Raw_Data/11223/',
               '/Users/joshswore/Manduca/MultiChannel/Floral/Raw_Data/111822/',
               '/Users/joshswore/Manduca/MultiChannel/Floral/Raw_Data/010623/']

    s = '/Users/joshswore/Manduca/MultiChannel/Floral/Processed_Data/Official/ButterLC.1_HC6/'

    process_data(DirList, savedir=f'{s}/Raw/Both_Channels/',
                 SUB=False, SUM=False, Norm=False, Smoothen=False, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/YY_Normalized/Both_Channels/',
                 SUB=False, SUM=False, Norm='YY', Smoothen=False, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/Normalized/Both_Channels/',
                 SUB=False, SUM=False, Norm='Yes', Smoothen=False, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/Smoothened/Both_Channels/',
                 SUB=False, SUM=False, Norm=False, Smoothen=True, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/YY_Normalized_Smoothened/Both_Channels/',
                 SUB=False, SUM=False, Norm='YY', Smoothen=True, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/Normalized_Smoothened/Both_Channels/',
                 SUB=False, SUM=False, Norm='Yes', Smoothen=True, LOG=False, Butter=[.1,6], RETURN='SAVE')

    process_data(DirList, savedir=f'{s}/Raw/CH_Subtraction/',
            SUB=True, SUM=False, Norm=False, Smoothen=False, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/YY_Normalized/CH_Subtraction/',
            SUB=True, SUM=False, Norm=False, Smoothen=False, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/Normalized/CH_Subtraction/',
            SUB=True, SUM=False, Norm='Yes', Smoothen=False, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/Smoothened/CH_Subtraction/',
            SUB=True, SUM=False, Norm=False, Smoothen=True, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/YY_Normalized_Smoothened/CH_Subtraction/',
            SUB=True, SUM=False, Norm='YY', Smoothen=True, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/Normalized_Smoothened/CH_Subtraction/',
            SUB=True, SUM=False, Norm='Yes', Smoothen=True, LOG=False, Butter=[.1,6], RETURN='SAVE')

    process_data(DirList, savedir=f'{s}/Raw/CH_Addition/',
                 SUB=False, SUM=True, Norm=False, Smoothen=False, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/YY_Normalized/CH_Addition/',
                 SUB=False, SUM=True, Norm='YY', Smoothen=False, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/Normalized/CH_Addition/',
                 SUB=False, SUM=True, Norm='Yes', Smoothen=False, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/Smoothened/CH_Addition/',
                 SUB=False, SUM=True, Norm=False, Smoothen=True, LOG=False, Butter=[.1,6], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/YY_Normalized_Smoothened/CH_Addition/',
                 SUB=False, SUM=True, Norm='YY', Smoothen=True, LOG=False, Butter=[.1,6],RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/Normalized_Smoothened/CH_Addition/',
                 SUB=False, SUM=True, Norm='Yes', Smoothen=True, LOG=False, Butter=[.1,6], RETURN='SAVE')

    Dlist=get_subdirectories(s)

    for D in Dlist:
        BaseDirList=get_subdirectories(D)

        OdorList = ['benzaldehyde/', 'benzylalcohol/', 'ylangylang/', 'roseoil/',
                    'lemonoil/', '1octen3ol/', 'linalool/', 'limonene/']
        ThreshList=[.5,.625,.75,.875,1]
        all_dfs = []
        for directory in BaseDirList:

            print(directory)
            print('building dataframe...')
            dfs = [EAG_df_build(os.path.join(directory, odor)) for odor in OdorList]
            all_df = pd.concat(dfs)
            print(all_df.shape)
            all_dfs.append(all_df)

        for directory, all_df in zip(BaseDirList, all_dfs):
            for t in ThreshList:
                print(f"begining quality control for {directory} at threshold of {t}")
                final = FFT_LSTSQ_QC(all_df, t)
                final_T = pd.DataFrame(final.T.dropna(axis=0))

                filename = f"_QC_T_{str(t)}.csv"
                outdir=f"{directory}"
                outdir = outdir.replace('Processed_Data/Official', 'Quality_Controlled_Data')
                print(outdir)
                print(os.path.exists(outdir))

                if os.path.exists(outdir)==False:
                    print('making directory...')
                    os.makedirs(outdir)
                    print('directory made')

                filename = os.path.join(outdir, filename)
                final_T.to_csv(filename)

run()