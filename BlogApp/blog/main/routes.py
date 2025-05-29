from flask import render_template, request, Blueprint
from blog.models import Post

main = Blueprint('main', __name__)



# Pagination
# posts.items → A list of posts on the current page.
# posts.page → The current page number.
# posts.per_page → The number of items per page.
# posts.total → Total number of posts in the database.
# posts.pages → Total number of pages.
# posts.has_next → True if there's a next page.
# posts.has_prev → True if there's a previous page.

@main.route('/')
@main.route('/home')
def home_page():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', title="Home", posts=posts)


@main.route('/about')
def about_page():
    return render_template('about.html', title="About")