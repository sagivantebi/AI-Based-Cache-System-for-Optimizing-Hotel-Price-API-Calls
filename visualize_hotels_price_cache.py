import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import numpy as np

# Load the CSV file
csv_file_path = 'hotel_losses_201.csv'
df = pd.read_csv(csv_file_path)

# Convert the dataframe from wide to long format for better visualization
df_long = pd.melt(df, id_vars=['Hotel/Vendor'], var_name='Vendor', value_name='Loss')

def visualize_top_vendors(df_long, top_n=10):
    """
    Visualize the top N vendors with the highest average loss.
    :param df_long: The long format DataFrame.
    :param top_n: Number of top vendors to display.
    """
    # Calculate the average loss per vendor
    avg_loss_per_vendor = df_long.groupby('Vendor')['Loss'].mean()

    # Select the top N vendors by average loss
    top_vendors = avg_loss_per_vendor.nlargest(top_n).index

    # Filter the dataframe to include only the top vendors
    df_top_vendors = df_long[df_long['Vendor'].isin(top_vendors)]

    # Plot 1: Bar plot showing the total loss per hotel for top vendors
    plt.figure(figsize=(12, 8))
    sns.barplot(data=df_top_vendors, x='Hotel/Vendor', y='Loss', hue='Vendor', ci=None)
    plt.title(f'Total Loss per Hotel by Top {top_n} Vendors')
    plt.xticks(rotation=90)
    plt.ylabel('Loss')
    plt.xlabel('Hotel/Vendor')
    plt.legend(title='Vendor')
    plt.tight_layout()
    plt.show()

    # Plot 2: Box plot showing the distribution of losses across top vendors
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_top_vendors, x='Vendor', y='Loss')
    plt.title(f'Distribution of Losses by Top {top_n} Vendors')
    plt.ylabel('Loss')
    plt.xlabel('Vendor')
    plt.tight_layout()
    plt.show()

def visualize_clustered_vendors(df, num_clusters=10):
    """
    Visualize vendors clustered by their loss profiles.
    :param df: The original wide format DataFrame.
    :param num_clusters: Number of clusters for KMeans.
    """
    # Calculate the average loss per vendor per hotel
    vendor_hotel_matrix = df.set_index('Hotel/Vendor').T  # Transpose the DataFrame

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    clusters = kmeans.fit_predict(vendor_hotel_matrix)

    # Add cluster information to the DataFrame
    vendor_cluster_map = {vendor: cluster for vendor, cluster in zip(vendor_hotel_matrix.index, clusters)}
    df_long['Cluster'] = df_long['Vendor'].map(vendor_cluster_map)

    # Plot 1: Box plot showing the distribution of losses by cluster
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_long, x='Cluster', y='Loss')
    plt.title('Distribution of Losses by Cluster')
    plt.ylabel('Loss')
    plt.xlabel('Cluster')
    plt.tight_layout()
    plt.show()

    # Plot 2: Heatmap showing the average loss per hotel and cluster
    df_long_cluster_avg = df_long.groupby(['Hotel/Vendor', 'Cluster'])['Loss'].mean().unstack().fillna(0)
    plt.figure(figsize=(12, 10))
    sns.heatmap(df_long_cluster_avg, annot=True, fmt=".1f", cmap="YlGnBu")
    plt.title('Heatmap of Average Losses by Hotel and Cluster')
    plt.xlabel('Cluster')
    plt.ylabel('Hotel/Vendor')
    plt.tight_layout()
    plt.show()

# Visualize Top Vendors
visualize_top_vendors(df_long, top_n=10)

# Visualize Clustered Vendors
visualize_clustered_vendors(df, num_clusters=10)
