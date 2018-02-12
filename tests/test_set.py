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

    def test_set_normal(self):
        username = 'max'
        motto = 'Every night I live and die'
        rv = self.set_info(2, 'ea7cdefd-fbff-4b6c-8c2a-9d5e10c0bd01', username=username, motto=motto, imageuri='nowhere')
        data = json.loads(rv.get_data().decode())
        assert data['state'] is True
        print(data)

    # def test_set_passwd(self):
    #     passwdtoken = 'ec5e1e94c042dda33822701a45eb5e30'
    #     rv = self.set_info(1, '16f8d711-a1f1-438d-932c-a83c6c5c1521', passwdtoken=passwdtoken)
    #     data = rv.get_data().decode()
    #     assert data == 'done'
