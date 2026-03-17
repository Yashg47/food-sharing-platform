from flask import Blueprint, request, jsonify, session
from datetime import datetime
from app import db
from app.models import (
    Claim,
    FoodPost,
    DeliveryPartner,
    Notification,
    Commission
)
import random

claim_bp = Blueprint('claim', __name__)


# ---------------- Assign Delivery Partner ----------------
def assign_delivery_partner():
    partners = DeliveryPartner.query.all()
    if not partners:
        return None
    return random.choice(partners)


# ---------------- Claim Food ----------------
@claim_bp.route('/<int:food_id>', methods=['POST'])
def claim_food(food_id):

    user_id = session.get('user_id')
    user_role = session.get('user_role')

    if not user_id or user_role != 'recipient':
        return jsonify({
            'success': False,
            'message': 'Only recipients can claim food.'
        }), 403

    food_item = FoodPost.query.get(food_id)

    if not food_item:
        return jsonify({
            'success': False,
            'message': 'Food item not found.'
        }), 404

    # Already claimed
    if food_item.is_claimed:
        return jsonify({
            'success': False,
            'message': 'This food item has already been claimed.'
        }), 400

    # Expiry check
    if food_item.expiration_date < datetime.utcnow():
        return jsonify({
            'success': False,
            'message': 'This food item has expired.'
        }), 400

    # Own post check
    if food_item.donor_id == user_id:
        return jsonify({
            'success': False,
            'message': 'You cannot claim your own post.'
        }), 403

    # Delivery request
    data = request.get_json(silent=True) or {}
    wants_delivery = data.get('wants_delivery', False)

    delivery_partner = assign_delivery_partner() if wants_delivery else None

    # Delivery fee monetization
    delivery_fee = 50.0 if delivery_partner else None

    # Create claim
    claim = Claim(
        food_id=food_item.id,
        recipient_id=user_id,
        claimed_at=datetime.utcnow(),
        status='pending',
        delivery_partner_id=delivery_partner.id if delivery_partner else None,
        delivery_fee=delivery_fee
    )

    # Mark claimed
    food_item.is_claimed = True

    db.session.add(claim)

    # ---------------- Notification ----------------
    notification = Notification(
        user_id=food_item.donor_id,
        message=f"Your food item '{food_item.name}' has been claimed."
    )
    db.session.add(notification)

    # ---------------- Commission ----------------
    if food_item.discounted_price:
        commission_amount = food_item.discounted_price * 0.10

        commission = Commission(
            food_id=food_item.id,
            business_id=food_item.donor_id,
            commission_amount=commission_amount
        )

        db.session.add(commission)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Claim successful.',
        'delivery_partner': {
            'name': delivery_partner.name,
            'phone': delivery_partner.phone,
            'email': delivery_partner.email
        } if delivery_partner else None,
        'delivery_fee': delivery_fee
    })