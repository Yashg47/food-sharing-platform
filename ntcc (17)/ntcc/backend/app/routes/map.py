from flask import Blueprint, render_template, session, redirect, url_for, flash

map_bp = Blueprint('map', __name__)

@map_bp.route('/map')
def show_map():

    if "user_id" not in session:
        flash("Please log in to access the map.", "warning")
        return redirect(url_for("auth.login"))

    return render_template('map.html')