import os

from flask import render_template, Blueprint, request, current_app
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