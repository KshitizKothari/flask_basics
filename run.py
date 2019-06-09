from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

app.config.update(
    SECRET_KEY='THISISSECRETKEY',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:postre123@localhost/catelog_db',
                            #   ⬆             ⬆         ⬆        ⬆          ⬆
                            #<database>://<userid>:<password>@<server>/<database_name>
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db=SQLAlchemy(app)


class Publication(db.Model):
    __tablename__='publication'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return 'The name is {}'.format(self.name)


class Book(db.Model):

    __tablename__='books'

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String,nullable=False, index=True)
    author=db.Column(db.String)
    avg_rating=db.Column(db.Float)
    format=db.Column(db.String)
    image=db.Column(db.String, unique=True)
    num_pages=db.Column(db.Integer)
    pub_date=db.Column(db.DateTime, default=datetime.utcnow())

    #relationship
    pub_id=db.Column(db.Integer,db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title=title
        self.author=author
        self.avg_rating=avg_rating
        self.format=book_format
        self.image=image
        self.num_pages=num_pages
        self.pub_id=pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title,self.author)





@app.route('/')
def home():
    return render_template('home.html')


if __name__=='__main__':
    db.create_all()
    app.run(debug=True)