from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y2k2000!'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(150))
    
    def __init__(self, title, body):
        self.title = title
        self.body = body


#displays form; retrieves user input
#tests for empty title or blog; if empty prints error, reloads form
#if title/blog not empty, stores user input (title, blog) in db and
#redirects to '/newpost' page
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title != "" and body != "":           
            new_title = Blog(title)
            new_body = Blog(body)
            
            new_user = Blog(title,body)
            
            db.session.add(new_user)
            db.session.commit()

        return "<h1>Yay!</h1>"
            #return redirect('/newpost')
        #else:
            #flash("You must have a title and body for each blog post", 'error')
    
    return "<h1>Fail</h1>"


    #return render_template('login.html')
    
    
    
    #if request.method == 'POST':
       # title = request.form['title']
        #titles.append(title)
        #body = request.form['body']
        
        #new_title = Blog(title)
        #db.session.add(new_title)
        #db.session.commit()
        
       # new_body = Blog(body)
        #db.session.add(new_body)
       # db.session.commit()


    #return render_template('index.html', title="Build a Blog", 
        #titles=titles, bodies=bodies)

#@app.route('/newpost', methods=['POST'])
#def newpost():
#retrieves current title and body from db
#displays current title and body

    #return render_template('index.html', title="Build a Blog", 
        #new_title=new_title, new_body=new_body)

#@app.route('/blog', methods=['POST'])
#def index():
#retrieves all titles and blog bodies from db

#tasks = Task.query.filter_by(completed=False).all()
#completed_tasks = Task.query.filter_by(completed=True).all()

#@app.route('/', methods=['POST'])
#def delete_task():

    #task_id = int(request.form['task-id'])
    #task = Task.query.get(task_id)
    #task.completed = True
    #db.session.add(task)
    #db.session.commit()

    #return redirect('/')


if __name__ == '__main__':
    app.run()