Wind Power Data Analysis

A Python-based exploratory data analysis (EDA) project using the Spatial Dynamic Wind Power Forecasting (SDWPF) dataset. The project demonstrates practical data loading, cleaning, statistical analysis, aggregation, visualization, and time-series preparation using Python.

Project Overview

This project was completed as a Python and data-analysis practice project using real-world wind-turbine operational data.

The SDWPF dataset contains observations from 134 wind turbines in a wind farm in China. The variables include meteorological conditions, turbine-control measurements, reactive power, and active power. In the original analysis, Patv (kW) — active power — is the target variable for prediction. 

The original exploratory workflow covered package import, dataset loading, missing-value analysis, descriptive statistics, turbine selection, and several visualization techniques including histograms, box/violin plots, scatterplots, pairplots, correlation matrices, and time-series plots. 

This repository presents a cleaned, independent Python script extracted from that analysis workflow.

Dataset

The dataset contains information from 134 turbines and includes the following variables: 

Variable

Description

TurbID

Wind turbine identification number

Day

Day of the observation

Tmstamp

Measurement time

Wspd (m/s)

Wind speed

Wdir (°)

Wind direction

Etmp (°C)

External/environmental temperature

Itmp (°C)

Internal turbine temperature

Ndir (°)

Nacelle direction

Pab1 (°)

Blade 1 pitch angle

Pab2 (°)

Blade 2 pitch angle

Pab3 (°)

Blade 3 pitch angle

Prtv (kW)

Reactive power

Patv (kW)

Active power

Data Quality

The original dataset contains 4,727,520 rows. The analysis identified 49,518 rows containing missing values, corresponding to approximately 1.047% of the dataset. fileciteturn0file0L191-L210

For this practice analysis, rows containing missing values are removed before the statistical and visualization steps.

The original workflow also noted unusually negative temperature values that were likely caused by sensor errors; the original exercise provided an interpolation option for visualizing these temperature time series.

Analysis Performed

1. Data Loading and Inspection

The project loads the CSV file with Pandas, assigns descriptive column names, and inspects the dataset structure and first observations.

2. Missing-Value Analysis

Missing values are counted for each feature and their percentage of the dataset is calculated.

missing_values = data.isnull().sum()
missing_percentage = (missing_values / len(data)) * 100

Rows containing missing values are then removed for the subsequent analysis.

3. Descriptive Statistics

The numerical variables are summarized using:

clean_data[numerical_features].describe()

The resulting statistics include count, mean, standard deviation, minimum, quartiles, and maximum values. 

4. Turbine-Level Analysis

Mean active power is calculated for each turbine and the turbines are ordered by average power output.

clean_data.groupby("TurbID")["Patv (kW)"].mean()

The original exercise also used a subset of 10 higher-performing turbines for detailed exploration. 

5. Correlation Analysis

A Pearson correlation matrix is generated for the numerical variables to investigate relationships among wind speed, temperatures, turbine-control variables, reactive power, and active power.

6. Wind Speed vs. Active Power

A scatterplot is used to explore the relationship between wind speed and active power. This is particularly relevant to wind-energy analysis because wind speed is an important factor associated with turbine power production. The original exercise specifically highlights investigation of relationships with Patv (kW). 

7. Time-Series Analysis

The original dataset stores the day and measurement time separately. These fields are combined into a datetime variable for time-series analysis. The source material specifies that Day 1 corresponds to May 1, 2020. 

The script then plots active power over time for one selected turbine.

Python Skills Demonstrated

Python programming

Pandas

Matplotlib

Seaborn

Data loading and inspection

Missing-value analysis

Data cleaning

Descriptive statistics

groupby() aggregation

Correlation analysis

Data visualization

Time-series preparation

Exploratory Data Analysis (EDA)

Project Structure

wind-power-data-analysis/
│
├── data/
│   └── wtbdata_245days.csv
│
├── wind_power_analysis.py
│
└── README.md

Note: The raw SDWPF dataset is large. For GitHub, it is preferable to keep the dataset out of the repository and provide the official/source link instead, unless its redistribution terms permit you to upload it.

How to Run

Install the required packages:

pip install pandas matplotlib seaborn

Place the dataset at:

data/wtbdata_245days.csv

Then run:

python wind_power_analysis.py

The script prints the main data-quality and statistical results and generates visualizations for the correlation matrix, wind-speed/power relationship, and active-power time series.

Analysis Workflow

Raw Wind-Turbine Data
        ↓
Data Inspection
        ↓
Missing-Value Analysis
        ↓
Data Cleaning
        ↓
Descriptive Statistics
        ↓
Turbine-Level Aggregation
        ↓
Correlation Analysis
        ↓
Wind Speed / Power Analysis
        ↓
Time-Series Analysis

Learning Outcome

This project provided practical experience in moving from raw operational data to structured exploratory analysis.

It demonstrates how Python can be used to:

assess data quality,

identify and handle missing observations,

summarize large datasets statistically,

compare turbine-level performance,

investigate relationships between variables,

visualize power-generation behavior, and

prepare operational data for subsequent predictive modelling.

The project therefore serves as a foundation for a later wind-power prediction workflow.

Source

The analysis is based on the Spatial Dynamic Wind Power Forecasting (SDWPF) dataset and the associated exploratory-analysis learning material. The provided material describes the dataset as containing data from 134 wind turbines and links to the SDWPF research paper.

Research paper:

https://arxiv.org/abs/2208.04360

Portfolio Context

This repository represents a Python and data-analysis practice project focused on exploratory analysis of wind-energy data.

It demonstrates practical experience with a real-world energy dataset and complements broader interests in data analysis, optimization, quantitative modelling, risk-aware decision-making, and energy systems.
