pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        FLASK_ENV = 'testing'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv .venv
                            . .venv/bin/activate
                            python -m pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            @echo off
                            if not exist .venv (
                                where uv >nul 2>nul
                                if %errorlevel%==0 (
                                    uv venv .venv
                                ) else (
                                    python -m venv .venv
                                )
                            )
                            where uv >nul 2>nul
                            if %errorlevel%==0 (
                                uv pip install --python .venv\\Scripts\\python.exe -r requirements.txt
                            ) else (
                                .venv\\Scripts\\python.exe -m pip install --upgrade pip
                                .venv\\Scripts\\pip.exe install -r requirements.txt
                            )
                        '''
                    }
                }
            }
        }

        stage('Syntax & Lint Check') {
            steps {
                script {
                    if (isUnix()) {
                        sh '.venv/bin/python -m compileall -q app tests run.py'
                    } else {
                        bat '.venv\\Scripts\\python.exe -m compileall -q app tests run.py'
                    }
                }
            }
        }

        stage('Run Automated Tests (pytest)') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'mkdir -p reports && .venv/bin/pytest -v --junitxml=reports/junit.xml'
                    } else {
                        bat '''
                            if not exist reports mkdir reports
                            .venv\\Scripts\\pytest.exe -v --junitxml=reports/junit.xml
                        '''
                    }
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/junit.xml'
                }
            }
        }

        stage('Application Smoke Verification') {
            steps {
                script {
                    def smokeScript = "from app import create_app; from app.config import TestConfig; app = create_app(TestConfig); c = app.test_client(); routes = ['/', '/films/', '/scenes/', '/crew/', '/schedules/', '/production/', '/api/stats']; assert all(c.get(r).status_code == 200 for r in routes); print('All 7 CineFlow module routes verified (HTTP 200)')"
                    if (isUnix()) {
                        sh """.venv/bin/python -c "${smokeScript}" """
                    } else {
                        bat """.venv\\Scripts\\python.exe -c "${smokeScript}" """
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'CineFlow CI Pipeline succeeded: all tests and route checks passed.'
        }
        failure {
            echo 'CineFlow CI Pipeline failed. Check pytest output and stage logs.'
        }
    }
}
