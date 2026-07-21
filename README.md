# Air Quality Intelligence Platform - Frontend Requirements

## Overview

The frontend application provides a visualization layer for the Air Quality Intelligence Platform.

The application consumes APIs from the FastAPI backend and displays:

- AQI monitoring dashboard
- Monitoring stations
- Historical air quality trends
- ML-based AQI prediction
- Pollution alerts
- Pollution ranking
- Air quality insights


# Frontend Pages & API Integration

---

# 1. Dashboard Page

## Purpose

Provide an overall view of the current air quality status across monitored locations.

## API

```
GET /dashboard
```

## UI Components

### AQI Overview Cards

Display:

- Current average AQI
- AQI category
- Total monitoring stations
- Pollution status


### Charts

Display:

- AQI distribution
- Pollution summary
- Recent trends


## Data Source

Backend:

```
DashboardService.get_dashboard()
```

---

# 2. Summary Page

## Purpose

Display high-level statistics of the air quality system.

## API

```
GET /summary
```

## UI Components

Display:

- Total stations
- Average AQI
- Highest AQI location
- Lowest AQI location
- Pollution summary


---

# 3. Monitoring Stations Page

## Purpose

Display all available AQI monitoring stations.

## API

```
GET /stations
```

## UI Components

### Station Table / Cards

Display:

- Station name
- City
- State
- Latitude
- Longitude


Example:

```
Station:
Maninagar

City:
Ahmedabad

Coordinates:
23.012,72.589
```


## Future Enhancement

Display stations on an interactive map.

---

# 4. Station Details Page

## Purpose

Show detailed AQI information for a selected monitoring station.

## Input

```
station_id
```


## APIs Used

### Historical Data

```
GET /stations/{station_id}/history
```


### AQI Trend

```
GET /aqi-trend
```


## UI Components


### AQI Trend Chart

Display:

- AQI over time
- Date/time


### Pollutant Charts

Display:

- PM2.5
- PM10
- CO
- NO2
- SO2
- O3


### Weather Information

Display:

- Temperature
- Humidity
- Wind Speed
- Pressure


---

# 5. AQI Prediction Page

## Purpose

Display ML-based future AQI prediction.


## API

```
GET /ml/predict/{station_id}
```


## UI Components


### Prediction Card

Display:

```
Current AQI:
108


Predicted AQI:
105.48


Confidence:
92.36%


Category:
Unhealthy for Sensitive Groups
```


### Trend Information

Display:

Example:

```
Air quality is expected to remain stable.
```


### Health Advisory

Display:

Example:

```
Children, elderly and asthma patients
should reduce outdoor activity.
```


---

# 6. AQI History Page

## Purpose

Display historical AQI patterns.


## API

```
GET /ml/history/{station_id}
```


## UI Components


### Historical AQI Chart

Display:

- Timestamp
- AQI value


Example:

```
Date          AQI

22-Jun        114
23-Jun        108
24-Jun        120
```


---

# 7. Pollution Alerts Page

## Purpose

Display AQI-based warnings and recommendations.


## API

```
GET /alerts
```


## UI Components


Alert Cards:

Display:

- Location
- AQI value
- Severity
- Recommendation


Example:

```
⚠ High Pollution Alert

Location:
Ahmedabad

AQI:
220

Recommendation:
Avoid outdoor activities
```


---

# 8. Top Polluted Locations Page

## Purpose

Display locations with highest pollution levels.


## API

```
GET /top-polluted
```


## UI Components


Ranking Table:


```
Rank | City | AQI

1    | Delhi | 250
2    | Kolkata | 220
3    | Ahmedabad | 190
```


---

# 9. AQI Trend Page

## Purpose

Analyze AQI movement over selected periods.


## API

```
GET /aqi-trend
```


## Query Parameters


```
station_id
days
```


Example:

```
/aqi-trend?station_id=abc&days=30
```


## UI Components


Display:

- Line chart
- Date range filter
- AQI trend


---

# Frontend Navigation Structure


```
Application

|
|-- Dashboard
|
|-- Stations
|      |
|      |-- Station Details
|
|-- AQI Prediction
|
|-- AQI Trends
|
|-- Alerts
|
|-- Top Polluted Locations

```


---

# API Configuration


Backend Base URL:

```
http://localhost:8000
```


Environment Variable:


```
VITE_API_URL=http://localhost:8000
```


---

# API Summary


| Feature | API |
|---|---|
| Dashboard | GET /dashboard |
| Summary | GET /summary |
| Stations | GET /stations |
| Station History | GET /stations/{station_id}/history |
| AQI Trend | GET /aqi-trend |
| AQI Prediction | GET /ml/predict/{station_id} |
| AQI History | GET /ml/history/{station_id} |
| Alerts | GET /alerts |
| Top Polluted | GET /top-polluted |


---

# Future Frontend Enhancements

## Geospatial Dashboard

- AQI heatmap
- Station markers
- Pollution hotspot visualization


## AI Insights

- LLM-generated AQI explanations
- Natural language queries


## Advanced Analytics

- Pollution source attribution
- Weather impact analysis
- Multi-city comparison