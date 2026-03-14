import streamlit as st
from services.database import DatabaseService
from utils.conversions import convert_height_to_cm, convert_weight_to_kg, convert_temperature_to_celsius, calculate_bmi
from utils.health_rules import classify_bmi, classify_blood_sugar, classify_blood_pressure, classify_spo2, classify_temperature, get_health_advice

def show_tests_page():
    if st.session_state.guest_mode:
        st.markdown('<h1 class="main-title">Quick Health Check</h1>', unsafe_allow_html=True)
        st.info("🔍 Guest Mode: Results will not be saved")
    else:
        if not st.session_state.user:
            st.session_state.page = 'login'
            st.rerun()
            return
        
        st.markdown('<h1 class="main-title">Health Tests</h1>', unsafe_allow_html=True)
        st.success(f"👋 Welcome, {st.session_state.user['full_name']}!")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back to Home", key="back_home"):
            st.session_state.page = 'landing'
            st.rerun()
    
    if not st.session_state.guest_mode:
        with col3:
            if st.button("📊 View Dashboard", key="dashboard"):
                st.session_state.page = 'dashboard'
                st.rerun()
    
    st.markdown("---")
    
    # Initialize selected test in session state
    if 'selected_test' not in st.session_state:
        st.session_state.selected_test = None
    
    # Test selection
    st.markdown("### Choose a Health Test")
    
    # Create test buttons in a grid
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📏 BMI Test", key="bmi_test", use_container_width=True):
            st.session_state.selected_test = "bmi"
        
        if st.button("🩸 Blood Sugar", key="sugar_test", use_container_width=True):
            st.session_state.selected_test = "sugar"
        
        if st.button("🌡️ Temperature", key="temp_test", use_container_width=True):
            st.session_state.selected_test = "temperature"
    
    with col2:
        if st.button("💓 Blood Pressure", key="bp_test", use_container_width=True):
            st.session_state.selected_test = "bp"
        
        if st.button("🫁 SpO2 & Pulse", key="spo2_test", use_container_width=True):
            st.session_state.selected_test = "spo2"
    
    # Show selected test
    if st.session_state.selected_test == "bmi":
        show_bmi_test()
    elif st.session_state.selected_test == "sugar":
        show_blood_sugar_test()
    elif st.session_state.selected_test == "temperature":
        show_temperature_test()
    elif st.session_state.selected_test == "bp":
        show_blood_pressure_test()
    elif st.session_state.selected_test == "spo2":
        show_spo2_test()

def show_bmi_test():
    st.markdown("### BMI Test")
    
    # Get user's current measurements if logged in
    current_height = None
    current_weight = None
    
    if not st.session_state.guest_mode and st.session_state.user:
        current_height = st.session_state.user.get('height_cm')
        current_weight = st.session_state.user.get('weight_kg')
    
    with st.form("bmi_form"):
        # Height input
        col1, col2 = st.columns([2, 1])
        with col1:
            height_value = st.number_input(
                "Height", 
                min_value=0.1, 
                value=float(current_height) if current_height else 170.0,
                step=0.1
            )
        with col2:
            height_unit = st.selectbox("Unit", ["cm", "m", "ft", "inch"], key="bmi_height_unit")
        
        # Weight input
        col3, col4 = st.columns([2, 1])
        with col3:
            weight_value = st.number_input(
                "Weight", 
                min_value=0.1, 
                value=float(current_weight) if current_weight else 70.0,
                step=0.1
            )
        with col4:
            weight_unit = st.selectbox("Unit", ["kg", "lbs"], key="bmi_weight_unit")
        
        calculate_btn = st.form_submit_button("Calculate BMI", use_container_width=True)
    
    if calculate_btn:
        try:
            # Convert to standard units
            height_cm = convert_height_to_cm(height_value, height_unit)
            weight_kg = convert_weight_to_kg(weight_value, weight_unit)
            
            # Calculate BMI
            bmi = calculate_bmi(weight_kg, height_cm)
            status, color_class = classify_bmi(bmi)
            
            # Display result
            st.markdown(f'<div class="health-result {color_class}">BMI: {bmi:.1f}<br>{status}</div>', unsafe_allow_html=True)
            
            # Show advice
            advice = get_health_advice("BMI", status)
            st.info(f"💡 {advice}")
            
            # Save result if logged in (with error handling)
            if not st.session_state.guest_mode and st.session_state.user:
                try:
                    save_test_result("Weight", weight_kg, None, status)
                    
                    # Update user's measurements if they changed
                    db = DatabaseService()
                    if height_cm != current_height or weight_kg != current_weight:
                        db.update_user_measurements(st.session_state.user['user_id'], height_cm, weight_kg)
                        st.session_state.user['height_cm'] = height_cm
                        st.session_state.user['weight_kg'] = weight_kg
                        st.success("✅ BMI calculated and measurements updated!")
                    else:
                        st.success("✅ BMI calculated and saved!")
                except Exception as e:
                    st.warning("⚠️ BMI calculated successfully, but couldn't save to database. Results shown above.")
                    st.error(f"Database error: {e}")
            else:
                st.success("✅ BMI calculated successfully!")
            
        except ValueError as e:
            st.error(f"Error: {e}")

