# 🌍 Global Temperature Analysis

A Python data-analysis project exploring global temperature changes using historical weather station data from 1880 to 2021.

This project was developed as part of my Python programming and data-analysis practice. The goal is to use Python to investigate long-term temperature patterns, calculate temperature anomalies, and visualize changes in global temperature over time.

## 📊 Project Objectives

- Load and inspect historical temperature data
- Clean and organize climate data
- Calculate annual average temperatures
- Calculate temperature anomalies
- Analyze long-term temperature trends
- Calculate moving averages
- Compare temperature behavior across locations
- Visualize climate trends using Python

## 🗂️ Dataset

The dataset contains yearly temperature observations from weather stations around the world covering the period from 1880 to 2021.

The original data was compiled from publicly available climate datasets from NOAA.

## 🛠️ Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook

## 📚 Python Concepts Practiced

- Reading CSV files with Pandas
- DataFrame manipulation
- Handling missing values
- NumPy arrays
- Statistical calculations
- Rolling averages
- Linear trend analysis
- Data visualization
- Functions
- Data cleaning

## 📈 Analysis

### Global Temperature Trend

The project calculates the annual average temperature across available weather stations and examines the long-term trend from 1880 to 2021.

### Temperature Anomalies

Temperature anomalies are calculated relative to a baseline representing the estimated pre-industrial temperature level.

### Moving Average

A 10-year moving average is used to reduce short-term fluctuations and highlight the long-term temperature pattern.

### Long-Term Trend

A linear regression/trend calculation is used to estimate the rate of temperature change over the study period.

## 📁 Project Structure

```text
Day05_GlobalTemperatureAnalysis/
│
├── global_temperature_analysis.ipynb
├── README.md
│
└── data/
    └── global_temperature.csv
```

## ▶️ How to Run

Install the required packages:

```bash
pip install pandas numpy matplotlib jupyter
```

Then open the notebook:

```bash
jupyter notebook
```

Open:

```text
global_temperature_analysis.ipynb
```

and run the cells.

## 🚀 Future Improvements

- Add interactive geographical maps
- Analyze temperature trends by continent
- Compare different climate regions
- Add statistical significance testing
- Investigate relationships between temperature and extreme weather events
- Create an interactive dashboard
