from flask import Flask, render_template, request, jsonify
import folium
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Set up Google Sheets API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("path_to_credentials.json", scope)  # Replace with the path to your credentials file
client = gspread.authorize(creds)

# Open the Google Sheet (replace the URL with your Google Sheets URL)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/10W-FJz1sNhM7OE7Y9y_A649kz9MBQE9HYdjkNLMWmMw/export?format=csv")  # Replace with your Google Sheet ID

@app.route('/')
def index():
    # Center coordinates for the map
    bridge_coords = [49.6923366, -124.9949615]
    my_map = folium.Map(location=bridge_coords, zoom_start=13)

    # Load data from Google Sheets into a DataFrame
    worksheet = sheet.sheet1
    data = worksheet.get_all_records()
    data_frame = pd.DataFrame(data)

    # Add existing markers from the DataFrame
    for index, row in data_frame.iterrows():
        lat = row['Latitude']
        lng = row['Longitude']
        popup_text = ", ".join([str(item) for item in row[2:].values if item])  # Customize this line based on your sheet columns
        folium.Marker([lat, lng], popup=popup_text).add_to(my_map)

    # Convert the map to HTML
    map_html = my_map._repr_html_()

    return render_template('index.html', map_html=map_html)

@app.route('/add_point', methods=['POST'])
def add_point():
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')
    attributes = data.get('attributes')

    # Split attributes if needed
    attributes_list = attributes.split(',')

    # Prepare the data row to append
    # Assuming your sheet columns are: Latitude, Longitude, Attribute1, Attribute2, etc.
    row = [lat, lng] + attributes_list

    try:
        # Append the data to the Google Sheet
        worksheet = sheet.sheet1
        worksheet.append_row(row)
        return jsonify({'message': 'Point added successfully!'})
    except Exception as e:
        return jsonify({'message': f'An error occurred: {e}'})

if __name__ == '__main__':
    app.run(debug=True)


