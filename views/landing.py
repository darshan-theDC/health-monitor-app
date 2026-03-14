import streamlit as st

def show_landing_page():
    st.markdown('<h1 class="main-title">Health Monitor for Parents</h1>', unsafe_allow_html=True)
    
    # Initialize language in session state
    if 'language' not in st.session_state:
        st.session_state.language = 'english'
    
    # About This Project section
    st.markdown("### About This Project")
    
    # Language toggle buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("English", key="lang_en", type="primary" if st.session_state.language == 'english' else "secondary"):
            st.session_state.language = 'english'
            st.rerun()
    with col2:
        if st.button("ಕನ್ನಡ", key="lang_kn", type="primary" if st.session_state.language == 'kannada' else "secondary"):
            st.session_state.language = 'kannada'
            st.rerun()
    
    if st.button("About This Project", key="about_btn", help="Click to learn more"):
        with st.expander("Project Story", expanded=True):
            if st.session_state.language == 'english':
                st.markdown("""
                **A Personal Dedication to My Parents**
                
                This health monitoring system was created with love and dedication to my parents, 
                who inspired this project through their daily health management routines.
                
                **The Inspiration**
                
                I observed how my parents diligently measure their health readings at home using 
                various devices - blood sugar meters, blood pressure monitors, thermometers, 
                pulse oximeters, and weighing scales. However, they often struggled to understand 
                whether their readings were normal, concerning, or required attention.
                
                **The Solution**
                
                This application was designed to help parents and older adults:
                - Understand their health readings more clearly
                - Visualize trends through simple graphs
                - Avoid the hassle of writing everything on paper
                - Get immediate feedback on whether values are normal
                
                **Development Journey**
                
                This project was developed with guidance and research discussions using ChatGPT, 
                which helped shape the structure, user experience, and technical implementation 
                during the development process.
                
                **Sharing with Love**
                
                This project is shared publicly on GitHub so other families can benefit from it, 
                and other developers can learn from or extend the codebase to help even more people.
                
                The interface prioritizes simplicity, large text, and mobile-friendly design 
                because our parents deserve technology that works for them, not against them.
                """)
            else:  # Kannada
                st.markdown("""
                <div class="kannada-text">
                
                **ನನ್ನ ಅಪ್ಪ-ಅಮ್ಮನಿಗೆ ಮೀಸಲಾದ ಪ್ರೀತಿಯ ಕೊಡುಗೆ**
                
                ಈ ಆರೋಗ್ಯ ಪರಿಶೀಲನಾ ಅಪ್ಲಿಕೇಶನ್ ಅನ್ನು ನನ್ನ ಅಪ್ಪ-ಅಮ್ಮನ ಪ್ರೀತಿಯಿಂದ ಮಾಡಿದ್ದೇನೆ. 
                ಅವರು ಪ್ರತಿದಿನ ಆರೋಗ್ಯ ಪರೀಕ್ಷೆ ಮಾಡುವುದನ್ನು ನೋಡಿ ಈ ಕಲ್ಪನೆ ಬಂದಿತು.
                
                **ಏಕೆ ಈ ಅಪ್ಲಿಕೇಶನ್?**
                
                ನನ್ನ ಅಪ್ಪ-ಅಮ್ಮ ಮನೆಯಲ್ಲೇ ಎಲ್ಲಾ ಆರೋಗ್ಯ ಪರೀಕ್ಷೆಗಳನ್ನು ಮಾಡುತ್ತಾರೆ - ಸಕ್ಕರೆ ಪರೀಕ್ಷೆ, 
                ಬ್ಲಡ್ ಪ್ರೆಶರ್, ಜ್ವರ ಅಳತೆ, ಆಕ್ಸಿಜನ್ ಮಟ್ಟ, ತೂಕ ಇತ್ಯಾದಿ. ಆದರೆ ಈ ಸಂಖ್ಯೆಗಳು 
                ಸರಿಯಾಗಿವೆಯೇ ಅಥವಾ ಚಿಂತೆಯ ವಿಷಯವೇ ಎಂದು ಅರ್ಥ ಮಾಡಿಕೊಳ್ಳಲು ಕಷ್ಟವಾಗುತ್ತಿತ್ತು.
                
                **ಈ ಅಪ್ಲಿಕೇಶನ್ ಏನು ಮಾಡುತ್ತದೆ?**
                
                ಈ ಅಪ್ಲಿಕೇಶನ್ ನಮ್ಮ ಅಪ್ಪ-ಅಮ್ಮಂದಿರಿಗೆ ಸಹಾಯ ಮಾಡುತ್ತದೆ:
                - ಆರೋಗ್ಯ ಸಂಖ್ಯೆಗಳನ್ನು ಸುಲಭವಾಗಿ ಅರ್ಥ ಮಾಡಿಕೊಳ್ಳಲು
                - ಸರಳ ಚಾರ್ಟ್‌ಗಳಲ್ಲಿ ಬದಲಾವಣೆಗಳನ್ನು ನೋಡಲು
                - ಕಾಗದದಲ್ಲಿ ಬರೆಯುವ ಕಷ್ಟ ಇಲ್ಲದೆ ಇರಲು
                - ತಕ್ಷಣವೇ ಸಾಮಾನ್ಯ/ಅಸಾಮಾನ್ಯ ಎಂದು ತಿಳಿಯಲು
                
                **ಹೇಗೆ ಮಾಡಿದೆ?**
                
                ಈ ಅಪ್ಲಿಕೇಶನ್ ಅನ್ನು ChatGPT ಸಹಾಯದಿಂದ ಮಾಡಿದ್ದೇನೆ. ಅದು ಸರಿಯಾದ ರಚನೆ, 
                ಬಳಕೆದಾರರಿಗೆ ಸುಲಭ ಮತ್ತು ತಾಂತ್ರಿಕ ಅಂಶಗಳನ್ನು ಯೋಚಿಸಲು ಸಹಾಯ ಮಾಡಿತು.
                
                **ಎಲ್ಲರಿಗೂ ಉಚಿತ**
                
                ಈ ಅಪ್ಲಿಕೇಶನ್ ಅನ್ನು GitHub ನಲ್ಲಿ ಎಲ್ಲರಿಗೂ ಉಚಿತವಾಗಿ ಕೊಟ್ಟಿದ್ದೇನೆ. ಇತರ ಕುಟುಂಬಗಳಿಗೂ 
                ಉಪಯೋಗವಾಗಲಿ ಮತ್ತು ಇತರ ಡೆವಲಪರ್‌ಗಳು ಇದನ್ನು ಇನ್ನೂ ಉತ್ತಮಗೊಳಿಸಲಿ ಎಂಬ ಆಶಯದಿಂದ.
                
                ಈ ಅಪ್ಲಿಕೇಶನ್ ಸರಳ, ದೊಡ್ಡ ಅಕ್ಷರಗಳು ಮತ್ತು ಮೊಬೈಲ್‌ನಲ್ಲಿ ಸುಲಭವಾಗಿ ಬಳಸಬಹುದಾಗಿ ಮಾಡಿದ್ದೇನೆ. 
                ನಮ್ಮ ಅಪ್ಪ-ಅಮ್ಮಂದಿರಿಗೆ ತಂತ್ರಜ್ಞಾನ ಸಹಾಯಕವಾಗಬೇಕು, ಕಷ್ಟವಾಗಬಾರದು.
                
                </div>
                """, unsafe_allow_html=True)
    
    
    st.markdown("---")
    
    # Main action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Check Health Now", key="guest_btn", help="Quick health check without saving data"):
            st.session_state.guest_mode = True
            st.session_state.page = 'tests'
            st.rerun()
    
    with col2:
        if st.button("💾 Login & Save History", key="login_btn", help="Create account to save and track your health data"):
            st.session_state.guest_mode = False
            st.session_state.page = 'login'
            st.rerun()
    
    # Instructions
    st.markdown("---")
    
    if st.session_state.language == 'english':
        st.markdown("""
        ### How to Use This App
        
        **Check Health Now** - Get instant results without creating an account
        - Perfect for quick health checks
        - Results are not saved
        - No login required
        
        **Login & Save History** - Track your health over time
        - Save all your readings
        - View graphs and trends
        - Download reports for your doctor
        - Requires creating a simple account
        """)
    else:  # Kannada
        st.markdown("""
        <div class="kannada-text">
        
        ### ಈ ಅಪ್ಲಿಕೇಶನ್ ಹೇಗೆ ಬಳಸಬೇಕು
        
        **ಈಗಲೇ ಆರೋಗ್ಯ ಪರೀಕ್ಷೆ** - ಅಕೌಂಟ್ ಇಲ್ಲದೆಯೇ ತಕ್ಷಣ ಫಲಿತಾಂಶ
        - ಬೇಗನೆ ಆರೋಗ್ಯ ಪರೀಕ್ಷೆಗೆ ಸೂಕ್ತ
        - ಫಲಿತಾಂಶಗಳು ಉಳಿಸಲಾಗುವುದಿಲ್ಲ
        - ಲಾಗಿನ್ ಅಗತ್ಯವಿಲ್ಲ
        
        **ಲಾಗಿನ್ ಮಾಡಿ ಇತಿಹಾಸ ಉಳಿಸಿ** - ಕಾಲಾನುಕ್ರಮದಲ್ಲಿ ಆರೋಗ್ಯ ಟ್ರ್ಯಾಕ್ ಮಾಡಿ
        - ಎಲ್ಲಾ ರೀಡಿಂಗ್‌ಗಳನ್ನು ಉಳಿಸಿ
        - ಗ್ರಾಫ್‌ಗಳು ಮತ್ತು ಟ್ರೆಂಡ್‌ಗಳನ್ನು ನೋಡಿ
        - ಡಾಕ್ಟರ್‌ಗೆ ರಿಪೋರ್ಟ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ
        - ಸರಳ ಅಕೌಂಟ್ ರಚಿಸುವುದು ಅಗತ್ಯ
        
        </div>
        """, unsafe_allow_html=True)