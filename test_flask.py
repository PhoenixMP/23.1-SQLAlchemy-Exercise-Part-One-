from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""
        with app.app_context():
            User.query.delete()

            user = User(first_name="TestMan", last_name="Him",
                        )
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id
            self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        """Test that the list_users routes successfully to the list.html file with the correct html"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestMan', html)

    def test_show_user(self):
        """Test that the show_user routes successfully to the detail.html file with the correct html"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestMan Him', html)
            self.assertIn(
                "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png", html)

    def test_add_user(self):
        """Test that after submitting the form with new user information, the page correctly redirects to the list_user directory 
        and the new user is displayed on the page"""
        with app.test_client() as client:
            d = {"first-name": "TestWoman", "last-name": "her",
                 "image-url": "https://media.istockphoto.com/id/1369508766/photo/beautiful-successful-latin-woman-smiling.jpg?b=1&s=170667a&w=0&k=20&c=owOOPDbI6VOp1xYA4smdTNSHxjcJGRtGfVXx24g6J4c="}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestWoman", html)

    def test_delete_user(self):
        """Test that after submitting the form to delete a user, the page correctly redirects to the list_user directory 
        and the new user is no longer displayed on the page"""
        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<ul>\n    \n</ul>", html)
