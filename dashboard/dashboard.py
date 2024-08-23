import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="🚲 Dashboard Berbagi Sepeda", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Pemuatan data dengan caching
@st.cache_data
def muat_data():
    return pd.read_csv('main_data.csv')

data = muat_data()

# Konversi kolom 'dteday' menjadi tipe tanggal
data['dteday'] = pd.to_datetime(data['dteday'], format='%Y-%m-%d')

# Palet warna modern dan ramah pengguna
warna = {
    'latar': '#fafafa',
    'teks': '#333333',
    'utama': '#1abc9c',
    'sekunder': '#e74c3c',
    'aksen': '#3498db',
    'netral': '#bdc3c7'
}

# CSS kustom untuk meningkatkan tampilan
st.markdown(f"""
    <style>
    .reportview-container .main .block-container {{
        max-width: 1200px;
        padding: 2rem;
        background-color: {warna['latar']};
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }}
    .reportview-container .main {{
        color: {warna['teks']};
        font-family: 'Helvetica', sans-serif;
    }}
    h1, h2, h3 {{
        color: {warna['utama']};
        font-weight: 600;
    }}
    .stSelectbox label, .stSlider label {{
        color: {warna['teks']} !important;
    }}
    .stMetric {{
        background-color: {warna['utama']};
        padding: 15px;
        border-radius: 8px;
        color: white;
    }}
    .stMetric .stMetricLabel {{
        color: white !important;
        font-size: 1rem;
    }}
    .stMetric .stMetricValue {{
        font-size: 1.8rem;
    }}
    .st-expander {{
        background-color: {warna['netral']};
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

# Judul dashboard
st.title("🚲 Dashboard Analitik Sepeda")
st.markdown("Jelajahi pola penggunaan sepeda dengan visualisasi interaktif dan desain modern.")

# Sidebar untuk pilihan data
with st.sidebar:
    st.header("🛠️ Opsi Dashboard")
    jenis_data = st.selectbox("Pilih Jenis Data", options=['Harian', 'Per Jam'])

# Filter data berdasarkan jenis yang dipilih
data_terfilter = data[data['type'] == ('daily' if jenis_data == 'Harian' else 'hourly')]

# Metrik utama yang ditampilkan di dashboard
st.subheader("📊 Metrik Utama")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", f"{data_terfilter['cnt'].sum():,} Unit")
with col2:
    st.metric("Penggunaan Terbanyak", f"{data_terfilter['cnt'].max():,} Unit")
with col3:
    st.metric("Jumlah Data", f"{data_terfilter.shape[0]} Rekaman")

# Tren penggunaan sepeda
st.subheader("📈 Tren Penggunaan Sepeda")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    data_terfilter["dteday"],
    data_terfilter["cnt"],
    marker='o', 
    linewidth=2,
    color=warna['utama']
)
ax.set_title("Penyewaan Sepeda Sepanjang Waktu", fontsize=16)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10)
st.pyplot(fig)

# Dampak cuaca terhadap penyewaan sepeda
st.subheader("🌦️ Dampak Cuaca terhadap Penyewaan Sepeda")
data_cuaca = data_terfilter.groupby('weathersit')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="weathersit", y="cnt", data=data_cuaca, palette="coolwarm", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda berdasarkan Kondisi Cuaca", fontsize=16)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10)
st.pyplot(fig)

# Pola penggunaan sepeda berdasarkan waktu
st.subheader("⏰ Pola Penggunaan Sepeda berdasarkan Waktu")
if jenis_data == 'Per Jam':
    data_waktu = data_terfilter.groupby('hr')['cnt'].mean().reset_index()
    x_label = "Jam"
else:
    data_waktu = data_terfilter.groupby('weekday')['cnt'].mean().reset_index()
    x_label = "Hari dalam Seminggu"

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr' if jenis_data == 'Per Jam' else 'weekday', y="cnt", data=data_waktu, marker='o', color=warna['utama'], ax=ax)
ax.set_title(f"Rata-rata Penyewaan per {x_label}", fontsize=16)
ax.set_xlabel(x_label)
ax.set_ylabel("Rata-rata Penyewaan")
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10)
st.pyplot(fig)

# Prediksi interaktif penyewaan sepeda
st.subheader("🔮 Prediksi Penyewaan Sepeda")
col1, col2 = st.columns(2)
with col1:
    suhu = st.slider("Suhu (°C)", min_value=0, max_value=40, value=20)
    kelembaban = st.slider("Kelembaban (%)", min_value=0, max_value=100, value=50)
with col2:
    kecepatan_angin = st.slider("Kecepatan Angin (km/jam)", min_value=0, max_value=50, value=10)
    cuaca = st.selectbox("Kondisi Cuaca", options=['Cerah', 'Berkabut', 'Hujan Ringan', 'Hujan Lebat'])

# Model prediksi sederhana
dampak_cuaca = {'Cerah': 50, 'Berkabut': 30, 'Hujan Ringan': 10, 'Hujan Lebat': -20}
prediksi = (suhu * 2) + (50 - abs(kelembaban - 50)) - (kecepatan_angin * 0.5) + dampak_cuaca.get(cuaca, 0)
prediksi = max(0, prediksi)  # Memastikan prediksi tidak negatif

st.metric("Prediksi Penyewaan", f"{int(prediksi)} Unit")

# Tampilan data mentah
with st.expander("📄 Tampilkan Data Mentah"):
    st.dataframe(data_terfilter.style.highlight_max(axis=0), use_container_width=True)

# Footer dengan kredit
st.markdown("---")
st.markdown("Created by Niko Dwicahyo Widiyanto © 2024 | [LinkedIn](https://www.linkedin.com/in/nikodwicahyo/)")
