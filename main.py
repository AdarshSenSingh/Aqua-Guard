import pandas as pd
import networkx as nx
from datetime import datetime
from src.core.simulator import DataSimulator, SARIMAModelTrainer  # Adjust the import path if necessary

def main():
    # Create the graph structure
    graph = nx.DiGraph()

    # Create the data simulator object and load temperature data from 'temp.csv'
    temp_file = 'temp.csv'  # Path to your temperature CSV file
    simulator = DataSimulator(graph, temp_file)

    # Add sensors to the graph (example: adding source, leaf sensors, and connecting them)
    simulator.add_sensor('source', initial_flow_rate=50, initial_temperature=25)  # Source sensor with flow and temp
    simulator.add_sensor('s1', parent_sensor='source', edge_weight=10, initial_flow_rate=45, initial_temperature=25)
    simulator.add_sensor('s2', parent_sensor='s1', edge_weight=15, initial_flow_rate=40, initial_temperature=25)
    simulator.add_sensor('s3', parent_sensor='s1', edge_weight=10, initial_flow_rate=42, initial_temperature=25)
    simulator.add_sensor('s4', parent_sensor='s2', edge_weight=20, initial_flow_rate=38, initial_temperature=25)
    simulator.add_sensor('s5', parent_sensor='s3', edge_weight=25, initial_flow_rate=39, initial_temperature=25)
    simulator.add_sensor('s6', parent_sensor='s4', edge_weight=18, initial_flow_rate=35, initial_temperature=25)
    simulator.add_sensor('s7', parent_sensor='s5', edge_weight=22, initial_flow_rate=36, initial_temperature=25)

    # Set initial conditions for the source node and leaf sensors
    leaf_conditions = {
        's1': (45, 25),
        's2': (40, 25),
        's3': (42, 25),
        's4': (38, 25),
        's5': (39, 25),
        's6': (35, 25),
        's7': (36, 25),
    }
    simulator.set_initial_conditions(source_flow_rate=50, source_temperature=25, leaf_conditions=leaf_conditions)

    # Generate data for a set of timestamps (e.g., a single timestamp for simplicity)
    timestamps = pd.date_range(datetime(2025, 1, 19), periods=1, freq='H')  # Example: generate data for one hour
    simulator.generate_data(timestamps)

    # Print generated data for inspection (optional)
    print("Generated flow data:", simulator.flow_data)
    print("Generated temperature data:", simulator.temperature_data)
    print("Generated pressure data:", simulator.pressure_data)

    # Train SARIMA models for each sensor
    trainer = SARIMAModelTrainer()
    for sensor_id, data in simulator.temperature_data.items():
        trainer.train(sensor_id, data)

    # Predict future values for each sensor (example: predicting 5 steps ahead)
    for sensor_id in simulator.temperature_data.keys():
        predictions = trainer.predict(sensor_id, 5)  # Adjust the number of steps as needed
        print(f"Predictions for sensor {sensor_id}: {predictions}")

if __name__ == '__main__':
    main()
# Before training, print the data length and a sample of the data
