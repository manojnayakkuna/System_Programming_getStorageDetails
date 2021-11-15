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
                    echo "current workspace: ${workspace}"
                    dir(workspace) {
                        bat '''
                            conda env list
                            conda activate base
                        '''
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