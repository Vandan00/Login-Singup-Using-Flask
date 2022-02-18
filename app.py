from distutils.log import debug
from os import abort
from flask import Flask, flash, redirect, render_template, request
import flask
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import false
from forms import SignupForm   
from login_form import LoginForm
from datetime import datetime, date
import logging
# from error_handlers import not_found

from werkzeug.security import generate_password_hash, check_password_hash 


app = Flask(__name__)

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/Users'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.db'

app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login --
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    age = db.Column(db.Integer, nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

	# Create A String
    def __repr__(self):
        return '<Name %r>' % self.name



@app.route("/")
def index():
    # flash("Hello")
    app.logger.info('Info level log')
    # app.logger.warning('Warning level log')
    week_days = ['Monday', 'Tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    return render_template("index.html", Date = date.today(), day = week_days[date.today().weekday()])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    else:
        form = LoginForm()
        app.logger.info('Info level log')
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user:
                # Check the hash
                if check_password_hash(user.password_hash, form.password.data):
                    login_user(user)
                    flash("Logged In Successfully !! ")
                    app.logger.info(f"user '{user.username}' Logged In")
                    return redirect('/dashboard')
                else:
                    flash("Wrong Password - Try Again!")
            else:
                flash("User Doesn't Exist! Try Again...")


        return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    app.logger.info("User logged out")
    logout_user()
    flash("You Have Been Logged Out! ")
    return redirect('/login')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    # name = None
    app.logger.info("Accessing the signup page")
    if current_user.is_authenticated:
        return redirect("/dashboard")
    else:
        form = SignupForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user is None:
                # Hash the password!!!
                try:
                    hash_password =generate_password_hash(form.password.data)
                    user = Users(username=form.name.data, email = form.email.data, password_hash = hash_password, age = form.age.data, profession = form.profession.data, location = form.location.data)
                    db.session.add(user)
                    db.session.commit()
                    flash("User Added Successfully! Please Login now.")
                    return redirect("/login")
                except:
                    flash("Couldn't add user to the database")
            # name = form.name.data
            # form.name.data = ''
            form.name.data = ''
            form.email.data = ''
            form.password.data = ''
            form.age.data = ''
            form.profession.data = ''
            form.location.data = ''
            flash("User already exist !")
        return render_template("signup.html", 
            form=form)

@app.route("/dashboard", methods = ['POST', 'GET'])
@login_required
def dashboard():
    app.logger.info('Info level log')
    # app.logger.warning('Warning level log')
    users = Users.query.order_by(Users.date_added)
    # app.logger.info(users)
    return render_template("dashboard.html",users = users)

@app.route("/update/<int:id>", methods =['POST', 'GET'])
def update(id):
    form = SignupForm()
    breakpoint()
    user_to_update = Users.query.get_or_404(id)
    app.logger.info(f'Trying to update the user "{user_to_update.username}"')
    if request.method == 'POST':
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.age = request.form['age']
        user_to_update.profession = request.form['profession']
        user_to_update.location = request.form['location']
        breakpoint()
        try:
            db.session.commit()
            flash("User Info Updated!")
            app.logger.info(f'User info updated for user {user_to_update.username}')
            return redirect("/dashboard")
        except:
            app.logger.exception('Problem with updating the user')
            return "There was a problem updating the user !!"

    else:
        return render_template('update.html',form = form, user_to_update = user_to_update)

@app.route("/delete/<int:id>")
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully !")
        app.logger.info('User Deleted')
        return redirect("/dashboard")
    except:
        app.logger.exception('Problem with deleting the user')
        return ("There was a problem delete the user!")


# Error Handling

@app.errorhandler(404)
def not_found(e):
    app.logger.exception(f'Page not Found {e}, route: {request.url}')

    return render_template("404.html")

@app.errorhandler(500)
def not_found(e):
    app.logger.exception(f'Internal Server Error {e}, route: {request.url}')

    return render_template("500.html")


if __name__ == "__main__":
    app.run(debug=True)
