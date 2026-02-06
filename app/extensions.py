from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

jwt = JWTManager()
bcrypt = Bcrypt()
db=SQLAlchemy()
migrate=Migrate()
jwt_blacklist = set()
