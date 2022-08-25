#%%
def curvesmooth(x_vec,y_vec):
    import numpy as np
    import statsmodels.api as sm
    lowess = sm.nonparametric.lowess
    y_flt = lowess(y_vec, x_vec, frac=0.05)[:,1]
    return y_flt


def zerovalues(x_vec, y_vec):
    xval = []
    for i in range(len(y_vec)-1):
        if y_vec[i] * y_vec[i+1] <= 0 :
            delx = (-y_vec[i]*(x_vec[i+1]-x_vec[i]))/(y_vec[i+1]-y_vec[i])
            xval.append(x_vec[i] + delx)
    return xval


def nearest_index(array, value):
    import numpy as np
    abs_val_array = np.abs(array - value)
    smallest_diff_index = abs_val_array.argmin()
    return smallest_diff_index


def get_resampling(_Curve_x,_Curve_y,_sampleNum):
    import numpy as np

    New_x = np.linspace(min(_Curve_x),max(_Curve_x),_sampleNum)
    New_y = np.interp(New_x, _Curve_x, _Curve_y)

    return New_x, New_y


def resampling_point(pointx, pointy,num):
    from scipy.interpolate import InterpolatedUnivariateSpline
    x = pointx
    y = pointy 
    fx = InterpolatedUnivariateSpline(x,y,k=1)
    new_x = np.linspace(min(x),max(x),num) 
#     new_x = np.linspace(0,8.3,num) 
    new_y = fx(new_x)
    return new_y


def get_resampling(pointx, pointy, num):
    import numpy as np
    x = pointx/pointx[-1]
    y = pointy 
#     New_x = np.linspace(min(pointx),max(_Curve_x),num)
    New_x = np.linspace(0,1,num)
    New_y = np.interp(New_x, x, y)
#     New_y = np.interp(New_x, pointx, pointy)    

    return New_x, New_y


