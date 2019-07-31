import os

from flask import render_template, Blueprint, request, current_app, send_from_directory, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from albumy.extentions import db
from albumy.forms.main import DescriptionForm, TagForm, CommentForm
from albumy.models import Photo, Tag, Comment, Collect
from albumy.decorators import confirm_required, permission_required
from albumy.utils import rename_image, resize_image, flash_errors


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/explore')
def explore():
    return render_template('main/explore.html')


@main_bp.route('/upload', methods=['GET','POST'])
@login_required                 #验证登陆状态
@confirm_required               #验证确认状态
@permission_required('UPLOAD')  #验证权限
def upload():
    # print(request.files)
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file')           #获取文件
        filename = rename_image(f.filename)     #生成随机文件名
        f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename))    #保存文件
        filename_s = resize_image(f, filename, current_app.config['ALBUMY_PHOTO_SIZE']['small'])
        filename_m = resize_image(f, filename, current_app.config['ALBUMY_PHOTO_SIZE']['medium'])
        photo = Photo(
            filename=filename,
            filename_s=filename_s,
            filename_m=filename_m,
            author=current_user._get_current_object()
        )
        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')


@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


@main_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['ALBUMY_UPLOAD_PATH'], filename)


@main_bp.route('/photo/<int:photo_id>')
def show_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(photo).order_by(Comment.timestamp.asc()).paginate(page, per_page)
    comments = pagination.items

    comment_form = CommentForm()
    description_form = DescriptionForm()
    tag_form = TagForm()

    description_form.description.data = photo.description
    return render_template('main/photo.html', photo=photo, description_form=description_form,
                           comment_form=comment_form,tag_form=tag_form,pagination=pagination,comments=comments)


@main_bp.route('/photo/n/<int:photo_id>')
def photo_next(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id<photo_id).order_by(Photo.id.desc()).first()
    if photo_n is None:
        flash('已经是最后一张图片啦！', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))

@main_bp.route('/photo/p/<int:photo_id>')
def photo_previous(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_p = Photo.query.with_parent(photo.author).filter(Photo.id>photo_id).order_by(Photo.id.asc()).first()
    if photo_p is None:
        flash('已经是第一张图片了！', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_p.id))

@main_bp.route('/delete/photo/<int:photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author:
        abort(403)
    db.session.delete(photo)
    db.session.commit()
    flash('已删除图片', 'info')

    #删除后返回下一张图片，没有则返回上一张，也没有则返回用户首页
    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id<photo_id).order_by(Photo.id.desc()).first()
    if photo_n is None:
        photo_p = Photo.query.with_parent(photo.author).filter(Photo.id>photo_id).order_by(Photo.id.asc()).first()
        if photo_p is None:
            return redirect(url_for('user.index', username=photo.author.username))
        return redirect(url_for('.show_photo', photo_id=photo_p.id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))


@main_bp.route('/report/photo/<int:photo_id>', methods=['POST'])
@login_required
@confirm_required
def report_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo.flag += 1
    db.session.commit()
    flash('已举报图片', 'success')
    return redirect(url_for('.show_photo', photo_id=photo.id))


