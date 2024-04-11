import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 读取CSV文件
dfno = pd.read_csv('../1-nocom.csv')
dfcom = pd.read_csv('../1-com.csv')
dfcbb = pd.read_csv('../1-cbb.csv')

x1=np.arange(0,10,2)
width = 0.5
flush_nocom = dfno.groupby(['size', 'app'])['flush'].mean().reset_index()
flush_com = dfcom.groupby(['size', 'app'])['flush'].mean().reset_index()
flush_cbb = dfcbb.groupby(['size', 'app'])['flush'].mean().reset_index()


flusht_nocom = flush_nocom.groupby('size')['flush'].sum().reset_index()['flush'].drop(1)
flusht_com = flush_com.groupby('size')['flush'].sum().reset_index()['flush'].drop(1)
flusht_cbb= flush_cbb.groupby('size')['flush'].sum().reset_index()['flush'].drop(1)

p0=plt.bar(x1, flusht_nocom, width, label="non-compress",edgecolor='k',color="#56ae57")
p1=plt.bar(x1+width+0.05, flusht_com, width, label="Compression",edgecolor='k',color="#FFA500")
p2=plt.bar(x1+width*2+0.1, flusht_cbb, width, label="CBB",edgecolor='k',color="#1E90FF")
for i, value in zip(x1,flusht_nocom):
    if value == 0:
        plt.text(i, value + 1, 'x', ha='center', va='bottom',fontsize=20,)  # 标记值为 0 的柱子，设置为红
for i, value in zip(x1+width*2+0.1,flusht_com):
    if value == 0:
        plt.text(i, value + 1, 'x', ha='center', va='bottom',fontsize=20,)  # 标记值为 0 的柱子，设置为红色
for i, value in zip(x1+width+0.05,flusht_cbb):
    if value == 0:
        plt.text(i, value + 1, 'x', ha='center', va='bottom',fontsize=20,)  # 标记值为 0 的柱子，设置为红色

a = plt.legend(p0, ['Baseline'],bbox_to_anchor=(-0.01, 1.01), loc=3, borderaxespad=0,frameon=False,fontsize=18,handletextpad=0.4)
b = plt.legend(p1, ['Compression'],bbox_to_anchor=(0.75, 1.01),loc=4, borderaxespad=0,frameon=False,fontsize=18,handletextpad=0.4)
plt.legend(p2, ['CBB'],bbox_to_anchor=(1.02, 1.01),loc=4, borderaxespad=0,frameon=False,fontsize=18,handletextpad=0.4)
plt.gca().add_artist(a)
plt.gca().add_artist(b)
plt.gcf().set_size_inches(8,4.8) 
plt.xticks(x1+width+0.04,['10','20','30','40','50'], fontsize=20)
plt.yticks(fontsize=20)
plt.ylabel("Time (Second)", fontsize=20)
plt.xlabel("Burst Buffers Size (GB)", fontsize=20)
plt.savefig("flush_time.pdf", bbox_inches='tight')