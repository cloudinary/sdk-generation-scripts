pipeline{
    agent{
        label "build-sdk"
    }
    options { timestamps () }
    environment{
        TOKEN = credentials('cloudinary-bot-release-token')
        CLOUDINARY_URL = credentials('CLOUDINARY_URL')
        CLOUDINARY_ACCOUNT_URL = credentials('CLOUDINARY_ACCOUNT_URL')
        SHELL_INTERPRETER="#!/bin/bash"
        SHELL_ADDITIONAL_COMMAND="export SHELLOPTS\nset -ex"
    }
    stages{
        stage("Clone sdk generation repo"){
            steps{
                git url: "git@github.com:cloudinary/sdk-generation-scripts", branch: "main", credentialsId: 'cloudinary-bot'
            }
        }
        stage("Clone services YMLs"){
            steps{
                  dir ('service_interfaces') {
                    git url: "git@github.com:CloudinaryLtd/service_interfaces.git", branch: "master", credentialsId: 'cloudinary-bot'
                  }
            }
        }
        stage("Generate"){
            steps{
                getShOutput("python3 main.py")
            }
        }
    }
}

/**
 * Runs the shell script (command) and returns the output (STDOUT).
 *
 * @param script The script (shell command) to run.
 *
 * @return The output of the script.
 */
def getShOutput(String script)
{
    return sh(script: "${SHELL_INTERPRETER}\n${SHELL_ADDITIONAL_COMMAND}\n${script}", returnStdout: true).trim()
}
