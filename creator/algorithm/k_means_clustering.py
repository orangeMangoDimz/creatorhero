from sklearn.cluster import KMeans
import numpy as np

def k_means_clustering(arr_point):
    data = np.array(arr_point)
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(data)

    # centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    return labels
    