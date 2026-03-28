import requests
import json
import time

url="https://api.open-meteo.com/v1/forecast"

def getWeatherinfo(city,lat,long):
    params = {
	"latitude": float(lat), 
	"longitude": float(long),
	"current" :"temperature_2m",
    }
    
    try:
        
        response =requests.get(url,params=params,timeout=5)
        response.raise_for_status()
        data=response.json()
        return data

    except requests.exceptions.ConnectionError:
        return {"city": city, "status": "failed", "reason": "no internet"}
    except requests.exceptions.Timeout:
        return {"city": city, "status": "failed", "reason": "timeout"}
    except requests.exceptions.HTTPError as e:
        return {"city": city, "status": "failed", "reason": str(e)}

cities = [
    {"name": "Patna",  "lat": 25.625, "lon": 85.1356},
    {"name": "Delhi",  "lat": 28.6139, "lon": 77.2090},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
]
start=time.time()
for city in cities:
    
    data=getWeatherinfo(city['name'],city['lat'],city['lon'])
    temp=data.get('current',{}).get('temperature_2m')
    if temp is None:
        print(f"API Call failed for {city['name']}")
        continue
    print(f"Temperature of {city['name']} is:{temp} ")
    with open(f"{city['name']}_temp.json","w") as f:
            json.dump(data,f,indent=2)
            print(f"Saved as {city['name']}_temp.json") 
print(f"Time taken: {time.time() - start:.2f}s")  # ← print at the end