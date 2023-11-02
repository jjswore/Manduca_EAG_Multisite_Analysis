import os
import pandas as pd
import glob
import csv
import os
from matplotlib import pyplot as plt


def gather_csv_files_from_directory(root_dir):
    # This function searches for all CSV files from root directory and its sub-directories.

    # Use os.walk and glob to find all csv files in the directory and sub-directories
    csv_files = []
    for dir_name, _, _ in os.walk(root_dir):
        csv_files.extend(glob.glob(os.path.join(dir_name, "*.csv")))
    return csv_files

def open_wave(FILE):
    with open(FILE, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    f.close()
    l=data[0]
    l = list(map(float, l))
    return l

def EAG_df_build(DIR):
    F_List=[]
    for dirpath, dirnames, filenames in os.walk(DIR):
        for filename in filenames:
            F_List.append(os.path.join(dirpath, filename))
    master=[]
    mastern=[]
    masterl=[]
    masterc=[]
    masterDate=[]
    odor100=[]
    odor300=[]
    odor1K=[]
    odor3K=[]
    odor10K=[]
    o100n=[]
    o300n=[]
    o1kn=[]
    o3kn=[]
    o10kn=[]


    for file in F_List:
        if file.endswith('.csv'):
            #print('filename: ', file)
            fbase = os.path.basename(file)
            cat=fbase.lower().split('_')
            print(cat)
            n=os.path.basename(fbase.lower()).split("_")
            name=n[0]+n[1] +n[2] + n[3] + n[4].replace('.csv','')
            lab=n[2]
            conc=n[1]
            date=n[0]
            x=open_wave(file)
            if cat[1] == '100':
                odor100.append(x)
                master.append(x)
                o100n.append(name)
                mastern.append(name)
                masterl.append(lab)
                masterc.append(conc)
                masterDate.append(date)

            if cat[1] == '300':
                odor300.append(x)
                master.append(x)
                o300n.append(name)
                mastern.append(name)
                masterl.append(lab)
                masterc.append(conc)
                masterDate.append(date)

            elif cat[1] == '1k':
                odor1K.append(x)
                master.append(x)
                o1kn.append(name)
                mastern.append(name)
                masterl.append(lab)
                masterc.append(conc)
                masterDate.append(date)

            elif cat[1] == '3k':
                odor3K.append(x)
                master.append(x)
                o3kn.append(name)
                mastern.append(name)
                masterl.append(lab)
                masterc.append(conc)
                masterDate.append(date)

            elif cat[1] == '10k':
                odor10K.append(x)
                master.append(x)
                o10kn.append(name)
                mastern.append(name)
                masterl.append(lab)
                masterc.append(conc)
                masterDate.append(date)

    odor100_df=pd.DataFrame(dict(zip(o100n,odor100)),index=[x for x in range(0,9000)])
    odor300_df=pd.DataFrame(dict(zip(o300n,odor300)),index=[x for x in range(0,9000)])
    odor10K_df=pd.DataFrame(dict(zip(o10kn,odor10K)),index=[x for x in range(0,9000)])
    odor1K_df=pd.DataFrame(dict(zip(o1kn,odor1K)),index=[x for x in range(0,9000)])
    odor3K_df=pd.DataFrame(dict(zip(o3kn,odor3K)),index=[x for x in range(0,9000)])
    master_df=pd.DataFrame(dict(zip(mastern,master)),index=[x for x in range(0,9000)])

    master_df=master_df.T
    master_df['label']=masterl
    master_df['concentration']=masterc
    master_df['date']=masterDate

    odor100_df['Mean']=odor100_df.mean(axis=1)
    odor300_df['Mean']=odor300_df.mean(axis=1)
    odor10K_df['Mean']=odor10K_df.mean(axis=1)
    odor1K_df['Mean']=odor1K_df.mean(axis=1)
    odor3K_df['Mean']=odor3K_df.mean(axis=1)

    odor100_df['Var']=odor100_df.iloc[:,:-1].var(axis=1)
    odor300_df['Var']=odor300_df.iloc[:,:-1].var(axis=1)
    odor10K_df['Var']=odor10K_df.iloc[:,:-1].var(axis=1)
    odor1K_df['Var']=odor1K_df.iloc[:,:-1].var(axis=1)
    odor3K_df['Var']=odor3K_df.iloc[:,:-1].var(axis=1)

    odor100_df['SEM']=odor100_df.iloc[:,:-2].sem(axis=1)
    odor300_df['SEM']=odor300_df.iloc[:,:-2].sem(axis=1)
    odor10K_df['SEM']=odor10K_df.iloc[:,:-2].sem(axis=1)
    odor1K_df['SEM']=odor1K_df.iloc[:,:-2].sem(axis=1)
    odor3K_df['SEM']=odor3K_df.iloc[:,:-2].sem(axis=1)

    odor100_df['STD']=odor100_df.iloc[:,:-2].std(axis=1)
    odor300_df['STD']=odor300_df.iloc[:,:-2].std(axis=1)
    odor10K_df['STD']=odor10K_df.iloc[:,:-2].std(axis=1)
    odor1K_df['STD']=odor1K_df.iloc[:,:-2].std(axis=1)
    odor3K_df['STD']=odor3K_df.iloc[:,:-2].std(axis=1)

    return master_df,odor100_df,odor300_df,odor1K_df,odor3K_df,odor10K_df


def main():
    print('building df')
    raw = pd.read_csv('/Users/joshswore/Manduca/Multi_Channel_Analysis/'
                      'Normalized_Extracted_Waves/Quality_Controlled_Data/_QC_T_1.csv', index_col=0)
    norm = pd.read_csv('/Users/joshswore/Manduca/Multi_Channel_Analysis/'
                       'Normalized_Extracted_Waves/Quality_Controlled_Data/_QC_T_1.csv', index_col=0)


    fig, axes = plt.subplots(nrows=8, ncols=2, sharey=False, sharex=True, figsize=(15, 25))
    Conc = ['Raw', 'Normalized']

    print('building plots')
    for x, label in zip(enumerate(raw['label'].unique()), enumerate(norm['label'].unique())):
        axes[x[0], 0].set_ylabel(label[1], weight='bold', size=16)
        for y, conc in zip(range(len(Conc)), Conc):
            axes[x[0], y].spines['top'].set_visible(False)
            axes[x[0], y].spines['right'].set_visible(False)
            axes[0, y].set_title(conc, weight='bold', size=26)
            axes[x[0], y].set_xlim(-5, 5000)
            axes[x[0], 0].set_ylim(-150, 50)
            axes[x[0], 1].set_ylim(-1.50, .50)

    print('displaying plots')
    for x, label in zip(range(len(raw['label'].unique())), raw['label'].unique()):
        Rtemp = raw[(raw['label'] == label) & (raw['concentration'] == '1k')]
        Ntemp = norm[(norm['label'] == label) & (norm['concentration'] == '1k')]

        for (_, Raw_row), (_, Norm_row) in zip(Rtemp.iterrows(), Ntemp.iterrows()):
            print(f'plotting {label} and Raw')
            Raw_row.drop(['label', 'concentration', 'date']).plot(ax=axes[x, 0])


            print(f'plotting {label} and Normalized')
            Norm_row.drop(['label', 'concentration', 'date']).plot(ax=axes[x, 1])

    #plt.savefig('/Users/joshswore/Manduca/Single_Channel_Analysis/Figures/Norm_v_Raw_PreFilter_AllSingleSiteWaves.svg')
    #plt.savefig('/Users/joshswore/Manduca/Single_Channel_Analysis/Figures/Norm_v_Raw_PreFilter_AllSingleSiteWaves.jpg')
    plt.show()


if __name__ == "__main__":
    main()

