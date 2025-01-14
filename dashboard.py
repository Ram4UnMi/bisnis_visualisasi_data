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
Explore how mobility patterns in retail, workplaces, and residential areas have changed over time.
Use the filters on the left to customize your view. Let's dive in!
""")

# Adding translation section
st.header("Translate Text to Indonesian")
translator = Translator()

input_text = st.text_area("Enter text to translate to Indonesian:")
if st.button("Translate"):
    if input_text.strip():
        translated_text = translator.translate(input_text, src='en', dest='id').text
        st.success(f"Translated Text: {translated_text}")
    else:
        st.error("Please enter some text to translate.")

# Visualizations
st.header("Mobility Trends Overview")

col1, col2 = st.columns(2)

# Retail & Recreation vs Grocery & Pharmacy
with col1:
    fig1 = px.line(
        filtered_df,
        x='date',
        y=['retail_and_recreation_percent_change_from_baseline',
           'grocery_and_pharmacy_percent_change_from_baseline'],
        labels={"value": "% Change", "variable": "Category"},
        title="Retail vs Grocery & Pharmacy Trends",
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

st.markdown("""
In these visualizations:
- The line chart shows percentage changes in mobility for retail and recreation versus grocery and pharmacy. 
- The bar chart depicts changes in workplace mobility over time.

Both charts allow us to observe trends and fluctuations in public movement across different sectors. Let's look further into daily behavior.
""")

# Daily Mobility Heatmap
st.header("Daily Mobility Patterns")
heatmap_data = filtered_df.pivot_table(
    index=filtered_df['date'].dt.weekday,
    columns=filtered_df['date'].dt.hour,
    values='residential_percent_change_from_baseline',
    aggfunc='mean'
)
heatmap_data.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

fig3 = px.imshow(
    heatmap_data,
    labels={"color": "% Change"},
    title="Residential Mobility Heatmap",
    color_continuous_scale="Plasma",
    aspect="auto"
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
The heatmap visualizes residential mobility changes across different days of the week and times of the day. 
It helps identify peak activity times and general patterns in lifestyle choices.
""")

# Additional Chart: Box Plot for Outlier Detection
st.header("Analysis of Workplace Mobility Variability")
fig4 = px.box(filtered_df, 
               x='date', 
               y='workplaces_percent_change_from_baseline', 
               title="Workplace Mobility Variability Over Time")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
This box plot reveals the distribution of workplace mobility changes over the selected date range. 
It highlights variability, outliers, and can help us understand periods of significant changes in mobility behavior.
""")

# Final Notes
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
