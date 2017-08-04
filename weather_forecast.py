#coding: utf-8
import os
import pytz
import forecastio # https://github.com/ZeevG/python-forecast.io
from conf_darksky import conf

tz = pytz.timezone('Europe/Helsinki')

icon_mapping = {
  "clear-day": "wi-day-sunny",
  "clear-night": "wi-night-clear",
  "rain": "wi-rain",
  "snow": "wi-snow",
  "sleet": "wi-sleet",
  "wind": "wi-strong-wind",
  "fog": "wi-fog",
  "cloudy": "wi-cloudy",
  "partly-cloudy-day": "wi-day-cloudy",
  "partly-cloudy-night": "wi-night-cloudy"
}

def get_forecast():
  ds = conf['forecastio']
  resp = forecastio.load_forecast(ds['api_key'], ds['latitude'], ds['longitude'])
  return resp

def get_html(temp_now):
  forecast = get_forecast()
  forecast_html = format_forecast(forecast, temp_now)
  return forecast_html

def format_forecast(forecast, temp_now):
  hourly = forecast.hourly()
  daily = forecast.daily()
  html_string = '<header>Sää lähitunteina</header>'
  html_string += '<table class="bright">'
  forecast_html = read_template('hourly_forecast.html')
  html_string += format_forecast_line(forecast_html, hourly.data[0].icon, 'Nyt', str(temp_now))
  for data_point in hourly.data[3:14:3]: # Every three hours
    point_in_time = data_point.time
    point_in_time = point_in_time.replace(tzinfo=pytz.utc).astimezone(tz)
    time_string = point_in_time.strftime('%H:%M')
    temperature = temp_now if temp_now else int(round(data_point.temperature))
    html_string += format_forecast_line(forecast_html, data_point.icon, time_string, str(temperature))
  html_string += '</table><br/>'
  html_string += '<header>Sää lähipäivinä</header>'
  html_string += '<table class="bright">'
  for data_point in daily.data[1:6]: # Every three hours
    point_in_time = data_point.time
    point_in_time = point_in_time.replace(tzinfo=pytz.utc).astimezone(tz)
    time_string = ['Su','Ma','Ti','Ke','To','Pe','La'][int(point_in_time.strftime('%w'))]
    temperature_string = ' <span class="normal small">' + str(int(data_point.temperatureMin)) + '-</span>' + '<span class="bold">' + str(int(data_point.temperatureMax)) + '</span>'
    html_string += format_forecast_line(forecast_html, data_point.icon, time_string, temperature_string)
  html_string += '</table>'
  return html_string
  
def format_forecast_line(forecast_html, icon, time_string, temperature_string):
  icon = icon_mapping.get(icon, 'na')
  return forecast_html % {
          'temperature': temperature_string,
          'time': time_string,
          'icon': icon
  }

def format_calendar(daily, calendar_events):
  html_string = ''
  calendar_day_html = read_template('calendar_day.html')
  for data_point in daily.data[:7]: # For a week
    point_in_time = data_point.time
    point_in_time = point_in_time.replace(tzinfo=pytz.utc).astimezone(tz)
    weekday = ['Su','Ma','Ti','Ke','To','Pe','La'][int(point_in_time.strftime('%w'))]
    month = point_in_time.strftime('%m')
    day = point_in_time.strftime('%d')
    date = point_in_time.strftime('%Y-%m-%d')
    max_temp = int(round(data_point.temperatureMax))
    min_temp = int(round(data_point.temperatureMin))
    icon = data_point.icon
    if icon not in conf['forecastio']['icons']:
      icon = 'na'
    icon = conf['s3'] + icon + '.png'
    events_string = format_events(calendar_events, date)
    html_string = html_string + calendar_day_html % {
            'weekday': weekday,
            'month': month,
            'day': day,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'icon': icon,
            'calendar_entry': events_string
    }
  return html_string

def read_template(filename):
  read_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
  read_string = ''
  if os.path.exists(read_filename):
    with open(read_filename) as file_in:
      read_string = file_in.read()
  return read_string

if __name__ == '__main__':
  pass

