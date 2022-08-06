from flask import Flask,redirect,url_for,render_template,request,make_response,flash,session
from flask_session import Session
from flask_mail import Mail,Message
import mysql.connector
import math, random
from flask import *  
import json
import pandas as pd
import json
from email.mime import base
from flask import render_template
import io
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure



app = Flask (__name__)
app.config['SECRET_KEY']='SECRET_KEY'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_USERNAME']='test31032022@gmail.com'
app.config['MAIL_PASSWORD']='TEST31032022@'
app.config['MAIL_PORT']='465'
app.config['MAIL_DEFAULT_SENDER']='465'
app.config['MAIL_USE_SSL']=True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
mail=  Mail()
mail.init_app(app)

otp=0
email=''

@app.route("/")
def home():
    return render_template("login.html")


def establish_connection():
    connection = mysql.connector.connect(host='localhost',
                                             database='obe_proj',
                                             user='root',
                                             password='1234',auth_plugin='mysql_native_password')
    return connection



@app.route("/login",methods=['POST'])
def Login():
    print(request.form['username'])
    connection=establish_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * from user_credentials where email='{}' and password='{}'".format(request.form['username'],request.form['password']))
    record = cursor.fetchall()
    #print(record)
    if len(record)>0:
        session["name"]=record[0][2]
        cursor.execute("SELECT * from courses where faculty='{}'".format(session["name"]))
        record = cursor.fetchall()
        
        return render_template("dashboard1.html",records=record)
    else:
        return render_template("error.html")

    return render_template("homepage.html")
@app.route("/forgotpass",methods=['GET','POST'])

def forgotpass():
    if request.method=='GET':
        return render_template('forgotpass.html')
    else:
        connection=establish_connection()
        cursor = connection.cursor()
        global otp
        global email 
        otp = generateOTP()
        receiver=request.form['useremail']
        sender1='test31032022@gmail.com'
        #receiver2='sanjna.sur10@gmail.com'
        #msg=Message('Password change',sender=sender1,recipients=[receiver2])
        msg=Message('Password change',sender=sender1,recipients=[request.form['useremail']])
        print(sender1)
        print(receiver)
        msg.body='''
        OBE management system-OTP validation
        Password change code is {}
        
        '''.format(otp)
        flag =1
        cursor.execute("SELECT * from user_credentials where email='{}' ".format(receiver))
        if len(cursor.fetchall())!=1:
            print('invalid mail')
            flag=0

        if flag == 1:
            print("message sent")
            email=receiver
            mail.send(msg)
            print(otp)
            return render_template('validateotp.html') 
        return render_template("forgotpass.html")

def generateOTP() :
 
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP

@app.route("/validateotp",methods=['POST'])

def validateotp():
    connection=establish_connection()
    cursor = connection.cursor()
    global otp
    global email
    otpverification=request.form['otp']
    password1=request.form['password']
    updatepassword=request.form['updatepassword']
    print(password1==updatepassword)
    if otp==otpverification:
        if password1 == updatepassword:
            print("correct")
            cursor.execute("UPDATE user_credentials set password='{}' where email='{}'".format(password1,email))
            connection.commit()
            if connection.is_connected():
                cursor.close()
                connection.close()

            #print("MySQL connection is closed")
            try:
                session["name"]=record[0][2]
            except:
                connection=establish_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT * from user_credentials where email='{}' and password='{}'".format(password1,email))
                record = cursor.fetchall()
                print(record)
                if len(record)>0:
                    session["name"]=record[0][2]
            cursor.execute("SELECT * from courses where faculty='{}'".format(session["name"]))
            record = cursor.fetchall()
            return render_template("dashboard1.html",records=record)
        else:
            print(" wrong pass")
            flash("wrong password")  
            return render_template('validateotp.html')
    else:
        print("wrong otp")
        flash("wrong otp")
        return render_template('validateotp.html')
    return render_template('validateotp.html')

@app.route("/dashboard",methods=['POST', 'GET'])

def dashboard():
    if request.method=='GET':
        if session['name']==None:
            return render_template("login.html")
        else:
            connection=establish_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * from courses where faculty='{}'".format(session["name"]))
            record = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template("dashboard1.html",records=record)

if __name__ == "__main__":
    app.run(debug=True)
