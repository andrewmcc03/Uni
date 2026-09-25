import datetime
import json
import urllib.request

def url_builder(lat, lon):
    user_api = '2975d8fae93d5fb86bc1e9f0349a3500'  
    unit = 'metric'
    return 'http://api.openweathermap.org/data/2.5/weather' + \
           '?units=' + unit + \
           '&APPID=' + user_api + \
           '&lat=' + str(lat) +  \
           '&lon=' + str(lon)

def fetch_data(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    return json.loads(output)
    
def time_converter(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d %b %I:%M %p')

userInput1 = input("Enter FIRST location to compare (lon, lat): ")
lon1, lat1 = map(float, userInput1.split(','))

userInput2 = input("Enter SECOND location to compare (lon, lat): ")
lon2, lat2 = map(float, userInput2.split(','))


# lon = -5.93491
# lat = 54.6032231

def get_weather_data(lon, lat):
    json_data = fetch_data(url_builder(lat, lon))
    temperature = str(json_data['main']['temp'])
    timestamp = time_converter(json_data['dt'])
    description = json_data['weather'][0]['description']
    location_name = json_data['name']

    return location_name, timestamp, temperature, description

location_name1, timestamp1, temperature1, description1 = get_weather_data(lon1, lat1)
location_name2, timestamp2, temperature2, description2 = get_weather_data(lon2, lat2)

if temperature1 > temperature2:
    print(f"{location_name1} is hotter than {location_name2}.")
elif temperature1 < temperature2:
    print(f"{location_name2} is hotter than {location_name1}.")
else:
    print(f"{location_name1} and {location_name2} have the same temperature.")


# json_data = fetch_data( url_builder(lat, lon) )

# temperature = str( json_data['main']['temp'] )
# timestamp = time_converter( json_data['dt'] )
# description = json_data['weather'][0]['description']
# print("Current weather in " + json_data['name']) # adds location to output
# print(timestamp + " : " + temperature +  " : " + description)