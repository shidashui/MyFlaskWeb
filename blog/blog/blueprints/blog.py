from flask import render_template, Blueprint

blog_dp = Blueprint('blog', __name__)


@blog_dp.route('/')
def index():
    return render_template('blog/index.html')


@blog_dp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_dp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/category.html')


@blog_dp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    return render_template('blog/post.html')

