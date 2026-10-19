pipeline {
    agent any

    stages {
        stage('1. Instalacion de Dependencias') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            python -m venv venv
                            call venv\\Scripts\\activate.bat
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('2. Pruebas Unitarias') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            pytest tests/
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            pytest tests/
                        '''
                    }
                }
            }
        }

        stage('3. Ejecucion del Script Principal (3 Modulos AG)') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . venv/bin/activate
                            python main.py
                        '''
                    } else {
                        bat '''
                            call venv\\Scripts\\activate.bat
                            python main.py
                        '''
                    }
                }
            }
        }

        stage('4. Almacenamiento de Artefactos') {
            steps {
                archiveArtifacts artifacts: 'outputs/**', fingerprint: true, allowEmptyArchive: false
            }
        }
    }

    post {
        success {
            echo '¡Pipeline de Optimizacion Genetica ejecutado con exito!'
        }
        failure {
            echo 'El pipeline ha fallado. Revisa la consola para mas detalles.'
        }
    }
}
