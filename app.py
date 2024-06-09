import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import requests
import dropbox
from io import BytesIO

# Akses token Dropbox (awal)
ACCESS_TOKEN = "sl.B1y7hImSo3mrrq0GWevhOQG1lsrI8BBKSWkNxVbv-9swdoRghESbKt9xgIVK9gJPgs8OAElpVIyFrzQsNCoGkZCi5JEcDxH2jwadlL-jAeQ0SxTTgCSja05YdF5QioGxwKkuRsP-gZRI"
REFRESH_TOKEN = "YQYhc7OUG98AAAAAAAAAATJ2SBVuv8yMMZbzYqfpfW0Hgye_iTliKFeL11barG5s"
APP_KEY = "os3wd6val28otux"
APP_SECRET = "ah6624h2dkqi2hk"

# Fungsi untuk mendapatkan akses token baru menggunakan refresh token
def refresh_access_token(refresh_token, client_id, client_secret):
    url = "https://api.dropboxapi.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, data=data)
    response_data = response.json()
    return response_data["access_token"]

# Inisialisasi klien Dropbox dengan token akses baru
def initialize_dropbox_client():
    global ACCESS_TOKEN
    ACCESS_TOKEN = refresh_access_token(REFRESH_TOKEN, APP_KEY, APP_SECRET)
    return dropbox.Dropbox(ACCESS_TOKEN)

dbx = initialize_dropbox_client()

# Fungsi untuk memuat data dari Dropbox
@st.cache_data
def load_data_from_dropbox(file_path):
    _, res = dbx.files_download(file_path)
    data = pd.read_csv(BytesIO(res.content))
    return data

# Load data dari Dropbox
df_user1 = load_data_from_dropbox("/multimodal_tweets_data_user1.csv")
df_user2 = load_data_from_dropbox("/multimodal_tweets_data_user2.csv")
df_user3 = load_data_from_dropbox("/multimodal_tweets_data_user3.csv")

# Gabungkan data dari beberapa file
df_user1['anotasi2'] = df_user2['anotasi']
df_user1['anotasi3'] = df_user3['anotasi']

# Ambil kolom yang diperlukan
df = df_user1[['No', 'tweet_text', 'tweet_url', 'images', 'anotasi', 'anotasi2', 'anotasi3']]

# Streamlit interface
st.title("Twitter Data Visualization")

tweet_index = st.number_input("Masukkan indeks tweet yang ingin ditampilkan", min_value=1, max_value=len(df), value=1, step=1)
tweet_index -= 1
if st.button("Tampilkan Tweet"):
    tweet_url = df.iloc[tweet_index]['tweet_url']
    target_value = df.iloc[tweet_index]['anotasi']
    st.code(tweet_url)
    tweet_html = f"<p style='background-color:black;color:white;text-align:center;'>Target: {target_value}</p><blockquote class='twitter-tweet' data-media-max-width='350' align='center' data-conversation='none' data-theme='dark'><a href='{tweet_url}'></a></blockquote><script async src='https://platform.twitter.com/widgets.js' charset='utf-8'></script>"
    components.html(tweet_html, height=600, scrolling=True)

# Membuat chart dari jumlah target
target_counts = df['anotasi'].value_counts()

fig_bar, ax_bar = plt.subplots()
bars = ax_bar.bar(target_counts.index, target_counts.values)
ax_bar.set_xticklabels(target_counts.index, rotation=45)

# Menambahkan label jumlah yang tepat di atas setiap batang
for bar in bars:
    yval = bar.get_height()
    ax_bar.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom')

# Menambahkan teks total data di dalam diagram batang
total_data = len(df)
ax_bar.text(0.5, 1.05, f"Total Data: {total_data}", transform=ax_bar.transAxes, ha='center')

st.pyplot(fig_bar)

fig_pie, ax_pie = plt.subplots()
ax_pie.pie(target_counts, labels=target_counts.index, autopct='%1.1f%%')
st.pyplot(fig_pie)

# Paginasi
page_size = 25
page_number = st.number_input("Pilih halaman", min_value=1, max_value=(len(df) // page_size) + 1, value=1)

start_idx = (page_number - 1) * page_size
end_idx = start_idx + page_size
st.dataframe(df.iloc[start_idx:end_idx])
