from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from app import db  # ✅ correct import
from app.models import FoodPost, Claim  # ✅ also import Claim for claimed_items()

food_bp = Blueprint("food", __name__, template_folder="../templates")


# -------------------------------
# View All Available Food Items (for recipients)
# -------------------------------
@food_bp.route("/available")
def available_food():
    if "user_id" not in session or session.get("user_role") != "recipient":
        flash("Please log in as a recipient to view available food.", "warning")
        return redirect(url_for("auth.login"))

    now = datetime.utcnow()
    food_items = FoodPost.query.filter(
        FoodPost.is_claimed == False,
        FoodPost.is_expired == False,
        FoodPost.expiration_date > now
    ).order_by(FoodPost.expiration_date).all()

    return render_template("available_food.html", food_items=food_items)


# -------------------------------
# Expire Old Food Items (can be called by cron or manually)
# -------------------------------
@food_bp.route("/expire-check", methods=["POST"])
def expire_old_posts():
    now = datetime.utcnow()
    expired_items = FoodPost.query.filter(
        FoodPost.expiration_date < now,
        FoodPost.is_expired == False
    ).all()

    for item in expired_items:
        item.is_expired = True

    db.session.commit()
    return f"{len(expired_items)} food items marked as expired.", 200


# -------------------------------
# Recipient's Claimed Items View
# -------------------------------
@food_bp.route("/claimed")
def claimed_items():
    if "user_id" not in session or session.get("user_role") != "recipient":
        flash("Please log in as a recipient to view your claimed items.", "warning")
        return redirect(url_for("auth.login"))

    recipient_id = session["user_id"]

    # Get all claims by this recipient and extract the food items
    claims = Claim.query.filter_by(recipient_id=recipient_id).join(FoodPost).all()

    # Extract associated food items
    claimed_food_items = [claim.food_item for claim in claims]

    return render_template("claimed_items.html", claimed_items=claimed_food_items)
