 
import requests
import json
import pandas as pd
import io
 
URL = "https://stats.oecd.org/sdmx-json/data/DP_LIVE/.EXCH.TOT.NATUSD.A/OECD?json-lang=en&dimensionAtObservation=allDimensions&startPeriod=2000"
DATA_FILE_NAME = "OECD-Exchange-Rates-Data"
session = requests.Session()
response: requests.Response = session.get(url=URL)
 
if response.status_code >= 200 and response.status_code < 300:
    json_data = json.load(fp=io.BytesIO(response.content))
    with open(file=DATA_FILE_NAME+'.json', mode="w") as file:
        json.dump(obj=json_data, fp=file, indent=4)
 
    observations = json_data['dataSets'][0]['observations']
    locations = [item['name'] for item in json_data['structure']
                 ['dimensions']['observation'][0]['values']]
    time_periods = [item['name'] for item in json_data['structure']
                    ['dimensions']['observation'][5]['values']]
 
    dataFrame = pd.DataFrame(index=locations, columns=time_periods)
 
    for key, value in observations.items():
        location_index = int(key.split(":")[0])
        time_period_index = int(key.split(":")[-1])
        dataFrame.iloc[location_index, time_period_index] = value[0]
 
    dataFrame.to_csv(DATA_FILE_NAME+'.csv', index=True, header=True)
 
 
else:
    print("Failed to fetch data from the OECD website")
 
