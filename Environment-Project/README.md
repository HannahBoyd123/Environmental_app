# MeteoMapper
Meteo-Mapper is a project created by a team of 3 CodeFirst Girls Nanodegree students that is an accumulation of all the skills gained from the program to contribute to the final grade of the Nanodegree. 

Meteo-Mapper is a web application that allows you to find data regarding the weather, pollution and maps, based upon the city name.

## Setup & Installation

Make sure you have the latest version of Python installed.

Example:
```bash
git clone <repo-url>
```

```bash
pip install -r requirements.txt
```

Installation:

Clone the files from GitHub to your local directory
Install the requirements for the libraries needed.
You will need an API key. Register at: https://openweathermap.org/
Once you have an API key, paste this in the pollution_and_weather_links.py file. The file makes clear where this needs to go.
Go to the connect_to_db file change:
host='localhost',
user='root',
password='Kettle123!' to your local host, user and MySQL password,

## Running The App

```bash
python __init__.py
```
Go to the __init__.py file, set the Flask app as __init__ in your local environment using the terminal (information on how to do this can be found here (https://flask.palletsprojects.com/en/2.0.x/quickstart/)
the run the app using the flask run command in your terminal


## Viewing The App

Go to `http://127.0.0.1:5000`

## GIF
![Project Demo](https://github.com/panda88-hub/Environment-Project/blob/main/climate/website/static/media/Meteo-Mapper-Personal-Microsoft.gif?raw=true))

## Details:  

Authors: Jessica Li, Hannah Boyd, Samanta Norbury-Webster.

License: This project is open source and all ownership rights are attributed to the authors.

Project status: This game was created as a final project for a bootcamp on software engineering. Development has stopped completely as we have submitted our project.
