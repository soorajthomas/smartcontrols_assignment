# Smart Controls Assignment

This is the assignment assigned to me for reviewing my coding capabilities

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You should be having python3, pip3 and virtualenv installed on the machine. Sharing commands for the same below

```
Steps to install python3 and pip3 (pip comes as a package with python now so you only need to install python)
1. Open terminal via Ctrl+Alt+T or searching for “Terminal” from app launcher. When it opens, run command to add the PPA:
    sudo add-apt-repository ppa:jonathonf/python-3.6
2. Then check updates and install Python 3.6 via commands:
    sudo apt-get update
    sudo apt-get install python3.6
3. Check you installation by running the command:
    python3 -V

Command to install virtualenv: sudo pip install virtualenv
Create a virtual environment with the command: virtualenv -p python3 env
Activate the environment with the command: source env/bin/activate
```

### Installing

To install all the dependencies for the project run the following command:

```
1. cd into the project root director where you will find a requirements.txt file
2. pip install -r requirements.txt
```

You are done with the installation of the dependencies.

We need to setup a small sqlite db for handling users and there sessions. For this execute the following commands:

```
    python manage.py makemigrations
    python manage.py migrate
```

Now all you project requirements are done.

#### Running the Project

To activate the server just run the following command in the terminal:
```
    python manage.py runserver
```
You can access the server by visiting http://127.0.0.1:8000/ in any of your browser.


## Running the tests

Execute the following command in the terminal:

```
    python manage.py test
```