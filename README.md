# Desktop Weather Dashboard (M602 Computer Programming)

**Student:** Ankitkumar Rajubhai Patel  
**Degree Programme:** Master of Engineering in Computer Science  
**University:** Gisma University of Applied Sciences  
**Module:** M602 – Computer Programming (Task 3: Weather Dashboard)

---

## Project Overview

A Python-based desktop Weather Dashboard application built with Object-Oriented Programming (OOP) principles. The application connects to the OpenWeatherMap RESTful API to fetch live meteorological conditions and 24-hour temperature forecasts, renders interactive trend charts inside a Tkinter GUI, and persists favorite cities locally using JSON file handling.

---

## Features

* **Real-Time Weather Telemetry:** Displays current temperature (°C), feels-like temperature, weather condition summary, relative humidity (%), atmospheric pressure (hPa), and wind speed (m/s).
* **24-Hour Temperature Trend Chart:** Embedded Matplotlib line plot displaying forecasted temperatures across 3-hour intervals directly inside the desktop window.
* **Persistent Favorite Cities:** Save, deduplicate, and reload favorite locations across sessions via `favorites.json`.
* **Defensive Error Handling:** Gracefully handles empty user inputs, invalid/unregistered city names (HTTP 404), network disconnects/timeouts, and missing or corrupted JSON files.

---

## Project Structure

```text
M602B-Computer-Programming-WS0926-/
├── main.py            # Application entry point and Tkinter root loop
├── gui.py             # Tkinter UI components and embedded Matplotlib canvas
├── models.py          # WeatherReport data model and WeatherFetcher API client
├── storage.py         # FavoritesStorage class for JSON file I/O persistence
├── favorites.json     # Local JSON storage for saved cities
└── README.md          # Project documentation and setup guide
