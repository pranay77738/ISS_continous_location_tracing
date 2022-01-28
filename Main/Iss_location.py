import datetime
import math
import time
import requests
import plotly.graph_objects as go

latitude_mx = []
longitude_mx = []
Avg_speed = []


def get_json():
    """
    Get Json file from International Space Station.

    Returns
    -------
    json
        Json with keys "iss_position" position of "latitude", "longitude" and
        "timestamp" indicating time and position of ISS.
        :param url:
    """
    url = "http://api.open-notify.org/iss-now.json"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        return RuntimeError("Unable to access Open Notify API")


def get_coordinates(data):
    """
    Get timestamped geo-coordinates of International Space Station.

    Parameters
    ----------
    Json: Json with keys "iss_position" position of "latitude", "longitude" and
        "timestamp" indicating time and position of ISS.

    Returns
    -------
    dict
        Dictionary with keys "latitude", "longitude" and
        "timestamp" indicating time and position of ISS.
        :param data:
    """
    ts_la_lo = {}

    resp = data

    if resp['message'] == "success":
        ts_la_lo["timestamp"] = resp["timestamp"]
        ts_la_lo["latitude"] = float(resp["iss_position"]["latitude"])
        ts_la_lo["longitude"] = float(resp["iss_position"]["longitude"])

    else:
        return RuntimeError("Unable to access Open Notify API")

    return ts_la_lo


def distance_between_coordinate(geoloc1, geoloc2, R=6367):
    """
    Compute distance between geographic coordinate pairs in kilometers.

    Parameters
    ----------
    geoloc1: tuple or list
        (lat1, lon1) of first geolocation.
    geoloc2: tuple or list
        (lat2, lon2) of second geolocation.
    R: float
        Radius of the Earth (est).

    Returns
    -------
    float
        Distance in kilometers between geoloc1 and geoloc2.
    """
    rlat1, rlon1 = [i * math.pi / 180 for i in geoloc1]
    rlat2, rlon2 = [i * math.pi / 180 for i in geoloc2]
    drlat, drlon = (rlat2 - rlat1), (rlon2 - rlon1)

    init = (math.sin(drlat / 2.)) ** 2 + (math.cos(rlat1)) * \
           (math.cos(rlat2)) * (math.sin(drlon / 2.)) ** 2
    return 2.0 * R * math.asin(min(1., math.sqrt(init)))


def get_avg_speed(dloc1, dloc2):
    """
    Compute speed of ISS relative to Earth's surface using
    a pair of coordinates.

    Parameters
    ----------
    dloc1: dict
        Dictionary with keys "latitude", "longitude" "timestamp"
        associated with the first position.
    dloc2: dict
        Dictionary with keys "latitude", "longitude" "timestamp"
        associated with the second position.

    Returns
    -------
    float
        Average speed of the International Space Station relative to the Earth.
    """
    ts1 = datetime.datetime.fromtimestamp(dloc1['timestamp'])
    ts2 = datetime.datetime.fromtimestamp(dloc2['timestamp'])
    secs = abs((ts2 - ts1).total_seconds())
    loc1 = (dloc1["latitude"], dloc1["longitude"])
    loc2 = (dloc2["latitude"], dloc2["longitude"])
    dist = distance_between_coordinate(geoloc1=loc1, geoloc2=loc2)
    vinit = (dist / secs)  # kilometers per second
    return vinit * 3600


def plot_trajectory(dloc1, dloc2):
    """
    Plot the trajectory on map for every given interval.

    Parameters
    ----------
    dloc1: dict
        Dictionary with keys "latitude", "longitude" "timestamp"
        associated.
    dloc2: dict
        Dictionary with keys "latitude", "longitude" "timestamp"
        associated.
    """
    latitude_mx.append(float(dloc1["latitude"]))
    longitude_mx.append(float(dloc1["longitude"]))

    latitude_mx.append(float(dloc2["latitude"]))
    longitude_mx.append(float(dloc2["longitude"]))

    fig = go.Figure(go.Scattergeo(
        lon=latitude_mx,
        lat=longitude_mx,
        text=Avg_speed,
        marker={'size': 4}))
    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'style': "stamen-terrain",
            'zoom': 1})

    fig.show()


ts_init = datetime.datetime.now().strftime("%c")
print(f"[{ts_init}] Retrieving ISS geographic coordinate...")
while True:
    dpos1 = get_coordinates(get_json())
    time.sleep(15)
    dpos2 = get_coordinates(get_json())
    speed = get_avg_speed(dloc1=dpos1, dloc2=dpos2)
    Avg_speed.append("speed=" + str(f"{speed:.2f}"))
    plot_trajectory(dloc1=dpos1, dloc2=dpos2)
    ts_final = datetime.datetime.now().strftime("%c")
    print(f"[{ts_final}] ISS speed relative to Earth's surface: {speed:.2f}km/h")
