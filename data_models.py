from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.String(10))
    date_of_death = db.Column(db.String(10))
    books = db.relationship('Book', backref='author', lazy=True)

    def __str__(self):
        return self.name

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20))
    title = db.Column(db.String(120), nullable=False)
    publication_year = db.Column(db.String(4))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __str__(self):
        return f"{self.title} by {self.author.name}"
