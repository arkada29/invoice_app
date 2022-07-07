from asyncio import streams
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# from enum import unique
# from app import db
# from datetime import datetime
# from flask import current_app
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# from hashlib import md5

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from sqlalchemy.sql.expression import func, between
from sqlalchemy import Integer, cast, Date, and_, UniqueConstraint, Float
import json
from sqlalchemy import event

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        "sqlite:///" + os.path.join(basedir, 'app',"sembako.db")

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    about_user = db.Column(db.Text(255), nullable=True)
    status = db.Column(db.String(50))
    level = db.Column(db.String(10))
    phone = db.Column(db.String(14), nullable=True)
    join_date = db.Column(db.DateTime, default=datetime.datetime.now())
    profile_pic = db.Column(db.String(500), nullable=True)
    last_login = db.Column(db.DateTime) 
    last_logout = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_date = db.Column(db.DateTime)

    #backref
    user_penjualan = db.relationship('Penjualan', backref='user_penjualan')
    user_vendor = db.relationship('Vendor', backref='user_vendor')

    @property
    def password(self):
        raise AttributeError('password is not readable !')

    @password.setter
    def password(self, user_pwd):
        self.password = generate_password_hash(user_pwd)

    def verify(self, user_pwd):
        return check_password_hash(self.password, user_pwd)

    def __repr__(self):
        return '<Name %r>' % self.name

class Category(db.Model):
    __tablename__ = 'kategori'
    id_kategori = db.Column(db.Integer, primary_key=True)
    kode_kategori = db.Column(db.String(10), nullable=False, unique=True)
    nama_kategori = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_date = db.Column(db.DateTime)

    #backref
    kategori_barang = db.relationship('Barang', backref='kategori_barang')
    kategori_vendor = db.relationship('Vendor', backref='kategori_vendor')

    def __repr__(self):
        return '<Name %r>' % self.category_name

class DiskonKhusus(db.Model):
    __tablename__ = 'diskon_khusus'
    id_diskon_khusus = db.Column(db.Integer, primary_key=True)
    kode_diskon = db.Column(db.String(10), nullable=False, unique=True)
    nama_diskon = db.Column(db.String(200))
    besaran_diskon = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_date = db.Column(db.DateTime)

    #backef
    diskon_detail_penjualan = db.relationship('DetailPenjualan', backref='diskon_detail_penjualan')

    def __repr__(self):
        return '<Name %r>'% self.name_diskon

class Barang(db.Model):
    __tablename__ = 'barang'
    id_barang = db.Column(db.Integer, primary_key=True)
    kode_barang = db.Column(db.String(10), nullable=False)
    nama_barang = db.Column(db.String(255), nullable=False)
    harga_jual = db.Column(db.Float(20, True, 2))
    harga_beli = db.Column(db.Float(20, True, 2))
    stok = db.Column(db.Integer)
    jumlah_grosir = db.Column(db.Integer)
    harga_grosir = db.Column(db.Float(20, True, 2))
    diskon = db.Column(db.Integer)
    status = db.Column(db.String(20))
    barang_pic = db.Column(db.String(500))
    tanggal_masuk = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_date = db.Column(db.DateTime)

    # foreign
    id_kategori = db.Column(db.Integer, db.ForeignKey('kategori.id_kategori'))
    id_satuan = db.Column(db.Integer, db.ForeignKey('satuan.id_satuan'))

    #constraint
    __table_args__ = (UniqueConstraint('kode_barang', 'nama_barang', 'id_satuan', name='uq_barang_kode_nama_satuan'),)

    #backref
    barang_detail_penjualan = db.relationship('DetailPenjualan', backref='barang_detail_penjualan')
    # barang_supplier = db.relationship('Supplier', backref='barang_supplier')

    def __repr__(self):
        return '<Name %r>' % self.nama_barang

@event.listens_for(db.session, "before_flush")
def reduce_stok_barang(*args):
    sess = args[0]
    for obj in sess.new:
        if not isinstance(obj, DetailPenjualan):
            continue

        barang = Barang.query.filter_by(kode_barang=obj.kode_barang).first()
        barang.stok = barang.stok - int(obj.jumlah_barang)
        db.session.add(barang)

class Satuan(db.Model):
    __tablename__ = 'satuan'
    id_satuan = db.Column(db.Integer, primary_key=True)
    satuan = db.Column(db.String(200), unique=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_date = db.Column(db.DateTime)

    #backref
    satuan_barang = db.relationship('Barang', backref='satuan_bareng')
    satuan_vendor = db.relationship('Vendor', backref='satuan_vendor')

    def __repr__(self):
        return '<Name %r>' % self.nama_barang

class Penjualan(db.Model):
    __tablename__ = 'penjualan'
    id_penjualan = db.Column(db.Integer, primary_key=True)
    kode_penjualan = db.Column(db.String(10), nullable=False, unique=True)
    tanggal_penjualan = db.Column(db.DateTime)
    jumlah_penjualan = db.Column(db.Integer)
    grand_total = db.Column(db.Float(20,True, 2))
    total_pembayaran = db.Column(db.Float(20, True, 2)) 
    total_kembalian = db.Column(db.Float(20, True, 2))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_date = db.Column(db.DateTime)

    #foreign
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))

    #backref
    penjualan_detail = db.relationship('DetailPenjualan', backref='penjualan_detail')

    def __repr__(self):
        return '<Name %r>' % self.kode_penjualan

