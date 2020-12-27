from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginUserForm, RegistrationUserForm, ResetUserPasswordForm, ResetPasswordRequestForm, AddTaskForm, EditTaskForm
from app.models import User, Task
from flask_login import current_user, login_user, logout_user, login_required
from app.email import send_password_reset_email

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('user_task',user_name=current_user.username))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your Email adrress for the instruction to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Pssword', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetUserPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)

@app.route('/user/<user_name>', methods=['GET','POST'])
@login_required
def user_task(user_name):
    form = AddTaskForm()
    if form.validate_on_submit():
        task = Task(content=form.content.data, owner=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Your task was added')
        return redirect(url_for('user_task', user_name=current_user.username))
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.timestamp).all()
    return render_template('user_task.html', title='{}s task'.format(current_user.username), form=form, tasks=tasks)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash('Your task was been deleted')
        return redirect(url_for('user_task', user_name=current_user.username))
    except:
        flash ('There was an issue deleting your task')

@app.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update(id):
    task_to_update = Task.query.get_or_404(id)
    form = EditTaskForm(content=task_to_update.content)
    if form.validate_on_submit():
        new_task = form.content.data
        try:
            task_to_update.content = new_task
            db.session.commit()
            flash('Your task was been updated')
        except:
            flash('There was an issue updating your task')
        return redirect(url_for('user_task', user_name=current_user.username))
    return render_template('update.html', form=form, title='Update task')
