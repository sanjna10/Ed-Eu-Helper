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



def CO_PO_map(temp):
    #f=open(qpname,'r')
    #contents=f.read()
    #print(contents)
    #temp=contents.split('\n')
   
    print(temp)
    CO_PO={}
    flag=0
    count=0
    key=1
    for i in range(len(temp)):
        if temp[i].startswith('\nCO-PO Mapping'):
            print('------------------------FOUND CO-PO------------------------------------')
            print(temp[i])
            while temp[i]!='\nCO':
                i=i+1
                count=0
            print('-----------------------------------temp;i--------------')
            print(temp[i])
            i=i+1
            while(not(temp[i].startswith('CO'))):
                print('--------------------------------find count-------------------')
                print(temp[i])
                i=i+1
                count=count+1
            print(count)
            temp_count=0
            while flag == 0:
                if temp_count == count and not(temp[i].startswith('CO')):
                    flag=1
                    return CO_PO
                temp_count=0
                print(temp[i])
                i=i+1
                arr=[]
                while temp_count<count:
                    if(temp[i]==''):
                        arr.append('0')
                    else:
                        arr.append(temp[i])
                    i=i+1
                    temp_count=temp_count+1
                CO_PO.update({key : arr})
                key=key+1
                print(arr)
                print(count)
                print('-----------------------------------------if clause------------------------')
                print(temp[i])
                if not(temp[i].startswith('CO')):
                    print(len(CO_PO))
                    #CO_PO=CO_def2(temp,CO_PO)
                    return CO_PO
def CO_def2(temp,CO_PO):
    
    CO_def={}
    
    for i in range(0,len(temp)):
        if temp[i].startswith('\nCourse Outcomes'):
            while temp[i]!='\nCO' and i<len(temp):
                i=i+1
            print(temp[i])
            while not(temp[i].startswith('CO01')) and i<len(temp):
                i=i+1
            print(temp[i])
            if temp[i]=='CO01':
                for key in range(1,len(CO_PO)+1):
                    i=i+1
                    arr1=temp[i]
                    print(arr1)
                    i=i+1
                    arr2=temp[i]
                    i=i+1
                    arr3=[arr1,arr2]
                    CO_def.update({key:arr3})
                    #CO_def[key].append(arr2)
                    CO_PO[key].append(arr1)
                    CO_PO[key].append(arr2)
                    
                return CO_def
            else:
                break
