import streamlit as st
import pandas as pd
import joblib

st.title("🔍 Halaman Testing - Naive Bayes (Pilih Baris)")

# Load model
@st.cache_resource
def load_model():
    return joblib.load("naive_bayes_models.pkl")

model = load_model()

# Mapping kategori ke angka
mapping_status_perkawinan = {
    "Belum Menikah": 0,
    "Menikah": 1
}
mapping_status_pekerjaan = {
    "Karyawan Tetap": 0,
    "Karywana Kontrak": 1,
    "Wirausaha": 2,
    "Pensiunan": 3
}

# Cek apakah data_testing sudah ada
if "data_testing" not in st.session_state:
    st.error("Data Testing belum tersedia. Silakan input data terlebih dahulu di menu Data Testing.")
    st.stop()

# Tampilkan tabel data testing (tanpa kolom Lulus_Kredit)
st.subheader("Tabel Data Testing (Tanpa Lulus_Kredit)")
try:
    data_testing_tanpa_target = st.session_state.data_testing.drop(columns=["Lulus_Kredit"])
except KeyError:
    data_testing_tanpa_target = st.session_state.data_testing

st.dataframe(data_testing_tanpa_target, use_container_width=True)

# Pilih baris untuk testing
st.subheader("Pilih Baris untuk Testing")
if not data_testing_tanpa_target.empty:
    selected_index = st.selectbox(
        "Pilih Index Baris yang Mau Dites:",
        data_testing_tanpa_target.index.tolist()
    )

    if st.button("🔎 LAKUKAN TESTING BARIS TERPILIH"):
        # Ambil 1 baris berdasarkan index yang dipilih
        selected_row = data_testing_tanpa_target.loc[[selected_index]].copy()  # tetap dalam bentuk DataFrame

        # Mapping kolom yang perlu diubah
        selected_row["Status_Perkawinan"] = selected_row["Status_Perkawinan"].map(mapping_status_perkawinan)
        selected_row["Status_Pekerjaan"] = selected_row["Status_Pekerjaan"].map(mapping_status_pekerjaan)

            # Cek NaN
        if selected_row.isnull().any().any():
            st.error("Data yang dipilih memiliki nilai yang tidak valid setelah mapping.\nPeriksa kembali inputan Status_Perkawinan dan Status_Pekerjaan.")
            st.stop()

        # Prediksi
        prediction = model.predict(selected_row)[0]
        prediction_proba = model.predict_proba(selected_row)[0]

        st.subheader("Hasil Prediksi")
        st.write(f"**Prediksi:** {prediction}")
        st.write(f"**Probabilitas:**")
        st.write({
            "Layak": f"{round(prediction_proba[1]*100, 2)}%",
            "Tidak Layak": f"{round(prediction_proba[0]*100, 2)}%"
        })
        # --- Tambahkan Simpan ke Session State ---
        # Inisialisasi jika belum ada
        if "hasil_prediksi" not in st.session_state:
            st.session_state.hasil_prediksi = pd.DataFrame()

        # Ambil data original + tambahkan hasil prediksi
        new_result = data_testing_tanpa_target.loc[[selected_index]].copy()
        new_result["Hasil_Prediksi"] = prediction

        # Simpan ke hasil_prediksi
        st.session_state.hasil_prediksi = pd.concat(
            [st.session_state.hasil_prediksi, new_result],
            ignore_index=True
        )

        st.success(f"✅ Hasil prediksi untuk baris {selected_index} berhasil disimpan!")

