import streamlit as st
import pandas as pd
import joblib

st.title("📊 Menu Klasifikasi - Hasil Prediksi Naive Bayes")

# Cek apakah ada hasil prediksi
if "hasil_prediksi" not in st.session_state or st.session_state.hasil_prediksi.empty:
    st.warning("Belum ada hasil prediksi yang tersedia. Silakan lakukan testing dulu.")
    st.stop()

hasil_prediksi = st.session_state.hasil_prediksi

st.subheader("📑 Data Testing + Hasil Prediksi")
st.dataframe(hasil_prediksi, use_container_width=True)

# Kalau mau menghitung akurasi:
if "Lulus_Kredit" in hasil_prediksi.columns:
    y_true = hasil_prediksi["Lulus_Kredit"]
    y_pred = hasil_prediksi["Hasil_Prediksi"]

    total_data = len(y_true)
    jumlah_tepat = (y_true == y_pred).sum()
    jumlah_tidak_tepat = total_data - jumlah_tepat
    akurasi = (jumlah_tepat / total_data) * 100

    st.subheader("📊 Hasil Evaluasi Akurasi")
    st.metric("Jumlah Data", total_data)
    st.metric("Klasifikasi Tepat", jumlah_tepat)
    st.metric("Klasifikasi Tidak Tepat", jumlah_tidak_tepat)
    st.metric("Akurasi (%)", f"{akurasi:.2f}%")
