from flask import Flask,render_template,request,redirect,flash
import matplotlib.pyplot as plt
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField,PasswordField,SelectField,FileField
import numpy as np
from flask_mysqldb import MySQL
from wtforms.validators import Length, EqualTo, Email,NumberRange,DataRequired,Regexp,InputRequired
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import os
import datetime

app= Flask(__name__)
app.config['SECRET_KEY']='asxbjasgdajsckjnac7987' 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'flask'
mysql = MySQL(app)
class AdminForm(FlaskForm):
    name = StringField(label='Student Name :',validators=[Length(max=35, message="Max Length Of The Name Should be 35 Character"),DataRequired()])
    id = StringField(label='Student Id :',validators=[Length(min=10, max=10, message="Id Should Be 10 Character"), DataRequired(),Regexp(regex="[0-9A-Z]*", message="Id Must Contain AlphaNumeric Character ")])
    age = IntegerField(label='Age :',validators=[NumberRange(min=18, max=26, message="Enter The Vaid Age(18-26)"), DataRequired()])
    sex = StringField(label='Gender (M/F/O) :', validators=[Length(min=1, max=1), DataRequired(), Regexp(regex="M|F|O",message="Enter M(male) F(female) O(others)")])
    submit = SubmitField(label='Add Admin')

@app.route('/history')
def history():
    usn = request.args.get('id')
    val = request.args.get('balance')
    cur = mysql.connection.cursor()
    print(usn)
    cur.execute("SELECT order_id,order_name,date_time,price FROM orders WHERE student_id=%s;",(usn,))
    list = cur.fetchall()
    cur.close()
    return render_template('history.html',item=list,id=usn,amt=val,user_name=usn)

@app.route('/addadmin',methods=['GET','POST'])
def Add_admin():
         form = AdminForm()
         if form.validate_on_submit():
             if request.method == 'POST':
                 name = form.name.data
                 id = form.id.data
                 age = form.age.data
                 sex = form.sex.data
                 print(name,age,sex,id)
         if form.errors != {}:
             for error_msg in form.errors.values():
                   flash(error_msg, category='danger')
         return render_template('addadminbyroot.html', form=form)
class order_item(FlaskForm):
    submit = SubmitField(label='order')


class SupplierForm(FlaskForm):
    name = StringField(label='Student Name :',validators=[Length(max=35, message="Max Length Of The Name Should be 35 Character"),DataRequired()])
    id = StringField(label='Student Id :',validators=[Length(min=10, max=10, message="Id Should Be 10 Character"), DataRequired(),Regexp(regex="[0-9A-Z]*", message="Id Must Contain AlphaNumeric Character ")])
    age = IntegerField(label='Age :',validators=[NumberRange(min=18, max=26, message="Enter The Vaid Age(18-26)"), DataRequired()])
    sex = StringField(label='Gender (M/F/O) :', validators=[Length(min=1, max=1), DataRequired(), Regexp(regex="M|F|O",message="Enter M(male) F(female) O(others)")])
    submit = SubmitField(label='Add Supplier')

@app.route('/addsupplier',methods=['GET','POST'])
def Add_supplier():
         form = SupplierForm()
         if form.validate_on_submit():
             if request.method == 'POST':
                 name = form.name.data
                 id = form.id.data
                 age = form.age.data
                 sex = form.sex.data
                 print(name,age,sex,id)
         if form.errors != {}:
             for error_msg in form.errors.values():
                   flash(error_msg, category='danger')
         return render_template('addsuppliersbyroot.html', form=form)

class LoginForm(FlaskForm):
    type= SelectField(label='Account Type: ',choices=[('Admin'),('Student')])
    id = StringField(label='Id :',validators=[Length(min=10, max=10, message="Id Should Be 10 Character"), DataRequired(), Regexp(regex="[0-9A-Z]*",message="Id Must Contain AlphaNumeric Character ")])
    password = PasswordField(label='Password :',validators=[Length(min=8, max=20, message="Password Must be Between 8-20 Character Long"),DataRequired()])
    submit = SubmitField(label='Login')

