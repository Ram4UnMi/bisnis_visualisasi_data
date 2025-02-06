import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load datasets
df2020 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2020_ID_Region_Mobility_Report.csv")
df2021 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2021_ID_Region_Mobility_Report.csv")
df2022 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2022_ID_Region_Mobility_Report.csv")

# Add year column to each dataset
df2020['year'] = 2020
df2021['year'] = 2021
df2022['year'] = 2022

# Combine datasets
df = pd.concat([df2020, df2021, df2022], ignore_index=True)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Translation state
if 'language' not in st.session_state:
    st.session_state.language = 'en'  # Default to English

def toggle_language():
    if st.session_state.language == 'en':
        st.session_state.language = 'id'
    else:
        st.session_state.language = 'en'

# Streamlit page configuration
st.set_page_config(page_title="Data Mobility Visualization", layout="wide")

# Sidebar - add image at the top
st.sidebar.image("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/img/covidindo.jpg", use_container_width=True)

# Sidebar filters
st.sidebar.header("Filter Data")

# Year selector for clustering
selected_year = st.sidebar.selectbox(
    "Select Year for Clustering Analysis:",
    options=[2020, 2021, 2022],
    index=0
)

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

# Text content in both languages
texts = {
    'en': {
        'title': f"📊 Data Mobility Visualization for {region_filter}",
        'date_range': f"### Date Range: {start_date} to {end_date}",
        'intro': "Explore how mobility patterns in retail, workplaces, and residential areas have changed over time. Use the filters on the left to customize your view.",
        'translate': 'Translate to Indonesian',
        'retail_recreation_title': "Retail & Recreation vs Grocery & Pharmacy Mobility",
        'retail_recreation_insight': """
        ### Analysis & Strategic Insights
        - **Lockdown Period (2020-2021)**:
          - Sharp decline in retail/recreation showing strict movement restrictions
          - Grocery/pharmacy more resilient due to essential service status
          - Periodic spikes indicating essential shopping patterns
        - **New Normal (2021-2022)**:
          - Gradual recovery across both metrics
          - Stronger recovery in retail/recreation
          - Converging patterns suggesting return to pre-pandemic behavior
        """,
        'workplace_title': "Workplace Mobility Patterns",
        'workplace_insight': """
        ### Analysis & Strategic Insights
        - **Lockdown Period**:
          - Dramatic reduction showing successful work-from-home implementation
          - Gradual increases indicating phased return-to-office
          - Consistent negative values reflecting sustained remote work
        - **New Normal**:
          - Higher but below-baseline values showing hybrid work adoption
          - More stable patterns indicating established new workplace norms
        """,
        'residential_title': "Residential Mobility Patterns",
        'residential_insight': """
        ### Analysis & Strategic Insights
        - **Lockdown Impact**:
          - Intense residential presence during weekdays
          - Limited weekend variation suggesting restricted social activities
          - Peak hours aligned with work-from-home schedules
        - **New Normal Transition**:
          - More varied patterns showing return to normal routines
          - Distinct weekend-weekday differences
          - Lower overall residential presence indicating increased outdoor activities
        """,
        'clustering_title': "Mobility Pattern Clusters Analysis Dashboard",
        'clustering_subtitle': "Understanding Mobility Behavioral Patterns",
        'cluster_overview': """
        ### Cluster Overview
        The clustering analysis identifies three distinct mobility pattern groups:
        - **Cluster 0**: High Restriction Compliance
        - **Cluster 1**: Moderate Activity Patterns
        - **Cluster 2**: Essential/Active Movement
        """,
        'clustering_insight': """
        ### Analysis & Strategic Insights
        - **During Lockdown (2020)**:
          - Distinct clusters showing varying compliance levels
          - Tight clustering patterns indicating clear behavioral segments
          - Outliers potentially indicating essential worker movements
          - Strong negative correlation between residential and workplace mobility
        
        - **Transition Period (2021)**:
          - Clusters showing more spread, indicating behavioral variation
          - Emergence of hybrid patterns between clusters
          - Gradual shift towards pre-pandemic mobility patterns
          - Mixed workplace-retail relationships emerging
        
        - **New Normal Period (2022)**:
          - More dispersed clusters showing increased mobility variety
          - Cluster overlaps indicating blended pre-pandemic and new behaviors
          - Reduced distinction between weekend and weekday patterns
          - New stable patterns emerging in workplace mobility
        """,
        'cluster_characteristics': """
        ### Cluster Characteristics
        #### Cluster 0: High Restriction Compliance
        - Highest residential mobility (+)
        - Lowest retail/recreation mobility (-)
        - Minimal workplace mobility
        - Typical during strict lockdown periods
        
        #### Cluster 1: Moderate Activity Patterns
        - Balanced residential and workplace mobility
        - Moderate retail/recreation activity
        - Represents transition to hybrid working
        - Common during relaxed restrictions
        
        #### Cluster 2: Essential/Active Movement
        - Higher workplace mobility
        - Increased retail/recreation activity
        - Lower residential presence
        - Characteristic of essential workers/new normal
        """,
        'cluster_recommendations': """
        ### Strategic Recommendations
        1. **Policy Planning**:
           - Use cluster transitions to guide restriction adjustments
           - Monitor cluster sizes for compliance assessment
           - Target interventions based on cluster characteristics
        
        2. **Business Adaptations**:
           - Adjust operations based on dominant cluster patterns
           - Plan for hybrid work based on cluster distributions
           - Prepare for pattern shifts between clusters
        
        3. **Public Health Measures**:
           - Focus restrictions based on cluster movement patterns
           - Implement targeted measures for different clusters
           - Monitor cluster evolution for outbreak risks
        """,
        'final_notes': 'Data sourced from Google Mobility Reports | Visualization by Turtle IF-3 Team'
    },
    'id': {
        'title': f"📊 Visualisasi Mobilitas Data untuk {region_filter}",
        'date_range': f"### Rentang Tanggal: {start_date} hingga {end_date}",
        'intro': "Jelajahi bagaimana pola mobilitas di ritel, tempat kerja, dan area pemukiman telah berubah seiring waktu. Gunakan filter di sebelah kiri untuk menyesuaikan tampilan Anda.",
        'translate': 'Terjemahkan ke Bahasa Inggris',
        'retail_recreation_title': "Mobilitas Retail & Rekreasi vs Toko Kelontong & Farmasi",
        'retail_recreation_insight': """
        ### Analisis & Wawasan Strategis
        - **Periode Lockdown (2020-2021)**:
          - Penurunan tajam retail/rekreasi menunjukkan pembatasan pergerakan ketat
          - Toko kelontong/farmasi lebih stabil karena layanan esensial
          - Lonjakan periodik menunjukkan pola belanja kebutuhan pokok
        - **Normal Baru (2021-2022)**:
          - Pemulihan bertahap pada kedua metrik
          - Pemulihan lebih kuat di sektor retail/rekreasi
          - Pola konvergen menunjukkan kembali ke perilaku pra-pandemi
        """,
        'workplace_title': "Pola Mobilitas Tempat Kerja",
        'workplace_insight': """
        ### Analisis & Wawasan Strategis
        - **Periode Lockdown**:
          - Penurunan drastis menunjukkan keberhasilan WFH
          - Peningkatan bertahap menunjukkan kembali ke kantor secara bertahap
          - Nilai negatif konsisten mencerminkan kerja jarak jauh berkelanjutan
        - **Normal Baru**:
          - Nilai lebih tinggi namun di bawah baseline menunjukkan adopsi kerja hybrid
          - Pola lebih stabil menunjukkan norma baru tempat kerja
        """,
        'residential_title': "Pola Mobilitas Residensial",
        'residential_insight': """
        ### Analisis & Wawasan Strategis
        - **Dampak Lockdown**:
          - Kehadiran residensial intens selama hari kerja
          - Variasi akhir pekan terbatas menunjukkan aktivitas sosial terbatas
          - Jam puncak selaras dengan jadwal WFH
        - **Transisi Normal Baru**:
          - Pola lebih bervariasi menunjukkan kembali ke rutinitas normal
          - Perbedaan jelas antara akhir pekan-hari kerja
          - Kehadiran residensial lebih rendah menunjukkan peningkatan aktivitas luar
        """,
        'clustering_title': "Dashboard Analisis Klaster Pola Mobilitas",
        'clustering_subtitle': "Memahami Pola Perilaku Mobilitas",
        'cluster_overview': """
        ### Ikhtisar Klaster
        Analisis klaster mengidentifikasi tiga kelompok pola mobilitas yang berbeda:
        - **Klaster 0**: Kepatuhan Pembatasan Tinggi
        - **Klaster 1**: Pola Aktivitas Moderat
        - **Klaster 2**: Pergerakan Esensial/Aktif
        """,
        'clustering_insight': """
        ### Analisis & Wawasan Strategis
        - **Selama Lockdown (2020)**:
          - Klaster berbeda menunjukkan tingkat kepatuhan bervariasi
          - Pola pengelompokan ketat menunjukkan segmen perilaku yang jelas
          - Outlier menunjukkan pergerakan pekerja esensial
          - Korelasi negatif kuat antara mobilitas residensial dan tempat kerja
        
        - **Periode Transisi (2021)**:
          - Klaster menunjukkan lebih banyak sebaran, menandakan variasi perilaku
          - Munculnya pola hybrid antar klaster
          - Pergeseran bertahap menuju pola mobilitas pra-pandemi
          - Muncul hubungan campuran antara tempat kerja-retail
        
        - **Periode Normal Baru (2022)**:
          - Klaster lebih tersebar menunjukkan variasi mobilitas meningkat
          - Tumpang tindih klaster menunjukkan pencampuran perilaku lama dan baru
          - Berkurangnya perbedaan antara pola akhir pekan dan hari kerja
          - Munculnya pola stabil baru dalam mobilitas tempat kerja
        """,
        'cluster_characteristics': """
        ### Karakteristik Klaster
        #### Klaster 0: Kepatuhan Pembatasan Tinggi
        - Mobilitas residensial tertinggi (+)
        - Mobilitas retail/rekreasi terendah (-)
        - Mobilitas tempat kerja minimal
        - Tipikal selama periode lockdown ketat
        
        #### Klaster 1: Pola Aktivitas Moderat
        - Mobilitas residensial dan tempat kerja seimbang
        - Aktivitas retail/rekreasi moderat
        - Mewakili transisi ke kerja hybrid
        - Umum selama pembatasan dilonggarkan
        
        #### Klaster 2: Pergerakan Esensial/Aktif
        - Mobilitas tempat kerja lebih tinggi
        - Aktivitas retail/rekreasi meningkat
        - Kehadiran residensial lebih rendah
        - Karakteristik pekerja esensial/normal baru
        """,
        'cluster_recommendations': """
        ### Rekomendasi Strategis
        1. **Perencanaan Kebijakan**:
           - Gunakan transisi klaster untuk panduan penyesuaian pembatasan
           - Pantau ukuran klaster untuk penilaian kepatuhan
           - Targetkan intervensi berdasarkan karakteristik klaster
        
        2. **Adaptasi Bisnis**:
           - Sesuaikan operasi berdasarkan pola klaster dominan
           - Rencanakan kerja hybrid berdasarkan distribusi klaster
           - Persiapkan pergeseran pola antar klaster
        
        3. **Langkah Kesehatan Masyarakat**:
           - Fokuskan pembatasan berdasarkan pola pergerakan klaster
           - Terapkan langkah-langkah terarah untuk klaster berbeda
           - Pantau evolusi klaster untuk risiko wabah
        """,
        'final_notes': 'Data bersumber dari Laporan Mobilitas Google | Visualisasi oleh Tim Turtle IF-3'
    }
}

