from flask import Flask
from config import Config
from models import db
from routes.books import books_bp
from flask_migrate import Migrate
from routes.reservations import reservations_bp
from routes.borrowings import borrowings_bp
from routes.users import users_bp
from routes.notifications import notifications_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

app.register_blueprint(books_bp)
app.register_blueprint(reservations_bp)
app.register_blueprint(borrowings_bp)
app.register_blueprint(users_bp)
app.register_blueprint(notifications_bp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)