@app.route('/login',methods=['GET','POST'])
def Login():
    form = LoginForm()
    value=0
    if form.validate_on_submit():
         if request.method == 'POST':
               id = form.id.data
               password = form.password.data
               type= form.type.data
               cur = mysql.connection.cursor()
               if type == "Admin":
                   value=cur.execute("SELECT id,password FROM Admin WHERE id=%s AND password= %s;",(id,password))
               if type == "Student":
                   value=cur.execute("SELECT id,student_password,balance FROM Student WHERE id=%s AND student_password=%s;",(id,password))
               result=cur.fetchall()
               if value > 0 :
                  cur.close()
                  if type == "Student" :
                    id = result[0][0]
                    balance = result[0][2]
                    return redirect('/home?id={}&balance={}'.format(id,balance))
                  if type == "Admin" :
                   return redirect('/admin')
               else :
                   flash("Id And Password Missmatch", category='danger')
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(error_msg,category='danger')
    return  render_template('login.html',form=form)

class RegisterForm(FlaskForm):
    name = StringField(label='Student Name :',validators=[Length(max=35,message="Max Length Of The Name Should be 35 Character"),DataRequired()])
    id = StringField(label='Student Id :',validators=[Length(min=10,max=10,message="Id Should Be 10 Character"),DataRequired(),Regexp(regex="[0-9A-Z]*",message="Id Must Contain AlphaNumeric Character ")])
    age = IntegerField(label='Age :',validators=[NumberRange(min=18,max=26,message="Enter The Vaid Age(18-26)"),DataRequired()])
    sex = StringField(label='Gender (M/F/O) :',validators=[Length(min=1,max=1),DataRequired(),Regexp(regex="M|F|O",message="Enter M(male) F(female) O(others)")])
    roomno = StringField(label='Room No :',validators=[Length(min=1,max=3,message="Enter Valid Room No"),DataRequired()])
    email = StringField(label='Email :',validators=[Email(),DataRequired()])
    password= PasswordField(label='Password :',validators=[Length(min=8,max=20,message="Password Must be Between 8-20 Character Long"),DataRequired()])
    cpassword = PasswordField(label='Confirm Password :',validators=[EqualTo('password'),DataRequired()])
    branch = SelectField(label='Branch: ', choices=[('CSE'), ('ISE'), ('ENC'), ('EEE'), ('CE'), ('ME'), ('IPE')])
    submit = SubmitField(label='Create Account')

@app.route('/register',methods=['GET','POST'])
def Register():
    form=RegisterForm()
    if form.validate_on_submit():
         if request.method == 'POST':
               name = form.name.data
               email = form.email.data
               id = form.id.data
               roomno = form.roomno.data
               age = form.age.data
               sex = form.sex.data
               password = form.password.data
               branch = form.branch.data
               cur = mysql.connection.cursor()
               cur.execute("INSERT INTO student(id,student_name,age,gender,room_no,email,student_password,branch) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);",(id,name,str(age),sex,roomno,email,password,branch))
               mysql.connection.commit()
               cur.close()
               return redirect('/home?id={}&balance=0'.format(id))
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(error_msg,category='danger')
    return  render_template('register.html',form=form)

@app.route('/home',methods=['GET','POST'])
def Home() :
    usn = request.args.get('id')
    val = request.args.get('balance')
    date = datetime.datetime.now()
    date = str(date)
    date = date[0:19]


    if request.method == 'POST':
        order_name = request.args.get("order_name")
        order_value = request.args.get("order_value")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE student set balance=balance+%s WHERE id=%s", (order_value,usn))
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT id,email,balance FROM student WHERE id=%s",(usn,))
        record = cur.fetchall()
        val=record[0][2]
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO orders(order_name,price,student_id,email,date_time) VALUES(%s,%s,%s,%s,%s);",(order_name, order_value,record[0][0],record[0][1],date))
        mysql.connection.commit()
        cur.close()


    itemnames1=[{'name': 'Idli','src': 'idli.png','no':1,'amount':20 },
               {'name': 'Idli Vada','src': 'Idly-Vada.png','no':2,'amount':25 },
               {'name': 'Masala Dosa','src': 'masala.png','no':3 ,'amount':30},
               {'name': 'Pulav','src': 'pulav.png','no':4 ,'amount':35},
    ]
    itemnames2 = [{'name': 'Puri', 'src': 'puri1.jpeg', 'amount': 20},
                  {'name': 'Upma', 'src': 'upma.jpeg', 'amount': 25},
                  {'name': 'Puliyogare', 'src': 'Puliyogare.jpg', 'amount': 25},
                  {'name': 'Parotta Dal ', 'src': 'parota.jpeg', 'amount': 30},
                  ]



    return render_template('home.html',user_name=usn,amount='1000',item1=itemnames1,item2=itemnames2,id=usn,amt=val)


