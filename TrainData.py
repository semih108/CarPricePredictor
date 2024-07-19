import requests
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import json

# Load Data
data = pd.read_csv('/content/drive/MyDrive/car_data_25k_.csv')
print('Data loaded')
print(data.head())

# Fetch make and model data from JSON
with open('make_model_data.json', 'r') as f:
    make_model_data = json.load(f)
with open('all_model_details.json', 'r') as f:
    all_model_details = json.load(f)

# Function to find make and model in the name
def find_make_model(name, make_model_data):
    for make, models in make_model_data.items():
        for model in models['models']:
            if model.lower() in name.lower():
                return make, model
    return None, None

# Function to find subType in the name
def find_subtype(name, make, model, all_model_details):
    if make in all_model_details and model in all_model_details[make]:
        subtypes = all_model_details[make][model].keys()
        for subtype in subtypes:
            if subtype.lower() in name.lower():
                return subtype
    return None

# Function to clean data
def clean_data(df, make_model_data, all_model_details):
    df['Price'] = df['Price'].str.replace(r'[^\d]', '', regex=True)
    df['Mileage'] = df['Mileage'].str.replace(r'[^\d]', '', regex=True)
    power = df['Power'].str.extract(r'(\d+) kW \((\d+) PS\)')
    df['Power_PS'] = power[1]
    df.drop(columns=['Power'], inplace=True)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Mileage'] = pd.to_numeric(df['Mileage'], errors='coerce')
    df['Power_PS'] = pd.to_numeric(df['Power_PS'], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'].apply(lambda x: x if re.match(r'\d{2}/\d{4}', x) else None), format='%m/%Y', errors='coerce')

    # Extract brand and model details using the API data
    df[['Brand', 'Model']] = df['Name'].apply(lambda x: pd.Series(find_make_model(x, make_model_data)))
    
    # If make and model are not found, use the first and second words in 'Name'
    df['Brand'].fillna(df['Name'].apply(lambda x: x.split()[0]), inplace=True)
    df['Model'].fillna(df['Name'].apply(lambda x: x.split()[1] if len(x.split()) > 1 else ''), inplace=True)
    
    # Extract subType using the API data
    df['subType'] = df.apply(lambda x: find_subtype(x['Name'], x['Brand'], x['Model'], all_model_details), axis=1)
    
    # Extract additional features
    df['Model_Detail'] = df['Name'].apply(lambda x: re.sub(r'^[^\s]+\s[^\s]+\s', '', x))
    df[['Engine_Size', 'Additional_Features']] = df['Model_Detail'].apply(lambda x: pd.Series(x.split(' ', 1) if ' ' in x else [x, '']))

    df.drop(columns=['Model_Detail', 'Additional_Features'], inplace=True)
    return df

data = clean_data(data, make_model_data, all_model_details)
data.dropna(inplace=True)
print('Data after')
print(data.head(20))
# Handle categorical data
le_transmission = LabelEncoder()
le_fuel = LabelEncoder()
le_brand = LabelEncoder()
le_model = LabelEncoder()
le_engine_size = LabelEncoder()
le_subtype = LabelEncoder()

data['Transmission'] = le_transmission.fit_transform(data['Transmission'])
data['Fuel'] = le_fuel.fit_transform(data['Fuel'])
data['Brand'] = le_brand.fit_transform(data['Brand'])
data['Model'] = le_model.fit_transform(data['Model'])
data['Engine_Size'] = le_engine_size.fit_transform(data['Engine_Size'])
data['subType'] = le_subtype.fit_transform(data['subType'].fillna(''))

# Feature Engineering: Calculate car age
data['Car_Age'] = 2024 - data['Date'].dt.year
data.drop(columns=['Date', 'Name'], inplace=True)

print('Data after cleaning')
print(data.head(20))

# Prepare features and target
X = data.drop(columns=['Price'])
y = data['Price']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')

# Save the model and label encoders
joblib.dump(model, '/content/drive/MyDrive/predictionData/car_price_predictor.pkl')
joblib.dump(le_transmission, '/content/drive/MyDrive/predictionData/le_transmission.pkl')
joblib.dump(le_fuel, '/content/drive/MyDrive/predictionData/le_fuel.pkl')
joblib.dump(le_brand, '/content/drive/MyDrive/predictionData/le_brand.pkl')
joblib.dump(le_model, '/content/drive/MyDrive/predictionData/le_model.pkl')
joblib.dump(le_engine_size, '/content/drive/MyDrive/predictionData/le_engine_size.pkl')
joblib.dump(le_subtype, '/content/drive/MyDrive/predictionData/le_subtype.pkl')
