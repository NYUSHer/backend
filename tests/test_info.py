import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.test_basic import BasicTestCase
import json


class InfoTestCase(BasicTestCase):

    def get_info(self, user_id, token):
        return self.client.post('/auth/info', headers=dict(userid=user_id, token=token),
                                follow_redirects=True)

    def test_get_info_successful(self):
        rv = self.get_info(1, 'b8ef7162-9078-407f-ad97-b236afc9e11a')
        raw_data = rv.get_data().decode()
        print(raw_data)
        data = json.loads(raw_data)['data']
        assert data['email'] == 'hl2752@nyu.edu'
        assert data['imageuri'] == 'nowhere'
        assert data['motto'] == 'Every night I live and die'
        assert data['username'] == 'maxee'

    def test_get_info_fail_1(self):
        rv = self.get_info(16, 'aa170d6f-b1ad-4330-b348-77c754e7b2ec')
        data = json.loads(rv.get_data().decode())
        print(data)
        assert data['state'] is False
        assert data['error']['errorCode'] == '102'

    def test_get_info_fail_2(self):
        rv = self.get_info(1, '1111111117c4-95cd-7feb20ff11cb')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is False
        assert data['error']['errorCode'] == '101'
