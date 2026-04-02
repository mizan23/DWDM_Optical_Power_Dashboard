# DWDM Optical Power Dashboard

## 📌 Overview

A lightweight, Dockerized toolkit for DWDM (Dense Wavelength Division
Multiplexing) optical network operations.\
This project provides two independent web applications:

-   **Gain Calculator** → Helps calculate amplifier gain values quickly
-   **OA Dashboard** → Visual interface for monitoring Optical
    Amplifiers (OA)

Designed for lab, NOC, and field engineers working with Huawei NCE /
DWDM environments.

------------------------------------------------------------------------

## 🧱 Architecture

    User (Browser)
       │
       ├── Gain Calculator (Flask + Docker)
       │       └── Gain Computation Logic
       │
       └── OA Dashboard (Flask + Docker)
               └── UI + Visualization Layer

Both services are containerized and can run independently.

------------------------------------------------------------------------

## 📁 Project Structure

    DWDM_Optical_Power_Dashboard/
    │
    ├── Gain_Calculator/
    │   ├── app.py
    │   ├── Dockerfile
    │   ├── docker-compose.yml
    │   ├── requirements.txt
    │   └── templates/
    │
    ├── OA-dashboard/
    │   ├── app.py
    │   ├── Dockerfile
    │   ├── docker-compose.yml
    │   ├── requirements.txt
    │   ├── static/
    │   └── templates/
    │
    └── README.md

------------------------------------------------------------------------

## ⚙️ Features

### Gain Calculator

-   Input optical parameters
-   Compute amplifier gain
-   Simple and fast UI
-   Lightweight Flask backend

### OA Dashboard

-   Visual representation of optical amplifiers
-   Clean UI with static assets
-   Ready for future real-time integration

------------------------------------------------------------------------

## 🐳 Requirements

-   Docker
-   Docker Compose
-   Git

------------------------------------------------------------------------

## 🚀 Getting Started

### 1. Clone Repository

``` bash
git clone https://github.com/your-username/DWDM_Optical_Power_Dashboard.git
cd DWDM_Optical_Power_Dashboard
```

------------------------------------------------------------------------

### 2. Run Gain Calculator

``` bash
cd Gain_Calculator
docker-compose up --build
```

Access:

    http://localhost:5000

------------------------------------------------------------------------

### 3. Run OA Dashboard

``` bash
cd OA-dashboard
docker-compose up --build
```

Access:

    http://localhost:5001

------------------------------------------------------------------------

## 🔧 Configuration

You can modify ports inside:

-   `docker-compose.yml`

Example:

    ports:
      - "5002:5000"

------------------------------------------------------------------------

## ⚠️ Important Notes

## 📊 Future Enhancements

-   🔗 Integrate with Huawei NCE APIs
-   📡 SNMP / Kafka real-time data ingestion
-   📈 Historical power trend graphs
-   🔐 Authentication & role-based access
-   🧩 Merge into single unified dashboard

------------------------------------------------------------------------

## 🧪 Use Cases

-   DWDM lab testing
-   Optical amplifier tuning
-   NOC monitoring tools
-   Training/demo environment

------------------------------------------------------------------------

## 🤝 Contributing

1.  Fork the repo
2.  Create a new branch
3.  Commit your changes
4.  Open a Pull Request

------------------------------------------------------------------------

## 📄 License

MIT License

------------------------------------------------------------------------

## 👤 Author

**Mizanur Rahman**

------------------------------------------------------------------------

## ⭐ Support

If this project helps you, consider giving it a ⭐ on GitHub!
