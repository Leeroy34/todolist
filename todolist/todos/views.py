from flask import render_template, flash, redirect, url_for, request, jsonify, Response, session, Blueprint, abort
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime

from todolist.models import User, Todo
from todolist import db

todos = Blueprint('todos', __name__)


@todos.route('/todo/<username>', methods=['GET', 'POST'])
@login_required
def todo(username):
    user = User.query.filter_by(username=username).first()
    if current_user != user:
        abort(403)
    if user:
        incomplete = Todo.query.filter_by(complete=False, user_id=user.id).all()
        complete = Todo.query.filter_by(complete=True, user_id=user.id).all()
    return render_template('todo.html', username=username, incomplete=incomplete, complete=complete)
    


@todos.route('/add/<username>', methods=['GET','POST'])
@login_required
def add(username):
    user = User.query.filter_by(username=username).first()
    if user:
        todo = Todo(text=request.form['todoitem'], complete=False, user_id = user.id)
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for('todos.todo', username=username))


@todos.route('/complete/<username>/<id>')
@login_required
def complete(username, id):
    
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('todos.todo', username=username))


@todos.route('/delete/<username>/<id>')
@login_required
def delete(username, id):
    user = User.query.filter_by(username=username).first()
    if user:
        todo = Todo.query.filter_by(id=int(id)).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('todos.todo', username=username,))