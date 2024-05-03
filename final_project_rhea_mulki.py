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
temperature_df = pd.read_csv("data.csv")  

# Convert timestamp to datetime with error handling
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows with NaT values
df.dropna(subset=['timestamp'], inplace=True)

# Create a new column to represent the index
df['index'] = df.index

# Function to generate visualizations
def generate_visualizations(filtered_df):
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
    taxonomy_levels = ['class', 'order', 'family', 'genus', 'species']
    for level in taxonomy_levels:
        level_counts = filtered_df[level].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(level_counts, labels=level_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        plt.axis('equal')
        plt.title(f"{level.capitalize()} Distribution")
        st.pyplot(plt)

# Function to display research questions
def display_research_questions():
    st.write("""
1. **What did you set out to study?**  
    The primary aim of this project was to delve into the intricate connections between coastal habitats and adjacent marine systems along the California coast. 
    By leveraging camera trap technology to track wildlife, the project sought to integrate geographical, climate, and wildlife observation data. 
    The overarching goal was to unravel the complexities of species distribution, abundance, and behavior in response to environmental factors. 
    Throughout the project lifecycle, the objectives remained consistent, and there were no significant shifts in focus or objectives.
                
2. **What did you Discover/what were your conclusions?**  
    **Conclusions:**  
    a. Most commonly observed classes of species are Mammalia, Aves, and Reptilia.  
    b. Within Mammalia, the most common orders are Carnivore, Cetartiodactyla, and Rodentia. Within Aves, the most common orders are Charadriiformes, Pelecaniformes, and Cathartiformes. Reptiles observed belong to the Squamata order.  
    c. The most common mammals observed include Coyote, Wild Boar, and Mule Deer. The most common birds observed include Glaucous-winged Gull, California Gull, and Turkey Vulture. Reptiles observed include Western Fence Lizard and Common Gartersnake.  
    d. Human presence was also captured by the cameras.  
    Original assumption was that the most common orders would be Mammalia, Aves, and Reptilia, and this assumption is confirmed after analysis.

3. **What difficulties did you have in completing the project?**  
    During the project, several challenges were encountered, including:  
    - Difficulty in capturing specific climate and weather data for the given timestamps in the wildlife observation dataset.  
    - Limited availability of environmental data for establishing relationships between wildlife behavior and habitat characteristics.  
    - Settled for Santa Barbara County's average temperature data due to the closeness in proximity to coordinates of observed wildlife in the dataset, as capturing specific climate and weather data was challenging.  
    - Difficulty obtaining environmental data as an API or JSON.
    - Learning and applying web scraping techniques (e.g., BeautifulSoup and HTML parsing) for data acquisition.

4. **What skills did you wish you had while you were doing the project?**  
    While working on the project, the following skills were identified as areas for improvement:  
    - Enhanced proficiency in Python programming, particularly in data manipulation, analysis, and visualization.  
    - Improved understanding of web scraping and API usage for data acquisition from diverse sources.  
    - Further development of statistical and analytical skills for advanced data interpretation and modeling.

5. **What would you do “next” to expand or augment the project?**  
    In the future, the project could be expanded or augmented in the following ways:  
    - Focus on acquiring specific weather and climate data to enhance the analysis of wildlife habitat relationships.  
    - Incorporate advanced machine learning techniques for predictive modeling and species distribution mapping.  
    - Collaborate with environmental agencies and organizations to access additional datasets and conduct comprehensive studies.
""")


# Function to display dataframe
def display_dataframe(filtered_df):
    st.title("Filtered DataFrame (Images Table):")
    st.dataframe(filtered_df)

# Page Selection
def page_selection(filtered_df):
    st.title("Coastal Connections: Tracking Wildlife on the California Coast")
    st.title("Page Selection")

    # Create radio buttons to select the page
    page = st.radio("Select Page", ("Startup", "Research Questions", "Data", "Main App"))

    # Conditional rendering based on the selected page
    if page == "Startup":
        st.write("""
1. **Your name:**  
    Rhea Ranjit Mulki

2. **Explanation of how to use the webapp:**  
    **Objective:**  
    Investigating species diversity and richness in coastal habitats through camera trap observations and analyzing the influence of environmental variables, such as climate and habitat characteristics, on wildlife distribution patterns.  

    **Interactivity:**  
    The Streamlit app provides various interactive features to explore the wildlife camera trap data:  
    - Filter Options: Users can filter the dataset based on species name and taxonomic levels (class, order, family, genus, species).  
    - Index Range Slider: Allows users to select a specific range of indices to display rows from the images table, facilitating focused exploration of the dataset.  
    - Sidebar Information: Provides additional context and explanations about the project overview, conclusions, challenges faced, desired skills for improvement, future expansion plans, dataset descriptions, and visualizations.  

    **Visualizations:**  
    - Class Distribution: This bar chart illustrates the distribution of species across different taxonomic classes, such as mammals, birds, and reptiles. It provides insights into the overall composition of wildlife in the dataset.  
    - Species Distribution: This bar chart shows the distribution of different species observed in the wildlife camera trap data. It helps in understanding the relative abundance of various species in the study area.  
    - Common Name Distribution: This bar chart displays the distribution of species based on their common names. It offers a more familiar perspective on the observed wildlife, highlighting frequently encountered species.  
    - Timestamp Distribution: This histogram depicts the distribution of observations over time. It allows for the identification of temporal patterns in wildlife activity and can reveal peak periods of species presence.  
    - Map of Observations: This interactive map visualizes the spatial distribution of camera trap deployments. It enables users to explore the geographic locations of wildlife observations and identify hotspot areas.  
    - Taxonomic Classification: These pie charts represent the taxonomic classification of observed species at different levels, such as class, order, family, genus, and species. They provide a hierarchical view of species diversity in the dataset.  

    **Conclusions:**  
    - Most commonly observed classes of species are Mammalia, Aves, and Reptilia.  
    - Within Mammalia, the most common orders are Carnivore, Cetartiodactyla, and Rodentia. Within Aves, the most common orders are Charadriiformes, Pelecaniformes, and Cathartiformes. Reptiles observed belong to the Squamata order.  
    - The most common mammals observed include Coyote, Wild Boar, and Mule Deer. The most common birds observed include Glaucous-winged Gull, California Gull, and Turkey Vulture. Reptiles observed include Western Fence Lizard and Common Gartersnake.  
    - Human presence was also captured by the cameras.  

3. **Major "gotchas":**  
    Experiencing difficulties in capturing climate and weather data posed a significant challenge during the course of Project ECOTONE. The objective was to establish relationships between wildlife behavior and habitat study based on environmental factors. However, obtaining precise climate data aligned with the timestamps in the dataset proved to be challenging.  

    In response to this challenge, the project resorted to utilizing average temperature data for Santa Barbara County, CA. This decision was made due to the similarity of coordinates between the dataset and the Santa Barbara region. While this provided a workaround solution, it's acknowledged that more precise and comprehensive climate data would have strengthened the analysis and conclusions drawn from the project.
""")
    elif page == "Research Questions":
        display_research_questions()
    elif page == "Data":
        display_dataframe(filtered_df)
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

        #Dataset Description
        st.title("Dataset Descriptions")
        st.write(
            "1. **images.csv**: Contains wildlife observation data obtained from camera traps, including species information, timestamps, and behavioral observations.\n"
            "2. **deployments.csv**: Provides details about camera trap deployments, such as location coordinates, deployment dates, and environmental conditions.\n"
            "3. **data.csv**: Contains average temperature data for Santa Barbara County, CA, for the period April to March, for the years 2022 till 2024.\n"
            "4. **https://www.gps-coordinates.net/api**: This URL is utilized to fetch latitude and longitude coordinates for Santa Barbara, California, to enhance geographical analysis in the project."
        )
    elif page == "Main App":
        generate_visualizations(filtered_df)

# Filter dataframe based on user input
def filter_dataframe(df):
    # Filter options
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

    return filtered_df

# Run the page selection function
if __name__ == "__main__":
    # Filter dataframe
    filtered_df = filter_dataframe(df)
    # Display selected page
    page_selection(filtered_df)
