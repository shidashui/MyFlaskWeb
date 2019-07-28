import os

from flask import render_template, Blueprint, request, current_app, send_from_directory, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from albumy.extentions import db
from albumy.models import Photo
from albumy.decorators import confirm_required, permission_required
from albumy.utils import rename_image, resize_image

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
    return render_template('main/photo.html', photo=photo)

@main_bp.route('/photo/n/<int:photo_id')
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
    photo_n = Photo.query.with_parent(photo.author).filter(Photo,id<photo_id).order_by(Photo.id.desc()).first()
    if photo_n is None:
        photo_p = Photo.query.with_parent(photo.author).filter(Photo.id>photo_id).order_by(Photo.id.asc()).first()
        if photo_p is None:
            return redirect(url_for('user.index', username=photo.author.username))
        return redirect(url_for('.show_photo', photo_id=photo_p.id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))