import os
import sys
import pytest
import numpy as np
import pandas as pd

# Asegurar que la raíz del proyecto esté en el path de búsqueda de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ag_feature_selection import FeatureSelectionGA

def test_dataset_exists():
    if not os.path.exists("sdss_sample.csv"):
        df = pd.DataFrame({
            'u': [1, 2], 'g': [2, 3], 'r': [3, 4], 'i': [4, 5], 'z': [5, 6],
            'redshift': [0.1, 0.2], 'class': ['GALAXY', 'STAR']
        })
        df.to_csv("sdss_sample.csv", index=False)
    assert os.path.exists("sdss_sample.csv")

def test_chromosome_length():
    X = pd.DataFrame(np.random.rand(10, 6))
    y = pd.Series(['A'] * 5 + ['B'] * 5)
    ga = FeatureSelectionGA(X, y)
    pop = ga.init_population()
    assert pop.shape == (20, 6)
