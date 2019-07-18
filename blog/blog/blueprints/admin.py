from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from flask_login import login_required

from blog import Category, db, Comment
from blog.forms import PostForm
from blog.models import Post
from blog.utils import redirect_back

admin_bp = Blueprint('admin', __name__)

#为所有视图添加登陆保护
@admin_bp.before_request
@login_required
def login_protect():
    pass

@admin_bp.route('/settings')
def settings():
    return render_template('admin/settings.html')


@admin_bp.route('/post/manage')
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).pageinate(
        page,per_page=current_app.config['BLUEBLOG_MANAGE_POST_PER_PAGE']
    )
    posts = pagination.items
    return render_template('admin/manage_post.html', pagination=pagination,posts=posts)

#创建文章
@admin_bp.route('/post/new', methos=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post=Post(title=title,body=body,category=category)
        db.session.add(post)
        db.session.commit()
        flash('文章已创建', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)

#编辑文章
@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('文章已更新', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html',form=form)

#删除文章
@admin_bp.route('/post/<int:post_id>/delete',methdos=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('已删除','success')
    return redirect_back()

#文章评论状态
@admin_bp.route('/set-comment/<int:post_id>')
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('已关闭评论','info')
    else:
        post.can_comment = True
        flash('已开启评论', 'info')
    db.session.commit()
    return redirect(url_for('blog.show_post', post_id=post_id))

#批准评论
@admin_bp.route('/comment/<int:comment_id>/approve')
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash('评论已审核', 'success')
    return redirect_back()

#筛选评论
@admin_bp.route('/comment/manage')
def manage_comment():
    filter_rule = request.args.get('filter', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    if filter_rule == 'unread':
        filtered_comments = Comment.query.filter_by(reviewed=False)
    elif filter_rule == 'admin':
        filtered_comments = Comment.query.filter_by(from_admin=True)
    else:
        filtered_comments = Comment.query
    pagination = filtered_comments.order_by(Comment.timestamp.desc()).paginate(page,per_page=per_page)
    comments = pagination.items
    return render_template('admin/manage_comment.html',comments=comments,pagination=pagination)


#分类管理
@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('无法删除默认分类','warning')
        return redirect_back(url_for('blog.index'))
    category.delete()
    flash('已删除分类','success')
    return redirect(url_for('.manage_category'))