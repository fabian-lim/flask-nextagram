from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.user import User
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    # get data from the form
    username = request.form.get("username")
    password = request.form.get("password")
    
    # check if user exists in database
    user = User.get_or_none(User.username == username)

    if user:
        result = check_password_hash(user.password_hash, password)
        # if passwords match 
        if result:
            flash("Successfully logged in!", 'success')
            # save user id in browser session
            login_user(user) 
            return redirect(url_for('users.show', username=user.username))
        else: 
            flash("Password not matched", 'danger')
            return render_template("sessions/new.html")
    else:
        flash("Password not matched")
        return render_template("sessions/new.html")

@sessions_blueprint.route('/delete', methods=['POST'])
@login_required
def destroy():
    logout_user()
    flash("Logout successful", 'info')
    return redirect(url_for('sessions.new'))