
def test_login(app):
    app.session.Login(username="administrator", password="root")
    app.session.Logout()
    assert app.session.is_logged_in_as("administrator")