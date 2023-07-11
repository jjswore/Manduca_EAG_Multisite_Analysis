import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.family'] = 'Arial'
# Load your data
OR6KO = pd.read_csv('/Users/joshswore/Manduca/MultiChannel/OR6_KO/Official/ButterLC.1_HC5/Smoothened/Both_Channels/_QC_T_1.csv', index_col=0)
WTF = pd.read_csv('/Users/joshswore/Manduca/MultiChannel/WildType/Floral/Quality_Controlled_Data/ButterLC.1_HC5/Smoothened/_QC_T_1.csv', index_col=0)
WTFem =pd.read_csv('/Users/joshswore/Manduca/Processed_Data/Smooth_Independent_Waves_EAG_Vals.csv', index_col=0)
WTC = pd.read_csv('/Users/joshswore/Manduca/MultiChannel/WildType/Covid/Official/ButterLC.1_HC5/Smoothened/Both_Channels/_QC_T_1.csv', index_col=0)

# Assuming max_intensity calculation is similar for all datasets and 'labels' and 'concentration' columns are present in all datasets
for df in [OR6KO, WTF, WTC, WTFem]:
    df['max_intensity'] = abs(df.iloc[:, 500:2500].min(axis=1))  # Modify this range
    df['concentration'] = df['concentration'].replace({'1': '1k', 'cov1': '1k'})
    df['label'] = df['label'].replace({'artcov1':'artcov'})# replace '1' and 'cov1' with '1k'

# Filter dataframes
OR6KO = OR6KO.loc[(OR6KO['concentration'] == '1k') & (OR6KO['label'] != 'ketaldstandard')]   # Select only rows where 'concentration' is '1k'
WTF = WTF.loc[WTF['concentration'] == '1k']
WTC = WTC.loc[(WTC['concentration'] == '1k') & (WTC['label'].isin(['artcov', 'healthy1k']))]  # 'artcov' and 'healthy1k' for WTC
WTFem = WTFem.loc[WTFem['concentration']=='1k']# Select only rows where 'concentration' is '1k'

# Assign experiment names
OR6KO['experiment'] = 'OR6 KO'
WTF['experiment'] = 'Floral'
WTC['experiment'] = 'Covid'
WTFem['experiment'] = 'Female (single site)'

# Concatenate dataframes
combined_df = pd.concat([OR6KO, WTF, WTC, WTFem])
fig, ax = plt.subplots(1, 1, sharex=True, figsize=(28,16))

custom_palette = ['blue', 'orange', 'brown', 'red']
# Assuming that 'labels' column is categorical and contains the categories you want to compare
sns.boxplot(x='label', y='max_intensity', hue='experiment', data=combined_df,palette=custom_palette, linewidth=2.5)

# Modify the legend labels
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
# Increase the line width of the spines
plt.gca().spines['left'].set_linewidth(2.5)
plt.gca().spines['bottom'].set_linewidth(2.5)

plt.tick_params(axis='y', labelsize=30)
plt.tick_params(axis='x', labelsize=30)
plt.xlabel('',fontsize=30)
plt.ylabel('Voltage (mV)',fontsize=30)

# Rotate x-axis labels
plt.xticks(rotation=25)

# Change legend labels
legend_labels, _= plt.gca().get_legend_handles_labels()
plt.gca().legend(legend_labels, ['OR6 KO', 'WT Floral', 'WT Covid', 'Female (single site)'], title=None, fontsize=30 )
#plt.savefig('/Users/joshswore/Manduca/Presentations and Updates/figures/OR6KO_WT.svg')
plt.show()



#plt.title('Dose-Response',fontsize=15)