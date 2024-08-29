import os
import json
import numpy as np
from sklearn.cluster import KMeans

# Configuration
main_folder = 'hotel_data_changes_quality.json'
new_folder_name = 'changes_by_vendor_ttt_los'
new_cluster_folder = 'clustered_data_by_vendor_ttt_los'
folder_single_values = 'single_values_by_vendor_ttt_los'

# Global dictionary to hold hotel data
hotel_data = {}

def load_json_data(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON from {file_path}: {e}")
        return None

def save_json_data(file_path, data):
    """Save JSON data to a file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving JSON to {file_path}: {e}")

def create_data_for_clustering():
    """Organize hotel data into files based on vendor, ttt, and los."""
    data = load_json_data(main_folder)
    if not data:
        return

    for key, value in data.items():
        # Split key into hotel, vendor, ttt, and los
        hotel, vendor, ttt, los = key.split('_')
        folder = f'{vendor}_{ttt}_{los}'
        new_entry = {hotel: value}
        
        if folder in hotel_data:
            hotel_data[folder].append(new_entry)
        else:
            hotel_data[folder] = [new_entry]
        
    # Create the new folder if it doesn't exist
    os.makedirs(new_folder_name, exist_ok=True)
    
    # Save each folder's data to a JSON file
    for key, value in hotel_data.items():
        print(f"Processing: {key}")
        new_path = os.path.join(new_folder_name, f"{key}.json")
        save_json_data(new_path, value)

def checks():
    """Perform checks on the data to identify files with specific conditions."""
    all_files = len(os.listdir(new_folder_name))
    less_than_10 = 0
    over_50 = 0
    over_30 = 0

    for file in os.listdir(new_folder_name):
        data = load_json_data(os.path.join(new_folder_name, file))
        if not data:
            continue

        length = len(data)
        if length < 10:
            less_than_10 += 1
        if length > 50:
            print(f"Over 50 entries: {file}")
            over_50 += 1
        if length > 30:
            over_30 += 1

    print(f"Total files: {all_files}")
    print(f"Files with less than 10 entries: {less_than_10}")
    print(f"Files with over 30 entries: {over_30}")
    print(f"Files with over 50 entries: {over_50}")

def switch_data_from_array_to_singular_value(percentile=40):
    """Convert array data to singular values based on the specified percentile."""
    os.makedirs(folder_single_values, exist_ok=True)

    for file in os.listdir(new_folder_name):
        print(f"Processing: {file}")
        data = load_json_data(os.path.join(new_folder_name, file))
        if not data:
            continue

        new_list = []
        for hotel_and_array in data:
            key = list(hotel_and_array.keys())[0]
            value = hotel_and_array[key]
            percentile_data = int(np.percentile(value, percentile))
            new_list.append({key: percentile_data})
        
        new_path_file = os.path.join(folder_single_values, file)
        save_json_data(f"{new_path_file}.json", new_list)

def cluster_data(data, n_clusters=4):
    """Cluster the provided data using KMeans."""
    values = np.array(list(data.values())).reshape(-1, 1)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(values)
    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_

    clusters = {key: int(label) for key, label in zip(data.keys(), labels)}
    return clusters, cluster_centers

def cluster_files():
    """Cluster data from each vendor-ttt-los file."""
    os.makedirs(new_cluster_folder, exist_ok=True)

    for file in os.listdir(new_folder_name):
        print(f"Clustering: {file}")
        data = load_json_data(os.path.join(new_folder_name, file))
        if not data:
            continue

        combined_data = {k: v for d in data for k, v in d.items()}
        clusters_2, _ = cluster_data(combined_data, n_clusters=2)
        clusters_4, _ = cluster_data(combined_data, n_clusters=4)

        new_path = os.path.join(new_cluster_folder, f"{file}.json")
        save_json_data(new_path, [clusters_2, clusters_4])

def cluster_the_single_value_data():
    """Cluster single-value data for each vendor-ttt-los file."""
    os.makedirs(new_cluster_folder, exist_ok=True)

    for file in os.listdir(folder_single_values):
        print(f"Clustering single-value data: {file}")
        data = load_json_data(os.path.join(folder_single_values, file))
        if not data:
            continue

        combined_data = {k: v for d in data for k, v in d.items()}
        if len(combined_data) < 10:
            continue

        clusters_4, cluster_centers = cluster_data(combined_data, n_clusters=4)

        file_split = file.split('.json')[0]
        new_path = os.path.join(new_cluster_folder, f"{file_split}.json")

        json_list_to_file = [clusters_4, {i: center[0] for i, center in enumerate(cluster_centers)}]
        save_json_data(new_path, json_list_to_file)

# Run the desired functions
# create_data_for_clustering()
# checks()
# switch_data_from_array_to_singular_value()
# cluster_files()
# cluster_the_single_value_data()
