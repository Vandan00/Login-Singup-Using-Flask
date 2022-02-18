from flask_wtf import FlaskForm  
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import  DataRequired
  
class LoginForm(FlaskForm):  
 
   email = StringField("Email", validators = [DataRequired(message="Please enter your email address.")]) 
   password = PasswordField("Password", validators = [DataRequired("Please enter a Password.")])
  
   submit = SubmitField("Submit") 