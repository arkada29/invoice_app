from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField

class SatuanForm(FlaskForm):
    satuan = StringField('Satuan')
    submit = SubmitField('Submit')

class DiskonForm(FlaskForm):
    kode_diskon = StringField("Kode Diskon")
    nama_diskon = StringField('Nama Diskon')
    besaran_diskon = IntegerField('Besar Diskon')
    submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
    kode_kategori = StringField('Kode Kategori')
    nama_kategori = StringField('Nama Kategori')
    submit = SubmitField('Submit')


