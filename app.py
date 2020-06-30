from flask import Flask, render_template, url_for, request, redirect

import config


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('contact'))
    else:
        text = config.CITATION_TEXT
        return render_template('index.html', text=text)


@app.route('/rolunk')
def about():
    text = config.HELP_TEXT
    return render_template('about.html', text=text)


@app.route('/kapcsolat')
@app.route('/kapcsolat/<name>')
def contact(name=None):
    if name:
        if name == "Simonka Enikő":
            return render_template('simonkaeniko.html')
        elif name == "Tomor Andrea":
            return render_template('tomorandrea.html')
    else:
        return render_template('contact.html')


@app.route('/szolgaltatasok')
def services():
    text = config.SERVICES
    print(text)
    return render_template('services.html', text=text)
