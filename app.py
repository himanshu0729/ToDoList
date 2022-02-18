from email.policy import default
from importlib.resources import contents
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
# For data and time
from datetime import datetime


# To reference just this file 
app = Flask(__name__)
# Now create a Flask application object and set URI for the database to be used.
# It is telling our app where our database is located
# Here we are using sqllite lots of resources are there how to this with MySql, PostgreSQL
# //// => for absolute path but here we are using relative path because keeping the dabase file in same folder
# Every thing is going to be store in test.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# Initiallize databse
# Then create an object of SQLAlchemy class with application object as the parameter. This object contains helper functions for ORM operations. It also provides a parent Model class using which user defined models are declared
db = SQLAlchemy(app)
class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    #  Ignore this line the completed column is never used
    completed = db.Column(db.Integer, default=0) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # We just need a function that is going to return a string every time we create a new element
    def __repr__(self):
        # so every time we make a new element it is just going to return task and then the id of that task that is just been created
        return '<Task %r>' % self.id


# Create a Index Route so that when browser to URL so that we just don't immediatly 404 
# In Flask for route use app.route() and app URL as string
# After the route going to add option called methods (so it can accept two methods, get is by default)
@app.route('/', methods=['POSt', 'GET'])
def index():
    # return "Hello 1st day in Flask"
    # It is going to say if the request that set to this route is post do that stuff
    if request.method == 'POST':
        # Put logic for adding a task here
        task_content = request.form['content'] 
        # create Todo object and it content is going to equal task_content
        new_task = Todo(content=task_content)
        # push it to database
        try:
            db.session.add(new_task)
            # commit to database
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding you task'
        
    else:
        # Create a variable tasks, it is going to look at all of the database contents in the order they were created
        tasks = Todo.query.order_by(Todo.date_created).all()
        #  pass it to the template 
        return render_template('index.html', tasks=tasks)
    # Here we are returing render_template
    # No need to specify folder name beacause it knows look into that folder(giving templates as folder name having some purpose)
    # return render_template('index.html')

# setup new route for delete and passing ID  to it
@app.route('/delete/<int:id>')
def delete(id):
    # get the task by id 
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    
# setup new route for update and passing ID to it 
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
    
        try:
            db.session.commit() 
            return redirect('/')
        except:
            return 'There was an issue updating you task'
    else:
        return render_template('update.html', task = task)


if __name__ == "__main__":
    # Keep debug=True give error if occur
    app.run(debug=True)

 