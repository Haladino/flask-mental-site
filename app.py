from flask import Flask, render_template, url_for, request, redirect, flash, session

app = Flask(__name__)

app.secret_key = '7afbbd085cd10de82a67572c1ebf7827'

import db


@app.route('/en')
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('contact'))
    else:
        lang = session.get('lang', 'hu')
        return render_template('index.html', text=db.CITATION_TEXT[lang], lang=lang)


@app.route('/en/about')
@app.route('/rolunk')
def about():
    lang = session.get('lang', 'hu')
    return render_template('about.html', text=db.HELP_TEXT[lang], lang=lang)


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
    lang = session.get('lang', 'hu')
    return render_template('services.html', text=db.SERVICES[lang], lang=lang)


@app.route('/change_lang', methods=['POST'])
def change_language():
    session['lang'] = request.form['lang']
    return redirect(url_for('index'))
