import pickle
import sys
# import sklearn
from sklearn.preprocessing import StandardScaler  
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import numpy as np

# 

#
#Current Directory path
import os
cwd = os.path.dirname(os.path.realpath(__file__))
#


# load the model from disk
model_MCL = pickle.load(open("{}/nn_mcl.sav".format(cwd), 'rb'))
model_ACL = pickle.load(open("{}/nn_acl.sav".format(cwd), 'rb'))
model_PCL = pickle.load(open("{}/nn_pcl.sav".format(cwd), 'rb'))
model_F1 = pickle.load(open("{}/nn_F1.sav".format(cwd), 'rb'))
model_F2 = pickle.load(open("{}/nn_F2.sav".format(cwd), 'rb'))
model_F3 = pickle.load(open("{}/nn_F3.sav".format(cwd), 'rb'))
model_T1 = pickle.load(open("{}/nn_T1.sav".format(cwd), 'rb'))
model_T2 = pickle.load(open("{}/nn_T2.sav".format(cwd), 'rb'))
model_T3 = pickle.load(open("{}/nn_T3.sav".format(cwd), 'rb'))
model_T4 = pickle.load(open("{}/nn_T4.sav".format(cwd), 'rb'))
MCL_bias = model_MCL.intercepts_
ACL_bias = model_ACL.intercepts_
PCL_bias = model_PCL.intercepts_
F1_bias = model_F1.intercepts_
F2_bias = model_F2.intercepts_
F3_bias = model_F3.intercepts_
T1_bias = model_T1.intercepts_
T2_bias = model_T2.intercepts_
T3_bias = model_T3.intercepts_
T4_bias = model_T4.intercepts_

MCL_weight = model_MCL.coefs_
ACL_weight = model_ACL.coefs_
PCL_weight = model_PCL.coefs_
F1_weight = model_F1.coefs_
F2_weight = model_F2.coefs_
F3_weight = model_F3.coefs_
T1_weight = model_T1.coefs_
T2_weight = model_T2.coefs_
T3_weight = model_T3.coefs_
T4_weight = model_T4.coefs_


all_of_L1_bias = np.array([ MCL_bias[0], ACL_bias[0], PCL_bias[0], F1_bias[0], F2_bias[0], F3_bias[0], T1_bias[0], T2_bias[0], T3_bias[0], T4_bias[0] ])
all_of_L2_bias = np.array([ MCL_bias[1], ACL_bias[1], PCL_bias[1], F1_bias[1], F2_bias[1], F3_bias[1], T1_bias[1], T2_bias[1], T3_bias[1], T4_bias[1] ])
all_of_L3_bias = np.array([ MCL_bias[2], ACL_bias[2], PCL_bias[2], F1_bias[2], F2_bias[2], F3_bias[2], T1_bias[2], T2_bias[2], T3_bias[2], T4_bias[2] ])
all_of_L4_bias = np.array([ MCL_bias[3], ACL_bias[3], PCL_bias[3], F1_bias[3], F2_bias[3], F3_bias[3], T1_bias[3], T2_bias[3], T3_bias[3], T4_bias[3] ])

all_of_L1_weight = np.array([ MCL_weight[0], ACL_weight[0], PCL_weight[0], F1_weight[0], F2_weight[0], F3_weight[0], T1_weight[0], T2_weight[0], T3_weight[0], T4_weight[0] ])
all_of_L2_weight = np.array([ MCL_weight[1], ACL_weight[1], PCL_weight[1], F1_weight[1], F2_weight[1], F3_weight[1], T1_weight[1], T2_weight[1], T3_weight[1], T4_weight[1] ])
all_of_L3_weight = np.array([ MCL_weight[2], ACL_weight[2], PCL_weight[2], F1_weight[2], F2_weight[2], F3_weight[2], T1_weight[2], T2_weight[2], T3_weight[2], T4_weight[2] ])
all_of_L4_weight = np.array([ MCL_weight[3], ACL_weight[3], PCL_weight[3], F1_weight[3], F2_weight[3], F3_weight[3], T1_weight[3], T2_weight[3], T3_weight[3], T4_weight[3] ])


np.save("L1_bias.npy",all_of_L1_bias)
np.save("L2_bias.npy",all_of_L2_bias)
np.save("L3_bias.npy",all_of_L3_bias)
np.save("L4_bias.npy",all_of_L4_bias)
np.save("L1_weight.npy",all_of_L1_weight)
np.save("L2_weight.npy",all_of_L2_weight)
np.save("L3_weight.npy",all_of_L3_weight)
np.save("L4_weight.npy",all_of_L4_weight)


