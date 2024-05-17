from flask import Flask, send_file, request
from timeit import default_timer as timer
import json
import datetime
import requests
import pymysql.cursors

# Informations de connexion
db_host = 'localhost'
db_user = 'votre_utilisateur'
db_password = 'votre_mot_de_passe'
db_name = 'nom_de_votre_base_de_donnees'

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/hello/', defaults={'username': 'Guest'})
@app.route('/hello/<username>')
def index(username):
    return f'Hello, {username}!'

@app.route('/mockfile')
def mockfile():
    startTime = timer()

    stars = ''
    for x in range(0, 357000):
        stars += "*"

    #use of datetime and json to have a date format that is JSON serializable
    dt = datetime.datetime.utcnow()

    # Convert the datetime object to a string in a specific format 
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S") 
    
    # Serialize the string using the json module 
    json_data = json.dumps(dt_str) 

    #create and fill a json file (~350kB)
    data = {
        "value": stars,
        "creation-date": json_data,
        "execution_time": 0,
    }

    #compute execution time of the function (ms)
    endTime = timer()
    executionTime = endTime - startTime
    
    data.update({"execution_time": executionTime})

    return data


@app.route('/mockfile_by_proxy')
def getmockfile():
    #récupérer fichier depuis http://127.0.0.1:5000/mockfile et mesurer le temps (duration timestamps (ms): end date - start date)
    #url = "http://127.0.0.1:5000/mockfile"

    startTime = timer()
    
    # Récupérer l'hôte et le port du serveur Flask
    host = request.host

    # Construire l'URL complète
    url = f"http://{host}/mockfile"
    response = requests.get(url)

    if response.headers.get('Content-Type') == 'application/json':
        json_data = response.json()
        received_file = { 
            "data": json_data,
            "duration" : 0
        }
        endTime = timer()
        executionTime = endTime - startTime
        received_file["duration"] = executionTime
        return received_file
    else:
        print("The response is not in JSON format")
        return "The response is not in JSON format"
    
def get_db_connection():
    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection