#coding: utf-8
import requests, time
#from tenacity import retry, wait_exponential

# See http://dev.hsl.fi/graphql/console/ for the HSL transit data browser

transit_url = 'http://api.digitransit.fi/routing/v1/routers/hsl/index/graphql'

def get_html():
  departures_html = 'Tietoja ei saatavilla'
  try:
    departures = get_departures()
    departures_html = '<table class="bright"><th>Pysäkiltä</th><th>&nbsp;&nbsp;</th><th>Linja</th><th>&nbsp;&nbsp;</th><th>Perillä</th>'
    for (departure_time, bus_number, arrival_time) in departures:
      #start_time = time.strftime('%H <span class="bold">%M</span>', time.localtime(departure_time))
      start_time = time.strftime('%H:%M', time.localtime(departure_time))
      end_time = time.strftime('%H:%M', time.localtime(arrival_time))
      departures_html += '<tr><td class="bold">' + start_time + '</td><td>&nbsp;&nbsp;</td><td class="align-center">' + bus_number + '</td><td>&nbsp;&nbsp;</td><td class="normal">' + end_time + '</td></tr>'
    departures_html += '</table>'
  except Exception as e: print(e)
  departures_html = '<header>Helsinkiin</header>' + departures_html
  return departures_html

#@retry(wait=wait_exponential(multiplier=0.2, max=2))
def get_departures():
  headers = { 'Content-Type': 'application/graphql' }
  # Next departures from home to Kamppi
  data = """{
  plan(
    from: {lat: 60.137662, lon: 24.656858}
    to: {lat: 60.168992, lon: 24.932366}
    numItineraries: 10
  ) {
    itineraries {
      legs {
        startTime
        endTime
        transitLeg
        route {
          shortName
        }
      }
    }
  }
}"""
  result = requests.post(transit_url, headers=headers, data=data.encode(encoding='UTF-8'))
  
  departures = []
  prev_starting_time = 0
  plan = result.json()['data']['plan']
  for itinerary in plan['itineraries']:
    starting_time = int(itinerary['legs'][0]['startTime'])/1000
    if starting_time > prev_starting_time:
      for leg in itinerary['legs']:
        if leg['transitLeg']:
          departure_time = int(leg['startTime'])/1000
          bus_number = leg['route']['shortName']
          break
      arrival_time = int(itinerary['legs'][-1]['endTime'])/1000
      departures.append((departure_time, bus_number, arrival_time))
      prev_starting_time = starting_time
  return departures[:5]


if __name__ == '__main__':
  pass
