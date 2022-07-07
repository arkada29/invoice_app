from flask import redirect, render_template, url_for, request, flash, current_app, jsonify
from app import db
from app.penjualan import bp
from app.models import Barang, User, Satuan, Category, DiskonKhusus, Vendor, Penjualan, DetailPenjualan
from app.penjualan.forms import PenjualanForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import date, datetime
from sqlalchemy import Float
# from weasyprint import HTML
import io
import pandas as pd

@bp.route('/penjualan/penjualan_add', methods=['POST', 'GET'])
@login_required
def penjualan_add():
    date_time = datetime.now()
    add_form = PenjualanForm() 
    dk = DiskonKhusus.query.all()
    date_time_string = date_time.strftime("%A, %d-%m-%Y %H:%M:%S") 
    date_time_date = date_time.strftime("%d-%m-%Y") 
    invoice = increment_invoice_number()
    if request.method == 'POST':
        user = request.form['nama-kasir']
        diskon = request.form['diskon-khusus']
        user_id = db.session.query(User.id).filter_by(name=user).first()[0]
        # print(user)
        # print(user_id)
        kode_diskon = db.session.query(DiskonKhusus.kode_diskon).filter_by(nama_diskon=diskon).first()[0]
        # print(diskon)
        # print(kode_diskon)
        kode_barang = request.form.getlist('kode-barang-input')
        banyak = request.form.getlist('banyak-input')
        total_harga = request.form.getlist('total-harga-input')
        # print(total_harga)
        sub_total = request.form['sub-total']
        ppn = request.form['ppn']
        potongan = request.form['potongan']

        grand_total = add_form.total_harga.data
        jumlah_barang = add_form.jumlah_barang.data
        jumlah_bayar = add_form.jumlah_bayar.data
        kembalian = add_form.jumlah_kembalian.data

        penjualan = Penjualan(
                    id_user = user_id,
                    kode_penjualan = invoice,
                    tanggal_penjualan = datetime.now(),
                    jumlah_penjualan = jumlah_barang,
                    total_pembayaran = jumlah_bayar,
                    total_kembalian = kembalian,
                    grand_total = grand_total,
                    created_date = datetime.now()
        )
        

        for i, j in enumerate(total_harga):
            # print(i, j)
            detail_penjualan = DetailPenjualan(
                                no_urut = i,
                                jumlah_barang = banyak[i],
                                total_harga = j,
                                kode_barang = kode_barang[i],
                                sub_total = sub_total,
                                potongan = potongan,
                                ppn = ppn,
                                kode_penjualan = invoice,
                                kode_diskon = kode_diskon,
                                created_date = datetime.now()
                                )
            p = penjualan
            dp = detail_penjualan
            p.penjualan_detail.append(dp)
            db.session.add(p)
            db.session.flush()
        try:
            db.session.commit()
            return redirect(url_for('penjualan.penjualan_add'))
        except Exception as e:
            print(e)
            flash('Oops something wrong')
            return redirect(url_for('penjualan.penjualan_add'))

    return render_template('penjualan_add.html',
                        date_time_date=date_time_date,
                        date_time_string=date_time_string,
                        add_form=add_form,
                        dk=dk,
                        invoice=invoice
                    )

@bp.route('/penjualan/penjualan_edit/<int:id>', methods=['GET','POST'])
def penjualan_edit(id):
    penjualan = Penjualan.query.get_or_404(id)
    edit_form = PenjualanForm()
    if request.method == 'POST':
        id_user = User.query.filter_by(User.name==request.form['nama-user'])
        penjualan.id_user = id_user.id
        penjualan.kode_penjualan = request.form['kode-penjualan']
        penjualan.kode_penjualan = request.form['tanggal-faktur']
        penjualan.jumlah_penjualan = edit_form.jumlah_barang.data
        penjualan.total_pembayaran = edit_form.jumlah_bayar.data
        penjualan.total_kembalian = edit_form.jumlah_kembalian.data
        penjualan.updated_date = datetime.now()
        try:
            db.session.commit()
            flash('Invoice updated')
            return redirect(url_for('penjualan.penjualan_list'))
        except:
            db.session.rollback()
            flash('Sorry, invoice is not updated') 
            return redirect(url_for('penjualan.penjualan_edit', id=penjualan.id_penjualan))
    edit_form.jumlah_barang.data = penjualan.jumlah_penjualan
    edit_form.jumlah_bayar.data = penjualan.total_pembayaran
    edit_form.jumlah_kembalian.data = penjualan.total_kembalian
    return render_template('penjualan_edit.html',
                        edit_form=edit_form,
                        penjualan=penjualan)

