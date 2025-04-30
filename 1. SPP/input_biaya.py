import streamlit as st
import pandas as pd
from datetime import datetime

# Simulasi data
biaya_kuliah_data = []
angsuran_data = []

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", [
    "Input Biaya Kuliah",
    "Input Pembayaran Angsuran",
    "Pencarian Pembayaran Angsuran",
    "Laporan Sudah Lunas",
    "Laporan Belum Lunas"
])

# 1. Input Biaya Kuliah
if menu == "Input Biaya Kuliah":
    st.title("Input Biaya Kuliah")
    program_studi = st.selectbox("Program Studi", ["Teknik Informatika", "Sistem Informasi"])
    nim = st.text_input("NIM")
    nama = st.text_input("Nama")
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100, value=2023)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])
    sks = st.number_input("Jumlah SKS", min_value=0, max_value=24)
    biaya = st.number_input("Biaya Kuliah", min_value=0)

    if st.button("Simpan"):
        biaya_kuliah_data.append({"NIM": nim, "Nama": nama, "Tahun": tahun, "Semester": semester, "Program Studi": program_studi, "SKS": sks, "Biaya": biaya})
        st.success("Data disimpan!")

    st.dataframe(pd.DataFrame(biaya_kuliah_data))

# 2. Input Pembayaran Angsuran
elif menu == "Input Pembayaran Angsuran":
    st.title("Input Pembayaran Angsuran")
    program_studi = st.selectbox("Program Studi", ["Teknik Informatika", "Sistem Informasi"])
    nim = st.text_input("NIM")
    nama = st.text_input("Nama")
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100, value=2023)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])
    angsuran_ke = st.number_input("Angsuran Ke", min_value=1, max_value=10)
    tanggal = st.date_input("Tanggal")
    bayar = st.number_input("Jumlah Bayar", min_value=0)

    if st.button("Simpan"):
        angsuran_data.append({"NIM": nim, "Nama": nama, "Tahun": tahun, "Semester": semester, "Program Studi": program_studi, "Angsuran Ke": angsuran_ke, "Tanggal": tanggal, "Bayar": bayar})
        st.success("Pembayaran dicatat!")

    st.dataframe(pd.DataFrame(angsuran_data))

# 3. Pencarian Pembayaran
elif menu == "Pencarian Pembayaran Angsuran":
    st.title("Pencarian Pembayaran Angsuran")
    program_studi = st.selectbox("Program Studi", ["Teknik Informatika", "Sistem Informasi"])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100, value=2023)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])
    pilih_pencarian = st.selectbox("Pilih Pencarian", ["Tanggal", "Bulan"])

    hasil = pd.DataFrame(angsuran_data)

    if pilih_pencarian == "Tanggal":
        tanggal = st.date_input("Tanggal")
        hasil = hasil[hasil["Tanggal"] == tanggal]
    else:
        bulan = st.selectbox("Bulan", list(range(1, 13)))
        hasil = hasil[pd.to_datetime(hasil["Tanggal"]).dt.month == bulan]

    st.dataframe(hasil)

# 4. Laporan Sudah Lunas
elif menu == "Laporan Sudah Lunas":
    st.title("Laporan Angsuran Sudah Lunas")
    program_studi = st.selectbox("Program Studi", ["Teknik Informatika", "Sistem Informasi"])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100, value=2023)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])

    df = pd.DataFrame(angsuran_data)
    df_lunas = df.groupby("NIM")["Bayar"].sum().reset_index()
    df_lunas = df_lunas[df_lunas["Bayar"] >= 5000000]  # Misal batas lunas
    st.dataframe(df_lunas)

# 5. Laporan Belum Lunas
elif menu == "Laporan Belum Lunas":
    st.title("Laporan Angsuran Belum Lunas")
    program_studi = st.selectbox("Program Studi", ["Teknik Informatika", "Sistem Informasi"])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100, value=2023)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])

    df = pd.DataFrame(angsuran_data)
    df_lunas = df.groupby("NIM")["Bayar"].sum().reset_index()
    df_belum_lunas = df_lunas[df_lunas["Bayar"] < 5000000]  # Misal batas lunas
    st.dataframe(df_belum_lunas)
