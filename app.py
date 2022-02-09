from flask import Flask, render_template, redirect, session, flash
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, User, connect_db
from forms import RegisterForm, LoginForm, CSRFProtectForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

connect_db(app)
db.create_all()


# LOG IN/REGISTER ROUTES

@app.get("/")
def homepage():
    """Redirect to register"""

    return redirect("/register")


@app.route("/register", methods=['GET', 'POST'])
def register():
    """Register user:
        if form validates, create new user, log in as said user, redirect to userinfo
        if does not validate, render registration form
    """

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        return redirect(f"/users/{new_user.usename}")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """LOGIN USER:
        if form validates, login user and redirect to userinfo
        if does not validate, render login form
    """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session["username"] = user.username
            return redirect(f'/users/{user.username}')

    return render_template("login.html", form=form)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "username" if present, but no errors if it wasn't
        session.pop("username", None)
        return redirect("/")
    else:
        return render_template("logout.html", form=form)


@app.get("/users/<username>")
def user_info(username):
    """Displays user's info if logged in
        redirects to home if not logged in as <username>
    """

    if session["username"] != username:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.filter_by(username=username).one_or_none()
        return render_template("userinfo.html", user=user)
