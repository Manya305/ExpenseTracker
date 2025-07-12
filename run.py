#!/usr/bin/env python3
"""
Personal Expense Tracker - Startup Script
"""

import os
import sys
from app import app, db

def main():
    """Main function to run the Flask application"""
    print("Starting Personal Expense Tracker...")
    print("A modern expense tracking application")
    print("=" * 50)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print(" Database initialized successfully")
    
    # Run the application
    print("Application will be available at: http://localhost:5000")
    print("Register a new account to get started!")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main() 