from flask import render_template, Blueprint, request, current_app, url_for, flash, redirect
from flask_login import current_user

from blog import Category, db
from blog.emails import send_new_comment_email
from blog.forms import AdminCommentForm, CommentForm
from blog.models import Post, Comment

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
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page,per_page=per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category,pagination=pagination,posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id) #没有找到返回404
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(page,per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLUELOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.site.data
        comment = Comment(
            author=author,email=email,site=site,body=body,
            from_admin=from_admin,post=post,reviewed=reviewed
        )
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            # send_new_comment_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('评论完成','success')
        else:
            flash('谢谢评论，稍后审核', 'info')
            # send_new_comment_email(post)
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post,pagination=pagination,comments=comments,form=form)

# @blog_bp.route('/post/<slug>')
# def show_post(slug):
#     post = Post.query.filter_by(slug=slug).first_or_404()
#     return render_template('post.html', post=post)

@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('.show_post', post_id=comment.post_id,reply=comment_id,author=comment.author)+'#comment-form')