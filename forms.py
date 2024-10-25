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
        ('algebra', 'Algebra'),
        ('counting_and_probability', 'Counting & Probability'),
        ('geometry', 'Geometry'),
        ('number_theory', 'Number Theory'),
        ('exponent', 'Exponents'),
        ('trigonometry', 'Trigonometry'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('biology', 'Biology')
    ])
    description = TextAreaField('Description')
    image = FileField('Image')

class CommentForm(FlaskForm):
    content = TextAreaField('Add a comment', validators=[DataRequired(), Length(min=1, max=1000)])
