from tests.test_basic import BasicTestCase
import json


class LoginTestCase(BasicTestCase):

    def auth(self, user_id, token):
        return self.client.post('/auth/authtest', headers=dict(userid=user_id, token=token),
        follow_redirects=True)

    def test_authentication_success(self):
        rv = self.auth(1, 'eb0df5ff-dcfb-497c-a396-cf3cf4f13a78')
        data = rv.get_data().decode()
        assert data == 'hello'
