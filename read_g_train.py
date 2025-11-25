from google.transit import gtfs_realtime_pb2
import urllib.request
from datetime import datetime

# MTA real-time data feeds are free and no longer require API keys
feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.request.urlopen('https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g')
feed.ParseFromString(response.read())

print("Trains arriving at Greenpoint Avenue (G22):\n")

for entity in feed.entity:
    if entity.HasField('trip_update'):
        trip = entity.trip_update.trip
        
        for stop in entity.trip_update.stop_time_update:
            # G22N = Northbound, G22S = Southbound
            if stop.stop_id in ['G22N', 'G22S']:
                direction = "Northbound (to Queens)" if stop.stop_id == 'G22N' else "Southbound (to Brooklyn)"
                
                if stop.HasField('arrival'):
                    arrival_time = datetime.fromtimestamp(stop.arrival.time)
                    minutes_away = (arrival_time - datetime.now()).total_seconds() / 60
                    
                    print(f"{direction}")
                    print(f"  Arrives: {arrival_time.strftime('%H:%M:%S')} ({int(minutes_away)} minutes)")
                    print()
                break  # Found Greenpoint, move to next train
