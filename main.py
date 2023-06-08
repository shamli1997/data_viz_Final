
import streamlit as st
import pandas as pd
import pickle
import folium
from streamlit_folium import folium_static

# Read the CSV file
data = pd.read_csv('recycle_data_updated_final.csv')

# Get the unique types from the 'Type' column
available_types = data['Type'].unique()

# Define the marker colors for each location type
marker_colors = {
    'Electronics': 'blue',
    'Metal': 'green',
    'Used Oil': 'red',
    'Paper' : 'black',
    'Plastic':'orange',
    'Glass': 'pink',
    'Household Hazardous Waste (HHW)':'lightred'
}

# Filter the data based on the selected type
def filter_data(selected_type):
    filtered_data = data[data['Type'] == selected_type]
    return filtered_data

# Display the map with markers
def display_map(selected_type, marker_color):

    filtered_data = filter_data(selected_type)

    if filtered_data.empty:
        st.error("No Recycling Centers Found!")

    else:
        # Create a folium map centered on the first data point
        try:
            map = folium.Map(location=[filtered_data['Latitude'].iloc[0], filtered_data['Longitude'].iloc[0]], zoom_start=10)
        except:
            print("Recycling Location Name: ",filtered_data['Recycling Location Name'],filtered_data)
        # Add markers for each data point with the specified color
        for index, row in filtered_data.iterrows():
            location = [row['Latitude'], row['Longitude']]
            name = row['Recycling Location Name']
            address = row['Address']
            city = row['City']
            popup_text = f"{name}<br>{address}, {city}"
            folium.Marker(location, popup=popup_text, icon=folium.Icon(color=marker_color[selected_type])).add_to(map)

        # Display the map
        folium_static(map)

# Streamlit app
def main():
    st.title("CalRecycle Data Vizualisation")

    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    with open('vectors.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
        
    waste = st.text_input("Enter Waste: ")  
    if waste != "":  
    
        text_features = vectorizer.transform([waste])

        # Predict the category
        category = model.predict(text_features)[0]
        st.success(f"Our model predicted this waste to be of type : {category}")

        # Title and description
        st.title("Recycling Locations Map")
        

        display_map(category, marker_colors)

if __name__ == '__main__':
    main()
