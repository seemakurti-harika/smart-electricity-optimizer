import pandas as pd

from sklearn.linear_model import LinearRegression

import joblib


# MONTHLY USAGE DATA

data = {

    'month': [1, 2, 3, 4, 5, 6, 7, 8],

    'units': [120, 135, 150, 170, 190, 220, 240, 265]
}

df = pd.DataFrame(data)

X = df[['month']]

y = df['units']

model = LinearRegression()

model.fit(X, y)

joblib.dump(
    model,
    'ml/energy_forecast.pkl'
)

print("Forecast model trained.")