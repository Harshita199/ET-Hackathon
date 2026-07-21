class AQIInsights:

    @staticmethod
    def generate(current_aqi, predicted_aqi):

        diff = predicted_aqi - current_aqi

        if predicted_aqi <= 50:
            category = "Good"
            advice = "Air quality is good. Outdoor activities are safe."

        elif predicted_aqi <= 100:
            category = "Moderate"
            advice = "Sensitive individuals should avoid prolonged outdoor exposure."

        elif predicted_aqi <= 150:
            category = "Unhealthy for Sensitive Groups"
            advice = "Children, elderly and asthma patients should reduce outdoor activity."

        elif predicted_aqi <= 200:
            category = "Unhealthy"
            advice = "Wear a mask and avoid unnecessary outdoor exposure."

        elif predicted_aqi <= 300:
            category = "Very Unhealthy"
            advice = "Stay indoors whenever possible."

        else:
            category = "Hazardous"
            advice = "Avoid going outside. Emergency precautions recommended."

        if diff > 15:
            trend = "Air quality is expected to worsen."
        elif diff < -15:
            trend = "Air quality is expected to improve."
        else:
            trend = "Air quality is expected to remain stable."

        return {
            "category": category,
            "trend": trend,
            "health_advice": advice
        }