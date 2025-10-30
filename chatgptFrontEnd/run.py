from flaskapi.flask_api import app
import subprocess

#Function to check if Node.js is installed
def checkNodeM():
    try:
        #Check if 'node' command works (assuming Node.js is installed)
        subprocess.run(['node', '--version'], check=True)
        print("Node.js is installed.")
    except FileNotFoundError:
        print("Node.js is not installed. Please install Node.js.")
        exit(1)

    try:
        # Check if 'npm' command works as well
        subprocess.run(['npm.cmd', '--version'], check=True)
        print("Npm is installed.")
    except FileNotFoundError as e:
        print("Npm was not found.")
        exit(1)

# Function to start the React app
def startReact():
    try:
        subprocess.Popen(['npm.cmd', 'start'], cwd="my-app", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("React app started. (If it doesn't automatically open, connect to it with localhost:3000. If that doesn't work, re-launch the program)")
    except FileNotFoundError:
        print("Error starting React. Please ensure 'npm' is available in the system PATH.")
        exit(1)


def installReact():
    try:
        subprocess.Popen(['npm.cmd', 'install'], cwd="my-app", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("React app installed.")
    except FileNotFoundError:
        print("Error installing React. Please ensure 'npm' is available in the system PATH.")
        exit(1)


if __name__ == '__main__':

    # Check if Node.js is installed
    checkNodeM()

    # Install React app required modules
    installReact()
    
    # Start React app
    startReact()

    # Run the Flask server
    app.run(port=5000)
