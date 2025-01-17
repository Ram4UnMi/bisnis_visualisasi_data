import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import geopandas as gpd
import matplotlib.pyplot as plt

# Load datasets
df2020 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2020_ID_Region_Mobility_Report.csv")
df2021 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2021_ID_Region_Mobility_Report.csv")
df2022 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2022_ID_Region_Mobility_Report.csv")

# Combine datasets
df = pd.concat([df2020, df2021, df2022], ignore_index=True)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Sidebar filters
st.sidebar.header("Filter Data")
min_date = df['date'].min()
max_date = df['date'].max()

start_date, end_date = st.sidebar.date_input(
    "Select date range:", [min_date, max_date], min_value=min_date, max_value=max_date
)

region_filter = st.sidebar.selectbox(
    "Select Region:", options=df['sub_region_1'].dropna().unique(), index=0
)

# Filter data based on user input
filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) &
                 (df['date'] <= pd.to_datetime(end_date))]

# Perform clustering
clustering_columns = [
    'retail_and_recreation_percent_change_from_baseline',
    'grocery_and_pharmacy_percent_change_from_baseline',
    'parks_percent_change_from_baseline',
    'workplaces_percent_change_from_baseline',
    'residential_percent_change_from_baseline'
]

data_for_clustering = filtered_df[clustering_columns].dropna()
data_scaled = StandardScaler().fit_transform(data_for_clustering)

kmeans = KMeans(n_clusters=3, random_state=42)
filtered_df['Cluster'] = kmeans.fit_predict(data_scaled)

# Visualizations
st.title("Data Mobility Clustering and Visualization")

# Heatmap
st.header("Heatmap of Residential Mobility")
heatmap_data = filtered_df.pivot_table(
    index=filtered_df['date'].dt.weekday,
    columns=filtered_df['date'].dt.hour,
    values='residential_percent_change_from_baseline',
    aggfunc='mean'
)

if not heatmap_data.empty:
    heatmap_data.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    fig_heatmap = px.imshow(
        heatmap_data,
        labels={"color": "% Change"},
        title="Residential Mobility Heatmap",
        color_continuous_scale="Plasma",
        aspect="auto"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
else:
    st.warning("No data available for the selected dates. Please try a different date range or region.")

# Scatter Plot of Clusters
st.header("Scatter Plot of Mobility Clusters")
fig_scatter = px.scatter(
    filtered_df,
    x='retail_and_recreation_percent_change_from_baseline',
    y='workplaces_percent_change_from_baseline',
    color='Cluster',
    title="Clustering of Mobility Data",
    labels={
        'retail_and_recreation_percent_change_from_baseline': 'Retail & Recreation Mobility',
        'workplaces_percent_change_from_baseline': 'Workplace Mobility'
    },
    hover_data=clustering_columns
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Geospatial Map of Workplace Mobility
st.header("Geospatial Map of Workplace Mobility")
workplace_mobility = df.groupby('sub_region_1')['workplaces_percent_change_from_baseline'].mean().reset_index()

# Placeholder: Replace with actual Indonesia shapefile
indonesia_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
indonesia_map = indonesia_map[indonesia_map['name'] == 'Indonesia']

# Merge mobility data with geospatial data
indonesia_map = indonesia_map.merge(workplace_mobility, left_on='name', right_on='sub_region_1', how='left')

# Plot geospatial map
fig, ax = plt.subplots(1, 1, figsize=(12, 10))
indonesia_map.plot(column='workplaces_percent_change_from_baseline',
                   cmap='OrRd',
                   legend=True,
                   legend_kwds={'label': "Workplace Mobility Change (%)"},
                   ax=ax)
plt.title('Workplace Mobility Across Provinces in Indonesia')
st.pyplot(fig)

st.caption("Data sourced from Google Mobility Reports | Visualization by Streamlit")
