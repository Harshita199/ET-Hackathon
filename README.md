# 🌍 ET Hackathon – Air Quality Monitoring Platform

## Overview

This project is an Air Quality Monitoring Platform built using FastAPI and PostgreSQL.

The backend ingests live AQI data from the WAQI API, parses it into a normalized format, stores stations and AQI readings in Neon PostgreSQL, and exposes REST APIs for frontend dashboards.

The architecture is designed so that additional data sources (such as CPCB/OpenAQ) can be integrated later without changing the database or service layer.

---

# Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy ORM
- Alembic
- PostgreSQL (Neon)
- WAQI API
- Pydantic
- HTTPX

---

# Project Structure

```
app/
│
├── api/
├── core/
├── database/
├── ingestion/
│   ├── waqi.py
│   ├── cities.py
│
├── models/
│   ├── station.py
│   ├── aqi_reading.py
│
├── services/
│   ├── station_service.py
│   ├── aqi_reading_service.py
│   ├── dashboard_service.py
│   ├── station_query_service.py
│   ├── sync_service.py
│   ├── waqi_parser.py
│
└── main.py
```

---

# Backend Features Completed

## Database

- ✅ Neon PostgreSQL configured
- ✅ SQLAlchemy models
- ✅ Alembic migrations
- ✅ UUID primary keys
- ✅ Station table
- ✅ AQI Reading table

---

## Data Ingestion

- ✅ WAQI API integration
- ✅ API key authentication
- ✅ Live AQI retrieval
- ✅ Multiple city support

---

## Data Parsing

WAQI response is converted into a common format.

Example:

```
Station
-------
Station Code
Station Name
City
State
Latitude
Longitude

Reading
-------
Timestamp
AQI
PM2.5
PM10
CO
NO2
SO2
O3
Temperature
Humidity
Wind Speed
Pressure
```

---

## Database Services

### Station Service

- Get Station
- Create Station
- Get or Create Station

---

### AQI Reading Service

- Save Reading
- Prevent duplicate readings
- Fetch station history

---

### Sync Service

- Sync one city
- Sync multiple cities
- Automatically creates station if not present
- Stores latest AQI reading

---

## Dashboard APIs

### GET /

Application status

---

### GET /health

Health check

---

### GET /health/db

Database connectivity

---

### GET /summary

Returns

- Total stations
- Average AQI
- Good AQI count
- Moderate AQI count
- Poor AQI count
- Very Poor AQI count
- Severe AQI count

---

### GET /stations

Returns

- Station information
- Latest AQI
- Latest timestamp

---

### GET /stations/{station_id}/history

Returns historical AQI readings for a station.

---

### POST /sync

Syncs all configured cities from WAQI into PostgreSQL.

---

### POST /test/save-station

Sync a single city into the database.

---

# Current Workflow

```
WAQI API
     │
     ▼
WAQI Client
     │
     ▼
WAQI Parser
     │
     ▼
Station Service
     │
     ▼
AQI Reading Service
     │
     ▼
Neon PostgreSQL
     │
     ▼
REST APIs
     │
     ▼
Frontend
```

---

# Current Status

## ✅ Completed

- Backend setup
- Database design
- Live AQI ingestion
- Parsing
- Data persistence
- Sync APIs
- Dashboard APIs
- Station APIs
- History APIs

Backend is functional and ready for frontend integration.

---

# Frontend Work Remaining

## Dashboard

- Display Summary API
    - Total Stations
    - Average AQI
    - AQI Category Counts

---

## Stations Page

Use

```
GET /stations
```

Display

- Station Name
- City
- Current AQI
- Last Updated

---

## Station Details Page

Use

```
GET /stations/{station_id}/history
```

Display

- AQI trend chart
- PM2.5 trend
- PM10 trend
- Historical readings table

---

## Charts

Suggested charts

- AQI Line Chart
- PM2.5 Line Chart
- PM10 Line Chart
- AQI Distribution

---

## Maps (Optional)

Show stations on map using

- Latitude
- Longitude

---

## Auto Refresh (Optional)

Refresh dashboard every

- 5 minutes
- 10 minutes

---

## Future Enhancements

- CPCB Integration
- OpenAQ Integration
- Forecast ingestion
- ML AQI prediction
- Alert engine
- Weather integration
- Authentication
- Scheduled background sync
- Docker deployment
- Kubernetes deployment

---

# API Summary

| Method | Endpoint | Purpose |
|---------|----------|---------|
| GET | / | Application status |
| GET | /health | Health check |
| GET | /health/db | Database health |
| GET | /summary | Dashboard summary |
| GET | /stations | List stations with latest AQI |
| GET | /stations/{station_id}/history | AQI history |
| POST | /sync | Sync all cities |
| POST | /test/save-station | Sync one city |

---

# Next Milestone

Build the frontend dashboard using the existing APIs and visualize AQI trends and station data.
