import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.test_basic import BasicTestCase
import json


class LoginTestCase(BasicTestCase):

    def set_info(self, user_id, token, username=None, imageuri=None, motto=None, passwdtoken=None):
        data = dict()
        if username is not None:
            data['username'] = username
        if imageuri is not None:
            data['imageuri'] = imageuri
        if motto is not None:
            data['motto'] = motto
        if passwdtoken is not None:
            data['passwdtoken'] = passwdtoken
        return self.client.post('/auth/set', headers=dict(userid=user_id, token=token),
                                data=data,
                                follow_redirects=True)

    #def test_set_normal(self):
    #    username = 'masaki'
    #    motto = 'aloha'
    #    rv = self.set_info(20, '3736ccac-ac45-490f-b486-9ebb1e0cc909', username=username, motto=motto, imageuri='https://storage-1.nya.vc/UNuejL2a')
    #    data = json.loads(rv.get_data().decode())
    #    print(data)
    #    assert data['state'] is True

    # def test_set_passwd(self):
    #     passwdtoken = 'ec5e1e94c042dda33822701a45eb5e30'
    #     rv = self.set_info(1, '16f8d711-a1f1-438d-932c-a83c6c5c1521', passwdtoken=passwdtoken)
    #     data = rv.get_data().decode()
    #     assert data == 'done'
