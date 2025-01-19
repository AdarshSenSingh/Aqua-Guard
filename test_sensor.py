from src.clustering.clustering_logic import ClusteringManager

def test_clustering():
    clustering_manager = ClusteringManager()

    # Add sensors
    clustering_manager.add_sensor('sensor1', (10, 20))
    clustering_manager.add_sensor('sensor2', (15, 25))
    clustering_manager.add_sensor('sensor3', (30, 40))
    clustering_manager.add_sensor('sensor4', (50, 60))

    # Check initial clusters
    initial_clusters = clustering_manager.get_clusters()

    # Remove a sensor and check clusters again
    clustering_manager.remove_sensor('sensor2')
    updated_clusters = clustering_manager.get_clusters()

    return initial_clusters, updated_clusters

# Run the test
if __name__ == "__main__":
    initial, updated = test_clustering()
    print("Initial Clusters:", initial)
    print("Updated Clusters after removing sensor2:", updated)
