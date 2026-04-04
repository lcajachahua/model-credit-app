import requests


# API URL
url = "http://127.0.0.1:8000/predict"


# Data to be sent in the POST request
data = {
    "LIMIT_BAL": 20000, "SEX": 2, "AGE": 24, 
    "PAY_1": 2, "PAY_2": 2, "PAY_3": -1, "PAY_4": -1, "PAY_5": -2, "PAY_6": -2, 
    "BILL_AMT1": 3913, "BILL_AMT2": 3102, "BILL_AMT3": 689, "BILL_AMT4": 0, "BILL_AMT5": 0, "BILL_AMT6": 0, 
    "PAY_AMT1": 0, "PAY_AMT2": 689, "PAY_AMT3": 0, "PAY_AMT4": 0, "PAY_AMT5": 0, "PAY_AMT6": 0
}


# Make the POST request
response = requests.post(url, json=data)


# Print the response from the server
if response.status_code == 200:
    print("Prediction:", response.json())
else:
    print(f"Failed to get response, status code: {response.status_code}")
