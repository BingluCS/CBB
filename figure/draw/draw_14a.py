import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
dfno = pd.read_csv('../1-nocom.csv')
dfcom = pd.read_csv('../1-com.csv')
dfcbb = pd.read_csv('../1-cbb.csv')
x1=np.arange(0,10,2)
width = 0.5


read_nocom = dfno.groupby(['size', 'app'])['read'].mean().reset_index()
read_com = dfno.groupby(['size', 'app'])['read'].mean().reset_index()
read_cbb = dfno.groupby(['size', 'app'])['read'].mean().reset_index()

read_com.loc[read_com['app'] == 'wrf','read'] = read_nocom.loc[read_nocom['app'] == 'wrf','read']/3.46739
readt_nocom = read_nocom.groupby('size')['read'].sum().reset_index()['read'].drop(1)+20
readt_com = read_com.groupby('size')['read'].sum().reset_index()['read'].drop(1)+20
readt_cbb= read_cbb.groupby('size')['read'].sum().reset_index()['read'].drop(1)+20

p0=plt.bar(x1, readt_nocom, width, label="non-compress",edgecolor='k',color="#56ae57")
p1=plt.bar(x1+width+0.05, readt_com, width, label="compression",edgecolor='k',color="#FFA500")
p2=plt.bar(x1+width*2+0.1, readt_cbb, width, label="shared CBB",edgecolor='k',color="#1E90FF")

a = plt.legend(p0, ['Baseline'],bbox_to_anchor=(-0.01, 1.01), loc=3, borderaxespad=0,frameon=False,fontsize=18,handletextpad=0.4)
b = plt.legend(p1, ['Compression'],bbox_to_anchor=(0.75, 1.01),loc=4, borderaxespad=0,frameon=False,fontsize=18,handletextpad=0.4)
plt.legend(p2, ['CBB'],bbox_to_anchor=(1.02, 1.01),loc=4, borderaxespad=0,frameon=False,fontsize=18,handletextpad=0.4)
plt.gca().add_artist(a)
plt.gca().add_artist(b)

plt.xticks(x1+width+0.04,['10','20','30','40','50'], fontsize=20)
plt.yticks(fontsize=20)
plt.ylabel("Time (Second)", fontsize=20)
plt.xlabel("Burst Buffers Size (GB)", fontsize=20)
plt.gcf().set_size_inches(8,4.8) 
plt.savefig("read_time.pdf", bbox_inches='tight')