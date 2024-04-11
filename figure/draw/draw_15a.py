import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import  make_interp_spline
from matplotlib.ticker import PercentFormatter

with open('../test3/ratio0', 'r') as file:
    data = file.read()

# 将数据拆分成块
matches = re.findall(r': (\d+\.?\d*)', data)
bb_sizes, baseline, gzip1, gzip3, cbb = [], [], [], [], []
if matches:
    for i in range(0, len(matches), 17):
        bb_sizes.append(int(matches[i]))
        baseline.append(float(matches[i+4]))
        gzip1.append(float(matches[i+8]))
        gzip3.append(float(matches[i+12]))
        cbb.append(float(matches[i+16]))
baseline_hr, gzip1_hr, gzip3_hr, cbb_hr = [], [], [], []
epoch = len(cbb)/6

for i in range(6):
    baseline_hr.append((baseline[i] + baseline[i+6] + baseline[i+12]) / 3)
    gzip1_hr.append((gzip1[i] + gzip1[i+6] + gzip1[i+12]) / 3)
    gzip3_hr.append((gzip3[i] + gzip3[i+6] + gzip3[i+12]) / 3)
    cbb_hr.append((cbb[i] + cbb[i+6] + cbb[i+12]) / 3)

x = [5, 10, 15, 20, 25, 30]
# ori = mn(xs)
# zip4 = mc(xs)
# cbb = mb(xs)

p3 = plt.plot(x, gzip3_hr, label='Local BB', linewidth=3, marker='*', markersize=8, color="#9467bd")
p0 = plt.plot(x, baseline_hr, label='Baseline', linewidth=3, marker='o', markersize=8, color="#56ae57")
p1 = plt.plot(x, gzip1_hr, label='Compression', linewidth=3, marker='v', markersize=9, color="#FFA500")
p2 = plt.plot(x, cbb_hr, label='CBB', linewidth=3, marker='^', markersize=8, color="#1E90FF")
# plt.plot(xn, yn)
# plt.plot(xn, yc)
# # 添加标题和标签
a = plt.legend([p0[0],p1[0]], ['Baseline','Gzip 1'],bbox_to_anchor=(-0.01, 1.01), borderaxespad=0,frameon=False,loc=3,fontsize=16)
plt.legend([p2[0],p3[0]], ['CBB','Gzip 3'],bbox_to_anchor=(1.0, 1.01),borderaxespad=0,frameon=False,loc=4,fontsize=16)
plt.gca().add_artist(a)

#plt.legend(fontsize=12)
plt.xticks(x,fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Burst Buffer Size (GB)', fontsize=20)
plt.ylabel('Cache Hit Rate', fontsize=20)
plt.ylim(0)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.savefig("Cache_hit_ratio", bbox_inches='tight')