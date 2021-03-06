from django.test import TestCase

from accounts.forms import LoginForm, RegisterForm


class LoginFormTest(TestCase):
    """Test for all login related forms (registration not included)."""

    def test_login_form_returns_correct_elements(self):
        """`LoginForm` should return expected html names and ids."""

        form = LoginForm()

        form_elements = ['id="id_username"', 'id="id_password', 'class="form-control"']

        for element in form_elements:
            self.assertIn(element, form.as_p())

        username_html = 'id="id_username"'
        password_html = 'id="id_password"'

        self.assertIn(username_html, form.as_p())
        self.assertIn(password_html, form.as_p())

class RegisterFormTest(TestCase):
    """Test for all registration related forms."""

    def test_registration_form_returns_correct_elements(self):
        """`RegisterForm` should return expected html names and ids."""

        form = RegisterForm()

        form_elements = ['id="id_username"', 'id="id_password',
                         'id="id_password1', 'id="id_password2',
                         'class="form-control"', 'id="id_email"']

        for element in form_elements:
            self.assertIn(element, form.as_p())
