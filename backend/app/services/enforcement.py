from sqlalchemy.orm import Session

from app.services.source_attribution import SourceAttributionService


class EnforcementService:

    @staticmethod
    def recommend(db: Session, station_id: str):

        attribution = SourceAttributionService.analyze(
            db,
            station_id
        )

        if attribution is None:
            return None

        actions = []

        if attribution["traffic"] >= 35:
            actions.extend([
                "Increase traffic police deployment during peak hours.",
                "Promote public transport in hotspot zones.",
                "Restrict heavy diesel vehicle movement."
            ])

        if attribution["construction"] >= 25:
            actions.extend([
                "Inspect nearby construction sites for dust suppression compliance.",
                "Enforce covering of construction materials.",
                "Increase water sprinkling on exposed roads."
            ])

        if attribution["industry"] >= 20:
            actions.extend([
                "Inspect nearby industrial emission sources.",
                "Verify stack emission monitoring records.",
                "Conduct surprise pollution control inspections."
            ])

        if attribution["other"] >= 15:
            actions.append(
                "Monitor open waste burning and local emission sources."
            )

        score = max(
            attribution["traffic"],
            attribution["construction"],
            attribution["industry"]
        )

        if score >= 45:
            priority = "HIGH"
        elif score >= 30:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        return {
            "station": attribution["station"],
            "city": attribution["city"],
            "priority": priority,
            "source_breakdown": {
                "traffic": attribution["traffic"],
                "construction": attribution["construction"],
                "industry": attribution["industry"],
                "other": attribution["other"]
            },
            "recommended_actions": actions,
            "confidence": attribution["confidence"]
        }