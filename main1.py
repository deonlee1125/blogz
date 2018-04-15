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

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    #retrieves and displays all blog posts (title, body) from DB
    #Contains hyperlinks on titles to allow navigation to..
    #..single page ("/blog?ID=#") !!Not done!!

    title = ""
    body = ""
    title = Blog.query.get(title)
    body = Blog.query.get(body)
    return render_template('blog.html')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost(): 
    #Displays form allowing users to input blog title and body
    #POSTS blogpost (title, body) to DB
    #Verify: If title or body blank, reload w/error ms..
            #..If OK, redirect to singlepage '/blog?ID=#' and display
    #If GET, display singlepage; if POST posts blogs to DB
    
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect("/blog")

        if title != "" and body != "":        
            blog_post = Blog(title, body)
            db.session.add(blog_post)
            db.session.commit()
            return render_template('newpost.html')
        else:
            flash('Title and body cannot be blank.', 'error')
            return render_template('newpost.html')
    else:
        return redirect("/blog")

@app.route('/')
def index():
    #redirects to blog page "/blog"
    return redirect('/blog')
        
if __name__ == '__main__':
    app.run()