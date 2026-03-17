# app/routes/seed_delivery_partners.py

from app import create_app, db
from app.models import DeliveryPartner

app = create_app()

dummy_partners = [
    {"name": "Akash Singh", "email": "akash@example.com", "phone": "9876543210"},
    {"name": "Priya Mehta", "email": "priya@example.com", "phone": "9123456780"},
    {"name": "Rahul Sharma", "email": "rahul@example.com", "phone": "9988776655"},
    {"name": "Neha Verma", "email": "neha@example.com", "phone": "9765432109"},
    {"name": "Deepak Rao", "email": "deepak@example.com", "phone": "9871234567"},
]

with app.app_context():
    for partner in dummy_partners:
        existing = DeliveryPartner.query.filter_by(email=partner["email"]).first()
        if not existing:
            new_partner = DeliveryPartner(
                name=partner["name"],
                email=partner["email"],
                phone=partner["phone"]
            )
            db.session.add(new_partner)
    db.session.commit()
    print("✅ Dummy delivery partners added.")
