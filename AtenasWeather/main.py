#+begin_src python :results output :exports both
import requests
import os
import csv
import pytz
from datetime import datetime

ATENAS_LAT = 37.9795
ATENAS_LONG = 23.7162
API_KEY = "16f7df2e30eff6d81c157efb5989dc4b"
FILE_NAME = "/home/alex_1805/AtenasWeather/clima-atenas-hoy.csv"

COLUMNAS_CSV = [
    "dt", "coord_lon", "coord_lat", "weather_0_id", "weather_0_main", "weather_0_description",
    "weather_0_icon", "base", "main_temp", "main_feels_like", "main_temp_min", "main_temp_max",
    "main_pressure", "main_humidity", "main_sea_level", "main_grnd_level", "visibility",
    "wind_speed", "wind_deg", "wind_gust", "clouds_all", "sys_type", "sys_id", "sys_country",
    "sys_sunrise", "sys_sunset", "timezone", "id", "name", "cod"
]

def getweatherdata(lat, lon, api):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en la solicitud HTTP: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None
        
def escsv(json_response, csv_name):
    with open(csv_name, 'a', newline = '') as csv_file:
        fieldnames = json_response.keys()
        writer = csv.DictWriter(csv_file, fieldnames = COLUMNAS_CSV)
        if csv_file.tell() == 0:
            writer.writeheader()
        writer.writerow({k: json_response.get(k, "") for k in COLUMNAS_CSV})

def formato_csv(original_json):
    result_dict = {}
    for key, value in original_json.items():
        if isinstance(value, dict):
            for key_s, value_s in value.items():
                result_dict[f"{key}_{key_s}"] = value_s
        elif isinstance(value, list):    
            for idn, item in enumerate(value):
                for key_s, value_s in item.items():
                    result_dict[f"{key}_{idn}_{key_s}"] = value_s
        else:
            result_dict[key] = value        
    csv_orden = {'dt' : result_dict.pop('dt')}
    csv_orden.update(result_dict)
    return csv_orden

def main():
    print("---Clima Atenas, Grecia---")
    atenas_wea = getweatherdata(lat = ATENAS_LAT, lon = ATENAS_LONG, api = API_KEY)
    if atenas_wea['cod']!= 404:
        atenas_wea_for = formato_csv(atenas_wea)
        print(atenas_wea)
        print("-----")
        print(atenas_wea_for)
        escsv(json_response = atenas_wea_for, csv_name = FILE_NAME)
    else:
        print("Ciudad no encontrada")

if __name__ == "__main__":
    main()
                    
#+end_src
