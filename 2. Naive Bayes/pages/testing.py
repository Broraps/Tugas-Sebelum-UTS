import streamlit as st
import pandas as pd
import joblib

st.title("🔍 Halaman Testing - Naive Bayes")

# Load model
@st.cache_resource
def load_model():
    return joblib.load("naive_bayes_model.pkl")

model = load_model()

# Form input untuk data baru
with st.form("form_testing"):
    st.subheader("Input Data Testing")
    col1, col2 = st.columns(2)

    with col1:
        pekerjaan = st.selectbox("Jenis Pekerjaan", ["KARYAWAN SWASTA", "WIRAUSAHA", "BURUH HARIAN LEPAS", "PETANI", "PETERNAK"])
        pendapatan = st.selectbox("Pendapatan", ["<200000", "200000-5000000", ">5000000"])
        usia = st.selectbox("Usia", ["21-35", "36-50", "51-65"])

    with col2:
        jumlah_kredit = st.selectbox("Jumlah Kredit", ["<1000000", "1000000-3000000", "3000000-6000000"])
        jangka_waktu = st.selectbox("Jangka Waktu", ["11 MINGGU", "12 BULAN"])
        nilai_jaminan = st.selectbox("Nilai Jaminan", ["<100000", "300000-600000"])

    submitted = st.form_submit_button("TESTING")

    if submitted:
        # Buat data input sebagai dataframe
        new_data = pd.DataFrame([{
            "Pekerjaan": pekerjaan,
            "Pendapatan": pendapatan,
            "Usia": usia,
            "Jumlah_Kredit": jumlah_kredit,
            "Jangka_Waktu": jangka_waktu,
            "Nilai_Jaminan": nilai_jaminan
        }])

        # Preprocessing (pastikan sama seperti waktu training)
        # Misal kamu sudah pakai encoder sebelumnya, load juga
        # encoder = joblib.load("encoder.pkl")
        # new_data_encoded = encoder.transform(new_data)

        prediction = model.predict(new_data)[0]
        prediction_proba = model.predict_proba(new_data)[0]

        st.success(f"Hasil Prediksi: **{prediction}**")
        st.write(f"Persentase:")
        st.write({
            "Layak": f"{round(prediction_proba[1]*100, 2)}%",
            "Tidak Layak": f"{round(prediction_proba[0]*100, 2)}%"
        })
