# OA Dashboard

## Overview

OA Dashboard is a Flask-based web application designed to visualize and
monitor Optical Amplifiers (OA) in DWDM networks.

## Features

-   Simple and clean UI
-   Visualization-ready structure
-   Dockerized deployment
-   Extendable for real-time data (NCE, SNMP, Kafka)

## Project Structure

    OA-dashboard/
    ├── app.py
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    ├── static/
    └── templates/

## Requirements

-   Docker
-   Docker Compose

## Run

``` bash
docker-compose up --build
```

Access: http://localhost:5001

## Future Improvements

-   Real-time telemetry integration
-   Graphs for optical power levels
-   Alarm correlation view
