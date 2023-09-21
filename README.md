# WeatherAPI_GPX_Project

Context:

Each year, I go on a bicycle tour often repeating the same routes. I often want certain information for planning my effort levels and timing. Usually, all I care about is the wind and when sunset is because I have to get to my destination regardless of rain. This program takes GPX data from my longest bicycle rides and extracts GPS data from them at the top of each hour. This information is then passed into Apple Weather Kit to retrieve current wind speed, wind direction, and sunset times for each latitude and longitude pair. A webpage with location markers and weather information is generated. 


Features:
GPX Data Integration: Extracts GPS data from my longest bicycle rides at hourly intervals.

Real-time Weather Info: Utilizes Apple's Weather Kit to fetch current wind speed, wind direction, and sunset times for each latitude and longitude pair extracted from the GPX data. 

Mapping: Visualizes data points on a map with important weather data available as tooltips for each point. Wind direction in degrees is converted to compass points. 

Usage:
Prepare GPX data from Strava, name them in the format Morning_RideMM.DD.YY.gpx or Afternoon_RideMM.DD.YY.gpx.
Run the program using the date for which you want to fetch weather details as an argument.
The program will save a map with tooltips providing wind speed, wind direction, and sunset time for each point.

Prerequisites:
Python (Version: 3.11.4 recommended).
Packages: folium, gpxpy, weatherkit, datetime, argparse, os.
An Apple Weather Kit API key and the associated service details.
