from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import FoodPost
from app import db
from datetime import datetime

donor_bp = Blueprint("donor", __name__)

# ----------------------- Donor Dashboard -----------------------
@donor_bp.route("/dashboard")
def donor_dashboard():
    if "user_id" not in session or session.get("user_role") != "donor":
        flash("Please log in as a donor to access the dashboard.", "warning")
        return redirect(url_for("auth.login"))

    donor_id = session["user_id"]
    food_items = FoodPost.query.filter_by(donor_id=donor_id).order_by(FoodPost.created_at.desc()).all()

    # ✅ Prepare serialized data for map rendering
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
        for item in food_items if item.latitude is not None and item.longitude is not None
    ]

    return render_template(
        "donor_dashboard.html",
        food_items=food_items,
        serialized_food_items=serialized_food_items  # ✅ map markers
    )

# ------------------------ Post New Food ------------------------
@donor_bp.route("/post", methods=["GET", "POST"])
def post_food():
    if "user_id" not in session or session.get("user_role") != "donor":
        flash("Please log in as a donor to post food.", "warning")
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        name = request.form["name"]
        quantity = request.form["quantity"]
        location = request.form["location_name"]
        expiration_date = request.form["expiration_date"]
        description = request.form.get("description", "")

        # Coordinates
        lat = request.form.get("latitude")
        lng = request.form.get("longitude")

        lat = float(lat) if lat else None
        lng = float(lng) if lng else None

        # Monetization fields
        original_price = request.form.get("original_price")
        discounted_price = request.form.get("discounted_price")
        is_sponsored = True if request.form.get("is_sponsored") else False

        try:
            expiration = datetime.strptime(expiration_date, "%Y-%m-%d")
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("donor.post_food"))

        new_post = FoodPost(
            donor_id=session["user_id"],
            name=name,
            quantity=quantity,
            location_name=location,
            expiration_date=expiration,
            description=description,
            latitude=lat,
            longitude=lng,
            original_price=float(original_price) if original_price else None,
            discounted_price=float(discounted_price) if discounted_price else None,
            is_sponsored=is_sponsored
        )

        db.session.add(new_post)
        db.session.commit()

        flash("Food item posted successfully!", "success")
        return redirect(url_for("donor.donor_dashboard"))

    return render_template("post_food.html")