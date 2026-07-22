from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.station import AQIStation
from app.models.aqi_reading import AQIReading


class IntelligenceService:

    @staticmethod
    def city_risk(db: Session):

        rows = (
            db.query(
                AQIStation.city,
                func.avg(AQIReading.aqi).label("avg_aqi")
            )
            .join(
                AQIReading,
                AQIReading.station_id == AQIStation.id
            )
            .group_by(AQIStation.city)
            .all()
        )

        result = []

        for city, avg in rows:

            if avg <= 50:
                risk = "Low"

            elif avg <= 100:
                risk = "Moderate"

            elif avg <= 200:
                risk = "High"

            else:
                risk = "Critical"

            result.append({

                "city": city,

                "average_aqi": round(avg, 2),

                "risk": risk

            })

        return result

    @staticmethod
    def interventions(db: Session):

        rows = (
            db.query(
                AQIStation.city,
                func.avg(AQIReading.aqi).label("avg_aqi")
            )
            .join(
                AQIReading,
                AQIReading.station_id == AQIStation.id
            )
            .group_by(AQIStation.city)
            .all()
        )

        response = []

        for city, avg in rows:

            if avg <= 50:

                priority = "LOW"

                actions = [
                    "Continue monitoring air quality."
                ]

            elif avg <= 100:

                priority = "MEDIUM"

                actions = [
                    "Reduce traffic congestion.",
                    "Increase roadside monitoring."
                ]

            elif avg <= 200:

                priority = "HIGH"

                actions = [
                    "Inspect construction sites.",
                    "Restrict heavy diesel vehicles.",
                    "Increase industrial inspections."
                ]

            else:

                priority = "CRITICAL"

                actions = [
                    "Emergency pollution control measures.",
                    "Temporary industrial emission restrictions.",
                    "Restrict construction activity.",
                    "Issue public health advisory."
                ]

            response.append({

                "city": city,

                "average_aqi": round(avg, 2),

                "priority": priority,

                "recommended_actions": actions

            })

        return response

    @staticmethod
    def health_risk(db: Session):

        avg = (
            db.query(
                func.avg(AQIReading.aqi)
            ).scalar()
        ) or 0

        if avg <= 50:

            risk = "Low"

            advice = {
                "general": "Air quality is good.",
                "children": "Outdoor activities are safe.",
                "elderly": "Normal activity.",
                "patients": "No special precautions."
            }

        elif avg <= 100:

            risk = "Moderate"

            advice = {
                "general": "Sensitive individuals should limit prolonged outdoor activity.",
                "children": "Take breaks during outdoor sports.",
                "elderly": "Avoid long exposure outdoors.",
                "patients": "Carry prescribed medication."
            }

        elif avg <= 200:

            risk = "High"

            advice = {
                "general": "Reduce outdoor exposure.",
                "children": "Avoid outdoor sports.",
                "elderly": "Stay indoors whenever possible.",
                "patients": "Wear an N95 mask outdoors."
            }

        else:

            risk = "Critical"

            advice = {
                "general": "Avoid going outdoors.",
                "children": "Remain indoors.",
                "elderly": "Avoid exposure completely.",
                "patients": "Seek medical attention if symptoms worsen."
            }

        return {

            "average_aqi": round(avg, 2),

            "risk_level": risk,

            "health_advisory": advice

        }