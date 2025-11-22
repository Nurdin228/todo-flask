from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from models import Task, Tag, task_tags, db
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'moi-secret-key'


db.init_app(app)


with app.app_context():
    db.create_all()


# Главная страница
@app.route('/')
def index():
    status_filter = request.args.get('status')
    tag_filter = request.args.get('tag')

    query = Task.query
    if status_filter:
        query = query.filter(Task.status == status_filter)
    if tag_filter:
        query = query.filter(Task.tags.any(Tag.name == tag_filter))

    tasks = query.order_by(Task.created_at.desc()).all()
    tags = Tag.query.all()

    return render_template('index.html', 
                           tasks=tasks, 
                           tags=tags, 
                           current_status=status_filter, 
                           current_tag=tag_filter)


# Создание и обновление задач
@app.route('/task')
def create_task():
    title = request.form['title'].strip()
    description = request.form.get('description', '').strip()
    status = request.form.get('status', 'todo')
    priority = request.form.get('priority', 'medium')
    tag_names = request.form.getlist('tags')

    if not title:
        flash('Название обзательно!', 'danger')
        return redirect(url_for('index'))

    task = Task(title=title, description=description, status=status, priority=priority)
    if tag_names:
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if tag:
                task.tags.append()

    db.session.add(task)
    db.session.commit()
    flash('Задача создана', 'success')
    return redirect(url_for('index'))













if __name__ == '__main__.':
    app.run(debug=True)