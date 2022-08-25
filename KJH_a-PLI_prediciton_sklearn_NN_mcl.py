import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler  
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score

cwd = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(f"{cwd}/0deg_all_data.csv")

input_parameter = df.loc[:,"Lwr_STIF_X":"t_Top"] 

output_list = ["Bottom_displacement","MID_displacement","Top_displacement", "MCL",
        "F1", "F2", "F3", "T1", "T2", "T3", "T4", "ACL", "PCL" ] 

item = output_list[3]

result = df.loc[:,item]
print(f"result columns : {result.name}")

X_train, X_test, y_train, y_test = train_test_split(input_parameter, \
                                result,random_state=1, test_size=0.3)

scaler = StandardScaler()  
scaler.fit(X_train)  
train_data = scaler.transform(X_train)
test_data = scaler.transform(X_test)

node = 64
regressor = MLPRegressor(hidden_layer_sizes=(node,node,node),activation="relu" \
            ,random_state=1, max_iter=2000,early_stopping=False).fit(train_data, y_train)

y_prediction = regressor.predict(test_data)
r2_value = r2_score(y_prediction, y_test)
print("The Score with ", (r2_score(y_prediction, y_test)))
import pickle
filename = "nn_" + item + ".sav"
pickle.dump(regressor, open(filename, 'wb'))
pickle.dump(scaler, open('std_scaler.pkl', 'wb'))

plt.scatter(y_test, y_prediction, alpha=0.3, label="Neural Net")
max_value = max((y_test.max(), (y_prediction.max())))
plt.plot([0, max_value], [0, max_value], "--", label="Perfect model",c="black")
plt.xlim(0,max_value)
plt.ylim(0,max_value)
plt.xlabel("True")
plt.ylabel("Prediction")
plt.legend()
plt.show()
