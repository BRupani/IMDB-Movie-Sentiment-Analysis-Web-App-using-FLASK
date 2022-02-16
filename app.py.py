from flask import Flask,render_template,url_for,request
import numpy as np
import pickle
import pandas as pd
import flasgger
from flasgger import Swagger
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import sqlite3 as sql
app=Flask(__name__)
Swagger(app)

mnb = pickle.load(open('Naive_Bayes_model_imdb.pkl','rb'))
countVect = pickle.load(open('countVect_imdb.pkl','rb'))

@app.route('/')
def home():
    return render_template('home.html')
'''
@app.route('/predict',methods=['POST'])
def predict():

    if request.method == 'POST':
        Reviews = request.form['Reviews']
        data = [Reviews]
        vect = countVect.transform(data).toarray()
        my_prediction = mnb.predict(vect)
    return render_template('result.html',prediction = my_prediction)'''

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            Reviews = request.form['Reviews']
            data = [Reviews]
            vect = countVect.transform(data).toarray()
            my_prediction = mnb.predict(vect)
            if my_prediction==1:
                sentiment='positive'
            else:
                sentiment='negative'
        #    review = request.form['value']
            with sql.connect("database.db") as con:
               cur = con.cursor()
               cur.execute("INSERT INTO moviereviewss (Reviewss, my_predictions) VALUES (?,?)",
                           (Reviews, sentiment))  # ? and tuple for placeholders
               con.commit()
               msg = "Record successfully added"
             #  print(msg)


        except:
            con.rollback()
            msg = "error in insert operation"
          #  print(msg)
        finally:
            return render_template("result.html", msg=msg, prediction = my_prediction)
            con.close()


@app.route('/data')
def list_all():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from moviereviewss")

    rows = cur.fetchall()  # returns list of dictionaries
    return render_template("data.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
    