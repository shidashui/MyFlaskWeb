from flask import Blueprint, render_template

from albumy.models import User

user_bp = Blueprint('user',__name__)


@user_bp.route('/<username>')
def index(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user/index.html', user=user)