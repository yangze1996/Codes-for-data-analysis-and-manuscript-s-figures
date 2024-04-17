import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

file_path = "E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/原始资料/T2 distribution.xlsx"
xls = pd.ExcelFile(file_path)
tit_label = ["(a) Slow Injection Rate (SR)", "(b) Basic Injection Rate (BR)", "(c) Fast Injection Rate (FR)", 
             "(d) Low Bacterial Density (LD)","(e) Basic Bacterial Density (BD)","(f) High Bacterial Density (HD)"]

# 创建一个3行2列的子图布局
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 12))

for index, sheet_name in enumerate(xls.sheet_names):
    data = pd.read_excel(file_path, sheet_name=sheet_name)

    # 计算子图的行和列索引
    col = index // 3
    row = index % 3

    # 在对应的子图中绘制图形
    axes[row, col].plot(data['T2'], data['T2_initial'], label="Initial", color="#0059A8")
    axes[row, col].plot(data['T2'], data['T2_cycle1'], label="Cycle 1", color="#505EB5")
    axes[row, col].plot(data['T2'], data['T2_cycle2'], label="Cycle 2", color="#7D60BD")
    axes[row, col].plot(data['T2'], data['T2_cycle3'], label="Cycle 3", color="#A661C0")
    axes[row, col].plot(data['T2'], data['T2_cycle4'], label="Cycle 4", color="#CB62BF")
    axes[row, col].plot(data['T2'], data['T2_cycle5'], label="Cycle 5", color="#ED64B8")
    axes[row, col].plot(data['T2'], data['T2_biomineralized'], label="Biomineralized", color="black")

    # 设置标题和标签
    axes[row, col].set_xscale('log')
    axes[row, col].set_xlabel('$\t{T}_{2}$ Relaxation Time (ms)',fontsize=16)
    axes[row, col].set_ylabel('Signal Amplitude (A.u.)',fontsize=16)
    axes[row, col].set_title(tit_label[index])

    # 设置坐标轴刻度
    axes[row, col].set_xlim(0.001, 10000)
    axes[row, col].set_xticks([0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000])
    axes[row, col].set_xticklabels(['0.001', '0.01', '0.1', '1', '10', '100', '1000', '10000'])
    axes[row, col].tick_params(axis='x', labelsize=14)
    axes[row, col].tick_params(axis='y', labelsize=14)


    # 添加背景颜色并调整 x 轴范围
    axes[row, col].axvspan(0.001, 60, facecolor=(160/255,109/255,32/255,0.7), label='Micropores ($\t{T}_{2}$<60 ms)')
    axes[row, col].axvspan(60, 300, facecolor=(218/255, 160/255,83/255, 0.7), label='Mesopores (60 ms<$\t{T}_{2}$<300 ms)')
    axes[row, col].axvspan(300, 10000,facecolor=(255/255, 215/255,134/255, 0.7), label='Macropores ($\t{T}_{2}$>300 ms)')

    # 显示图例
    axes[row, col].legend()
# 调整子图之间的间距
plt.tight_layout()

# 保存图形
plt.savefig(
    "E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/Figure/1- T2 distribution.jpg",
    dpi=1200)
# Show the plot (optional)
plt.show()

