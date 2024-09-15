"""Provide several sample math calculations.

This module allows the user to make mathematical calculations.

The module contains the following functions:

- `add(a, b)` - Returns the sum of two numbers.
- `subtract(a, b)` - Returns the difference of two numbers.
- `multiply(a, b)` - Returns the product of two numbers.
- `divide(a, b)` - Returns the quotient of two numbers.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__, instance_path=f'{os.getcwd()}')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db= SQLAlchemy(app)

class Book(db.Model):
    """
    A class used to represent an Animal

    ...

    Attributes
    ----------
    says_str : str
        a formatted string to print out what the animal says
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """
    id= db.Column(db.Integer, primary_key=True)#primary key
    created= db.Column('Created',db.DateTime, default = datetime.datetime.now)#timestamp when the item was created
    book_name=db.Column('Name of the book',db.String())
    date_published = db.Column('Date_published', db.String())
    genre = db.Column('Genre',db.String())
    date_sold = db.Column('Date Sold',db.String())
    number_of_pages = db.Column('Number of Pages',db.String())   
    language = db.Column('Language',db.String())
    description = db.Column('Description',db.Text)
    isbn=db.Column('ISBN', db.String())
 
    


#finish creating the fields here, before setting the site again
    def __repr__(self):
        """Prints what the animals name is and what sound it makes.

        If the argument `sound` isn't passed in, the default Animal
        sound is used.

        Parameters
        ----------
        sound : str, optional
            The sound the animal makes (default is None)

        Raises
        ------
        NotImplementedError
            If no sound is set for the animal or passed in as a
            parameter.
        """
        return f'''
            Book Name:{self.book_name}
            Created:{self.created}
            Date Published :{self.date_published}
            Genre:{self.genre}
            Date Sold:{self.date_sold}
            Language: {self.language}
            Description: {self.description}
            Number of pages:{self.number_of_pages}
                
                )
                '''
                
                

