import numpy as np

class ClusteringGA:
    def __init__(self, X, n_clusters=3, pop_size=20, generations=15):
        self.X = np.array(X)
        self.n_clusters = n_clusters
        self.pop_size = pop_size
        self.generations = generations
        self.n_features = self.X.shape[1]

    def fitness(self, chromosome):
        centroids = chromosome.reshape(self.n_clusters, self.n_features)
        distances = np.linalg.norm(self.X[:, np.newaxis, :] - centroids, axis=2)
        min_dists = np.min(distances, axis=1)
        sse = np.sum(min_dists ** 2)
        return 1.0 / (sse + 1e-6), sse, np.argmin(distances, axis=1)

    def run(self):
        min_vals, max_vals = np.min(self.X, axis=0), np.max(self.X, axis=0)
        pop = np.array([
            np.random.uniform(min_vals, max_vals, size=(self.n_clusters, self.n_features)).flatten()
            for _ in range(self.pop_size)
        ])

        best_history = []
        best_sse = float('inf')
        best_labels = None
        best_centroids = None
        best_fit = -1

        for gen in range(self.generations):
            evals = [self.fitness(ind) for ind in pop]
            fits = np.array([e[0] for e in evals])

            max_idx = np.argmax(fits)
            if fits[max_idx] > best_fit:
                best_fit = fits[max_idx]
                best_sse = evals[max_idx][1]
                best_labels = evals[max_idx][2]
                best_centroids = pop[max_idx].reshape(self.n_clusters, self.n_features)

            best_history.append(best_fit)

            next_pop = [pop[max_idx]]
            while len(next_pop) < self.pop_size:
                p1 = pop[np.random.randint(0, self.pop_size)]
                p2 = pop[np.random.randint(0, self.pop_size)]
                child = 0.5 * p1 + 0.5 * p2
                if np.random.rand() < 0.2:
                    child += np.random.normal(0, 0.1, size=child.shape)
                next_pop.append(child)

            pop = np.array(next_pop)

        return best_centroids, best_sse, best_labels, best_history

