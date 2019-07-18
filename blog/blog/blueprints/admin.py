from flask import Blueprint, render_template
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/settings')
@login_required
def settings():
    return render_template('admin/settings.html')


