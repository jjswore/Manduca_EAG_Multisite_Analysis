import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyabf
import pyabf.filter
import os
import csv
import glob
from scipy.signal import butter, lfilter
from scipy import optimize

def Check_Dir(DIR):
    if not os.path.exists(DIR):
        os.makedirs(DIR)

def find_sol(data):  # data = abf.sweepY of second channel out of three channels "channel = 1" from abf file
    SolFall = np.diff(data)
    NI = [i for i, v in enumerate(SolFall) if v < -0.3]
    PI = [i for i, v in enumerate(SolFall) if v > 0.3]
    test = zip(PI, NI)
    sol = list(test)
    return sol

def Extract_mEAG(FILE, lc, hc, ORDER, BF=True):
    print(FILE)
    print('meag', type(FILE))
    # first we load the data into our variable abf
    abf = pyabf.ABF(FILE)
    # now lets find out how many channels are in the files
    chList = [x for x in range(abf.channelCount)]
    # next lets find when the solenoid is activated
    # the data associated with our stimulus is stored in channel=1
    abf.setSweep(0, channel=1)
    sol = find_sol(abf.sweepY)
    # we now have a set of tuples. the first number in the tuple is when the solenoid is open, the second is close
    # for our data let extract the .5 seconds prior to solenoid activating and 5 seconds after it closes

    ni = len(sol)
    npts = 9000
    CH1 = np.zeros((ni, npts))
    CH2 = np.zeros((ni, npts))
    CHL = [CH1, CH2]
    for CH, ch in zip(CHL, chList[::2]):
        abf.setSweep(0, channel=ch)
        for i in range(0, ni):
            temp = abf.sweepY[sol[i][0] - 500:sol[i][1] + 8000]
            avg = np.mean(temp[0:500])
            # baselined=abf.sweepY[sol[i][0]-500:sol[i][1]+8000]
            CH[i, :] = [x - avg for x in temp]
            # CH[i,:]= abf.sweepY[sol[i][0]-500:sol[i][1]+8000]
    #remove the ch1 signal from channel to that occurs due to propagation of signal towards brain.
    CHL[1] = CHL[1]-CHL[0]
    CHL_Final=[]
    if BF == True:
        for ch in CHL:
            for x in range(0, 3):
                ch[x][:] = [n - (ch[x][:500].mean()) for n in ch[x][:]]
                ch[x, :] = butter_bandpass_filter(ch[x], lowcut=lc, highcut=hc, fs=1000.0, order=ORDER)
            CHL_Final.append(ch)
    else:
        for ch in CHL:
            CHL_Final.append(ch)
    return CHL_Final

def name_con(f):
    # This will splits the basename of the file on "_" to find the concentration in the file name

    n = os.path.basename(f)
    tn = n.split("_", 2)
    if tn[1].lower() == '100':
        x = '1:100'
    elif tn[1].lower() == '1k':
        x = '1:1k'
    elif tn[1].lower() == '10k':
        x = '1:10k'
    else:
        x = ''
    name = x + ' ' + tn[2]
    return name

def butter_bandpass(lowcut, highcut, fs, order=1):
    # creates a butterworth bandpass filter

    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=1):
    # applies a butterworth bandpass filter to some data
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y



def ConcCh(data):
    # concatenates the data from two channels into a single array

    waves = len(data[0])
    Ndata = np.zeros((waves, 18000))
    for ch in range(len(data)):
        for w in range(0, waves):
            try:
                Ndata[w, :] = np.concatenate((data[0][w], data[ch + 1][w]))
            except:
                pass
    return Ndata

def multisiteSave(data, directory, name):  # data is an numpy array
    # saves nested array of multichannel data to a

    Dir = directory
    if not os.path.isdir(Dir):
        os.makedirs(Dir)
    for i in range(len(data)):
        with open(Dir + name + '_wave' + str(i) + '.csv', 'w') as f1:
            write = csv.writer(f1)
            write.writerow(data[i])


