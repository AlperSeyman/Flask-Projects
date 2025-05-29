from flask import render_template,url_for, flash, redirect, request, abort, Blueprint
from blog import db
from blog.models import Post
from blog.posts.forms import PostForm
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)



# Create Post
@posts.route('/post/new', methods=['POST', 'GET'])
@login_required
def createPost_page():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data, content=post_form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has created!", category="success")
        return redirect(url_for('main.home_page'))
    return render_template("create_post.html", title="New Post", post_form=post_form, legend='New Post')


# Get Post by user id
@posts.route('/post/<int:post_id>')
def post_page(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)



# Update Post
@posts.route('/post/<int:post_id>/update', methods=['POST','GET'])
@login_required
def updatePost_page(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    update_form = PostForm()
    if update_form.validate_on_submit():
        post.title = update_form.title.data
        post.content = update_form.content.data
        db.session.commit()
        flash("Your post has updated!", category="success")
        return redirect(url_for('posts.post_page', post_id=post.id))
    elif request.method == "GET":
        update_form.title.data = post.title
        update_form.content.data = post.content
    return render_template('create_post.html', title="Update Post", post_form=update_form, legend='Update Post')

# Deleting Post
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def deletePost_page(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has deleted!", category="success")
    return redirect(url_for('main.home_page'))