from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", 
                                     validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    
    password = PasswordField("Password", validators=[DataRequired()])

    remember = BooleanField("Remember me")
    
    submit = SubmitField("Sign In")


