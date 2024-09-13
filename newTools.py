import folium
import pandas as pd
import webbrowser
from folium.plugins import Fullscreen, Search

#
# Create the map centered on the specified coordinates
my_map = folium.Map(location=bridge_coords, zoom_start=13)

# Load the CSV data from Google Sheets into a DataFrame
url2 = "https://docs.google.com/spreadsheets/d/10W-FJz1sNhM7OE7Y9y_A649kz9MBQE9HYdjkNLMWmMw/export?format=csv"
try:
    data_frame = pd.read_csv(url2)
except Exception as e:
    print(f"Error loading data: {e}")

# Extract the necessary data for markers
try:
    latitudes = data_frame['Latitude'].tolist()
    longitudes = data_frame['Longitude'].tolist()
    area_names = data_frame['Area Name'].tolist()
    access_names = data_frame['Access Name'].tolist()
    boat_launch_cond = data_frame['Boat Launch Condition'].tolist()
    access_types = data_frame['Access Type'].tolist()
except KeyError as e:
    print(f"Missing expected column: {e}")

# Define the center of the map
bridge_coords = [49.6923366, -124.9949615]

#######################################################################################################################
# 
# Additional Basemap Layers
#
#######################################################################################################################


# various OSM and other layers
folium.TileLayer('OpenStreetMap').add_to(my_map)             # Default OpenStreetMap layer
#folium.TileLayer('Stamen Terrain').add_to(my_map)            # Stamen Terrain layer
#folium.TileLayer('Stamen Toner').add_to(my_map)              # High-contrast black and white map
#folium.TileLayer('Stamen Watercolor').add_to(my_map)         # Artistic watercolor style
folium.TileLayer('CartoDB positron').add_to(my_map)          # Light, clean basemap
folium.TileLayer('CartoDB dark_matter').add_to(my_map)       # Dark-themed map


# Add ESRI World Imagery layer (high-quality satellite imagery)
esri_world_imagery = folium.TileLayer(
    tiles="https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="ESRI World Imagery",
    name="ESRI World Imagery",
    overlay=False,
    control=True
).add_to(my_map)

# Add the ESRI World Imagery layer to the map
#esri_world_imagery.add_to(my_map)



#######################################################################################################################
# 
# Tools for the map
#
#######################################################################################################################

# Add a zoom to full screen button
Fullscreen().add_to(my_map)

# Add Search Control
#search = Search(layer=my_map, search_label="access_name, Pplaceholder='Search for an access point'")

#  Layer Control Allows users to toggle between different layers on the map (e.g., satellite, street view).
folium.LayerControl().add_to(my_map)


#Measure Control Adds a tool to measure distances and areas directly on the map.
from folium.plugins import MeasureControl
my_map.add_child(MeasureControl())


#Draw Tools Adds drawing tools that allow users to draw shapes (lines, polygons, circles) on the map.
from folium.plugins import Draw
Draw().add_to(my_map)

# Geolocation Control - Adds a button to find and zoom to the user's current location using their device's GPS.
from folium.plugins import LocateControl
LocateControl().add_to(my_map)







# Add markers using zip to iterate through the data
for lat, lon, area_name, access_name, boat_launch_cond, access_type in zip(latitudes, longitudes, area_names, access_names, boat_launch_cond, access_types):
    # Prepare the popup text
    popup_text = f"Area Name: {area_name}"
    
    if pd.notnull(access_name):
        popup_text += f"<br>Access Name: {access_name}"
    if pd.notnull(boat_launch_cond):
        popup_text += f"<br>Boat Launch: {boat_launch_cond}"
    
    # Create a popup
    data_popup = folium.Popup(popup_text, max_width=300)
    
    # Determine marker styling based on access type and boat launch condition
    if pd.notnull(boat_launch_cond):
        # Boat Launches: Use squares, color-coded by condition
        color = 'yellow' if 'paved' in boat_launch_cond.lower() else 'red'
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                html=f"""<div style='background-color: {color}; width: 10px; height: 10px;'></div>"""
            ),
            popup=data_popup
        ).add_to(my_map)
    else:
        # Access Types: use circles, color-coded by access type
        if access_type.lower() == 'walk in':
            folium.CircleMarker(
                location=[lat, lon],
                radius=4,
                color='black',
                weight=2,
                fill=True,
                fill_color='green',
                fill_opacity=0.6,
                opacity=0.7,
                popup=data_popup,
                draggable=False
            ).add_to(my_map)
        elif access_type.lower() == 'drive in':
            folium.CircleMarker(
                location=[lat, lon],
                radius=4,
                color='black',
                weight=2,
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                opacity=0.7,
                popup=data_popup,
                draggable=False
            ).add_to(my_map)

# Create a legend using HTML to describe each marker type
legend_html = '''
     <div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: 180px; height: 130px; 
     background-color: white; 
     border:2px solid grey; 
     z-index:9999; 
     font-size:14px;
     padding: 10px;
     ">
     <b>Legend</b> <br>
     <i class="fa fa-circle" style="color:green"></i>&nbsp; Walk-In Access<br>
     <i class="fa fa-circle" style="color:blue"></i>&nbsp; Drive-In Access<br>
     <div style='width: 10px; height: 10px; background-color: yellow; display: inline-block;'></div>&nbsp; Paved Boat Launch<br>
     <div style='width: 10px; height: 10px; background-color: red; display: inline-block;'></div>&nbsp; Rough Boat Launch
     </div>
     '''

# Add the legend to the map
my_map.get_root().html.add_child(folium.Element(legend_html))

# Create HTML for the title
title_html = '''
     <h3 align="center" style="font-size:20px"><b>Beach Accesses and Boat Launches of Comox Valley and Beyond Map</b></h3>
     '''

# Add the title to the map
my_map.get_root().html.add_child(folium.Element(title_html))

# Save the map to an HTML file and open it
my_map.save('my_map.html')
webbrowser.open('my_map.html')

# Display the map...
my_map
