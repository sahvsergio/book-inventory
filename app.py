#!/usr/bin/env python3.10
import io
from io import BytesIO
import base64
import os
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import sqlalchemy
from sqlalchemy import cast, create_engine, func, or_, select
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap5

# ==========================================
# 1. ONE-WAY IMPORTS FROM MODELS
# ==========================================
from models import db, Book  # Pull both out of models.py smoothly

app = Flask(__name__, instance_path=f'{os.getcwd()}')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Bind the database to this app instance
db.init_app(app)
bootstrap = Bootstrap5(app)

# Connect to the database engine for extension use cases
with app.app_context():
    engine = db.engine

# Config the admin site
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(ModelView(Book, db.session))

# ==========================================
# 3. ROUTE DEFINITIONS (Keep all routes exactly the same as before)
# ==========================================
# ==========================================
# 3. ROUTE DEFINITIONS
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders the main index page with book listings and pagination."""
    # Retrieve all book records smoothly via modern execution
    books = db.session.execute(db.select(Book)).scalars().all()
    total_books = len(books)
    
    # Prepare pagination parameters systematically
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(books) + per_page - 1) // per_page
    books_on_page = books[start:end]

    return render_template(
        'index.html', 
        books=books, 
        total_books=total_books, 
        books_on_page=books_on_page, 
        total_pages=total_pages, 
        page=page
    )


@app.route('/book/<id>')
def book(id):
    """Fetches details for a single book using SQLAlchemy 3.0+ session handling."""
    # Book.query.get_or_404 is deprecated/broken in modern setups
    book = db.session.get(Book, id)
    if not book:
        return render_template('404.html', msg="Book data structure not found."), 404
        
    book_length = db.session.execute(db.select(Book)).scalars().all()
    isbn = book.isbn
    
    return render_template(
        'book.html', 
        book=book, 
        book_length=book_length, 
        isbn=isbn
    )


@app.route('/addbook', methods=['GET', 'POST'])
def add_book():
    """Handles the creation of a new Book entry into the database repository."""
    if request.method == 'POST' and request.form:
        new_book = Book(
            book_name=request.form['book_name'],
            isbn=request.form['ISBN'],
            date_published=request.form['date_pusblished'],
            genre=request.form['genre'],
            date_sold=request.form['date_sold'],
            number_of_pages=int(request.form['number_of_pages']) if request.form['number_of_pages'].isdigit() else 0,
            language=request.form['language'],
            description=request.form['description'],
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))
        
    return render_template('addbook.html')


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_book(id):
    """Updates an existing Book entity safely via session state management."""
    book = db.session.get(Book, id)
    if not book:
        return render_template('404.html', msg="Book data structure not found."), 404

    if request.method == 'POST' and request.form:
        book.book_name = request.form['book_name']
        book.isbn = request.form['ISBN']
        book.date_published = request.form['date_pusblished']
        book.genre = request.form['genre']
        book.date_sold = request.form['date_sold']
        book.number_of_pages = int(request.form['number_of_pages']) if request.form['number_of_pages'].isdigit() else 0
        book.language = request.form['language']
        book.description = request.form['description']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit-book.html', book=book)


@app.route('/delete/<id>')
def delete_book(id):
    """Deletes a targeted book record safely without crashing the transaction manager."""
    book = db.session.get(Book, id)
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Executes structural SQL LIKE operations to query items matching criteria."""
    if request.method == 'POST':
        form = request.form
        search_value = form['searchstring']
        search_pattern = f'%{search_value}%'
        
        # Modern execution block matching SQLAlchemy 2.0/3.0 paradigms
        stmt = db.select(Book).where(
            or_(
                Book.book_name.like(search_pattern),
                Book.isbn.like(search_pattern)
            )
        )
        results = db.session.execute(stmt).scalars().all()

        page = request.args.get('page', 1, type=int)
        per_page = 10
        total_pages = (len(results) + per_page - 1) // per_page

        return render_template(
            'index.html', 
            results=results, 
            page=page, 
            total_pages=total_pages
        )
    else:
        return redirect(url_for('index'))


@app.route('/stats')
def stats():
    """Calculates statistics and presents transactional data charts."""
    records = db.session.execute(db.select(Book)).scalars().all()
    charts_data = charts()

    return render_template(
        'stats.html', 
        title='Book Stats', 
        records=records, 
        charts_data=charts_data
    )


def charts():
    """Generates an embedded visualization plot for tracking metric performance."""
    fig = Figure(figsize=(10, 4))
    ax = fig.subplots()
    ax.plot([1, 2])
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    
    return f"<img src='data:image/png;base64,{data}' />"


@app.errorhandler(404)
def not_found(error):
    """Standard fallback route handler for missing files or endpoints."""
    return render_template('404.html', msg=error), 404


# ==========================================
# 4. RUNTIME SYSTEM EXECUTION
# ==========================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Network-accessible infrastructure interface run setup
    app.run(host='0.0.0.0', port=8080, debug=True)