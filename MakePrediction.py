import numpy as np
import joblib

# Load the model and label encoders
model = joblib.load('/content/drive/MyDrive/predictionData/car_price_predictor.pkl')
le_transmission = joblib.load('/content/drive/MyDrive/predictionData/le_transmission.pkl')
le_fuel = joblib.load('/content/drive/MyDrive/predictionData/le_fuel.pkl')
le_brand = joblib.load('/content/drive/MyDrive/predictionData/le_brand.pkl')
le_model = joblib.load('/content/drive/MyDrive/predictionData/le_model.pkl')
le_subType = joblib.load('/content/drive/MyDrive/predictionData/le_subtype.pkl')
le_engine_size = joblib.load('/content/drive/MyDrive/predictionData/le_engine_size.pkl')

# Function to add unseen labels to encoders
def add_unseen_label(encoder, label):
    if label not in encoder.classes_:
        encoder.classes_ = np.append(encoder.classes_, label)
    return encoder.transform([label])[0]

# Function to predict car price
def predict_car_price(brand, model_name, mileage, transmission, fuel, power_ps, car_age, sub_type, engine_size):
    # Transform categorical inputs
    brand_encoded = add_unseen_label(le_brand, brand)
    model_encoded = add_unseen_label(le_model, model_name)
    transmission_encoded = add_unseen_label(le_transmission, transmission)
    fuel_encoded = add_unseen_label(le_fuel, fuel)
    sub_type_encoded = add_unseen_label(le_subType, sub_type)
    engine_size_encoded = add_unseen_label(le_engine_size, engine_size)

    # Prepare the feature array
    features = np.array([[mileage, transmission_encoded, fuel_encoded, power_ps, brand_encoded, model_encoded, sub_type_encoded, engine_size_encoded, car_age]])

    # Predict the price
    predicted_price = model.predict(features)
    
    return predicted_price[0]

# Example usage
brand = 'Mercedes-Benz'  # example brand
model_name = 'E'  # example model
mileage = 115000  # example mileage
transmission = 'schaltgetriebe'  # example transmission
fuel = 'benzin'  # example fuel
power_ps = 184  # example power in PS
car_age = 13  # example car age
sub_type = 'E200'  # example sub type
engine_size = '200'  # example engine size

predicted_price = predict_car_price(brand, model_name, mileage, transmission, fuel, power_ps, car_age, sub_type, engine_size)
print(f'The predicted price of the car is: € {predicted_price:.2f}')
