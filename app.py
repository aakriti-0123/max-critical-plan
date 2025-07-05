import streamlit as st
from utils import authenticate_user

st.set_page_config(page_title="MAX Critical Plan", layout="wide")

# Sidebar Navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["📤 Upload Calendar", "🎯 Make Selection", "📅 View Calendar"])

if page == "📤 Upload Calendar":
    if authenticate_user("aakriti-0123"):
        from pages.upload import render_upload_page
        render_upload_page()
    else:
        st.error("You are not authorized to upload calendars.")

elif page == "🎯 Make Selection":
    from pages.selection import render_selection_page
    render_selection_page()

elif page == "📅 View Calendar":
    from pages.calendar import render_calendar_page
    render_calendar_page()