def multisiteSave2(data, directory, name):  # data is an numpy array
    #Save each channel seperately in different files
    Dir = directory
    n = name
    CH1 = data[0]
    CH2 = data[1]
    if not os.path.isdir(Dir):
        os.makedirs(Dir)
    for i in range(0, 3):
        with open(Dir + n + '_CH1' + '_wave' + str(i) + '.csv', 'w') as f1:
            write = csv.writer(f1)
            write.writerow(CH1[i])
        with open(Dir + n + '_CH2' + '_wave' + str(i) + '.csv', 'w') as f1:
            write = csv.writer(f1)
            write.writerow(CH2[i])


def namer(f):
    #removes the "." from the file name
    n = os.path.basename(f)
    tn = n.split(".")

    return tn[0]


def findCTRL(file1, folder):
    #used to find the control file.
    result = 1000000000
    ctrl = None
    date = os.path.basename(file1).split('_')[0]
    pfiles = [x for x in folder if date.lower() in os.path.basename(x.lower())]
    for x in pfiles:
        #get the time difference between experiment and the control. repeat for all files in folder
        tt = abs(os.path.getmtime(file1) - os.path.getmtime(x))
        if tt < result:
            #if the difference is smaller than the result variable then replace "result" with new dif
            result = tt
            ctrl = x
            # print(ctrl)
    return ctrl

def findNORM(file1, folder):
    print(f'finding the normalizer for: {file1}')
    #used the find the control file.
    result = 1000000000
    ctrl = None
    concentration = file1.split('_')[3].lower()
    date = os.path.basename(file1).split('_')[0]
    print(f'concentration of file is: {concentration.lower()}')
    print(f'date of file is: {date}')
    pfiles = [x.lower() for x in folder if concentration.lower() in os.path.basename(x.lower())]
    print(pfiles)
    pfiles2 = [x for x in pfiles if date.lower() in os.path.basename(x.lower())]
    print(pfiles2)
    for x in pfiles2:
        #get the time difference between experiment and the control. repeat for all files in folder
        tt = abs(os.path.getmtime(file1) - os.path.getmtime(x))
        if tt < result:
            #if the difference is smaller than the result variable then replace "result" with new dif
            result = tt
            ctrl = x
            # print(ctrl)
    return ctrl


