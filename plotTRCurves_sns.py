#%%
import os
import matplotlib.pyplot as plt
import numpy as np
# curr_dir = os.path.dirname(os.path.abspath(__file__))
curr_dir = r"F:\CON_2021_TRANSYS_RollingComfort\data\fromHUNI\to_ESI_220711_adjustAxis"

# get file list
f_list = os.listdir(os.path.join(curr_dir,"TR"))
# f_list = os.listdir(r"Z:\to_LWR\Con_RollingComfort\data\fromHUNI\to_ESI_220711_adjustAxis\csv")

case_list = []
cond_list = []
sens_list = []
for fi in f_list:
    tmplst = fi.split("_")
    if tmplst[0] not in case_list:
        case_list.append(tmplst[0])
    if tmplst[1] not in cond_list:
        cond_list.append(tmplst[1])
    if tmplst[2] not in sens_list:
        sens_list.append(tmplst[4])

# print(case_list, cond_list, sens_list)
case_list = ["1-1", "1-2","2","3","4","5","6","7","8"]
cond_list = ["A1","A2","B1","B2","B3","B4","C1","C2","D1","D2","D3","D4","E1","E2","F1","F2"]
sens_list = ['X51.csv','X52.csv','X53.csv','X54.csv']

# A Condition | LSH head
import pandas as pd
case_list = ["1-1"]
cond_list = ["B1","B2","B3","B4"]
sens_list = ['X51.csv']
plot_list = []
pgwd_list = []
for case in case_list:
    for cond in cond_list:
        for sens in sens_list:
            plot_list.append(case+"_"+cond+"_LPF_TR_"+sens)

df11 = pd.DataFrame()
plt.figure(figsize=(8,4))
plt.axvline(x=0 )  # draw x =0 axes
plt.axhline(y=0 )  # draw y =0 axes
plt.xlabel(r'$time (sec)$',labelpad=15, fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
plt.ylabel(r'$Acceleration (m/s^2)$',labelpad=20, fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
# plt.ylim(ymin=-0.4,ymax=0.4)
# plt.ylim(ymin=-5.0,ymax=5.0)
# plt.xlim(xmin=0.0,xmax=15.0)
# plt.axis('square')

#%%
import pandas as pd
# crv = os.path.abspath(os.path.join(curr_dir, "csv/"+plot_list[i]))
for i in range(0,len(plot_list)): 
   
    crv = os.path.abspath(os.path.join(curr_dir, "TR/"+plot_list[i]))
    print(crv)
    if os.path.isfile(crv):
        print(crv)
        df1 = pd.read_csv(crv, encoding = 'utf-8')   

        x_vec = df1.Freq.to_numpy()
        print(x_vec.mean)
        y_vec = df1.AccY.to_numpy()
        y_flt = curvesmooth(x_vec,y_vec)

    plt.plot(x_vec, y_flt)
# %%