class DetailPenjualan(db.Model):
    __tablename__ = 'detail_penjualan'
    id_detail_penjualan = db.Column(db.Integer, primary_key=True)
    no_urut = db.Column(db.Integer)
    jumlah_barang = db.Column(db.Integer)
    total_harga = db.Column(db.Float(20, True, 2))
    sub_total = db.Column(db.Integer)
    potongan = db.Column(db.Integer)
    ppn = db.Column(db.Integer)

    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_date = db.Column(db.DateTime)

    #foreign
    kode_barang = db.Column(db.Integer, db.ForeignKey('barang.kode_barang'))
    kode_penjualan = db.Column(db.Integer, db.ForeignKey('penjualan.kode_penjualan'))
    # id_penjualan = db.Column(db.Integer, db.ForeignKey('penjualan.id_penjualan'))
    kode_diskon = db.Column(db.Integer, db.ForeignKey('diskon_khusus.kode_diskon'))

    def __repr__(self):
        return '<Name %r>' % self.id_detail_penjualan

class Vendor(db.Model):
    __tablename__ = 'vendor'
    id_vendor = db.Column(db.Integer, primary_key=True)
    nama_vendor = db.Column(db.String(255))
    nama_barang = db.Column(db.String(255))
    jumlah = db.Column(db.Integer)
    terjual = db.Column(db.Integer)
    sisa = db.Column(db.Integer)
    harga_satuan = db.Column(db.Float(20, True, 2))
    harga_total = db.Column(db.Float(20, True, 2))
    tanggal_taruh = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    updated_date = db.Column(db.DateTime)

    #foreign
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    # id_barang = db.Column(db.Integer, db.ForeignKey('barang.id_barang'))
    id_kategori = db.Column(db.Integer, db.ForeignKey('kategori.id_kategori'))
    id_satuan = db.Column(db.Integer, db.ForeignKey('satuan.id_satuan'))

    def __repr__(self):
        return '<Name %r>' % self.nama_vendor

kontol = 'arka'

# anjing = db.session.query(User.level).filter_by(name='arka').first()
# print(anjing)

# user = User.query.get_or_404(1)
# print(user)

# category = db.session.query(Category.nama_kategori).all()
# for i in category:
    # print(i[0])

# barang = db.session.query(Barang.nama_barang.like('%'+str('ind')+'%')).all()
# barang = Barang.query.filter(Barang.nama_barang.like('%'+str('ind')+'%')).all()
# for b in barang:
#     print(b.nama_barang)


# if os.path.exists(os.path.join(basedir, 'app', 'sembako.db')):
#     print("yess")
# date_time = '2020/04/24'
# date_time_str = datetime.datetime.strptime(date_time,'%Y/%m/%d')
# # date_time_previous = date_time-datetime.timedelta(days=14)
# date_time_string = date_time_previous.strftime("%Y-%m-%d") 
import datetime
binatang = datetime.datetime.now()
testeddate = binatang.strftime('%m/%d/%Y')
dt_obj = datetime.datetime.strptime(testeddate,'%m/%d/%Y')
kontol = datetime.timedelta(days=7)
babi = dt_obj-kontol
dt_str = datetime.datetime.strftime(dt_obj,'%Y-%m-%d %H:%M:%S')

current_date = datetime.datetime.now()
current_date_string = current_date.strftime('%m/%d/%Y')
now_object = datetime.datetime.strptime(current_date_string, '%m/%d/%Y')
previous_date = datetime.timedelta(days=7)

dayBarang = db.session.query(func.count(Barang.id_barang), func.Date(Barang.tanggal_masuk))\
            .group_by(func.Date(Barang.tanggal_masuk)).all()

total_barang = db.session.query(func.sum(Barang.stok).label('Total barang')).all()

dateLatest = db.session.query(func.Date(Barang.tanggal_masuk))\
            .order_by(Barang.tanggal_masuk.desc()).limit(1).all()[0][0]

# barang = db.session.query(Barang.nama_barang, Barang.stok, Barang.created_date)\
#         .filter(func.Date(Barang.created_date==testeddate))\
#         .filter(func.Date(Barang.created_date==kontol))\
#         .group_by(func.Date(Barang.created_date), Barang.nama_barang)\
#         .all()

barang = db.session.query(func.sum(Barang.stok), func.Date(Barang.created_date))\
            .filter(func.Date(Barang.created_date==current_date_string))\
            .filter(func.Date(Barang.created_date==previous_date))\
            .group_by(func.Date(Barang.created_date)).all()

user = db.session.query(func.Count(User.id), func.Date(User.join_date))\
        .group_by(func.Date(User.join_date))\
        .all()   

vendor = db.session.query(Vendor.terjual, func.Date(Vendor.tanggal_taruh))\
        .group_by(func.Date(Vendor.tanggal_taruh))\
        .all()

