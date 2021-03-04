# this is the "app/robo_advisor.py" file

import requests
import json

# INFO INPUTS

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
response = requests.get(request_url)
print(type(response)) #requests.models.Response
print(response.status_code) #200
print(response.text)


quit()


# INFO OUTPUTS 


