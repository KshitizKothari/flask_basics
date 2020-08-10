from flask_wtf import FlaskForm, RecaptchaField
from wtforms import SubmitField,StringField, PasswordField, BooleanField
from wtforms.validators import EqualTo, DataRequired, Length, Email, ValidationError
from app.auth.models import User
from app import login_manager



def email_exists(form, field):
    email = User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError('email already exist')


class RegistrationForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired(), Length(3,25, message='Between 3 to 25 characters only')])
    email = StringField('Enter your Email', validators=[DataRequired(),Email(), email_exists])
    password = PasswordField('Password', validators=[DataRequired(), Length(5,message='Atleast 5 character long')])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message="Password doesn't match")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Enter your Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    stay_loggedin = BooleanField('Remember me')
    submit = SubmitField('Login')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class ChangePassword(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(5,message='Atleast 5 character long')])
    new_confirm_password = PasswordField('Confirm password', validators=[EqualTo('new_password', message="Password doesn't match")])
    update = SubmitField('Update')
