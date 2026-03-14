# Health Monitor for Parents 🏥

A simple, user-friendly health monitoring system designed specifically for parents and older adults to track basic health indicators using common home devices.

## 💝 Project Purpose

This application was created with love and dedication to my parents, who inspired this project through their daily health management routines. I observed how they diligently measure their health readings at home using various devices but often struggled to understand whether their readings were normal or concerning.

This project aims to help parents and older adults:
- Understand their health readings more clearly
- Visualize trends through simple graphs  
- Avoid the hassle of writing everything on paper
- Get immediate feedback on whether values are normal

## ✨ Features

### For All Users (Guest Mode)
- **Quick Health Checks**: Test BMI, Blood Sugar, Blood Pressure, SpO2, and Temperature
- **Instant Results**: Get immediate Low/Normal/High classifications
- **Health Advice**: Receive basic guidance based on your readings
- **No Account Required**: Use the app without creating an account

### For Registered Users
- **Data Storage**: All readings are automatically saved
- **Health Dashboard**: View interactive graphs and trends over time
- **PDF Reports**: Download professional reports for your healthcare provider
- **Profile Management**: Store height, weight, and personal information
- **Historical Tracking**: Monitor your health progress over time

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Supabase (PostgreSQL database)
- **Authentication**: bcrypt password hashing
- **Visualizations**: Plotly interactive charts
- **Reports**: ReportLab PDF generation
- **Deployment**: Streamlit Cloud compatible

## 📱 Mobile-Friendly Design

The interface prioritizes:
- Large, readable fonts for older users
- Simple navigation and clear buttons
- Mobile-responsive layout
- High contrast and accessibility
- Intuitive user experience

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Supabase account (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/health-monitor-parents.git
   cd health-monitor-parents
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Supabase**
   - Create a new project at [supabase.com](https://supabase.com)
   - Go to Settings > API to get your project URL and anon key
   - Create the required database tables (see Database Setup below)

4. **Configure environment variables**
   - Copy `.env.example` to `.env` and update with your Supabase credentials:
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` with your actual credentials:
   ```
   SUPABASE_URL=your_actual_supabase_project_url
   SUPABASE_KEY=your_actual_supabase_anon_key
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🗄️ Database Setup

Create these tables in your Supabase database:

### Users Table
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR NOT NULL,
    password_hash VARCHAR NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR NOT NULL,
    height_cm DECIMAL,
    weight_kg DECIMAL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Test Sessions Table
```sql
CREATE TABLE test_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    session_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Test Results Table
```sql
CREATE TABLE test_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES test_sessions(session_id),
    test_type VARCHAR NOT NULL,
    value_1 DECIMAL NOT NULL,
    value_2 DECIMAL,
    status VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🏗️ Project Structure

```
health-monitor-parents/
├── app.py                      # Main application entry point
├── views/                      # User interface pages
│   ├── landing.py             # Landing page with project story
│   ├── login.py               # Authentication and signup
│   ├── tests.py               # Health testing interface
│   └── dashboard.py           # Data visualization and reports
├── services/                   # Business logic and external services
│   ├── database.py            # Supabase database operations
│   ├── auth.py                # Authentication service
│   └── report_generator.py    # PDF report generation
├── utils/                      # Utility functions
│   ├── conversions.py         # Unit conversions (height, weight, temp)
│   └── health_rules.py        # Health classification rules
├── .env                       # Environment variables (not in git)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🏥 Health Tests Supported

1. **BMI Test**: Calculate Body Mass Index from height and weight
2. **Blood Sugar**: Monitor glucose levels (mg/dL)
3. **Blood Pressure**: Track systolic and diastolic pressure
4. **SpO2 & Pulse**: Oxygen saturation and heart rate monitoring
5. **Temperature**: Body temperature with Celsius/Fahrenheit support

## 📊 Health Classifications

The app uses medically-standard ranges to classify readings as Low, Normal, or High:

- **BMI**: <18.5 (Low), 18.5-24.9 (Normal), ≥25 (High)
- **Blood Sugar**: <70 (Low), 70-139 (Normal), ≥140 (High) mg/dL
- **Blood Pressure**: <90/60 (Low), <120/80 (Normal), ≥120/80 (High) mmHg
- **SpO2**: <95% (Low), ≥95% (Normal)
- **Temperature**: <36.1°C (Low), 36.1-37.2°C (Normal), >37.2°C (Fever)

## 🚀 Deployment on Streamlit Cloud

1. **Push to GitHub**: Ensure your code is in a GitHub repository
2. **Connect to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)
3. **Deploy**: Connect your GitHub repo and set environment variables
4. **Configure Secrets**: Add your Supabase credentials in the Streamlit Cloud secrets management

### Environment Variables for Deployment
In Streamlit Cloud secrets, add:
```toml
SUPABASE_URL = "your_supabase_project_url"
SUPABASE_KEY = "your_supabase_anon_key"
```

## 🤝 Contributing

This project is shared publicly so other families can benefit and developers can learn or extend the codebase. Contributions are welcome!

### Development Guidelines
- Keep the interface simple and accessible
- Maintain large text and mobile-friendly design
- Follow the existing code structure
- Add tests for new health classification rules
- Update documentation for new features

## 📄 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute it to help more families manage their health.

## 🙏 Acknowledgments

- **My Parents**: For inspiring this project and being the motivation behind every feature
- **ChatGPT**: For guidance and research discussions during development
- **Streamlit Community**: For creating an amazing framework for rapid web app development
- **Supabase Team**: For providing an excellent backend-as-a-service platform

## 💡 Future Enhancements

- Medication reminders and tracking
- Integration with wearable devices
- Multi-language support
- Family member sharing and monitoring
- Healthcare provider integration
- Advanced analytics and insights

---

**Built with ❤️ for parents everywhere**

*This project demonstrates that technology should serve people, especially our loved ones who deserve tools that work for them, not against them.*