@bp.route('/penjualan/penjualan_detail/<int:id>')
@login_required
def penjualan_detail(id):
    penjualan = Penjualan.query.get_or_404(id)
    detail_penjualan = DetailPenjualan.query\
                .filter_by(kode_penjualan=penjualan.kode_penjualan)\
                .all()
    return render_template('penjualan_detail.html',
                            detail_penjualan=detail_penjualan,
                            penjualan=penjualan
                            )

@bp.route('/penjualan/penjualan_list')
@login_required
def penjualan_list():
    page = request.args.get('page', 1, type=int)
    penjualan_list = Penjualan.query.order_by(Penjualan.id_penjualan.desc()).\
                    paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    cp = Penjualan.query.count()
    next_url = url_for('penjualan.penjualan_list', page=penjualan_list.next_num)\
        if penjualan_list.has_next else None
    prev_url = url_for('penjualan.penjualan_list', page=penjualan_list.prev_num)\
        if penjualan_list.has_prev else None
    return render_template('penjualan_list.html',
                            penjualan_list=penjualan_list.items,
                            next_url=next_url,
                            prev_url=prev_url,
                            cp=cp,
                            page=page
                                )

@bp.route('/penjualan/penjualan_delete/<int:id>')
@login_required
def penjualan_delete():
    if current_user.level == 'Admin':
        penjualan_to_delete = Penjualan.query.get_or_404(id)
        try:
            db.session.delete(penjualan_to_delete)
            db.session.commit()
            flash('Barang has been deleted')
            return redirect(url_for('penjualan.penjualan_list'))
        except:
            db.session.rollback()
            flash('Problem occured. cannot delete barang user')
            return redirect(url_for('penjualan.penjualan_list'))

@bp.route('/detail_penjualan/detail/<int:header_id>/<int:id>')
@login_required
def detail_penjualan_detail(header_id, id):
    penjualan = Penjualan.query.get_or_404(header_id)
    detail_penjualan = DetailPenjualan.query.get_or_404(id)
    return render_template('detail_penjualan_detail.html',
                            detail_penjualan=detail_penjualan, penjualan=penjualan)

@bp.route('/detail_penjualan/edit/<int:header_id>/<int:id>', methods=['GET','POST'])
def detail_penjualan_edit(header_id, id):
    edit_detail_form = PenjualanForm()
    penjualan = Penjualan.query.get_or_404(header_id)
    detail_penjualan = DetailPenjualan.query.get_or_404(id)
    if request.method == 'POST':
        diskon_name = request.form['diskon-khusus']
        kode_barang = db.session.query(Barang.kode_barang).filter_by(nama_barang=request.form['nama-barang'])
        if diskon_name == 'none':
            diskon_name = '--- CHOOSE DISKON ---'
        kode_diskon = db.session.query(DiskonKhusus.kode_diskon).filter_by(nama_diskon=diskon_name)
        # print(request.form.get('nama-barang'))
        # print(request.form['no-urut'])
        detail_penjualan.no_urut = request.form['no-urut']
        detail_penjualan.kode_penjualan = request.form['kode-penjualan']
        detail_penjualan.kode_barang = kode_barang
        detail_penjualan.jumlah_barang = edit_detail_form.jumlah_barang.data
        detail_penjualan.kode_diskon = kode_diskon
        detail_penjualan.total_harga = edit_detail_form.total_harga.data
        detail_penjualan.sub_total = edit_detail_form.sub_total.data
        detail_penjualan.ppn = edit_detail_form.ppn.data
        detail_penjualan.potongan = edit_detail_form.potongan.data
        print(edit_detail_form.potongan.data)
        detail_penjualan.updated_date = datetime.now()
        db.session.flush()
        try:
            db.session.commit()
            flash('Detail Invoice has been updated')
            return redirect(url_for('penjualan.detail_penjualan_edit', header_id=penjualan.id_penjualan,id=detail_penjualan.id_detail_penjualan))
        except Exception as e:
            db.session.rollback()
            print(e)
            flash('Failed to update Detail Invoice')
            return redirect(url_for('penjualan.detail_penjualan_edit', header_id=penjualan.id_penjualan,id=detail_penjualan.id_detail_penjualan))
    edit_detail_form.jumlah_barang.data = detail_penjualan.jumlah_barang
    edit_detail_form.total_harga.data = detail_penjualan.total_harga
    edit_detail_form.sub_total.data = detail_penjualan.sub_total
    edit_detail_form.potongan.data = detail_penjualan.potongan
    edit_detail_form.ppn.data = detail_penjualan.ppn
    return render_template('detail_penjualan_edit.html',
                            edit_detail_form=edit_detail_form,
                            detail_penjualan=detail_penjualan,
                            penjualan=penjualan)

