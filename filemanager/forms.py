from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, MultipleFileField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Login: ', validators=[DataRequired(), Length(min=3, max=32)],
                           id="username-input")
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=3, max=64)],
                             id="password-input")
    submit = SubmitField('Submit', id="submit")

class TransferInputs(FlaskForm):
    directory = StringField('Directory', id="directory-input")
    files = MultipleFileField('Files', validators=[DataRequired()], id="files-input")
    submit = SubmitField('Upload', id="upload")
    regexp = StringField('RegExp', id="regexp-input")
