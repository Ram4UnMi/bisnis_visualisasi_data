import pandas as pd
import plotly.express as px
import streamlit as st

# Load datasets
df2020 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2020_ID_Region_Mobility_Report.csv")
df2021 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2021_ID_Region_Mobility_Report.csv")
df2022 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2022_ID_Region_Mobility_Report.csv")

# Combine datasets
df = pd.concat([df2020, df2021, df2022], ignore_index=True)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Streamlit page configuration
st.set_page_config(page_title="Data Mobility Visualization", layout="wide")

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
                 (df['date'] <= pd.to_datetime(end_date)) &
                 (df['sub_region_1'] == region_filter)]

# Main Page Title
st.title(f"📊 Data Mobility Visualization for {region_filter}")
st.markdown(f"### Date Range: {start_date} to {end_date}")
st.markdown("""
As the world navigates through changes prompted by various events, the patterns of mobility in retail, workplaces, and public spaces tell a critical story. This visualization aims to inform how these mobility trends have evolved over time in your selected region.
""")

# Visualizations
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(
        filtered_df,
        x='date',
        y=['retail_and_recreation_percent_change_from_baseline',
           'grocery_and_pharmacy_percent_change_from_baseline'],
        labels={"value": "% Change", "variable": "Category"},
        title="Retail & Recreation vs Grocery & Pharmacy Trends"
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("""
    The line chart above shows the percentage change in mobility for retail and recreation compared to a baseline period. 
    Observing these trends can highlight how public sentiment influences shopping behaviors and activity in these areas over time.
    """)

with col2:
    fig2 = px.bar(
        filtered_df,
        x='date',
        y='workplaces_percent_change_from_baseline',
        color='workplaces_percent_change_from_baseline',
        title="Workplace Mobility Change Over Time",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""
    This bar chart illustrates changes in workplace mobility. Significant fluctuations in this metric may correlate with policy changes, remote working trends, or public health guidance, offering insights into how work habits may have shifted.
    """)

st.markdown("---")

# Heatmap for Daily Trends
st.header("Daily Mobility Trends")
heatmap_data = filtered_df.pivot_table(
    index=filtered_df['date'].dt.weekday,
    columns=filtered_df['date'].dt.hour,
    values='residential_percent_change_from_baseline',
    aggfunc='mean'
)
heatmap_data.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
fig3 = px.imshow(
    heatmap_data,
    labels={"color": "% Change"},
    title="Residential Mobility Heatmap",
    color_continuous_scale="Plasma"
)
st.plotly_chart(fig3, use_container_width=True)
st.markdown("""
The heatmap provides a visual representation of residential mobility changes throughout the week, differentiated by hours of the day. Analyzing this data can indicate patterns of residence activity, health assessments, or seasonal trends.
""")

st.caption('Data sourced from Google Mobility Reports | Visualization by Turtle IF-3 Team')

# Hide Streamlit style
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