def plotTRAy(case_list,cond_list, cycle):
    import matplotlib.pyplot as plt
    import pandas as pd
    # case_list = ["3"]
    # cond_list = ["B1","B2","B3","B4"]
    # cond_list = ["D1","D2","D3","D4"]
    sens_list = ['X01r.csv']
    plot_list = []
    pgwd_list = []
    for case in case_list:
        for cond in cond_list:
            for sens in sens_list:
                plot_list.append(case+"_"+cond+"_"+sens)
    
    df11 = pd.DataFrame()
    plt.figure(figsize=(8,6))
    plt.axvline(x=0 )  # draw x =0 axes
    plt.axhline(y=0 )  # draw y =0 axes
    plt.xlabel(r'$time (sec)$',labelpad=15, fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
    plt.ylabel(r'$Acceleration (m/s^2)$',labelpad=20, fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
    # plt.ylim(ymin=0,ymax=1.0)
    # plt.ylim(ymin=0.0,ymax=14.0)
    # plt.xlim(xmin=0.0,xmax=cycle)
    # plt.axis('square')
    
    import pandas as pd
    # crv = os.path.abspath(os.path.join(curr_dir, "csv/"+plot_list[i]))
    for i in range(0,len(plot_list)): 
       
        crv = os.path.abspath(os.path.join(curr_dir, "csv/"+plot_list[i]))
        # print(crv)
        if os.path.isfile(crv):
            # print(os.path.basename(crv))
            df1 = pd.read_csv(crv, encoding = 'utf-8')   
    
            x_vec = df1.time.to_numpy()
            y_vec = df1.AccY.to_numpy()
            y_flt = curvesmooth(x_vec,y_vec)

            xval = zerovalues(x_vec, y_flt)
    
            for val in xval:
                if cycle == 8.3:
                    vel = "30kph"
                    if 5.0 < float(val) < 9.0:
                        xoff1 = val
                    elif 9.0 <= float(val):
                        xoff2 = val
                        break  
                elif cycle == 5.0:
                    vel = "50kph"
                    if 3 < float(val) < 6:
                        xoff1 = val
                    elif 6.0 <= float(val): 
                        xoff2 = val
                        break  
        x_new = x_vec - xoff1
        # x_new = x_vec - 0.5*(xoff1+xoff2)
        xval = np.array(zerovalues(x_new, y_flt))

        x_value1 = 0.0
        x_value2 = cycle
        num_point = 1000
        x_loc1 = nearest_index(xval, x_value1)
        x_loc2 = nearest_index(xval, x_value2)
        x_loc1 = nearest_index(x_new, xval[x_loc1])
        x_loc2 = nearest_index(x_new, xval[x_loc2])
        
        trim_x = x_new[x_loc1:x_loc2]
        trim_y = y_flt[x_loc1:x_loc2] 

        new_time, new_acc = get_resampling(trim_x, trim_y,num_point)
        df11[f"y_flt{i}"]=new_acc
        
        # plt.plot(x_new,y_flt, label=f"{os.path.basename(crv)}")
        # plt.plot(trim_x,trim_y, label=f"{os.path.basename(crv)}")
        plt.plot(new_time*x_value2,new_acc, color='gainsboro', label=f"{os.path.basename(crv)}")

    plt.legend() 
    mean_y = df11.mean(axis=1)    
    plt.plot(new_time*x_value2,mean_y, 'black', label=f"mean")  
    plt.legend()   
    #export mean curve
    crv2 = os.path.abspath(os.path.join(curr_dir, "csv_mean/"+"head_"+str(case_list[0])+"_"+vel+"_mean.csv"))
    df11[f"time"]=new_time*cycle
    df11[f"Ay_mean"]=new_acc
    df11.to_csv(crv2)


def plotTROm(case_list,cond_list):
    import matplotlib.pyplot as plt
    import pandas as pd
    # case_list = ["3"]
    # cond_list = ["B1","B2","B3","B4"]
    # cond_list = ["D1","D2","D3","D4"]
    sens_list = ['X01r.csv']
    plot_list = []
    pgwd_list = []
    for case in case_list:
        for cond in cond_list:
            for sens in sens_list:
                plot_list.append(case+"_"+cond+"_LPF_TR_"+sens)
    
    df11 = pd.DataFrame()
    plt.figure(figsize=(8,6))
    plt.axvline(x=0 )  # draw x =0 axes
    plt.axhline(y=0 )  # draw y =0 axes
    plt.xlabel(r'$Freq (Hz)$',labelpad=15, fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
    plt.ylabel(r'$Omega (deg/s)$',labelpad=20, fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
    # plt.ylim(ymin=0,ymax=1.0)
    plt.ylim(ymin=0.0,ymax=60.0)
    plt.xlim(xmin=0.0,xmax=1.0)
    # plt.axis('square')
    
    import pandas as pd
    # crv = os.path.abspath(os.path.join(curr_dir, "csv/"+plot_list[i]))
    for i in range(0,len(plot_list)): 
       
        crv = os.path.abspath(os.path.join(curr_dir, "TR/"+plot_list[i]))
        print(crv)
        if os.path.isfile(crv):
            print(os.path.basename(crv))
            df1 = pd.read_csv(crv, encoding = 'utf-8')   
    
            x_vec = df1.Freq.to_numpy()
            y_vec = df1.OmX.to_numpy()
            y_flt = curvesmooth(x_vec,y_vec)
    
        plt.plot(x_vec, y_flt, label=f"{os.path.basename(crv)}")
    
    plt.legend()  


#%%
import os
import matplotlib.pyplot as plt
import numpy as np
# curr_dir = os.path.dirname(os.path.abspath(__file__))
curr_dir = r"F:\CON_2021_TRANSYS_RollingComfort\data\fromHUNI\to_ESI_220711_adjustAxis"


# get file list
f_list = os.listdir(os.path.join(curr_dir,"csv"))
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
        sens_list.append(tmplst[2])
        
# print(case_list, cond_list, sens_list)
case_list = ["1-1", "1-2","2","3","4","5","6","7","8"]
cond_list = ["A1","A2","B1","B2","B3","B4","C1","C2","D1","D2","D3","D4","E1","E2","F1","F2"]
sens_list = ['X01r.csv','X02r.csv','X03r.csv','X04r.csv','X05r.csv']



# %%
cycle = 8.3
cond_list = ["B1","B2","B3","B4"]
case_list = ["3"]
plotTRAy(case_list,cond_list, cycle)
case_list = ["6"]
plotTRAy(case_list,cond_list, cycle)
case_list = ["4"]
plotTRAy(case_list,cond_list, cycle)
case_list = ["7"]
plotTRAy(case_list,cond_list, cycle)
case_list = ["5"]
plotTRAy(case_list,cond_list, cycle)
case_list = ["8"]
plotTRAy(case_list,cond_list, cycle)

cycle = 5.0
cond_list = ["D1","D2","D3","D4"]
case_list = ["3"]
plotTRAy(case_list,cond_list, cycle)
case_list = ["6"]
plotTRAy(case_list,cond_list, cycle)
case_list = ["4"]
plotTRAy(case_list,cond_list, cycle)
case_list = ["7"]
plotTRAy(case_list,cond_list, cycle)
case_list = ["5"]
plotTRAy(case_list,cond_list, cycle)
case_list = ["8"]
plotTRAy(case_list,cond_list, cycle)
# %%
# cycle = 5.0
# cond_list = ["B1","B2","B3","B4"]
# case_list = ["3"]
# plotTROm(case_list,cond_list, cycle)
# case_list = ["6"]
# plotTROm(case_list,cond_list, cycle)
# case_list = ["4"]
# plotTROm(case_list,cond_list, cycle)
# case_list = ["7"]
# plotTROm(case_list,cond_list, cycle)
# case_list = ["5"]
# plotTROm(case_list,cond_list, cycle)
# case_list = ["8"]
# plotTROm(case_list,cond_list, cycle)
# cond_list = ["D1","D2","D3","D4"]
# case_list = ["3"]
# plotTROm(case_list,cond_list, cycle)
# case_list = ["6"]
# plotTROm(case_list,cond_list, cycle)
# case_list = ["4"]
# plotTROm(case_list,cond_list, cycle)
# case_list = ["7"]
# plotTROm(case_list,cond_list, cycle)
# case_list = ["5"]
# plotTROm(case_list,cond_list, cycle)
# case_list = ["8"]
# plotTROm(case_list,cond_list, cycle)
# %%
