To:
sudo nano ~/.config/lxsession/LXDE-pi/autostart

@sudo /usr/local/bin/python3 /home/pi/Documents/app.py

Installs:

- bottle
- bottle-tornadosocket
- (tenacity, monotonic)
- forecastio # https://github.com/ZeevG/python-forecast.io
- pytz

Weather icons:

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
