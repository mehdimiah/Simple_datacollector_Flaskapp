from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres123@localhost/height_collector'
#creating a connection to database
db = SQLAlchemy(app)
#creating a sqlalchemy object which is pointing to the app name

class Data(db.Model):
    #inherting the model class from the sqlalchemy object
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key = True)
    email_ = db.Column(db.String(120), unique = True)
    #email field in the table, string input and set limit to 120, cannot accept if longer than 120
    #setting unique so there cannot be duplicate emails
    height_ = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_
        #intialising the instance variables so when class called the variables are first executed



@app.route("/")
def index():
    return render_template("index.html")
    #py will go to templates folder and render the index file

@app.route("/success" , methods = ['POST']) #when this url is visited we want to execute the below
def success():
    if request.method == 'POST':
        email=request.form['email_name'] #grabbing the form element name in the inputs
        #creating a varible to capture the form element called email_name to take the info from the website
        height = request.form['height_name']

        
        if db.session.query(Data).filter(Data.email_ == email).count() == 0: #querying the database to see if there is existing email
            #is the query is == 0 then store the data to the database

            data = Data(email,height) #object instance of the data class passing the parameters
        #this creates a db model object which is recognised by the db add method
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar() #scalar will extract number from statement
            average_height = round(average_height,1)
            count = db.session.query(Data.height_).count()
            send_email(email,height,average_height,count) #calling the function that will send email            
            return render_template("success.html")

        else:
            return render_template("index.html",
             text="Seems like this email has been used already!")
            #if the email was used, python will re-render the index page

if __name__ == '__main__':
    app.debug=True
    app.run()

#if script is being executed and not imported execute the below lines
#app.run runs application in the default port which is 5000


#in virtualenv, python app.py will run the flask application in the browser

#import from script, the script is not executed
"""
so we use
python
from app import db
db.create_all()

this uses the db from line 8 which points to the app, and runs through the Data class
and then creates the table and columns as instructed 

reason why we are using the  venv, is because when running the script the name of the script is __main__
therefore the db wouldnt be run or instantiated. by using venve it uses the name as app which is what 
sql alchemy is pointing to in line 8

"""