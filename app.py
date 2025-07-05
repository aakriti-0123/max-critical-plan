import streamlit as st
import pandas as pd

st.set_page_config(page_title="MAX Critical Plan", layout="wide")

# ----------------------------
# Utility functions
# ----------------------------

def clean_calendar(df):
    # Convert datetime columns to just dates, and blank out NaT/empty
    df = df.copy()
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x.date() if pd.notnull(x) and isinstance(x, pd.Timestamp) else (x if pd.notnull(x) else ""))
    return df

def load_dropdown_options(path):
    df = pd.read_excel(path)
    dropdown_dict = {}
    current_key = None
    for _, row in df.iterrows():
        if pd.notna(row['Selections']):
            current_key = row['Selections']
            dropdown_dict[current_key] = []
        if current_key and pd.notna(row['Dropdowns']):
            dropdown_dict[current_key].append(row['Dropdowns'])
    return dropdown_dict

# ----------------------------
# Session State for Navigation
# ----------------------------

if 'page' not in st.session_state:
    st.session_state.page = "upload"

# ----------------------------
# Page: Upload & Selection
# ----------------------------

if st.session_state.page == "upload":
    st.markdown("## 🗂️ MAX Critical Plan – Selection Hub")

    st.markdown("Upload up to 4 seasonal calendar Excel files. These will be used as your source calendars.")

    uploaded_files = st.file_uploader("Upload Calendar Files", accept_multiple_files=True, type=["xlsx"])
    dropdown_file = st.file_uploader("Upload Dropdown Sheet", type=["xlsx"], help="This is 'Selections and dropdowns.xlsx'")

    if uploaded_files and dropdown_file:
        st.success("✅ All files uploaded. Now configure your view options below.")
        dropdowns = load_dropdown_options(dropdown_file)

        # Store calendars in session
        st.session_state.calendars = {}
        for f in uploaded_files:
            xls = pd.ExcelFile(f, engine="openpyxl")
            for sheet in xls.sheet_names:
                df = pd.read_excel(f, sheet_name=sheet, engine="openpyxl")
                st.session_state.calendars[f.name + " - " + sheet] = df

        # Render dropdowns
        st.markdown("---")
        st.markdown("### 🔽 Select View Parameters")
        st.session_state.user_selections = {}
        for key, options in dropdowns.items():
            st.session_state.user_selections[key] = st.selectbox(key, options)

        if st.button("View Calendar ➡️"):
            st.session_state.page = "calendar"
            st.rerun()

    else:
        st.warning("Please upload both calendar files and the dropdowns file.")

# ----------------------------
# Page: Calendar View
# ----------------------------

elif st.session_state.page == "calendar":
    st.markdown("## 🗓️ MAX Critical Plan – Calendar View")
    st.markdown("Use the button below to return to the selection page.")
    if st.button("⬅️ Back to Selections"):
        st.session_state.page = "upload"
        st.rerun()

    if 'calendars' in st.session_state:
        for name, df in st.session_state.calendars.items():
            st.markdown(f"### 📁 {name}")
            cleaned_df = clean_calendar(df)
            st.dataframe(cleaned_df, use_container_width=True)
    else:
        st.error("No calendar files loaded. Please go back and upload them.")