# Button to toggle language
st.button(texts[st.session_state.language]['translate'], on_click=toggle_language)

st.title(texts[st.session_state.language]['title'])
st.markdown(texts[st.session_state.language]['date_range'])
st.markdown(texts[st.session_state.language]['intro'])


# Retail & Recreation vs Grocery & Pharmacy
st.header(texts[st.session_state.language]['retail_recreation_title'])

# Membuat grafik garis tanpa penanda
fig1 = px.line(
    filtered_df,
    x='date',
    y=['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline'],
    labels={"value": "% Change", "variable": "Category"},
    line_shape='linear'  # Menentukan bentuk garis
)

# Menambahkan titik maksimum dan minimum untuk retail
max_value_retail = filtered_df['retail_and_recreation_percent_change_from_baseline'].max()
min_value_retail = filtered_df['retail_and_recreation_percent_change_from_baseline'].min()

max_date_retail = filtered_df.loc[filtered_df['retail_and_recreation_percent_change_from_baseline'].idxmax(), 'date']
min_date_retail = filtered_df.loc[filtered_df['retail_and_recreation_percent_change_from_baseline'].idxmin(), 'date']

# Menambahkan titik maksimum dan minimum untuk grocery & pharmacy
max_value_grocery = filtered_df['grocery_and_pharmacy_percent_change_from_baseline'].max()
min_value_grocery = filtered_df['grocery_and_pharmacy_percent_change_from_baseline'].min()

