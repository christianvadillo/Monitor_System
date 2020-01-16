import joblib
import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import StandardScaler
# import pandas as pd

classifier = joblib.load("static/classifier/models/RandomForestClassifier.sav")
print(f"classifier loaded")
sc = joblib.load("static/classifier/models/StandardScaler.sav")


def clasificar_estado(medicion):
    x = []

    for key, value in medicion.items():
        # print(f"key:{key} - value:{value}")
        x.append(value)

    print(np.array(x[1:]).reshape(-1, 16))

    # Transform data
    x = np.array(x[1:]).reshape(-1, 16)
    x = sc.transform(np.array(x))
    x = np.nan_to_num(x)
    print(f"x after sc: {x}")

    y_pred = classifier.predict(x)

    if y_pred != 0:
        return {'estado': "Anormal", 'code': 1}
    else:
        return {'estado': "Normal", 'code': 0}
