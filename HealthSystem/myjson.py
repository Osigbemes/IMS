import requests

response = requests.get('https://youngancient.000webhostapp.com/fetch-data-gbemi.php')
print ((response.json()))