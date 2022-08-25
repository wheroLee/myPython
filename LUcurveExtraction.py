import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# curr_dir = os.path.dirname(os.path.abspath(__file__))
curr_dir = r"F:\CON_2021_TRANSYS_RollingComfort\data\fromTransys"

# get file list
f_list = os.listdir(os.path.join(curr_dir,"Static"))

for i in range(0,len(f_list)):
    _csv = os.path.abspath(os.path.join(curr_dir, "Static/"+f_list[i]))
    print(_csv)
    df = pd.read_csv( _csv )

    _mm        = df.mm.to_numpy()
    _force     = df.N.to_numpy()
    _idxmax_force = df.N.idxmax()

    _F_LCC = df.loc[:_idxmax_force]
    _F_UCC = df.loc[_idxmax_force:]

    _LCC_time = _F_LCC.sec.to_numpy()
    _LCC_mm = _F_LCC.mm.to_numpy()
    _LCC_force = _F_LCC.N.to_numpy()

    _UCC_mm = _F_UCC.mm.to_numpy()
    _UCC_force = _F_UCC.N.to_numpy()

    _LCC_stress = _LCC_force*0.001/(100*100)
    _LCC_strain = _LCC_mm/100

    interval = _F_LCC.sec.idxmax()/16

    static_force = []
    static_stroke = []
    for j in range(0,16):
        min = interval*j
        max = interval*j+interval*0.5
        static_force.append(_F_LCC.loc[min:max].N.min())
        static_stroke.append(_F_LCC.mm[int((min))])

    arr_static_force = np.array(static_force)
    arr_static_stroke = np.array(static_stroke)

    arr_static_force = arr_static_force * 0.001 / (100*100)
    arr_static_stroke = arr_static_stroke / 100

    df_ss = pd.DataFrame([arr_static_stroke, arr_static_force]).transpose()
    df_ss.columns = ['strain','stress']

    _csv2 = os.path.abspath(os.path.join(curr_dir, "Static/ss_"+f_list[i]))
    
    df_ss.to_csv(_csv2)

    print(f"_csv2 exported: {_csv2}")