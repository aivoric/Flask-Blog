from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    """Login form structure"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """Registration form structure and two validators which
    check if the username or email have already been taken."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Check if the username has already been taken.
         When you add any methods that match the pattern validate_<field_name>, 
         WTForms takes those as custom validators and invokes them in addition to 
         the stock validators."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please user a different username.')

    def validate_email(self, email):
        """Check if the email has already been taken."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
