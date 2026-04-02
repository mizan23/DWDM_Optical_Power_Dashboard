# Gain Calculator

## Overview

Gain Calculator is a lightweight Flask application for calculating
optical amplifier gain values in DWDM environments.

## Features

-   Fast gain calculation
-   Simple UI
-   Dockerized
-   Useful for lab/NOC engineers

## Project Structure

    Gain_Calculator/
    ├── app.py
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    └── templates/

## Requirements

-   Docker
-   Docker Compose

## Run

``` bash
docker-compose up --build
```

Access: http://localhost:5000

## Use Case

-   Optical link tuning
-   Amplifier configuration validation
