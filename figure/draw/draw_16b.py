import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data_cbb, data_com = [], []
for i in range(12):
    data_cbb.append( pd.read_csv(f'../test2/cbb/warpx/cpu_utilization-{i+1}.txt', header=None))
for index in range(1,12):
   data_cbb[0][:1050] = data_cbb[0][:1050]+data_cbb[index][:1050]

data_cbb_sums = (data_cbb[0].iloc[:1050].sum(axis=1))
cpu_cbb = data_cbb_sums[:690].mean()/32
# print(cpu_no)
data_cbb_sums = data_cbb_sums.groupby(data_cbb_sums.index // 5).mean()/32

x_no = np.arange(0,103,0.4)

for i in range(12):
    data_com.append( pd.read_csv(f'../test2/com/warpx/cpu_utilization-{i+1}.txt', header=None))
for index in range(1,12):
   data_com[0][:1050] = data_com[0][:1050]+data_com[index][:1050]
data_com_sums = (data_com[0].iloc[:1050].sum(axis=1))
cpu_com = data_com_sums[:1030].mean()/32
# print(cpu_com)
data_com_sums = data_com_sums.groupby(data_com_sums.index // 5).mean()/32

x_com = np.arange(0,105,0.5)

p1 = plt.plot(x_com, data_com_sums, label='Compression', color="#1d5dec")
p0 = plt.plot(x_com, data_cbb_sums, label='Baseline', color="red")


a = plt.legend([p0[0]], ['CBB'],bbox_to_anchor=(-0.01, 1.01), borderaxespad=0,frameon=False,loc=3,fontsize=20)
plt.legend([p1[0]], ['Compression'],bbox_to_anchor=(1.01, 1.01), borderaxespad=0,frameon=False,loc=4,fontsize=20)
# plt.legend([p2[0],p3[0]], ['Shared CBB','Gzip 3'],bbox_to_anchor=(1.0, 1.01),borderaxespad=0,frameon=False,loc=4,fontsize=16)
plt.gca().add_artist(a)


plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Time (Second)', fontsize=20)
plt.ylabel('CPU Utilization (%)', fontsize=20)

plt.savefig("CPU_WarpX", bbox_inches='tight')