def insertBLOB_course(cid, cname, threshold,internal,external,detail_file,detailfile2):
    print("Inserting BLOB into python table")
    try:
        connection = establish_connection()

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO course_proporties2
                          (course_id, course_name,course_outcome,co_po,threshold,internal,external) VALUES (%s,%s,%s,%s,%s,%s,%s)"""


        # Convert data into tuple format
        insert_blob_tuple = (cid, cname,detail_file,detailfile2,threshold,internal,external)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("file inserted successfully as a BLOB into qp table", result)
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))


def generate_csv(detail,rollno):
    dict1=detail
    headerlist=["roll_no"]
    ccolumn=["roll_no"]
    for i in dict1.keys():
        l=dict1[i]
        if len(l[0])>1:
            for k in range(len(l[3])):
                name="Q("+str(i)+"."+str(k+1)+")"+"("+str(l[3][k])+")"
                headerlist.append(name)
                ccolumn.append(name)
        if len(l[0])==1:
            name="Q("+str(i)+")"+"("+str(l[4])+")"
            headerlist.append(name)
            ccolumn.append(name)
    #print(ccolumn)
    df1 = pd.DataFrame([],columns=(ccolumn))
    df1
    df=pd.read_csv(rollno,header=[0])
    count=df[df.columns[0]].count()
    count
    df
    roll_no=df[df.columns[0]]
    roll_no
    for i in range(count):
        list1=[]
        list1.append(roll_no[i])
        for i in range(len(ccolumn)-1):
            list1.append(0)
        df1.loc[len(df1.index)] = list1
    return (df1,headerlist)
    


def find_qns(temp):
    qns=0
    for i in temp:
        if i.startswith(str(qns+1)+'.')==True or i.startswith(str(qns+1)+')')==True:
            qns+=1
        
    return qns
def find_COs_1(temp,detail):
    qns=0
    pqns=0
    #print(detail)
    for i in temp:
        #print(qns,pqns)
        if i.startswith(str(qns+1)+'.')==True or i.startswith(str(qns+1)+')')==True:
            pqns=0
            qns+=1
        if i.find('[C')!=-1:
            if i.startswith(str(qns+1)+'.')==True or i.startswith(str(qns+1)+')')==True: 
                ele=""
                for k in i.split('['):
                    if k.find('CO0')!=-1:
                        ele=k
                        break
                try:
                    detail[qns][0].append(ele.split(']')[0])
                except:
                    detail[qns].append([ele.split(']')[0]])
                #pqns=max(0,pqns-1)
                #print("L1",qns,pqns,detail[qns])
                if pqns==0:
                    qns+=1
            else:
                pqns+=1
                ele=""
                for k in i.split('['):
                    if k.find('CO0')!=-1:
                        ele=k
                        break
                try:
                    detail[qns][0].append(ele.split(']')[0])
                except:
                    detail[qns].append([ele.split(']')[0]])
                #pqns=max(0,pqns-1)
                #print("L2",qns,pqns,detail[qns])
                if pqns==0:
                    qns+=1
                    
        if qns>len(detail):
            break
            
    return detail

def find_BTLs_1(temp,detail):
    qns=0
    pqns=0
    #print(detail)
    for i in temp:
        #print(qns,pqns)
        if i.startswith(str(qns+1)+'.')==True or i.startswith(str(qns+1)+')')==True:
            pqns=0
            qns+=1
        if i.find('[C')!=-1:
            if i.startswith(str(qns+1)+'.')==True or i.startswith(str(qns+1)+')')==True: 
                ele=""
                for k in i.split('['):
                    if k.find('BTL')!=-1:
                        ele=k
                        break
                try:
                    detail[qns][1].append(ele.split(']')[0])
                except:
                    detail[qns].append([ele.split(']')[0]])
                #pqns=max(0,pqns-1)
                #print("L1",qns,pqns,detail[qns])
                if pqns==0:
                    qns+=1
            else:
                pqns+=1
                ele=""
                for k in i.split('['):
                    if k.find('BTL')!=-1:
                        ele=k
                        break
                try:
                    detail[qns][1].append(ele.split(']')[0])
                except:
                    detail[qns].append([ele.split(']')[0]])
                #pqns=max(0,pqns-1)
                #print("L2",qns,pqns,detail[qns])
                if pqns==0:
                    qns+=1
                    
        if qns>len(detail):
            break
    return detail
            

def find_DLs_1(temp,detail):
    qns=0
    pqns=0
    #print(detail)
    for i in temp:
        #print(qns,pqns)
        if i.startswith(str(qns+1)+'.')==True or i.startswith(str(qns+1)+')')==True:
            pqns=0
            qns+=1
        if i.find('[C')!=-1:
            if i.startswith(str(qns+1)+'.')==True or i.startswith(str(qns+1)+')')==True: 
                ele=""
                for k in i.split('['):
                    if k.find('DL')!=-1:
                        ele=k
                        break
                try:
                    detail[qns][2].append(ele.split(']')[0])
                except:
                    detail[qns].append([ele.split(']')[0]])
                #pqns=max(0,pqns-1)
                #print("L1",qns,pqns,detail[qns])
                if pqns==0:
                    qns+=1
            else:
                pqns+=1
                ele=""
                for k in i.split('['):
                    if k.find('DL')!=-1:
                        ele=k
                        break
                try:
                    detail[qns][2].append(ele.split(']')[0])
                except:
                    detail[qns].append([ele.split(']')[0]])
                #pqns=max(0,pqns-1)
                #print("L2",qns,pqns,detail[qns])
                if pqns==0:
                    qns+=1
                    
        if qns>len(detail):
            break
    return detail

            

def find_mark_split(temp,detail):
    qns=0
    incre=True
    arr=[]
    for i in temp:
        if i.startswith(str(qns+1)+'.')==True or i.startswith(str(qns+1)+')')==True or incre==False:
            incre=False
            if i.startswith(str(qns+1)+'.')==True or i.startswith(str(qns+1)+')')==True:
                if qns>0:
                    #print(arr)
                    detail[qns].append(arr)
                    detail[qns].append(sum(arr))
                    del arr
                    arr=[]
                qns+=1
            if incre==False:
                temp1=[j.strip('\t') for j in i.split(' ')]
                #print(temp)
                #try:
                    #print(qns,temp1[len(temp1)-1],temp1[len(temp1)-2][0],temp1[len(temp1)-3]=='+')
                #except:
                    #continue
                if temp1[len(temp1)-1].startswith('(') and temp1[len(temp1)-1][1] in '123456789':
                    
                    #print("l1",temp1[ind-1])
                    arr.append(int(temp1[len(temp1)-1].split('(')[1][0]))
                    if temp1[len(temp1)-2]=='+':
                        print("in loop 1")
                        ind=len(temp1)-2
                        while(temp1[ind]=='+'):
                            if temp1[ind-1].find('(')==-1:
                                print(temp1[ind-1])
                                arr.append(temp1[ind-1])
                            if temp1[ind-1][0]=='(':
                                print(temp1[ind-1])
                                arr.append(temp1[ind-1][1:])
                                
                            ind=ind-2
                try:
                    if temp1[len(temp1)-2][0] in '123456789' and temp1[len(temp1)-2][1]==')':
                        print("help")
                        print(qns)
                        arr.append(int(temp1[len(temp1)-2][0]))
                        if temp1[len(temp1)-3]=='+':
                            print("in loop 2")
                            ind=len(temp1)-3
                            while(temp1[ind]=='+'):
                                #print("in loop")
                                if temp1[ind-1].find('(')==-1:
                                    print(temp1[ind-1])
                                    arr.append(int(temp1[ind-1]))
                                if temp1[ind-1][0]=='(':
                                    print(temp1[ind-1])
                                    arr.append(int(temp1[ind-1][1:]))

                                ind=ind-2
                except:
                    continue
                if temp1[len(temp1)-2].startswith('(') and temp1[len(temp1)-2][1] in '123456789':
                    print("b0",temp1[len(temp1)-2])
                    arr.append(int(temp1[len(temp1)-2].split('(')[1][0]))
                    
                try:
                    if temp1[len(temp1)-3].startswith('(') and temp1[len(temp1)-3][1] in '123456789':
                        print("b1",temp1[len(temp1)-3])
                        arr.append(int(temp1[len(temp1)-3].split('(')[1][0:temp1[len(temp1)-3].split('(')[1].find(')')]))
                except:
                    continue
                #continue
    #print(arr)
    detail[qns].append(arr)
    detail[qns].append(sum(arr))
    del arr
    return detail
def find_part_splitup(temp):
    part=1
    psu={}
    bqns=0
    
    for i in temp:
        if i.lower().startswith('part'):
            print(i.split(' '))
        try:
            if i.lower().startswith('part'):
                psu[part]={}
                psu[part]['no_of_q']=sum([int(j.split('(')[1]) for j in i.split(' ') if j.startswith('(')])
                psu[part]['Marks']=sum([int(i.split(' ')[j+2]) for j in range(len(i.split(' '))) if i.split(' ')[j].startswith('(')] )
                psu[part]['qns']=[i for i in range(bqns+1,bqns+psu[part]['no_of_q']+1)]
                bqns=bqns+len(psu[part]['qns'])
                part+=1
        except:
            del psu[part]
            part+=1
    return psu

def update_details(psu,detail):
    for i in detail:
        if detail[i][2]==0:
            for j in psu:
                if i in psu[j]['qns']:
                    detail[i][4]=psu[j]['Marks']
                    detail[i][3].append(psu[j]['Marks'])
                    break
        else:
            for j in psu:
                if i in psu[j]['qns']:
                    
                    if detail[i][4]!=psu[j]['Marks']:
                        detail[i][4]=psu[j]['Marks']
                        detail[i][3]=[psu[j]['Marks']]
    return detail

def insertBLOB1(sem,year,title,qp):
    print("Inserting BLOB into python table")
    try:
        connection = establish_connection()

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO assessment_qps
                          (title,semester,year,details) VALUES (%s,%s,%s,%s)"""


        # Convert data into tuple format
        insert_blob_tuple = (title,sem,year,qp)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("file inserted successfully as a BLOB into qp table", result)
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

