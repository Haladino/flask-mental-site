from flask import Flask, json
from util import read_file
from db import new_database
from config import FRONTEND_CONFIG_FILE

app = Flask(__name__)

### Set session
#   - language session variable

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

    return make_response( render_template('error.html', data=translate_error( 500, 'hun' ) ) , 500 )


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
    
    data = json.loads(response.data)

    ### When a session variable is set to a language, that variable is passed to translate_error
    ### translate_error( data['code'], session_variable_for_language )
    ### later same variable is passed to templates in views.py

    return make_response( render_template('error.html', data=translate_error( data['code'], 'hun' ) ), data['code'] )


def translate_error(error_code, lang):
    error_ls = read_file('database/error_list.json', json)
    return {
                "code"        : error_ls['error_list'][str(error_code)]['code'],
                "name"        : error_ls['error_list'][str(error_code)]['name'][str(lang)],
                "description" : error_ls['error_list'][str(error_code)]['description'][str(lang)]  
            }
            
### Register and raise custom error
# class InsufficientStorage(werkzeug.exceptions.HTTPException):
#     code = 507
#     description = 'Not enough storage space.'

# app.register_error_handler(InsufficientStorage, handle_507)

# raise InsufficientStorage()


### Error report email

#-----------------------------------------------------------------------------


import views


if __name__ == '__main__':
    app.run(debug=True)