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
    subject = StringField("Subject)", validators=[DataRequired(message="Please enter a subject.")])
    message = TextAreaField("Message.", validators=[DataRequired(message="Please enter a message.")])
    submit = SubmitField("Send")
