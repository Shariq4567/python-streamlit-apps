import streamlit as st
from password_strength import PasswordStats
import random
import string


def check_password_strength(password):
    stats = PasswordStats(password)
    strength = stats.strength()
    return strength

def generate_strong_password(length=15):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.sample(characters, length))
    return password

st.title("Password Strength Checker")

if st.button("Generate Strong Password"):
    strong_password = generate_strong_password()
    st.text_input("Generated Strong Password", value=strong_password, type="password", key="generated_password")

password = st.text_input("Enter a password", type="password")

if password:
    strength = check_password_strength(password)
    st.write(f"Password strength: {strength:.2f}")

    if strength < 0.3:
        st.error("Weak password")
    elif strength < 0.6:
        st.warning("Moderate password")
    else:
        st.success("Strong password")