from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256 as hashpass
from models import User

# Custom validator for Login Form
def invalid_credentials(form, field):
    """ User and password checker """

    username_entered = form.username.data
    password_entered = field.data

    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None or not hashpass.verify(password_entered, user_object.password):
        raise ValidationError('Username or Password is incorrect.')

# Registration Form
class RegistrationForm(FlaskForm):
    """ Registration Form """

    username = StringField('username_label',
                           validators=[InputRequired(message='Username required'),
                                       Length(min=4, max=25, message='Username must be between 4 and 25 characters.')])
    password = PasswordField('password_label',
                             validators=[InputRequired(message='Password required.'),
                                         Length(min=6, max=128, message='Password must be between 6 and 128 characters.')])
    confirm_pswd = PasswordField('confirm_pswd_label',  # Fixed typo from "cofirm_pswd_label"
                                 validators=[InputRequired(message='Confirmation password required.'),
                                             EqualTo('password', message="Passwords must match.")])

    submit_button = SubmitField("Create")

    # Custom validator for username uniqueness
    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError('Username already exists.')

# Login Form
class LoginForm(FlaskForm):
    """ Login Form """

    username = StringField('username_label',
                           validators=[InputRequired(message='Username required.')])
    password = PasswordField('password_label',
                             validators=[InputRequired(message='Password required.'),
                                         invalid_credentials])
    submit_button = SubmitField('Login')
