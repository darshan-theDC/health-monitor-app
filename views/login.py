import streamlit as st
from services.auth import AuthService
from utils.conversions import convert_height_to_cm, convert_weight_to_kg

def show_login_page():
    st.markdown('<h1 class="main-title">Login & Save History</h1>', unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Home", key="back_home"):
        st.session_state.page = 'landing'
        st.rerun()
    
    st.markdown("---")
    
    # Check if database is available
    try:
        auth_service = AuthService()
        database_available = True
    except Exception as e:
        database_available = False
        st.error("⚠️ Database connection issue. You can still use the app in guest mode!")
        st.info("Click 'Back to Home' and use 'Check Health Now' for instant results without saving.")
        st.error(f"Technical details: {e}")
        return
    
    # Login form
    with st.form("login_form"):
        st.markdown("### Enter Your Information")
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        login_submitted = st.form_submit_button("Continue", use_container_width=True)
    
    if login_submitted and email and password:
        try:
            # Try to login
            user = auth_service.login(email, password)
            
            if user:
                # Login successful
                st.session_state.user = user
                st.session_state.page = 'tests'
                st.success("Login successful!")
                st.rerun()
            else:
                # Check if user exists
                if auth_service.user_exists(email):
                    st.error("Incorrect password. Please try again.")
                else:
                    # New user - show signup form
                    st.info("Email not found. Let's create your account!")
                    show_signup_form(email, password, auth_service)
        except Exception as e:
            st.error("⚠️ Login failed due to database issues. Please try guest mode instead.")
            st.error(f"Technical details: {e}")

def show_signup_form(email: str, password: str, auth_service: AuthService):
    st.markdown("### Create Your Account")
    
    with st.form("signup_form"):
        st.markdown("**Required Information:**")
        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        age = st.number_input("Age", min_value=1, max_value=120, value=50)
        gender = st.selectbox("Gender", ["Male", "Female"])
        
        st.markdown("**Optional Information:**")
        st.markdown("*You can skip these if you don't know or prefer not to share*")
        
        # Height input
        col1, col2 = st.columns([2, 1])
        with col1:
            height_value = st.number_input("Height (optional)", min_value=0.0, value=0.0, step=0.1)
        with col2:
            height_unit = st.selectbox("Unit", ["Don't know", "cm", "m", "ft", "inch"], key="height_unit")
        
        # Weight input
        col3, col4 = st.columns([2, 1])
        with col3:
            weight_value = st.number_input("Weight (optional)", min_value=0.0, value=0.0, step=0.1)
        with col4:
            weight_unit = st.selectbox("Unit", ["Don't know", "kg", "lbs"], key="weight_unit")
        
        signup_submitted = st.form_submit_button("Create Account & Continue", use_container_width=True)
    
    if signup_submitted and full_name:
        # Convert measurements if provided
        height_cm = None
        weight_kg = None
        
        if height_value > 0 and height_unit != "Don't know":
            try:
                height_cm = convert_height_to_cm(height_value, height_unit)
            except ValueError:
                st.error("Invalid height unit")
                return
        
        if weight_value > 0 and weight_unit != "Don't know":
            try:
                weight_kg = convert_weight_to_kg(weight_value, weight_unit)
            except ValueError:
                st.error("Invalid weight unit")
                return
        
        # Create user account
        try:
            user = auth_service.register(
                email=email,
                password=password,
                full_name=full_name,
                age=age,
                gender=gender,
                height_cm=height_cm,
                weight_kg=weight_kg
            )
            
            if user:
                st.session_state.user = user
                st.session_state.page = 'tests'
                st.success("Account created successfully!")
                st.rerun()
            else:
                st.error("Failed to create account. Please try again.")
        except Exception as e:
            st.error("⚠️ Account creation failed due to database issues. Please try guest mode instead.")
            st.error(f"Technical details: {e}")