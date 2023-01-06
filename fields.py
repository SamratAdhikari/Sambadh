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
    if user_object is None:
        raise ValidationError('Username or Password is incorrect.')
    elif not hashpass.verify(password_entered, user_object.password):
        raise ValidationError('Password is incorrect.')


# Registration Form
class RegistrationForm(FlaskForm):
    """ Registration Form """

    username = StringField('username_label',
                           validators=[InputRequired(message='Username required'),
                                       Length(min=4, max=25, message='Username is invalid.')])
    password = PasswordField('password_label',
                             validators=[InputRequired(message='Password required.'),
                                         Length(min=4, max=25, message='Password is invalid.')])
    confirm_pswd = PasswordField('cofirm_pswd_label',
                                 validators=[InputRequired(message='Password required.'),
                                             EqualTo('password', message="Passwords must match.")])

    submit_button = SubmitField("Create")

    # Custom validator -- must have a specific name

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError('Username already exists.')


# login Form
class LoginForm(FlaskForm):
    """ Login Form """

    username = StringField('username_label',
                           validators=[InputRequired(message='Username required.')])
    password = PasswordField('password_label',
                             validators=[InputRequired(message='Password required.'),
                                         invalid_credentials])
    submit_button = SubmitField('Login')
