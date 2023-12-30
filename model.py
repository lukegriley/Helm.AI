import pandas as pd
import numpy as np
import requests
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from processdata import process_api_data, process_api_target

CEJST = pd.read_csv('CEJST.csv')
CVI = pd.read_csv('CVI-pct-allinone.csv')
property_data = pd.read_csv('property-char.csv')  

CEJST = pd.merge(CEJST, property_data, how='left', on='property_id')

features = [
    'Expected agricultural loss rate (Natural Hazards Risk Index)',
    'Expected building loss rate (Natural Hazards Risk Index)',
    'Expected population loss rate (Natural Hazards Risk Index)',
    'Energy burden', 'Housing burden (percent)',
    'Median value ($) of owner-occupied housing units',
    'Proximity to hazardous waste sites (percentile)',
    'Age of property',
    'Material of property'
]

target = 'Baseline.Environment'

imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(CEJST[features])
y = imputer.fit_transform(CVI[[target]])

api_url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&locationid=ZIP:02912&startdate=2023-10-31&enddate=2023-10-31'
headers = {'token': 'OXghkwOAAuldNdePViyWQWKjSRUNKgYK'}
response = requests.get(api_url, headers=headers)
api_data = response.json()

X_api = process_api_data(api_data)
y_api = process_api_target(api_data)
X = np.concatenate((X, X_api), axis=0)
y = np.concatenate((y, y_api), axis=0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GradientBoostingRegressor()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

new_data_imputed = imputer.transform(CEJST[features])

new_predictions = model.predict(new_data_imputed)

print(new_predictions)
