String condaInstallPath = "C:\\Users\\manoj\\Anaconda3\\condabin";
String pythonInstallPath = "C:\\Users\\manoj\\AppData\\Local\\Programs\\Python\\Python37-32";
String parameterFileName = "parameter.json";

pipeline {

    agent any

    stages {

        /*
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }*/

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

        stage('prepare environment and execute the module') {
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
                            SET PATH=%PATH%;%PYTHONPATH%
                            type parameter.json > param.json
                            python GetStorage.py
                        '''
                        //bat(script:'C:\\Users\\manoj\\AppData\\Local\\Programs\\Python\\Python37-32\\python.exe GetStorage.py', returnStdout: true).tokenize().last
                    }
                }
            }
        }

        stage('Move the result file to a different space location') {
            steps {
                dir(workspace) {
                    echo "Execute project artifacts"
                    bat '''
                        copy "PublishResults\\diskSpaceInfo.json" /A "C:\\Users\\manoj\\Downloads\\Python Study\\Coding Challenges\\Interview Problem Statement\\System_Programming_getStorageDetails\\CaptureResults\\Windows\\diskSpaceInfo.json" /A /Y
                    '''
                }
            }
        }

    }
}
