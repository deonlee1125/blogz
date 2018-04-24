from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y2k2000'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner #Object that links to backref='owner' below. Owner is a User object

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')
    #line above means squalchemy should populate blogs list with things from class Blogs
    # such that their owner property is equal to the specific user in consideration 
  
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['index', 'blog', 'login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods=['POST', 'GET'])
def index():
    #displays a bulleted list of all users with logins with hyperlinks
    #to each author's own posts (singleUser)
    #if method == 'GET': render 'singleUser.html'
    #return redirect('/blog?user= {username}') 
    
    users = User.query.all()
    if request.method == 'GET':
        return render_template('index.html', users=users)
    else:
        user_id = int(request.args.get('owner_id'))
        owner = User.query.filter_by(user_id=user_id).first()
        return render_template("singleUser.html", owner=owner)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form['password']
        password_verify= request.form['password_verify']
        username_error=""
        password_error_1=""
        password_error_2=""
        existing_user_error=""

        if username=="" or " " in username or len(username) <3 or len(username) >20:
            username_error="  Username is not valid."

        if password=="" or " " in password or len(password) <3 or len(password) >20:
            password_error_1="  Password is not valid."

        if password != password_verify:
            password_error_2="  Password must match password verification."

        if not username_error and not password_error_1 and not password_error_2:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return render_template('newpost.html')
            if existing_user:
                existing_user_error = "  A user with that name already exists."
        return render_template('signup.html', username_error=username_error, password_error_1=password_error_1, password_error_2=password_error_2, existing_user_error=existing_user_error)
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in", "correct")
            #return render_template('newpost.html')
            return redirect('/blog/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/blog', methods=['GET'])
def blog():
    #retrieves and displays all blog posts (title, body) from DB
    #Contains hyperlinks on titles to allow navigation to single page ("/blog?ID=#")

    if request.args.get('id'):
        blog_id = int(request.args.get('id'))
        blog_post = Blog.query.get(blog_id)
        user_id = int(request.args.get('id'))
        username = User.query.get(user_id)
        return render_template('singlepage.html', title=blog_post.title, body=blog_post.body, username=username.username)
    else:
        blogs = Blog.query.all()
        users = User.query.all()
        return render_template('blog.html', title='blog posts!', blogs=blogs, users=users)

@app.route('/blog/newpost', methods=['POST', 'GET'])
def newpost(): 
    #Displays form allowing users to input blog title and body
    #POSTS blogpost (title, body) to DB
    #Verify: If title or body blank, reload w/error ms..
            #..If OK, redirect to singlepage '/blog?ID=#' and display
    #If GET, display singlepage; if POST posts blogs to DB
#User.query.filter_by(email=session['email']).first() find first user with this email
#movie = Movie(new)movie_name, usr)


    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == "" or body == "":
            flash('Blog posts must contain a title and body.', 'error')
            return render_template('newpost.html', title=title, body=body)
        else:
            blogs = Blog.query.all()
            username = request.form['username']
            owner = User.query.filter_by(username=username).first()
          
            blog_post = Blog(title, body, owner)
            db.session.add(blog_post)
            db.session.commit()
            return render_template('singlepage.html', blogs=blogs, users=users)
    
    return render_template('newpost.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')
   
if __name__ == '__main__':
    app.run()