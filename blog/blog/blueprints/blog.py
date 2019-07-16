from flask import render_template, Blueprint, request, current_app

from blog.models import Post

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    #分页处理
    page = request.args.get('page',1,type=int) # 从查询字符串获取当前页数
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']  #每页数量
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html',pagination=pagination,posts=posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/category.html')


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    return render_template('blog/post.html')

