from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

#initialize database
db = SQLAlchemy(app)

#create model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return "<Task %r>",self.id

@app.route('/', methods=["POST","GET"])
def home():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(task=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_added).all() #fetching all data
        return render_template('index.html', title="Todo App", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)