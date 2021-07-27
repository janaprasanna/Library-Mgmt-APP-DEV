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


@app.route('/adminview/<username>')
def viewadmin(username):
    cursor = mysql.connection.cursor()
    result = cursor.execute("select * from admin where admin_name=%s",({username}))
    if result:
        return render_template('adminview.html',object=result)
    else:
        flash("No such Admin found !!")





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

def chkadminlogin(id,passwd):
    cursor = mysql.connection.cursor()
    cursor.execute("select admin_id,admin_password from admin where admin_id=%s and admin_password=%s",(int(id),passwd))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False


def tokenstatus():
    maxtokens = 5
    temp_token = 1
    token_left = 0
    if token_left <= 5:
        token_left = maxtokens - temp_token
        temp_token = temp_token + 1


    if token_left <= 5:
        return True
    else:
        return False





@app.route('/home')
@app.route('/')
def home():
    return render_template('child.html')



@app.route('/adminsignup',methods=["GET","POST"])
def admin_signup():
    if request.method == "POST":
        a_id = adminid()
        a_name = request.form["a_name"]
        a_email = request.form["a_email"]
        a_password = request.form["a_password"]
        a_c_password = request.form["a_c_password"]
        cursor = mysql.connection.cursor()
        if chkadminlogin(a_id, a_password):
            flash("Admin already exists !! Try Login.")
            return redirect(url_for('admin_login'))
        else:
            if chkpasswd(a_password,a_c_password):
                cursor.execute("INSERT INTO admin(admin_id,admin_name,admin_email, admin_password) VALUES(%s,%s,%s, %s)",(int(a_id),a_name,a_email,a_password))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('admin_login'))
            else:
                flash("Mismatching details ! Re-enter correctly !")
                return redirect(url_for('admin_signup'))
    return render_template('admin_signup.html')

admin_login = False
@app.route('/admin',methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        a_id = request.form["a_id"]
        a_password = request.form["a_password"]
        if chkadminlogin(a_id, a_password):
            session["admin_id"] = a_id
            session["admin_password"] = a_password
            admin_login = True
            flash(" Welcome Admin !")
            return redirect(url_for("user"))
        else:
            flash("You are not a Admin for this software !! please sign up as a Admin first!")
            return redirect(url_for("admin_signup"))
    return render_template('admin.html')


def adminid():
    admin_id = randint(100000, 990000)
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
    session.pop("admin_id", None)
    session.pop("admin_password", None)

    admin_login = False
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


@app.route('/mydashboard')
def dashboard():
    return render_template('student_dashboard.html')

@app.route('/booksdashboard')
def admindashboard():
    return render_template('books_inventory.html')


@app.route('/borrowbooks',methods=["GET","POST"])
def borrow():
    return render_template('borrow_books.html')


def admin_book_chk(book_id,book_name):
    cursor = mysql.connection.cursor()
    cursor.execute("select BookID,BookName,TotalBookCount from adminbooks_inventory where BookID=%s AND BookName=%s",(book_id,book_name))
    result = cursor.fetchone()  #returns a tuple
    if result == None:
        result = 0
        return result
    else:
        result2 = result[2]
        return result2
''' 
    print(result[2])
    print(type(result[2]))
    print(type(result)) '''



@app.route('/addbooks',methods=["GET","POST"])
def add_books():
    if admin_login == True:
        if request.method == "POST":
            book_id = request.form["add_book_id"]
            book_name = request.form["add_book_name"]
            book_count = request.form["add_book_count"]
            oldbook_count = admin_book_chk(book_id,book_name)
            cursor = mysql.connection.cursor()
            BI = 0
            BR = 50
            if oldbook_count !=0 :
                flash("The Book already found in the Library ! upating the current books...")
                oldbook_count = oldbook_count + int(book_count)
                #the resultant oldbook_count is the new book count

                cursor.execute("UPDATE adminbooks_inventory SET  TotalBookCount=%s WHERE BookID=%s ",(oldbook_count,  int(book_id) ))
                mysql.connection.commit()
                cursor.close()
            else:
                flash("The Book is not found in the library...adding new books...")
                cursor.execute("INSERT INTO adminbooks_inventory(BookID, BookName, TotalBookCount, TotalBooksIssued , TotalBooksRegistered ) VALUES(%s,%s,%s,%s,%s)",( int(book_id), book_name, int(book_count), int(BI), int(BR) ))
                mysql.connection.commit()
                cursor.close()
    else:
        flash("You have not logged in as a Admin !")
        flash("cannot perform operation !! Error")
        return redirect(url_for('admin_login'))


    return  render_template('addbooks.html')


@app.route('/removebooks',methods=["GET","POST"])
def remove_books():
    if request.method == "POST":
        book_id = request.form["remove_book_id"]
        book_name = request.form["remove_book_name"]
        book_count = request.form["remove_book_count"]
        oldbook_count = admin_book_chk(book_id,book_name)
        cursor = mysql.connection.cursor()
        BI = 0
        BR = 50
        if oldbook_count !=0 :
            flash("The Book already found in the Library ! upating the current books...")
            if oldbook_count > int(book_count):
                if (oldbook_count - int(book_count)) <= 0:
                    flash("Book count is so higher than available books !")
                else:
                    oldbook_count = oldbook_count - int(book_count)
            else:
                if (int(book_count) - oldbook_count)<=0:
                    flash("Book count is so higher than available books !")
                else:
                    oldbook_count = int(book_count) - oldbook_count

            #the resultant oldbook_count is the new book count

            cursor.execute("UPDATE adminbooks_inventory SET TotalBookCount=%s WHERE BookID=%s ",(  oldbook_count, int(book_id) ))
            mysql.connection.commit()
            cursor.close()
        else:
            flash("The Book is not found in the library...Please add the Book first !!")

    return  render_template('removebooks.html')

@app.route('/issuebooks',methods=["GET","POST"])
def issue_approval():
    return render_template('issuebooks.html')

if __name__== "__main__":
    app.run(debug = True)