import pandas as pd
import plotly.express as px
import streamlit as st
from googletrans import Translator

# Load datasets
df2020 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2020_ID_Region_Mobility_Report.csv")
df2021 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2021_ID_Region_Mobility_Report.csv")
df2022 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2022_ID_Region_Mobility_Report.csv")

# Combine datasets
df = pd.concat([df2020, df2021, df2022], ignore_index=True)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Translation state
if 'language' not in st.session_state:
    st.session_state.language = 'en'  # Default to English

def toggle_language():
    if st.session_state.language == 'en':
        st.session_state.language = 'id'  # Switch to Indonesian
    else:
        st.session_state.language = 'en'  # Switch to English

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
texts = {
    'en': {
        'title': f"📊 Data Mobility Visualization for {region_filter}",
        'date_range': f"### Date Range: {start_date} to {end_date}",
        'intro': "Explore how mobility patterns in retail, workplaces, and residential areas have changed over time. Use the filters on the left to customize your view. Let's dive in!",
        'translate': 'Translate to Indonesian',
        'mobility_overview': "Mobility Trends Overview",
        'workplace_variability': "Analysis of Workplace Mobility Variability",
        'final_notes': 'Data sourced from Google Mobility Reports | Visualization by Turtle IF-3 Team'
    },
    'id': {
        'title': f"📊 Visualisasi Mobilitas Data untuk {region_filter}",
        'date_range': f"### Rentang Tanggal: {start_date} hingga {end_date}",
        'intro': "Jelajahi bagaimana pola mobilitas di ritel, tempat kerja, dan area pemukiman telah berubah seiring waktu. Gunakan filter di sebelah kiri untuk menyesuaikan tampilan Anda. Ayo kita mulai!",
        'translate': 'Terjemahkan ke Bahasa Inggris',
        'mobility_overview': "Tinjauan Mobilitas",
        'workplace_variability': "Analisis Variabilitas Mobilitas Tempat Kerja",
        'final_notes': 'Data bersumber dari Laporan Mobilitas Google | Visualisasi oleh Tim Turtle IF-3'
    }
}

# Button to toggle language
st.button(texts[st.session_state.language]['translate'], on_click=toggle_language)

st.title(texts[st.session_state.language]['title'])
st.markdown(texts[st.session_state.language]['date_range'])
st.markdown(texts[st.session_state.language]['intro'])

# Visualizations
st.header(texts[st.session_state.language]['mobility_overview'])

col1, col2 = st.columns(2)

# Retail & Recreation vs Grocery & Pharmacy
with col1:
    fig1 = px.line(
        filtered_df,
        x='date',
        y=['retail_and_recreation_percent_change_from_baseline',
           'grocery_and_pharmacy_percent_change_from_baseline'],
        labels={"value": "% Change", "variable": "Category"},
        title=texts[st.session_state.language]['mobility_overview'],
        markers=True
    )
    st.plotly_chart(fig1, use_container_width=True)

# Workplace Mobility
with col2:
    fig2 = px.bar(
        filtered_df,
        x='date',
        y='workplaces_percent_change_from_baseline',
        color='workplaces_percent_change_from_baseline',
        title="Workplace Mobility Over Time",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Daily Mobility Heatmap
st.header("Daily Mobility Patterns")
# Ensure mean is correctly aggregated
heatmap_data = filtered_df.pivot_table(
    index=filtered_df['date'].dt.weekday,
    columns=filtered_df['date'].dt.hour,
    values='residential_percent_change_from_baseline',
 aggfunc='mean'
)

# Check if heatmap_data is not empty and has valid shape
if not heatmap_data.empty and heatmap_data.shape[0] == 7 and heatmap_data.shape[1] > 0:
    heatmap_data.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    fig3 = px.imshow(
        heatmap_data,
        labels={"color": "% Change"},
        title="Residential Mobility Heatmap",
        color_continuous_scale="Plasma",
        aspect="auto"
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("No data available for the selected dates. Please try a different date range or region.")

# Additional Chart: Box Plot for Outlier Detection
st.header(texts[st.session_state.language]['workplace_variability'])
fig4 = px.box(filtered_df, 
               x='date', 
               y='workplaces_percent_change_from_baseline', 
               title="Workplace Mobility Variability Over Time")
st.plotly_chart(fig4, use_container_width=True)

# Final Notes
st.caption(texts[st.session_state.language]['final_notes'])

# Hide Streamlit style
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
