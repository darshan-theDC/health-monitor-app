import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Import views AFTER loading environment variables
from views.landing import show_landing_page
from views.login import show_login_page
from views.tests import show_tests_page
from views.dashboard import show_dashboard_page

def main():
    st.set_page_config(
        page_title="Health Monitor for Parents",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for large text and mobile-friendly design
    st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .big-button {
        font-size: 1.5rem !important;
        padding: 1rem 2rem !important;
        margin: 0.5rem 0 !important;
        width: 100% !important;
        height: 80px !important;
    }
    .health-result {
        font-size: 2rem !important;
        font-weight: bold;
        text-align: center;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .result-normal { background-color: #d4edda; color: #155724; }
    .result-low { background-color: #cce7ff; color: #004085; }
    .result-high { background-color: #f8d7da; color: #721c24; }
    .kannada-text {
        font-family: 'Noto Sans Kannada', 'Tunga', 'Kedage', Arial, sans-serif !important;
        font-size: 1.1em !important;
        line-height: 1.6 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'guest_mode' not in st.session_state:
        st.session_state.guest_mode = False
    
    # Navigation logic
    if st.session_state.page == 'landing':
        show_landing_page()
    elif st.session_state.page == 'login':
        show_login_page()
    elif st.session_state.page == 'tests':
        show_tests_page()
    elif st.session_state.page == 'dashboard':
        show_dashboard_page()

if __name__ == "__main__":
    main()