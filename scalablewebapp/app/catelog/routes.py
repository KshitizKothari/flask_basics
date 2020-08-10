from app.catelog import main
from app import db
from app.catelog.models import Publication, Book
from flask import render_template, request, flash, redirect,url_for
from flask_login import login_required
from app.catelog.form import EditBookForm, CreateBookForm

@main.route('/')
@main.route('/home')
def display_books():
    books = Book.query.all()
    return render_template('home.html', books=books)


@main.route('/display/publisher/<publisher_id>')
def publisher(publisher_id):
    publisher = Publication.query.filter_by(id=publisher_id).first()
    publisher_books = Book.query.filter_by(pub_id=publisher_id).all()
    return render_template('publisher.html', publisher=publisher, publisher_books=publisher_books)


@main.route('/book/delete/<book_id>', methods=['POST', 'GET'])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        flash(book.title+'has been deleted')
        return redirect(url_for('main.display_books'))
    return render_template('delete_book.html', book=book, book_id=book_id)


@main.route('/edit_book/<book_id>', methods=['POST', 'GET'])
@login_required
def edit_book(book_id):
    book=Book.query.get(book_id)
    form=EditBookForm(obj=book)
    if request.method == 'POST':
        book.title = form.title.data
        book.format = form.format.data
        book.num_pages = form.num_pages.data

        db.session.add(book)
        db.session.commit()
        flash('Book edited sucessfully')
        return redirect(url_for('main.display_books'))
    return render_template('edit_book.html', form=form)


@main.route('/create_book/<pub_id>', methods=['POST', 'GET'])
@login_required
def create_book(pub_id):

    form = CreateBookForm()
    form.pub_id.data = pub_id   #pre-populating pub_id
    if form.validate_on_submit():
        book = Book(
                    title=form.title.data,
                    author=form.author.data,
                    book_format=form.format.data,
                    avg_rating=form.avg_rating.data,
                    image=form.image_url.data,
                    num_pages=form.num_pages.data,
                    pub_id=form.pub_id.data
                 )
        db.session.add(book)
        db.session.commit()
        flash('Book created sucessfully')
        return redirect(url_for('main.publisher', publisher_id=pub_id))
    return render_template('create_book.html', form=form, pub_id=pub_id)
