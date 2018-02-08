from tests.test_basic import BasicTestCase
import json


class InfoTestCase(BasicTestCase):

    def get_info(self, user_id, token):
        return self.client.post('/auth/info', headers=dict(userid=user_id, token=token),
                                follow_redirects=True)

    def test_get_info_successful(self):
        rv = self.get_info(1, '16f8d711-a1f1-438d-932c-a83c6c5c1521')
        raw_data = rv.get_data().decode()
        data = json.loads(raw_data)['data']
        assert data['email'] == 'hl2752@nyu.edu'
        assert data['imageuri'] == 'nowhere'
        assert data['motto'] == 'Every night I live and die'
        assert data['username'] == 'maxee'

    def test_get_info_fail_1(self):
        rv = self.get_info(3, '123')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is False
        assert data['error']['errorCode'] == '102'

    def test_get_info_fail_2(self):
        rv = self.get_info(2, '1cdb1ca2-b81a-43c4-b51c-aec4fe2e9ccefff')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is False
        assert data['error']['errorCode'] == '101'
