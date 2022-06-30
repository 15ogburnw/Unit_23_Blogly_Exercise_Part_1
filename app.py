"""Blogly application."""

from email.mime import image
import re
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def redirect_to_users():

    return redirect('/users')


@app.route('/users')
def show_users():
    """Renders the a page with a list of all users"""

    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Renders the details page for the user, given a user id"""

    user = User.query.get_or_404(user_id)

    return render_template('user_details.html', user=user)


@app.route('/users/new')
def new_user_form():
    """Renders the new user form page"""

    return render_template('new_user.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """Takes data from the new user form and adds the user to the database, then redirects the user to the user list page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    # If no first or last name are entered, the user is redirected back to the same page with an alert message flashed on the screen

    if not first_name or not last_name:
        flash('You must enter a first and last name!')
        return redirect('/users/new')

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Renders the edit user form with prepopulated fields, given a user id"""

    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Takes data from the edit user form and updates the user info in the database"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    # If no first or last name are entered, the user is redirected back to the same page with an alert message flashed on the screen

    if not first_name or not last_name:
        flash('You must enter a first and last name!')
        return redirect(f'/users/{user_id}/edit')

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes a user from the database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
