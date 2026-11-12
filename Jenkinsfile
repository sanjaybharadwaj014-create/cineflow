pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building the CineFlow project...'
                // If you need to run Windows commands, use 'bat' instead of 'sh'
                // Example: bat 'npm install' OR bat 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                // Example: bat 'pytest' OR bat 'npm test'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying to server...'
                // Add your deployment scripts here
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution finished.'
        }
        success {
            echo 'Build completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Please check the console output.'
        }
    }
}
