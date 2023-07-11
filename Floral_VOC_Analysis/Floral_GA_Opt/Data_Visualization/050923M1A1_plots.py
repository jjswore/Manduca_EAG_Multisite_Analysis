from Manduca_Multisite_EAG_Analysis.Disease_VOC_Analysis.Data_Processing.EAG_DataProcessing_Library import *

base='/Users/joshswore/Manduca/MultiChannel/TedlarBagExperiments/Raw_Data/050723/'
MA='050723M2A1'
KetAld40ul = f'{base}{MA}/{MA}_20ul_KetAldStandard_0001.abf'
ylangylang = f'{base}{MA}/{MA}_40ul_ylangylang_0002.abf'
#Covid=f'{base}{MA}/{MA}_40ul_ArtCov1_0002.abf'

C1 = f'{base}{MA}/{MA}_20ul_BagNoOdor_0000.abf'

#C3 = f'{base}{MA}/{MA}_40ul_BagNoOdor_0004.abf'
ch=2

starttime=5000
time = 15000

#cov = pyabf.ABF(Covid)
#cov.setSweep(0, channel=ch)
#NB = pyabf.ABF(NoBag)
#NB.setSweep(0, channel=ch)
KA40ul = pyabf.ABF(KetAld40ul)
KA40ul.setSweep(0, channel=ch)

#YY10ul = pyabf.ABF(ylangylang)
#YY10ul.setSweep(0, channel=ch)
ctrl1 = pyabf.ABF(C1)
ctrl1.setSweep(0, channel=ch)

#ctrl3 = pyabf.ABF(C3)
#ctrl3.setSweep(0, channel=ch)
# NC=abf.channelCount

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(18, 10))

KA40ul.setSweep(0, channel=1)

sol = find_sol1(KA40ul.sweepY[0:time])

KA40ul.setSweep(0, channel=ch)
ctrl1Y=Mean_Smoothing(ctrl1.sweepY[:],window=125)
#ctrl2Y=Mean_Smoothing(ctrl2.sweepY[:],window=125)
#ctrl3Y=Mean_Smoothing(ctrl3.sweepY[:],window=125)
#NBY=Mean_Smoothing(NB.sweepY[:],window=125)
#covY=Mean_Smoothing(cov.sweepY[:],window=125)

KA40ulY=Mean_Smoothing(KA40ul.sweepY[:],window=125)
#YY10ulY=Mean_Smoothing(YY10ul.sweepY[:],window=125)

def baseline(data):
    m=np.mean(data[25600:26000])
    bdata=[x-m for x in data]
    return bdata

dlist=[ctrl1Y,KA40ulY]
for d in dlist:
    d[:]=baseline(d)

ax.axvspan(.63, 1.13, color='red', alpha=.25)

# ax.axvspan(sol[1][0],sol[1][1],color='red',alpha=.25)
# ax.axvspan(sol[2][0],sol[2][1],color='red',alpha=.25)


# h=pyabf.ABF(Healthy)
# name=name_con(Healthy)
frame_rate = 1000  # Hz
duration = len(KA40ulY[starttime:time]) / frame_rate  # seconds
Xaxis = np.linspace(0, duration, len(KA40ulY[starttime:time]))

# fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(18, 10))
KA40ul.setSweep(0, channel=ch)

ax.plot(Xaxis, KA40ulY[starttime:time]-ctrl1Y[starttime:time], color='blue', label='KetAld 20ul')
ax.set_ylabel(ylabel=KA40ul.sweepLabelY, fontsize=35, fontname='Arial')
ax.set_xlabel(xlabel='Time (S)', fontsize=35, fontname='Arial')
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=35)




# ax.axvspan(sol[0][0],sol[0][1],color='red',alpha=.25)
# ax.axvspan(sol[1][0],sol[1][1],color='red',alpha=.25)
# ax.axvspan(sol[2][0],sol[2][1],color='red',alpha=.25)


plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.legend(fontsize=20)


#plt.savefig('/Users/joshswore/Manduca/MultiChannel/TedlarBagExperiments/controls.svg')
plt.show()