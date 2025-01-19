import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load existing data
csv_file = 'training_data.csv'
existing_data = pd.read_csv(csv_file, parse_dates=['timestamp'])

# Identify the last timestamp in the existing data
last_timestamp = existing_data['timestamp'].max()

# Generate data up to the current time
current_time = datetime.now()
timestamps = pd.date_range(start=last_timestamp + timedelta(hours=1), end=current_time, freq='h')

# Existing constants and graph configuration
graph_config = {
    'source': ['s1'],
    's1': ['s2', 's3'],
    's2': ['s4', 's5'],
    's3': ['s6', 's7'],
    's4': ['consumption1'],
    's5': ['consumption2'],
    's6': ['consumption3'],
    's7': ['consumption4'],
}
flow_capacity = {
    ('source', 's1'): 100,
    ('s1', 's2'): 80,
    ('s1', 's3'): 90,
    ('s2', 's4'): 70,
    ('s2', 's5'): 60,
    ('s3', 's6'): 50,
    ('s3', 's7'): 40,
}
k1 = 0.1
k2 = 0.05
base_pressure = 50

# Function to generate temperature data
def generate_temperature_data(timestamps):
    temperatures = []
    for timestamp in timestamps:
        base_temp = 15 + 10 * np.sin(2 * np.pi * (timestamp.timetuple().tm_yday / 365))
        noise = np.random.normal(0, 2)
        temperatures.append(base_temp + noise)
    return temperatures

# Function to calculate pressure
def calculate_pressure(flow_rate, temperature):
    return max(base_pressure + k1 * flow_rate + k2 * (temperature - 20), 0)

# Generate new data
data = []
for timestamp in timestamps:
    is_peak_hour = 9 <= timestamp.hour < 12
    is_peak_day = timestamp.weekday() == 6

    flow_rates = {'source': 100}
    temperatures = {}
    pressures = {}

    for node in graph_config.keys():
        if node not in ['source'] + [f'consumption{i}' for i in range(1, 5)]:
            temperatures[node] = generate_temperature_data([timestamp])[0]

    for parent, children in graph_config.items():
        for child in children:
            flow_rate = min(flow_rates[parent], flow_capacity.get((parent, child), float('inf')))
            if is_peak_hour:
                flow_rate *= 1.2
            if is_peak_day:
                flow_rate *= 1.5
            flow_rates[child] = flow_rate

            if child not in [f'consumption{i}' for i in range(1, 5)]:
                pressures[child] = calculate_pressure(flow_rate, temperatures[child])

    for sensor in flow_rates.keys():
        if sensor not in ['source'] + [f'consumption{i}' for i in range(1, 5)]:
            data.append({
                'timestamp': timestamp,
                'sensor': sensor,
                'flow_rate': flow_rates[sensor],
                'temperature': temperatures[sensor],
                'pressure': pressures[sensor],
            })

# Convert new data to DataFrame
new_data = pd.DataFrame(data)

# Combine and save updated data
updated_data = pd.concat([existing_data, new_data])
updated_data.to_csv(csv_file, index=False)

print(f"Data extended to {current_time}. CSV file updated: {csv_file}")
