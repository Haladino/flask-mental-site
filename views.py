from flask import render_template
from app import app, DB, CONFIG


### get database loaded files and frontend config here to pass to templates

    # { variable } = CONFIG.get_loaded_files_json()

    # { variables } = DB.get_loaded_files_json()

c = CONFIG.get_loaded_files_json()
data = DB.get_loaded_files_json()

# When session is set
# Pass session variable to templates
# lang={ session variable }

### Main pages go here ################################################

# Home
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name="Kezdolap", configuration=c, data=data) ### Config JSON passed ### useage c["site_config_data"]["author"]

# Services
@app.route('/szolgaltatasok')
def szolgaltatasok():
    return render_template('services.html', name="Szolgaltatasok", configuration=c, data=data)
