import os
import sys
import pytest
import numpy as np
import pandas as pd

# Asegurar que la raíz del proyecto esté en el path de búsqueda de módulos
# Asegurar que la raiz del proyecto este en el path de busqueda de modulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ag_feature_selection import FeatureSelectionGA

def test_dataset_exists():
    if not os.path.exists("sdss_sample.csv"):
    if not os.path.exists("sdss_sample.csv") or len(pd.read_csv("sdss_sample.csv")) < 50:
        np.random.seed(42)
        n = 300
        df = pd.DataFrame({
            'u': [1, 2], 'g': [2, 3], 'r': [3, 4], 'i': [4, 5], 'z': [5, 6],
            'redshift': [0.1, 0.2], 'class': ['GALAXY', 'STAR']
            'u': np.random.normal(18, 2, n),
            'g': np.random.normal(17, 2, n),
            'r': np.random.normal(16, 2, n),
            'i': np.random.normal(15, 2, n),
            'z': np.random.normal(14, 2, n),
            'redshift': np.random.uniform(0, 2, n),
            'class': np.random.choice(['GALAXY', 'STAR', 'QSO'], n)
        })
        df.to_csv("sdss_sample.csv", index=False)
    assert os.path.exists("sdss_sample.csv")
    assert len(pd.read_csv("sdss_sample.csv")) >= 50

def test_chromosome_length():
    X = pd.DataFrame(np.random.rand(10, 6))
    y = pd.Series(['A'] * 5 + ['B'] * 5)
    ga = FeatureSelectionGA(X, y)
    pop = ga.init_population()
    assert pop.shape == (20, 6)
