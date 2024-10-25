from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])

class ProblemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = SelectField('Subject', choices=[
        ('counting_and_probability', 'Counting & Probability'),
        ('number_theory', 'Number Theory'),
        ('algebra', 'Algebra'),
        ('geometry', 'Geometry'),
        ('trigonometry', 'Trigonometry'),
        ('exponent', 'Exponents & Powers')
    ])
    description = TextAreaField('Description')
    image = FileField('Image')
