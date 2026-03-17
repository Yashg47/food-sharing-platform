from datetime import datetime
from app import db


# ---------------- USERS ----------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    role = db.Column(db.String(20), nullable=False)

    # Subscription
    subscription_plan = db.Column(db.String(20), default="free")
    subscription_expiry = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    food_posts = db.relationship("FoodPost", backref="donor", lazy=True)
    claims = db.relationship("Claim", backref="recipient", lazy=True)
    notifications = db.relationship("Notification", backref="user", lazy=True)
    subscription_payments = db.relationship(
        "SubscriptionPayment",
        backref="user",
        lazy=True
    )


# ---------------- FOOD POSTS ----------------
class FoodPost(db.Model):
    __tablename__ = "food_posts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    quantity = db.Column(db.String(50))

    location_name = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    expiration_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    is_claimed = db.Column(db.Boolean, default=False)
    is_expired = db.Column(db.Boolean, default=False)

    # Monetization
    original_price = db.Column(db.Float)
    discounted_price = db.Column(db.Float)
    is_sponsored = db.Column(db.Boolean, default=False)

    claims = db.relationship("Claim", backref="food_item", lazy=True)


# ---------------- DELIVERY PARTNERS ----------------
class DeliveryPartner(db.Model):
    __tablename__ = "delivery_partners"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    deliveries = db.relationship(
        "Claim",
        back_populates="delivery_partner",
        lazy=True
    )


# ---------------- CLAIMS ----------------
class Claim(db.Model):
    __tablename__ = "claims"

    id = db.Column(db.Integer, primary_key=True)

    food_id = db.Column(
        db.Integer,
        db.ForeignKey("food_posts.id"),
        nullable=False
    )

    recipient_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    claimed_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pending")

    delivery_partner_id = db.Column(
        db.Integer,
        db.ForeignKey("delivery_partners.id")
    )

    delivery_fee = db.Column(db.Float)

    delivery_partner = db.relationship(
        "DeliveryPartner",
        back_populates="deliveries"
    )


# ---------------- COMMISSION ----------------
class Commission(db.Model):
    __tablename__ = "commissions"

    id = db.Column(db.Integer, primary_key=True)

    food_id = db.Column(db.Integer, db.ForeignKey("food_posts.id"))
    business_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    commission_percentage = db.Column(db.Float, default=10.0)
    commission_amount = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    food = db.relationship("FoodPost", backref="commissions")
    business = db.relationship("User", backref="commissions")


# ---------------- SUBSCRIPTIONS ----------------
class SubscriptionPayment(db.Model):
    __tablename__ = "subscription_payments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    plan = db.Column(db.String(20))
    amount = db.Column(db.Float)

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)


# ---------------- CSR PARTNERS ----------------
class CSRPartner(db.Model):
    __tablename__ = "csr_partners"

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float)

    meals_sponsored = db.Column(db.Integer)
    co2_reduced = db.Column(db.Float)

    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- ANALYTICS ----------------
class AnalyticsSnapshot(db.Model):
    __tablename__ = "analytics_snapshots"

    id = db.Column(db.Integer, primary_key=True)

    total_food_listed = db.Column(db.Integer)
    total_food_claimed = db.Column(db.Integer)
    total_commission_earned = db.Column(db.Float)

    generated_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- NOTIFICATIONS ----------------
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)