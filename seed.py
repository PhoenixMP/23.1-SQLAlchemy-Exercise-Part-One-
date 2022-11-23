"""Seed file to make sample data for user db."""

from models import User, db
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()
    User.query.delete()
    db.session.close()

# Add pets
user1 = User(first_name='Alan', last_name="Alda",
             image_url='https://img.freepik.com/free-photo/young-bearded-man-with-striped-shirt_273609-5677.jpg?size=626&ext=jpg')
user2 = User(first_name='Joel', last_name="Burton",
             image_url='https://cdn.pixabay.com/photo/2014/04/02/17/07/user-307993__340.png')
user3 = User(first_name='Jane', last_name="Smith")

# Add new objects to session, so they'll persist
with app.app_context():
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    db.session.close()