@app.route('/contact',methods=['POST','GET'])
def Contact_Us() :
    usn = request.args.get('id')
    val = request.args.get('balance')
    if request.method == 'POST':
        order_id = request.form.get("order-id")
        usn = request.form.get("usn")
        email = request.form.get("email")
        text = request.form.get('text')
        cur = mysql.connection.cursor()
        value = cur.execute("SELECT order_id FROM orders WHERE order_id=%s and student_id=%s",(order_id,usn))
        result = cur.fetchall()
        if  cur.rowcount != 0 :
                print(usn,email,text)
                cur.execute("UPDATE orders SET description=%s WHERE order_id=%s;",(text,order_id))
                flash("Successfully submitted", category='success')
                mysql.connection.commit()
                cur.close()
                return redirect('/contact?id={}&balance={}'.format(usn,val))
        else :
            flash("Order-Id does not exist", category='danger')




    return render_template('contact.html',amount='1000',id=usn,amt=val,user_name=usn)

@app.route('/')
@app.route('/mess managment')
def mess_managment() :
     return render_template('messmanagment.html')

@app.route('/admin',methods=['POST','GET'])
def Admin() :
    if request.method == 'POST':
        order_id = request.args.get("order_id")
        value = request.args.get("value")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE orders SET done=1 WHERE order_id=%s;", (order_id,))
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE amount set amt=amt+%s;", (value,))
        mysql.connection.commit()
        cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT order_id,order_name,room_no,student_id,student.student_name,price FROM orders,student WHERE done=0 and student.id=orders.student_id ORDER BY order_id;")
    orders = cur.fetchall()
    cur.execute("SELECT * FROM amount;")
    amount= cur.fetchall()
    cur.close()
    return render_template('admin.html',user_name='Admin',item=orders,mess_amount=amount[0][0])

@app.route('/admin/suppliers')
def Suppliers() :
    cur = mysql.connection.cursor()
    cur.execute("SELECT supplier_name,gender FROM supplier;")
    list = cur.fetchall()
    return render_template('suppliers.html',user_name='Admin',item=list)


@app.route('/admin/payment',methods=['POST','GET'])
def Payment() :
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        student_id = request.args.get("student_id")
        cur.execute("UPDATE student SET balance=0 WHERE id=%s;", (student_id,))
        mysql.connection.commit()
        cur.close()
    cur=mysql.connection.cursor()
    cur.execute("SELECT id,room_no,student_name,age,gender,branch,balance FROM student ORDER BY balance DESC;")
    list=cur.fetchall()
    cur.close()
    if request.method == 'POST':
        student_id = request.args.get("student_id")
    return render_template('payment.html',user_name='Admin',item=list)

