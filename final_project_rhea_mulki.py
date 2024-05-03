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
temperature_df = pd.read_csv("data.csv")  # New: Read temperature data from data.csv

# Convert timestamp to datetime with error handling
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows with NaT values
df.dropna(subset=['timestamp'], inplace=True)

# Create a new column to represent the index
df['index'] = df.index

# Project Title
st.sidebar.title("Coastal Connections: Tracking Wildlife on the California Coast")

# Name
st.sidebar.write("Rhea Ranjit Mulki")

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
index_range = st.sidebar.slider("Select Index Range (Images Table):", index_min, index_max, (index_min, index_max))

# Filter the dataset based on user inputs
filtered_df = df.copy()
if species_name:
    filtered_df = filtered_df[filtered_df['species'].str.contains(species_name, case=False)]
for level, values in taxonomy_filters.items():
    if values:
        filtered_df = filtered_df[filtered_df[level].isin(values)]
filtered_df = filtered_df[(filtered_df['index'] >= index_range[0]) & (filtered_df['index'] <= index_range[1])]

# Show the filtered data (images table)
st.title("Images Table")
st.write(filtered_df)

# Display deployments table
st.title("Deployments Table")
st.write(deployments_df)

# Fetch and display latitude and longitude for Santa Barbara
st.subheader("Santa Barbara Coordinates")
latitude, longitude = fetch_santa_barbara_coordinates()
if latitude is not None and longitude is not None:
    st.write(f"Latitude: {latitude}, Longitude: {longitude}")

# Display temperature data
st.title("Temperature Data")
st.write(temperature_df)  # New: Display temperature data from data.csv

# Visualizations
st.title("Visualizations")
if not filtered_df.empty:
    # Bar Chart of Class Distribution
    st.subheader("Class Distribution")
    class_counts = filtered_df['class'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=class_counts.index, y=class_counts.values, palette='muted')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Class")
    plt.ylabel("Count")
    st.pyplot(plt)

    # Bar Chart of Species Distribution
    st.subheader("Species Distribution")
    species_counts = filtered_df['species'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=species_counts.index, y=species_counts.values, palette='viridis')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Species")
    plt.ylabel("Count")
    st.pyplot(plt)

    # Bar Chart of Common Name Distribution
    st.subheader("Common Name Distribution")
    common_name_counts = filtered_df['common_name'].value_counts()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=common_name_counts.index, y=common_name_counts.values, palette='pastel')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Common Name")
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

# Project Overview and Conclusions
st.sidebar.title("Project Overview & Conclusions")
st.sidebar.write(
    "Objective: Investigating species diversity and richness in coastal habitats through camera trap observations and analyzing the influence of environmental variables, such as climate and habitat characteristics, on wildlife distribution patterns.\n"
    "\nConclusions:\n"
    "1. Most commonly observed classes of species are mammalia, aves, and reptilia.\n"
    "2. Within mammalia, the most common orders are carnivore, cetartiodactyla, and rodentia. "
    "Within aves, the most common orders are charadriiformes, pelecaniformes, and cathartiformes. "
    "Reptiles observed belong to the squamata order.\n"
    "3. The most common mammals observed include coyote, wild boar, and mule deer. "
    "The most common birds observed include Glaucous-winged gull, California gull, and turkey vulture. "
    "Reptiles observed include Western fence lizard and common gartersnake.\n"
    "4. Human presence was also captured by the cameras."
)

# Challenges Faced
st.sidebar.title("Challenges Faced")
st.sidebar.write(
    "During the project, several challenges were encountered, including:\n"
    "- Difficulty in capturing specific climate and weather data for the given timestamps in the wildlife observation dataset.\n"
    "- Limited availability of environmental data for establishing relationships between wildlife behavior and habitat characteristics.\n"
    "- As a result of difficulty faced in capturing specific climate and weather data, settled for Santa Barbara County's average temperature data due to closeness in proximity to coordinates of observed wildlife in the dataset.\n"
    "- Learning and applying web scraping techniques (e.g., BeautifulSoup and HTML parsing) for data acquisition."
)

# Desired Skills for Improvement
st.sidebar.title("Desired Skills for Improvement")
st.sidebar.write(
    "While working on the project, the following skills were identified as areas for improvement:\n"
    "- Enhanced proficiency in Python programming, particularly in data manipulation, analysis, and visualization.\n"
    "- Improved understanding of web scraping and API usage for data acquisition from diverse sources.\n"
    "- Further development of statistical and analytical skills for advanced data interpretation and modeling."
)

# Future Expansion Plans
st.sidebar.title("Future Expansion Plans")
st.sidebar.write(
    "In the future, the project could be expanded or augmented in the following ways:\n"
    "- Focus on acquiring specific weather and climate data to enhance the analysis of wildlife habitat relationships.\n"
    "- Incorporate advanced machine learning techniques for predictive modeling and species distribution mapping.\n"
    "- Collaborate with environmental agencies and organizations to access additional datasets and conduct comprehensive studies."
)

# Dataset Descriptions
st.sidebar.title("Dataset Descriptions")
st.sidebar.write(
    "1. **images.csv**: Contains wildlife observation data obtained from camera traps, including species information, timestamps, and behavioral observations.\n"
    "2. **deployments.csv**: Provides details about camera trap deployments, such as location coordinates, deployment dates, and environmental conditions.\n"
    "3. **data.csv**: Contains average temperature data for Santa Barbara County, CA, for the period April to March, for the years 2022 till 2024.\n"
)

# Visualizations Explanation
st.sidebar.title("Visualizations Explanation")
st.sidebar.write(
    "1. **Species Distribution**: This bar chart shows the distribution of different species observed in the wildlife camera trap data. "
    "It helps in understanding the relative abundance of various species in the study area.\n"
    "2. **Class Distribution**: This bar chart illustrates the distribution of species across different taxonomic classes, "
    "such as mammals, birds, and reptiles. It provides insights into the overall composition of wildlife in the dataset.\n"
    "3. **Common Name Distribution**: This bar chart displays the distribution of species based on their common names. "
    "It offers a more familiar perspective on the observed wildlife, highlighting frequently encountered species.\n"
    "4. **Timestamp Distribution**: This histogram depicts the distribution of observations over time. It allows for the "
    "identification of temporal patterns in wildlife activity and can reveal peak periods of species presence.\n"
    "5. **Map of Observations**: This interactive map visualizes the spatial distribution of camera trap deployments. "
    "It enables users to explore the geographic locations of wildlife observations and identify hotspot areas.\n"
    "6. **Taxonomic Classification**: These pie charts represent the taxonomic classification of observed species at different levels, "
    "such as class, order, family, genus, and species. They provide a hierarchical view of species diversity in the dataset."
)

# Interactivity Explanation
st.sidebar.title("Interactivity Explanation")
st.sidebar.write(
    "The Streamlit app provides various interactive features to explore the wildlife camera trap data:\n"
    "- **Filter Options**: Users can filter the dataset based on species name and taxonomic levels (class, order, family, genus, species).\n"
    "- **Index Range Slider**: Allows users to select a specific range of indices to display rows from the images table, facilitating "
    "focused exploration of the dataset.\n"
    "- **Sidebar Information**: Provides additional context and explanations about the project overview, conclusions, challenges faced, "
    "desired skills for improvement, future expansion plans, dataset descriptions, and visualizations."
)
