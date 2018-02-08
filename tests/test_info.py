from tests.test_basic import BasicTestCase
import json


class LoginTestCase(BasicTestCase):

    def get_info(self, user_id, token):
        return self.client.post('/auth/info', headers=dict(userid=user_id, token=token),
                                follow_redirects=True)

    def test_get_info_successful(self):
        rv = self.get_info(1, 'bdd27e84-2ade-4515-9ae9-3be1f6c24ea9')
        raw_data = rv.get_data().decode()
        data = json.loads(raw_data)['data']
        assert data['email'] == 'hl2752@nyu.edu'
        assert data['imageuri'] is None
        assert data['motto'] is None
        assert data['username'] == 'jack'

    def test_get_info_fail_1(self):
        rv = self.get_info(2, 'e031c058-dc20-45c4-8e67-b4b80f2c7025')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is True
        #assert data['error']['errorCode'] == '102'

    def test_get_info_fail_2(self):
        rv = self.get_info(1, '1cdb1ca2-b81a-43c4-b51c-aec4fe2e9ccefff')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is False
        assert data['error']['errorCode'] == '101'
