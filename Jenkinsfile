pipeline {
    agent any

    environment {
        // Define any environment variables if needed
        DOCKER_IMAGE = "swift-ch20-reproduce"
    }

    stages {
        stage('Checkout') {
            steps {
                // This step is standard for Jenkins to pull the code
                checkout scm
            }
        }

        stage('Build Docker') {
            steps {
                echo "Building Docker image..."
                sh 'docker compose build'
            }
        }

        stage('Execute SWIFT Tests') {
            steps {
                echo "Running SWIFT Reproduction tests in Docker..."
                // Use '--abort-on-container-exit' to stop all containers when one ends
                // '--exit-code-from' ensures the pipeline reflects the test result
                sh 'docker compose up --abort-on-container-exit --exit-code-from swift-reproduction'
            }
            post {
                always {
                    echo "Cleaning up containers..."
                    sh 'docker compose down'
                }
            }
        }

        stage('Publish Reports') {
            steps {
                echo "Archiving Robot Framework reports..."
                
                // 1. Archive the core artifacts so they are saved with the build
                archiveArtifacts artifacts: 'report.html, log.html, output.xml, data/records.csv', fingerprint: true
                
                // 2. Publish HTML report using the HTML Publisher Plugin
                // This allows viewing the report directly in Jenkins UI via 'Robot Framework Report' link
                publishHTML([
                    allowMissing: false,
                             alwaysLinkToLastBuild: true, 
                             keepAll: true, 
                             reportDir: '.', 
                             reportFiles: 'report.html', 
                             reportName: 'SWIFT Test Report'
                ])
                
                // 3. Optional: Publish via Robot Framework Plugin for rich metrics (if installed)
                /*
                step([$class: 'RobotPublisher',
                    disableArchiveOutput: false,
                    logFileName: 'log.html',
                    otherFiles: '',
                    outputFileName: 'output.xml',
                    outputPath: '.',
                    passThreshold: 100,
                    reportFileName: 'report.html',
                    unstableThreshold: 0])
                */
            }
        }
    }

    post {
        always {
            echo "Pipeline complete."
            // Clean up dangling images/volumes to save space on Jenkins agent
            sh 'docker compose down --rmi local --volumes --remove-orphans'
        }
    }
}
