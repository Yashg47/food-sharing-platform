from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import (
    DeliveryPartner,
    Claim,
    CSRPartner,
    AnalyticsSnapshot
)

admin_bp = Blueprint("admin", __name__, template_folder="../templates")


# ---------------- Admin Auth Check ----------------
def admin_required():
    return (
        "user_id" in session and
        session.get("user_role") == "admin"
    )


# ---------------- Add Delivery Partner ----------------
@admin_bp.route("/add-partner", methods=["GET", "POST"])
def add_partner():

    if not admin_required():
        flash("Admin access required.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")

        existing = DeliveryPartner.query.filter_by(email=email).first()
        if existing:
            flash("Partner with this email already exists.", "danger")
            return redirect(url_for("admin.add_partner"))

        new_partner = DeliveryPartner(
            name=name,
            email=email,
            phone=phone
        )

        try:
            db.session.add(new_partner)
            db.session.commit()
            flash("Delivery Partner added successfully!", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Email must be unique.", "danger")

        return redirect(url_for("admin.add_partner"))

    partners = DeliveryPartner.query.order_by(
        DeliveryPartner.name
    ).all()

    return render_template(
        "add_partner.html",
        partners=partners
    )


# ---------------- Assign Partner ----------------
@admin_bp.route("/assign-partner", methods=["GET", "POST"])
def assign_partner():

    if not admin_required():
        flash("Admin access required.", "danger")
        return redirect(url_for("auth.login"))

    claims = Claim.query.filter(
        Claim.delivery_partner_id == None
    ).all()

    partners = DeliveryPartner.query.all()

    if request.method == "POST":

        claim_id = request.form["claim_id"]
        partner_id = request.form["partner_id"]

        claim = Claim.query.get(claim_id)
        partner = DeliveryPartner.query.get(partner_id)

        if claim and partner:
            claim.delivery_partner = partner
            db.session.commit()
            flash("Partner assigned successfully!", "success")
        else:
            flash("Invalid selection.", "danger")

        return redirect(url_for("admin.assign_partner"))

    return render_template(
        "assign_partner.html",
        claims=claims,
        partners=partners
    )


# ---------------- CSR Partners ----------------
@admin_bp.route("/csr-partners")
def csr_partners():

    if not admin_required():
        flash("Admin access required.", "danger")
        return redirect(url_for("auth.login"))

    partners = CSRPartner.query.all()

    return render_template(
        "csr_partners.html",
        partners=partners
    )


# ---------------- Analytics Dashboard ----------------
@admin_bp.route("/analytics")
def analytics_dashboard():

    if not admin_required():
        flash("Admin access required.", "danger")
        return redirect(url_for("auth.login"))

    snapshots = AnalyticsSnapshot.query.order_by(
        AnalyticsSnapshot.generated_at.desc()
    ).all()

    return render_template(
        "analytics.html",
        snapshots=snapshots
    )