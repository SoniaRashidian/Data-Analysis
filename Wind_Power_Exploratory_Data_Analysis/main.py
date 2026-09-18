"""
Wind Power Data Analysis
Exploratory data analysis of the SDWPF wind turbine dataset.
Expected dataset: data/wtbdata_245days.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "data/wtbdata_245days.csv"

columns = [
    "TurbID", "Day", "Tmstamp", "Wspd (m/s)", "Wdir (°)",
    "Etmp (°C)", "Itmp (°C)", "Ndir (°)", "Pab1 (°)", "Pab2 (°)",
    "Pab3 (°)", "Prtv (kW)", "Patv (kW)"
]

# Load and inspect data
data = pd.read_csv(DATA_PATH)
data.columns = columns

print("Dataset shape:", data.shape)
print("\nFirst five rows:")
print(data.head())

# Missing-value analysis
missing_values = data.isnull().sum()
missing_percentage = (missing_values / len(data)) * 100

missing_summary = pd.DataFrame({
    "Missing Values": missing_values,
    "Missing (%)": missing_percentage.round(3)
})

print("\nMissing-value summary:")
print(missing_summary[missing_summary["Missing Values"] > 0])

clean_data = data.dropna().copy()

print("\nRows before cleaning:", len(data))
print("Rows after cleaning:", len(clean_data))
print("Rows removed:", len(data) - len(clean_data))

# Descriptive statistics
numerical_features = [
    "Wspd (m/s)", "Wdir (°)", "Etmp (°C)", "Itmp (°C)",
    "Ndir (°)", "Pab1 (°)", "Pab2 (°)", "Pab3 (°)",
    "Prtv (kW)", "Patv (kW)"
]

print("\nDescriptive statistics:")
print(clean_data[numerical_features].describe().round(3))

# Turbine-level active power
turbine_power = (
    clean_data.groupby("TurbID")["Patv (kW)"]
    .mean()
    .sort_values(ascending=False)
)

print("\nTop 10 turbines by mean active power:")
print(turbine_power.head(10))

# Correlation matrix
correlation = clean_data[numerical_features].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation, cmap="coolwarm", center=0)
plt.title("Correlation Matrix of Wind Turbine Features")
plt.tight_layout()
plt.show()

# Wind speed vs. active power
sample = clean_data.sample(n=min(10000, len(clean_data)), random_state=42)

plt.figure(figsize=(9, 6))
sns.scatterplot(
    data=sample,
    x="Wspd (m/s)",
    y="Patv (kW)",
    alpha=0.35
)
plt.title("Wind Speed vs. Active Power")
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Active Power (kW)")
plt.tight_layout()
plt.show()

# Time-series analysis
# Day 1 corresponds to May 1, 2020 in the SDWPF dataset.
clean_data["Datetime"] = (
    pd.to_datetime("2020-05-01")
    + pd.to_timedelta(clean_data["Day"] - 1, unit="D")
    + pd.to_timedelta(clean_data["Tmstamp"] + ":00")
)

selected_turbine = turbine_power.index[0]

turbine_data = (
    clean_data[clean_data["TurbID"] == selected_turbine]
    .sort_values("Datetime")
)

plt.figure(figsize=(12, 5))
plt.plot(
    turbine_data["Datetime"],
    turbine_data["Patv (kW)"],
    linewidth=0.8
)
plt.title(f"Active Power Time Series - Turbine {selected_turbine}")
plt.xlabel("Date")
plt.ylabel("Active Power (kW)")
plt.tight_layout()
plt.show()

print("\nAnalysis completed successfully.")
print(f"Number of turbines: {clean_data['TurbID'].nunique()}")
print(f"Observations after cleaning: {len(clean_data)}")
print(f"Selected turbine: {selected_turbine}")
