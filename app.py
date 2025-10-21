import streamlit as st

# ======================
# Conversion Logic
# ======================
def convert_temperature(value, from_unit, to_unit):
    if from_unit == "C":
        celsius = value
    elif from_unit == "F":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "K":
        celsius = value - 273.15
    else:
        return "Invalid"

    if to_unit == "C":
        return celsius
    elif to_unit == "F":
        return (celsius * 9 / 5) + 32
    elif to_unit == "K":
        return celsius + 273.15

# ======================
# Dark/Light Mode Setup
# ======================
def set_theme():
    if st.session_state.get("dark_mode", False):
        st.markdown(
            """
            <style>
            .reportview-container {background-color: #121212; color: #E0E0E0;}
            .stTextInput>div>div>input {background-color: #1E1E1E; color: #E0E0E0;}
            .stSelectbox>div>div>div>span {color: #E0E0E0;}
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            .reportview-container {background-color: #F5F5F5; color: #202020;}
            .stTextInput>div>div>input {background-color: #FFFFFF; color: #202020;}
            .stSelectbox>div>div>div>span {color: #202020;}
            </style>
            """,
            unsafe_allow_html=True,
        )

# ======================
# App Title
# ======================
st.set_page_config(page_title="🌡 Smart Temperature Converter", page_icon="🌡")
st.title("🌡 Smart Temperature Converter")
st.write("Type a value with its unit (C/F/K) and select the target unit. Live conversion updates instantly!")

# ======================
# Session State
# ======================
if "history" not in st.session_state:
    st.session_state.history = []

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ======================
# Dark/Light Toggle Button
# ======================
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode
    set_theme()

st.button("🌙 Dark Mode / ☀️ Light Mode", on_click=toggle_theme)

set_theme()  # Apply initial theme

# ======================
# Input & Live Conversion
# ======================
temp_input = st.text_input("Enter Temperature (e.g., 100C, 32F, 273K):")
target_unit = st.selectbox("Convert To:", ["C", "F", "K"])

if temp_input:
    try:
        temp_str = temp_input.strip().upper()
        if temp_str.endswith("C"):
            value, from_unit = float(temp_str[:-1]), "C"
        elif temp_str.endswith("F"):
            value, from_unit = float(temp_str[:-1]), "F"
        elif temp_str.endswith("K"):
            value, from_unit = float(temp_str[:-1]), "K"
        else:
            st.error("⚠ Please add a valid unit (C, F, or K).")
            st.stop()

        result = convert_temperature(value, from_unit, target_unit)
        st.success(f"✅ {value}°{from_unit} = {result:.2f}°{target_unit}")

        # Add to history
        st.session_state.history.append(f"{value}°{from_unit} → {result:.2f}°{target_unit}")

    except Exception as e:
        st.error(f"⚠ Error: {e}")

# ======================
# Conversion History Display
# ======================
if st.session_state.history:
    st.subheader("Conversion History")
    for item in reversed(st.session_state.history[-10:]):  # Show last 10 conversions
        st.write(item)
