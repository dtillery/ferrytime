import datetime
import StringIO
import zipfile
import requests
from google.transit import gtfs_realtime_pb2
import transitfeed

DT_FORMAT = "%b %d, %Y at %I:%M%p"
UPDATE_MSG = "New \"{}\" {} Time at {} (was {})"

def _get_gtfs_feed(url):
    r = requests.get(url)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(r.content)
    return feed

def get_trip_updates():
    return _get_gtfs_feed("http://cnx.ferry.nyc/rtt/public/utility/gtfsrealtime.aspx/tripupdate")

def get_service_alerts():
    return _get_gtfs_feed("http://cnx.ferry.nyc/rtt/public/utility/gtfsrealtime.aspx/alert")

def load_schedule():
    r = requests.get("http://cnx.ferry.nyc/rtt/public/utility/gtfs.aspx")
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    loader = transitfeed.Loader(zip=z)
    return loader.Load()

def _make_stop_time(stop_time):
    # stop time gives you "seconds since midnight"
    midnight = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight + datetime.timedelta(seconds=stop_time.arrival_secs)

def _compare_times(trip, new_time_secs, stop_sequence):
    new_time = datetime.datetime.fromtimestamp(float(new_time_secs))
    stop_time = [st for st in trip.GetStopTimes() if st.stop_sequence == stop_sequence][0]
    old_time = _make_stop_time(stop_time)
    return new_time, old_time, stop_time

def get_updated_arrival_times(trip, stop_time_update):
    if stop_time_update.HasField("arrival"):
        new_time, old_time, stop_time = _compare_times(trip, stop_time_update.arrival.time, stop_time_update.stop_sequence)
        stop_name = stop_time.stop.stop_name

        if new_time > datetime.datetime.now():
            if new_time > old_time:
                print "LATE ARRIVAL FOUND"
            print UPDATE_MSG.format(stop_name, "Arrival", new_time.strftime(DT_FORMAT), old_time.strftime(DT_FORMAT))

def get_update_departure_times(trip, stop_time_update):
    if stop_time_update.HasField("departure"):
        new_time, old_time, stop_time = _compare_times(trip, stop_time_update.departure.time, stop_time_update.stop_sequence)
        stop_name = stop_time.stop.stop_name

        if new_time > datetime.datetime.now():
            if new_time > old_time:
                print "LATE DEPARTURE FOUND"
            print UPDATE_MSG.format(stop_name, "Departure", new_time.strftime(DT_FORMAT), old_time.strftime(DT_FORMAT))


if __name__ == '__main__':

    service_alerts = get_service_alerts()
    if len(service_alerts.entity):
        print "=== SERVICE ALERTS FOUND ==="
        for i, entity in enumerate(service_alerts.entity, start=1):
            alert = entity.alert
            print "=== Alert {}: {}".format(i, alert.header_text.translation[0].text)
            affected_routes = [informed_entity.route_id for informed_entity in alert.informed_entity]
            print "Affected Routes: {}".format(", ".join(affected_routes))
            print "Ends: {}".format(datetime.datetime.fromtimestamp(alert.active_period[0].end).strftime(DT_FORMAT))
            print "Message: {}".format(alert.description_text.translation[0].text)
    print

    schedule = load_schedule()
    for update in get_trip_updates().entity:
        trip_id = update.id
        trip = schedule.GetTrip(trip_id)
        print "Updates for {} - {} ({})".format(trip.route_id, trip.trip_headsign, trip.trip_id)
        for stop_time_update in update.trip_update.stop_time_update:
            # print stop_time_update
            get_updated_arrival_times(trip, stop_time_update)
            get_update_departure_times(trip, stop_time_update)
        print "===\n"
