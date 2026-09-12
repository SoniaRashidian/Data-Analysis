# 🌬️ Wind Power Exploratory Data Analysis

A Python data-analysis project exploring wind turbine operational data from a wind farm in China.

This project focuses on exploratory data analysis (EDA), data quality assessment, statistical summaries, visualization, and understanding the relationship between wind conditions and wind power generation.

## 📊 Project Overview

The dataset contains measurements from **134 wind turbines** in a wind farm and covers approximately 245 days of operation.

The main variables include:

* Wind speed
* Wind direction
* External temperature
* Internal turbine temperature
* Nacelle direction
* Blade pitch angles
* Reactive power
* Active power

`Patv (kW)` — active power — is treated as the main output variable for the analysis.

## 🎯 Objectives

* Load and inspect wind turbine data
* Identify and quantify missing values
* Calculate descriptive statistics
* Investigate data quality and potential sensor errors
* Explore distributions of wind turbine variables
* Analyze relationships between variables
* Examine the relationship between wind speed and active power
* Analyze turbine behavior over time
* Identify patterns that could support future wind power prediction

## 🛠️ Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Jupyter Notebook

## 📚 Python Concepts Practiced

* Reading CSV data with Pandas
* DataFrame manipulation
* Missing-value analysis
* Data cleaning
* Descriptive statistics
* Data filtering
* Grouping and aggregation
* Statistical correlation
* Data visualization
* Histograms
* Box plots
* Violin plots
* Scatterplots
* Pairplots
* Time-series visualization

## 🔍 Analysis

### Missing Values

The dataset contains missing observations across the numerical measurement variables. Missing-value analysis is performed before continuing with the exploratory analysis.

### Descriptive Statistics

Summary statistics are calculated for the numerical variables to investigate their central tendency, variability, and range.

### Wind Speed and Power

The relationship between wind speed and active power is investigated using scatterplots. This provides insight into how changes in wind conditions relate to electricity generation.

### Correlation Analysis

A Pearson correlation matrix is used to examine linear relationships between the numerical variables.

### Time-Series Analysis

The day and timestamp information are converted into a datetime representation to investigate how turbine measurements change over time.

## 📁 Project Structure

```text
Day06_WindPowerExploratoryAnalysis/
│
├── wind_power_exploration.ipynb
├── README.md
│
└── data/
    └── wtbdata_245days.csv
```

## ▶️ How to Run

Install the required Python packages:

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

Launch Jupyter Notebook:

```bash
jupyter notebook
```

Then open:

```text
wind_power_exploration.ipynb
```

## 🚀 Future Improvements

* Develop a wind power prediction model
* Compare machine-learning algorithms
* Engineer additional time-based features
* Investigate turbine-level performance differences
* Detect anomalous turbine behavior
* Evaluate prediction accuracy using appropriate performance metrics
* Develop an interactive wind-power dashboard

## 👩‍💻 Author

Created by **Sono** as part of my Python programming and data-analysis practice.
