import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import train_test_split

from sklearn.metrics import r2_score

import joblib


# LOAD DATASET

data = pd.read_csv(
    'dataset/energy_data.csv'
)

# FEATURES

X = data[[

    'Power',
    'Hours'
]]

# TARGET

y = data['Units']

# SPLIT

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42
)

# MODEL

model = RandomForestRegressor(

    n_estimators=200,

    random_state=42
)

# TRAIN

model.fit(

    X_train,
    y_train
)

# PREDICT

predictions = model.predict(
    X_test
)

# ACCURACY

score = r2_score(
    y_test,
    predictions
)

print(
    "Model Accuracy:",
    round(score, 4)
)

# SAVE MODEL

joblib.dump(
    model,
    'model.pkl'
)

print("Model Trained Successfully")