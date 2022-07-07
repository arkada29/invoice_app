from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField

USER_LEVEL = ('Admin', 'Reguler')
ACTIVE = ('Active', 'Not-active')

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone')
    level = SelectField(label='Level', choices=[u for u in USER_LEVEL])
    password_hash = PasswordField('Password', validators=[DataRequired(), 
                    EqualTo('password_hash_match', message='Password Must Match!'),
                    Length(min=8, max=16)])
    password_hash_match = PasswordField('Confirm Password', validators=[DataRequired()])
    status = SelectField(label='Status', choices=[a for a in ACTIVE])
    profile_pic = FileField("Profile Picture")
    about = TextAreaField('About')
    submit = SubmitField('Submit')


