import requests
from bs4 import BeautifulSoup
import time
import csv

base_url = "https://www.autoscout24.at/lst"

def get_page_data(soup, data_list, make, model):
    for car in soup.find_all('div', class_='ListItem_wrapper__TxHWu'):
        try:
            name = car.find('h2').get_text(strip=True)
        except AttributeError:
            name = "N/A"
        
        try:
            price = car.find('p', class_='Price_price__APlgs').get_text(strip=True)
        except AttributeError:
            price = "N/A"

        try:
            details = car.find('div', class_='VehicleDetailTable_container__XhfV1')
            mileage = details.find('span', {'data-testid': 'VehicleDetails-mileage_road'}).get_text(strip=True)
            transmission = details.find('span', {'data-testid': 'VehicleDetails-transmission'}).get_text(strip=True)
            date = details.find('span', {'data-testid': 'VehicleDetails-calendar'}).get_text(strip=True)
            fuel = details.find('span', {'data-testid': 'VehicleDetails-gas_pump'}).get_text(strip=True)
            power = details.find('span', {'data-testid': 'VehicleDetails-speedometer'}).get_text(strip=True)
        except AttributeError:
            mileage = transmission = date = fuel = power = "N/A"
        
        data_list.append([make, model, name, price, mileage, transmission, date, fuel, power])

def scrape_autoscout24(make, model):
    data_list = [["Make", "Model", "Name", "Price", "Mileage", "Transmission", "Date", "Fuel", "Power"]]
    params = {
        'atype': 'C',
        'page': 1,
        'make': make,
        'model': model,
        'search_id': 'trvgtvky4n',
        'source': 'listpage_pagination'
    }
    while True:
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')

        get_page_data(soup, data_list, make, model)

        next_button = soup.find('button', {'aria-label': 'Zu nächsten Seite'})
        if next_button and 'disabled' not in next_button.attrs.get('class', []):
            print(f"Next button found on page {params['page']}")
            params['page'] += 1
            time.sleep(2)
        else:
            print("No next button found or it is disabled.")
            break
    
    return data_list


all_data = []

for car_model in audi_models:
    data = scrape_autoscout24(car_model['make'], car_model['model'])
    all_data.extend(data)

# Save the data to a CSV file
with open('/content/drive/MyDrive/audi_car_prices.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(all_data)