from flask import Flask, render_template, url_for, request, redirect, flash, session

app = Flask(__name__)

app.secret_key = '7afbbd085cd10de82a67572c1ebf7827'

import config


@app.route('/en')
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('contact'))
    else:
        text = config.CITATION_TEXT
        if 'language' in session.keys() and session['language'] == 'en':
            return render_template('index.html', text=text, en=True)
        else:
            return render_template('index.html', text=text, en=False)


@app.route('/en/about')
@app.route('/rolunk')
def about():
    text = config.HELP_TEXT
    return render_template('about.html', text=text)


@app.route('/en/contact')
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


@app.route('/en/services')
@app.route('/szolgaltatasok')
def services():
    text = config.SERVICES
    print(text)
    return render_template('services.html', text=text)


@app.route('/change_lang', methods=['POST'])
def change_language():
    if request.form['lang'] == 'en':
        session['language'] = 'en'
    else:
        session['language'] = 'hu'
    flash(session['language'])
    return redirect(url_for('index'))
