from flask import render_template, redirect, url_for, current_app, flash, request, session
from app import db, create_app, login_manager
from app.user import bp
from app.user.forms import LoginForm, UserForm
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from urllib.parse import urlparse, urljoin
from PIL import Image
import os
import uuid as uuid 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@bp.route('/', methods=['GET','POST'])
@bp.route('/login', methods=['GET','POST'])
def login():
    # session.permanent = True
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter_by(name=form.username.data).first()
        level = db.session.query(User.level).filter_by(name=form.username.data).first()
        next = request.args.get('next')
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                user.last_login = datetime.now()
                # return redirect(url_for('dashboard.dashboard'))
                if is_safe_url(next):
                    db.session.commit()
                    return redirect(next or url_for('dashboard.dashboard'))
                else:
                    db.session.rollback()
                    flash('sorry something is wrong')
                    return redirect('/')
            else:
                flash('Wrong password try again')
                return redirect('/')
    form.username.data = ""
    form.password.data = ""
    return render_template('login.html', form=form)

@bp.route('/user/user_add', methods=['POST', 'GET'])
def user_add():
    edit_form = UserForm() 
    if edit_form.validate_on_submit():
        user = User.query.filter_by(name=edit_form.name.data).first()
        try:
            # if not user:
            if user:
                flash("username exist try another")
            else:
                hashed_pw = generate_password_hash(edit_form.password_hash.data, "sha256")
                user = User(
                            name=edit_form.name.data,
                            phone=edit_form.phone.data,
                            level=edit_form.level.data,
                            status=edit_form.status.data,
                            join_date = datetime.now(),
                            created_date = datetime.now(),
                            password_hash=hashed_pw
                        ) 
                db.session.add(user)
                db.session.commit()
                edit_form.name.data = ''
                edit_form.phone.data = ''
                edit_form.level.data = ''
                edit_form.status.data = ''
                flash('user added successfully')
                return redirect(url_for('user.user_add'))
        except:
            db.session.rollback()
            flash('user failed to added')
            return redirect(url_for('user.user_add'))

    return render_template('user_add.html', edit_form=edit_form)

@bp.route('/user/edit/<int:id>', methods=['GET','POST'])
@login_required
def user_edit(id):
    # id = current_user.id
    updated = User.query.get_or_404(id)
    edit_form = UserForm() 

    if updated.profile_pic:
        del_img = os.path.join(current_app.config['UPLOAD_FOLDER'], updated.profile_pic)

    if request.method == 'POST':
        updated.name = edit_form.name.data
        updated.level = edit_form.level.data
        updated.phone = edit_form.phone.data
        updated.status = edit_form.status.data
        updated.about_user = edit_form.about.data
        updated.updated_date = datetime.now()
        filename = request.files['profile_pic']

        if filename and allowed_file(filename.filename):
            updated.profile_pic = filename
            image = Image.open(updated.profile_pic)
            image = image.resize((150,150), Image.ANTIALIAS)

            pic_filename = secure_filename(updated.profile_pic.filename)
            pic_name = str(uuid.uuid1()) + "_"  + pic_filename

            edit_form.profile_pic.data = pic_name
            updated.profile_pic = pic_name

            try:
                db.session.commit()
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name), optimize=True)
                if del_img:
                    os.remove(del_img)
                flash('User profile updated !')
                if current_user.level == 'Admin':
                    return redirect(url_for('dashboard.dashboard_admin', id=current_user.id))
                else:
                    return redirect(url_for('dashboard.dashboard_user', id=current_user.id))
            except:
                db.session.rollback()
                flash('An error has occured, please try again')
                return redirect(url_for('user.user_edit', id=current_user.id))
                # return redirect(url_for('dashboard.dashboard_admin'))
        else:
            try:
                db.session.commit()
                flash('User profile updated !')
                if current_user.level == 'Admin':
                    return redirect(url_for('dashboard.dashboard_admin', id=current_user.id))
                else:
                    return redirect(url_for('dashboard.dashboard_user', id=current_user.id))
                # return redirect(url_for('dashboard.dashboard'))
            except:
                db.session.rollback()
                flash('An error has occured, please try again')
                return redirect(url_for('user.user_edit', id=current_user.id))
                # return redirect(url_for('dashboard.dashboard_admin'))    
    # if updated.id == current_user.id:
    edit_form.name.data = updated.name
    edit_form.level.data = updated.level
    edit_form.status.data = updated.status
    edit_form.phone.data = updated.phone
    edit_form.about.data = updated.about_user
    return render_template('user_edit.html', 
                            edit_form=edit_form,
                            updated=updated
                            )

@bp.route('/user/password_change/<int:id>', methods=['GET', 'POST'])
@login_required
def user_change_password(id):
    edit_form = UserForm() 
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password_hash'], 'sha256')
        user.password_hash = hashed_pw
        try:
            db.session.commit()
            flash('Password has been changed')
            return redirect(url_for('user.user_change_password', id=user.id))
        except:
            db.session.rollback()
            flash('Error occured, failed to change password')
            return redirect(url_for('user.user_change_password', id=user.id))
    return render_template('user_change_password.html', edit_form=edit_form)

@bp.route('/user/user_list')
@login_required
def user_list():
    edit_form = UserForm() 
    count_data = db.session.query(User.id).count()
    page=request.args.get('page', 1, type=int)
    user = User.query.order_by(User.id).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user.user_list', page=user.next_num)\
            if user.has_next else None
    prev_url = url_for('user.user_list', page=user.prev_num)\
            if user.has_prev else None
    return render_template('user_list.html', 
                            edit_form=edit_form,
                            count_data=count_data,
                            user=user.items,
                            next_url=next_url,
                            prev_url=prev_url,
                            page=page
                            )

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('user.login'))

@bp.route('/user/delete/<int:id>')
@login_required
def user_delete(id):
    if current_user.level == 'Admin':
        user_to_delete = User.query.get_or_404(id)
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('User has been deleted')
            return redirect(url_for('user.user_list'))
        except:
            db.session.rollback()
            flash('Problem occured. cannot delete this user')
            return redirect(url_for('user.user_list'))

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.',1)[1].lower() in current_app.config['ALLOWED_EXTENSION']