def show_blood_sugar_test():
    st.markdown("### Blood Sugar Test")
    
    with st.form("sugar_form"):
        glucose = st.number_input("Blood Sugar (mg/dL)", min_value=1.0, value=100.0, step=1.0)
        test_btn = st.form_submit_button("Check Blood Sugar", use_container_width=True)
    
    if test_btn:
        status, color_class = classify_blood_sugar(glucose)
        
        # Display result
        st.markdown(f'<div class="health-result {color_class}">{glucose:.0f} mg/dL<br>{status}</div>', unsafe_allow_html=True)
        
        # Show advice
        advice = get_health_advice("Sugar", status)
        st.info(f"💡 {advice}")
        
        # Save result if logged in (with error handling)
        if not st.session_state.guest_mode and st.session_state.user:
            try:
                save_test_result("Sugar", glucose, None, status)
                st.success("✅ Blood sugar reading saved!")
            except Exception as e:
                st.warning("⚠️ Blood sugar checked successfully, but couldn't save to database. Results shown above.")
        else:
            st.success("✅ Blood sugar checked successfully!")

def show_blood_pressure_test():
    st.markdown("### Blood Pressure Test")
    
    with st.form("bp_form"):
        col1, col2 = st.columns(2)
        with col1:
            systolic = st.number_input("Systolic (top number)", min_value=50, max_value=300, value=120, step=1)
        with col2:
            diastolic = st.number_input("Diastolic (bottom number)", min_value=30, max_value=200, value=80, step=1)
        
        test_btn = st.form_submit_button("Check Blood Pressure", use_container_width=True)
    
    if test_btn:
        status, color_class = classify_blood_pressure(systolic, diastolic)
        
        # Display result
        st.markdown(f'<div class="health-result {color_class}">{systolic}/{diastolic} mmHg<br>{status}</div>', unsafe_allow_html=True)
        
        # Show advice
        advice = get_health_advice("Blood Pressure", status)
        st.info(f"💡 {advice}")
        
        # Save result if logged in (with error handling)
        if not st.session_state.guest_mode and st.session_state.user:
            try:
                save_test_result("Blood Pressure", systolic, diastolic, status)
                st.success("✅ Blood pressure reading saved!")
            except Exception as e:
                st.warning("⚠️ Blood pressure checked successfully, but couldn't save to database. Results shown above.")
        else:
            st.success("✅ Blood pressure checked successfully!")

def show_spo2_test():
    st.markdown("### SpO2 & Pulse Test")
    
    with st.form("spo2_form"):
        col1, col2 = st.columns(2)
        with col1:
            spo2 = st.number_input("SpO2 (%)", min_value=70.0, max_value=100.0, value=98.0, step=0.1)
        with col2:
            pulse = st.number_input("Pulse (BPM)", min_value=30, max_value=200, value=72, step=1)
        
        test_btn = st.form_submit_button("Check SpO2 & Pulse", use_container_width=True)
    
    if test_btn:
        status, color_class = classify_spo2(spo2, pulse)
        
        # Display result
        st.markdown(f'<div class="health-result {color_class}">SpO2: {spo2:.1f}%<br>Pulse: {pulse} BPM<br>{status}</div>', unsafe_allow_html=True)
        
        # Show advice
        advice = get_health_advice("SpO2", status)
        st.info(f"💡 {advice}")
        
        # Save result if logged in (with error handling)
        if not st.session_state.guest_mode and st.session_state.user:
            try:
                save_test_result("SpO2", spo2, pulse, status)
                st.success("✅ SpO2 and pulse readings saved!")
            except Exception as e:
                st.warning("⚠️ SpO2 and pulse checked successfully, but couldn't save to database. Results shown above.")
        else:
            st.success("✅ SpO2 and pulse checked successfully!")

def show_temperature_test():
    st.markdown("### Temperature Test")
    
    with st.form("temp_form"):
        col1, col2 = st.columns([2, 1])
        with col1:
            temp_value = st.number_input("Temperature", min_value=30.0, max_value=45.0, value=37.0, step=0.1)
        with col2:
            temp_unit = st.selectbox("Unit", ["Celsius", "Fahrenheit"], key="temp_unit")
        
        test_btn = st.form_submit_button("Check Temperature", use_container_width=True)
    
    if test_btn:
        # Convert to Celsius for classification
        temp_celsius = convert_temperature_to_celsius(temp_value, temp_unit)
        status, color_class = classify_temperature(temp_celsius)
        
        # Display result
        display_temp = f"{temp_value:.1f}°{temp_unit[0]}"
        st.markdown(f'<div class="health-result {color_class}">{display_temp}<br>{status}</div>', unsafe_allow_html=True)
        
        # Show advice
        advice = get_health_advice("Temperature", status)
        st.info(f"💡 {advice}")
        
        # Save result if logged in (with error handling)
        if not st.session_state.guest_mode and st.session_state.user:
            try:
                save_test_result("Temperature", temp_celsius, None, status)
                st.success("✅ Temperature reading saved!")
            except Exception as e:
                st.warning("⚠️ Temperature checked successfully, but couldn't save to database. Results shown above.")
        else:
            st.success("✅ Temperature checked successfully!")

def save_test_result(test_type: str, value_1: float, value_2: float, status: str):
    """Save test result to database"""
    try:
        db = DatabaseService()
        user_id = st.session_state.user['user_id']
        
        # Get or create today's session
        session_id = db.get_latest_session_for_user(user_id)
        if not session_id:
            session_id = db.create_test_session(user_id)
        
        # Save the test result
        db.save_test_result(session_id, test_type, value_1, value_2, status)
        
    except Exception as e:
        st.error(f"Failed to save result: {e}")