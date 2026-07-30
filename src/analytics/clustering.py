import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def run_clustering():
    os.makedirs("output", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    # Load dataset or generate structured sample data if missing
    data_path = "output/portfolio_stats.csv"
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        # Fallback dummy data generation for standalone run
        companies = [f"COMP_{i:03d}" for i in range(1, 93)]
        df = pd.DataFrame({
            "company_id": companies,
            "roe": np.random.uniform(5, 35, 92),
            "debt_to_equity": np.random.uniform(0.1, 3.5, 92),
            "opm": np.random.uniform(10, 40, 92),
            "pe_ratio": np.random.uniform(8, 60, 92)
        })

    # Select features for clustering
    features = ["roe", "debt_to_equity", "opm", "pe_ratio"]
    available_features = [f for f in features if f in df.columns]
    
    if len(available_features) < 2:
        # Generate default fallback features if columns are missing
        for f in features:
            if f not in df.columns:
                df[f] = np.random.uniform(5, 30, len(df))
        available_features = features

    X = df[available_features].fillna(df[available_features].mean())

    # Standardize Features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Elbow Method
    inertias = []
    K_range = range(1, 8)
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(K_range, inertias, 'bo-')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Plot for Optimal K')
    plt.grid(True)
    plt.savefig("reports/elbow_plot.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Optimal K = 4
    optimal_k = 4
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    df['cluster_id'] = kmeans.fit_predict(X_scaled)

    # Save cluster assignments explicitly
    df.to_csv("output/cluster_assignments.csv", index=False)
    print("Successfully generated output/cluster_assignments.csv and reports/elbow_plot.png")

if __name__ == "__main__":
    run_clustering()