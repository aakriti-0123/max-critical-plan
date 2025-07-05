import streamlit as st
import pandas as pd
import os

# ---- CONFIG ----
st.set_page_config(page_title="MAX Critical Plan", layout="wide")

# ---- STYLING ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #fbeaea;
    }

    .stApp {
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/0/0e/Max_Fashion_Logo.png");
        background-repeat: no-repeat;
        background-position: top right;
        background-size: 120px;
    }
    </style>
""", unsafe_allow_html=True)

# ---- USER CONTROL ----
ADMIN_USERNAME = "aakriti-0123"
CURRENT_USER = "aakriti-0123"  # Replace with login logic if needed

# ---- FILE PATHS ----
uploaded_files = {
    "SS26": "SS26 Upload 1.xlsx",
    "WN25": "WN25 Upload.xlsx",
    "WN26": "WN26 Upload 1.xlsx"
}

# ---- SIDEBAR NAVIGATION ----
page = st.sidebar.radio("🧭 Navigate", ["📤 Upload Calendar (Admin Only)", "📅 View Calendar"])

# ---- UPLOAD PAGE ----
if page == "📤 Upload Calendar (Admin Only)":
    if CURRENT_USER == ADMIN_USERNAME:
        st.title("📤 Upload Seasonal Calendars")
        st.markdown("Admins can upload up to 4 seasonal Excel files.")
        uploads = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)
        if uploads:
            for file in uploads:
                with open(file.name, "wb") as f:
                    f.write(file.getbuffer())
            st.success(f"Uploaded {len(uploads)} file(s).")
    else:
        st.error("⛔ You do not have permission to view this page.")

# ---- VIEW CALENDAR PAGE ----
elif page == "📅 View Calendar":
    st.title("📅 MAX Critical Plan Viewer")

    col1, col2, col3 = st.columns(3)
    with col1:
        season = st.selectbox("Select Season", list(uploaded_files.keys()))
    with col2:
        launch_type = st.selectbox("Select Launch Type", ["REGULAR CP", "EXPRESS CP"])
    with col3:
        duration = st.selectbox("Select Duration", ["90D", "120D"])

    st.markdown(f"### 📂 Showing: **{season} | {launch_type} | {duration}**")

    # Load selected calendar
    file_path = uploaded_files.get(season)
    if file_path and os.path.exists(file_path):
        df = pd.read_excel(file_path, header=None)

        # Clean display: remove NaT/time portion if present
        df = df.applymap(lambda x: x.strftime('%Y-%m-%d') if pd.api.types.is_datetime64_any_dtype(type(x)) else x)
        df.replace("NaT", "", inplace=True)

        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No calendar found for the selected season. Please upload it from the admin panel.")
