from elo_rank import db, assets_folder
from elo_rank.controllers import auth_blueprint, main_blueprint, user_blueprint, stats_blueprint
from flask import Flask
from flask_login import LoginManager
from elo_rank.models.users import User


def create_app():
    app = Flask(__name__, template_folder=assets_folder / "templates")

    # Please setup (at least) the following environment variables:
    #  - FLASK_SECRET_KEY
    #  - SQLALCHEMY_DATABASE_URI
    app.config.from_prefixed_env()

    db.init_app(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(stats_blueprint)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.display_login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: int) -> User:
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app


def launch():
    app = create_app()
    app.run()


if __name__ == "__main__":
    launch()
