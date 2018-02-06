from tests.test_basic import BasicTestCase
import json


class LoginTestCase(BasicTestCase):

    def get_info(self, user_id, token):
        return self.client.post('/auth/authtest', headers=dict(userid=user_id, token=token),
                                follow_redirects=True)

    def test_get_info(self):
        rv = self.get_info(1, 'e27bbaa25e61:c28d7a9a8d9fde8a82008d54b38dab981d6730be')
        data = json.load(rv.get_data().decode())['data']
        assert data['email'] == 'masaki@gmail.com'
        assert data['imageuri'] is None
        assert data['motto'] is None
        assert data['username'] is 'masaki'
