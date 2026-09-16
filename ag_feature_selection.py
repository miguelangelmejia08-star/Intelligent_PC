import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

class FeatureSelectionGA:
    def __init__(self, X, y, pop_size=20, generations=15, mutation_rate=0.1, tournament_size=3):
        self.X = X
        self.y = y
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.n_features = X.shape[1]

    def init_population(self):
        pop = np.random.randint(0, 2, size=(self.pop_size, self.n_features))
        for i in range(self.pop_size):
            if np.sum(pop[i]) == 0:
                pop[i][np.random.randint(0, self.n_features)] = 1
        return pop

    def fitness(self, chromosome):
        cols = np.where(chromosome == 1)[0]
        if len(cols) == 0:
            return 0.0

        X_sub = self.X.iloc[:, cols]
        min_class_count = self.y.value_counts().min() if hasattr(self.y, 'value_counts') else 0
        stratify_param = self.y if min_class_count >= 2 else None
        X_train, X_test, y_train, y_test = train_test_split(
            X_sub, self.y, test_size=0.3, random_state=42, stratify=stratify_param
        )
        clf = KNeighborsClassifier(n_neighbors=5)
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        return accuracy_score(y_test, preds)

    def selection(self, pop, fitnesses):
        selected = []
        for _ in range(self.pop_size):
            indices = np.random.choice(len(pop), self.tournament_size)
            best_idx = indices[np.argmax(fitnesses[indices])]
            selected.append(pop[best_idx].copy())
        return np.array(selected)

    def crossover(self, parent1, parent2):
        pt = np.random.randint(1, self.n_features)
        child1 = np.concatenate([parent1[:pt], parent2[pt:]])
        child2 = np.concatenate([parent2[:pt], parent1[pt:]])
        return child1, child2

    def mutate(self, chromosome):
        for i in range(self.n_features):
            if np.random.rand() < self.mutation_rate:
                chromosome[i] = 1 - chromosome[i]
        if np.sum(chromosome) == 0:
            chromosome[np.random.randint(0, self.n_features)] = 1
        return chromosome

    def run(self):
        pop = self.init_population()
        best_fitness_history = []
        avg_fitness_history = []
        best_chromo = None
        best_fit = -1.0

        for gen in range(self.generations):
            fitnesses = np.array([self.fitness(ind) for ind in pop])

            max_idx = np.argmax(fitnesses)
            if fitnesses[max_idx] > best_fit:
                best_fit = fitnesses[max_idx]
                best_chromo = pop[max_idx].copy()

            best_fitness_history.append(best_fit)
            avg_fitness_history.append(np.mean(fitnesses))

            selected = self.selection(pop, fitnesses)
            next_pop = []
            for i in range(0, self.pop_size, 2):
                p1, p2 = selected[i], selected[(i+1)%self.pop_size]
                c1, c2 = self.crossover(p1, p2)
                next_pop.extend([self.mutate(c1), self.mutate(c2)])
            pop = np.array(next_pop)[:self.pop_size]

        return best_chromo, best_fit, best_fitness_history, avg_fitness_history
