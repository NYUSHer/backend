import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.test_basic import BasicTestCase


class LoginTestCase(BasicTestCase):

    def auth(self, user_id, token):
        return self.client.post('/auth/authtest', headers=dict(userid=user_id, token=token),
        follow_redirects=True)

    def test_authentication_success(self):
        rv = self.auth(1, 'b8ef7162-9078-407f-ad97-b236afc9e11a')
        data = rv.get_data().decode()
        print(data)
        assert data == 'hello'

