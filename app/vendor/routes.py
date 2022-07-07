from flask import current_app, url_for, redirect, render_template, request, flash
from app import db
from app.models import Category, Satuan, Vendor, User
from app.vendor import bp
from app.vendor.forms import VendorForm
from datetime import date, datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

@bp.route('/vendor/vendor_add', methods=['GET', 'POST'])
@login_required
def vendor_add():
    vendor_add_form = VendorForm()
    category = Category.query.all()
    satuan = Satuan.query.all()
    user = current_user.name

    if request.method == 'POST':
        id_cat = db.session.query(Category.id_kategori).filter_by(nama_kategori=vendor_add_form.kategori.data)
        id_satuan = db.session.query(Satuan.id_satuan).filter_by(satuan=vendor_add_form.satuan.data)
        id_user = db.session.query(User.id).filter_by(name=request.form.get('user'))

        vendor = Vendor(
                    nama_vendor = vendor_add_form.nama_vendor.data,
                    nama_barang = vendor_add_form.barang.data,
                    jumlah = vendor_add_form.jumlah.data,
                    terjual = vendor_add_form.terjual.data,
                    sisa = request.form.get('sisa-barang'),
                    harga_satuan = vendor_add_form.harga_satuan.data,
                    harga_total = request.form.get('harga-total'),
                    tanggal_taruh = vendor_add_form.tanggal_drop.data,
                    created_date = datetime.now(),
                    id_user = id_user,
                    id_satuan = id_satuan,
                    id_kategori = id_cat
                    )
        
        try:
            db.session.add(vendor)
            db.session.commit()
            flash("Vendor added")
            return redirect(url_for('vendor.vendor_add'))
        except:
            db.session.rollback()
            flash('Failed to add vendor')
            return redirect(url_for('vendor.vendor_add'))
    return render_template('vendor_add.html', 
                            vendor_add_form=vendor_add_form,
                            category=category,
                            user=user,
                            satuan=satuan)

@bp.route('/vendor/vendor_edit/<int:id>', methods=['GET', 'POST'])
def vendor_edit(id):
    edit_vendor = Vendor.query.get_or_404(id)
    edit_vendor_form = VendorForm()
    category = Category.query.all()
    satuan = Satuan.query.all()

    if request.method == 'POST':
        id_cat = db.session.query(Category.id_kategori).filter_by(nama_kategori=edit_vendor_form.kategori.data)
        id_satuan = db.session.query(Satuan.id_satuan).filter_by(satuan=edit_vendor_form.satuan.data)
        id_user = db.session.query(User.id).filter_by(name=request.form.get('user'))

        edit_vendor.nama_vendor = edit_vendor_form.nama_vendor.data
        edit_vendor.nama_barang = edit_vendor_form.barang.data
        edit_vendor.jumlah = edit_vendor_form.jumlah.data
        edit_vendor.terjual = edit_vendor_form.terjual.data
        edit_vendor.sisa = request.form.get('sisa-barang')
        edit_vendor.harga_satuan = edit_vendor_form.harga_satuan.data
        edit_vendor.harga_total = request.form.get('harga-total')
        if edit_vendor_form.tanggal_drop.data:
        #     edit_vendor.tanggal_taruh = edit_vendor.tanggal_taruh
        # else:
            edit_vendor.tanggal_taruh = edit_vendor_form.tanggal_drop.data
        edit_vendor.updated_date = datetime.now()
        edit_vendor.id_user = id_user
        edit_vendor.id_satuan = id_satuan
        edit_vendor.id_kategori = id_cat

        try:
            db.session.commit()
            flash('Vendor updated')
            return redirect(url_for('vendor.vendor_list'))
        except:
            db.session.rollback()
            flash('Vendor updated')
            return redirect(url_for('vendor.vendor_list'))

    edit_vendor_form.nama_vendor.data = edit_vendor.nama_vendor
    edit_vendor_form.barang.data = edit_vendor.nama_barang
    edit_vendor_form.nama_vendor.data = edit_vendor.nama_vendor
    edit_vendor_form.jumlah.data = edit_vendor.jumlah
    edit_vendor_form.harga_satuan.data = edit_vendor.harga_satuan
    edit_vendor_form.terjual.data = edit_vendor.terjual
    edit_vendor_form.harga_satuan.data = edit_vendor.harga_satuan
    return render_template('vendor_edit.html',
                            edit_vendor_form=edit_vendor_form,
                            edit_vendor=edit_vendor,
                            category=category,
                            satuan=satuan
                            )

@bp.route('/vendor/vendor_detail/<int:id>')
@login_required
def vendor_detail(id):
    detail_vendor = Vendor.query.get_or_404(id)
    return render_template('vendor_detail.html',
                            detail_vendor=detail_vendor
                            )

@bp.route('/vendor/vendor_list')
@login_required
def vendor_list():
    page = request.args.get('page', 1, type=int)
    cp = Vendor.query.count()
    vendor = Vendor.query.order_by(Vendor.id_vendor.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('vendor.vendor_list', page=vendor.next_num)\
        if vendor.has_next else None
    prev_url = url_for('vendor.vendor_list', page=vendor.prev_num)\
        if vendor.has_prev else None
    return render_template('vendor_list.html',
                            vendor=vendor.items,
                            cp=cp,
                            page=page,
                            next_url=next_url,
                            prev_url=prev_url
                            )

@bp.route('/vendor/vendor_delete/<int:id>')
def vendor_delete(id):
    delete = Vendor.query.get_or_404(id)
    if current_user.level == 'Admin':
        db.session.delete(delete)
        db.session.commit()
        flash('Vendor deleted')
        return redirect(url_for('vendor.vendor_list'))
    else:
        db.session.rollback()
        flash('Vendor cannot be deleted you dont authorized')
        return redirect(url_for('vendor.vendor_list'))
