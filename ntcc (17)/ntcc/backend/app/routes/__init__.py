from flask import Flask, redirect, url_for, render_template, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import datetime
import os

# Initialize extensions globally
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "supersecretkey")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///foodshare.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "anothersecretkey")

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.donor import donor_bp
    from app.routes.recipient import recipient_bp
    from app.routes.claim import claim_bp
    from app.routes.food import food_bp
    from app.routes.map import map_bp
    from app.routes.notifications import notifications_bp
    from app.routes.api import api_bp 
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(donor_bp)
    app.register_blueprint(recipient_bp, url_prefix="/recipient")
    app.register_blueprint(claim_bp, url_prefix="/claim")
    app.register_blueprint(food_bp, url_prefix="/api/food")
    app.register_blueprint(map_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Automatically clear session if partially set
    @app.before_request
    def clear_session_if_invalid():
        if 'user_id' in session and not session.get('user_role'):
            print("⚠️ Clearing partial session (user_id set but no user_role)")
            session.clear()

    # Root route
    @app.route("/")
    def index():
        return render_template("index.html")

    # Inject current datetime into templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

    return app
