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


def plotCurve(x_vec, y_vec):

    import matplotlib.pyplot as plt

    plt.figure(figsize=(12,4))
    plt.axvline(x=0 )  # draw x =0 axes
    plt.axhline(y=0 )  # draw y =0 axes
    plt.xlabel(r'$time (sec)$',labelpad=15, fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
    plt.ylabel(r'$Location (mm)$',labelpad=20, fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
    # plt.ylim(ymin=-0.4,ymax=0.4)
    # plt.ylim(ymin=-5.0,ymax=5.0)
    # plt.xlim(xmin=0.0,xmax=30.0)
        #         plt.axis('square')
    plt.plot(x_vec, y_vec) 


def AddCulumnForNewNosePos(dataframe):
    df = dataframe
    shoulderCenter = 0.5*(df.shoulderL_x+df.shoulderR_x)
    df["shoulderCenter"] = shoulderCenter
    nose_x2 = df.nose_x-df.shoulderCenter
    df["nose_x2"] = nose_x2
    nose_x2_mean = df["nose_x2"].mean()
    print(nose_x2_mean)
    nose_x3 = df.nose_x2-nose_x2_mean
    df["nose_x3"] = nose_x3
    
    return df


def findFilesList(main_folder, case):
    #[1] main directory
    import os
    # main_folder = r"F:\CON_2021_TRANSYS_RollingComfort\data\fromHUNI\주행시험2차_영상데이터_toESI"
    
    #[2] first sub directory; case names
    sfolders_case = []
    for item in os.listdir(main_folder):
        sub_folder = os.path.join(main_folder, item)
        if os.path.isdir(sub_folder):
            sfolders_case.append(sub_folder)
    # print(os.listdir(main_folder))
    # case = ['1-1', '1-2', '2', '3', '4', '5', '6', '7', '8']
    
    #[3] 2nd, 3rd directories
    s1folder = os.path.join(main_folder, case)
    s2folder = os.path.join(s1folder, "1st_processed")
    s3folder = os.path.join(s2folder, "01_Seg_raw")
    
    # print(s3folder)
    
    #[4] csv file lists
    lst_csv_files = []
    for item in os.listdir(s3folder):
        # print(item)
        val = os.path.join(s3folder, item)
        # print(val)
        if os.path.isdir(val):
            pass
        elif os.path.isfile(val):
            lst_csv_files.append(val)
    # print(lst_csv_files)
    
    #[5] time files
    lst_time_files = []
    for csv in lst_csv_files:
        if "time" in csv:
            lst_time_files.append(csv)
    
    #[6] cond files
    lst_testA_files = []
    lst_testB_files = []
    lst_testC_files = []
    lst_testD_files = []
    lst_testE_files = []
    lst_testF_files = []
    dic_test = {}
    for csv in lst_time_files:
        if "_A" in csv:
            lst_testA_files.append(csv)
        if "_B" in csv:
            lst_testB_files.append(csv)     
        if "_C" in csv:
            lst_testC_files.append(csv)            
        if "_D" in csv:
            lst_testD_files.append(csv)         
        if "_E" in csv:
            lst_testE_files.append(csv)         
        if "_F" in csv:
            lst_testF_files.append(csv)         
    dic_test = {
        "A": lst_testA_files, 
        "B": lst_testB_files,
        "C": lst_testC_files,
        "D": lst_testD_files,
        "E": lst_testE_files,
        "F": lst_testF_files,
        }
    # print(dic_test)
    return dic_test



#%%
from genericpath import isfile
import pandas as pd
_csv = r"F:\CON_2021_TRANSYS_RollingComfort\data\fromHUNI\주행시험2차_영상데이터_toESI\1-1\1st_processed\01_Seg_raw\01_Seg_raw_1-1_B1_POSE_time.csv"
df = pd.read_csv( _csv )


# %% add culumn
# calculate nose position against the shoulder center
dataframe = df
df = AddCulumnForNewNosePos(dataframe)
df


# %% print nose_x3
x_vec = df.time
y_vec = df.nose_x3    
plotCurve(x_vec, y_vec)

# %% plot curves #1

main_folder = r"F:\CON_2021_TRANSYS_RollingComfort\data\fromHUNI\주행시험2차_영상데이터_toESI"
case = ['1-1', '1-2', '2', '3', '4', '5', '6', '7', '8']
dic_test = findFilesList(main_folder, case[0])
# print(dic_test["A"])

df2 = pd.DataFrame()
print(dic_test.keys())
df_nose = pd.DataFrame
for i in range(0, len(case)):
    dic_test = findFilesList(main_folder, case[i])
    for key in dic_test.keys():
        for _csv in dic_test[key]:
            df = pd.read_csv( _csv )
            dataframe = df
            df = AddCulumnForNewNosePos(dataframe)
            x_vec = df.time
            y_vec = df.nose_x3
    
    
            #export csv to new directory
            import os
            odir = r"F:\CON_2021_TRANSYS_RollingComfort\data\fromHUNI\주행시험2차_영상데이터_toESI\new"
            ofile = os.path.join(odir,os.path.basename(_csv))
            df2 = df.filter(items = ["time","nose_x3"])
            df2.to_csv(ofile)

   
            # plotCurve(x_vec, y_vec)



# %%
df2
# %%
