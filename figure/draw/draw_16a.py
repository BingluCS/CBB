import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data_no, data_com = [], []
for i in range(12):
    data_no.append( pd.read_csv(f'../test2/cbb/nyx/cpu_utilization-{i+1}.txt', header=None))
for index in range(1,12):
   data_no[0][:3150] = data_no[0][:3150]+data_no[index][:3150]

data_no_sums = (data_no[0].iloc[:3150].sum(axis=1))
cpu_no = data_no_sums[:1900].mean()/48


data_no_sums = data_no_sums.groupby(data_no_sums.index //5).mean()/48

x_no = np.arange(0,221,0.5)

for i in range(12):
    data_com.append( pd.read_csv(f'../test2/com/nyx/cpu_utilization-{i+1}.txt', header=None))
for index in range(1,12):
   data_com[0][:3150] = data_com[0][:3150]+data_com[index][:3150]
data_com_sums = (data_com[0].iloc[:3150].sum(axis=1))
cpu_com = data_com_sums[:3150].mean()/48
# print(cpu_com)
data_com_sums = data_com_sums.groupby(data_com_sums.index // 5).mean()/48

x_com = np.arange(0,315,0.5)

p1 = plt.plot(x_com, data_com_sums, label='Compression', color="#1d5dec")
p0 = plt.plot(x_com, data_no_sums, label='Baseline', color="red")

a = plt.legend([p0[0]], ['CBB'],bbox_to_anchor=(-0.01, 1.01), borderaxespad=0,frameon=False,loc=3,fontsize=20)
plt.legend([p1[0]], ['Compression'],bbox_to_anchor=(1.01, 1.01), borderaxespad=0,frameon=False,loc=4,fontsize=20)
plt.gca().add_artist(a)


plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Time (Second)', fontsize=20)
plt.ylabel('CPU Utilization (%)', fontsize=20)

plt.savefig("CPU_Nyx", bbox_inches='tight')