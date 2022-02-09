from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Class for user
        contains information (username, password, email, first and last name)
        also includes authentication and registration
    """

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        nullable=False,
        primary_key=True,
        unique=True,
    )

    password = db.Column(
        db.String(100),
        nullable=False,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.String(30),
        nullable=False,
    )

    last_name = db.Column(
        db.String(30),
        nullable=False,
    )

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Class method to register new user
            returns instance of user class
        """

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

    @classmethod
    def authenticate(cls, username, password):
        """Class method to authenticate user
            check if password is correct
            if yes, return user else return false
        
        """

        user = cls.query.filter_by(username=username).one_or_none()
        if user and bcrypt.check_password_hash(user.password, password):
            print("*************************************FOUND USER")
            return user
        else:
            print("*************************************DID NOT FIND USER")

            return False
