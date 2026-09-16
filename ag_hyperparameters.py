import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score

class HyperparameterGA:
    def __init__(self, X, y, pop_size=15, generations=12, k_min=1, k_max=30):
        self.X = X
        self.y = y
        self.pop_size = pop_size
        self.generations = generations
        self.k_min = k_min
        self.k_max = k_max

    def fitness(self, k_val):
        k = int(np.clip(round(k_val), self.k_min, self.k_max))
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)
        model = KNeighborsRegressor(n_neighbors=k)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        return 1.0 / (mse + 1e-6), mse, r2_score(y_test, preds)

    def run(self):
        pop = np.random.uniform(self.k_min, self.k_max, size=self.pop_size)
        best_history = []
        best_k = None
        best_mse = float('inf')
        best_r2 = -float('inf')
        best_fit = -1

        for gen in range(self.generations):
            evals = [self.fitness(k) for k in pop]
            fits = np.array([e[0] for e in evals])
            mses = [e[1] for e in evals]
            r2s = [e[2] for e in evals]

            max_idx = np.argmax(fits)
            if fits[max_idx] > best_fit:
                best_fit = fits[max_idx]
                best_k = int(np.clip(round(pop[max_idx]), self.k_min, self.k_max))
                best_mse = mses[max_idx]
                best_r2 = r2s[max_idx]

            best_history.append(best_fit)
            next_pop = [pop[max_idx]]
            probs = fits / np.sum(fits)

            while len(next_pop) < self.pop_size:
                parents = np.random.choice(pop, size=2, p=probs)
                alpha = np.random.rand()
                child = alpha * parents[0] + (1 - alpha) * parents[1]
                if np.random.rand() < 0.2:
                    child += np.random.normal(0, 2)
                child = np.clip(child, self.k_min, self.k_max)
                next_pop.append(child)

            pop = np.array(next_pop)

        return best_k, best_mse, best_r2, best_history

