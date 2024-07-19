import streamlit as st
import leafmap.foliumap as leafmap
import gpxpy
import gpxpy.gpx
import os
import folium

# Set the page configuration
st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
A Streamlit data visualization app by MVRL, WashU.
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "logos/WashU_Logo.jpg"
st.sidebar.image(logo)

# Customize page title
st.title("Geospatial Mobility Data Visualization")

st.markdown(
    """
    An interactive Web App to Visualize Geospatial Data
    """
)

st.markdown(markdown)

# Define the directories containing the .GPX files
gpx_dirs = ["demo"]

# Function to load and parse GPX files
def load_gpx_files(gpx_dir):
    gpx_files = [f for f in os.listdir(gpx_dir) if f.endswith('.gpx')]
    gpx_data = []
    for file in gpx_files:
        try:
            file_path = os.path.join(gpx_dir, file)
            with open(file_path, 'r') as gpx_file:
                gpx = gpxpy.parse(gpx_file)
                for track in gpx.tracks:
                    for segment in track.segments:
                        points = [(point.latitude, point.longitude) for point in segment.points]
                        gpx_data.append(points)
        except Exception as e:
            st.error(f"Error loading {file}: {e}")
    return gpx_data

# Create a map
m = leafmap.Map(minimap_control=True)

# Load GPX data and create FeatureGroups for each directory
for gpx_dir in gpx_dirs:
    gpx_data = load_gpx_files(gpx_dir)
    gpx_layer = folium.FeatureGroup(name=f'GPX Tracks ({gpx_dir})', show=False)
    
    # Add GPX data to the FeatureGroup
    for points in gpx_data:
        if points:  # Ensure there are points to add
            folium.PolyLine(points, popup="GPX Track", color="blue", weight=2.5, opacity=1).add_to(gpx_layer)
    
    # Add the FeatureGroup to the map
    gpx_layer.add_to(m)

# Add the base map
m.add_basemap("OpenTopoMap")

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Display the map in Streamlit
m.to_streamlit(height=500)