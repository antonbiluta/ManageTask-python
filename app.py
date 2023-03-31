from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Task({self.id}, {self.title}, {self.description}, {self.completed})'


class TaskAPI(Resource):
    def delete(self, id):
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return '', 204
    

api.add_resource(TaskAPI, '/api/tasks/<int:id>')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        title = request.form['title']
        new_task = Task(title=title, description=title)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!')
        return redirect(url_for('tasks'))
    else:
        tasks = Task.query.all()
        return render_template('tasks.html', tasks=tasks)


@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        # description = request.form['description']
        task = Task(title=title)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks'))
    return render_template('create_task.html')


@app.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        # task.description = request.form['description']
        db.session.commit()
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', task=task)


@app.route('/tasks/<int:id>/delete', methods=['GET', 'POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
        return redirect(url_for('tasks'))
    return render_template('delete_task.html', task=task)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)