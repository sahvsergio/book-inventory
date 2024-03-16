#!/usr/bin/env python3.10
"""Provide several sample math calculations.

This module allows the user to make mathematical calculations.

The module contains the following functions:

- `add(a, b)` - Returns the sum of two numbers.
- `subtract(a, b)` - Returns the difference of two numbers.
- `multiply(a, b)` - Returns the product of two numbers.
- `divide(a, b)` - Returns the quotient of two numbers.
"""


# Standard library imports

# creating a buffer
import io
from io import BytesIO

# Third-party imports

# decoding the buffer
import base64
# plotting the  charts
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# data handling
import numpy as np
import pandas as pd

# handling the apis
import requests

# handling the database and models
import sqlalchemy
from sqlalchemy import create_engine, cast, func, or_, select
from sqlalchemy.orm import scoped_session, sessionmaker

# flask imports
from flask import flash, redirect, render_template, request, url_for

# flask admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# flask_bootstrap
from flask_bootstrap import Bootstrap5

# Local imports
# models
from models import Book, Flask, app, db

bootstrap = Bootstrap(app)
# connect to the dabatase for pandas
with app.app_context():
    engine = db.engine

# config the admin site

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

admin.add_view(ModelView(Book, db.session))

# create routes(visible parts of the site- urls)


@app.route('/', methods=['GET', 'POST'])  # decorator
def index():
    """Renders the index page of the app.

    Examples:
        >>> index()
        6.0
        >>> index()


    Args:
       none

    Returns:
        float: A number representing the arithmetic sum of `a` and `b`.
    """
    # get the entire books
    books = Book.query.all()
    # print the total books
    total_books = len(books)
    book_cover_urls = []
    for book in books:
        isbn = book.isbn
        book_cover = requests.get(
            f'https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg')
        if book_cover.status_code == 200:
            book_cover_urls.append(book_cover.url)
        else:

            book_cover_urls.append(None)
    # prepare pagination
    page = request.args.get('page', 1, type=int)
    per_page = 2

    start = (page-1)*per_page
    end = start+per_page
    total_pages = (len(books)+per_page-1)//per_page
    books_on_page = books[start:end]

    return render_template('index.html', books=books, total_books=total_books, book_cover_urls=book_cover_urls, books_on_page=books_on_page, total_pages=total_pages, page=page)


@app.route('/book/<id>')
def book(id):
    """Compute and return the sum of two numbers.

    Examples:
        >>> add(4.0, 2.0)
        6.0
        >>> add(4, 2)
        6.0

    Args:
        a (float): A number representing the first addend in the addition.
        b (float): A number representing the second addend in the addition.

    Returns:
        float: A number representing the arithmetic sum of `a` and `b`.
    """
    book = Book.query.get_or_404(id)
    book_length = Book.query.all()
    isbn = book.isbn
    print('this is the isbn for this book', isbn)
    book_cover = requests.get(
        f'https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg')
    if book_cover.status_code == 200:
        book_cover_url = book_cover.url
        print('this is the url for the book cover', book_cover.url)
        return render_template('book.html', book=book, book_length=book_length, isbn=isbn, book_cover_url=book_cover_url)
    else:
        return render_template('book.html', book=book, book_length=book_length, isbn=isbn, book_cover_url=book_cover_url)


@app.route('/addbook', methods=['GET', 'POST'])
def add_book():
    """Compute and return the sum of two numbers.

    Examples:
        >>> add(4.0, 2.0)
        6.0
        >>> add(4, 2)
        6.0

    Args:
        a (float): A number representing the first addend in the addition.
        b (float): A number representing the second addend in the addition.

    Returns:
        float: A number representing the arithmetic sum of `a` and `b`.
    """

    if request.form:
        new_book = Book(book_name=request.form['book_name'],
                        isbn=request.form['ISBN'],
                        date_published=request.form['date_pusblished'],
                        genre=request.form['genre'],
                        date_sold=request.form['date_sold'],
                        number_of_pages=request.form['number_of_pages'],
                        language=request.form['language'],
                        description=request.form['description'],
                        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('addbook.html')


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_book(id):
    """Compute and return the sum of two numbers.

    Examples:
        >>> add(4.0, 2.0)
        6.0
        >>> add(4, 2)
        6.0

    Args:
        a (float): A number representing the first addend in the addition.
        b (float): A number representing the second addend in the addition.

    Returns:
        float: A number representing the arithmetic sum of `a` and `b`.
    """
    book = Book.query.get(id)

    if request.form:
        book.book_name = request.form['book_name']
        book.isbn = request.form['ISBN']
        book.date_published = request.form['date_pusblished']
        book.genre = request.form['genre']
        book.date_sold = request.form['date_sold']
        book.number_of_pages = request.form['number_of_pages']
        book.language = request.form['language']
        book.description = request.form['description']

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit-book.html', book=book)


@app.route('/delete/<id>')
def delete_book(id):
    """Compute and return the sum of two numbers.

    Examples:
        >>> add(4.0, 2.0)
        6.0
        >>> add(4, 2)
        6.0

    Args:
        a (float): A number representing the first addend in the addition.
        b (float): A number representing the second addend in the addition.

    Returns:
        float: A number representing the arithmetic sum of `a` and `b`.
    """
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))




@app.route('/stats')
def stats():
    """Compute and return the sum of two numbers.

    Examples:
        >>> add(4.0, 2.0)
        6.0
        >>> add(4, 2)
        6.0

    Args:
        a (float): A number representing the first addend in the addition.
        b (float): A number representing the second addend in the addition.

    Returns:
        float: A number representing the arithmetic sum of `a` and `b`.
    """

    records = Book.query
    charts_data = charts()

    return render_template('stats.html', title='Book Stats', records=records, charts_data=charts_data)


def charts():
    """Compute and return the sum of two numbers.

    Examples:
        >>> add(4.0, 2.0)
        6.0
        >>> add(4, 2)
        6.0

    Args:
        a (float): A number representing the first addend in the addition.
        b (float): A number representing the second addend in the addition.

    Returns:
        float: A number representing the arithmetic sum of `a` and `b`.
    """

    # generate the plot without using pytplot
    fig = Figure(figsize=(10, 4))

    ax = fig.subplots()
    ax.plot([1, 2])
    # save it to a temporary buffer
    buf = BytesIO()

    fig.savefig(buf, format="png")
    # embed the result in the html output
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return f"<img src='data:image/png;base64,{data}' />"


@app.errorhandler(404)
def not_found(error):
    """Compute and return the sum of two numbers.

    Examples:
        >>> add(4.0, 2.0)
        6.0
        >>> add(4, 2)
        6.0

    Args:
        a (float): A number representing the first addend in the addition.
        b (float): A number representing the second addend in the addition.

    Returns:
        float: A number representing the arithmetic sum of `a` and `b`.
    """
    return render_template('404.html', msg=error), 404


if __name__ == '__main__':
    # if it were to be exported to a diffent filem then the --main .- would be the name of the file it is exported t
    with app.app_context():
        db.create_all()

    # making the app run, you just need to run the app.py file on the terminal
    # local app.run(debug=True , port=8000, host='127.0.0.1')
    # internet
    app.run(host='0.0.0.0', port=8080, debug=True)
