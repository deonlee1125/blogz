
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(150))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title != "" and body != "":
            #session['email'] = email
            flash("Great blog post!")

            blog_post = Blog(title, body)
            db.session.add(blog_post)
            db.session.commit()
            return redirect('/newpost')
        else:
            flash('Title and body cannot be blank', 'error')
    else:
        return render_template('index.html')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title = ""
    body = ""
    title = Blog.query.filter_by(title=title).first()
    body = Blog.query.filter_by(body=body).first()
    return render_template('newpost.html')


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    title = Blog.query.filter_by(title=title).all()
    body = Blog.query.filter_by(body=body).all()
    return render_template('blog.html')


if __name__ == '__main__':
    app.run()