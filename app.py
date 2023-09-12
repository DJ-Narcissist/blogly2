"""Blogly application."""

from flask import Flask, redirect, render_template, url_for, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'School'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
connect_db(app)
db,create_all()

@app.route('/')
def root():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return redirect('/users')

@app.route('/users')
def user_list():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user_list.html', users = users)

@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('new_user'))
    return render_template('user_new.html')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get(user_id)
    return render_template('user_detail.html', user=user)

@app.route('users/<int:user_id>/edit', methods=['GET','POST'])
def edit_user(user_id):
    user = User.query.get(user_id)

    if  request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_list'))
    
    return render_template('user_edit.html', user = user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('user_list'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
