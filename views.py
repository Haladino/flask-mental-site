from flask import render_template
from app import app, DB, CONFIG


### get database loaded files and frontend config here to pass to templates

    # { variable } = CONFIG.get_loaded_files_json()

    # { variables } = DB.get_loaded_files_json()

c = CONFIG.get_loaded_files_json()
print(c)
data = DB.get_loaded_files_json()
### Main pages go here ################################################

# Home
@app.route('/')
@app.route('/Index')
def Index():
    return render_template('index.html', name="Kezdolap", configuration=c, data=data) ### Config JSON passed ### useage c["site_config_data"]["author"]

# Services
@app.route('/Szolgaltatasok')
def Szolgaltatasok():
    return render_template('services.html', name="Szolgaltatasok", configuration=c, data=data)
