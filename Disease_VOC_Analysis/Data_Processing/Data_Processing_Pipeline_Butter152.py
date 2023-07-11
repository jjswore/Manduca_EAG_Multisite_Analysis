from EAG_DataProcessing_Library import *

def run():
    ''
    DirList = ['/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data/021423/',
               '/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data/021523/',
               '/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data/022123/',
               '/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data/022323/',
               '/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data/022423/',
               '/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data/022723/',
               '/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data/030123/',
               '/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data/030223/']#,
               #'/Users/joshswore/Manduca/MultiChannel/Covid/Raw_Data/11223/',
               #'/Users/joshswore/Manduca/MultiChannel/Covid/Raw_Data/111822/',
               #'/Users/joshswore/Manduca/MultiChannel/Covid/Raw_Data/010623/',
              # ]

   #     DirList = ['/Users/joshswore/Manduca/MultiChannel/TedlarBagExperiments/Raw_Data/050723/',
   #            '/Users/joshswore/Manduca/MultiChannel/TedlarBagExperiments/Raw_Data/050923/']
   #     DirList=['/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data']


    DirList = [os.path.join('/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data/', entry) + '/' for entry in os.listdir('/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data/') if
           os.path.isdir(os.path.join('/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Raw_Data/', entry))]

    s = '/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Processed_Data/Official/ButterLC.1_HC5/'

    process_data(DirList, savedir=f'{s}/Raw/Both_Channels/',
                 SUB=False, SUM=False, Norm=False, Smoothen=False, LOG=False, Butter=[.1, 5], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/YY_Normalized/Both_Channels/',
                 SUB=False, SUM=False, Norm='YY', Smoothen=False, LOG=False, Butter=[.1, 5], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/Smoothened/Both_Channels/',
                 SUB=False, SUM=False, Norm=False, Smoothen=True, LOG=False, Butter=[.1, 5], RETURN='SAVE')
    process_data(DirList, savedir=f'{s}/YY_Normalized_Smoothened/Both_Channels/',
                 SUB=False, SUM=False, Norm='YY', Smoothen=True, LOG=False, Butter=[.1, 5], RETURN='SAVE')

    Dlist=get_subdirectories(s)

    for D in Dlist:
        BaseDirList=get_subdirectories(D)

        OdorList = ['ArtCov1/', 'Healthy1k/', '1propanol/', '2methyl2pentanal/', 'aceticacid/', 'acetone/', 'nonanal/',
                    'octanal/', 'pentadecane/', 'ylangylang/']
        ThreshList=[.5,1]
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