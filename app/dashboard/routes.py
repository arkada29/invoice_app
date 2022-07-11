from flask import render_template, url_for, redirect
from app import db, create_app, vendor
from app.dashboard import bp
from app.models import User, Barang, Vendor, Penjualan, DetailPenjualan
from app.user.forms import UserForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from datetime import datetime
from sqlalchemy.sql.expression import func, between
from sqlalchemy import cast, Date, and_, UniqueConstraint
import datetime
import calendar

@bp.route('/dashboard')
@login_required
def dashboard():
    date_time = datetime.datetime.now()
    date_time_string = date_time.strftime("%A, %d-%m-%Y %H:%M:%S") 
    count_user = db.session.query(User.id).count()
    count_barang = db.session.query(Barang.id_barang).count()
    count_vendor = db.session.query(Vendor.id_vendor).count()
    count_penjualan = db.session.query(Penjualan.id_penjualan).count()
    
    barang_label = staticGraphChart()[0]
    barang_value = staticGraphChart()[1]

    user_label = staticGraphChart()[2]
    user_value = staticGraphChart()[3]

    vendor_label = staticGraphChart()[4]
    vendor_value = staticGraphChart()[5]

    jual_label = staticGraphChart()[6]
    jual_value = staticGraphChart()[7]

    user = db.session.query(func.Count(User.id), func.Date(User.join_date))\
        .group_by(func.Date(User.join_date))\
        .all()   

    vendor = db.session.query(Vendor.terjual, func.Date(Vendor.tanggal_taruh))\
            .group_by(func.Date(Vendor.tanggal_taruh))\
            .all()

    return render_template('dashboard.html',
                            count_user=count_user,
                            count_barang=count_barang,
                            count_vendor=count_vendor,
                            count_penjualan=count_penjualan,
                            date_time_string=date_time_string,
                            barang_label=barang_label,
                            barang_value=barang_value,
                            user_label=user_label,
                            user_value=user_value,
                            vendor_label=vendor_label,
                            vendor_value=vendor_value,
                            user=user,
                            vendor=vendor,
                            jual_label=jual_label,
                            jual_value=jual_value
                            )

@bp.route('/dashboard/admin/<int:id>')
@login_required
def dashboard_admin(id):
    form = UserForm()
    date_time = datetime.datetime.now()
    date_time_string = date_time.strftime("%A, %d-%m-%Y %H:%M:%S") 
    count_user = db.session.query(User.id).count()
    count_barang = db.session.query(Barang.id_barang).count()
    count_vendor = db.session.query(Vendor.id_vendor).count()
    count_penjualan = db.session.query(Penjualan.id_penjualan).count()
    user = User.query.get_or_404(id)

    return render_template('dashboard_admin.html', 
                            form=form,
                            user=user,
                            date_time_string=date_time_string,
                            count_user=count_user,
                            count_barang=count_barang,
                            count_vendor=count_vendor,
                            count_penjualan=count_penjualan
                            )

@bp.route('/dashboard/user/<int:id>')
@login_required
def dashboard_user(id):
    form = UserForm()
    date_time = datetime.datetime.now()
    date_time_string = date_time.strftime("%A, %d-%m-%Y %H:%M:%S") 
    count_user = db.session.query(User.id).count()
    count_barang = db.session.query(Barang.id_barang).count()
    count_vendor = db.session.query(Vendor.id_vendor).count()
    count_penjualan = db.session.query(Penjualan.id_penjualan).count()
    user = User.query.get_or_404(id)
    return render_template('dashboard_user.html',
                            form=form,
                            user=user,
                            date_time_string=date_time_string,
                            count_user=count_user,
                            count_barang=count_barang,
                            count_vendor=count_vendor,
                            count_penjualan=count_penjualan)

def staticGraphChart():

    barang_label = []
    barang_value = []
    user_join = []
    user_count = []
    vendor_add = []
    vendor_value = []
    jual_label = []
    jual_value = []

    current_date = datetime.datetime.now()
    current_date_string = current_date.strftime('%m/%d/%Y')
    now_object = datetime.datetime.strptime(current_date_string, '%m/%d/%Y')
    previous_date = current_date - datetime.timedelta(days=8)
    

    # barang = db.session.query(func.sum(Barang.stok), func.Date(Barang.created_date))\
    #         .filter(func.Date(Barang.created_date==current_date_string))\
    #         .filter(func.Date(Barang.created_date==previous_date))\
    #         .group_by(func.Date(Barang.created_date))\
    #         .all()

    # barang = db.session.query(func.sum(Penjualan.jumlah_penjualan), func.Date(Penjualan.tanggal_penjualan))\
    #                 .filter(func.Date(Penjualan.tanggal_penjualan==current_date_string))\
    #                 .filter(func.Date(Penjualan.tanggal_penjualan==previous_date))\
    #                 .group_by(func.Date(Penjualan.tanggal_penjualan))\
    #                 .order_by(Penjualan.id_penjualan.desc())\
    #                 .all()
    barang = db.session.query(func.sum(DetailPenjualan.jumlah_barang), func.Date(DetailPenjualan.created_date))\
        .filter(func.Date(DetailPenjualan.created_date).between(previous_date,current_date))\
        .group_by(func.Date(DetailPenjualan.created_date))\
        .order_by(func.Date(DetailPenjualan.created_date))\
        .all()

    user = db.session.query(func.Count(User.id), func.Date(User.join_date))\
        .group_by(func.Date(User.join_date))\
        .all()   

    # vendor = db.session.query(Vendor.terjual, func.Date(Vendor.tanggal_taruh))\
    #         .filter(func.Date(Vendor.tanggal_taruh==current_date_string))\
    #         .filter(func.Date(Vendor.tanggal_taruh==previous_date))\
    #         .group_by(func.Date(Vendor.tanggal_taruh))\
    #         .all()

    # penjualan = db.session.query(func.Count(Penjualan.kode_penjualan), func.Date(Penjualan.tanggal_penjualan))\
    #             .filter(func.Date(Penjualan.tanggal_penjualan==current_date_string))\
    #             .filter(func.Date(Penjualan.tanggal_penjualan==previous_date))\
    #             .group_by(func.Date(Penjualan.tanggal_penjualan))\
    #             .order_by(Penjualan.id_penjualan.desc())\
    #             .all()

    vendor = db.session.query(func.sum(Vendor.terjual), func.Date(Vendor.tanggal_taruh))\
            .filter(func.Date(Vendor.tanggal_taruh).between(previous_date, current_date_string))\
            .group_by(func.Date(Vendor.tanggal_taruh))\
            .all()

    penjualan = db.session.query(func.Count(Penjualan.kode_penjualan), func.Date(Penjualan.tanggal_penjualan))\
                .filter(func.Date(Penjualan.tanggal_penjualan).between(previous_date, current_date))\
                .group_by(func.Date(Penjualan.tanggal_penjualan))\
                .all()

    for value, label in barang:
        barang_value.append(value)
        barang_label.append(label)

    for join, count in user:
        user_join.append(join)
        user_count.append(count)

    for add, value in vendor:
        vendor_add.append(add)
        vendor_value.append(value)

    for value, label  in penjualan:
        jual_value.append(value)
        jual_label.append(label)

    return (barang_label, barang_value, user_join, user_count,
             vendor_add, vendor_value, jual_label, jual_value)