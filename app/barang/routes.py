from app import db
from flask import current_app, render_template, request, redirect, url_for, flash, jsonify
from app.barang import bp
from app.barang.forms import BarangForm
from app.models import Barang, Satuan, Category
from app.user.routes import allowed_file
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
from config import Config
import uuid as uuid
import os

@bp.route('/barang/barang_add', methods=['GET','POST'])
@login_required
def barang_add():
    add_form = BarangForm()
    category = db.session.query(Category.nama_kategori).all()
    satuan = db.session.query(Satuan.satuan).all()
    if request.method == 'POST':
        kode_barang = Barang.query.filter_by(kode_barang=add_form.kode_barang.data).first()
        filename = request.files['barang_pic']
        id_kategori = db.session.query(Category.id_kategori).filter_by(nama_kategori=add_form.kategori.data)
        id_satuan = db.session.query(Satuan.id_satuan).filter_by(satuan=add_form.satuan.data)
        if not kode_barang:

            if filename and allowed_file(filename.filename):
                add_form.barang_pic = filename
                image = Image.open(add_form.barang_pic)
                image = image.resize((500,700), Image.ANTIALIAS)

                pic_filename = secure_filename(add_form.barang_pic.filename)
                pic_name = str(uuid.uuid1()) + "_" + pic_filename

                add_form.barang_pic = pic_name

                barang = Barang(
                        kode_barang=add_form.kode_barang.data,
                        nama_barang=add_form.nama_barang.data,
                        stok=add_form.stok.data,
                        diskon=add_form.discount.data,
                        status=add_form.status.data,
                        harga_jual=add_form.harga_jual.data,
                        harga_beli=add_form.harga_beli.data,
                        id_kategori=id_kategori,
                        id_satuan=id_satuan,
                        barang_pic = add_form.barang_pic,
                        tanggal_masuk = add_form.tanggal_masuk.data,
                        jumlah_grosir = add_form.jumlah_grosir.data,
                        harga_grosir = add_form.total_grosir.data,
                        created_date=datetime.now()
                        )
                # try:
                db.session.add(barang)
                db.session.commit()
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name), optimize=True)
                flash('Barang is successfully added')
                return redirect(url_for('barang.barang_add'))
                # except:
                #     db.session.rollback()
                #     flash('Barang is failed to add')
                #     return redirect(url_for('barang.barang_add'))
            else:
                barang = Barang(
                        kode_barang=add_form.kode_barang.data,
                        nama_barang=add_form.nama_barang.data,
                        stok=add_form.stok.data,
                        stok_akhir=add_form.stok.data,
                        diskon=add_form.discount.data,
                        status=add_form.status.data,
                        harga_jual=add_form.harga_jual.data,
                        harga_beli=add_form.harga_beli.data,
                        id_kategori=id_kategori,
                        id_satuan=id_satuan,
                        tanggal_masuk = add_form.tanggal_masuk.data,
                        jumlah_grosir = add_form.jumlah_grosir.data,
                        harga_grosir = add_form.total_grosir.data,
                        created_date=datetime.now()
                        )                
                # try:
                db.session.add(barang)
                db.session.commit()
                flash('Barang is successfully added')
                return redirect(url_for('barang.barang_add'))
                # except:    
        else:    
            db.session.rollback()
            flash('Barang is failed to add, kode barang is exist')
            return redirect(url_for('barang.barang_add'))
            # except:
            # flash('Sorry, cannot add barang')
            # db.session.rollback()
            # flash('Barang is failed to add')
            # return redirect(url_for('barang.barang_add'))
    add_form.kode_barang.data = ""
    add_form.nama_barang.data = ""
    add_form.stok.data = 0
    add_form.discount.data = 0
    add_form.status.data = ""
    add_form.harga_jual.data = 0
    add_form.harga_beli.data = 0
    add_form.kategori.data = ""
    add_form.satuan.data = ""
    add_form.jumlah_grosir.data = 0
    add_form.total_grosir.data = 0
    return render_template('barang_add.html', 
                        add_form=add_form,
                        category=category,
                        satuan=satuan
                        )

