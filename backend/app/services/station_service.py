from sqlalchemy.orm import Session

from app.models.station import AQIStation


class StationService:

    @staticmethod
    def get_by_station_code(db: Session, station_code: str):

        return (
            db.query(AQIStation)
            .filter(AQIStation.station_code == station_code)
            .first()
        )

    @staticmethod
    def create_station(db: Session, station_data: dict):

        station = AQIStation(**station_data)

        db.add(station)
        db.commit()
        db.refresh(station)

        return station

    @staticmethod
    def get_or_create(db: Session, station_data: dict):

        station = StationService.get_by_station_code(
            db,
            station_data["station_code"],
        )

        if station:
            return station

        return StationService.create_station(db, station_data)