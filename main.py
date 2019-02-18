#author - Thisuri
import base64
import numpy as np
import io
import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from flask import request
from flask import jsonify, render_template, Response
from flask import Flask
from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask_mail import Message, Mail

mail = Mail()

app = Flask(__name__)
app.secret_key = 'thisuri'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'little.palace123@gmail.com'
app.config["MAIL_PASSWORD"] = 'mbjfjsdqgksgilda'

mail.init_app(app)


def set_flag(j):
    tmp = np.zeros(28)
    tmp[j] = 1
    return(tmp)


@app.route('/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required. If form is correctly filled, you will get a message')
            return render_template('form.html', form=form)
        else:
            msg = Message(sender='little.palace123@gmail.com', recipients=['thisuri.lekamge94@gmail.com'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('thank_you.html', form=form)

    elif request.method == 'GET':
        return render_template('form.html', form=form)


def preprocess_gender(name):
    char_index = {' ': 0, 'b': 1, 'v': 2, 'c': 3, 'f': 4, 'o': 5, 'END': 6, 'd': 7, 'q': 8, 'h': 9, 'y': 10, 'p': 11, 'x': 12, 'u': 13,
                  's': 14, 'e': 15, 'l': 16, 't': 17, 'r': 18, 'n': 19, 'g': 20, 'z': 21, 'j': 22, 'i': 23, 'w': 24, 'm': 25, 'k': 26, 'a': 27}
    maxlen = 16
    name = [element.lower() for element in name]
    name
    X = []
    trunc_name = [str(i)[0:maxlen] for i in name]
    model = load_model('gender_load5.h5')
    for i in trunc_name:
        tmp = [set_flag(char_index[j]) for j in str(i)]
        for k in range(0, maxlen - len(str(i))):
            tmp.append(set_flag(char_index["END"]))
        X.append(tmp)

    prediction = model.predict(np.asarray(X)).tolist()
    predMale = "{:.0%}".format(prediction[0][0])
    # predMale = (prediction[0][0])*100
    male = str(predMale)
    predFemale = "{:.0%}".format(prediction[0][1])
    # predFemale = (prediction[0][1])*100
    female = str(predFemale)
    r = "Male: "+male+"        "+"    |        \n\n\nFemale: "+female
    print(prediction)
    print(r)
    return r


def preprocess_gana(name):
    char_index = {'l': 0, 'b': 1, 't': 2, 'h': 3, 'u': 4, 'o': 5, 'x': 6, 'f': 7, 'g': 8, 'm': 9, 'w': 10, 'e': 11, 'k': 12, 'n': 13,
                  'i': 14, 'p': 15, ' ': 16, 'r': 17, 'd': 18, 'END': 19, 'j': 20, 's': 21, 'a': 22, 'v': 23, 'q': 24, 'y': 25, 'z': 26, 'c': 27}
    maxlen = 16
    name = [element.lower() for element in name]
    name
    X = []
    trunc_name = [str(i)[0:maxlen] for i in name]
    model = load_model('gana1_load.h5')
    for i in trunc_name:
        tmp = [set_flag(char_index[j]) for j in str(i)]
        for k in range(0, maxlen - len(str(i))):
            tmp.append(set_flag(char_index["END"]))
        X.append(tmp)
    prediction = model.predict(np.asarray(X)).tolist()
    print(prediction[0][0])
    predGood = "{:.0%}".format(prediction[0][0])
    predBad = "{:.0%}".format(prediction[0][1])
    predNe = "{:.0%}".format(prediction[0][2])
    good = str(predGood)
    bad = str(predBad)
    ne = str(predNe)
    r = "Good: "+good+" | Bad: "+bad+" | Neutral: "+ne
    return r


@app.route('/')
def home():
    return render_template('form.html')


@app.route('/get_gender', methods=['GET', 'POST'])
def predict_gender():
    K.clear_session()
    x = []
    name = request.form['nm']
    x.append(name)
    prediction = preprocess_gender(x)
    return render_template('get_gender.html', r=prediction)


@app.route('/get_gana', methods=['GET', 'POST'])
def predict_gana():
    K.clear_session()
    x = []
    name = request.form['nm']
    x.append(name)
    prediction = preprocess_gana(x)
    return render_template('get_gana.html', r=prediction)


if __name__ == "__main__":
    app.run()
