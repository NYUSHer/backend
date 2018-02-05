from tests.test_sample import BasicTestCase


class LoginTestCase(BasicTestCase):


    def login(self, useremail, password):
        return self.app.post('/auth/login', data=dict(
            username=useremail,
            password=password
        ), follow_redirects=True)

    def test_login_success(self):
        rv = self.login('masaki@gmail.com', 'e27bbaa25e61:c28d7a9a8d9fde8a82008d54b38dab981d6730be')
        assert True in rv.state

    def test_login_fail(self):
        pass


