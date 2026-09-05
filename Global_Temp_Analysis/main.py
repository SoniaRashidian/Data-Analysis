import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
temperature_data = pd.read_csv("data/global_temperature.csv")

# Extract yearly temperature columns
years = list(range(1880, 2022))
temperature = temperature_data[years]

# Calculate global average temperature for each year
global_average = temperature.mean(axis=0)

# Create a DataFrame
global_temperature = pd.DataFrame({
    "Year": years,
    "Temperature": global_average.values
})

# Calculate 10-year moving average
global_temperature["Moving_Average"] = (
    global_temperature["Temperature"]
    .rolling(window=10)
    .mean()
)

# Calculate baseline
baseline = global_temperature[
    global_temperature["Year"].between(1981, 2010)
]["Temperature"].mean() - 0.69

# Calculate temperature anomaly
global_temperature["Anomaly"] = (
    global_temperature["Temperature"] - baseline
)

print(global_temperature.head())
print(f"Baseline temperature: {baseline:.2f} °C")

plt.figure(figsize=(12, 6))

plt.plot(
    global_temperature["Year"],
    global_temperature["Temperature"],
    label="Annual Average"
)

plt.plot(
    global_temperature["Year"],
    global_temperature["Moving_Average"],
    label="10-Year Moving Average",
    linewidth=3
)

plt.xlabel("Year")
plt.ylabel("Temperature (°C)")
plt.title("Global Temperature Change, 1880–2021")
plt.legend()
plt.grid(True)

plt.show()

plt.figure(figsize=(12, 6))

plt.bar(
    global_temperature["Year"],
    global_temperature["Anomaly"]
)

plt.axhline(0, linewidth=1)

plt.xlabel("Year")
plt.ylabel("Temperature Anomaly (°C)")
plt.title("Global Temperature Anomalies Relative to Baseline")

plt.show()
