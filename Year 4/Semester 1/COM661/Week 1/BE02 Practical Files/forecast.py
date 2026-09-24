import datetime
import json
import urllib.request

def url_builder(lat, lon):
    user_api = '2975d8fae93d5fb86bc1e9f0349a3500'  
    unit = 'metric'  
    return 'http://api.openweathermap.org/data/2.5/forecast' + \
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

lon = -5.93491   
lat = 54.6032231
json_data = fetch_data( url_builder(lat, lon) )

print("Weather forecast for " + json_data['city']['name'])
print(str( json_data['cnt'] ) + " forecast(s) retrieved")
for forecast in json_data['list']:
    timestamp = time_converter( forecast['dt'] )
    temperature = str( forecast['main']['temp'] )
    description = forecast['weather'][0]['description']
    print(timestamp + " : " + temperature +  " : " + description)