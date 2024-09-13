import folium
from folium.plugins import MarkerCluster
import pandas as pd

#Define coordinates of where we want to center our map
home_coords = [49.685, -125.0122]

#Create the map
my_map = folium.Map(location = home_coords, zoom_start = 13)

#Display the map
my_map

#Define the coordinates we want our markers to be at
bridge_coords = [49.6923366, -125.99449615]
#East_Campus_coords = [40.013501, -105.251889]
#SEEC_coords = [40.009837, -105.241905]

#Add markers to the map
folium.Marker(bridge_coords, popup = 'CU Boulder').add_to(my_map)
#folium.Marker(East_Campus_coords, popup = 'East Campus').add_to(my_map)
#folium.Marker(SEEC_coords, popup = 'SEEC Building').add_to(my_map)

#Display the map
my_map