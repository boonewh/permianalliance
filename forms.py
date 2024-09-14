from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.validators import ValidationError

def validate_email(form, field):
    if field.data.lower() == "kayleighbpsteamship@gmail.com":
        raise ValidationError("Thank you! We will get back to you soon.")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="Please enter your name.")])
    email = StringField("Email", validators=[DataRequired(message="Please enter your email address"), Email(), validate_email])
    subject = StringField("What is your current website? (ex: www.name.com or 'none' is also fine.)", validators=[DataRequired(message="Please enter a site or none.")])
    message = TextAreaField("Briefly describe what you need in your new website. 'Not sure' is a valid response.", validators=[DataRequired(message="Please enter a message. I don't know or I want to talk about it are good responses.")])
    submit = SubmitField("Send")
