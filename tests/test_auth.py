from tests.test_basic import BasicTestCase
import json


class LoginTestCase(BasicTestCase):

    def auth(self, user_id, token):
        return self.client.post('/auth/authtest', headers=dict(userid=user_id, token=token),
        follow_redirects=True)

    def test_authentication_success(self):
        rv = self.auth(1, '1cdb1ca2-b81a-43c4-b51c-aec4fe2e9cce')
        data = rv.get_data().decode()
        assert data == 'hello'
