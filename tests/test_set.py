from tests.test_basic import BasicTestCase


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
        username = 'maxee'
        motto = 'Every night I live and die'
        rv = self.set_info(1, 'bdd27e84-2ade-4515-9ae9-3be1f6c24ea9', username=username, motto=motto)
        data = rv.get_data().decode()
        assert data == 'done'

    def test_set_normal(self):
        passwdtoken = 'ec5e1e94c042dda33822701a45eb5e30'
        rv = self.set_info(1, 'bdd27e84-2ade-4515-9ae9-3be1f6c24ea9', passwdtoken=passwdtoken)
        data = rv.get_data().decode()
        assert data == 'done'