penjualan = db.session.query(func.Count(Penjualan.kode_penjualan), func.Date(Penjualan.tanggal_penjualan))\
            .filter(func.Date(Penjualan.tanggal_penjualan==current_date_string))\
            .filter(func.Date(Penjualan.tanggal_penjualan==previous_date))\
            .group_by(func.Date(Penjualan.tanggal_penjualan))\
            .order_by(Penjualan.id_penjualan.desc())\
            .all()

barang_penjualan = db.session.query(DetailPenjualan.kode_barang,Barang.nama_barang\
                    , func.sum(Barang.stok), func.sum(DetailPenjualan.jumlah_barang))\
                    .join(DetailPenjualan, Barang.kode_barang==DetailPenjualan.kode_barang)\
                    .join(Penjualan, DetailPenjualan.kode_penjualan==DetailPenjualan.kode_penjualan)\
                    .filter(func.Date(Penjualan.tanggal_penjualan==current_date_string))\
                    .filter(func.Date(Penjualan.tanggal_penjualan==previous_date))\
                    .group_by(DetailPenjualan.kode_barang,Barang.nama_barang)\
                    .order_by(DetailPenjualan.kode_penjualan.desc())\
                    .all()

struk = db.session.query(Barang.nama_barang\
        , Barang.harga_jual\
        , Barang.diskon.cast(Float)/100\
        , DetailPenjualan.jumlah_barang\
        , DetailPenjualan.total_harga\
        , DetailPenjualan.sub_total\
        , DetailPenjualan.potongan\
        , DetailPenjualan.ppn\
        , Penjualan.jumlah_penjualan\
        , Penjualan.grand_total\
        , Penjualan.total_pembayaran\
        , Penjualan.total_kembalian\
        , DetailPenjualan.sub_total-DetailPenjualan.sub_total*DetailPenjualan.potongan\
        , User.name)\
        .join(DetailPenjualan, Barang.kode_barang == DetailPenjualan.kode_barang)\
        .join(Penjualan, DetailPenjualan.kode_penjualan==Penjualan.kode_penjualan)\
        .join(User, Penjualan.id_user==User.id)\
        .filter(DetailPenjualan.kode_penjualan=='TSB2').all()


# barang_terjual = db.session.query(func.Date(Penjualan.tanggal_penjualan), func.sum(Penjualan.jumlah_penjualan))\
#                 .group_by(func.Date(Penjualan.tanggal_penjualan))\
#                     .order_by(Penjualan.id_penjualan.desc())\
#                         .all()

# test1 = Barang.query\
#         .join(DetailPenjualan, Barang.kode_barang == DetailPenjualan.kode_barang)\
#         .join(Penjualan, DetailPenjualan.kode_penjualan==Penjualan.kode_penjualan)\
#         .filter(DetailPenjualan.kode_penjualan=='TSB2').all()

kode_barang = db.session.query(Barang.kode_barang).filter_by(nama_barang='iNDOMIE KARI AYAM').all()

kontol = Penjualan.query.filter(Penjualan.id_penjualan==6).all()

for k in kontol:
    print(k.id_penjualan)

tai = {}
# print(kode_barang)
# print(barang_penjualan)
# print(barang_terjual)
# for s in struk:
#     print(s)


# for u in test1:
#     print(u.nama_barang)
#     print(u.jumlah_barang)




# x = {
#   "name": "John",
#   "age": 30,
#   "married": True,
#   "divorced": False,
#   "children": ("Ann","Billy"),
#   "pets": None,
#   "cars": [
#     {"model": "BMW 230", "mpg": 27.5},
#     {"model": "Ford Edge", "mpg": 24.1}
#   ]
# }

# w =  '{ "name":"John", "age":30, "city":"New York"}'

# convert into JSON:
# y = json.loads(w)

# z = json.load(x)

# print(total_barang)
# print(binatang.date())
# print(type(binatang))
# print(dt_obj)
# print(type(dt_obj))
# print(dt_str)
# print(type(dt_str))
# print(babi)
# print(dayBarang)         
# print(date_time)   
# print(date_time_previous)
# # print(date_time_string)
# print(dateLatest)
# # for d in dateLatest:
# #     print(type(d))
# print(barang)
# def increment_invoice_number():
#     last_invoice = db.session.query(Penjualan.kode_penjualan).order_by(Penjualan.id_penjualan.desc()).first()
#     print(last_invoice)
#     if not last_invoice:
#          return 'TSB1'
#     invoice_no = last_invoice.kode_penjualan
#     invoice_int = int(invoice_no.split('TSB')[-1])
#     print(invoice_int)
#     new_invoice_int = invoice_int + 1
#     new_invoice_no = 'TSB' + str(new_invoice_int)
#     return new_invoice_no

# print(increment_invoice_number())

# invoice_int = int('MAG0001'.split('MAG')[-1])
# print(('MAG0001'.split('MAG')))
# print(invoice_int)

# print(user)

# print(vendor)

# print(type(y))
# print(x['cars'][0]['model'])

# a = [1,2]

# def breaker_list(name):
#     for n in name:
#         print (n[0])


# breaker_list(barang)

# for i,j in barang:
#     print(i,j)