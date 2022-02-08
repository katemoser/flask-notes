from flask import Flask, jsonify, request, render_template, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, User, connect_db
from forms import RegisterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

connect_db(app)
db.create_all()




@app.get("/")
def homepage():
    """Redirect to register"""

    return redirect("/register")


@app.route("/register", methods=['GET', 'POST'])
def register():
    """Register user:
        if form validates, create new user, log in as said user, redirect to secret
        if does not validate, render registration form
    """

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        return redirect("/secret")
    else:
        return render_template("register.html", form = form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """LOGIN USER:
        if form validates, login user and redirect to secret
        if does not validate, render login form
    """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect('/secret')
            
    return render_template("login.html", form = form)




@app.get("/secret")
def secret():
    """Placeholder"""

    return render_template("secret.html")