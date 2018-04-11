from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1000))
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    new_body = ""
    new_title = ""
    if request.method == 'POST':
        title = request.form['title']
        new_title = Blog(title)
        body = request.form['body']
        new_body = Blog(body)

        db.session.add(new_title)
        db.session.add(new_body)
        db.session.commit()

    #tasks = Task.query.filter_by(completed=False).all()
    #completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('index.html', title="Build a Blog", 
        new_title=new_title, new_body=new_body)


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