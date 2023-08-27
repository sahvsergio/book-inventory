#!/usr/bin/env python3.10

import io
import random


# Third party imports
# import matplotlib as plt


import numpy as np
import pandas as pd
import requests
import sqlalchemy

from flask import flash, redirect, render_template, request, url_for

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import cast, func, or_, select
from sqlalchemy.orm import scoped_session, sessionmaker


from models import Book, Flask, app, db

# connect to the dabatase for pandas
with app.app_context():
    engine = db.engine

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

admin.add_view(ModelView(Book, db.session))

# create routes(visible parts of the site- urls)


@app.route('/', methods=['GET', 'POST'])  # decorator
def index():
    """creates the homepage for the app"""
    books = Book.query.all()
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

    return render_template('index.html', books=books, total_books=total_books, book_cover_urls=book_cover_urls)


@app.route('/book/<id>')
def book(id):
    """Creates the view for the app"""
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
    """Creates the route to create new books on the app and adds it to the database"""

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
    """Edits the book information both in the app and database"""
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
    """deletes books from the database and from the  app """
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])  # creating route
def search():
    if request.method == 'POST':  # if there is a post request on this side
        form = request.form  # getting the form info
        # selecting the form field where there is one  search text
        search_value = form['searchstring']
        # defining that whatever comes in the search value will be in there
        search = '%{0}%'.format(search_value)
        results = Book.query.filter(or_(Book.book_name.like(search),  # making the query through sqlalchemy and sql like queries
                                        Book.isbn.like(search))).all()
        total_results = len(results)
        return render_template('index.html', books=results, pageTitle='Sergio\'s Books', legend='Search  Results', total_results=total_results)
    else:
        return redirect('/')


@app.route('/stats')
def stats():
   pass


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors-non existant pages"""
    return render_template('404.html', msg=error), 404


if __name__ == '__main__':
    # if it were to be exported to a diffent filem then the --main .- would be the name of the file it is exported t
    with app.app_context():
        db.create_all()

    # making the app run, you just need to run the app.py file on the terminal
    # local app.run(debug=True , port=8000, host='127.0.0.1')
    # internet
    app.run(host='0.0.0.0', port=8080)