@bp.route('/penjualan/detail_penjualan/delete/<int:id>')
@login_required
def detail_penjualan_delete(id):
    pass

@bp.route('/search_barang_penjualan', methods=['GET','POST'])
def search_barang_penjualan():
    if request.method == 'POST':

        search_word = request.get_json()

        if search_word == '':
            barang_collection = ()
        else:
            print(search_word)
            barang_collection = ()
            barang = Barang.query.filter(Barang.nama_barang.like('%'+str(search_word[0]['name_barang'])+'%')).all()
            for b in barang:
                barang_collection = list(barang_collection)
                row_dict = {column: str(getattr(b, column)) for column in b.__table__.c.keys()}
                barang_collection.append(row_dict)
                barang_collection = tuple(barang_collection)
            numrows = len(barang_collection)
    return jsonify({'htmlresponse': render_template('penjualanResponse.html',
                    search_word=search_word[0]['name_barang'],
                    barang_collection=barang_collection,
                    numrows=numrows
                    )})

@bp.route('/print_layout')
@login_required
def print_layout():
    kode = db.session.query(Penjualan.kode_penjualan).order_by(Penjualan.kode_penjualan.desc()).first()[0] or None
    struk = db.session.query(Barang.nama_barang\
        , Barang.harga_jual\
        , Barang.diskon.cast(Float)/100\
        , DetailPenjualan.no_urut\
        , DetailPenjualan.jumlah_barang\
        , DetailPenjualan.total_harga\
        , DetailPenjualan.sub_total\
        , DetailPenjualan.potongan\
        , DetailPenjualan.ppn\
        , Penjualan.jumlah_penjualan\
        , Penjualan.grand_total\
        , Penjualan.total_pembayaran\
        , Penjualan.total_kembalian\
        , Penjualan.kode_penjualan\
        , Penjualan.tanggal_penjualan\
        , DetailPenjualan.sub_total-DetailPenjualan.sub_total*DetailPenjualan.potongan\
        , User.name)\
        .join(DetailPenjualan, Barang.kode_barang == DetailPenjualan.kode_barang)\
        .join(Penjualan, DetailPenjualan.kode_penjualan==Penjualan.kode_penjualan)\
        .join(User, Penjualan.id_user==User.id)\
        .filter(DetailPenjualan.kode_penjualan==str(kode)).all()
    return render_template('print_layout.html', struk=struk, kode=kode)
    # return 

def increment_invoice_number():
    last_invoice = db.session.query(Penjualan.kode_penjualan).order_by(Penjualan.id_penjualan.desc()).first()
    print(last_invoice)
    if not last_invoice:
         return 'TSB1'
    invoice_no = last_invoice.kode_penjualan
    invoice_int = int(invoice_no.split('TSB')[-1])
    print(invoice_int)
    new_invoice_int = invoice_int + 1
    new_invoice_no = 'TSB' + str(new_invoice_int)
    return new_invoice_no