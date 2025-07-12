# Personal Expense Tracker

A modern, user-friendly web application built with Python Flask for tracking personal expenses. Features a beautiful, responsive interface with comprehensive expense management capabilities.

## Features

### Core Features
-  **User Authentication**: Secure login/signup system with password hashing
-  **Add Expenses**: Record expenses with amount, category, date, and description
-  **View Expenses**: Tabular view of all expenses sorted by date
-  **Edit Expenses**: Modify existing expense entries
-  **Delete Expenses**: Remove unwanted expense records
-  **Dashboard Summary**: Overview of total expenses and monthly spending
-  **Category Breakdown**: Visual breakdown of expenses by category

### User Interface
-  **Modern Design**: Beautiful gradient background with glass-morphism effects
-  **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
-  **Fast & Smooth**: Optimized performance with Bootstrap 5
-  **User-Friendly**: Intuitive navigation and clear visual hierarchy

### Security Features
-  **Password Hashing**: Secure password storage using Werkzeug
-  **User Isolation**: Users can only access their own expenses
-  **Session Management**: Secure login/logout functionality

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download
```bash
# If using git
git clone <repository-url>
cd ExpenseTrackerP

# Or simply download and extract the project files
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### First Time Setup
1. **Register**: Create a new account with username, email, and password
2. **Login**: Sign in with your credentials
3. **Start Tracking**: Add your first expense entry

### Adding Expenses
1. Click "Add Expense" from the navigation or dashboard
2. Fill in the required fields:
   - **Amount**: Enter the expense amount
   - **Category**: Select from predefined categories
   - **Description**: Optional description of the expense
   - **Date**: Choose the expense date (defaults to today)
3. Click "Add Expense" to save

### Managing Expenses
- **View**: All expenses are displayed in a table on the dashboard
- **Edit**: Click the edit button (pencil icon) next to any expense
- **Delete**: Click the delete button (trash icon) to remove an expense

### Dashboard Features
- **Total Expenses**: Shows your overall spending
- **Monthly Spending**: Current month's total expenses
- **Category Breakdown**: Visual representation of spending by category
- **Recent Expenses**: Latest expense entries in a sortable table

## Project Structure

```
ExpenseTrackerP/
├── app.py                 
├── requirements.txt       
├── README.md             
├── templates/            
│   ├── base.html         
│   ├── login.html        
│   ├── register.html     
│   ├── dashboard.html    
│   ├── add_expense.html  
│   └── edit_expense.html 
└── expenses.db           
```

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Charts**: Chart.js (ready for future enhancements)

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password

### Expenses Table
- `id`: Primary key
- `amount`: Expense amount (float)
- `category`: Expense category (string)
- `description`: Optional description (string)
- `date`: Expense date (datetime)
- `user_id`: Foreign key to users table

## Customization

### Adding New Categories
To add new expense categories, modify the select options in:
- `templates/add_expense.html`
- `templates/edit_expense.html`

### Styling Changes
The main styling is in `templates/base.html`. You can customize:
- Color scheme (CSS variables in `:root`)
- Background gradients
- Card styling and animations

### Database Configuration
The application uses SQLite by default. To use a different database:
1. Update `SQLALCHEMY_DATABASE_URI` in `app.py`
2. Install appropriate database drivers

## Security Considerations

- Passwords are hashed using Werkzeug's security functions
- Users can only access their own expense data
- SQL injection protection through SQLAlchemy ORM
- CSRF protection available through Flask-WTF (can be enabled)

## Future Enhancements

Potential features for future versions:
-  **Advanced Analytics**: Charts and graphs for spending patterns
-  **Date Range Filtering**: Filter expenses by date ranges
-  **Export Functionality**: Export expenses to CSV/PDF
-  **Mobile App**: Native mobile application
-  **Notifications**: Budget alerts and reminders
-  **Budget Planning**: Set and track budget goals
-  **Custom Categories**: User-defined expense categories

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change the port in app.py
   app.run(debug=True, port=5001)
   ```

2. **Database Issues**
   ```bash
   # Delete the database file and restart
   rm expenses.db
   python app.py
   ```

3. **Import Errors**
   ```bash
   # Ensure all dependencies are installed
   pip install -r requirements.txt
   ```

### Getting Help
If you encounter any issues:
1. Check that all dependencies are installed correctly
2. Ensure Python 3.7+ is being used
3. Verify the database file has proper permissions

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---
