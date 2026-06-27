# models.py
import datetime
from flask_sqlalchemy import SQLAlchemy

# Create the database object right here
db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column('Created', db.DateTime, default=datetime.datetime.now)
    book_name = db.Column('Name of the book', db.String())
    date_published = db.Column('Date_published', db.String())
    genre = db.Column('Genre', db.String())
    date_sold = db.Column('Date Sold', db.String())
    number_of_pages = db.Column('Number of Pages', db.Integer)   
    language = db.Column('Language', db.String())
    description = db.Column('Description', db.Text)
    isbn = db.Column('ISBN', db.String())
 
    def __repr__(self):
        return f'<Book {self.book_name}>'