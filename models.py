"""Models for Blogly."""


"""Demo file showing off a model for SQLAlchemy."""


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.String(2000),
                          nullable=False, default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"