def insertBLOB2(dept,batch,sem,year,title,qp):
    print("Inserting BLOB into python table")
    try:
        connection = establish_connection()

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO CA_qps
                          (dept,batch,semester,year,title,details) VALUES (%s,%s,%s,%s,%s,%s)"""


        # Convert data into tuple format
        insert_blob_tuple = (dept,batch,sem,year,title,qp)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("file inserted successfully as a BLOB into qp table", result)
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))








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




def establish_connection():
    connection = mysql.connector.connect(host='localhost',
                                             database='obe_proj',
                                             user='root',
                                             password='1234',auth_plugin='mysql_native_password')
    return connection

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

@app.route("/login",methods=['POST'])
def login():
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


@app.route("/Dashboard",methods=['POST', 'GET'])

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
@app.route("/download_csv_2",methods=['POST', 'GET'])

def download_csv_2():
    if session['name']==None:
            return render_template("login.html")
    if request.method=='GET':
        return render_template('download_csv_2.html')
    else:
        dept=request.form['name']
        batch=request.form['batch']
        year=request.form['year']
        sem=request.form['sem']
        f = request.files['qp']  
        f2= request.files['csv']
        name = f.filename
        contents=f.read().decode('cp1252')
        print(type(contents))
        temp=contents.split('\r\n')
        print(temp)
        #tit=temp[6]+'-'+temp[3].split(' ')[1]+' '+temp[3].split(' ')[2]+'-'+temp[3].split(' ')[5]+' '+temp[3].split(' ')[6]
        title=temp[5]+" "+temp[2]+" "+temp[6]
        #list=['First Assessment','Second Assessment','End Semester']

        #for word in range(0,len(temp)):
            #if temp[word] in list:
                #title=temp[word+1]
                #break
        #for word in range(0,len(temp)):
            #if temp[word].lower().startswith('set'):
                #title=title+temp[word]
                #break
            #if temp[word].lower().startswith('course outcomes'):
                #title=title+'SET-0'
                #break
        print(title)
        qns=0
        #print(temp)
        #CO_map=get_CO_map(temp)
        qns1=find_qns(temp)
        detail={}
        for i in range(1,qns1+1):
            detail[i]=[]
        detail=find_COs_1(temp,detail)
        #print(detail)
        #detail
        detail=find_BTLs_1(temp,detail)
        print("_________________________BTL_____________________________")
        print(detail)
    
        detail=find_DLs_1(temp,detail)
        print("_________________________DL_____________________________")
        print(detail)
        detail=find_mark_split(temp,detail)
        print("--------------------mark---------------------------------------")
        print(detail)
        psu={}
        print("-----------------------------psu---------------------------")
        psu=find_part_splitup(temp)
        print(psu)
        detail=update_details(psu,detail)
        print('-------------------------------------------detail \n \n psu -------------------------------')
        print(detail,"\n\n",psu)
        print(title)
        #print(CO_map)
        k=generate_csv(detail,f2)
        k[0].to_csv('title2.csv', header=k[1], index=False)
        resp = make_response(k[0].to_csv(header=k[1], index=False))
        resp.headers["Content-Disposition"] = "attachment; filename={}.csv".format(title.encode('utf-8').decode('latin-1'))
       
        resp.headers["Content-Type"] = "text/csv"

        detail_file=json.dumps(detail).encode('utf-8')

        insertBLOB2(dept,batch,sem,year,title,detail_file)
        return resp
@app.route("/upload_csv_1",methods=['POST', 'GET'])

def upload_csv_1():
    if session['name']==None:
        return render_template("login.html")
    if request.method=='GET':
        return render_template('upload_csv_1.html')
    else:
        year=request.form['year']
        sem=request.form['sem']
        dept=request.form['dept']
        batch=request.form['batch']
        faculty=session["name"]
        qp=request.files['csv']
        cc=request.form['cc']
        df=pd.read_csv(qp)
        #print(df.to_dict())
        f=json.dumps(df.to_dict()).encode('utf-8')
        
        assess=request.form['ex']
        
        
        print(assess,faculty,cc,sem,year,dept,batch)
        connection=establish_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE Courses SET {} = %s WHERE course_id=%s AND faculty=%s AND sem=%s AND cyear= %s AND department= %s AND batch= %s ".format(assess),(f,cc,faculty,sem,year,dept,batch))
            connection.commit()
            if connection.is_connected():
                #cursor.close()
                #connection.close()
                print("MySQL connection is closed")
        except mysql.connector.Error as error:
            print("Failed to read BLOB data from MySQL table {}".format(error))
        cursor.execute("SELECT * from courses where faculty='{}'".format(session["name"]))
        record = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("dashboard1.html",records=record)

@app.route("/getcourseinfo",methods=['POST'])

def get_course_info():
    if session['name']==None:
        return render_template("login.html")
    if request.method=='POST':
        arr=[request.form["inp{}".format(i)] for i in range(1,7)]
        connection=establish_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * from courses where course_id='{}' and faculty='{}' and department ='{}' and batch='{}' and sem='{}' and Cyear='{}'".format(arr[0],arr[1],arr[2],arr[3],arr[4],arr[5]))
        record = cursor.fetchall()
        
        cursor.execute("SELECT * from assessment_qps where title like '%{}%'  and semester='{}' and year='{}'".format(arr[0],arr[4],arr[5]))
        record1 = cursor.fetchall()
        cursor.execute("SELECT * from CA_qps where title like '%{}%' and dept ='{}' and batch='{}' and semester='{}' and year='{}'".format(arr[0],arr[2],arr[3],arr[4],arr[5]))
        record2 = cursor.fetchall()
        cursor.execute("SELECT * from course_proporties2 where course_id like '%{}%'".format(arr[0]))
        record3 = cursor.fetchall()
        print(len(record3),arr[0])
        temp=json.loads(record3[0][2])
        #temp=5
        cursor.close()
        connection.close()
        if record[0][10]!=None:
            tab=pd.DataFrame(json.loads(record[0][10])).transpose()
            return render_template('course_info.html',records=record,qps=record1,ca=record2,prop=len(temp),tab=[tab.to_html()])
        else:
            return render_template('course_info.html',records=record,qps=record1,ca=record2,prop=len(temp))

@app.route("/mentorhomepage",methods=['POST'])
def get_course_info_1():
    if session['name']==None:
        return render_template("login.html")
    arr=[request.form["inp{}".format(i)] for i in range(1,7)]
    connection=establish_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * from courses where course_id='{}'  and sem='{}' and Cyear='{}'".format(arr[0],arr[4],arr[5]))
    record = cursor.fetchall()
    cursor.execute("SELECT * from course_proporties2 where course_id like '%{}%'".format(arr[0]))
    record3 = cursor.fetchall()
    cursor.execute("SELECT * from courses where course_id='{}'  and sem='{}' and Cyear='{}'and attainment IS NOT NULL".format(arr[0],arr[4],arr[5]))
    record4 = cursor.fetchall()
    mapping=json.loads(record3[0][2])
    #print(mapping)
    COs=[]
    for i in mapping:
        
        mapping[i].pop(-1)
        COs.append(mapping[i].pop(-1))
        mapping[i]=[int(j) for j in mapping[i]]
        
    print(COs,mapping)
    temp=pd.DataFrame(mapping).transpose()
    temp.columns=['PO0'+str(i+1) if i<9 else 'PO'+str(i+1) for i in range(temp.shape[1])]
    temp.index=['CO0'+str(i+1) for i in range(temp.shape[0])]
    #temp=temp.replace('0',None)
    if len(record4)==0:
        return render_template("error.html")
    if len(record4)>0:
        tsum=0
        cie_nsum=[]
        see_nsum=[]
        indirect_nsum=[]
        co=['CO0'+str(i+1) for i in range(temp.shape[0])]
        finaldf=pd.DataFrame([],columns=co)
        
        for i in record:
            try:
                strength=pd.DataFrame(json.loads(i[9])).shape[0]
                
                print(strength)
                attain=pd.DataFrame(json.loads(i[10]))
                try:
                    for i in range(len(attain.loc['CIE Attainment',:].values)):
                        cie_nsum[i]+= (attain.loc['CIE Attainment',:].values[i]*strength)
                except:
                    for i in range(len(attain.loc['CIE Attainment',:].values)):
                        cie_nsum.append(attain.loc['CIE Attainment',:].values[i]*strength)
                try:
                    for i in range(len(attain.loc['End Semester',:].values)):
                        see_nsum[i]+= (attain.loc['End Semester',:].values[i]*strength)
                except:
                    for i in range(len(attain.loc['End Semester',:].values)):
                        see_nsum.append(attain.loc['End Semester',:].values[i]*strength)
                try:
                    for i in range(len(attain.loc['Indirect Attainment',:].values)):
                        indirect_nsum[i]+= (attain.loc['Indirect Attainment',:].values[i]*strength)
                except:
                    for i in range(len(attain.loc['Indirect Attainment',:].values)):
                        indirect_nsum.append(attain.loc['Indirect Attainment',:].values[i]*strength)
                tsum+=strength
            except:
                continue
        cie_nsum=[i/tsum for i in cie_nsum]
        see_nsum=[i/tsum for i in see_nsum]
        indirect_nsum=[i/tsum for i in indirect_nsum]
        finaldf.loc['CIE Attainment',:]=cie_nsum
        finaldf.loc['CIE Level',:]=[2 if (i>40 and i<=60) else 3 if i>60 else 1 for i in finaldf.loc['CIE Attainment',:].values]
        finaldf.loc['SEE Attainment',:]=see_nsum
        finaldf.loc['SEE Level',:]=[2 if (i>40 and i<=60) else 3 if i>60 else 1 for i in finaldf.loc['SEE Attainment',:].values]
        x=[i for i in list(finaldf.loc['CIE Attainment',:].values)]
        y=[i for i in list(finaldf.loc['SEE Attainment',:].values)]
        z=[record3[0][5]*(x[i]/100)+record3[0][6]*(y[i]/100) for i in range(len(x))]
        finaldf.loc['Direct Attainment',:]=z
        x=[i for i in list(finaldf.loc['CIE Level',:].values)]
        y=[i for i in list(finaldf.loc['SEE Level',:].values)]
        z=[record3[0][5]*(x[i]/100)+record3[0][6]*(y[i]/100) for i in range(len(x))]
        finaldf.loc['Direct Level',:]=z
        finaldf.loc['Indirect Attainment',:]=indirect_nsum
        finaldf.loc['Indirect Level',:]=[2 if (i>40 and i<=60) else 3 if i>60 else 1 for i in finaldf.loc['Indirect Attainment',:].values]
        x1=list(finaldf.loc['Direct Attainment',:].values)
        x2=[0.8*x1[i]+0.2*float(indirect_nsum[i]) for i in range(len(x1))]
        finaldf.loc['Overall Attainment',:]=x2
        x1=list(finaldf.loc['Direct Level',:].values)
        x3=list(finaldf.loc['Indirect Level',:].values)
        x2=[0.8*x1[i]+0.2*x3[i] for i in range(len(x1))]
        finaldf.loc['Overall Level',:]=x2
        for i in finaldf.columns:
            if type(finaldf[i])!=object:
                finaldf[i]=finaldf.apply(lambda x: round(x[i],2),axis=1)
        x4=['Yes'if i>record3[0][4] else 'No' for i in finaldf.loc['Overall Attainment',:].values]
        finaldf.loc['Attainment?',:]=x4
        #print(finaldf)
        po_df=pd.DataFrame([],columns=temp.columns)
        po_attain=[]
        po_attain1=[]
        mapping=temp.transpose().to_dict()
        temp=temp.replace([0],[None])
        print(temp.info())
        for i in temp.columns:
            arr1=[int(i) if i!=None else 0 for i in temp[i].values]
            att=0
            print(arr1)
            for k in range(len(arr1)):
                if arr[k]!=0:
                    att=att+(x2[k]*arr1[k])
            if sum(arr1)>0:
                po_attain.append(att/sum(arr1))
                po_attain1.append(sum(arr1)/sum([1 for i in arr1 if i>0]))
            else:
                po_attain.append(None)
                po_attain1.append(sum(arr1))
        po_df.loc['PO Attainment']=po_attain
        po_df.loc['PAM']=po_attain1
        for i in po_df.columns:
            if type(po_df[i])!=object or type(po_df[i])!=str:
                po_df[i]=po_df.apply(lambda x: round(x[i],2),axis=1)    
        po_df.loc['Attainment?']=['Yes' if  po_attain[i]!=None and po_attain[i]>po_attain1[i]  else 'No' for i in range(len(po_attain))]
        print(po_df)
        #finaldf=finaldf.transpose()
        cursor.close()
        connection.close()
        
        

                
                

        return render_template("mentor_page.html", records=record,mapping=[temp.fillna('-').to_html(),finaldf.transpose().to_html(),po_df.fillna('-').to_html()],CO=COs)

@app.route("/upload_csv_2",methods=['POST', 'GET'])

def upload_csv_2():
    if session['name']==None:
        return render_template("login.html")
    if request.method=='GET':
        return render_template('upload_csv_2.html')
    else:
        year=request.form['year']
        sem=request.form['sem']
        dept=request.form['dept']
        batch=request.form['batch']
        #faculty=session["name"]
        qp=request.files['csv']
        param=request.form['choice']
        df=pd.read_csv(qp)
        #print(df.to_dict())
        f=json.dumps(df.to_dict()).encode('utf-8')
        
        
        
        
        #print(assess,faculty,cc,sem,year,dept,batch)
        connection=establish_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE CA_qps SET marks = %s WHERE title=%s  AND semester=%s AND year= %s AND dept= %s AND batch= %s ",(f,param,sem,year,dept,batch))
            connection.commit()
            if connection.is_connected():
                #cursor.close()
                #connection.close()
                print("MySQL connection is closed")
        except mysql.connector.Error as error:
            print("Failed to read BLOB data from MySQL table {}".format(error))
        cursor.execute("SELECT * from courses where faculty='{}'".format(session["name"]))
        record = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("dashboard1.html",records=record)


@app.route("/course_reg",methods=['POST', 'GET'])

def course_reg():
    if session['name']==None:
        return render_template("login.html")
    if request.method=='GET':
        return render_template('course_reg.html')
    if request.method=='POST':
        
        connection=establish_connection()
        cursor = connection.cursor()
        cid=request.form['courseid']
        cname=request.form['coursename']
        dept=request.form['dept']
        faculty=session["name"]
        batch=request.form['batch']
        sem=request.form['sem']
        year=request.form['year']
        threshold=request.form['threshold']
        internal=request.form['internal']
        try:
            mentor=request.form['mentor']
        except:
            mentor="no"
        f=request.files['file1']
        external=100-int(internal)
        contents=f.read().decode('cp1252')
        print(type(contents))
        temp=contents.split('\r')
        print(temp)
        
        res=CO_PO_map(temp)
        res2=CO_def2(temp,res)
        print(res)
        print(res2)
        detail_file=json.dumps(res).encode('utf-8')
        detail_file2=json.dumps(res2).encode('utf-8')
        insertBLOB_course(cid, cname, threshold,internal,external,detail_file,detail_file2)
        cursor.execute("INSERT INTO Courses (course_id ,faculty ,department ,batch ,sem,cyear,mentor)  VALUES ('{}','{}','{}','{}','{}','{}','{}') ".format(cid, faculty, dept,batch,sem,year,mentor))
        #cursor.execute("INSERT INTO Course_proporties (course_id ,course_name ,threshold ,internal ,external)  VALUES ('{}','{}','{}','{}','{}') ".format(cid, cname, threshold,internal,external))
        connection.commit()
        cursor.close()
        connection.close()
        return render_template('course_reg.html')


@app.route("/download_csv_1",methods=['GET','POST'])
def download_csv_1():
    if session['name']==None:
        return render_template("login.html")
    if request.method=='GET':
        return render_template('download_csv_1.html')
    else:
        print('uploading file')
        year=request.form['year']
        sem=request.form['sem']
        f = request.files['qp']  
        f2= request.files['namelist']
        name = f.filename
        contents=f.read().decode('cp1252')
        print(type(contents))
        temp=contents.split('\r\n')
        print(temp)
        #tit=temp[6]+'-'+temp[3].split(' ')[1]+' '+temp[3].split(' ')[2]+'-'+temp[3].split(' ')[5]+' '+temp[3].split(' ')[6]
        title=temp[5]+" "+temp[2]+" "+temp[6]
        #list=['First Assessment','Second Assessment','End Semester']

        #for word in range(0,len(temp)):
            #if temp[word] in list:
                #title=temp[word+1]
                #break
        #for word in range(0,len(temp)):
            #if temp[word].lower().startswith('set'):
                #title=title+temp[word]
                #break
            #if temp[word].lower().startswith('course outcomes'):
                #title=title+'SET-0'
                #break
        print(title)
        qns=0
        #print(temp)
        #CO_map=get_CO_map(temp)
        qns1=find_qns(temp)
        detail={}
        for i in range(1,qns1+1):
            detail[i]=[]
        detail=find_COs_1(temp,detail)
        #print(detail)
        #detail
        detail=find_BTLs_1(temp,detail)
        print("_________________________BTL_____________________________")
        print(detail)
    
        detail=find_DLs_1(temp,detail)
        print("_________________________DL_____________________________")
        print(detail)
        detail=find_mark_split(temp,detail)
        print("--------------------mark---------------------------------------")
        print(detail)
        psu={}
        print("-----------------------------psu---------------------------")
        psu=find_part_splitup(temp)
        print(psu)
        detail=update_details(psu,detail)
        print('-------------------------------------------detail \n \n psu -------------------------------')
        print(detail,"\n\n",psu)
        print(title)
        #sprint(CO_map)
        k=generate_csv(detail,f2)
        k[0].to_csv('title2.csv', header=k[1], index=False)
        resp = make_response(k[0].to_csv(header=k[1], index=False))
        resp.headers["Content-Disposition"] = "attachment; filename={}.csv".format(title.encode('utf-8').decode('latin-1'))
       
        resp.headers["Content-Type"] = "text/csv"

        detail_file=json.dumps(detail).encode('utf-8')

        insertBLOB1(sem,year,title,detail_file)
        return resp


        return render_template('download_csv_1.html')
def get_attainment_2(dff,dept,batch,sem,year,cc):

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='obe_proj',
                                             user='root',
                                             password='1234',auth_plugin='mysql_native_password')

        cursor = connection.cursor()
        #ia=[89.6,77.2,67.1,90.8]
        sql_fetch_blob_query = """SELECT details,marks from CA_qps where dept='{}' and batch='{}' and semester='{}' and year='{}' and title like'%{}%'""".format(dept,batch,sem,year,cc)
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()

        
        co_set=set()
        qp1={}
        #co_set.add('roll_no')
        df1=None
        
        for row in record:
            qp=json.loads(row[0])
            #print(row[1])
            qp2={}
            for i in qp:
                if len(qp[i][0])>1:
                    for j in range(len(qp[i][0])):
                        qp2[str(int(i)+0.1*(j+1))]=[qp[i][0][j],qp[i][3][j]]
                else:
                    qp2[str(i)]=[qp[i][0][0],qp[i][4]]
                for j in qp[i][0]:
                    co_set.add(j)
            for i in qp2:
                try:
                    qp1[qp2[i][0]]+=qp2[i][1]
                except:
                    qp1[qp2[i][0]]=qp2[i][1]
            temp=json.loads(row[1])
            df=pd.DataFrame(temp)
            df.drop(df.columns[0],axis=1,inplace=True)
            check=list(qp2.keys())
            try:
                if df1==None:
                    df1=pd.DataFrame(columns=['roll_no']+sorted(list(co_set)))
                    df1['roll_no']=df[df.columns[0]]
                    df1.fillna(0,inplace=True)
                    for i in range(1,len(qp)+1):
                        df1.loc[:,qp2[check[i-1]][0]]=df1.loc[:,qp2[check[i-1]][0]]+df.loc[:,df.columns[i-1]]
            except:
                for i in range(1,len(qp)+1):
                    df1.loc[:,qp2[check[i-1]][0]]=df1.loc[:,qp2[check[i-1]][0]]+df.loc[:,df.columns[i-1]]
        arr3={}
        for i in qp1:
            arr3[i]=df1[df1[i]>=0.5*qp1[i]].shape[0]*100/df1.shape[0]
        print(arr3)
        return arr3
            
        
            
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")    

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

def get_attainment_1(df,sem,year,cc,assess):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='obe_proj',
                                             user='root',
                                             password='1234',auth_plugin='mysql_native_password')

        cursor = connection.cursor()
        #ia=[89.6,77.2,67.1,90.8]
        
        sql_fetch_blob_query = """SELECT details,title from assessment_qps where title like'%{}%' and  semester='{}' and year='{}' and title like'%{}%'""".format(assess,sem,year,cc)
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        qp=None
        co_set=set()
        #co_set.add('roll_no')
        for row in record:
            qp=json.loads(row[0])
            print(row[1])
        qp1={}
        for i in qp:
            if len(qp[i][0])>1:
                for j in range(len(qp[i][0])):
                    qp1[str(int(i)+0.1*(j+1))]=[qp[i][0][j],qp[i][3][j]]
            else:
                qp1[str(i)]=[qp[i][0][0],qp[i][4]]
            for j in qp[i][0]:
                co_set.add(j)
        print(qp1)
        df1=pd.DataFrame(columns=['roll_no']+sorted(list(co_set)))
        df1['roll_no']=df[df.columns[0]]
        df1.fillna(0,inplace=True)
        check=list(qp1.keys())
        for i in range(1,len(qp1)+1):
            #print(df.columns[i])
            df1.loc[:,qp1[check[i-1]][0]]=df1.loc[:,qp1[check[i-1]][0]]+df.loc[:,df.columns[i-1]]
        #print(qp,df1)
        
        temp=pd.DataFrame(qp1).transpose()
        print(temp)
        arr2=temp.groupby(0).sum()[1].values
        print(arr2)
        #dff1=df1.describe()
        #dff1.drop(dff1.columns[0],axis=1,inplace=True)
        
        arr3={}
        for i in range(len(arr2)):
            arr3[df1.columns[i+1]]=df1[df1[df1.columns[i+1]]>=0.5*arr2[i]].shape[0]*100/df1.shape[0]
        #dff1.loc[assess,:]=arr3
        #print(dff1)       
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return arr3    

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

@app.route("/get_attainments", methods=["POST"])
def get_attainment():
    if session['name']==None:
        return render_template("login.html")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='obe_proj',
                                             user='root',
                                             password='1234',auth_plugin='mysql_native_password')

        cursor = connection.cursor()
        cc=request.form['cc']
        batch=request.form['batch']
        sem=request.form['sem']
        year=request.form['year']
        dept=request.form['dept']
        faculty=session['name']
        sql_fetch_blob_query = """SELECT * from Course_proporties2 where course_id like'%{}%'""".format(cc)
        cursor.execute(sql_fetch_blob_query)
        record1 = cursor.fetchall()
        co_map=json.loads(record1[0][2])
        arr=['CO0'+str(i+1) for i in range(len(co_map))]
        ia=[request.form[i] for i in arr]
        df1=pd.DataFrame(columns=arr)
        sql_fetch_blob_query = """SELECT * from Courses where department='{}' and faculty='{}' and batch='{}' and sem='{}' and cyear='{}' and course_id='{}'""".format(dept,faculty,batch,sem,year,cc)
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            #print(row)
            arr={6:"First Assessment",7:"Second Assessment",8:"Continuous Assessment",9:"End Semester"}
            for i in arr:
                if i!=8:
                    temp=json.loads(row[i])
                    df=pd.DataFrame(temp)
                    df.drop(df.columns[0],axis=1,inplace=True)
                    #file1 = row[1].decode('utf-8')
                    
                    val=get_attainment_1(df,sem,year,cc,arr[i])
                    if len(val)<len(co_map):
                        for j in co_map:
                            if j not in val:
                                val[j]=None
                    val=dict(sorted(val.items()))
                    df1.loc[arr[i],:]=list(val.values())
                    #print(df.describe())
                if i==8:
                    val=get_attainment_2(None,dept,batch,sem,year,cc)
                    #val=get_attainment_1(df,sem,year,cc,arr[i])
                    print(val)
                    if len(val)<len(co_map):
                        for j in co_map:
                            if j not in val:
                                val[j]=None
                    val=dict(sorted(val.items()))
                    df1.loc[arr[i],:]=list(val.values())
                    df1.loc['CIE Attainment',:]=df1.replace(0,None).mean().values
                    df1.loc['CIE Level']=[2 if (i>40 and i<=60) else 3 if i>60 else 1 for i in df1.mean().values]
        
        x=[i for i in list(df1.loc['CIE Attainment',:].values)]
        y=[i for i in list(df1.loc['End Semester',:].values)]
        df1.loc['SEE Level']=[2 if (i>40 and i<=60) else 3 if i>60 else 1 for i in y]
        z=[record1[0][5]*(x[i]/100)+record1[0][6]*(y[i]/100) for i in range(len(x))]
        df1.loc['Direct Attainment',:]=z
        x=[i for i in list(df1.loc['CIE Level',:].values)]
        y=[i for i in list(df1.loc['SEE Level',:].values)]
        z=[record1[0][5]*(x[i]/100)+record1[0][6]*(y[i]/100) for i in range(len(x))]
        df1.loc['Direct Level',:]=z
        df1.loc['Indirect Attainment',:]=[float(i) for i in ia]
        df1.loc['Indirect Level',:]=[2 if (i>40 and i<=60) else 3 if i>60 else 1 for i in df1.loc['Indirect Attainment',:].values]
        x1=list(df1.loc['Direct Attainment',:].values)
        x2=[0.8*x1[i]+0.2*float(ia[i]) for i in range(len(x1))]
        df1.loc['Overall Attainment',:]=x2
        x1=list(df1.loc['Direct Level',:].values)
        x3=list(df1.loc['Indirect Level',:].values)
        x2=[0.8*x1[i]+0.2*x3[i] for i in range(len(x1))]
        df1.loc['Overall Level',:]=x2
        print(df1)
        for i in df1.columns:
            if type(df1[i])!=object:
                df1[i]=df1.apply(lambda x: round(x[i],2),axis=1)
        f=json.dumps(df1.to_dict()).encode('utf-8')
        try:
            cursor.execute("UPDATE courses SET attainment = %s WHERE course_id=%s  AND sem=%s AND cyear= %s AND department= %s AND batch= %s ",(f,cc,sem,year,dept,batch))
            connection.commit()
            if connection.is_connected():
                #cursor.close()
                #connection.close()
                print("MySQL connection is closed")
        except mysql.connector.Error as error:
            print("Failed to read BLOB data from MySQL table {}".format(error))  
        cursor.execute("SELECT * from courses where faculty='{}'".format(session["name"]))
        record = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("dashboard1.html",records=record)
    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))


@app.route("/log_out")
def log_out():
    session["name"]=None
    print(session["name"])
   

    return render_template('login.html')



@app.route("/plot_co", methods=["POST"])
def course_outcome():
    if session['name']==None:
        return render_template("login.html")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='obe_proj',
                                             user='root',
                                             password='1234',auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        cc=request.form['cc']
        assess=request.form['assess']
        batch=request.form['batch']
        sem=request.form['sem']
        year=request.form['year']
        dept=request.form['dept']
        faculty=session['name']
        sql_fetch_blob_query = """SELECT * from Courses where department='{}' and faculty='{}' and batch='{}' and sem='{}' and cyear='{}' and course_id='{}'""".format(dept,faculty,batch,sem,year,cc)
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        check_arr={'p1':6,'p2':7,'endsem':9}
        df=pd.DataFrame(json.loads(record[0][check_arr[assess]])).transpose()
        count=df[df.columns[0]].count()
        roll_no=df[df.columns[0]]
        df2=pd.DataFrame(json.loads(record[0][check_arr[assess]]))

        title=cc+'_'+dept+batch+'_SEM'+sem+'_'+year
        sql_fetch_blob_query = """SELECT details from assessment_qps where title like '%{}%' and semester='{}' and year='{}' """.format(cc,sem,year)
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        
        dict2=json.loads(record[0][0])
        #print("dataframe pf qs paper",df)
        #print("dictionary",dict3)
        course=[]
        dict3={}
        for i in dict2.keys():
            l=dict2[i]
            if len(l[0])>1:
                for j in range(len(l[0])):
                    dict3[str(i)+'.'+str(j+1)]=[dict2[i][0][j],dict2[i][1][j],dict2[i][2][j],[dict2[i][3][j]],dict2[i][3][j]]
                    course.append(l[0][j])
            else:
                dict3[str(i)]=[dict2[i][0][0],dict2[i][1][0],dict2[i][2][0],dict2[i][3],dict2[i][4]]
                course.append(l[0][0])
        course=["roll_no"]+list(set(course))
                
        list1=[0 for i in range(len(course))]
        df1 = pd.DataFrame([],columns=(course))
        for i in range(count):
            list1=[]
            list1.append(roll_no[i])
            for i in range(len(course)-1):
                list1.append(0)
            df1.loc[len(df1.index)] = list1
        
        parts_track=0
        check=list(dict3.keys())
        for i in range(len(check)): 

            l=dict3[check[i]]
            course_outcome=l[0]
            total_mark=l[-1]
            parts=l[3]
            
            
            if len(parts)==1:
                
                df1[course_outcome]+=df[df.columns[i+1]]
            
            else:
               
                df1[course_outcome]+=df[df.columns[i+1+len(parts)+int(parts_track)]]
                parts_track+=len(parts)
        
        cursor.close()
        connection.close()
        #print("df1",df1)
        assess_map={'p1':'Periodicals 1','p2':'Periodicals 2','endsem':'End Semester'}
        recs=[cc,dept,batch,sem,year,assess_map[assess]]
        return co_plotting(dict3,df1,df2,recs)

    
    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))                                        
   
    
    
def co_plotting(dict3,df1,df2,recs):
    #fig=plt.figure(figsize=(6,6))
    plt.subplot(2,3,1)
    df4=pd.DataFrame(dict3).transpose()
    temp1=[0.12 if i==max(df4.groupby(0).sum()[4]) else 0 for i in df4.groupby(0).sum()[4]]
    plt.pie(df4.groupby(0).sum()[4],explode=temp1,radius=1.4,shadow=True,labels=df4[0].unique(),autopct='%.0f%%',textprops={'fontsize':9,'family':'arial'})
    plt.subplot(2,3,3)
    df4=pd.DataFrame(dict3).transpose()
    temp1=[0.12 if i==max(df4.groupby(1).sum()[4]) else 0 for i in df4.groupby(1).sum()[4]]
    plt.pie(df4.groupby(1).sum()[4],radius=1.4,explode=temp1,shadow=True,labels=df4[1].unique(),autopct='%.0f%%',textprops={'fontsize':9,'family':'arial'})
    plt.subplot(2,3,5)
    df4=pd.DataFrame(dict3).transpose()
    temp1=[0.12 if i==max(df4.groupby(2).sum()[4]) else 0 for i in df4.groupby(2).sum()[4]]
    plt.pie(df4.groupby(2).sum()[4],radius=1.4,explode=temp1,shadow=True,labels=df4[2].unique(),autopct='%.0f%%',textprops={'fontsize':9,'family':'arial'})
    
    
    # arr1=df1.mean().values
    arr2=df4.groupby(0).sum()[4].values
    # for i in range(len(arr2)):
    #     arr1[i]=round((arr1[i]/arr2[i])*100,1)
    # # fig,axes=plt.subplots(1,len(arr1),squeeze=False,figsize=(3*len(arr1),2))

    # for i in range(1,len(arr1)+1):
    #     plt.subplot(2,3,i+1)
    #     temp=df4.groupby(0).get_group('CO0{}'.format(i))[2].value_counts()
    #     sns.barplot(x=temp.keys(),y=temp.values)
    #     # axes[0,i-1].set_title('CO0{}'.format(i))
    # l=len(arr1)
    # plt.subplot(2,3,l+1)
    # l=l+1
    # arr2=df4.groupby(0).sum()[4].values
    # arr3={}
    # for i in range(1,len(arr2)+1):
    #     temp=len(df1[df1['CO0{}'.format(i)]>=(0.5*arr2[i-1])])
    #     arr3['CO0{}'.format(i)]=temp
    # sns.barplot(x=list(arr3.keys()),y=list(arr3.values()))
    
   
    # plt.subplot(2,4,l+1)
    command="print(df1["
    for i in range(1,len(arr2)+1):
        if i==len(arr2):
            temp="(df1['CO0"+str(i)+"']>=(0.7*{}))])".format(arr2[i-1])
        else:
            temp="(df1['CO0"+str(i)+"']>=(0.7*{})) & ".format(arr2[i-1])
        command+=temp
    res=exec(command)

  
   
    


    pngImage = io.BytesIO()
    FigureCanvas(plt.gcf()).print_png(pngImage)
    plt.close()
    df4.columns=['CO','BTL','DL','Mark-split','Total']
    pngImageB64String = base64.b64encode(pngImage.getvalue()).decode("UTF-8")
    return render_template("image.html",tables=[df4.to_html(),df2.describe().transpose().to_html()], titles=[''], image=pngImageB64String,rec=recs)



@app.route("/downloadattainment", methods=["POST"])

def download_attainment_1():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='obe_proj',
                                             user='root',
                                             password='1234',auth_plugin='mysql_native_password')

        cursor = connection.cursor()
        cc=request.form['cc']
        batch=request.form['batch']
        sem=request.form['sem']
        year=request.form['year']
        dept=request.form['dept']
        faculty=session['name']
        sql_fetch_blob_query = """SELECT * from Courses where department='{}' and faculty='{}' and batch='{}' and sem='{}' and cyear='{}' and course_id='{}'""".format(dept,faculty,batch,sem,year,cc)
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        df=pd.DataFrame(json.loads(record[0][10])).transpose()
        resp = make_response(df.to_csv())
        title=cc+'_'+dept+batch+'_SEM'+sem+'_'+year
        resp.headers["Content-Disposition"] = "attachment; filename={}.csv".format(title)
        resp.headers["Content-Type"] = "text/csv"
        cursor.close()
        connection.close()
        return resp

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))









if __name__ == "__main__":
    app.run(debug=True)