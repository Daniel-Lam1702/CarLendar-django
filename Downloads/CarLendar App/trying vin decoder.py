import requests

# Define the URL of the Django API endpoint you want to access
url = 'https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/2B3CJ7DJ9BH604233?format=json'  # Replace with your API endpoint URL

# Make a GET request
response = requests.get(url)

# Check the response status code
if response.status_code == 200:
    # Request was successful
    data = response.json() # Parse the response JSON data
    results = data['Results']
    decoded = results[4]['Value'][0] == '0'
    make = results[7]['Value'].capitalize()
    model = results[9]['Value']
    year = int(results[10]['Value'])
    print(decoded)
    print(make)
    print(model)
    print(year)
else:
    # Request failed
    print(f"Request failed with status code: {response.status_code}")