@app.route('/admin/statistics')
def Statistics() :
    x = datetime.datetime.now()
    year = int(x.strftime("%Y"))
    month= int(x.strftime("%m"))
    day = int(x.strftime("%d"))
    if day>28 :
        day=28
    if month == 1:
        month=12
        year=year-1
    else :
        month=month-1
    year=str(year)
    month=str(month)
    day=str(day)
    last_date=year+"-"+month+"-"+day+"%"

    y = str(x)

    y=y[:19]
    today_date = y[0:10]
    today_date=today_date+"%"

    #lastmonth order details
    cur = mysql.connection.cursor()
    cur.execute(" SELECT order_name,COUNT(order_id) FROM orders  WHERE DATE(date_time) >= %s AND  DATE(date_time) <= %s GROUP BY order_name;",(last_date,today_date))
    List = cur.fetchall()
    cur.close()
    df = DataFrame(List, columns=['order_Name', 'Total'])
    print(df)

    food = df["order_Name"].tolist()
    no = df["Total"].tolist()

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(food, no, color='blue',
            width=0.2)

    plt.xlabel("Food offered", )
    plt.ylabel("No. of orders")
    plt.title("No of Student order placed in last month")

    os.remove("C:/Users/HP/flaskprojects/static/image.jpg")
    plt.savefig("C:/Users/HP/flaskprojects/static/image.jpg")

    #lastmonth complaints
    cur = mysql.connection.cursor()
    cur.execute(" SELECT order_name,COUNT(order_id) FROM orders  WHERE DATE(date_time) >= %s AND  DATE(date_time) <= %s AND description IS NOT NULL GROUP BY order_name;",(last_date, today_date))
    List = cur.fetchall()
    cur.close()
    df = DataFrame(List, columns=['order_Name', 'Total'])
    print(df)

    foodofcomp = df["order_Name"].tolist()
    noofcomplaints = df["Total"].tolist()

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(foodofcomp, noofcomplaints, color='blue',
            width=0.2)

    plt.xlabel("Food offered", )
    plt.ylabel("No. of Complaints")
    plt.title("No of Student Complaints made in last month")
    # x = plt.show()
    os.remove("C:/Users/HP/flaskprojects/static/comp.jpg")
    plt.savefig("C:/Users/HP/flaskprojects/static/comp.jpg")
    #no of students per branch
    cur = mysql.connection.cursor()
    cur.execute("SELECT branch,COUNT(id) FROM student GROUP BY branch;")
    List = cur.fetchall()
    cur.close()
    df = DataFrame(List,columns=['Branch_Name','Total'])
    print(df)


    branch = df["Branch_Name"].tolist()
    noofstudents = df["Total"].tolist()
    print(branch)
    print(noofstudents)


    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(branch, noofstudents, color='blue',
            width=0.2)

    plt.xlabel("BRANCH", )
    plt.ylabel("No. of Students")
    plt.title("No of Student Per Branch")
    os.remove("C:/Users/HP/flaskprojects/static/students.jpg")
    plt.savefig("C:/Users/HP/flaskprojects/static/students.jpg")
    #todays order
    cur = mysql.connection.cursor()
    cur.execute("select order_name,COUNT(order_id) FROM orders WHERE date_time Like %s;",(today_date,))
    List = cur.fetchall()
    cur.close()
    df = DataFrame(List, columns=['order_name', 'Total'])
    print(df)

    foodfortoday = df["order_name"].tolist()
    ordersofday = df["Total"].tolist()

    fig = plt.figure(figsize=(10, 5))

    plt.bar(foodfortoday, ordersofday, color='blue',
            width=0.2)

    plt.xlabel("Food offered", )
    plt.ylabel("No. of orders")
    plt.title("No of Student order placed today")
    # x = plt.show()
    os.remove("C:/Users/HP/flaskprojects/static/imageofday.jpg")
    plt.savefig("C:/Users/HP/flaskprojects/static/imageofday.jpg")

    #todays complaint
    cur = mysql.connection.cursor()
    cur.execute("select order_name,COUNT(order_id) FROM orders WHERE date_time Like %s AND description IS NOT NULL;", (today_date,))
    List = cur.fetchall()
    cur.close()
    df = DataFrame(List, columns=['order_name', 'Total'])
    print(df)

    compfood = df["order_name"].tolist()
    compnumbers = df["Total"].tolist()
    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(compfood, compnumbers, color='blue',
            width=0.2)
    plt.xlabel("Food offered", )
    plt.ylabel("No. of Complaints")
    plt.title("No of Student Complaints made today")
    os.remove("C:/Users/HP/flaskprojects/static/todayscomp.jpg")
    plt.savefig("C:/Users/HP/flaskprojects/static/todayscomp.jpg")


    return render_template('stat.html',user_name='Admin',out="/static/image.jpg",comp="/static/comp.jpg",stu="/static/students.jpg",ord="/static/imageofday.jpg",todaycomp="/static/todayscomp.jpg")


@app.route('/admin/queries',methods=['POST','GET'])
def Queries() :
    if request.method == 'POST':
        order_id = request.args.get("order_id")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE orders SET solved=1 WHERE order_id=%s;", (order_id,))
        mysql.connection.commit()
        cur.close()

        print(order_id)
    cur = mysql.connection.cursor()
    cur.execute("SELECT order_id,order_name,student_id,price,date_time,description FROM orders WHERE solved!=1")
    list = cur.fetchall()

    return render_template('queries.html',user_name='Admin',item=list)
