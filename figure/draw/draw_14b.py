import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
dfno = pd.read_csv('../1-nocom.csv')
dfcom = pd.read_csv('../1-com.csv')
dfcbb = pd.read_csv('../1-cbb.csv')
x1=np.arange(0,10,2)
width = 0.5
ratio = [2.99495,13.780339,7.5352]
write_nocom = dfno.groupby(['size', 'app'])['write'].mean().reset_index()
write_com = dfcom.groupby(['size', 'app'])['write'].mean().reset_index()
write_cbb = dfcbb.groupby(['size', 'app'])['write'].mean().reset_index()

write_com.loc[write_com['app'] == 'wrf','write'] = write_nocom.loc[write_nocom['app'] == 'wrf','write']/ratio[0]
write_com.loc[write_com['app'] == 'nyx','write'] = write_nocom.loc[write_nocom['app'] == 'nyx','write']/ratio[1]
write_com.loc[write_com['app'] == 'warpx','write'] = write_nocom.loc[write_nocom['app'] == 'wrpx','write']/ratio[2]
writet_nocom = write_nocom.groupby('size')['write'].sum().reset_index()['write'].drop(1)
writet_com = write_com.groupby('size')['write'].sum().reset_index()['write'].drop(1)
writet_cbb= write_cbb.groupby('size')['write'].sum().reset_index()['write'].drop(1)

p0=plt.bar(x1, writet_nocom, width, label="baseline",edgecolor='k',color="#56ae57")
p1=plt.bar(x1+width+0.05, writet_com, width, label="compression",edgecolor='k',color="#FFA500")
p2=plt.bar(x1+width*2+0.1, writet_cbb, width, label="CBB",edgecolor='k',color="#1E90FF")

a = plt.legend(p0, ['Baseline'],bbox_to_anchor=(-0.01, 1.01), loc=3, borderaxespad=0,frameon=False,fontsize=18,handletextpad=0.4)
b = plt.legend(p1, ['Compression'],bbox_to_anchor=(0.75, 1.01),loc=4, borderaxespad=0,frameon=False,fontsize=18,handletextpad=0.4)
plt.legend(p2, ['CBB'],bbox_to_anchor=(1.02, 1.01),loc=4, borderaxespad=0,frameon=False,fontsize=18,handletextpad=0.4)
plt.gca().add_artist(a)
plt.gca().add_artist(b)


# plt.legend()
plt.xticks(x1+width+0.04,['10','20','30','40','50'], fontsize=20)
plt.yticks(fontsize=20)
plt.ylabel("Time (Second)", fontsize=20)
plt.gcf().set_size_inches(8,4.8) 
plt.xlabel("Burst Buffers Size (GB)", fontsize=20)
plt.savefig("write_time", bbox_inches='tight')