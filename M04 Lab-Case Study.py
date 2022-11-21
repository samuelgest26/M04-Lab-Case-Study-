"""
Samuel Gest

M04 Lab-Case Study.py

 Classes and functions

class Book(): defines everything in database
    id: the id of the book, primary key
    book_name: the unique  name of the book
    author: author
    publisher: publisher

    def get_books(): print out data of books.
    get get_book(): return error 
    def add_book(): adds books using POST
    def delete_book(): deletes books using DELETE
"""

import tempfile
import os.path
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(tempfile.gettempdir(), 'test.db')
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True,nullable=False)
    author = db.Column(db.String(80))
    publisher = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data={'book_name': book.book_name, 'author':book.author, 'publisher':book.publisher}
        output.append(book_data)
    return{"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"name":book.book_name,"author":book.author,'publisher':book.publisher}

@app.route('/books',methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], author=request.json['author'],publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id':book.id}

@app.route('/books/<id>',methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error":"not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message":"Yeet!"}