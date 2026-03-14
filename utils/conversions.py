def convert_height_to_cm(value: float, unit: str) -> float:
    """Convert height to centimeters"""
    if unit == "cm":
        return value
    elif unit == "m":
        return value * 100
    elif unit == "ft":
        return value * 30.48
    elif unit == "inch":
        return value * 2.54
    else:
        raise ValueError(f"Unknown height unit: {unit}")

def convert_weight_to_kg(value: float, unit: str) -> float:
    """Convert weight to kilograms"""
    if unit == "kg":
        return value
    elif unit == "lbs":
        return value * 0.453592
    else:
        raise ValueError(f"Unknown weight unit: {unit}")

def convert_temperature_to_celsius(value: float, unit: str) -> float:
    """Convert temperature to Celsius"""
    if unit == "Celsius":
        return value
    elif unit == "Fahrenheit":
        return (value - 32) * 5/9
    else:
        raise ValueError(f"Unknown temperature unit: {unit}")

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate BMI from weight in kg and height in cm"""
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def format_height_display(height_cm: float) -> str:
    """Format height for display"""
    return f"{height_cm:.1f} cm"

def format_weight_display(weight_kg: float) -> str:
    """Format weight for display"""
    return f"{weight_kg:.1f} kg"

def format_bmi_display(bmi: float) -> str:
    """Format BMI for display"""
    return f"{bmi:.1f}"