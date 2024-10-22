import requests
import json

# Function to fetch all makes data from API
def fetch_all_makes(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    return data

# Function to fetch make and model data from API
def fetch_make_model_data(api_url, makes_data):
    make_model_dict = {}
    for item in makes_data:
        make = item['name']
        model_url = f"{api_url}?make_id={item['id']}"
        model_response = requests.get(model_url)
        model_response.raise_for_status()
        model_data = model_response.json()
        make_model_dict[make] = {'id': item['id'], 'models': [model['name'] for model in model_data]}
    return make_model_dict

# Function to fetch model details from API
def fetch_model_details(make_id, model_name):
    url = f"https://www.ta-autoshop.at/api.php?make_id={make_id}&model_name=%27{model_name}%27"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    parsed_data = json.loads(data['details'])
    model_details = {car.get('subType', 'Unknown'): car for car in parsed_data}
    return model_details

# Fetch all makes data from API
api_url = 'https://www.ta-autoshop.at/api.php'
makes_data = fetch_all_makes(api_url)

# Fetch make and model data from API for all makes
make_model_data = fetch_make_model_data(api_url, makes_data)

# Fetch model details for each make and model
all_model_details = {}
for make, details in make_model_data.items():
    make_id = details['id']
    for model in details['models']:
        try:
            model_details = fetch_model_details(make_id, model)
            if make not in all_model_details:
                all_model_details[make] = {}
            all_model_details[make][model] = model_details
        except Exception as e:
            print(f"Error fetching details for {make} {model}: {e}")

# Save make, model, and model details data to a file
with open('make_model_data.json', 'w') as f:
    json.dump(make_model_data, f)
with open('all_model_details.json', 'w') as f:
    json.dump(all_model_details, f)

print("API data collection complete.")
