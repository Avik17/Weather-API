import aiohttp
import asyncio
import json

url = "https://api.open-meteo.com/v1/forecast"


async def getWeatherinfo(session, city, lat, long):
    params = {
        "latitude": float(lat),
        "longitude": float(long),
        "current": "temperature_2m",
    }
    try:
        async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=5)) as response:
            response.raise_for_status()
            data = await response.json()
            return {"city": city, "data": data}

    except aiohttp.ClientConnectionError:
        return {"city": city, "status": "failed", "reason": "no internet"}
    except asyncio.TimeoutError:
        return {"city": city, "status": "failed", "reason": "timeout"}
    except aiohttp.ClientResponseError as e:
        return {"city": city, "status": "failed", "reason": str(e)}


async def main():
    cities = [
        {"name": "Patna",  "lat": 25.625,  "lon": 85.1356},
        {"name": "Delhi",  "lat": 28.6139, "lon": 77.2090},
        {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    ]

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[getWeatherinfo(session, city["name"], city["lat"], city["lon"]) for city in cities]
        )

    for result in results:
        city = result["city"]
        data = result.get("data", {})
        temp = data.get("current", {}).get("temperature_2m")
        if temp is None:
            print(f"API call failed for {city}: {result.get('reason')}")
            continue
        print(f"Temperature of {city} is: {temp}")
        with open(f"{city}_temp.json", "w") as f:
            json.dump(data, f, indent=2)
            print(f"Saved as {city}_temp.json")


asyncio.run(main())