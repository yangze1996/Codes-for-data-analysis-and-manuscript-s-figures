import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec

# Create a figure and grid layout
fig = plt.figure(figsize=(9, 4))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

# Create left subplot
ax_left = plt.subplot(gs[0])
ax_left.set_title('(a) Reaction Rate', fontsize=14)
ax_left.set_ylabel('Reaction Rate (d\u207B\u00B9)', fontsize=14, color='black')
ax_left.set_xlabel('Experiments', fontsize=14, labelpad=8, ha='center')

# Create right subplot
ax_right = plt.subplot(gs[1])
ax_right.set_title('(b) Biomineralization Efficiency', fontsize=14)
ax_right.set_ylabel('Biomineralization Efficiency', fontsize=14, color='black')
ax_right.set_xlabel('Experiments', fontsize=14, labelpad=8, ha='center')

# Custom x-axis labels
custom_labels = ['v=0.5mL/min', '1', '2', 'OD=0.2', '0.8', '1.6']

file_path = "E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/原始资料/T2 distribution.xlsx"
columns_to_read = ["T2", "T2_initial", "T2_biomineralized"]
sheet_names = ['SR', 'BR', 'FR', 'LD', 'BD', 'HD']

# Lists to store sum data for each sheet
sum_less_than_60ms_list = []
sum_60_to_300ms_list = []
sum_greater_than_300ms_list = []
sum_T2_list = []
ratios_less_than_300ms_list = []
ratios_greater_than_300ms_list = []
Bio_Eff_list = []
Bio_Eff_1_list = []
Reaction_rate_gobal_list = []
Reaction_rate_Mac_list = []
Reaction_rate_Meso_list = []
Reaction_rate_Mic_list = []
# Create a transformation function for the y-axis labels
def y_fmt_2(y, pos):
    return f'{abs(y):.01f}'
def y_fmt_1(y, pos):
    return f'{abs(y):.02f}'
for sheet_name in sheet_names:
    data = pd.read_excel(file_path, sheet_name=sheet_name)
    # Exclude the 'T2' column from sum calculations
    columns_to_sum = data.columns[1:]  # Exclude the first column 'T2'
    # Calculate the sum of values for each column where T2 values fall into different ranges
    sum_less_than_60ms = data.loc[data['T2'] < 60, columns_to_sum].sum()
    sum_60_to_300ms = data.loc[(data['T2'] >= 60) & (data['T2'] <= 300), columns_to_sum].sum()
    sum_greater_than_300ms = data.loc[data['T2'] > 300, columns_to_sum].sum()
    sum_T2 = data.loc[(data['T2'] >= 0) , columns_to_sum].sum()

    sum_less_than_60ms_list.append(sum_less_than_60ms)
    sum_60_to_300ms_list.append(sum_60_to_300ms)
    sum_greater_than_300ms_list.append(sum_greater_than_300ms)
    sum_T2_list.append(sum_T2)

    Reaction_rate_gobal = (sum_T2[0] - sum_T2[6])/(sum_T2[0]*5)
    Reaction_rate_gobal_list.append(Reaction_rate_gobal)
    Reaction_rate_Mac = (sum_greater_than_300ms[0] - sum_greater_than_300ms[6])/(sum_greater_than_300ms[0]*5)
    Reaction_rate_Mac_list.append(Reaction_rate_Mac)
    Reaction_rate_Meso = (sum_60_to_300ms[0] - sum_60_to_300ms[6])/(sum_60_to_300ms[0]*5)
    Reaction_rate_Meso_list.append(Reaction_rate_Meso)
    Reaction_rate_Mic = (sum_less_than_60ms[0] - sum_less_than_60ms[6])/(sum_less_than_60ms[0]*5)
    Reaction_rate_Mic_list.append(Reaction_rate_Mic)

    ratio_less_than_300ms = (sum_less_than_60ms[0] + sum_60_to_300ms[0]-sum_less_than_60ms[6] - sum_60_to_300ms[6])/(sum_T2[0] - sum_T2[6])
    ratio_greater_than_300ms = (sum_greater_than_300ms[0]-sum_greater_than_300ms[6]) /(sum_T2[0] - sum_T2[6])
    less_than_300ms = sum_less_than_60ms[6] + sum_60_to_300ms[6]-sum_less_than_60ms[0] - sum_60_to_300ms[0]
    greater_than_300ms = sum_greater_than_300ms[0]-sum_greater_than_300ms[6]
    Bio_Eff = (greater_than_300ms/sum_greater_than_300ms[0])/(less_than_300ms/(sum_less_than_60ms[0] + sum_60_to_300ms[0]))
    Bio_Eff_1 = greater_than_300ms/less_than_300ms
    ratios_less_than_300ms_list.append(ratio_less_than_300ms)
    ratios_greater_than_300ms_list.append(ratio_greater_than_300ms)
    Bio_Eff_list.append(Bio_Eff)
    Bio_Eff_1_list.append(Bio_Eff_1)
    print(f"{sheet_name}: {(Bio_Eff)}")
print(Bio_Eff_list)
print(Bio_Eff_1_list)
# Scatter plots for the ratios in the left subplot
ax_left.scatter(custom_labels, Reaction_rate_gobal_list, label='Global', marker='o', facecolor='none', edgecolor='blue', s=50)
ax_left.scatter(custom_labels, Reaction_rate_Mac_list, label='Macropores', marker='s', facecolor='none', edgecolor='orange', s=50)
ax_left.scatter(custom_labels, Reaction_rate_Meso_list, label='Mesopores', marker='^', facecolor='none', edgecolor='green', s=50)
ax_left.scatter(custom_labels, Reaction_rate_Mic_list, label='Micropores', marker='D', facecolor='none', edgecolor='red', s=50)
ax_left.axvline(x=len(custom_labels) / 2-0.5, linestyle='--', color='gray', linewidth=1.8)
ax_left.axhspan(ymin=0, ymax=0.05, facecolor='yellow', alpha=0.2)
ax_left.axhspan(ymin=-0.2, ymax=0, facecolor='green', alpha=0.2)
ax_left.set_ylim(-0.2, 0.05)
ax_left.yaxis.set_major_formatter(FuncFormatter(y_fmt_1))
ax_left.legend(loc='lower left', ncol=1, frameon=False, fontsize=13)

# Scatter plots for the ratios in the right subplot
ax_right.scatter(custom_labels, Bio_Eff_list, label='Bio_Eff', marker='X', color='red', s=50)
ax_right.yaxis.set_major_formatter(FuncFormatter(y_fmt_2))
ax_right.tick_params(labelcolor='black')
ax_right.axvline(x=len(custom_labels) / 2-0.5, linestyle='--', color='gray', linewidth=1.8)

# Add spacing and show the plot
plt.tight_layout()

# Save the figure
plt.savefig("E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/Figure/6 - reactive rate.jpg", dpi=1200)
plt.show()