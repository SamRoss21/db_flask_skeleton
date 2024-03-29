from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.models import User, Concept
from app.forms import LoginForm, RegistrationForm, AddConcept
from app import db 

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = AddConcept()
    if form.validate_on_submit():
        concept = Concept(concept=form.concept.data, user_id=current_user.id, num_im=0, verified='0',deleted='0')
        db.session.add(concept)
        db.session.commit()
        flash('Concept Added')
        return redirect(url_for('index'))
    concepts = Concept.query.filter_by(deleted=False).order_by(Concept.timestamp.desc())
    return render_template("index.html", title='Home Page', form=form,
                           concepts=concepts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/deleteConcept", methods=['GET','POST'])
def deleteConcept():
    form = AddConcept()
    concept = request.form['data']
    del_concept = Concept.query.filter_by(concept=concept).first()
    del_concept.deleted='1'
    db.session.commit()
    concepts = Concept.query.filter_by(deleted=False).order_by(Concept.timestamp.desc())
    print(concepts)
    return render_template("index.html", title='Home Page', form=form,
                           concepts=concepts)




