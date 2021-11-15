String condaInstallPath = "C:\\Users\\manoj\\Anaconda3\\condabin";
String pythonInstallPath = "C:\\Users\\manoj\\AppData\\Local\\Programs\\Python\\Python37-32";
String parameterFileName = "parameter.json"

pipeline {

    agent any

    stages {

        stage('pipeline initialization') {
            steps {
                echo "This is pipeline initialization step"
                echo "We will be performing code check-out, prepare run environment and execute the project"
            }
        }

        stage('code checkout') {
            steps{
                echo "Perform code check-out"
            }
        }

        stage('prepare environment') {
            steps {
                script {
                    echo "Perform project execution run environment"
                    def workspace = env.WORKSPACE

                    echo "current workspace : ${workspace}"
                    echo "conda install path: ${condaInstallPath}"

                    dir(condaInstallPath) {
                        bat '''
                            dir
                            conda env list
                            conda activate base
                        '''
                    }

                    dir(workspace) {
                        bat '''
                            dir
                            SET PATH=%PATH%;%PYTHON_PATH%
                            python GetStorage.py %parameterFileName%
                        '''
                        //bat(script:'C:\\Users\\manoj\\AppData\\Local\\Programs\\Python\\Python37-32\\python.exe GetStorage.py', returnStdout: true).tokenize().last
                    }
                }
            }
        }

        stage('execute modules') {
            steps {
                echo "Execute project artifacts"
            }
        }

    }
}