max_date_grocery = filtered_df.loc[filtered_df['grocery_and_pharmacy_percent_change_from_baseline'].idxmax(), 'date']
min_date_grocery = filtered_df.loc[filtered_df['grocery_and_pharmacy_percent_change_from_baseline'].idxmin(), 'date']

# Menambahkan titik maksimum dan minimum ke grafik
fig1.add_scatter(
    x=[max_date_retail, min_date_retail],
    y=[max_value_retail, min_value_retail],
    mode='markers',
    marker=dict(color='blue', size=10),
    name='Retail Max/Min Points'
)

fig1.add_scatter(
    x=[max_date_grocery, min_date_grocery],
    y=[max_value_grocery, min_value_grocery],
    mode='markers',
    marker=dict(color='orange', size=10),
    name='Grocery Max/Min Points'
)

# Mengubah warna garis berdasarkan perubahan
for trace in fig1.data:
    if trace.name == 'retail_and_recreation_percent_change_from_baseline':
        trace.line.color = 'green' if trace.y[-1] > trace.y[0] else 'red'
    else:
        trace.line.color = 'red'  # Warna untuk grocery and pharmacy

# Menampilkan grafik
st.plotly_chart(fig1, use_container_width=True)
st.markdown(texts[st.session_state.language]['retail_recreation_insight'])

