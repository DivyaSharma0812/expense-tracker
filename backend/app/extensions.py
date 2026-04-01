from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

database = SQLAlchemy()
marshmallow_extension = Marshmallow()
cors = CORS()
