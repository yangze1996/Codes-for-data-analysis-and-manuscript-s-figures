import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# File paths
file_path1 = "E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/原始资料/T2 distribution.xlsx"

# Load data
data1 = pd.read_excel(file_path1, sheet_name='SR')

# Create a figure and subplots
fig, ax1 = plt.subplots(figsize=(8, 6))

# Plot T2 distribution data
ax1.plot(data1['T2'], data1['T2_initial'], label="Initial", color="#0059A8")
ax1.plot(data1['T2'], data1['T2_cycle1'], label="Cycle 1", color="#505EB5")
ax1.plot(data1['T2'], data1['T2_cycle2'], label="Cycle 2", color="#7D60BD")
ax1.plot(data1['T2'], data1['T2_cycle3'], label="Cycle 3", color="#A661C0")
ax1.plot(data1['T2'], data1['T2_cycle4'], label="Cycle 4", color="#CB62BF")
ax1.plot(data1['T2'], data1['T2_cycle5'], label="Cycle 5", color="#ED64B8")
ax1.plot(data1['T2'], data1['T2_biomineralized'], label="Biomineralized", color="black")
ax1.axvspan(0.001, 60, facecolor=(160 / 255, 109 / 255, 32 / 255, 0.7), label='Micropores ($\t{T}_{2}$<60 ms)')
ax1.axvspan(60, 300, facecolor=(218 / 255, 160 / 255, 83 / 255, 0.7), label='Mesopores (60 ms<$\t{T}_{2}$<300 ms)')
ax1.axvspan(300, 10000, facecolor=(255 / 255, 215 / 255, 134 / 255, 0.7), label='Macropores ($\t{T}_{2}$>300 ms)')
ax1.set_xlim(0.001, 10000)
ax1.set_xticks([0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000])
ax1.set_xticklabels(['0.001', '0.01', '0.1', '1', '10', '100', '1000', '10000'], fontsize=16)
ax1.set_yticklabels(ax1.get_yticks().astype(int), fontsize=16) 
ax1.text(0.2, 870, 'Experiment: Slow Injection Rate (SR)', fontsize=16, ha='center', zorder=10)
ax1.legend(fontsize=16,  loc='upper left',bbox_to_anchor=(0,0.94))

# Plot T2 distribution data
ax1.set_xscale('log')
ax1.set_xlabel('$\t{T}_{2}$ Relaxation Time (ms)', fontsize=16)
ax1.set_ylabel('NMR Signal Amplitude (A.u.)', fontsize=16)

plt.tight_layout()
plt.savefig("E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/Figure/Total Scan of SR.jpg", dpi=1200)
plt.show()
