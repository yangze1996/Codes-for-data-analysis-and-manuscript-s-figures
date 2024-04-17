import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the Excel file
file_path = "E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/原始资料/T2 distribution.xlsx"
sheet_names = ['SR', 'BR', 'FR', 'LD', 'BD', 'HD']  # Add the sheet names you want to process
columns_to_read = ["T2", "T2_initial", "T2_biomineralized"]

permeability_changes = []
porosity_changes = []

for sheet_name in sheet_names:
    data = pd.read_excel(file_path, sheet_name=sheet_name, usecols=columns_to_read)

    # Create a new time range with 1 ms intervals
    time_interval = 1  # in ms
    max_time = data['T2'].max()
    time_values = np.arange(0, max_time + time_interval, time_interval)

    # Interpolate the 'T2_initial' column based on the new time range
    interpolated_t2_initial = np.interp(time_values, data['T2'], data['T2_initial'])
    interpolated_t2_biomineralizated = np.interp(time_values, data['T2'], data['T2_biomineralized'])

    # Calculate the sum of the interpolated_t2_initial and interpolated_t2_biomineralizated data
    sum_interpolated_t2_initial = np.sum(interpolated_t2_initial)
    sum_interpolated_t2_biomineralizated = np.sum(interpolated_t2_biomineralizated)

    # Divide the sum into 17 equal parts
    num_parts = 17
    sum_per_part_initial = sum_interpolated_t2_initial / num_parts
    sum_per_part_biomineralizated = sum_interpolated_t2_biomineralizated / num_parts

    # Calculate the indices where the sum reaches the target for each part
    cumulative_sum_initial = np.cumsum(interpolated_t2_initial)
    cumulative_sum_biomineralizated = np.cumsum(interpolated_t2_biomineralizated)

    sum_indices_initial = np.searchsorted(cumulative_sum_initial, np.arange(sum_per_part_initial, sum_interpolated_t2_initial, sum_per_part_initial))
    sum_indices_biomineralizated = np.searchsorted(cumulative_sum_biomineralizated, np.arange(sum_per_part_biomineralizated, sum_interpolated_t2_biomineralizated, sum_per_part_biomineralizated))

    # Calculate the X values for the start and end of each interval
    x_values_by_section_initial = [(time_values[start_index], time_values[end_index]) for start_index, end_index in zip([0] + sum_indices_initial.tolist(), sum_indices_initial.tolist() + [len(time_values) - 1])]
    x_values_by_section_biomineralizated = [(time_values[start_index], time_values[end_index]) for start_index, end_index in zip([0] + sum_indices_biomineralizated.tolist(), sum_indices_biomineralizated.tolist() + [len(time_values) - 1])]

    # Calculate the mean X values for each interval and sort in descending order
    mean_x_values_initial = sorted([(start_x + end_x) / 2 for start_x, end_x in x_values_by_section_initial],
                                   reverse=True)
    mean_x_values_biomineralizated = sorted(
        [(start_x + end_x) / 2 for start_x, end_x in x_values_by_section_biomineralizated], reverse=True)

    # Calculate the sum of each part for 'T2_initial' data using the equation
    sum_initial = np.sum([(2 * i - 1) * r_i ** 2 for i, r_i in enumerate(mean_x_values_initial, start=1)])

    # Calculate the sum of each part for 'T2_biomineralizated' data using the equation
    sum_biomineralizated = np.sum([(2 * i - 1) * r_i ** 2 for i, r_i in enumerate(mean_x_values_biomineralizated, start=1)])


    # Calculate the sum of 'T2_initial' and 'T2_biomineralizated'
    sum_total_initial = np.sum(data['T2_initial'])
    sum_total_biomineralizated = np.sum(data['T2_biomineralized'])


    # Calculate the ratio of the sums
    ratio = sum_total_biomineralizated / sum_total_initial
    # Calculate the permeability change using the formula
    permeability_change = (1 - (sum_total_biomineralizated / sum_total_initial) ** 2 * ratio) * 100
    porosity_change = (1- sum_total_biomineralizated / sum_total_initial) * 100

    # Append values to the lists
    permeability_changes.append(permeability_change)
    porosity_changes.append(porosity_change)

   #print(f"Permeability Change for {sheet_name}: {permeability_change}, Porosity Change: {porosity_change}")
    print(f"{sheet_name}: {(permeability_change)/(porosity_change)}")
# Custom x-axis labels
custom_labels = ['v=0.5mL/min', '1', '2', 'OD=0.2', '0.8', '1.6']

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.35  # Width of the bars
x = np.arange(len(sheet_names))  # x values for the bars

# Plot porosity changes as blue bars
porosity_bars = ax.bar(x - bar_width/2, porosity_changes, bar_width, color='blue', label='$Φ_{R}$-Eq.(11)')

# Plot permeability changes as orange bars
permeability_bars = ax.bar(x + bar_width/2, permeability_changes, bar_width, color='orange', label='$\t{K}$$_{R}$-Eq.(12)')

ax.set_ylabel('Relative Reduction(%)', fontsize=20)
ax.set_xlabel('Experiments', fontsize=20)
ax.set_xticks(x)
ax.set_xticklabels(custom_labels, fontsize=20)  # Use custom x-axis labels
ax.set_yticklabels(ax.get_yticklabels(), fontsize=20)
ax.legend(loc='upper left', fontsize=20, frameon=False)
ax.set_ylim(0, 45)

# Save the figure
plt.savefig("E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/Figure/porosity&permeability.jpg", dpi=1200)

plt.show()