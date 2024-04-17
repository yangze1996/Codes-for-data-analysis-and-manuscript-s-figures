import pandas as pd
import matplotlib.pyplot as plt

file_path = "E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/原始资料/T2 distribution.xlsx"
data = pd.read_excel(file_path)

# List of sheet names in the Excel file
sheet_names = ['SR', 'BR', 'FR', 'LD', 'BD', 'HD']
# Custom tick label names
custom_tick_labels = ['$\mathit{Ini}$.', 'C1', 'C2', 'C3', 'C4', 'C5', '$\mathit{Bio}$.', '$\mathit{Com}$.']

# Define the subplot labels for each column
col_labels = ['(a) Slow Injection Rate (SR)', '(b) Basic Injection Rate (BR)', '(c) Fast Injection Rate (FR)',
              '(d) Low Bacterial Density (LD)', '(e) Basic Bacterial Density (BD)', '(f) High Bacterial Density (BD)']

# Define custom colors for the variables
colors = [(160 / 255, 109 / 255, 32 / 255, 0.7), (218 / 255, 160 / 255, 83 / 255, 0.7),
          (255 / 255, 215 / 255, 134 / 255, 0.7), 'green', 'blue', 'orange', 'grey']
# 定义自定义颜色列表 cycle_colors
cycle_colors = [(0.8, 0.2, 0.2), (0.2, 0.8, 0.2), (0.2, 0.2, 0.8), (0.8, 0.8, 0.2), (0.8, 0.2, 0.8)]
# 创建一个 3x2 的子图网格
# Create a 3x2 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(16, 20), gridspec_kw={'top': 0.885})

# Loop through each sheet and create stacked bar charts for each subplot
for i, sheet_name in enumerate(sheet_names):
    data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Calculate the sum of the 'T2_initial' column
    sum_T2_initial = data['T2_initial'].sum()

    # Exclude the 'T2' column from sum calculations
    columns_to_sum = data.columns[1:]  # Exclude the first column 'T2'

    # Calculate the sum of values for each column where T2 values are less than 60 ms
    sum_less_than_60ms = data.loc[data['T2'] < 60, columns_to_sum].sum()

    # Calculate the sum of values for each column where T2 values are between 60 ms and 300 ms
    sum_60_to_300ms = data.loc[(data['T2'] >= 60) & (data['T2'] <= 300), columns_to_sum].sum()

    # Calculate the sum of values for each column where T2 values are greater than 300 ms
    sum_greater_than_300ms = data.loc[data['T2'] > 300, columns_to_sum].sum()

    # Calculate the fraction of each column for micropores, mesopores, and macropores
    fraction_less_than_60ms = sum_less_than_60ms / sum_T2_initial
    fraction_60_to_300ms = sum_60_to_300ms / sum_T2_initial
    fraction_greater_than_300ms = sum_greater_than_300ms / sum_T2_initial
    
    # Create a DataFrame to hold the fractions
    fraction_data = pd.DataFrame({
        'Micropores (<60 ms)': fraction_less_than_60ms,
        'Mesopores (60-300 ms)': fraction_60_to_300ms,
        'Macropores (>300 ms)': fraction_greater_than_300ms
    })

    # Calculate the sum of micropores, mesopores, and macropores for each row
    fraction_data['Sum'] = fraction_data['Micropores (<60 ms)'] + fraction_data['Mesopores (60-300 ms)'] + \
                           fraction_data['Macropores (>300 ms)']

    # Create a new column 'Product' as 1 minus the sum
    fraction_data['Product'] = 1 - fraction_data['Sum']

    # Drop the 'Sum' column if you don't need it in the final DataFrame
    fraction_data.drop(columns=['Sum'], inplace=True)
    # Convert the values to percentages and round them to two decimal places
    fraction_data *= 100
    fraction_data = fraction_data.round(1)

    # Calculate the 'biogas' column as the difference between 'T2_cycle5' and 'T2_biomineralized'
    fraction_data_biogas = fraction_data.iloc[5, 3] - fraction_data.iloc[6, 3]
    fraction_data_water = fraction_data.iloc[5, 0] + fraction_data.iloc[5, 1] + fraction_data.iloc[5, 2]
    fraction_data_precipitation = 100 - fraction_data_biogas - fraction_data_water

    # Create a new DataFrame to hold the biogas, water, and precipitation fractions
    biogas_water_precipitation_data = pd.DataFrame({
        'Water': [fraction_data_water],
        'Biogas': [fraction_data_biogas],
        'Precipitation': [fraction_data_precipitation]
    })
    # Calculate the  "three components" as the sum of biogas, water, and precipitation
    fraction_data['Three Components'] = fraction_data_biogas + fraction_data_precipitation + fraction_data_water

    # Create a DataFrame with the desired data for the stacked bar chart
    plot_data = pd.concat([fraction_data.iloc[:, [2, 1, 0, 3]], biogas_water_precipitation_data], axis=1)

    # Get the current axis from the axes array
    row = i % 3  # 计算行索引，循环范围是0-2
    col = i // 3   # 计算列索引，循环范围是0-1
    ax = axes[row, col]

    # 创建当前子图的堆叠条形图
    plot_data.plot(kind='bar', stacked=True, color=colors, ax=ax)
    ax.set_title(col_labels[i], fontsize=20)  # 使用相应的标题标签
    ax.set_ylabel("Volume Fraction (%)", fontsize=20)
    ax.set_xticklabels(custom_tick_labels, rotation=0, fontsize=15, ha='center')
    ax.set_yticklabels(ax.get_yticks().astype(int), fontsize=16)
    ax.legend().set_visible(False)

# Add legend above the subplots, showing all legend items
legend_labels = ['Macropores ($\t{T}_{2}$>300 ms)', 'Mesopores (60 ms<$\t{T}_{2}$<300 ms)'
                 ,'Micropores ($\t{T}_{2}$<60 ms)', 'Products', 'Water','Biogas','Precipitate']
fig.legend(handles=ax.containers, labels=legend_labels, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 0.995),
           fontsize=20, frameon=False)

plt.tight_layout()
# Save and show the figure
plt.savefig("E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/Figure/2- Water distribution in the bio-exp.jpg", dpi=1200)
# 显示图形
plt.show()
