from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!')
            return render_template('register.html')
        
        user = User(username=username, email=email, 
                   password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get all expenses for current user
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    
    # Calculate summary statistics
    total_expenses = sum(expense.amount for expense in expenses)
    
    # Monthly spending (current month)
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_expenses = [expense for expense in expenses 
                       if expense.date.month == current_month and expense.date.year == current_year]
    monthly_total = sum(expense.amount for expense in monthly_expenses)
    
    # Category breakdown
    categories = {}
    for expense in expenses:
        if expense.category in categories:
            categories[expense.category] += expense.amount
        else:
            categories[expense.category] = expense.amount
    
    return render_template('dashboard.html', 
                         expenses=expenses,
                         total_expenses=total_expenses,
                         monthly_total=monthly_total,
                         categories=categories)

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        date_str = request.form['date']
        
        # Parse date
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            date = datetime.now()
        
        expense = Expense(amount=amount, category=category, 
                        description=description, date=date, user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()
        
        flash('Expense added successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_expense.html')

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    # Ensure user can only edit their own expenses
    if expense.user_id != current_user.id:
        flash('You can only edit your own expenses!')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        expense.amount = float(request.form['amount'])
        expense.category = request.form['category']
        expense.description = request.form['description']
        expense.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        
        db.session.commit()
        flash('Expense updated successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_expense.html', expense=expense)

@app.route('/delete_expense/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    # Ensure user can only delete their own expenses
    if expense.user_id != current_user.id:
        flash('You can only delete your own expenses!')
        return redirect(url_for('dashboard'))
    
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!')
    return redirect(url_for('dashboard'))

@app.route('/api/expenses')
@login_required
def api_expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    return jsonify([{
        'id': expense.id,
        'amount': expense.amount,
        'category': expense.category,
        'description': expense.description,
        'date': expense.date.strftime('%Y-%m-%d')
    } for expense in expenses])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 