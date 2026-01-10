# HES Project (Human Exploitability System)

**Initiated by Zeron [zeron.one] Research Team**

## Overview

The **Human Exploitability System (HES)** is a research project designed to assess and quantify human risk in cybersecurity contexts. By analyzing physiological and behavioral signals, the system calculates a real-time "exploitability score" that reflects an individual's susceptibility to social engineering and other security threats.

This project combines a Python-based analysis engine with a React-based frontend to visualize risk metrics, state dominance, and potential exploit scenarios.

## Features

- **Real-time Scoring**: Calculates risk scores based on live or synthetic signal inputs.
- **Signal Normalization**: Processes raw data (heart rate, typing speed, etc.) into normalized metrics.
- **State Analysis**: Identifies dominant user states (e.g., Stress, Fatigue, Focus) using weighted mappings.
- **Contextual Multipliers**: Adjusts scores based on time of day, session length, and environmental noise.
- **Exploit Scenarios**: Predicts specific vulnerability scenarios (e.g., "Phishing Susceptibility") based on the calculated state and score.
- **Interactive UI**: A modern dashboard for visualizing risk profiles and simulation results.

## Technology Stack

- **Backend**: Python, FastAPI
- **Frontend**: React, Vite
- **Data**: JSON configuration for signals and mappings

## Documentation

Comprehensive documentation for the project is available in the `docs/` directory:

- [**Home**](docs/Home.md): Welcome and introduction.
- [**Architecture**](docs/Architecture.md): System design and component data flow.
- [**Models & Logic**](docs/Models.md): Detailed explanation of the scoring algorithms and rule-based models.
- [**API Reference**](docs/API.md): Documentation for backend endpoints.

## Installation & Usage

### Prerequisites

- Python 3.8+
- Node.js & npm

### Backend Setup

1. Navigate to the project root.
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the API server:
   ```bash
   python -m uvicorn api.app:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the `ui` directory:
   ```bash
   cd ui
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The application will be accessible at `http://localhost:5173` (or the port shown in the terminal).

## Project Structure

- `api/`: FastAPI application and route definitions.
- `core/`: Core logic for session management and risk scoring.
- `ui/`: React frontend application.
- `utils/`: Helper functions for normalization and parsing.
- `constants/`: Configuration files for mappings and modifiers.

## Credits

This project is an initiative of the **Zeron Research Team**.

### Contributors
- [AYUSHSHARMA9817](https://github.com/AYUSHSHARMA9817)
- [srinjoy-zeron](https://github.com/srinjoy-zeron)
- [adevansh078](https://github.com/adevansh078)
- [KrishRandar](https://github.com/KrishRandar)
- [faux16](https://github.com/faux16)

