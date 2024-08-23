import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Pengaturan tampilan Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide", initial_sidebar_state="expanded")

# Membaca data yang telah dibersihkan
@st.cache_data
def load_data():
    return pd.read_csv('main_data.csv')

data = load_data()

# Tema warna
colors = {
    'background': '#0e1117',
    'text': '#ffffff',
    'primary': '#FF4B4B',
    'secondary': '#0083B8'
}

# Custom CSS
st.markdown(f"""
    <style>
    .reportview-container .main .block-container{{
        max-width: 1200px;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }}
    .reportview-container .main {{
        color: {colors['text']};
        background-color: {colors['background']};
    }}
    .sidebar .sidebar-content {{
        background-color: {colors['background']};
    }}
    .Widget>label {{
        color: {colors['text']};
    }}
    .stPlotlyChart {{
        background-color: {colors['background']};
    }}
    .st-bb {{
        background-color: {colors['background']};
    }}
    .st-at {{
        background-color: {colors['background']};
    }}
    .st-cy {{
        background-color: {colors['secondary']};
    }}
    .st-d5 {{
        background-color: {colors['primary']};
    }}
    </style>
    """, unsafe_allow_html=True)

# Judul dashboard
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis mendalam tentang pola penggunaan sepeda")

# Sidebar
st.sidebar.header("🛠️ Konfigurasi Dashboard")
data_type = st.sidebar.selectbox("Pilih Tipe Data", options=['daily', 'hourly'])

# Filter data
filtered_data = data[data['type'] == data_type]

# Metrik Utama
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Peminjaman", f"{filtered_data['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Harian", f"{filtered_data['cnt'].mean():.2f}")
with col3:
    st.metric("Jumlah Hari/Jam", f"{filtered_data.shape[0]}")

# Fungsi untuk membuat grafik
def create_chart(data, x, y, chart_type, title):
    if chart_type == 'Bar':
        fig = px.bar(data, x=x, y=y, title=title)
    else:  # Grafik Garis
        fig = px.line(data, x=x, y=y, title=title)
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig

# Tren Penggunaan Sepeda
st.header("📈 Tren Penggunaan Sepeda")
tren_chart = create_chart(filtered_data, 'dteday' if 'dteday' in filtered_data.columns else 'instant', 'cnt', 'Bar', 'Jumlah Peminjaman Sepeda Seiring Waktu')
st.plotly_chart(tren_chart, use_container_width=True)

# Pengaruh Cuaca
st.header("🌦️ Pengaruh Cuaca Terhadap Peminjaman Sepeda")
weather_chart = create_chart(filtered_data.groupby('weathersit')['cnt'].sum().reset_index(), 'weathersit', 'cnt', 'Bar', 'Total Peminjaman Sepeda Berdasarkan Kondisi Cuaca')
st.plotly_chart(weather_chart, use_container_width=True)

# Pola Penggunaan Berdasarkan Waktu
st.header("⏰ Pola Penggunaan Berdasarkan Waktu")
if data_type == 'hourly':
    time_chart = create_chart(filtered_data.groupby('hr')['cnt'].mean().reset_index(), 'hr', 'cnt', 'Line', 'Rata-rata Peminjaman per Jam')
else:
    time_chart = create_chart(filtered_data.groupby('weekday')['cnt'].mean().reset_index(), 'weekday', 'cnt', 'Line', 'Rata-rata Peminjaman per Hari')
st.plotly_chart(time_chart, use_container_width=True)

# Prediksi Sederhana
st.header("🔮 Prediksi Jumlah Peminjaman")
col1, col2 = st.columns(2)
with col1:
    temp = st.slider("Temperatur (Celsius)", min_value=0, max_value=40, value=20)
    humidity = st.slider("Kelembaban (%)", min_value=0, max_value=100, value=50)
with col2:
    windspeed = st.slider("Kecepatan Angin (km/h)", min_value=0, max_value=50, value=10)
    weather = st.selectbox("Kondisi Cuaca", options=['Clear', 'Mist', 'Light Rain', 'Heavy Rain'])

# Simulasi prediksi sederhana (gunakan model yang sebenarnya jika ada)
prediction = (temp * 2) + (humidity * 0.5) - (windspeed * 1.5) + (50 if weather == 'Clear' else 0)
st.metric("Prediksi Jumlah Peminjaman", f"{int(prediction)}")

# Data Mentah
if st.checkbox("Tampilkan Data Mentah"):
    st.subheader("Data Mentah")
    st.dataframe(filtered_data.style.highlight_max(axis=0), width=1000, height=500)

# Footer
st.markdown("---")
st.markdown("Created by Niko Dwicahyo Widiyanto © 2024 | [LinkedIn](https://www.linkedin.com/in/nikodwicahyo/)")
