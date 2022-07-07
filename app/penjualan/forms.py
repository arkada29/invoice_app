from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileField

class PenjualanForm(FlaskForm):
    kode_faktur = StringField('No. Faktur')
    nama_kasir = StringField('Nama')
    level_kasir = StringField('Level')
    tanggal_faktur = StringField('Tgl. Faktur')
    kode_barang = StringField("Kode Barang")
    jumlah_barang = IntegerField("Banyak")
    total_harga = DecimalField("Total Harga")
    jumlah_bayar = IntegerField("Jumlah Bayar")
    jumlah_kembalian = IntegerField("Kembalian")
    sub_total = DecimalField("Sub Total")
    potongan = DecimalField("Potongan")
    ppn = DecimalField("PPN")
    diskon_khusus = StringField("Diskon Ks")
    submit = SubmitField('Submit')
