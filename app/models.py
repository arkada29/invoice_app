from email.policy import default
from sqlalchemy import UniqueConstraint
from app import db
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from sqlalchemy import event

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    about_user = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50))
    level = db.Column(db.String(10))
    phone = db.Column(db.String(14), nullable=True)
    join_date = db.Column(db.DateTime, default=datetime.now())
    profile_pic = db.Column(db.String(500), nullable=True)
    last_login = db.Column(db.DateTime) 
    last_logout = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=datetime.now())
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
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
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
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_date = db.Column(db.DateTime)

    #backef
    diskon_detail_penjualan = db.relationship('DetailPenjualan', backref='diskon_detail_penjualan')

    def __repr__(self):
        return '<Name %r>'% self.name_diskon

class Barang(db.Model):
    __tablename__ = 'barang'
    id_barang = db.Column(db.Integer, primary_key=True)
    kode_barang = db.Column(db.String(10), nullable=False, unique=True)
    nama_barang = db.Column(db.String(255), nullable=False)
    harga_jual = db.Column(db.Float(20, True, 2))
    harga_beli = db.Column(db.Float(20, True, 2))
    stok = db.Column(db.Integer)
    stok_akhir = db.Column(db.Integer)
    jumlah_grosir = db.Column(db.Integer)
    harga_grosir = db.Column(db.Float(20, True, 2))
    diskon = db.Column(db.Integer)
    status = db.Column(db.String(20))
    barang_pic = db.Column(db.String(500))
    tanggal_masuk = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
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
        barang.stok_akhir = barang.stok_akhir - int(obj.jumlah_barang)
        db.session.add(barang)

class Satuan(db.Model):
    __tablename__ = 'satuan'
    id_satuan = db.Column(db.Integer, primary_key=True)
    satuan = db.Column(db.String(200), unique=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
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
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
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
    sub_total = db.Column(db.Float(20, True, 2))
    potongan = db.Column(db.Float(20, True, 2))
    ppn = db.Column(db.Float(20, True, 2))

    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_date = db.Column(db.DateTime)

    #foreign
    kode_barang = db.Column(db.String(10), db.ForeignKey('barang.kode_barang'))
    kode_penjualan = db.Column(db.String(10), db.ForeignKey('penjualan.kode_penjualan'))
    # id_penjualan = db.Column(db.Integer, db.ForeignKey('penjualan.id_penjualan'))
    kode_diskon = db.Column(db.String(10), db.ForeignKey('diskon_khusus.kode_diskon'))

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
    harga_satuan = db.Column(db.Float(20, True, 2), default=0)
    harga_total = db.Column(db.Float(20, True, 2))
    tanggal_taruh = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_date = db.Column(db.DateTime)

    #foreign
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    # id_barang = db.Column(db.Integer, db.ForeignKey('barang.id_barang'))
    id_kategori = db.Column(db.Integer, db.ForeignKey('kategori.id_kategori'))
    id_satuan = db.Column(db.Integer, db.ForeignKey('satuan.id_satuan'))

    def __repr__(self):
        return '<Name %r>' % self.nama_vendor

class Grosir(db.Model):
    __tablename__ = 'grosir'
    id_grosir = db.Column(db.Integer, primary_key=True)   
    min_jumlah = db.Column(db.Integer)
    harga_grosir = db.Column(db.Float(20, True, 2))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_date = db.Column(db.DateTime)

    #foreign key
    # id_barang = db.Column(db.Integer, db.ForeignKey('barang.id_barang'))
    # id_kategori = db.Column(db.Integer, db.ForeignKey('kategori.id_kategori'))

    def __repr__(self):
        return '<Name %r>' % self.nama_barang