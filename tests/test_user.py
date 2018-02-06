from tests.test_basic import BasicTestCase
import json


class LoginTestCase(BasicTestCase):

    def login(self, user_email, password):
        return self.client.post('/auth/login', data=dict(
            email=user_email,
            passwdtoken=password
        ), follow_redirects=True)

    def test_login_success(self):
        rv = self.login('masaki@gmail.com', 'e27bbaa25e61:c28d7a9a8d9fde8a82008d54b38dab981d6730be')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is True
        assert data['data']['userid'] is 1

    def test_login_fail(self):
        rv = self.login('john@gmail.com', 'e27bbaa25e61:c28d7a9a8d9fde8a82008d54b38dab981d6730be')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is False
        assert data['error']['errorCode'] == "001"

