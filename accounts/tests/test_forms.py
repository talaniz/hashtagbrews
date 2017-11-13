from django.test import TestCase

from accounts.forms import LoginForm


class LoginFormTest(TestCase):
    """Test for all login related forms (registration not included)."""

    def test_login_form_returns_correct_elements(self):
        """`LoginForm` should return expected html names and ids."""

        form = LoginForm()

        form_elements = ['id="id_username"', 'id="id_password', 'class="form-control"']

        for element in form_elements:
            self.assertIn(element, form.as_p())

        username_html = 'input class="form-control" id="id_username" name="username" type="text"'
        password_html = 'input class="form-control" id="id_password" name="password" type="password"'

        self.assertIn(username_html, form.as_p())
        self.assertIn(password_html, form.as_p())
