from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

def validate_email(form, field):
    if field.data.lower() == "kayleighbpsteamship@gmail.com":
        raise ValidationError("Your message has been rejected")

def validate_subject(form, field):
    blocked_words = ["write", "writing", "wrote"]
    if any(word in field.data.lower() for word in blocked_words):
        raise ValidationError("Your message has been marked as spam. If this is a mistake, please email us directly at boonewh@pathsixdesigns.com")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(message="Please enter your name.")])
    email = StringField("Email", validators=[DataRequired(message="Please enter your email address"), Email(), validate_email])
    subject = StringField("Subject", validators=[DataRequired(message="Please enter a subject."), validate_subject])
    message = TextAreaField("Message", validators=[DataRequired(message="Please enter a message.")])
    recaptcha = RecaptchaField() 
    submit = SubmitField("Send")
