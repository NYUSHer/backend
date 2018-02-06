from tests.test_basic import BasicTestCase
import json


class LoginTestCase(BasicTestCase):

    def auth(self, user_id, token):
        return self.client.post('/auth/authtest', headers=dict(userid=user_id, token=token),
        follow_redirects=True)

    def test_authentication_success(self):
        rv = self.auth(1, '07c2cb31-6b5e-4438-bccf-7c97752d1573')
        data = rv.get_data().decode()
        print(data)
        assert data == 'hello'
