from flask import Blueprint, render_template, redirect, url_for, request, current_app, abort
from flask_login import login_required, current_user
from flask_socketio import emit

from catchat.extensions import db, socketio
from catchat.forms import ProfileForm
from catchat.models import Message, User
from catchat.utils import flash_errors, to_html

chat_bp = Blueprint('chat', __name__)


online_users = []  #存储在线用户id


@chat_bp.route('/')
def home():
    amount = current_app.config['CATCHAT_MESSAGE_PER_PAGE']
    messages = Message.query.order_by(Message.timestamp.asc())[-amount:]
    user_amount = User.query.count()
    return render_template('chat/home.html', messages=messages, user_amount=user_amount)


@chat_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.github = form.github.data
        current_user.website = form.website.data
        current_user.bio = form.bio.data
        db.session.commit()
        return redirect(url_for('.home'))
    flash_errors(form)
    return render_template('chat/profile.html', form=form)


@chat_bp.route('/profile/<user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('chat/_profile_card.html', user=user)


@chat_bp.route('/anonymous')
def anonymous():
    return render_template('chat/anonymous.html')


@chat_bp.route('/messages')
def get_messages():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['CATCHAT_MESSAGE_PER_PAGE']
    pagination = Message.query.order_by(Message.timestamp.desc()).paginate(page,per_page)
    messages = pagination.items
    return render_template('chat/_messages.html', messages=messages[::-1])


@chat_bp.route('/message/delete/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if current_user != message.author and not current_user.is_admin:
        abort(403)
    db.session.delete(message)
    db.session.commit()
    return '', 204



@socketio.on('new message')
def new_message(message_body):
    # print(message_body)
    # print(online_users)
    html_message = to_html(message_body)
    message = Message(author=current_user._get_current_object(), body=html_message)
    db.session.add(message)
    db.session.commit()
    emit('new message',
         {'message_html': render_template('chat/_message.html', message=message),
          'message_body': html_message,
          'gravatar': current_user.gravatar,
          'nickname': current_user.nickname,
          'user_id': current_user.id},
         broadcast=True)


@socketio.on('new message', namespace='/anonymous')
def new_anonymous_message(message_body):
    html_message = to_html(message_body)
    avatar = 'https//www.gravatar.com/avatar?d=mm'
    nickname = '匿名用户'
    emit('new message',
         {'message_html': render_template('chat/_anonymous_message.html',
                                          message=html_message,
                                          avatar=avatar,
                                          nickname=nickname),
        'message_body': html_message,
        'gravatar': avatar,
        'nickname': nickname,
        'user_id': current_user.id},
        broadcast = True, namespace = '/anonymous')


#在线人数统计，通过connect和disconect事件
@socketio.on('connect')
def connect():
    global online_users
    # print(online_users)
    if current_user.is_authenticated and current_user.id not in online_users:
        online_users.append(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    global online_users
    if current_user.is_authenticated and current_user.id in online_users:
        online_users.remove(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


