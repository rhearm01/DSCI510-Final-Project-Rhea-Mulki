import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# Function to fetch latitude and longitude for Santa Barbara
def fetch_santa_barbara_coordinates():
    # URL of the API endpoint
    url = "https://www.gps-coordinates.net/api"
    # Identifier for Santa Barbara
    identifier = "santabarbara"
    # Construct the full URL with the identifier
    full_url = f"{url}/{identifier}"
    # Send an HTTP GET request to the API
    response = requests.get(full_url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract latitude and longitude from the response
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        # Return latitude and longitude
        return latitude, longitude
    else:
        # Request was not successful, print an error message
        st.error(f"Failed to fetch coordinates for Santa Barbara. Status code: {response.status_code}")
        return None, None

# Load the datasets
df = pd.read_csv("images.csv")
deployments_df = pd.read_csv("deployments.csv")

# Convert timestamp to datetime with error handling
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows with NaT values
df.dropna(subset=['timestamp'], inplace=True)

# Create a new column to represent the index
df['index'] = df.index

# Sidebar options
st.sidebar.title("Filter Options")
species_name = st.sidebar.text_input("Enter Species Name (optional):")
taxonomy_levels = ['class', 'order', 'family', 'genus', 'species']
taxonomy_filters = {}
for level in taxonomy_levels:
    taxonomy_filters[level] = st.sidebar.multiselect(f"Filter by {level.capitalize()}", df[level].unique())

# Get min and max index values
index_min = df['index'].min()
index_max = df['index'].max()

# Slider for index range
index_range = st.sidebar.slider("Select Index Range:", index_min, index_max, (index_min, index_max))

# Filter the dataset based on user inputs
filtered_df = df.copy()
if species_name:
    filtered_df = filtered_df[filtered_df['species'].str.contains(species_name, case=False)]
for level, values in taxonomy_filters.items():
    if values:
        filtered_df = filtered_df[filtered_df[level].isin(values)]
filtered_df = filtered_df[(filtered_df['index'] >= index_range[0]) & (filtered_df['index'] <= index_range[1])]

# Show the filtered data
st.title("Images Table:")
st.write(filtered_df)

# Display deployments table
st.title("Deployments Table")
st.write(deployments_df)

# Fetch and display latitude and longitude for Santa Barbara
st.subheader("Santa Barbara Coordinates")
latitude, longitude = fetch_santa_barbara_coordinates()
if latitude is not None and longitude is not None:
    st.write(f"Latitude: {latitude}, Longitude: {longitude}")

# Visualizations
st.title("Visualizations")
if not filtered_df.empty:
    # Bar Chart of Species Distribution
    st.subheader("Species Distribution")
    species_counts = filtered_df['species'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=species_counts.index, y=species_counts.values, palette='viridis')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Species")
    plt.ylabel("Count")
    st.pyplot(plt)

    # Histogram of Timestamps
    st.subheader("Timestamp Distribution")
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_df['timestamp'], bins=20, kde=True, color='skyblue')
    plt.xlabel("Timestamp")
    plt.ylabel("Count")
    st.pyplot(plt)

    # Map of Observations using latitude and longitude from deployments.csv
    st.subheader("Map of Observations")
    if 'latitude' in deployments_df.columns and 'longitude' in deployments_df.columns:
        st.map(deployments_df[['latitude', 'longitude']])
    else:
        st.warning("Latitude and longitude columns not found in deployments.csv")

    # Pie Chart of Taxonomic Classification
    st.subheader("Taxonomic Classification")
    for level in taxonomy_levels:
        level_counts = filtered_df[level].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(level_counts, labels=level_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        plt.axis('equal')
        plt.title(f"{level.capitalize()} Distribution")
        st.pyplot(plt)
