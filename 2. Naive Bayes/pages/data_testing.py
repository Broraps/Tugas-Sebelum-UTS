import streamlit as st
import pandas as pd

# Load dataset dari file CSV saat pertama kali
if "data_testing" not in st.session_state:
    st.session_state.data_testing = pd.read_csv("pinjaman.csv")

st.title("🧾 Kelola Data Testing")

# # Tampilkan tabel data
# st.subheader("Tabel Data Training")
# st.dataframe(st.session_state.data_training, use_container_width=True)

# Form Input
with st.form("input_form"):
    st.subheader("Input Data Baru")
    col1, col2 = st.columns(2)

    with col1:
        Usia = st.text_input("Usia")
        Pendapatan = st.text_input("Pendapatan")
        Status_Perkawinan = st.selectbox("Status Perkawinan", ["Menikah", "Belum Menikah"])

    with col2:
        Jumlah_Pinjaman = st.text_input("Jumlah Pinjaman")
        Durasi_Pinjaman = st.text_input("Durasi Pinjaman")
        Status_Pekerjaan = st.selectbox("Jenis Pekerjaan", ["Karyawan Tetap", "Karywana Kontrak", "Wirausaha", "Pensiunan"])

    submit = st.form_submit_button("SIMPAN")

    if submit:
        new_row = {
            "Usia": Usia,
            "Pendapatan": Pendapatan,
            "Status_Perkawinan": Status_Perkawinan,
            "Jumlah_Pinjaman": Jumlah_Pinjaman,
            "Durasi_Pinjaman": Durasi_Pinjaman,
            "Status_Pekerjaan": Status_Pekerjaan,
        }
        st.session_state.data_testing = pd.concat(
            [st.session_state.data_testing, pd.DataFrame([new_row])],
            ignore_index=True
        )
        st.success("Data berhasil ditambahkan!")

# Pilih index untuk dihapus
st.subheader("Hapus Data Tertentu")

if not st.session_state.data_testing.empty:
    row_to_delete = st.selectbox(
        "Pilih baris yang ingin dihapus (berdasarkan index):",
        st.session_state.data_testing.index.tolist()
    )

    if st.button("HAPUS BARIS TERPILIH"):
        st.session_state.data_testing = st.session_state.data_testing.drop(row_to_delete).reset_index(drop=True)
        st.success(f"Baris ke-{row_to_delete} berhasil dihapus.")
else:
    st.info("Data masih kosong.")


# Tampilkan tabel data
st.subheader("Tabel Data Testing")
# Tampilkan Data Testing tanpa kolom Lulus_Kredit
st.dataframe(st.session_state.data_testing, use_container_width=True)