@main_bp.route('/photo/<int:photo_id>/desription', methods=['POST'])
@login_required
def edit_description(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author:
        abort(403)
    form = DescriptionForm()
    if form.validate_on_submit():
        photo.description = form.description.data
        db.session.commit()
        flash('已更新图片描述', 'success')
    flash_errors(form)                              #flash表单的错误
    return redirect(url_for('.show_photo', photo_id=photo_id))

#标签
@main_bp.route('/photo/<int:photo_id>/tag/new', methods=['POST'])
@login_required
def new_tag(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author:
        abort(403)

    form = TagForm()
    if form.validate_on_submit():
        for name in form.tag.data.split():
            tag = Tag.query.filter_by(name=name).first()
            if tag is None:
                tag = Tag(name=name)
                db.session.add(tag)
                db.session.commit()
            if tag not in photo.tags:
                photo.tags.append(tag)
                db.session.commit()
        flash('已添加标签', 'success')
    flash_errors(form)
    return redirect(url_for('.show_photo', photo_id=photo_id))

@main_bp.route('/delete/tag/<int:photo_id>/<int:tag_id>', methods=['POST'])
@login_required
def delete_tag(photo_id, tag_id):
    tag = Tag.query.get_or_404(tag_id)
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author:
        abort(403)

    photo.tags.remove(tag)
    db.session.commit()

    if not tag.phots:
        db.session.delete(tag)
        db.session.commit()
    flash('已删除标签', 'info')
    return redirect(url_for('.show_photo', photo_id=photo_id))

@main_bp.route('/tag/<int:tag_id>', defaults={'order':'by_time'})
@main_bp.route('/tag/<int:tag_id>/<order>')
def show_tag(tag_id, order):
    tag = Tag.query.get_or_404(tag_id)

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    order_rule = 'time'
    pagination = Photo.query.with_parent(tag).order_by(Photo.timestamp.desc()).paginate(page, per_page)
    photos = pagination.items

    if order == 'by_collects':
        photos.sort(key=lambda x:len(x.collectors), reverse=True) #根据收藏数量
        order_rule = 'collects'
    return render_template('main/tag.html', tag=tag, pagination=pagination,photos=photos,order_rule=order_rule)


#评论
@main_bp.route('/report/comment/<int:comment_id>', methods=['POST'])
@login_required
@confirm_required
def report_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.flag += 1
    db.session.commit()
    flash('已举报评论', 'success')
    return redirect(url_for('.show_photo', photo_id=comment.photo_id))


@main_bp.route('/photo/<int:photo_id>/comment/new', methods=['POST'])
@login_required
@permission_required('COMMENT')
def new_comment(photo_id):
    photo = Photo.query.get_or_404(photo_id)

    page = request.args.get('page', 1, type=int)
    form = CommentForm()
    if form.validate_on_submit():
        body = form.body.data
        author = current_user._get_current_object()
        comment = Comment(body=body, author=author, photo=photo)

        print(request.args)
        replied_id = request.args.get('reply')
        print(replied_id)
        if replied_id:
            comment.replied = Comment.query.get_or_404(replied_id)
        db.session.add(comment)
        db.session.commit()
        flash('已评论', 'success')
    flash_errors(form)
    return redirect(url_for('.show_photo', photo_id=photo_id,page=page))


@main_bp.route('/set-comment/<int:photo_id>', methods=['POST'])
@login_required
def set_comment(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author:
        abort(403)

    if photo.can_comment:
        photo.can_comment = False
        flash('已禁止评论', 'info')
    else:
        photo.can_comment = True
        flash('可以评论', 'info')
    db.session.commit()
    return redirect(url_for('.show_photo', photo_id=photo_id))


@main_bp.route('/reply/comment/<int:comment_id>')
@login_required
@permission_required('COMMENT')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    # print(url_for('.show_photo', photo_id=comment.photo_id, reply=comment_id,author=comment.author.name, _external=True)+'#comment-form')
    return redirect(url_for('.show_photo', photo_id=comment.photo_id, reply=comment_id,author=comment.author.name)+'#comment-form')


@main_bp.route('/delete/comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if current_user != comment.author and current_user !=comment.photo.author:
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    flash('已删除评论', 'info')
    return redirect(url_for('.show_photo', photo_id=comment.photo_id))


#收藏
@main_bp.route('/collect/<int:photo_id>', methods=['POST'])
@login_required
@confirm_required
@permission_required('COLLECT')
def collect(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user.is_collecting(photo):
        flash('已经收藏过了', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    current_user.collect(photo)
    flash('已收藏', 'success')
    return redirect(url_for('.show_photo', photo_id=photo_id))

@main_bp.route('/uncollect/<int:photo_id>', methods=['POST'])
@login_required
def uncollect(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if not current_user.is_collecting(photo):
        flash('还没有收藏', 'info')
        return redirect(url_for('main.show_photo', photo_id=photo_id))
    current_user.uncollect(photo)
    flash('已取消收藏', 'info')
    return redirect(url_for('.show_photo', photo_id=photo_id))

@main_bp.route('/photo/<int:photo_id>/collectors')
def show_collectors(photo_id):
    photo = Photo.query.get_or_404(photo_id)

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_USER_PER_PAGE']
    pagination = Collect.query.with_parent(photo).order_by(Collect.timestamp.asc()).paginate(page,per_page)
    collects = pagination.items
    return render_template('main/collectors.html', collects=collects, photo=photo, pagination=pagination)