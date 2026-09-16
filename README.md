# Pipeline de Optimización con Algoritmos Genéticos (Intelligent_PC)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/miguelangelmejia08-star/Intelligent_PC/blob/main/Untitled13.ipynb)

Proyecto integral de Inteligencia Computacional y DevOps que implementa tres algoritmos genéticos (AG) para optimización y aprendizaje de máquina, empaquetado en contenedores Docker y orquestado mediante un pipeline de Integración Continua (CI/CD) en Jenkins.

---

## 📌 Enlaces del Proyecto

* **Repositorio en GitHub:** [https://github.com/miguelangelmejia08-star/Intelligent_PC](https://github.com/miguelangelmejia08-star/Intelligent_PC)
* **Cuaderno Google Colab:** [Abrir en Colab](https://colab.research.google.com/github/miguelangelmejia08-star/Intelligent_PC/blob/main/Untitled13.ipynb)

---

## 📁 Estructura del Proyecto

```text
Intelligent_PC/
│
├── ag_feature_selection.py  # Módulo 1: Selección Genética de Características (KNN)
├── ag_hyperparameters.py    # Módulo 2: Optimización Genética de Hiperparámetros (k en KNN)
├── ag_clustering.py         # Módulo 3: Agrupamiento Genético por Centroides (GA vs KMeans)
├── main.py                  # Script Orquestador del pipeline completo
│
├── tests/
│   └── test_ag.py           # Pruebas unitarias automatizadas (pytest)
├── pytest.ini               # Configuración de rutas de pruebas
│
├── Dockerfile               # Configuración para contenedorización con Docker
├── Jenkinsfile              # Pipeline Declarativo CI/CD para Jenkins (5 etapas)
├── requirements.txt         # Dependencias del proyecto
├── Untitled13.ipynb         # Cuaderno de investigación y prototipado original en Colab
│
└── outputs/                 # Artefactos y métricas generadas
    ├── clustering_comparison.png
    ├── fs_confusion_matrix.png
    ├── fs_convergence.png
    ├── hp_convergence.png
    └── metrics_summary.txt
```

---

## 🧬 Módulos de Algoritmos Genéticos

1. **Módulo 1 - Selección de Características (`ag_feature_selection.py`):**
   * Selecciona el subconjunto óptimo de características para clasificación mediante cromosomas binarios evaluados con un modelo KNN.
2. **Módulo 2 - Optimización de Hiperparámetros (`ag_hyperparameters.py`):**
   * Encuentra el valor óptimo del hiperparámetro `k` (vecinos) minimizando el error cuadrático medio (MSE).
3. **Módulo 3 - Clustering Evolutivo (`ag_clustering.py`):**
   * Agrupamiento genético basado en la minimización de la suma de errores cuadráticos (SSE) comparado frente a KMeans clásico.

---

## 🧪 Pruebas Unitarias

Para ejecutar las pruebas automatizadas del dataset y longitud cromosómica:

```bash
python -m pytest tests/
```

---

## 🐳 Ejecución con Docker

### 1. Construir la imagen:
```bash
docker build -t intelligent-pc .
```

### 2. Ejecutar y exportar resultados:
```bash
docker run --rm -v "${PWD}/outputs:/app/outputs" intelligent-pc
```

---

## ⚙️ Pipeline CI/CD en Jenkins

El proyecto cuenta con un `Jenkinsfile` declarativo que ejecuta automáticamente las **5 etapas requeridas**:

1. **Checkout del Repositorio:** Clona la rama `main` desde GitHub.
2. **Instalación de Dependencias:** Instala `requirements.txt` en el entorno.
3. **Pruebas Básicas:** Ejecuta `pytest tests/` para validar el dataset y la inicialización cromosómica.
4. **Ejecución del Script Principal:** Corre `main.py` ejecutando los 3 módulos de optimización.
5. **Almacenamiento de Artefactos:** Publica en Jenkins las gráficas `.png` y el archivo `metrics_summary.txt`.

