from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from restaurant.databases import User

class registerForm(FlaskForm) :
    username = StringField('Username', validators = [DataRequired(), Length(min = 4, max = 25)])
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password')])
    submitButton = SubmitField('Sign up!')

    def validate_username(self, username) :
        user = User.query.filter_by(username = username.data).first()
        
        if user :
            raise ValidationError('Username taken.')

    def validate_email(self, email) :
        email = User.query.filter_by(email = email.data).first()
        
        if email :
            raise ValidationError('Email taken.')

class loginForm(FlaskForm) :
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    submitButton = SubmitField('Login')

class AccountUpdateForm(FlaskForm) :
    username = StringField('Username', validators = [DataRequired(), Length(min = 4, max = 25)])
    email = StringField('Email', validators= [DataRequired(), Email()])
    submitButton = SubmitField('Update')

    def validate_username(self, username) :
        if username.data != current_user.username :
            user = User.query.filter_by(username = username.data).first()
        
            if user :
                raise ValidationError('Username taken.')

    def validate_email(self, email) :
         if email.data != current_user.email :
            email = User.query.filter_by(email = email.data).first()
        
            if email :
                raise ValidationError('Email taken.')

class adjustMenu(FlaskForm) :
    Name = StringField('Name', validators= [DataRequired()])
    description = TextAreaField('description', validators= [DataRequired()])
    price = StringField('Price', validators= [DataRequired()])
    item_section = StringField('Section', validators= [DataRequired()])
    submit = SubmitField('Add')
