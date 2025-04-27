import streamlit as st

def rle_encode(text):
    if not text:
        return ""
    encoded = ""
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i - 1]:
            count += 1
        else:
            encoded += str(count) + text[i - 1]
            count = 1
    encoded += str(count) + text[-1]
    return encoded

def rle_decode(encoded_text):
    if not encoded_text:
        return ""
    decoded = ""
    count = ""
    for char in encoded_text:
        if char.isdigit():
            count += char
        else:
            decoded += char * int(count)
            count = ""
    return decoded

# UI
st.title("📦 RLE Text Compressor & Decompressor")
st.write("Kompress atau decompress file `.txt` menggunakan Run-Length Encoding.")

# Upload
uploaded_file = st.file_uploader("Unggah file .txt", type=["txt"])
action = st.radio("Pilih aksi:", ("Encode", "Decode"))

if uploaded_file is not None:
    # Baca isi file
    text = uploaded_file.read().decode("utf-8")
    st.text_area("📄 Isi File:", text, height=200)

    # Proses
    if action == "Encode":
        result = rle_encode(text)
    else:
        result = rle_decode(text)

    # Tampilkan hasil
    st.subheader("📤 Hasil:")
    st.text_area("Output:", result, height=200)

    # Tombol download
    st.download_button(
        label="💾 Download hasil sebagai file .txt",
        data=result,
        file_name=f"rle_{action.lower()}d.txt",
        mime="text/plain"
    )
