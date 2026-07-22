import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy.orm import Session

from app.ml.predictor import AQIPredictor
from app.services.source_attribution import SourceAttributionService
from app.services.enforcement import EnforcementService


load_dotenv()


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

Air Quality Information:

Station:
{prediction['station']}

City:
{prediction['city']}

Current AQI:
{prediction['current_aqi']}

Predicted AQI:
{prediction['predicted_aqi']}

Trend:
{prediction['trend']}

Category:
{prediction['category']}


Pollution Source Attribution:

Traffic:
{attribution['traffic']}%

Construction:
{attribution['construction']}%

Industry:
{attribution['industry']}%

Other:
{attribution['other']}%


Enforcement Information:

Priority:
{enforcement['priority']}

Recommended Actions:

{", ".join(enforcement['recommended_actions'])}


Health Advice:

{prediction['health_advice']}


Return ONLY valid JSON.

The JSON format must be:

{{
    "situation_summary": "",
    "forecast_analysis": "",
    "pollution_source_analysis": "",
    "enforcement_recommendation": "",
    "citizen_health_advisory": ""
}}

Rules:
- Do not use markdown.
- Do not add extra fields.
- Keep the response below 250 words.
"""


        try:

            response = client.chat.completions.create(

                model=os.getenv(
                    "OPENAI_MODEL",
                    "gpt-5-mini"
                ),

                response_format={
                    "type": "json_object"
                },

                messages=[

                    {
                        "role": "system",
                        "content":
                        "You are an expert Environmental Intelligence Assistant."
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ]
            )


            llm_response = json.loads(
                response.choices[0].message.content
            )


        except Exception as e:

            llm_response = {
                "error": "AI analysis unavailable",
                "details": str(e)
            }


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


            "source_attribution": {

                "traffic": attribution["traffic"],

                "construction": attribution["construction"],

                "industry": attribution["industry"],

                "other": attribution["other"],

                "confidence": attribution.get(
                    "confidence"
                )

            },


            "priority": enforcement["priority"],


            "recommended_actions":
                enforcement["recommended_actions"],


            "llm_insights": llm_response

        }