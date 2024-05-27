import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# Membaca file CSV
df = pd.read_csv("multimodal_tweets_data_user1.csv")

tweet_index = st.number_input("Masukkan indeks tweet yang ingin ditampilkan", min_value=1, max_value=len(df), value=1, step=1)
tweet_index -= 1
if st.button("Tampilkan Tweet"):
    tweet_url = df.iloc[tweet_index]['tweet_url']
    target_value = df.iloc[tweet_index]['target']
    st.code(tweet_url)
    tweet_html = f"<p style='background-color:black;color:white;text-align:center;'>Target: {target_value}</p><blockquote class='twitter-tweet' data-media-max-width='350' align='center' data-conversation='none' data-theme='dark'><a href='{tweet_url}'></a></blockquote><script async src='https://platform.twitter.com/widgets.js' charset='utf-8'></script>"
    components.html(tweet_html, height=600, scrolling=True)

# Membuat chart dari jumlah target
target_counts = df['target'].value_counts()

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
