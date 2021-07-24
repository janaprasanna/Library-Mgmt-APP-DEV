from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_mysqldb import MySQL
from sensitiveinfo import *
from random import randint, random, randrange
''' tutorial on sql alchemy - adding,deleting and updating users'''


app = Flask(__name__)
#MySql configuration
app.config["MYSQL_HOST"] = mysql_host
app.config["MYSQL_USER"] = mysql_user
app.config["MYSQL_PASSWORD"] =mysql_password
app.config["MYSQL_DB"] = mysql_db
#mysql = MySQL(app)
mysql = MySQL(app)
#mysql.init_app(app)


app.secret_key = "jana"




#db.Model is a inheritance from which the functions (such as columns), keywords are used



#to Display all the user details from the db

@app.route('/view')
def viewdb():
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM users")
    if result>0:
        userdetails = cursor.fetchall()
    return render_template('view.html',values=userdetails)


def chkusers(email):
    cursor = mysql.connection.cursor()
   # result = cursor.execute(f"SELECT email FROM users WHERE email='{email}'")
    cursor.execute("select email from users where email=%s", (email,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False

def chkpasswd(p1,p2):
    if p1==p2:
        return True;
    else:
        return False;

def chklogin(email,passwd):
    cursor = mysql.connection.cursor()
    cursor.execute("select name,email,password from users where email=%s and password=%s",(email,passwd))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False



@app.route('/home')
@app.route('/')
def home():
    return render_template('child.html')

@app.route('/admin',methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        a_id = admin()
        a_name = request.form["a_name"]
        a_email = request.form["a_email"]
        a_password = request.form["a_password"]
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO admin(admin_name,admin_password, admin_email) VALUES(%s,%s,%s)",(a_name,a_password,a_email))
        mysql.connection.commit()
    return render_template('admin.html')

def admin():
    admin_id = randint(100000, 900000)
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO admin(admin_id) VALUES(%d)",(admin_id))
    mysql.connection.commit()
    cursor.close()
    return admin_id

@app.route('/signup',methods=["POST","GET"])
def signup():
    if request.method == "POST":
        username = request.form["name"]
        usermail = request.form["email"]
        userpasswd = request.form["passwd"]
        confirm_passwd = request.form["c_passwd"]
        cursor = mysql.connection.cursor()
        if chkusers(usermail):
            if chkpasswd(userpasswd,confirm_passwd):
                flash("Account already exists! Please try to Login...")
                mysql.connection.commit()
                return redirect(url_for("login"))
            else:
                flash("ALERT! Account already exists with the entered email id, User entered Wrong details !!")
                return redirect(url_for("login"))
        else:
            if chkpasswd(userpasswd,confirm_passwd):
                session["user"] = username
                session["mail"] = usermail
                session["password"] = userpasswd
                cursor.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",(username,usermail,userpasswd))
                mysql.connection.commit()
                flash(f"Sign up successful {username}!")
                return redirect(url_for("user"))
            else:
                flash("ALERT! Invalid Signup details!!")
                return redirect(url_for("signup"))
        cursor.close()
    else:
        if "user" in session:
            name = session["user"]
            flash(f"{name}, you have already logged in !!")
            return redirect(url_for("user"))
    return render_template('login.html')

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        login_mail = request.form["l_mail"]
        login_passwd = request.form["l_passwd"]
        if chklogin(login_mail,login_passwd):
            flash("Login successful ! Welcome back....")
            return  redirect(url_for("user"))
        else:
            flash("User not found with the entered Account details ! please sign up first!")
            return redirect(url_for("signup"))
    return render_template('login2.html')



@app.route('/user', methods = ["POST", "GET"])
def user():
    flash("Login successful !!")
    flash(f"Hello !")
    return render_template('user.html')





@app.route('/logout')
def logout():
    flash("you have been logged out!", "info")
    '''deleting the sessions that was created at the time of login'''
    session.pop("user", None)
    session.pop("mail", None)
    return redirect(url_for("login"))


@app.route('/delete',methods=["POST","GET"])
def rem_ac():
    if request.method == "POST":
        delusrn = request.form["delname"]
        delusrm = request.form["delmail"]
        #users.query.filter_by(name=delusrn,email=delusrm).delete()
        #db.session.commit()
        username = session.get("uname")
        if username:
            session.pop("uname",None)
            '''if a session is found with this user (logged in after a long time)
            , it should delete them as well to avoid flash mssg bug.'''
        flash("Account deleted successfully !!")
        return redirect(url_for("login"))
    return render_template('delete_ac.html')




if __name__== "__main__":
    #db.create_all()
    app.run(debug = True)