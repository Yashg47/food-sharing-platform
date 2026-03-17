import random
from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request
from datetime import datetime
from sqlalchemy.orm import joinedload
from app import db
from app.models import FoodPost, Claim, DeliveryPartner, Notification, Commission

recipient_bp = Blueprint("recipient", __name__, template_folder="../templates")


# --------------------- Recipient Dashboard ---------------------
@recipient_bp.route("/dashboard")
def recipient_dashboard():

    if "user_id" not in session or session.get("user_role") != "recipient":
        flash("Please log in as a recipient.", "warning")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    claimed_items = (
        Claim.query
        .filter_by(recipient_id=user_id)
        .options(
            joinedload(Claim.food_item),
            joinedload(Claim.delivery_partner)
        )
        .order_by(Claim.claimed_at.desc())
        .all()
    )

    available_food = (
        FoodPost.query
        .filter(
            FoodPost.is_claimed == False,
            FoodPost.expiration_date >= datetime.utcnow()
        )
        .order_by(
            FoodPost.is_sponsored.desc(),
            FoodPost.created_at.desc()
        )
        .all()
    )

    serialized_food_items = [
        {
            "id": item.id,
            "name": item.name,
            "quantity": item.quantity,
            "location_name": item.location_name,
            "expiration_date": item.expiration_date.strftime('%Y-%m-%d'),
            "description": item.description,
            "created_at": item.created_at.strftime('%Y-%m-%d %H:%M'),
            "latitude": item.latitude,
            "longitude": item.longitude
        }
        for item in available_food
        if item.latitude and item.longitude
    ]

    return render_template(
        "recipient_dashboard.html",
        claimed_items=claimed_items,
        food_items=available_food,
        serialized_food_items=serialized_food_items
    )


# --------------------- Available Foods ---------------------
@recipient_bp.route("/available-foods")
def available_foods():

    if "user_id" not in session or session.get("user_role") != "recipient":
        flash("Login required.", "warning")
        return redirect(url_for("auth.login"))

    food_items = (
        FoodPost.query
        .filter(
            FoodPost.is_claimed == False,
            FoodPost.expiration_date >= datetime.utcnow()
        )
        .order_by(
            FoodPost.is_sponsored.desc(),
            FoodPost.created_at.desc()
        )
        .all()
    )

    return render_template("available_foods.html", food_items=food_items)


# --------------------- Claim Food ---------------------
@recipient_bp.route("/claim/<int:food_id>", methods=["POST"])
def claim_food(food_id):

    if "user_id" not in session or session.get("user_role") != "recipient":
        return jsonify({"success": False, "message": "Login required."}), 401

    user_id = session["user_id"]
    food_item = FoodPost.query.get(food_id)

    if not food_item:
        return jsonify({"success": False, "message": "Food not found."}), 404

    if food_item.is_claimed:
        return jsonify({"success": False, "message": "Already claimed."}), 400

    if food_item.expiration_date < datetime.utcnow():
        return jsonify({"success": False, "message": "Food expired."}), 400

    if food_item.donor_id == user_id:
        return jsonify({"success": False, "message": "Cannot claim own post."}), 403

    data = request.get_json(silent=True) or {}
    wants_delivery = data.get("wants_delivery", False)

    food_item.is_claimed = True

    claim = Claim(
        food_id=food_id,
        recipient_id=user_id,
        claimed_at=datetime.utcnow(),
        status="pending"
    )

    delivery_partner_info = None

    if wants_delivery:
        partners = DeliveryPartner.query.all()
        if partners:
            selected_partner = random.choice(partners)
            claim.delivery_partner = selected_partner

            delivery_partner_info = {
                "name": selected_partner.name,
                "phone": selected_partner.phone
            }

    # 🔔 Notification
    notification = Notification(
        user_id=food_item.donor_id,
        message=f"Your food item '{food_item.name}' has been claimed."
    )

    db.session.add(notification)

    # 💰 Commission
    if food_item.discounted_price:
        commission_amount = food_item.discounted_price * 0.10

        commission = Commission(
            food_id=food_item.id,
            business_id=food_item.donor_id,
            commission_amount=commission_amount
        )

        db.session.add(commission)

    db.session.add(claim)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Food claimed successfully!",
        "delivery_partner": delivery_partner_info
    })