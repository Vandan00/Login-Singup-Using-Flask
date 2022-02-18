from flask_wtf import FlaskForm  
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField, PasswordField
from wtforms.validators import  DataRequired, InputRequired
  
class SignupForm(FlaskForm):  
   name = StringField("Name ", validators = [DataRequired("Please enter your name.")])   

   email = StringField("Email", validators = [DataRequired(message="Please enter your email address.")]) 

#    , granular_message=False, check_deliverability=False, allow_smtputf8=True, allow_empty_local=False

   password = PasswordField("Password", validators = [DataRequired("Please enter a Password.")])

   age = IntegerField("Age", validators = [InputRequired(message="Please enter your age. ")])  

   location = TextAreaField("Address", validators = [DataRequired("Please enter your name.")])  
     
   profession = SelectField('Your Profession', choices = ['Student', 'Professional','Teacher', 'Developer', 'Tester'])
  
   submit = SubmitField("Submit") 