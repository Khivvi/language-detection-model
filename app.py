# Import The Libraries
from flask import Flask, request, render_template
import sklearn
import pickle
import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
import os
import twilio
import twilio.rest
from twilio.rest import Client

le = LabelEncoder()

app = Flask(__name__)
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict',methods = ["POST"])

def predict():
    # Load the Data Set
    data = pd.read_csv("language_detection.csv")
    y = data["Language"]

    # Label Encoding
    y = le.fit_transform(y)

    # Loading the Model & CV
    model = pickle.load(open("model.pkl", "rb"))
    cv = pickle.load(open("transform.pkl", "rb"))

    if request.method == "POST":
        # Taking the Input
        text = request.form["text"]
        # Preprocessing the Text
        text = re.sub(r'[!@#$(),\n"%^*?\:;~`0-9]', '', text)
        text = re.sub(r'[[]]', '', text)
        text = text.lower()
        dat = [text]
        # Creating the vector
        vect = cv.transform(dat).toarray()
        # Prediction
        my_pred = model.predict(vect)
        my_pred = le.inverse_transform(my_pred)

    # Twillio
    account_sid = 'AC834cae60260145f99b7780904b56ae4e'
    auth_token = 'c460d3fca400ce074ee7395df5736da8'
    client = Client(account_sid, auth_token)

    # If Prediction is English
    if my_pred[0] == "English":
        message = client.messages \
                        .create(
                            body=text,
                            from_='+12074368578',
                            to='+917028009000'
                        )
        print(message.sid)
    if my_pred[0] == "French":
        message = client.messages \
                        .create(
                            body=text,
                            from_='+12074368578',
                            to='+917760326600'
                        )
        print(message.sid)

    if my_pred[0] == "Italian":
        message = client.messages \
                        .create(
                            body=text,
                            from_='+12074368578',
                            to='+917028009000'
                        )
        print(message.sid)
    if my_pred[0] == "Russian":
        message = client.messages \
                        .create(
                            body=text,
                            from_='+12074368578',
                            to='+917028009000'
                        )
        print(message.sid)
    if my_pred[0] == "Danish":
        message = client.messages \
                        .create(
                            body=text,
                            from_='+12074368578',
                            to='+918139059075'
                        )
        print(message.sid)
    if my_pred[0] == "Swedish":
        message = client.messages \
                        .create(
                            body=text,
                            from_='+12074368578',
                            to='+918807721580'
                        )
        print(message.sid)
    if my_pred[0] == "Hindi":
        message = client.messages \
                        .create(
                            body=text,
                            from_='+12074368578',
                            to='+917028009000'
                        )
        print(message.sid)

    # Returning the Result on the Main Page
    return render_template("home.html", pred = "The above text is in {}".format(my_pred[0]))

if __name__ =="__main__":
    app.run(debug = True)