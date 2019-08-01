from flask import Blueprint, render_template, jsonify
from flask_login import current_user

from albumy.models import User,Notification
from albumy.notifications import push_follow_notification

ajax_bp = Blueprint('ajax', __name__)


@ajax_bp.route('/profile/<int:user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('main/profile_popup.html', user=user)

@ajax_bp.route('/followers-count/<int:user_id>')
def followers_count(user_id):
    user = User.query.get_or_404(user_id)
    count = user.followers.count() - 1
    return jsonify(count=count)


@ajax_bp.route('/unfollow/<username>', methods=['GET','POST'])
def unfollow(username):
    print('------------------------------有请求来')
    if not current_user.is_authenticated:
        return jsonify(message='需要登陆'), 403

    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.is_following(user):
        return jsonify(message='还没有关注'), 400

    current_user.unfollow(user)
    return jsonify(message='已取消关注')


@ajax_bp.route('/follow/<username>', methods=['POST'])
def follow(username):
    print('------------------------------有请求来')
    if not current_user.is_authenticated:
        return jsonify(message='需要登陆'), 403
    if not current_user.confirmed:
        return jsonify(message='需要验证账号'), 400
    if not current_user.can('FOLLOW'):
        return jsonify(message='没有权限'), 403

    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_following(user):
        return jsonify(message='已经关注'), 400

    current_user.follow(user)
    push_follow_notification(follower=current_user, receiver=user)
    return jsonify(message='已关注')


#消息提醒
@ajax_bp.route('/notifications-count')
def notifications_count():
    if not current_user.is_authenticated:
        return jsonify(message='需要登陆'), 403

    count = Notification.query.with_parent(current_user).filter_by(is_read=False).count()
    return jsonify(count=count)