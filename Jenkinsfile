
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(
            numToKeepStr: '10'
        ))
    }

    environment {
        APP_URL = 'http://127.0.0.1:5000'
        BUILD_ID = 'dontKillMe'
    }

    stages {

        stage('1. Checkout') {
            steps {
                echo 'Checking out CineFlow from GitHub'
                checkout scm
            }
        }

        stage('2. Environment Setup') {
            steps {
                bat '''
                    python --version
                    git --version

                    if not exist .venv (
                        python -m venv .venv
                    )

                    .venv\\Scripts\\python.exe -m pip install --upgrade pip
                    .venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('3. Code Validation') {
            steps {
                bat '''
                    .venv\\Scripts\\python.exe -m compileall -q app run.py
                '''
            }
        }

        stage('4. Automated Testing') {
            steps {
                bat '''
                    if not exist reports mkdir reports

                    .venv\\Scripts\\python.exe -m pytest -v --junitxml=reports\\junit.xml
                '''
            }

            post {
                always {
                    junit allowEmptyResults: true,
                          testResults: 'reports/junit.xml'
                }
            }
        }

        stage('5. Deploy Locally') {
            steps {
                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$port = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue; if (-not $port) { $env:BUILD_ID='dontKillMe'; $p = Start-Process -FilePath (Resolve-Path '.venv\\Scripts\\python.exe').Path -ArgumentList 'run.py' -WorkingDirectory $env:WORKSPACE -PassThru -WindowStyle Hidden -RedirectStandardOutput 'cineflow-server.log' -RedirectStandardError 'cineflow-error.log'; Set-Content -Path 'cineflow.pid' -Value $p.Id; }"
                '''
            }
        }

        stage('6. Application Health Check') {
            steps {
                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ready = $false; for ($i=0; $i -lt 30; $i++) { try { $r = Invoke-WebRequest -Uri $env:APP_URL -UseBasicParsing -TimeoutSec 3; if ($r.StatusCode -eq 200) { $ready = $true; break } } catch { Start-Sleep -Seconds 2 } }; if (-not $ready) { Get-Content cineflow-error.log -ErrorAction SilentlyContinue; throw 'CineFlow failed to start or respond on port 5000' }"
                '''
            }
        }
    }

    post {
        success {
            echo 'CineFlow pipeline completed successfully.'
            echo 'Application: http://127.0.0.1:5000'
        }

        failure {
            echo 'CineFlow pipeline failed. Check Console Output.'
        }

        always {
            echo 'CineFlow pipeline execution finished.'
        }
    }
}
