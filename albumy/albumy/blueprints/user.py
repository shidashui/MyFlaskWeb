from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from flask_login import login_required, current_user

from albumy.decorators import confirm_required, permission_required
from albumy.models import User, Photo, Collect
from albumy.notifications import push_follow_notification
from albumy.utils import redirect_back

user_bp = Blueprint('user',__name__)


@user_bp.route('/<username>')
def index(username):
    user = User.query.filter_by(username=username).first_or_404()

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    pagination = Photo.query.with_parent(user).order_by(Photo.timestamp.desc()).paginate(page,per_page)
    photos = pagination.items

    return render_template('user/index.html', user=user, pagination=pagination, photos=photos)


@user_bp.route('/<username>/collections')
def show_collections(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    pagination = Collect.query.with_parent(user).order_by(Collect.timestamp.desc()).paginate(page, per_page)
    collects = pagination.items
    return render_template('user/collections.html', user=user, pagination=pagination, collects=collects)


#关注视图
@user_bp.route('/follow/<username>',methods=['POST'])
@login_required
@confirm_required
@permission_required('FOLLOW')
def follow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_following(user):
        flash('已关注', 'info')
        return redirect(url_for('.index', usernam=username))

    current_user.follow(user)
    push_follow_notification(follower=current_user,receiver=user)
    flash('已关注', 'success')
    return redirect_back()

@user_bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.is_following(user):
       flash('还没有关注', 'info')
       return redirect(url_for('.index', username=username))
    current_user.unfollow(user)
    flash('已取消关注','info')
    return redirect_back()

@user_bp.route('/<username>/followers')
def show_followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_USER_PER_PAGE']
    pagination = user.followers.paginate(page, per_page)
    follows = pagination.items
    return render_template('user/followers.html', user=user, pagination=pagination, follows=follows)

@user_bp.route('/<username>/following')
def show_following(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_USER_PER_PAGE']
    pagination = user.following.paginate(page, per_page)
    follows = pagination.items
    return render_template('user/following.html', pagination=pagination,user=user,follows=follows)

