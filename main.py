import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

from ag_feature_selection import FeatureSelectionGA
from ag_hyperparameters import HyperparameterGA
from ag_clustering import ClusteringGA

def main():
    print("Iniciando Pipeline de Optimizacion...")
    os.makedirs("outputs", exist_ok=True)

    if not os.path.exists("sdss_sample.csv") or len(pd.read_csv("sdss_sample.csv")) < 50:
        print("Generando dataset de muestra sdss_sample.csv...")
        np.random.seed(42)
        n = 300
        df_dummy = pd.DataFrame({
            'u': np.random.normal(18, 2, n),
            'g': np.random.normal(17, 2, n),
            'r': np.random.normal(16, 2, n),
            'i': np.random.normal(15, 2, n),
            'z': np.random.normal(14, 2, n),
            'redshift': np.random.uniform(0, 2, n),
            'class': np.random.choice(['GALAXY', 'STAR', 'QSO'], n)
        })
        df_dummy.to_csv("sdss_sample.csv", index=False)

    df = pd.read_csv("sdss_sample.csv")

    # Modulo 1: Seleccion de caracteristicas
    print("Ejecutando Modulo 1: Seleccion de Caracteristicas (GA)...")
    X_fs = df[['u', 'g', 'r', 'i', 'z', 'redshift']]
    y_fs = df['class']
    ga_fs = FeatureSelectionGA(X_fs, y_fs)
    best_chrom, best_acc, best_hist, avg_hist = ga_fs.run()

    plt.figure()
    plt.plot(best_hist, label='Best Fitness')
    plt.plot(avg_hist, label='Avg Fitness')
    plt.title('Feature Selection GA Convergence')
    plt.legend()
    plt.savefig('outputs/fs_convergence.png')
    plt.close()

    cols = np.where(best_chrom == 1)[0]
    X_sub = X_fs.iloc[:, cols]
    X_tr, X_te, y_tr, y_te = train_test_split(X_sub, y_fs, test_size=0.3, random_state=42)
    clf = KNeighborsClassifier(n_neighbors=5).fit(X_tr, y_tr)
    cm = confusion_matrix(y_te, clf.predict(X_te))

    plt.figure()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.savefig('outputs/fs_confusion_matrix.png')
    plt.close()

    # Modulo 2: Optimizacion de hiperparametros
    print("Ejecutando Modulo 2: Optimizacion de Hiperparametros (GA)...")
    X_hp = df[['u', 'g', 'r', 'i', 'z']]
    y_hp = df['redshift']
    ga_hp = HyperparameterGA(X_hp, y_hp)
    best_k, best_mse, best_r2, hp_hist = ga_hp.run()

    plt.figure()
    plt.plot(hp_hist)
    plt.title('Hyperparameter Optimization Convergence')
    plt.savefig('outputs/hp_convergence.png')
    plt.close()

    # Modulo 3: Clustering
    print("Ejecutando Modulo 3: Clustering (GA vs KMeans)...")
    X_cl = df[['u', 'g', 'r', 'i', 'z']]
    ga_cl = ClusteringGA(X_cl, n_clusters=3)
    best_centroids, best_sse, ga_labels, cl_hist = ga_cl.run()

    kmeans = KMeans(n_clusters=3, random_state=42).fit(X_cl)
    km_labels = kmeans.labels_

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(X_cl.iloc[:, 0], X_cl.iloc[:, 1], c=ga_labels, cmap='viridis')
    axes[0].set_title('GA Clusters')
    axes[1].scatter(X_cl.iloc[:, 0], X_cl.iloc[:, 1], c=km_labels, cmap='viridis')
    axes[1].set_title('KMeans Clusters')
    plt.savefig('outputs/clustering_comparison.png')
    plt.close()

    with open("outputs/metrics_summary.txt", "w") as f:
        f.write(f"FS Best Accuracy: {best_acc:.4f}\n")
        f.write(f"HP Best k: {best_k}, MSE: {best_mse:.4f}, R2: {best_r2:.4f}\n")
        f.write(f"Clustering GA SSE: {best_sse:.4f}, KMeans SSE: {kmeans.inertia_:.4f}\n")

    print("Pipeline completado exitosamente. Salidas generadas en la carpeta outputs/.")

if __name__ == "__main__":
    main()