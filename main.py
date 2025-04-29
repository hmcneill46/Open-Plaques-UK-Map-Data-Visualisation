import pandas as pd
import folium
from folium.plugins import MarkerCluster, Search
from folium import IFrame

# Load CSV
csv_file = 'open-plaques-gb-2021-05-14 partial fix.csv'
df = pd.read_csv(csv_file)
df = df.dropna(subset=['latitude', 'longitude'])

colour_mapping = {
    "Belgian Blue Stone": "gray",
    "black": "black",
    "blue": "blue",
    "brass": "orange",
    "bronze": "orange",
    "brown": "beige",
    "brushed metal": "lightgray",
    "claret": "darkred",
    "clear": "white",
    "film cell": "gray",
    "glass": "lightblue",
    "gold": "orange",
    "green": "green",
    "green and red": "darkgreen",
    "grey": "gray",
    "marble": "lightgray",
    "maroon": "darkred",
    "multicoloured": "pink",
    "orange": "orange",
    "pink": "pink",
    "purple": "purple",
    "purple, white and green": "purple",
    "red": "red",
    "red and black": "darkred",
    "slate": "gray",
    "stone": "gray",
    "terracotta": "orange",
    "white": "white",
    "wood": "beige",
    "yellow": "orange",  # No "yellow" icon in Folium
}

fallback_colour = 'cadetblue'

def get_marker_colour(colour_field):
    if pd.isna(colour_field):
        return fallback_colour
    colour_field = colour_field.strip().lower()
    return colour_mapping.get(colour_field, fallback_colour)

# Create map
mean_lat = df['latitude'].mean()
mean_lon = df['longitude'].mean()
m = folium.Map(location=[mean_lat, mean_lon], zoom_start=6, tiles='OpenStreetMap')

marker_cluster = MarkerCluster().add_to(m)

for idx, row in df.iterrows():
    popup_html = f"<h4>{row['title']}</h4>"
    if pd.notna(row['main_photo']):
        popup_html += f'<img src="{row["main_photo"]}" width="300px" style="margin-top:10px;">'
    if pd.notna(row['inscription']):
        popup_html += f"<p><b>Inscription:</b> {row['inscription']}</p>"
    if pd.notna(row['address']):
        popup_html += f"<p><b>Address:</b> {row['address']}</p>"
    if pd.notna(row['area']):
        popup_html += f"<p><b>Area:</b> {row['area']}</p>"
    if pd.notna(row['country']):
        popup_html += f"<p><b>Country:</b> {row['country']}</p>"
    if pd.notna(row['erected']):
        popup_html += f"<p><b>Erected:</b> {int(row['erected'])}</p>"
    
    iframe = IFrame(popup_html, width=350, height=400)
    popup = folium.Popup(iframe, max_width=400)

    marker_colour = get_marker_colour(row['colour'])

    marker = folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup,
        tooltip=row['title'],
        icon=folium.Icon(color=marker_colour, icon='info-sign')
    )

    marker.add_to(marker_cluster)

# Save map
m.save('plaques_map_clustered_clean.html')

print('🎯 New clustered map saved as plaques_map_clustered_clean.html')
