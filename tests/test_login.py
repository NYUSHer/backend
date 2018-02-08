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
        rv = self.login('hl2752@nyu.edu', 'ec5e1e94c042dda33822701a45eb5e30')
        data = json.loads(rv.get_data().decode())
        print(data)
        assert data['state'] is True
        assert data['data']['userid'] is 1

    def test_login_fail(self):
        rv = self.login('john@gmail.com', 'e27bbaa25e61:c28d7a9a8d9fde8a82008d54b38dab981d6730be')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is False
        assert data['error']['errorCode'] == "001"

    def test_login_fail_1(self):
        rv = self.login('zz1444@nyu.edu', '202cb962ac59075b964b07152d234b70')
        data = json.loads(rv.get_data().decode())
        print(data)
        assert data['state'] is False
        assert data['error']['errorCode'] == "102"

    def test_check_email(self):
        rv = self.check_email('zz1444@nyu.edu')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is True

    def test_check_email(self):
        rv = self.check_email('johnDoe@nyu.edu')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is False
