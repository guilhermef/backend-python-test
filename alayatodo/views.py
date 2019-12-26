import functools

from flask import (
    current_app,
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    )

from alayatodo.models import User, Todo
from alayatodo import db


bp = Blueprint("routes", __name__)

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("routes.login"))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""

    user_id = session.get("user_id")
    g.user = User.query.get(user_id) if user_id is not None else None

@bp.route('/')
def home():
    with current_app.open_resource('../README.md', mode='r') as readme:
        return render_template('index.html', readme=readme.read())


@bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@bp.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user_id'] = user.id
        return redirect('/todo')

    return redirect('/login')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@bp.route('/todo/<id>/json', methods=['GET'])
@bp.route('/todo/<id>', methods=['GET'])
@login_required
def todo(id):
    todo = Todo.query.filter_by(user=g.user, id=id).one()
    if request.url.endswith("/json"):
        return todo.as_dict()
    return render_template('todo.html', todo=todo)


@bp.route('/todo', methods=['GET'])
@bp.route('/todo/', methods=['GET'])
@login_required
def todos():
    pagination = Todo.query.filter_by(user=g.user).paginate(
        page=int(request.args.get('page', '1')),
        per_page=5,
    )
    return render_template('todos.html', pagination=pagination)


@bp.route('/todo', methods=['POST'])
@bp.route('/todo/', methods=['POST'])
@login_required
def todos_POST():
    g.user.todos.append(Todo(description=request.form.get('description')))
    db.session.commit()
    flash(f"Todo {request.form.get('description')} added!")
    return redirect('/todo')


@bp.route('/todo/<id>/delete', methods=['POST'])
@login_required
def todo_delete(id):
    todo = Todo.query.filter_by(user=g.user, id=id).delete()
    db.session.commit()
    flash(f"Todo {id} deleted!")
    return redirect('/todo')

@bp.route('/todo/<id>/complete', methods=['POST'])
@login_required
def todo_complete(id):
    todo = Todo.query.filter_by(user=g.user, id=id).one()
    todo.completed = True
    db.session.commit()
    flash(f"Todo {id} marked as complete!")
    return redirect('/todo')
