from flask_sqlalchemy import SQLAlchemy
from pathlib import Path


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
assets_folder = Path(__file__).parent.parent.parent / "assets"