# Workplace Mobility
st.header(texts[st.session_state.language]['workplace_title'])

# Identifikasi titik maksimum dan minimum
max_value = filtered_df['workplaces_percent_change_from_baseline'].max()
min_value = filtered_df['workplaces_percent_change_from_baseline'].min()

max_date = filtered_df.loc[filtered_df['workplaces_percent_change_from_baseline'].idxmax(), 'date']
min_date = filtered_df.loc[filtered_df['workplaces_percent_change_from_baseline'].idxmin(), 'date']

# Grafik utama
fig2 = px.bar(
    filtered_df,
    x='date',
    y='workplaces_percent_change_from_baseline',
    color='workplaces_percent_change_from_baseline',
    color_continuous_scale="Viridis"
)

# Tambahkan titik maksimum dan minimum
fig2.add_scatter(
    x=[max_date, min_date],
    y=[max_value, min_value],
    mode='markers',
    marker=dict(color='red', size=10),
    name='Max/Min Points'
)

st.plotly_chart(fig2, use_container_width=True)
st.markdown(texts[st.session_state.language]['workplace_insight'])

# Sub grafik yang hanya menampilkan grafik kenaikan data
st.subheader("Workplace Mobility Increase Patterns")

# Filter data untuk kenaikan (nilai positif)
increase_df = filtered_df[filtered_df['workplaces_percent_change_from_baseline'] > 0]

