"""Blogly application."""

from flask import Flask, redirect, render_template, url_for,flash,request
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


@app.route('/')
def root():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('/posts/homepage.html', posts = posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 error page"""
    return render_template('404.html')

#### USERS #####
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
    flash(f"User {user.full_name} edited.")
    return render_template('user_edit.html', user = user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")
    return redirect(url_for('user_list'))

##### POSTS ######


@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    "Show form to create new posts for user"
    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html' user = user)

@app.route('/users/<int:user_id>/posts/new', methods = ["POST"])
def posts_new(user_id):
    """Handle form submission for new posts from user"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title = request.form['title'],
                    content =request.form['content'],
                    user = user)
    
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info for post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods = ["POST"])
def posts_update(post_id):
    """Handle form submission to update a post"""
    post = Post.query_or_get_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.") 

    return redirect(f"/users/post {post.uer_id}")

@app.route('/posts/<int:post_id>/delete', methods = ["POST"])
def post_delete(post_id):
    """Handle Form submission to delete a post"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted.")

    return redirect(f"/users/post {post.user_id}")
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
