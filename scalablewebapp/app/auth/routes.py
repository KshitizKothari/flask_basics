from app import db, bcrypt
from app.auth import authentication as at
from app.auth.forms import RegistrationForm, LoginForm, ChangePassword
from flask import render_template, flash, redirect, url_for, request
from app.auth.models import User
from flask_login import login_user, logout_user, login_required, current_user


@at.route('/register', methods=['GET','POST'])
def register_user():
    if current_user.is_authenticated:
        flash('Already Logged In')
        return redirect(url_for('main.display_books'))
    form=RegistrationForm()
    if form.validate_on_submit():
        User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        flash('User account created for'+form.name.data,'success')
        return redirect(url_for('authentication.do_the_login'))
    return render_template('registration.html', form=form)


@at.route('/login', methods=['GET', 'POST'])
def do_the_login():
    if current_user.is_authenticated:
        flash('Already Logged In')
        return redirect(url_for('main.display_books'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(user_email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid Credential')
            return redirect(url_for('authentication.do_the_login'))

        login_user(user, form.stay_loggedin.data)
        return redirect(url_for('main.display_books'))

    return render_template('login.html', form=form)

@at.route('/logout')
@login_required
def do_the_logout():
    logout_user()
    return redirect(url_for('authentication.do_the_login'))


@at.route('/user_profile/<user_id>', methods=['GET', 'POST'])
@login_required
def user_profile(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        input = request.form
        if input['action'] == 'change_password':
            return redirect(url_for('authentication.change_password', user_id=user.id))

        elif input['action'] == 'delete_user':
            db.session.delete(user)
            db.session.commit()
            flash(user.user_email + ' has been successfully deleted')
            return redirect(url_for('authentication.do_the_login'))
    return render_template('user_profile.html', user=user)


@at.route('/change_password/<user_id>', methods=['GET', 'POST'])
def change_password(user_id):
    form = ChangePassword()
    user = User.query.get(user_id)
    if form.validate_on_submit() and user.check_password(form.old_password.data):
        p = user.user_name
        user.user_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        db.session.commit()
        flash('Password has been updated for '+p)
        return redirect(url_for('main.display_books'))
    return render_template('change_password.html', form=form)

@at.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html')



