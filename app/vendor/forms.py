from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField

class VendorForm(FlaskForm):
    nama_vendor = StringField('Nama Vendor', validators=[DataRequired()])
    barang = StringField('Nama Barang', validators=[DataRequired()])
    jumlah = IntegerField('Jumlah barang')
    terjual = IntegerField('Jumlah terjual')
    sisa = IntegerField('Sisa barang')
    harga_satuan = IntegerField('Harga Satuan')
    harga_total = DecimalField(places=2)
    tanggal_drop = DateField('Tanggal Masuk')
    kategori = StringField('Kategori')
    satuan = StringField('Satuan')
    user = StringField('User')
    submit = SubmitField('Submit')