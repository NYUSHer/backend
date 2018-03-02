import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.test_basic import BasicTestCase
import json


# TODO: This test is not finished
class RegisterTestCase(BasicTestCase):

    def register(self, user_email, password, username):
        return self.client.post('/auth/register', data=dict(
            email=user_email,
            passwdtoken=password,
            username=username
        ), follow_redirects=True)

    def Register_login_success(self):
        rv = self.login('hl2752@nyu.edu', 'ec5e1e94c042dda33822701a45eb5e30', 'maxee')
        data = json.loads(rv.get_data().decode())
        print(data)
        assert data['state'] is True
        assert data['data']['userid'] is 1

    def test_login_fail(self):
        rv = self.login('john@gmail.com', 'e27bbaa25e61:c28d7a9a8d9fde8a82008d54b38dab981d6730be', 'john')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is False
        assert data['error']['errorCode'] == "002"
