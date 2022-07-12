from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField

STATUS = ('Ada', 'kosong')

class BarangForm(FlaskForm):
    kode_barang = StringField('Kode Barang', validators=[DataRequired()])
    nama_barang = StringField('Nama Barang', validators=[DataRequired()])
    stok = StringField('Stok')
    stok_akhir = StringField('Stok Akhir')
    discount = IntegerField('Discount')
    status = SelectField(label='Status', choices=[s for s in STATUS])
    harga_beli = DecimalField(places=4)
    harga_jual = DecimalField(places=4)
    kategori = StringField('Kategori')
    satuan  = StringField('Satuan')
    barang_pic = FileField('Foto Barang')
    tanggal_masuk = DateField('Tanggal Masuk', validators=[DataRequired()])
    jumlah_grosir = IntegerField('Jumlah Grosir Barang')
    total_grosir = DecimalField('Total Harga Grosir')
    submit = SubmitField('Submit')

class GrosirForm(FlaskForm):
    min_jumlah = StringField('Minimal Jumlah')
    harga_grosir = DecimalField(places=2)
    kode_barang = StringField('Kode Barang')
    kategori = StringField('Kategori')
    submit = SubmitField('Submit')

