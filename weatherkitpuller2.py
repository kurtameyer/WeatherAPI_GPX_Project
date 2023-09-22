import os
import datetime
import argparse
import folium
import gpxpy
from weatherkit.client import WKClient

WK_TEAM = os.environ.get("WK_TEAM")
WK_SERVICE = os.environ.get("WK_SERVICE")
WK_KEYID = os.environ.get("WK_KEYID")
WK_PATHTOKEY = os.environ.get("WK_PATHTOKEY")

client = WKClient(WK_TEAM, WK_SERVICE, WK_KEYID, WK_PATHTOKEY)


def parse_gpx_date(date_string):
    """
    Convert a date string into a datetime.date object, 
    then check for existing GPX files with that date.
    
    :param date_string: String in the format MM.DD.YY.
    :return: Parsed GPX file.
    """
    date_parts = date_string.split('.')
    date_obj = datetime.datetime(int('20' + date_parts[2]), int(date_parts[0]), int(date_parts[1])).date()
    filename_date = date_obj.strftime("%m.%d.%y")
    potential_filenames = [f"Morning_Ride{filename_date}.gpx", f"Afternoon_Ride{filename_date}.gpx"]

    for filename in potential_filenames:
        if os.path.exists(filename):
            return parse_gpx(filename)

    raise FileNotFoundError(f"GPX file for date {date_string} not found.")


def parse_gpx(filename):
    """
    Parse the GPX file.
    
    :param filename: Name of the GPX file to parse.
    :return: Parsed GPX file.
    """
    with open(filename, "r") as gpx_file:
        return gpxpy.parse(gpx_file)


def gpx_extract(gpx):
    """
    Extract hourly points from a GPX file.
    
    :param gpx: Parsed GPX file.
    :return: List of hourly points (latitude, longitude).
    """
    hourly_points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if point.time.minute == 0 and point.time.second == 0:
                    hourly_points.append((point.latitude, point.longitude))
    return hourly_points


def weather_data(latitude, longitude):
    """
    Fetch weather data for a given latitude and longitude.
    
    :param latitude: Latitude of the location.
    :param longitude: Longitude of the location.
    :return: Weather data.
    """
    return client.get_weather(latitude, longitude)


def get_weather_for_points(points):
    """
    Fetch weather data for a list of points.
    
    :param points: List of points (latitude, longitude).
    :return: List of weather data for each point.
    """
    return [weather_data(lat, lon) for lat, lon in points]


def plot_on_map(points, weather_data_list):
    """
    Plot points with weather data on a map using Folium.
    
    :param points: List of points (latitude, longitude).
    :param weather_data_list: List of weather data for each point.
    """
    m = folium.Map(location=points[0], zoom_start=10)

    # for point, weather in zip(points, weather_data_list):
    #     wind_speed = weather['currentWeather']['windSpeed']
    #     wind_direction = weather['currentWeather']['windDirection']
    #     sunset_time = datetime.datetime.strptime(weather['forecastDaily']['days'][0]['sunset'], "%Y-%m-%dT%H:%M:%SZ")
    #     tooltip_info = f"Wind Speed: {wind_speed} m/s\nWind Direction: {wind_direction}°\nSunset: {sunset_time}"
    #     folium.Marker(point, tooltip=tooltip_info).add_to(m)
    for point, weather in zip(points, weather_data_list):
        wind_speed = weather['currentWeather']['windSpeed']
        wind_direction = weather['currentWeather']['windDirection']
        
        # Convert wind direction in degrees to compass direction
        compass_points = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        wind_direction_compass = compass_points[int((wind_direction + 11.25) % 360 / 22.5)]
        
        sunset_time = datetime.datetime.strptime(weather['forecastDaily']['days'][0]['sunset'], "%Y-%m-%dT%H:%M:%SZ")
        tooltip_info = f"Wind Speed: {wind_speed} m/s\nWind Direction: {wind_direction_compass}\nSunset: {sunset_time}"
        folium.Marker(point, tooltip=tooltip_info).add_to(m)
    m.save('map_with_weather.html')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch weather data for GPX files corresponding to a given date.")
    parser.add_argument("date", type=str, help="Date in the format MM.DD.YY.")
    args = parser.parse_args()

    gpx_data = parse_gpx_date(args.date)
    points = gpx_extract(gpx_data)
    weather_data_list = get_weather_for_points(points)
    plot_on_map(points, weather_data_list)