def open_wave(FILE):
    #open a csv file containing a EAG wave
    with open(FILE, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    f.close()
    l = data[0]
    l = list(map(float, l))
    return l


def csv_plot(FILE, NAME, SDir, SAVE=True):
    #plot a csv file
    t = open_wave(FILE)
    # n=NAME.split("\\")
    plt.title(label=NAME, size=10)
    plt.plot(t, color='black')
    plt.axvspan(500, 1000, color='pink', alpha=.25)
    plt.ylim(-1.5,1.5)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    if SAVE == True:
        plt.savefig(SDir+NAME+".svg")
        plt.savefig(SDir+NAME+".jpg")
        plt.show()
        plt.close()
    else:
        plt.show()
        plt.close()


def MinMax_Norm(xdata):
    # Normalize the data to the greatest responding odorant (Currently YlangYlang)
    # Ylangylang is used as the "control"
    mx = max(xdata)
    mn = min(xdata)
    xScaled = [((n - mn) / (mx - mn)) for n in xdata]

    # for n in xdata:
    # x=(n-mn)/(mx-mn)
    # xScaled.append(x)
    return xScaled


def Min_Normalization(minCTRL_xdata, xdata):
    """Normalize the data to the greatest responding odorant (Currently YlangYlang)
    Ylangylang is used as the "control"""

    xScaled = []
    mx = max(minCTRL_xdata)
    mn = min(minCTRL_xdata)
    for n in xdata:
        x = (n - mn) / (mx - mn)
        xScaled.append(x)
    return xScaled

def log_transform(file):
    """
    Apply log2 transformation to a numpy array.

    Parameters:
    file (ndarray): A numpy array to be transformed.

    Returns:
    ndarray: A log2 transformed numpy array.
    """
    # Get the minimum value in the array and add a small value to prevent taking the log of zero
    a = np.min(file)
    # Apply the log2 transformation to each element in the array
    log2T = [np.log2(x + a) for x in file]
    return log2T

def EAG_Cov_df_build(DIR):
    """
        Builds a Pandas DataFrame from all CSV files in a directory that contain 'cov1' in their names.

        Args:
            DIR (str): Path to the directory containing the CSV files.

        Returns:
            A Pandas DataFrame containing the wave data from all CSV files in the directory that contain 'cov1' in their names.
            The DataFrame has one row per file, with columns for the wave data, label, concentration, and date.
        """
    files = glob.glob(f"{DIR}/*.csv")
    data = {os.path.basename(file).lower().replace('.csv', ''): open_wave(file) for file in files if 'cov1' in file.lower()}
    df = pd.DataFrame(data).T
    df['label'] = [name.split('_')[2] for name in df.index]
    df['concentration'] = [name.split('_')[1] for name in df.index]
    df['date'] = [name.split('_')[0] for name in df.index]
    df.index = df.index.str.replace('_', '')
    return df


"""def find_MaxIntenseWave(data):

    m = 0
    best = data
    for l in range(len(data)):
        mx = max(abs(data[l].T))
        wave = data[0]
        if mx > m:
            wave = data[l]
            m = mx
            best = wave
    return best"""

def find_MaxIntenseWave(data):
    """
    This function takes an array of waves as input and returns the wave with the highest maximum absolute value.

    Args:
    - data: A 2D numpy array of shape (n, m) containing n waves, each with m samples.

    Returns:
    - The wave with the highest maximum absolute value as a 1D numpy array.

    Example:
    >>> data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> find_MaxIntenseWave(data)
    array([7, 8, 9])
    """
    best_index = max(range(len(data)), key=lambda i: abs(data[i]).max())
    return data[best_index]

def EAG_df_build(DIR):
    F_List = [os.path.join(dirpath, filename) for dirpath, dirnames, filenames in os.walk(DIR) for filename in
              filenames if '.DS_Store' not in filename]
    master = []
    mastern = []
    masterl = []
    masterc = []
    masterDate = []

    for file in F_List:
        print(file)
        n = os.path.basename(file.lower()).split("_")
        name = n[0] + n[1] + n[2] + n[3] + n[4].replace('.csv', '')
        lab = n[2]
        conc = n[1]
        date = n[0]
        x = open_wave(file)
        master.append(x)
        mastern.append(name)
        masterl.append(lab)
        masterc.append(conc)
        masterDate.append(date)


    master_df = pd.DataFrame(dict(zip(mastern, master)), index=[x for x in range(0, len(x))])
    master_df = master_df.T
    master_df['label'] = masterl
    master_df['concentration'] = masterc
    master_df['date'] = masterDate

    return master_df

def Mean_Smoothing(data, window, normalized=False):
    if normalized==True:
        filtsig = [1 for x in range(len(data))]
    elif normalized ==False:
        filtsig = [0 for x in range(len(data))]
    for i in range (window+1, len(data)-window-1):
        filtsig[i] = np.mean(data[i-window:i+window])
    windowsize = 1000*(window*2+1) / 1000
    return np.array(filtsig)

def get_subdirectories(directory):
    subdirectories = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isdir(path):
            subdirectories.append(path)
    return subdirectories

def process_data(DIR, savedir=None, SUB=False, SUM=False, Norm='YY', Smoothen=False, LOG=False, Butter=[],
                 B_filt=True, RETURN='Save'):
    """
        Process data from DList and save the processed data to savedir.

        Parameters:
        DList (list): A list of directories containing the data to process.
        norm (str): Normalization method to use. Possible values: 'YY', 'Yes', False. Default is 'YY'. This normalizes
                    data to the strongest odorant ylangylang.
        sub (bool): Whether to subtract channel 1 from channel 2. Default is False.
        savedir (str): Directory to save processed data to. Default is ''.

        Returns: None
        """
    B_filt = B_filt
    Sub = SUB
    Sum = SUM
    SAVEDIR = savedir
    #DList=[(subdir +'/') for directory in DL for subdir in get_subdirectories(directory)]
    FileList = [os.path.join(dirpath, filename) for dirpath, dirnames, filenames in os.walk(DIR) for filename in
                filenames if '.DS_Store' not in filename]

    f1 = [f for f in FileList
          if 'DS_Store' not in os.path.basename(f)]
    # seperate the data into experimental and control lists
    ctrl = [x for x in f1 if 'mineraloil' in os.path.basename(x) or 'Mineral_Oil' in os.path.basename(
        x)]  # if 'BagNoOdor' in os.path.basename(x)
    print(f'these are {len(ctrl)} control files')
    exp = [x for x in f1 if 'mineraloil' not in os.path.basename(x) and 'Mineral_Oil' not in os.path.basename(
        x) and '_300_' not in os.path.basename(x) and '_3k_' not in os.path.basename(x)]
    # print(f'these are the experiments {exp}')
    YY = [x for x in f1 if 'ylangylang' in os.path.basename(x) or 'YlangYlang' in os.path.basename(x)]
    print(f'these are {len(YY)} control files')

    # Do we want to Normalize the data?
    Normalize = Norm
    # Extract the each individual wave and subtract the miniral oil control
    for e in exp:
        data = e
        control = findCTRL(data, ctrl)
        MINIM = findNORM(data, YY)
        # print(data,control)
        n = os.path.basename(data)
        print(n, 'is an experiment')
        VOC = n.split("_")[2]

        DIR = SAVEDIR + VOC + '/'
        n = namer(data)
        print('pre meag',data)
        Odor = Extract_mEAG(data, Butter[0], Butter[1], Butter[2], BF=B_filt)
        CTRL = Extract_mEAG(control, Butter[0], Butter[1], Butter[2], BF=B_filt)
        MIN = Extract_mEAG(MINIM, Butter[0], Butter[1], Butter[2], BF=B_filt)
        print(Odor)
        for x in range(0, 3):
            # subtract the control
            Odor[0][x, :] = Odor[0][x, :] - (CTRL[0].mean(axis=0))
            Odor[1][x, :] = Odor[1][x, :] - (CTRL[1].mean(axis=0))
            #subtract the signal of tip from the base
            Odor[1][x, :] = Odor[0][x, :] - Odor[1][x, :]

            MIN[0][x, :] = MIN[0][x, :] - (CTRL[0].mean(axis=0))
            MIN[1][x, :] = MIN[1][x, :] - (CTRL[1].mean(axis=0))
            # subtract channel 1 from channel 2
            if Sub == True:
                Odor[0][x, :] = -1 * Odor[0][x, :]
                Odor[0][x, :] = Odor[1][x, :] - Odor[0][x, :]

            if Sum == True:
                Odor[0][x, :] = -1 * Odor[0][x, :]

                Odor[0][x, :] = Odor[1][x, :] + Odor[0][x, :]

        MIN1 = find_MaxIntenseWave(MIN[0])
        MIN2 = find_MaxIntenseWave(MIN[1])
        if Normalize == 'Yes':
            for x in range(0, 3):
                Odor[0][x, :] = MinMax_Norm(Odor[0][x, :])
                Odor[1][x, :] = MinMax_Norm(Odor[1][x, :])

        elif Normalize == 'YY':
            for x in range(0, 3):
                # normalize to ylangylang each channel seperately
                Odor[0][x, :] = Min_Normalization(MIN1, Odor[0][x, :])
                Odor[1][x, :] = Min_Normalization(MIN2, Odor[1][x, :])
                # baseline the result to 0
                avg = np.mean(Odor[0][x, 0:500])
                Odor[0][x, :] = [n - avg for n in Odor[0][x, :]]
                avg = np.mean(Odor[1][x, 0:500])
                Odor[1][x, :] = [n - avg for n in Odor[1][x, :]]

                if Smoothen == True:
                    for x in range(0, 3):
                        Odor[0][x, :] = Mean_Smoothing(data = Odor[0][x, :], window=125, normalized=True)
                        Odor[1][x, :] = Mean_Smoothing(data = Odor[1][x, :], window=125, normalized=True)

        elif Normalize == False:
            for x in range(0, 3):
                avg = np.mean(Odor[0][x, 0:500])
                Odor[0][x, :] = [n - avg for n in Odor[0][x, :]]
                avg = np.mean(Odor[1][x, 0:500])
                Odor[1][x, :] = [n - avg for n in Odor[1][x, :]]

        if Smoothen == True:
            for x in range(0, 3):
                Odor[0][x, :] = Mean_Smoothing(data = Odor[0][x, :], window=125, normalized=False)
                Odor[1][x, :] = Mean_Smoothing(data = Odor[1][x, :], window=125, normalized=False)

        if LOG == True:
            Odor[0][x, :] = log_transform(Odor[0][x, :])
            Odor[1][x, :] = log_transform(Odor[1][x, :])


        if  (Sub or Sum)  != True:

            print('neither subtraction or addition happened')
            Odor = ConcCh(Odor)

            # plt.plot(Odor[0])
            # plt.show()

            # multisiteSave2(Odor,directory=DIR, name=n)

        if RETURN == 'SAVE':
            if Sub == True:
                multisiteSave(Odor[0], directory=DIR, name=n)
            elif Sum == True:
                multisiteSave(Odor[0], directory=DIR, name=n)
            else:
                multisiteSave(Odor, directory=DIR, name=n)

        elif RETURN == 'PLOT':
            plt.plot(Odor[1][0])
            plt.show()

def PSD_analysis(data):
    dt = 1
    t = np.arange(9000, 18000, dt)
    n = len(t)
    fhat = np.fft.fft(data.T, n)  # Compute the FFT
    PSD = np.abs(fhat) ** 2 / (dt * n)  # Power spectrum (power per freq)
    freq = np.fft.fftfreq(n, dt)[:n//2]  # Create x-axis of frequencies in Hz
    return PSD[:n//2], freq


def FFT_analysis(data, th):
    dt = 1
    t = np.arange(0, 9000, dt)
    n = len(t)
    fhat = np.fft.fft(data.T, n)
    PSD = np.abs(fhat) ** 2 / n
    freq = ((dt * n) / 9) * np.arange(n)
    L = np.arange(1, n // 2)
    alpha, pcov = optimize.curve_fit(lambda x, a, b: a * x + b, freq[1:9], np.log(PSD[1:9]))
    if pcov[1][1] > th:
        perr = np.sqrt(np.diag(pcov))
        print('perr:', perr)
    PSD[PSD <= 2] = 0
    return pcov[1][1]

def FFT_LSTSQ_QC(df,t):
    if len(df) > 10000:
        CH1=df.T.iloc[:9000,]
        CH2=df.T.iloc[9000:-3,]
        E_List=list(df.T.columns)
        good1=[CH1.columns[x] for x in range(len(CH1.columns)) if
            (FFT_analysis(CH1[E_List[x]],th=t)) < t]
        good2=[CH2.columns[x] for x in range(len(CH2.columns)) if
            (FFT_analysis(CH2[E_List[x]],th=t)) < t]
        good=list(np.intersect1d(good1,good2))
        QCdf=df.T[good]
    else:
        CH1 = df.T.iloc[:9000, ]
        E_List = list(df.T.columns)
        good = [CH1.columns[x] for x in range(len(CH1.columns)) if
                 (FFT_analysis(CH1[E_List[x]], th=t)) < t]
        QCdf = df.T[good]
    print(len(df))
    print(len(QCdf.T))
    return(QCdf)

def find_sol1(data):#data = abf.sweepY of second channel out of three channels "channel = 1" from abf file
    SolFall = np.diff(data)
    NI = [i*.001 for i,v in enumerate(SolFall) if v < -0.3]
    PI = [i*.001 for i,v in enumerate(SolFall) if v > 0.3]
    test=zip(PI,NI)
    sol=list(test)
    return(sol)

def intensity_alignment(df):
    IDmins=list(df.iloc[:,:2600].idxmin(axis=1))
    min_idx=[int(x) for x in IDmins]
    maxSHIFT=max(min_idx)
    df_data = df.iloc[:, :-3]
    index_map = {name: i for i, name in enumerate(df_data.index)}
    shifted_df_data = df_data.apply(lambda row: row.shift(maxSHIFT - min_idx[index_map[row.name]]), axis=1)
    shifted_df_data.fillna(0, inplace=True)
    return shifted_df_data

    #SHFT=intensity_alignment(df)
