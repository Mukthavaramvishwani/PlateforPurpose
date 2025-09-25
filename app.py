from flask import Flask, request, render_template, redirect,flash ,session,url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

app.secret_key = 'sneha'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Enter your MySQL username
app.config['MYSQL_PASSWORD'] = 'root'  # Enter your MySQL password
app.config['MYSQL_DB'] = 'pfp'  # Enter your MySQL database name

mysql = MySQL(app)
@app.route('/')
def login():
    return render_template('welcome.html')
@app.route('/user_login')
def loginpage_user():
    return render_template('login.html')
@app.route('/org_login')
def loginpage_org():
    return render_template('orglogin.html')
@app.route('/login_submit', methods=['POST'])
def login_submit():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT password FROM user_login WHERE email = %s", (email,))
        user = cur.fetchone()
        if user is not None and password==user[0]:
                return render_template('home.html')
        else:
                return render_template('login.html')
@app.route('/orglogin_submit', methods=['POST'])
def orglogin_submit():
    if request.method == 'POST':
        email = request.form['org_number']
        password = request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT password FROM org_login WHERE number= %s", (email,))
        user = cur.fetchone()
        if user is not None and password==user[0]:
                return render_template('orghome.html')
        else:
                return render_template('orglogin.html')
@app.route('/user_register')
def user_register():
     return render_template('signup.html')
@app.route('/submit_signup', methods=['GET','POST'])
def user_registersave():
     if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        number=request.form['mobile']
        location=request.form['location']
        pincode=request.form['pincode']             
        password=request.form['password']
        confirm_password = request.form['confirm_password']
        # print(name,email,number,location,pincode,password)
        cur=mysql.connection.cursor()
        if password != confirm_password:
          return render_template('signup.html', error="Passwords do not match")
        cur = mysql.connection.cursor()
        try:
            cur.execute("insert into user_login (name,email,Mobile,location,pincode,password) values(%s,%s,%s,%s,%s,%s)",(name,email,number,location,pincode,password,))
            mysql.connection.commit()
            return redirect('/user_login')
        except Exception as e:
            return render_template('signup.html')#, error=str(e)
        finally:
            cur.close()
     return render_template('signup.html')
@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the login page or any other page you prefer
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)