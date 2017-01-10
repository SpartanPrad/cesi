from flask import Flask, render_template, url_for, redirect, jsonify, request, g, session, flash,Blueprint
from datetime import datetime

from config import app,DATABASE,ACTIVITY_LOG,HOST,get_db


user_blueprint = Blueprint('user', __name__,)


# Username and password control
@user_blueprint.route('/login/control', methods = ['GET', 'POST'])
def control():
    if request.method == 'POST':
        if 'application/json' in request.mimetype:
            username = request.json.get('email')
            password = request.json.get('password')
        else:
            username = request.form['email']
            password = request.form['password']
        cur = get_db().cursor()
        cur.execute("select * from userinfo where username=?",(username,))
#if query returns an empty list
        if not cur.fetchall():
            session.clear()
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - Login fail. Username is not avaible.\n"%( datetime.now().ctime() ))
            return jsonify(status = "warning",
                           message = "Username is not  avaible ")
        else:
            cur.execute("select * from userinfo where username=?",(username,))
            if password == cur.fetchall()[0][1]:
                session['username'] = username
                session['logged_in'] = True
                cur.execute("select * from userinfo where username=?",(username,))
                session['usertype'] = cur.fetchall()[0][2]
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s logged in.\n"%( datetime.now().ctime(), session['username'] ))
                return jsonify(status = "success")
            else:
                session.clear()
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - Login fail. Invalid password.\n"%( datetime.now().ctime() ))
                return jsonify(status = "warning",
                               message = "Invalid password")

# Render login page
@user_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')

# Logout action
@user_blueprint.route('/logout', methods = ['GET', 'POST'])
def logout():
    add_log = open(ACTIVITY_LOG, "a")
    add_log.write("%s - %s logged out.\n"%( datetime.now().ctime(), session['username'] ))
    session.clear()
    return render_template('login.html')


# Delete user method for only admin type user
@user_blueprint.route('/delete/user')
def del_user():
    if session.get('logged_in'):
        if session['usertype'] == 0:
            cur = get_db().cursor()
            cur.execute("select username, type from userinfo")
            users = cur.fetchall();
            usernamelist =[str(element[0]) for element in users]
            usertypelist =[str(element[1]) for element in users]
            return jsonify(status = 'success',
                           names = usernamelist,
                           types = usertypelist)
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - Unauthorized user request for delete user event. Delete user event fail .\n"%( datetime.now().ctime() ))
            return jsonify(status = 'error')

@user_blueprint.route('/delete/user/<username>')
def del_user_handler(username):
    if session.get('logged_in'):
        if session['usertype'] == 0:
            if username != "admin":
                cur = get_db().cursor()
                cur.execute("delete from userinfo where username=?",[username])
                get_db().commit()
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s user deleted .\n"%( datetime.now().ctime(), username ))
                return jsonify(status = "success")
            else:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write("%s - %s  user request for delete admin user. Delete admin user event fail .\n"%( datetime.now().ctime(), session['username'] ))
                return jsonify(status = "error",
                               message= "Admin can't delete")
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user for request to delete a user. Delete event fail .\n"%( datetime.now().ctime(), session['username'] ))
            return jsonify(status = "error",
                           message = "Only Admin can delete a user")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for delete user event.\n"%( datetime.now().ctime()))
        return redirect(url_for('login'))

