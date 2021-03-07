"""All the forms used on the site."""
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    """Login form structure"""
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

class RegistrationForm(FlaskForm):
    """Registration form structure and two validators which
    check if the username or email have already been taken."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField(
        _l('Email'), validators=[DataRequired(), Email()]
    )
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        """Check if the username has already been taken.
         When you add any methods that match the pattern validate_<field_name>, 
         WTForms takes those as custom validators and invokes them in addition to 
         the stock validators."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please user a different username.'))

    def validate_email(self, email):
        """Check if the email has already been taken."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address.'))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
