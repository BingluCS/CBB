import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import  make_interp_spline
# 读取CSV文件
dfno = pd.read_csv('../1-nocom.csv')
dfcom = pd.read_csv('../1-com.csv')
dfcbb = pd.read_csv('../1-cbb.csv')

ratio = [2.99495,13.780339,7.5352]
result_nocom = dfno.drop_duplicates(subset=['num','size'], keep='first')
nocom_avg = result_nocom.groupby('size')['all'].mean().reset_index()

result_com = dfcom.drop_duplicates(subset=['num', 'size'], keep='first')
com_avg = result_com.groupby('size')['all'].mean().reset_index()

result_cbb = dfcbb.drop_duplicates(subset=['num', 'size'], keep='first')
cbb_avg = result_cbb.groupby('size')['all'].mean().reset_index()


decomp = dfcbb.groupby(['size', 'app'])['read'].mean().reset_index()
comp = dfcbb.groupby(['size', 'app'])['write'].mean().reset_index()

read_nocom = dfno.groupby(['size', 'app'])['read'].mean().reset_index()
write_nocom = dfno.groupby(['size', 'app'])['write'].mean().reset_index()

decomp.loc[decomp['app'] == 'wrf','read']  = decomp.loc[decomp['app'] == 'wrf','read'] - read_nocom.loc[read_nocom['app'] == 'wrf','read']/3.46739

comp.loc[comp['app'] == 'wrf','write']  = comp.loc[comp['app'] == 'wrf','write'] - write_nocom.loc[write_nocom['app'] == 'wrf','write']/ratio[0]
comp.loc[comp['app'] == 'nyx','write']  = comp.loc[comp['app'] == 'nyx','write'] - write_nocom.loc[write_nocom['app'] == 'nyx','write']/ratio[1]
comp.loc[comp['app'] == 'warpx','write']  = comp.loc[comp['app'] == 'warpx','write'] - write_nocom.loc[write_nocom['app'] == 'warpx','write']/ratio[2]
decomp = decomp.groupby(['size'])['read'].sum().reset_index()
comp = comp.groupby(['size'])['write'].sum().reset_index()

xn = [10,15,20,30,40,50]
yn = nocom_avg['all']

xc = [10,15,20,30,40,50]
yc = com_avg['all']

xb = [10,15,20,30,40,50]
yb = cbb_avg['all']
ylb = yb - comp['write'] - decomp['read']

mn = make_interp_spline(xn, yn)
mc = make_interp_spline(xc, yc)
mb = make_interp_spline(xb, yb)
mlb = make_interp_spline(xc, ylb)

xs = np.arange(10,55,5)

yyn = mn(xs)
yyc = mc(xs)
yyb = mb(xs)
yylb = mlb(xs)


p0 = plt.plot(xs, yyn, label='Baseline', linewidth=3, marker='o', markersize=8, color="#56ae57")
p1 = plt.plot(xs, yyc, label='Compression', linewidth=3, marker='v', markersize=9, color="#FFA500")
p2 = plt.plot(xs, yyb, label='Shared BB', linewidth=3, marker='^', markersize=8, color="#1E90FF")
p3 = plt.plot(xs, yylb, label='Local BB', linewidth=3, marker='*', markersize=8, color="red", linestyle='--', dashes=(2.5, 3))
# # plt.plot(xn, yn)
# # plt.plot(xn, yc)
a = plt.legend([p0[0],p1[0]], ['Baseline','Compression'],bbox_to_anchor=(-0.01, 1.01), borderaxespad=0,frameon=False,loc=3,fontsize=16)
plt.legend([p2[0],p3[0]], ['Shared CBB','Local CBB'],bbox_to_anchor=(1.0, 1.01),borderaxespad=0,frameon=False,loc=4,fontsize=16)
plt.gca().add_artist(a)

#plt.legend(fontsize=12)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlabel('Burst Buffer Size (GB)', fontsize=20)
plt.ylabel('Time (Second)', fontsize=20)
plt.ylim(0)

plt.gcf().set_size_inches(8,4.8) 
plt.savefig("BB_running_time.pdf", bbox_inches='tight')