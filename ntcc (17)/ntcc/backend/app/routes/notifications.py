from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from app.models import Notification
from app import db

notifications_bp = Blueprint('notifications', __name__)


# ---------------- Show Notifications Page ----------------
@notifications_bp.route('/notifications')
def show_notifications():

    user_id = session.get('user_id')

    if not user_id:
        flash('Please log in to view notifications.', 'warning')
        return redirect(url_for('auth.login'))

    notifications = (
        Notification.query
        .filter_by(user_id=user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return render_template(
        'notifications.html',
        notifications=notifications
    )


# ---------------- Notification Count API ----------------
@notifications_bp.route('/api/notifications/count')
def notification_count():

    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"count": 0})

    count = Notification.query.filter_by(user_id=user_id).count()

    return jsonify({"count": count})