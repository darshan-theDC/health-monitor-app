import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from services.database import DatabaseService
from services.report_generator import ReportGenerator
from utils.conversions import calculate_bmi
from utils.health_rules import get_bmi_color_for_chart

def show_dashboard_page():
    if not st.session_state.user:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    st.markdown('<h1 class="main-title">Health Dashboard</h1>', unsafe_allow_html=True)
    st.success(f"📊 {st.session_state.user['full_name']}'s Health History")
    
    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Tests", key="back_tests"):
            st.session_state.page = 'tests'
            st.rerun()
    with col2:
        if st.button("🏠 Home", key="home"):
            st.session_state.page = 'landing'
            st.rerun()
    
    st.markdown("---")
    
    # Get user's test history
    db = DatabaseService()
    user_id = st.session_state.user['user_id']
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📈 Health Graphs", "📄 Download Reports"])
    
    with tab1:
        show_health_graphs(db, user_id)
    
    with tab2:
        show_download_reports(db, user_id)

def show_health_graphs(db: DatabaseService, user_id: str):
    st.markdown("### Your Health Trends")
    
    # Weight/BMI History
    weight_data = db.get_user_test_history(user_id, "Weight")
    if weight_data:
        st.markdown("#### Weight & BMI History")
        
        # Prepare data for plotting
        dates = []
        weights = []
        bmis = []
        colors = []
        
        user_height = st.session_state.user.get('height_cm')
        
        for record in reversed(weight_data):  # Reverse to show chronological order
            session_date = record['test_sessions']['session_date']
            weight = record['value_1']
            
            dates.append(session_date)
            weights.append(weight)
            
            if user_height:
                bmi = calculate_bmi(weight, user_height)
                bmis.append(bmi)
                colors.append(get_bmi_color_for_chart(bmi))
            else:
                bmis.append(None)
                colors.append('gray')
        
        # Create weight chart
        fig_weight = go.Figure()
        fig_weight.add_trace(go.Scatter(
            x=dates, y=weights,
            mode='lines+markers',
            name='Weight (kg)',
            line=dict(color='blue', width=3),
            marker=dict(size=8)
        ))
        fig_weight.update_layout(
            title="Weight Over Time",
            xaxis_title="Date",
            yaxis_title="Weight (kg)",
            height=400
        )
        st.plotly_chart(fig_weight, use_container_width=True)
        
        # Create BMI chart if height is available
        if user_height and bmis and any(b is not None for b in bmis):
            fig_bmi = go.Figure()
            fig_bmi.add_trace(go.Bar(
                x=dates, y=bmis,
                marker_color=colors,
                name='BMI'
            ))
            fig_bmi.update_layout(
                title="BMI Over Time (Color-coded: Blue=Low, Green=Normal, Red=High)",
                xaxis_title="Date",
                yaxis_title="BMI",
                height=400
            )
            st.plotly_chart(fig_bmi, use_container_width=True)
    else:
        st.info("No weight data available yet. Take a BMI test to see your weight trends!")
    
    # Blood Sugar History
    sugar_data = db.get_user_test_history(user_id, "Sugar")
    if sugar_data:
        st.markdown("#### Blood Sugar History")
        
        dates = [record['test_sessions']['session_date'] for record in reversed(sugar_data)]
        values = [record['value_1'] for record in reversed(sugar_data)]
        
        fig_sugar = go.Figure()
        fig_sugar.add_trace(go.Scatter(
            x=dates, y=values,
            mode='lines+markers',
            name='Blood Sugar (mg/dL)',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        
        # Add reference lines
        fig_sugar.add_hline(y=70, line_dash="dash", line_color="blue", annotation_text="Low threshold")
        fig_sugar.add_hline(y=140, line_dash="dash", line_color="orange", annotation_text="High threshold")
        
        fig_sugar.update_layout(
            title="Blood Sugar Over Time",
            xaxis_title="Date",
            yaxis_title="Blood Sugar (mg/dL)",
            height=400
        )
        st.plotly_chart(fig_sugar, use_container_width=True)
    else:
        st.info("No blood sugar data available yet. Take a blood sugar test to see your trends!")
    
    # Blood Pressure History
    bp_data = db.get_user_test_history(user_id, "Blood Pressure")
    if bp_data:
        st.markdown("#### Blood Pressure History")
        
        dates = [record['test_sessions']['session_date'] for record in reversed(bp_data)]
        systolic = [record['value_1'] for record in reversed(bp_data)]
        diastolic = [record['value_2'] for record in reversed(bp_data)]
        
        fig_bp = go.Figure()
        fig_bp.add_trace(go.Scatter(
            x=dates, y=systolic,
            mode='lines+markers',
            name='Systolic',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        fig_bp.add_trace(go.Scatter(
            x=dates, y=diastolic,
            mode='lines+markers',
            name='Diastolic',
            line=dict(color='blue', width=3),
            marker=dict(size=8)
        ))
        
        fig_bp.update_layout(
            title="Blood Pressure Over Time",
            xaxis_title="Date",
            yaxis_title="Blood Pressure (mmHg)",
            height=400
        )
        st.plotly_chart(fig_bp, use_container_width=True)
    else:
        st.info("No blood pressure data available yet. Take a blood pressure test to see your trends!")
    
    # SpO2 History
    spo2_data = db.get_user_test_history(user_id, "SpO2")
    if spo2_data:
        st.markdown("#### SpO2 & Pulse History")
        
        dates = [record['test_sessions']['session_date'] for record in reversed(spo2_data)]
        spo2_values = [record['value_1'] for record in reversed(spo2_data)]
        pulse_values = [record['value_2'] for record in reversed(spo2_data)]
        
        # Create subplot with secondary y-axis
        fig_spo2 = go.Figure()
        fig_spo2.add_trace(go.Scatter(
            x=dates, y=spo2_values,
            mode='lines+markers',
            name='SpO2 (%)',
            line=dict(color='green', width=3),
            marker=dict(size=8)
        ))
        
        fig_spo2.update_layout(
            title="SpO2 Over Time",
            xaxis_title="Date",
            yaxis_title="SpO2 (%)",
            height=400
        )
        st.plotly_chart(fig_spo2, use_container_width=True)
        
        # Pulse chart
        fig_pulse = go.Figure()
        fig_pulse.add_trace(go.Scatter(
            x=dates, y=pulse_values,
            mode='lines+markers',
            name='Pulse (BPM)',
            line=dict(color='purple', width=3),
            marker=dict(size=8)
        ))
        
        fig_pulse.update_layout(
            title="Pulse Over Time",
            xaxis_title="Date",
            yaxis_title="Pulse (BPM)",
            height=400
        )
        st.plotly_chart(fig_pulse, use_container_width=True)
    else:
        st.info("No SpO2 data available yet. Take a SpO2 test to see your trends!")
    
    # Temperature History
    temp_data = db.get_user_test_history(user_id, "Temperature")
    if temp_data:
        st.markdown("#### Temperature History")
        
        dates = [record['test_sessions']['session_date'] for record in reversed(temp_data)]
        temps = [record['value_1'] for record in reversed(temp_data)]
        
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=dates, y=temps,
            mode='lines+markers',
            name='Temperature (°C)',
            line=dict(color='orange', width=3),
            marker=dict(size=8)
        ))
        
        # Add reference lines
        fig_temp.add_hline(y=36.1, line_dash="dash", line_color="blue", annotation_text="Low threshold")
        fig_temp.add_hline(y=37.2, line_dash="dash", line_color="red", annotation_text="Fever threshold")
        
        fig_temp.update_layout(
            title="Temperature Over Time",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            height=400
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    else:
        st.info("No temperature data available yet. Take a temperature test to see your trends!")

def show_download_reports(db: DatabaseService, user_id: str):
    st.markdown("### Download Health Reports")
    st.markdown("Generate PDF reports to share with your healthcare provider.")
    
    report_gen = ReportGenerator()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Download Weight History", use_container_width=True):
            generate_report(report_gen, db, user_id, "Weight", "Weight History Report")
        
        if st.button("🩸 Download Blood Sugar History", use_container_width=True):
            generate_report(report_gen, db, user_id, "Sugar", "Blood Sugar History Report")
        
        if st.button("🌡️ Download Temperature History", use_container_width=True):
            generate_report(report_gen, db, user_id, "Temperature", "Temperature History Report")
    
    with col2:
        if st.button("💓 Download Blood Pressure History", use_container_width=True):
            generate_report(report_gen, db, user_id, "Blood Pressure", "Blood Pressure History Report")
        
        if st.button("🫁 Download SpO2 History", use_container_width=True):
            generate_report(report_gen, db, user_id, "SpO2", "SpO2 & Pulse History Report")

def generate_report(report_gen: ReportGenerator, db: DatabaseService, user_id: str, test_type: str, title: str):
    """Generate and download a PDF report"""
    try:
        data = db.get_user_test_history(user_id, test_type)
        if not data:
            st.warning(f"No {test_type.lower()} data available to generate report.")
            return
        
        user_name = st.session_state.user['full_name']
        pdf_buffer = report_gen.generate_health_report(data, test_type, title, user_name)
        
        # Offer download
        st.download_button(
            label=f"📥 Download {title}",
            data=pdf_buffer,
            file_name=f"{test_type.lower().replace(' ', '_')}_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
        
    except Exception as e:
        st.error(f"Failed to generate report: {e}")