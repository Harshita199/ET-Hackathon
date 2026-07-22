import os

from openai import OpenAI
from sqlalchemy.orm import Session

from app.ml.predictor import AQIPredictor
from app.services.source_attribution import SourceAttributionService
from app.services.enforcement import EnforcementService


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class AIInsightsService:

    @staticmethod
    def analyze(db: Session, station_id: str):

        prediction = AQIPredictor.predict(
            db,
            station_id
        )

        if prediction is None:
            return None

        attribution = SourceAttributionService.analyze(
            db,
            station_id
        )

        enforcement = EnforcementService.recommend(
            db,
            station_id
        )

        prompt = f"""
You are an Environmental Intelligence AI working for a Smart City command center.

Analyze the following air quality data.

Current AQI:
{prediction['current_aqi']}

Predicted AQI:
{prediction['predicted_aqi']}

Trend:
{prediction['trend']}

Category:
{prediction['category']}

Pollution Source Attribution

Traffic:
{attribution['traffic']}%

Construction:
{attribution['construction']}%

Industry:
{attribution['industry']}%

Other:
{attribution['other']}%

Priority:
{enforcement['priority']}

Recommended Enforcement Actions:
{", ".join(enforcement['recommended_actions'])}

Health Advice:
{prediction['health_advice']}

Generate a professional response with the following headings.

1. Situation Summary
2. Forecast Analysis
3. Pollution Source Analysis
4. Enforcement Recommendation
5. Citizen Health Advisory

Keep the response below 250 words.
"""

        response = client.chat.completions.create(
            model="gpt-5.5",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Environmental Intelligence Assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        llm_response = response.choices[0].message.content

        return {

            "station": prediction["station"],

            "city": prediction["city"],

            "current_status": {
                "current_aqi": prediction["current_aqi"],
                "category": prediction["category"]
            },

            "forecast": {
                "predicted_aqi": prediction["predicted_aqi"],
                "confidence": prediction["confidence"],
                "trend": prediction["trend"]
            },

            "source_attribution": attribution,

            "priority": enforcement["priority"],

            "recommended_actions": enforcement["recommended_actions"],

            "llm_insights": llm_response

        }