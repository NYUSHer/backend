from tests.test_basic import BasicTestCase
import json


class LoginTestCase(BasicTestCase):

    def login(self, user_email, password):
        return self.client.post('/auth/login', data=dict(
            email=user_email,
            passwdtoken=password
        ), follow_redirects=True)

    def check_email(self, user_email):
        return self.client.post('/auth/check', data=dict(
            email=user_email
        ), follow_redirects=True)

    def test_login_success(self):
        rv = self.login('hl2752@nyu.edu', '38db1d874425d645de1c30a8096c2eec')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is True
        assert data['data']['userid'] is 1

    def test_login_fail(self):
        rv = self.login('john@gmail.com', 'e27bbaa25e61:c28d7a9a8d9fde8a82008d54b38dab981d6730be')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is False
        assert data['error']['errorCode'] == "001"

    def test_email_check_success(self):
        rv = self.check_email('masaki@gmail.com')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is True

    def test_email_check_fail(self):
        rv = self.check_email('john@gmail.com')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is False



