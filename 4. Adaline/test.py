import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- ADALINE Model ---
class Adaline:
    def __init__(self, learning_rate=0.1, n_iter=1000, tolerance=0.05):
        self.learning_rate = learning_rate
        self.n_iter = n_iter
        self.tolerance = tolerance
        self.history_ = []

    def fit(self, X, y):
        np.random.seed(1)  # Supaya hasil acakan tetap sama setiap jalan
        self.w_ = np.random.uniform(-0.5, 0.5, 1 + X.shape[1])  # Bobot random kecil
        self.cost_ = []

        for epoch in range(1, self.n_iter + 1):
            net_input = self.net_input(X)
            output = net_input
            errors = y - output
            self.w_[1:] += self.learning_rate * X.T.dot(errors)
            self.w_[0] += self.learning_rate * errors.sum()
            mse = (errors ** 2).mean()
            cost = 0.5 * mse
            self.cost_.append(cost)

            self.history_.append({
                'Epoch': epoch,
                'w1': self.w_[1],
                'w2': self.w_[2],
                'Bias': self.w_[0],
                'MSE': mse
            })

            if mse < self.tolerance:
                print(f"Training stopped at epoch {epoch} with MSE: {mse:.4f}")
                break

        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def activation(self, X):
        return self.net_input(X)

    def predict(self, X):
        return np.where(self.activation(X) >= 0.0, 1, -1)  # bipolar output

# --- Streamlit UI ---
st.title("PENGENALAN POLA FUNGSI LOGIKA XNOR MENGGUNAKAN MODEL ADALINE")

# Input X
st.subheader("Input Data Uji (Bipolar)")
col1, col2 = st.columns(2)
x1 = col1.selectbox("x1", options=[-1, 1])
x2 = col2.selectbox("x2", options=[-1, 1])

# Learning rate dan iterasi
learning_rate = st.number_input("Learning Rate (α)", value=0.10, step=0.01)
n_iter = st.number_input("Maksimum Iterasi", value=1000, step=10)

# Tombol Latih Model
if 'model' not in st.session_state:
    st.session_state.model = None
if 'history' not in st.session_state:
    st.session_state.history = None

if st.button("Latih Model ADALINE"):
    # Data training XNOR bipolar
    X_train = np.array([
        [-1, -1],
        [-1,  1],
        [ 1, -1],
        [ 1,  1]
    ])
    y_train = np.array([1, -1, -1, 1])  # Output XNOR bipolar

    adaline = Adaline(learning_rate=learning_rate, n_iter=n_iter, tolerance=0.05)
    adaline.fit(X_train, y_train)
    st.session_state.model = adaline
    st.session_state.history = adaline.history_

    st.success("Model telah dilatih!")

    # Tampilkan tabel history training
    st.subheader("Tabel Data Training per Epoch")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)

    # Tampilkan learning curve
    st.subheader("Learning Curve (MSE vs Epoch)")
    fig, ax = plt.subplots()
    ax.plot(history_df['Epoch'], history_df['MSE'], marker='o')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('MSE')
    ax.set_title('Learning Curve ADALINE')
    ax.grid(True)
    st.pyplot(fig)

# Tombol Prediksi
if st.button("Prediksi"):
    if st.session_state.model is not None:
        X_test = np.array([[x1, x2]])
        output = st.session_state.model.predict(X_test)

        st.subheader("Output Prediksi")
        st.write(int(output[0]))

        st.subheader("Bobot (w)")
        for idx, weight in enumerate(st.session_state.model.w_[1:], start=1):
            st.write(f"w{idx} = {weight:.4f}")

        st.subheader("Bias (b)")
        st.write(f"b = {st.session_state.model.w_[0]:.4f}")

        st.subheader("MSE Terakhir")
        mse = (2 * st.session_state.model.cost_[-1])
        st.write(f"{mse:.4f}")
    else:
        st.warning("Model belum dilatih. Silakan klik tombol 'Latih Model ADALINE' dulu.")
