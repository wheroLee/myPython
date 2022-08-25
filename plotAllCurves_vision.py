#%%
def AddCulumnForNewNosePos(dataframe):
    df = dataframe
    shoulderCenter = 0.5*(df.shoulderL_x+df.shoulderR_x)
    df["shoulderCenter"] = shoulderCenter
    nose_x2 = df.nose_x-df.shoulderCenter
    df["nose_x2"] = nose_x2
    nose_x2_mean = df["nose_x2"].mean()
    # print(nose_x2_mean)
    nose_x3 = df.nose_x2-nose_x2_mean
    # nose_x3 = df.nose_x2
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
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

main_folder = r"F:\CON_2021_TRANSYS_RollingComfort\data\fromHUNI\주행시험2차_영상데이터_toESI"
case = ['1-1', '1-2', '2', '3', '4', '5', '6', '7', '8']
dic_test = findFilesList(main_folder, case[0])
# print(dic_test["A"])


import matplotlib.pyplot as plt
plt.figure(figsize=(8,4))
plt.axvline(x=0 )  # draw x =0 axes
plt.axhline(y=0 )  # draw y =0 axes
plt.xlabel(r'$time (sec)$',labelpad=15, fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
plt.ylabel(r'$Displacement (mm)$',labelpad=20, fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
# plt.ylim(ymin=-0.4,ymax=0.4)
plt.ylim(ymin=-250.0,ymax=250.0)
# plt.xlim(xmin=0.0,xmax=15.0)
# print(dic_test.keys())

# case = ['1-1', '1-2', '2']
# case = ['3', '4', '5']
# case = ['8']
for i in range(0, len(case)):
    dic_test = findFilesList(main_folder, case[i])
    for key in dic_test.keys():
        # key = "D"
        df = pd.DataFrame()
        for _csv in dic_test[key]:
            print(_csv)
            df = pd.read_csv( _csv )
            dataframe = df
            df = AddCulumnForNewNosePos(dataframe)
            x_vec = df.time
            y_vec = df.nose_x3
            val = df["nose_x3"].describe()
            print(f"<<<   describe   >>> : {val}")
            plt.plot(x_vec, y_vec)
# %%