# Writes new user information to database
@user_blueprint.route('/add/user/handler', methods=['GET', 'POST'])
def adduserhandler():
    if session.get('logged_in'):
        if session['usertype'] == 0:
            username = request.form['username']
            password = request.form['password']
            confirmpassword = request.form['confirmpassword']

            if username == "" or password == "" or confirmpassword == "":
                return jsonify(status="null",
                               message="Please enter value")
            else:
                if request.form['usertype'] == "Admin":
                    usertype = 0
                elif request.form['usertype'] == "Standart User":
                    usertype = 1
                elif request.form['usertype'] == "Only Log":
                    usertype = 2
                elif request.form['usertype'] == "Read Only":
                    usertype = 3

                cur = get_db().cursor()
                cur.execute("select * from userinfo where username=?", (username,))
                if not cur.fetchall():
                    if password == confirmpassword:
                        cur.execute("insert into userinfo values(?, ?, ?)", (username, password, usertype,))
                        get_db().commit()
                        add_log = open(ACTIVITY_LOG, "a")
                        add_log.write("%s - New user added.\n" % (datetime.now().ctime()))
                        return jsonify(status="success",
                                       message="User added")
                    else:
                        add_log = open(ACTIVITY_LOG, "a")
                        add_log.write("%s - Passwords didn't match at add user event.\n" % (datetime.now().ctime()))
                        return jsonify(status="warning",
                                       message="Passwords didn't match")
                else:
                    add_log = open(ACTIVITY_LOG, "a")
                    add_log.write("%s - Username is avaible at add user event.\n" % (datetime.now().ctime()))
                    return jsonify(status="warning",
                                   message="Username is avaible. Please select different username")
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s is unauthorized user for request to add user event. Add user event fail .\n" % (
            datetime.now().ctime(), session['username']))
            return jsonify(status="error",
                           message="Only Admin can add a user")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write("%s - Illegal request for add user event.\n" % (datetime.now().ctime()))
        return jsonify(status="error",
                       message="First login please")

@user_blueprint.route('/change/password/<username>')
def changepassword(username):
    if session.get('logged_in'):
        if session['username'] == username:
            return jsonify(status="success")
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s user request to change %s 's password. Change password event fail\n" % (
            datetime.now().ctime(), session['username'], username))
            return jsonify(status="error",
                           message="You can only change own password.")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write(
            "%s - Illegal request for change %s 's password event.\n" % (datetime.now().ctime(), username))
        return redirect(url_for('login'))

@user_blueprint.route('/change/password/<username>/handler', methods=['POST'])
def changepasswordhandler(username):
    if session.get('logged_in'):
        if session['username'] == username:
            cur = get_db().cursor()
            cur.execute("select password from userinfo where username=?", (username,))
            ar = [str(r[0]) for r in cur.fetchall()]
            if request.form['old'] == ar[0]:
                if request.form['new'] == request.form['confirm']:
                    if request.form['new'] != "":
                        cur.execute("update userinfo set password=? where username=?",
                                    [request.form['new'], username])
                        get_db().commit()
                        add_log = open(ACTIVITY_LOG, "a")
                        add_log.write(
                            "%s - %s user change own password.\n" % (datetime.now().ctime(), session['username']))
                        return jsonify(status="success")
                    else:
                        return jsonify(status="null",
                                       message="Please enter valid value")
                else:
                    add_log = open(ACTIVITY_LOG, "a")
                    add_log.write(
                        "%s - Passwords didn't match for %s 's change password event. Change password event fail .\n" % (
                        datetime.now().ctime(), session['username']))
                    return jsonify(status="error", message="Passwords didn't match")
            else:
                add_log = open(ACTIVITY_LOG, "a")
                add_log.write(
                    "%s - Old password is wrong for %s 's change password event. Change password event fail .\n" % (
                    datetime.now().ctime(), session['username']))
                return jsonify(status="error", message="Old password is wrong")
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - %s user request to change %s 's password. Change password event fail\n" % (
            datetime.now().ctime(), session['username'], username))
            return jsonify(status="error", message="You can only change own password.")
    else:
        add_log = open(ACTIVITY_LOG, "a")
        add_log.write(
            "%s - Illegal request for change %s 's password event.\n" % (datetime.now().ctime(), username))
        return redirect(url_for('login'))

# Add user method for only admin type user
@user_blueprint.route('/add/user')
def add_user():
    if session.get('logged_in'):
        if session['usertype'] == 0:
            return jsonify(status='success')
        else:
            add_log = open(ACTIVITY_LOG, "a")
            add_log.write("%s - Unauthorized user request for add user event. Add user event fail .\n" % (
            datetime.now().ctime()))
            return jsonify(status='error')

@user_blueprint.route('/mobile', methods = ['POST'])
def get_otp():
    if request.method == 'POST':
        if 'application/json' in request.mimetype:
            mobile_number = request.json.get('mobile')
            otp = '1234'