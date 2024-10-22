# Car Price Predictor

![Car Price Predictor Logo](https://github.com/user-attachments/assets/b35c5b9c-73af-4188-b740-b71df0f40c18)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit%20Learn-green)](https://scikit-learn.org/)
[![API](https://img.shields.io/badge/API-Google%20Cloud-lightgrey)](https://cloud.google.com/)

**Car Price Predictor** is an AI-driven project that leverages machine learning models to predict the resale value of cars based on various parameters such as make, model, year, mileage, and more. This tool is designed to assist potential car buyers and sellers in making informed decisions by providing accurate price estimates.

## Key Features:

- 🔍 **Data Scraping**: Collects data from multiple sources, ensuring a comprehensive dataset of car listings from manufacturers like Audi, BMW, Mercedes, Volkswagen, Ford, and more.
- 🧠 **Machine Learning**: Trained on historical data to predict car prices with a focus on popular car makes.
- 🌐 **User Interface**: Interactive HTML forms allow users to input car details and get an instant price prediction.
- 🔗 **API Integration**: The project includes a backend API that processes the car data and returns price estimates.
- ⚙️ **Customization**: The prediction model is customizable to allow users to fine-tune input variables for more accurate predictions.

---

## Technologies Used:

- 🐍 **Python**: For data scraping, model training, and API implementation.
- 🌐 **HTML/CSS/JavaScript**: For creating a user-friendly interface.
- 📓 **Jupyter Notebooks**: For data cleaning, training the model, and generating predictions.
- 📊 **Machine Learning Libraries**: Pandas, Scikit-learn, and TensorFlow for building and training the prediction model.
- ☁️ **Google Cloud**: For hosting the prediction API.

---

## How It Works:

1. Users input the car details via the form (e.g., make, model, year, mileage).
2. The details are sent to the backend API for processing.
3. The machine learning model analyzes the input and provides a price estimate.
4. The result is displayed back to the user with relevant information about car value and potential future depreciation.

---

## Data Sources:
- **Scraped Data**: The dataset includes all car makes available in the code.
- **Trained Model**: Focuses on brands like Audi, Mercedes, BMW, Volkswagen, and Ford.

---

## Example Code

Here’s an example of how you can use the car price prediction model:

```python
from car_price_predictor import predict_price

# Input car details
car_details = {
    "make": "BMW",
    "model": "X5",
    "year": 2017,
    "mileage": 50000
}

# Predict price
price = predict_price(car_details)
print(f"The predicted price for the car is: ${price:.2f}")
