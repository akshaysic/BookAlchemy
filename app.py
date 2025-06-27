from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)


@app.route('/')
def home():
    """
    Display the homepage with a list of books.

    Allows optional filtering by title or author using a query string,
    and supports sorting by title or author name.
    """
    query = request.args.get('query')
    sort = request.args.get('sort')

    books = Book.query
    if query:
        books = books.filter(
            (Book.title.ilike(f'%{query}%')) |
            (Book.author.has(Author.name.ilike(f'%{query}%')))
        )

    if sort == 'title':
        books = books.order_by(Book.title)
    elif sort == 'author':
        books = books.join(Author).order_by(Author.name)

    return render_template('home.html', books=books.all())


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Display a form to add a new author.

    On POST request, creates a new Author and saves it to the database.
    """
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        date_of_death = request.form['date_of_death']

        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        flash('Author added successfully!')
        return redirect(url_for('add_author'))

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Display a form to add a new book.

    On POST request, creates a new Book linked to an existing author
    and saves it to the database.
    """
    authors = Author.query.all()
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('add_book'))

    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Delete a book by its ID.

    If the author has no other books after deletion, the author is also removed.
    """
    book = Book.query.get_or_404(book_id)
    author = book.author
    db.session.delete(book)
    db.session.commit()

    if not author.books:
        db.session.delete(author)
        db.session.commit()

    flash('Book deleted successfully!')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