fig_increase = px.bar(
    increase_df,
    x='date',
    y='workplaces_percent_change_from_baseline',
    color='workplaces_percent_change_from_baseline',
    color_continuous_scale="Viridis",
    title="Workplace Mobility Increase Only"
)

st.plotly_chart(fig_increase, use_container_width=True)

# Sub grafik yang hanya menampilkan grafik penurunan data
st.subheader("Workplace Mobility Decrease Patterns")

# Filter data untuk penurunan (nilai negatif)
decrease_df = filtered_df[filtered_df['workplaces_percent_change_from_baseline'] < 0]

fig_decrease = px.bar(
    decrease_df,
    x='date',
    y='workplaces_percent_change_from_baseline',
    color='workplaces_percent_change_from_baseline',
    color_continuous_scale="Viridis",
    title="Workplace Mobility Decrease Only"
)

st.plotly_chart(fig_decrease, use_container_width=True)

# Residential Mobility Bar Chart
st.header(texts[st.session_state.language]['residential_title'])

# Hitung rata-rata perubahan mobilitas per hari
daily_avg = filtered_df.groupby(filtered_df['date'].dt.weekday)['residential_percent_change_from_baseline'].mean()
daily_avg.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Buat grafik batang
fig_bar = px.bar(
    daily_avg,
    x=daily_avg.index,
    y=daily_avg.values,
    labels={"x": "Day", "y": "Average % Change"},
    color=daily_avg.index,
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title="Average Residential Mobility Change by Day"
)

# Soroti akhir pekan
fig_bar.update_traces(marker_color=["blue"]*5 + ["red"]*2)

st.plotly_chart(fig_bar, use_container_width=True)
st.markdown(texts[st.session_state.language]['residential_insight'])

# Clustering Analysis
st.header(texts[st.session_state.language]['clustering_title'])
st.markdown(texts[st.session_state.language]['clustering_subtitle'])
st.markdown(texts[st.session_state.language]['cluster_overview'])

# Filter data for the selected year
clustering_df = df[df['year'] == selected_year].copy()

features = [
    'retail_and_recreation_percent_change_from_baseline',
    'grocery_and_pharmacy_percent_change_from_baseline',
    'parks_percent_change_from_baseline',
    'transit_stations_percent_change_from_baseline',
    'workplaces_percent_change_from_baseline',
    'residential_percent_change_from_baseline'
]

clustering_df = clustering_df.dropna(subset=features)

if len(clustering_df) > 0:
    scaler = StandardScaler()
    X = scaler.fit_transform(clustering_df[features])
    
    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clustering_df['cluster'] = kmeans.fit_predict(X)
    
    fig_cluster = px.scatter(
        clustering_df,
        x='retail_and_recreation_percent_change_from_baseline',
        y='workplaces_percent_change_from_baseline',
        color='cluster',
        labels={
            'retail_and_recreation_percent_change_from_baseline': 'Retail & Recreation Change (%)',
            'workplaces_percent_change_from_baseline': 'Workplace Change (%)'
        },
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_cluster, use_container_width=True)
    st.markdown(texts[st.session_state.language]['clustering_insight'])
    
    # Display cluster statistics with enhanced formatting
    st.subheader("Cluster Statistics")
    cluster_stats = clustering_df.groupby('cluster')[features].mean().round(2)
    st.dataframe(cluster_stats, use_container_width=True)
    
    # Display detailed cluster characteristics and recommendations
    st.markdown(texts[st.session_state.language]['cluster_characteristics'])
    st.markdown(texts[st.session_state.language]['cluster_recommendations'])
else:
    st.warning(f"No data available for clustering in {selected_year}")

# Final Notes
st.caption(texts[st.session_state.language]['final_notes'])

# Sidebar creators section
st.sidebar.markdown("---")
st.sidebar.markdown("**Anggota Kelompok:**")
st.sidebar.markdown("10122080 - Gilang Rifaldi")
st.sidebar.markdown("10122087 - Rama Hadi Nugraha")
st.sidebar.markdown("10122102 - Muhamad Hafiz Akbar")

# Hide Streamlit style
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
