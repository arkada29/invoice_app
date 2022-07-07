from flask import redirect, render_template, url_for, request, flash, current_app, jsonify
from app import db
from app.unit import bp
from app.models import Satuan, Category, DiskonKhusus
from app.unit.forms import SatuanForm, DiskonForm, CategoryForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import date, datetime

@bp.route('/unit_change')
@login_required
def unit_change():
    satuan = Satuan.query.all()
    category = Category.query.all()
    diskon = DiskonKhusus.query.filter(DiskonKhusus.id_diskon_khusus!=1).all()
    satuan_form = SatuanForm()
    diskon_form = DiskonForm()
    category_form = CategoryForm()
    return render_template('unit_Change.html',
                satuan=satuan,
                category=category,
                diskon=diskon,
                satuan_form = satuan_form,
                diskon_form=diskon_form,
                category_form=category_form
                    )

@bp.route('/unit_change/satuan/add', methods=['GET', 'POST'])
def satuan_add():
    satuan_add = Satuan.query.all()
    satuan_add_form = SatuanForm()

    if request.method == 'POST':

        satuan = Satuan(
                satuan=satuan_add_form.satuan.data,
                created_date=datetime.now()
        )
        db.session.add(satuan)
        try:
            db.session.commit()
            flash('New satuan added')
            return redirect(url_for('unit.satuan_add'))
        except:
            db.session.rollback()
            flash('Error to add new satuan')
            return redirect(url_for('unit.satuan_add'))
    return render_template('satuan_add.html',
                            satuan_add=satuan_add,
                            satuan_add_form=satuan_add_form
                            )


@bp.route('/unit_change/satuan/edit/<int:id>', methods=['GET', 'POST'])
def satuan_edit(id):
    satuan_edit = Satuan.query.get_or_404(id)
    satuan_edit_form = SatuanForm()

    if request.method == 'POST':

        satuan_edit.satuan = satuan_edit_form.satuan.data
        satuan_edit.updated_date = datetime.now()

        try:
            db.session.commit()
            flash('Satuan has been updated')
            return redirect(url_for('unit.satuan_edit', id=satuan_edit.id_satuan))
        except:
            db.session.rollback()
            flash('Failed to update satuan')
            return redirect(url_for('unit.satuan_edit', id=satuan_edit.id_satuan))      
    satuan_edit_form.satuan.data = satuan_edit.satuan  
    return render_template('satuan_edit.html',
                    satuan_edit_form=satuan_edit_form,
                    satuan_edit=satuan_edit)

@bp.route('/unit_change/diskon_khusus/add', methods=['GET', 'POST'])
def diskon_khusus_add():
    diskon_khusus = DiskonKhusus.query.all()
    diskon_khusus_form = DiskonForm()

    if request.method == 'POST':

        diskon = DiskonKhusus(
                kode_diskon = diskon_khusus_form.kode_diskon.data,
                nama_diskon = diskon_khusus_form.nama_diskon.data,
                besaran_diskon = diskon_khusus_form.besaran_diskon.data,
                created_date = datetime.now()
            )
        db.session.add(diskon)
        try:
            db.session.commit()
            flash('Added New Diskon khusus')
            return redirect(url_for('unit.diskon_khusus_add'))
        except:
            db.session.rollback()
            flash('Failed to add new Diskon')
            return redirect(url_for('unit.diskon_khusus_add'))  

    return render_template('diskon_add.html',
                    diskon_khusus=diskon_khusus,
                    diskon_khusus_form=diskon_khusus_form)

@bp.route('/unit_change/diskon_khusus/edit/<int:id>', methods=['GET', 'POST'])
def diskon_khusus_edit(id):
    diskon_khusus = DiskonKhusus.query.get_or_404(id)
    diskon_khusus_form = DiskonForm()

    if request.method == 'POST':

        diskon_khusus.kode_diskon = diskon_khusus_form.kode_diskon.data
        diskon_khusus.nama_diskon = diskon_khusus_form.nama_diskon.data
        diskon_khusus.besaran_diskon = diskon_khusus_form.besaran_diskon.data
        diskon_khusus.updated_date = datetime.now()

        try:
            db.session.commit()
            flash('Diskon khusus has been updated')
            return redirect(url_for('unit.diskon_khusus_edit', id=diskon_khusus.id_diskon_khusus))
        except:
            db.session.rollback()
            flash('Failed to update Diskon khusus')
            return redirect(url_for('unit.diskon_khusus_edit', id=diskon_khusus.id_diskon_khusus))  

    diskon_khusus_form.kode_diskon.data = diskon_khusus.kode_diskon
    diskon_khusus_form.nama_diskon.data = diskon_khusus.nama_diskon
    diskon_khusus_form.besaran_diskon.data = diskon_khusus.besaran_diskon
    return render_template('diskon_edit.html',
                    diskon_khusus=diskon_khusus,
                    diskon_khusus_form=diskon_khusus_form)

@bp.route('/unit_change/category/add', methods=['GET', 'POST'])
def category_add():
    category_add_form = CategoryForm()

    if request.method == 'POST':

        category = Category(
                    kode_kategori = category_add_form.kode_kategori.data,
                    nama_kategori = category_add_form.nama_kategori.data,
                    created_date = datetime.now()
                    )
        db.session.add(category)
        try:
            db.session.commit()
            flash('Added new category')
            return redirect(url_for('unit.category_add'))
        except:
            db.session.rollback()
            flash('Failed to add new category')
            return redirect(url_for('unit.category_edit'))  


    return render_template('category_add.html',
                    category_add_form=category_add_form)

@bp.route('/unit_change/category/edit/<int:id>', methods=['GET', 'POST'])
def category_edit(id):
    category_edit = Category.query.get_or_404(id)
    category_edit_form = CategoryForm()

    if request.method == 'POST':

        category_edit.kode_kategori = category_edit_form.kode_kategori.data
        category_edit.nama_kategori = category_edit_form.nama_kategori.data
        category_edit.updated_date = datetime.now()

        try:
            db.session.commit()
            flash('Category has been updated')
            return redirect(url_for('unit.category_edit', id=category_edit.id_kategori))
        except:
            db.session.rollback()
            flash('Failed to update category')
            return redirect(url_for('unit.category_edit', id=category_edit.id_kategori))  

    category_edit_form.nama_kategori.data = category_edit.nama_kategori
    category_edit_form.kode_kategori.data = category_edit.kode_kategori
    return render_template('category_edit.html',
                    category_edit=category_edit,
                    category_edit_form=category_edit_form)
