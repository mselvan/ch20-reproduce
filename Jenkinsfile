pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: test-runner
    image: python:3.9-slim
    command:
    - cat
    tty: true
    resources:
      requests:
        memory: "256Mi"
        cpu: "500m"
      limits:
        memory: "512Mi"
        cpu: "1000m"
  - name: mock-server
    image: python:3.9-slim
    command:
    - cat
    tty: true
    ports:
    - containerPort: 5005
    resources:
      requests:
        memory: "128Mi"
        cpu: "200m"
      limits:
        memory: "256Mi"
        cpu: "500m"
"""
        }
    }

    stages {
        stage('Setup Dependencies') {
            steps {
                container('test-runner') {
                    echo "Installing dependencies on test runner..."
                    sh 'pip install --no-cache-dir -r requirements.txt'
                }
                container('mock-server') {
                    echo "Installing dependencies on mock server..."
                    sh 'pip install --no-cache-dir -r requirements.txt'
                }
            }
        }

        stage('Start Mock Server') {
            steps {
                container('mock-server') {
                    echo "Starting SWIFT Mock Server in background..."
                    sh 'python scripts/mock_server.py > mock_server.log 2>&1 &'
                    
                    echo "Waiting for server readiness..."
                    sh """
                        count=0
                        until python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5005/health')" || [ \$count -eq 10 ]; do
                            sleep 2
                            count=\$((count + 1))
                            echo "Waiting for mock server... (\$count/10)"
                        done
                        # Final check to fail the build if still not ready
                        python3 -c "import urllib.request, sys; res = urllib.request.urlopen('http://localhost:5005/health'); sys.exit(0 if res.getcode() == 200 else 1)"
                    """
                }
            }
        }

        stage('Run SWIFT Tests') {
            steps {
                container('test-runner') {
                    echo "Executing SWIFT Reproduction Suite..."
                    // Note: localhost works because containers in the same pod share the network
                    sh 'python run_swift.py --count 150'
                }
            }
        }

        stage('Reporting') {
            steps {
                echo "Archiving artifacts and publishing results..."
                
                // Archive key files including the server logs for debugging
                archiveArtifacts artifacts: 'report.html, log.html, output.xml, mock_server.log', fingerprint: true
                
                // Publish results via Robot Framework Plugin (native rich reports)
                step([$class: 'RobotPublisher',
                    disableArchiveOutput: false,
                    logFileName: 'log.html',
                    otherFiles: '',
                    outputFileName: 'output.xml',
                    outputPath: '.',
                    passThreshold: 100,
                    reportFileName: 'report.html',
                    unstableThreshold: 0])
            }
        }
    }

    post {
        always {
            echo "Cleaning up..."
            // In Kubernetes agent, the pod is destroyed automatically after the job finishes
        }
    }
}
