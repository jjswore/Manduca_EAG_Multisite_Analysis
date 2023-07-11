from Manduca_Multisite_EAG_Analysis.Disease_VOC_Analysis.Data_Processing.EAG_DataProcessing_Library import *

base='/Users/joshswore/Manduca/MultiChannel/TedlarBagExperiments/Raw_Data/050923/'
MA='050923M1A1/'
KetAld40ul = f'{base}{MA}050923M1A1_40ul_KetAldStandard_0002.abf'
KetAld10ul = f'{base}{MA}050723M1A1_10ul_KetAldStandard_0003.abf'
KetAld20ul = f'{base}{MA}050723M2A1_20ul_KetAldStandard_0003.abf'
ylangylang = f'{base}{MA}050723M2A1_10ul_ylangylang_0002.abf'
Covid=f'{base}{MA}050723M2A1_10ul_ArtCov1_0004.abf'
NoBag = f'{base}{MA}050723M2A1_10ul_NoBag_0008.abf'
C1 = f'{base}{MA}050723M1A1_1_BagNoOdor_0002.abf'
C2 = f'{base}{MA}050723M2A1_20ul_BagNoOdor_0002.abf'
C3 = f'{base}{MA}050723M2A1_10ul_BagNoOdor_0004.abf'

cov = pyabf.ABF(Covid)
cov.setSweep(0, channel=2)
NB = pyabf.ABF(NoBag)
NB.setSweep(0, channel=2)
KA1ul = pyabf.ABF(KetAld1ul)
KA1ul.setSweep(0, channel=2)
KA10ul = pyabf.ABF(KetAld10ul)
KA10ul.setSweep(0, channel=2)
KA20ul = pyabf.ABF(KetAld20ul)
KA20ul.setSweep(0, channel=2)
YY10ul = pyabf.ABF(ylangylang)
YY10ul.setSweep(0, channel=2)
ctrl1 = pyabf.ABF(C1)
ctrl1.setSweep(0, channel=2)
ctrl2 = pyabf.ABF(C2)
ctrl2.setSweep(0, channel=2)
ctrl3 = pyabf.ABF(C3)
ctrl3.setSweep(0, channel=2)
starttime=26000
time = 31000
# NC=abf.channelCount

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(18, 10))

KA1ul.setSweep(0, channel=1)

sol = find_sol1(KA1ul.sweepY[0:time])

KA1ul.setSweep(0, channel=2)
ctrl1Y=Mean_Smoothing(ctrl1.sweepY[:],window=125)
ctrl2Y=Mean_Smoothing(ctrl2.sweepY[:],window=125)
ctrl3Y=Mean_Smoothing(ctrl3.sweepY[:],window=125)
NBY=Mean_Smoothing(NB.sweepY[:],window=125)
covY=Mean_Smoothing(cov.sweepY[:],window=125)

KA1ulY=Mean_Smoothing(KA1ul.sweepY[:],window=125)
KA10ulY=Mean_Smoothing(KA10ul.sweepY[:],window=125)
KA20ulY=Mean_Smoothing(KA20ul.sweepY[:],window=125)
YY10ulY=Mean_Smoothing(YY10ul.sweepY[:],window=125)

def baseline(data):
    m=np.mean(data[25600:26000])
    bdata=[x-m for x in data]
    return bdata

dlist=[ctrl1Y,ctrl2Y,ctrl3Y,NBY,covY,KA1ulY,KA10ulY,KA20ulY,YY10ulY]
for d in dlist:
    d[:]=baseline(d)

ax.axvspan(.63, 1.13, color='red', alpha=.25)

# ax.axvspan(sol[1][0],sol[1][1],color='red',alpha=.25)
# ax.axvspan(sol[2][0],sol[2][1],color='red',alpha=.25)


# h=pyabf.ABF(Healthy)
# name=name_con(Healthy)
frame_rate = 1000  # Hz
duration = len(KA20ulY[starttime:time]) / frame_rate  # seconds
Xaxis = np.linspace(0, duration, len(KA20ulY[starttime:time]))

# fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(18, 10))
KA20ul.setSweep(0, channel=2)

ax.plot(Xaxis, KA20ulY[starttime:time]-ctrl2Y[starttime:time], color='blue', label='KetAld 20ul')
ax.set_ylabel(ylabel=KA1ul.sweepLabelY, fontsize=35, fontname='Arial')
ax.set_xlabel(xlabel='Time (S)', fontsize=35, fontname='Arial')
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=35)

cov.setSweep(0, channel=2)

ax.plot(Xaxis, covY[starttime:time]-ctrl3Y[starttime:time], color='steelblue', label='Covid')
ax.set_ylabel(ylabel=cov.sweepLabelY, fontsize=35, fontname='Arial')
ax.set_xlabel(xlabel='Time (S)', fontsize=35, fontname='Arial')
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=35)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.ylim(-35,35)
plt.legend(fontsize=20)
plt.savefig('/Users/joshswore/Manduca/MultiChannel/TedlarBagExperiments/KetAlds_Cov.svg')
plt.show()

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(18, 10))
KA1ul.setSweep(0, channel=2)
ax.axvspan(.63, 1.13, color='red', alpha=.25)
ax.plot(Xaxis, KA1ulY[starttime:time]-ctrl1Y[starttime:time], color='blue', label='KetAld 1ul')
ax.set_ylabel(ylabel=KA1ul.sweepLabelY, fontsize=35, fontname='Arial')

ax.tick_params(axis='y', labelsize=20)

KA10ul.setSweep(0, channel=2)

ax.plot(Xaxis, KA10ulY[starttime:time]-ctrl1Y[starttime:time], color='skyblue', label='KetAld 10ul')
ax.set_ylabel(ylabel=KA1ul.sweepLabelY, fontsize=35, fontname='Arial')
ax.set_xlabel(xlabel='Time (S)', fontsize=35, fontname='Arial')
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

YY10ul.setSweep(0, channel=2)

ax.plot(Xaxis, YY10ulY[starttime:time]-ctrl2Y[starttime:time], color='navy', label='ylangylang 10ul')
ax.set_ylabel(ylabel=YY10ul.sweepLabelY, fontsize=35, fontname='Arial')
ax.set_xlabel(xlabel='Time (S)', fontsize=35, fontname='Arial')
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=35)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.ylim(-35,35)
plt.legend(fontsize=20)

plt.savefig('/Users/joshswore/Manduca/MultiChannel/TedlarBagExperiments/KetAlds_YY_NoResponse.svg')
plt.show()

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(18, 10))
ax.axvspan(.63, 1.13, color='red', alpha=.25)
ax.plot(Xaxis, NBY[starttime:time], color='grey', label='No Bag')
ax.set_ylabel(ylabel=NB.sweepLabelY, fontsize=35, fontname='Arial')
ax.set_xlabel(xlabel='Time (S)', fontsize=35, fontname='Arial')
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=35)

ax.plot(Xaxis, ctrl3Y[starttime:time], color='black', label='Bag No Odor')
ax.set_ylabel(ylabel=ctrl2.sweepLabelY, fontsize=35, fontname='Arial')
ax.set_xlabel(xlabel='Time (S)', fontsize=35, fontname='Arial')
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=35)
# ax.axvspan(sol[0][0],sol[0][1],color='red',alpha=.25)
# ax.axvspan(sol[1][0],sol[1][1],color='red',alpha=.25)
# ax.axvspan(sol[2][0],sol[2][1],color='red',alpha=.25)


plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.ylim(-35,35)
plt.legend(fontsize=20)


plt.savefig('/Users/joshswore/Manduca/MultiChannel/TedlarBagExperiments/controls.svg')
plt.show()