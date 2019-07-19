import os

from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, send_from_directory
from flask_ckeditor import upload_fail, upload_success
from flask_login import login_required, current_user

from blog.forms import PostForm, CategoryForm, LinkForm, SettingForm
from blog.models import Post, Category, db, Comment, Link
from blog.utils import redirect_back, allowed_file

admin_bp = Blueprint('admin', __name__)

#为所有视图添加登陆保护
@admin_bp.before_request
@login_required
def login_protect():
    pass

@admin_bp.route('/settings')
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('已修改', 'success')
        return redirect(url_for('blog.index'))
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/post/manage')
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE']
    )
    posts = pagination.items
    return render_template('admin/manage_post.html', pagination=pagination,posts=posts, page=page)

#创建文章
@admin_bp.route('/post/new', methods=['GET', 'POST'])
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
@admin_bp.route('/post/<int:post_id>/delete',methods=['POST'])
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

@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('已删除评论', 'success')
    return redirect_back()


#分类管理
@admin_bp.route('/category/manage')
def manage_category():
    return render_template('admin/manage_category.html')

@admin_bp.route('/category/new', methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('已创建分类', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html', form=form)

@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('无法删除默认分类','warning')
        return redirect_back(url_for('blog.index'))
    category.delete()
    flash('已删除分类','success')
    return redirect(url_for('.manage_category'))

#链接管理
@admin_bp.route('/link/manage')
def manage_link():
    return render_template('admin/manage_link.html')

@admin_bp.route('/link/new', methods=['GET', 'POST'])
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        link = Link(name=name, url=url)
        db.session.add(link)
        db.session.commit()
        flash('已添加链接', 'success')
        return redirect(url_for('.manage_link'))
    return render_template('admin/new_link.html', form=form)


#ckeditor图片上传
@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['BLUBLOG_UPLOAD_PATH'], filename)

@admin_bp.route('/upload', methods=['POST'])
def upload_image():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('只允许图片')
    f.save(os.path.join(current_app.config['BLUELOG_UPLOAD_PATH'], f.filename))
    url = url_for('.get_image', filename=f.filename)
    return upload_success(url, f.filename)
