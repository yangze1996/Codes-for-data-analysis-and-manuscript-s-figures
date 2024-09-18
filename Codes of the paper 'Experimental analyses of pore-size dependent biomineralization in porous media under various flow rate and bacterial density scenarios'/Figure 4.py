import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit

# Load the Excel file
file_path = "E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/原始资料/precipitation.xlsx"
data = pd.read_excel(file_path, sheet_name="Sheet1")

# Extract the columns for x and y axes
mass_Caco3 = data.iloc[:, 2]  # Third column as x-axis
Tot_data = data.iloc[:, 1]    # Second column as left y-axis

# Define the linear function through the origin
def linear_func(x, a):
    return a * x

# Fit the data using curve_fit
popt, _ = curve_fit(linear_func, Tot_data, mass_Caco3)

# Create figure and axes
fig, ax1 = plt.subplots(figsize=(7, 7))

# Scatter plot for each experimental condition with unique markers and legends
marker_styles = ['o', 's', '^', 'D', 'P', '*']
marker_colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan']
scatter_handles = []
scatter_labels = []
Tot_legend = ['Slow Injection Rate (SR)', 'Basic Injection Rate (BR)', 'Fast Injection Rate (FR)',
              'Low Bacterial Density (LD)', 'Basic Bacterial Density (BD)', 'High Bacterial Density (BD)']



for idx, row in data.iterrows():
    marker = marker_styles[idx % len(marker_styles)]
    ax1.errorbar(row[1], row[2],  fmt='none', ecolor=marker_colors[idx], elinewidth=1, capsize=5)
    scatter = ax1.scatter(row[1], row[2], edgecolors=marker_colors[idx], facecolors='none', marker=marker, s=100)
    scatter_handles.append(scatter)
    scatter_labels.append(Tot_legend[idx])

# Define a larger range of x-values to cover the desired range of the plot
x_extended = np.linspace(0, 20000, 100)  # Adjust the range as needed

# Calculate the corresponding y values using the fitted function
y_extended = linear_func(x_extended, popt[0])  # Use popt[0] as the slope

# Plot the extended fitted line
line_extended = ax1.plot(x_extended, y_extended, color='black', linestyle='--', label='Linear Regression')[0]

# Set labels for the axes
ax1.set_xlabel('CaCO$_{3}$ Volume by NMR (A.u.)', fontsize=18)
ax1.set_ylabel('CaCO$_{3}$ Mass by acid-wash (g)', fontsize=18)
ax1.tick_params(axis='y', labelsize=14)
ax1.tick_params(axis='x', labelsize=14)
ax1.set_ylim(0, 4)
ax1.set_xlim(0, 3000)

# Calculate the predicted values using the fitted function
predicted_values = linear_func(Tot_data, *popt)

# Calculate mean and standard deviation of the observed data
mean_observed = np.mean(mass_Caco3)
std_dev_observed = np.std(mass_Caco3)

# Calculate CV
CV = (std_dev_observed / mean_observed) * 100

# Calculate R-squared
residuals = mass_Caco3 - predicted_values
error = np.std(residuals)
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((mass_Caco3 - np.mean(mass_Caco3)) ** 2)
R_squared = 1 - (ss_res / ss_tot)
se = np.std(residuals) / np.sqrt(len(mass_Caco3))
normalized_se_mean = se / mean_observed
# Residual standard error
RSE = np.sqrt(np.sum(residuals**2) / (len(mass_Caco3) - 2))
# Calculate RMSD
RMSD = np.sqrt(np.mean(residuals ** 2))
MSE = np.mean(residuals ** 2)

def prediction_interval(x_extended, residuals, x_data, alpha=0.05):
    n = len(x_data)
    mean_x = np.mean(x_data)
    Sxx = np.sum((x_data - mean_x) ** 2)
    
    # t-distribution critical value
    t_value = stats.t.ppf(1 - alpha / 2, df=n - 2)
    
    # Prediction interval calculation
    interval_p = t_value * np.sqrt(np.mean(residuals ** 2) * (1 + 1/n + ((x_extended - mean_x) ** 2) / Sxx))
    
    return interval_p

# Calculate intervals for the extended x-values
# pred_interval_extended_c = confidence_interval(x_extended, residuals, Tot_data, alpha=0.05)
pred_interval_extended_p = prediction_interval(x_extended, residuals, Tot_data, alpha=0.05)
print(pred_interval_extended_p)
# # Plot the confidence interval as a shaded area
# interval_confidence = ax1.fill_between(x_extended, y_extended - pred_interval_extended_c, 
#                  y_extended + pred_interval_extended_c, color='green', alpha=0.2, label='95% Confidence Interval')

# Plot the prediction interval as a shaded area
interval_prediction = ax1.fill_between(x_extended, y_extended - pred_interval_extended_p, 
                 y_extended + pred_interval_extended_p, color='blue', alpha=0.2, label='95% Prediction Interval')


# Display the results
print(f"CV: {CV:.2f}%")
print(f"R-squared: {R_squared:.4f}")
print(f"RMSD: {RMSD:.4f}")
print(f"std_dev_observed: {std_dev_observed:.4f}")
print(f"se: {se:.4f}")
print(f"RSE: {RSE:.4f}")
print(f"error: {error:.4f}")
print(f"normalized_se_mean: {normalized_se_mean:.4f}")
# Create legend including the proportional fit line
ax1.legend(scatter_handles + [line_extended] +  [interval_prediction],  # Fixed the legend variable name
           scatter_labels + [f'Linear regression'] + [f'95% Prediction Interval'],  # Fixed the legend label
           loc='upper left', bbox_to_anchor=(0.002, 0.998), ncol=1, fontsize=12,frameon=False)

# Save and show the plot
plt.tight_layout()
plt.savefig("E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/Figure/5-precipitation.jpg", dpi=120)
plt.show()
