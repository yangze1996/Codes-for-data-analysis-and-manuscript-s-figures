import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# 文件路径
file_path = "E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/原始资料/T2 distribution.xlsx"

# 读取Excel文件
xls = pd.ExcelFile(file_path)

# 创建一个图形
fig, ax = plt.subplots(figsize=(8, 6))

# 标题
tit_label = ["(a) Slow Injection Rate", "(b) Basic Injection Rate", "(c) Fast Injection Rate", "(d) Low Bacterial Density", "(e) Basic Bacterial Density", "(f) High Bacterial Density"]

# 遍历表格并绘制图形
for index, sheet_name in enumerate(xls.sheet_names):
    data = pd.read_excel(file_path, sheet_name=sheet_name)

    # 绘制初始T2数据
    ax.plot(data['T2'], data['T2_initial'], label=tit_label[index])

# 设置标题和标签
ax.set_xscale('log')
ax.set_xlabel('$\t{T}_{2}$ Relaxation Time (ms)',fontsize=16)
ax.set_ylabel('Signal Amplitude (A.u.)',fontsize=16)

# 设置坐标轴刻度
ax.set_xlim(0.001, 10000)
ax.set_xticks([0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000])
ax.set_xticklabels(['0.001', '0.01', '0.1', '1', '10', '100', '1000', '10000'])
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)
# 添加背景颜色并调整 x 轴范围
ax.axvspan(0.001, 60, facecolor=(160/255, 109/255, 32/255, 0.7), label='Micropores ($\t{T}_{2}$<60 ms)')
ax.axvspan(60, 300, facecolor=(218/255, 160/255, 83/255, 0.7), label='Mesopores (60ms<$\t{T}_{2}$<300 ms)')
ax.axvspan(300, 10000, facecolor=(255/255, 215/255, 134/255, 0.7), label='Macropores ($\t{T}_{2}$>300 ms)')

# 显示图例
ax.legend(fontsize=16)

# 调整图形布局
plt.tight_layout()

# 保存图形
plt.savefig(
    "E:/河海大学资料/论文/2022.7 基于低场核磁监测不同浓度及注入方式对生物矿化作用的影响/新投稿资料/Figure/1- T2 initial distribution.jpg",
    dpi=1200)

# 显示图形
plt.show()
