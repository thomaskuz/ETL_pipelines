from pathlib import Path
import requests
import csv

def fetch_weather():
    # Hardcoded API
    base_url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        "latitude": 50.88,
        "longitude": 3.67,
        "hourly": "temperature_2m",
        "timezone": "Europe/Berlin",


    }
    response = requests.get(base_url,params=params, timeout=15)
    response.raise_for_status()
    return response.json() # verandert de HTTP response body in een python dictionary
    # deze dictionary wordt in de volgende functie als payload terug gestuurd

def transform_to_rows(payload):
    times = payload["hourly"]["time"] # payload is hetgeen wat er terug wordt gestuurd op de request
    temps = payload["hourly"]["temperature_2m"] 
    for t, temp in zip(times, temps):
        yield {"time":t, "temperature_2m": temp}

def write_csv(path, rows, header):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def main():
    print("Fetching weather data")
    data = fetch_weather()
    print("transforming data")
    rows = list(transform_to_rows(data))
    output_file = "data/out/weather.csv"
    print(f"Writing {len(rows)} rows to {output_file}...")
    print("DONE")\
    
if __name__ == "__main__":
    main()