from flask import Blueprint, request, flash , redirect, url_for, render_template , session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Bug
from . import db

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    return render_template("index.html")

@bp.route('/login', methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):

            flash('Invalid credentials', 'danger')
            return redirect(url_for('main.login_page'))
        session['user_id'] = user.id
        session['role'] = user.role
        flash('Logged in successfully', 'success')

        if user.role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        else:
            return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@bp.route('/register', methods=['GET','POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role' , 'developer')

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('main.register_page'))
        
        hased_password = generate_password_hash(password)
        new_user = User(username=username, password=hased_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('main.login_page'))
    return render_template('register.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('main.login_page'))

@bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    role = session.get('role')
    if not user_id:
        flash('Please log in to access this page', 'warning')
        return redirect(url_for('main.login_page'))
    
    if role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
    
    tasks = Bug.query.filter_by(assigned_to = user_id).all()
    current_user = User.query.filter_by(id=user_id).first()
    return render_template('dashboard.html' , current_user=current_user , tasks=tasks)


@bp.route('/admin')
def admin_dashboard():
    role = session.get('role')
    if role != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('main.dashboard'))
    users = User.query.all()
    tasks = Bug.query.all()
    return render_template('admin.html', users=users, tasks=tasks)

@bp.route('/tasks/create', methods = ['GET' , 'POST'])
def create_task():
    user_id = session.get('user_id')
    role = session.get('role')
    if not user_id:
        flash('Please log in to access this page' , 'warning')
        return redirect(url_for('main.login_page'))
    users = User.query.all() if role == 'admin' else []
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description' , "")
        assigned_to = request.form.get('assigned_to', user_id)

        task = Bug(title=title , description=description , assigned_to= assigned_to)
        db.session.add(task)
        db.session.commit()
        flash("Task added successfully!!" , "success")

        role = session.get("role")
        if role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        else:
            return redirect(url_for('main.dashboard'))
        
    return render_template('create_task.html', users=users , role=role)

@bp.route('/tasks/<int:task_id>/update' , methods = ['GET' , 'POST'])
def update_task(task_id):
    user_id = session.get('user_id')
    role = session.get('role')

    if not user_id:
        flash("Please login to access this page" , "warning")
        return redirect(url_for('main.login'))
    task = Bug.query.get_or_404(task_id)
    if role != 'admin' and task.assigned_to != user_id:
        flash('Permission denied' , 'danger')
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form.get('description' , task.description)
        task.status = request.form.get('status' , task.status)
        db.session.commit()
        flash('Task updated successfully!' , "success")

        if role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        else:
            return redirect(url_for('main.dashboard'))
    return render_template('update_task.html' , task=task)    

@bp.route('/tasks/<int:task_id>/delete')
def delete_task(task_id):
    user_id = session.get('user_id')
    role = session.get('role')

    if not user_id:
        flash('Please log in to access this page' , 'warning')
        return redirect(url_for('main.login'))
    task = Bug.query.get_or_404(task_id)
    if role != 'admin':
        flash('Permission denied' , 'danger')
        return redirect(url_for('main.dashboard'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!' , 'success')
    return redirect(url_for('main.admin_dashboard'))
    
@bp.route('/users/<int:user_id>/edit' , methods = ['GET' , 'POST'])
def update_user(user_id):
    role = session.get('role')
    if role != 'admin':
        flash('Permission denied' , 'danger')
        return redirect(url_for('main.dashboard'))
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form['username']
        if request.form.get('password'):
            user.password = generate_password_hash(request.form['password'])
        user.role = request.form['role']
        db.session.commit()
        flash('User updated successfully' , 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('update_user.html' , user=user)

@bp.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    current_user = session.get('user_id')
    role = session.get('role')
    if role != 'admin':
        flash('permission denied' , 'danger')
        return redirect(url_for('main.dashboard'))
    user = User.query.get_or_404(user_id)

    if user.id == current_user:
        flash("Cannot delete yourself man" , 'danger')
        return redirect(url_for('main.admin_dashboard'))

    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.id} deleted successfully' , 'success')
    return redirect(url_for('main.admin_dashboard'))








    
