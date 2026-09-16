pipeline {
    agent any

    stages {
        stage('1. Checkout del Repositorio') {
            steps {
                checkout scm
            }
        }

        stage('2. Instalacion de Dependencias') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 -m pip install --upgrade pip'
                        sh 'python3 -m pip install -r requirements.txt'
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
        }
        failure {
            echo 'El pipeline ha fallado. Revisa los logs de ejecucion en la consola.'
        }
    }
}

