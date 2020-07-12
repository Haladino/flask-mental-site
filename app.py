from flask import Flask, json
from util import read_file
from db import new_database
from config import FRONTEND_CONFIG_FILE

app = Flask(__name__)

### Select Configuration -------------------------------------------------------
# To set env use console
# For Linux / Mac
# $ export FLASK_ENV={ your config name }
#
# For Windows PowerShell
# $env:FLASK_ENV= "{ your config name }"
# 
# For cmd
# > set FLASK_ENV={ your config name }
#
# To set here
# TEST
# app.config.from_object('config.test_config')
# DEVELOPMENT
# app.config.from_object('config.development_config')
# PRODUCTION
# app.config.from_object('config.production_config')

if app.config["ENV"] == "test":
    app.config.from_object("config.test_config")

elif app.config["ENV"] == "development":
    app.config.from_object("config.development_config")

else:
    app.config.from_object("config.production_config")

print("The server runs on: " + app.config['ENV'].upper() + " configuration")

#-----------------------------------------------------------------------------


### Read in database/{}.json with util.py >> read_file -----------------------
#
# DB_Language = read_file('database/language.json', json)
#
###
# static/text/{}.txt anyaga megy ide ami a DB_Language objectumba kerul
#
# Useage print( DB_Language["Language"]["Citation"]["Eng"] / ["Hun"] )

### Loading JSON database files listed in config.py DATABASE_FILES

CONFIG = new_database()
DB = new_database()

CONFIG.load(FRONTEND_CONFIG_FILE["filename"])
DB.load()

#-----------------------------------------------------------------------------


### Handle errors & custom error page ----------------------------------------
from flask import render_template, make_response
from werkzeug.exceptions import HTTPException, BadRequest


# Gets all Exceptions
# If the the exeption is HTTP, redirects to that handler
# else displays internal server error
@app.errorhandler(Exception)
def handle_exeptions(e):
    
    if isinstance(e, HTTPException):
        return http_exeption_handler(e)

    return make_response( render_template('error.html') , 500 )


# Handles HTTP exceptions
@app.errorhandler(HTTPException)
def http_exeption_handler(e):
    
    response = e.get_response()
    response.data = json.dumps({

        "code"        : e.code,
        "name"        : e.name,
        "description" : e.description 
    
    })
    response.content_type = "application/json"


    ### Here we display the hungarian equivalent of errors from file
    ### error_ls = read_file('database/error_list.json' json)
    data = json.loads(response.data)
    print(data)

    return make_response( render_template('error.html', data=data) , data['code'] )

#-----------------------------------------------------------------------------


import views


if __name__ == '__main__':
    app.run(debug=True)