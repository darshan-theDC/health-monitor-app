def classify_bmi(bmi: float) -> tuple:
    """Classify BMI and return (status, color_class)"""
    if bmi < 18.5:
        return ("Low BMI", "result-low")
    elif 18.5 <= bmi < 25:
        return ("Normal BMI", "result-normal")
    else:
        return ("High BMI", "result-high")

def classify_blood_sugar(glucose: float) -> tuple:
    """Classify blood sugar (mg/dL) and return (status, color_class)"""
    if glucose < 70:
        return ("Low Blood Sugar", "result-low")
    elif 70 <= glucose < 140:
        return ("Normal Blood Sugar", "result-normal")
    else:
        return ("High Blood Sugar", "result-high")

def classify_blood_pressure(systolic: float, diastolic: float) -> tuple:
    """Classify blood pressure and return (status, color_class)"""
    if systolic < 90 or diastolic < 60:
        return ("Low Blood Pressure", "result-low")
    elif systolic < 120 and diastolic < 80:
        return ("Normal Blood Pressure", "result-normal")
    else:
        return ("High Blood Pressure", "result-high")

def classify_spo2(spo2: float, pulse: float) -> tuple:
    """Classify SpO2 and return (status, color_class)"""
    if spo2 < 95:
        return ("Low SpO2", "result-low")
    elif spo2 >= 95:
        return ("Normal SpO2", "result-normal")
    # Note: SpO2 rarely goes above 100%, so no "high" category

def classify_temperature(temp_celsius: float) -> tuple:
    """Classify temperature (Celsius) and return (status, color_class)"""
    if temp_celsius < 36.1:
        return ("Low Temperature", "result-low")
    elif 36.1 <= temp_celsius <= 37.2:
        return ("Normal Temperature", "result-normal")
    else:
        return ("High Temperature / Fever", "result-high")

def get_bmi_color_for_chart(bmi: float) -> str:
    """Get color for BMI chart visualization"""
    if bmi < 18.5:
        return "blue"  # Underweight
    elif 18.5 <= bmi < 25:
        return "green"  # Normal
    else:
        return "red"  # High

def get_health_advice(test_type: str, status: str) -> str:
    """Get basic health advice based on test results"""
    advice = {
        "BMI": {
            "Low BMI": "Consider consulting with a healthcare provider about healthy weight gain strategies.",
            "Normal BMI": "Great! Maintain your current healthy lifestyle.",
            "High BMI": "Consider consulting with a healthcare provider about healthy weight management."
        },
        "Sugar": {
            "Low Blood Sugar": "If you feel symptoms, consider having a small snack. Consult your doctor if this happens frequently.",
            "Normal Blood Sugar": "Excellent! Your blood sugar is in a healthy range.",
            "High Blood Sugar": "Monitor your diet and consider consulting with your healthcare provider."
        },
        "Blood Pressure": {
            "Low Blood Pressure": "Stay hydrated and consult your doctor if you feel dizzy or weak.",
            "Normal Blood Pressure": "Great! Your blood pressure is in a healthy range.",
            "High Blood Pressure": "Consider lifestyle changes and consult with your healthcare provider."
        },
        "SpO2": {
            "Low SpO2": "This may indicate breathing issues. Consider consulting with a healthcare provider.",
            "Normal SpO2": "Excellent! Your oxygen levels are healthy."
        },
        "Temperature": {
            "Low Temperature": "Stay warm and monitor. Consult a doctor if you feel unwell.",
            "Normal Temperature": "Perfect! Your body temperature is normal.",
            "High Temperature / Fever": "Rest, stay hydrated, and consider consulting with a healthcare provider."
        }
    }
    
    return advice.get(test_type, {}).get(status, "Consult with your healthcare provider for personalized advice.")