@bp.route('/barang/barang_edit/<int:id>', methods=['GET','POST'])
def barang_edit(id):
    update_barang = Barang.query.get_or_404(id)
    edit_barang_form = BarangForm()
    category = db.session.query(Category.nama_kategori).all()
    satuan = db.session.query(Satuan.satuan).all()
    if update_barang.barang_pic:
        del_img = os.path.join(current_app.config['UPLOAD_FOLDER'], update_barang.barang_pic)

    if request.method == 'POST':
        id_kategori = db.session.query(Category.id_kategori).filter_by(nama_kategori=request.form.get('kategori-barang'))
        id_satuan = db.session.query(Satuan.id_satuan).filter_by(satuan=edit_barang_form.satuan.data)

        update_barang.kode_barang = request.form.get('kode-barang')
        update_barang.nama_barang = request.form.get('nama-barang')
        update_barang.stok = edit_barang_form.stok.data
        update_barang.stok_akhir = edit_barang_form.stok_akhir.data 
        update_barang.diskon = edit_barang_form.discount.data
        update_barang.harga_jual = edit_barang_form.harga_jual.data
        update_barang.harga_beli = edit_barang_form.harga_beli.data
        update_barang.status = edit_barang_form.status.data
        update_barang.id_kategori = id_kategori
        update_barang.id_satuan = id_satuan
        update_barang.jumlah_grosir = edit_barang_form.jumlah_grosir.data
        update_barang.harga_grosir = edit_barang_form.total_grosir.data
        if edit_barang_form.tanggal_masuk.data:
            update_barang.tanggal_masuk = edit_barang_form.tanggal_masuk.data
        #  if edit_vendor_form.tanggal_drop.data:
        # #     edit_vendor.tanggal_taruh = edit_vendor.tanggal_taruh
        # # else:
        #     edit_vendor.tanggal_taruh = edit_vendor_form.tanggal_drop.data
        update_barang.updated_date=datetime.now()
        filename = request.files['barang_pic']
        print(edit_barang_form.tanggal_masuk.data)

        if filename and allowed_file(filename.filename):
            
            update_barang.barang_pic = filename

            image = Image.open(update_barang.barang_pic)
            image = image.resize((500,700), Image.ANTIALIAS)

            barang_filename = secure_filename(update_barang.barang_pic.filename)
            barang_name = str(uuid.uuid1()) + "_" + barang_filename

            edit_barang_form.barang_pic.data = barang_name
            update_barang.barang_pic = barang_name

            try:
                db.session.commit()
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], barang_name), optimize=True)
                if del_img:
                    os.remove(del_img)
                flash('Barang detail is updated')
                return redirect(url_for('barang.barang_list'))
            except:
                db.session.rollback()
                flash('Barang failed to updated')
                return redirect(url_for('barang.barang_list'))
        else:
            try:
                db.session.commit()
                flash('Barang detail is updated')
                return redirect(url_for('barang.barang_list'))
            except:
                db.session.rollback()
                flash('Barang failed to updated')
                return redirect(url_for('barang.barang_list'))

    edit_barang_form.kode_barang.data = update_barang.kode_barang
    edit_barang_form.nama_barang.data = update_barang.nama_barang
    edit_barang_form.stok.data = update_barang.stok
    edit_barang_form.stok_akhir.data = update_barang.stok_akhir
    edit_barang_form.discount.data = update_barang.diskon
    edit_barang_form.status.data = update_barang.status
    edit_barang_form.harga_jual.data = update_barang.harga_jual
    edit_barang_form.harga_beli.data = update_barang.harga_beli
    edit_barang_form.jumlah_grosir.data = update_barang.jumlah_grosir
    edit_barang_form.total_grosir.data = update_barang.harga_grosir
    return render_template('barang_edit.html',
                        edit_barang_form=edit_barang_form,
                        update_barang=update_barang,
                        category=category,
                        satuan=satuan
                        )

@bp.route('/barang/barang_list')
@login_required
def barang_list():
    add_form = BarangForm()
    page = request.args.get('page', 1, type=int)
    # category = db.session.query(Category.nama_kategori).all()
    barang = Barang.query.order_by(Barang.id_barang.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    cp = Barang.query.count()
    next_url = url_for('barang.barang_list', page=barang.next_num)\
            if barang.has_next else None
    prev_url = url_for('barang.barang_list', page=barang.prev_num)\
            if barang.has_prev else None
    count_barang = db.session.query(Barang.id_barang).count()
    return render_template('barang_list.html', 
                        add_form=add_form,
                        # category=category,
                        barang=barang.items,
                        count_barang=count_barang,
                        next_url=next_url,
                        prev_url=prev_url,
                        page=page,
                        cp=cp
                        )

@bp.route('/barang/barang_detail/<int:id>')
@login_required
def barang_detail(id):
    barang_detail = Barang.query.get_or_404(id)
    return render_template('barang_detail.html', 
                            barang_detail=barang_detail)

@bp.route('/barang/delete/<int:id>')
@login_required
def barang_delete(id):
    if current_user.level == 'Admin':
        barang_to_delete = Barang.query.get_or_404(id)
        try:
            db.session.delete(barang_to_delete)
            db.session.commit()
            flash('Barang has been deleted')
            return redirect(url_for('barang.barang_list'))
        except:
            db.session.rollback()
            flash('Problem occured. cannot delete barang user')
            return redirect(url_for('barang.barang_list'))

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.',1)[1].lower() in current_app.config['ALLOWED_EXTENSION']