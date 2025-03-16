from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(max=100)])
    project_type = SelectField('Project Type', choices=[
        ('road', 'Road Construction'),
        ('water', 'Water Pipeline'),
        ('drainage', 'Drainage System'),
        ('building', 'Building Construction'),
        ('bridge', 'Bridge Construction')
    ], validators=[DataRequired()])
    village_code = StringField('Village Code', validators=[DataRequired(), Length(max=10)])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed')
    ], validators=[DataRequired()])
    cost = FloatField('Cost (in INR)', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=200)])
    contractor = StringField('Contractor', validators=[DataRequired(), Length(max=100)])