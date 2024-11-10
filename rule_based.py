import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None


def cluster_analysis(df, num_clusters=3):
    X = df[['Amount']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X_scaled)
    df['Cluster'] = kmeans.labels_

    cluster_analysis = df.groupby(['Cluster', 'Category']).agg({'Amount': ['mean', 'std', 'count']})
    cluster_analysis.columns = ['Mean Amount', 'Standard Deviation', 'Number of Transactions']

    return cluster_analysis


def generate_recommendations(cluster_analysis):
    recommendations = {}
    for (cluster, category), data in cluster_analysis.iterrows():
        mean_amount = data['Mean Amount']
        std_deviation = data['Standard Deviation']
        count = data['Number of Transactions']

        if count == 0:
            recommendations[(cluster, category)] = "No spending detected in this category."
        else:
            if std_deviation < mean_amount * 0.25:
                recommendations[(cluster, category)] = "Your spending in this category is consistent. Keep it up!"
            elif std_deviation < mean_amount * 0.5:
                recommendations[(
                cluster, category)] = "Your spending in this category varies slightly. Monitor your expenses closely."
            else:
                recommendations[(cluster,
                                 category)] = "Your spending in this category fluctuates significantly. Consider setting a stricter budget."

    return recommendations


def main():
    file_path = 'personal_transactions1.csv'
    df = load_data(file_path)
    if df is None:
        return

    num_clusters = int(input("Enter the number of clusters: "))

    cluster_analysis_result = cluster_analysis(df, num_clusters)
    print("Cluster Analysis:")
    print(cluster_analysis_result)

    recommendations = generate_recommendations(cluster_analysis_result)
    print("\nRecommendations:")
    for (cluster, category), recommendation in recommendations.items():
        print(f"Cluster {cluster}, Category '{category}': {recommendation}")


if __name__ == "__main__":
    main()
