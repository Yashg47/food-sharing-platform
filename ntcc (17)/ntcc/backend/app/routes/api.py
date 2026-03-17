from flask import Blueprint, jsonify, request
from app.models import FoodPost
from datetime import datetime

api_bp = Blueprint("api", __name__)


# ---------------- Get Food Items API ----------------
@api_bp.route("/food-items")
def get_food_items():

    now = datetime.utcnow()

    location_query = request.args.get("location", "").lower()
    keyword_query = request.args.get("keyword", "").lower()
    expires_after = request.args.get("expires_after")

    base_query = (
        FoodPost.query
        .filter(
            FoodPost.is_claimed == False,
            FoodPost.is_expired == False,
            FoodPost.expiration_date > now,
            FoodPost.latitude.isnot(None),
            FoodPost.longitude.isnot(None)
        )
        .order_by(
            FoodPost.is_sponsored.desc(),   # 🔥 sponsored first
            FoodPost.created_at.desc()
        )
    )

    # Location filter
    if location_query:
        base_query = base_query.filter(
            FoodPost.location_name.ilike(f"%{location_query}%")
        )

    # Keyword search
    if keyword_query:
        base_query = base_query.filter(
            (FoodPost.name.ilike(f"%{keyword_query}%")) |
            (FoodPost.description.ilike(f"%{keyword_query}%"))
        )

    # Expiry filter
    if expires_after:
        try:
            expires_dt = datetime.strptime(expires_after, "%Y-%m-%d")
            base_query = base_query.filter(
                FoodPost.expiration_date >= expires_dt
            )
        except ValueError:
            pass

    food_items = base_query.all()

    result = []

    for item in food_items:
        result.append({
            "id": item.id,
            "name": item.name,
            "quantity": item.quantity,
            "location_name": item.location_name,
            "expiration_date": item.expiration_date.strftime('%Y-%m-%d %H:%M'),
            "description": item.description,
            "latitude": item.latitude,
            "longitude": item.longitude,

            # Monetization
            "original_price": item.original_price,
            "discounted_price": item.discounted_price,
            "is_sponsored": item.is_sponsored,

            # Donor info
            "donor": item.donor.username
        })

    return jsonify(result)