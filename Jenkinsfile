pipeline {
    agent any

    environment {
        // Asegurar que el servicio de Jenkins en Windows encuentre la ruta de Python
        PATH = "C:\\Users\\migue\\AppData\\Local\\Python\\bin;C:\\Users\\migue\\AppData\\Local\\Python\\pythoncore-3.14-64;C:\\Users\\migue\\AppData\\Local\\Python\\pythoncore-3.14-64\\Scripts;${env.PATH}"
    }

    stages {
        stage('1. Checkout del Repositorio') {
            steps {
                checkout scm
                // Clona directamente el repositorio y rama especificados
                git branch: 'main', url: 'https://github.com/miguelangelmejia08-star/Intelligent_PC'
            }
        }

        stage('2. Instalacion de Dependencias') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m pip install --upgrade pip'
                        sh 'python3 -m pip install -r requirements.txt'
                        sh 'python3 -m pip install --upgrade pip || pip install --upgrade pip || true'
                        sh 'python3 -m pip install --break-system-packages -r requirements.txt || python3 -m pip install -r requirements.txt || pip install -r requirements.txt'
                    } else {
                        bat 'python -m pip install --upgrade pip'
                        bat 'python -m pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('3. Pruebas Basicas (Dataset y Cromosomas)') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m pytest tests/'
                        sh 'python3 -m pytest tests/ || pytest tests/'
                    } else {
                        bat 'python -m pytest tests/'
                    }
                }
            }
        }

        stage('4. Ejecucion del Script Principal (3 Modulos AG)') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 main.py'
                        sh 'python3 main.py || python main.py'
                    } else {
                        bat 'python main.py'
                    }
                }
            }
        }

        stage('5. Almacenamiento de Artefactos') {
            steps {
                archiveArtifacts artifacts: 'outputs/**', fingerprint: true, allowEmptyArchive: false
            }
        }
    }

    post {
        success {
            echo 'Pipeline de Optimizacion Genetica ejecutado exitosamente.'
            echo '¡Pipeline de Optimizacion Genetica ejecutado con exito!'
            echo 'Pipeline de Optimizacion Genetica ejecutado con exito!'
        }
        failure {
            echo 'El pipeline ha fallado. Revisa los logs de ejecucion en la consola.'
            echo 'El pipeline ha fallado. Revisa la consola para mas detalles.'
        }
    }
}

