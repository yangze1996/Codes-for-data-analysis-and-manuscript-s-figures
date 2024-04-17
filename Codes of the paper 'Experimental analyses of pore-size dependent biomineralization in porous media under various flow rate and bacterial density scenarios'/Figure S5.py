import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

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
# Create a transformation function for the y-axis labels
def y_fmt_1(y, pos):
    return f'{abs(y):.0f}'
def y_fmt_2(y, pos):
    return f'{abs(y):.01f}'
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

    ratio_less_than_300ms = (sum_less_than_60ms[0] + sum_60_to_300ms[0]-sum_less_than_60ms[6] - sum_60_to_300ms[6])/(sum_T2[0] - sum_T2[6])
    ratio_greater_than_300ms = (sum_greater_than_300ms[0]-sum_greater_than_300ms[6]) /(sum_T2[0] - sum_T2[6])
    ratios_less_than_300ms_list.append(ratio_less_than_300ms)
    ratios_greater_than_300ms_list.append(ratio_greater_than_300ms)

# Custom x-axis labels
custom_labels = ['v=0.5mL/min', '1', '2', 'OD=0.2', '0.8', '1.6']

# Create a figure and axis
fig, ax1 = plt.subplots()

# Scatter plots for the data
ax1.scatter(custom_labels, [item[0] - item[6] for item in sum_T2_list], label='Global', marker='o', edgecolor='blue',facecolor='none')
ax1.scatter(custom_labels, [item[0] - item[6] for item in sum_greater_than_300ms_list], label='Macropores', marker='s', edgecolor='orange',facecolor='none')
ax1.scatter(custom_labels, [item[0] - item[6] for item in sum_60_to_300ms_list], label='Mesopores', marker='^', edgecolor='green',facecolor='none')
ax1.scatter(custom_labels, [item[0] - item[6] for item in sum_less_than_60ms_list], label='Micropores', marker='D', edgecolor='red',facecolor='none')
print([ item[6]- item[5] for item in sum_T2_list])
# Set y-axis labels
ax1.set_xlabel('Experiments', fontsize=14)
ax1.set_ylabel('Total NMR signal amplitude (A.u.)', fontsize=14)

# # Create a secondary y-axis
# ax2 = ax1.twinx()

# # Scatter plots for the ratios
# ax2.scatter(custom_labels, ratios_less_than_300ms_list, label='Ratio_Mac', marker='x',color='black')
# ax2.scatter(custom_labels, ratios_greater_than_300ms_list, label='Ratio_Mic+Mes', marker='+',color='black')

# # Set y-axis label for the secondary y-axis
# ax2.set_ylabel('Ratios', fontsize=12)

# # Apply the custom y-axis label transformation
# ax1.yaxis.set_major_formatter(FuncFormatter(y_fmt_1))
# # Apply the custom y-axis label transformation
# ax2.yaxis.set_major_formatter(FuncFormatter(y_fmt_2))
# Add spans and text
ax1.axhspan(ymin=0, ymax=39000, facecolor='yellow', alpha=0.2)
ax1.axhspan(ymin=-12200, ymax=0, facecolor='green', alpha=0.2)
ax1.set_ylim(-2000, 4000)

# Combine legend handles
handles1, labels1 = ax1.get_legend_handles_labels()
# handles2, labels2 = ax2.get_legend_handles_labels()
all_handles = handles1 
all_labels = labels1
# Show legends
ax1.legend(all_handles, all_labels, loc='upper left',ncol=1,fontsize=14,frameon=False)
ax1.axvline(x=len(custom_labels) / 2-0.5, linestyle='--', color='gray', linewidth=1.8)
ax1.tick_params(axis='x', labelsize=14)
ax1.tick_params(axis='y', labelsize=14)
ax1.yaxis.set_major_formatter(FuncFormatter(y_fmt_1))
# Add spacing and show the plot
plt.tight_layout()
# Save and show the figure
plt.savefig("E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/Figure/8-Pore-size-dependent change of pore volume.jpg", dpi=1200)
plt.show()
