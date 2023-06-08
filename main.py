
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Read the CSV file
data = pd.read_csv('recycle_data_updated_final.csv')

# Get the unique types from the 'Type' column
available_types = data['Type'].unique()

# Define the marker colors for each location type
marker_colors = {
    'E-waste': 'blue',
    'Beverage Container': 'green',
    'Used Oil': 'red',
    'Paper' : 'black',
    'Plastic':'purple'
}

# Filter the data based on the selected type
def filter_data(selected_type):
    filtered_data = data[data['Type'] == selected_type]
    return filtered_data

# Display the map with markers
def display_map(filtered_data, marker_color):
    if filtered_data.empty:
        st.error("No data available for the selected type.")
    else:
        # Create a folium map centered on the first data point
        map = folium.Map(location=[filtered_data['Latitude'].iloc[0], filtered_data['Longitude'].iloc[0]], zoom_start=10)

        # Add markers for each data point with the specified color
        for index, row in filtered_data.iterrows():
            location = [row['Latitude'], row['Longitude']]
            name = row['Recycling Location Name']
            address = row['Address']
            city = row['City']
            popup_text = f"{name}<br>{address}, {city}"
            folium.Marker(location, popup=popup_text, icon=folium.Icon(color=marker_color)).add_to(map)

        # Display the map
        folium_static(map)

# Streamlit app
def main():
    # Title and description
    st.title("Recycling Locations Map")
    
    selected_type = st.selectbox("Select Type", available_types)
    st.write("where do I recycle the ", selected_type,"?")

    # Filter the data based on the selected type
    filtered_data = filter_data(selected_type)

    # Get the marker color for the selected type
    marker_color = marker_colors[selected_type]

    # Display the map with markers
    display_map(filtered_data, marker_color)

if __name__ == '__main__':
    main()
