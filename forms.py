# from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError


class ContactForm(Form):
    name = TextField("Name",  [validators.Required()])
    email = TextField("Email",  [validators.Required(), validators.Email()])
    # subject = TextField("Subject")
    message = TextAreaField("Message",  [validators.Required()])
    submit = SubmitField("Send")
