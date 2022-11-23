"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask,  request, render_template,  redirect, flash, session
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)


@app.route("/")
def home():
    """Redirect to list of users."""

    return redirect(f'/users')


@app.route("/users")
def list_users():
    """List users and show add user form."""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("list.html", users=users)


@app.route("/users/new")
def new_user_form():
    """Render form for creating a new user."""

    return render_template("add-user-form.html")


@app.route('/users/new', methods=["POST"])
def add_user():
    """Process the add form, adding a new user and going back to /users."""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]

    if len(image_url) > 0:
        new_user = User(first_name=first_name,
                        last_name=last_name, image_url=image_url)
    else:
        new_user = User(first_name=first_name,
                        last_name=last_name)

    db.session.add(new_user)
    db.session.commit()
    db.session.close()

    return redirect(f'/users')


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)

    return render_template("edit-user-form.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def commit_edit_user(user_id):
    """Process the edit form, returning the user to the /users page."""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name

    if len(image_url) > 0:
        user.image_url = image_url

    db.session.add(user)
    db.session.commit()
    db.session.close()

    return redirect(f'/users')


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete the user."""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    db.session.close()

    return redirect(f'/users')
