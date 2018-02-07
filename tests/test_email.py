from tests.test_basic import BasicTestCase


class EmailTestCase(BasicTestCase):

    def send_email(self, user_id, token, subject, recipient, content):
        return self.client.post('/post/sendmail', headers=dict(userid=user_id, token=token), data=dict(subject=subject, recipient=recipient, content=content),
                                follow_redirects=True)

    def test_send_email(self):
        rv = self.send_email(1, 'eb0df5ff-dcfb-497c-a396-cf3cf4f13a78', "Test Email", ["hl2752@nyu.edu"], "This is just a test.")
        data = rv.get_data().decode()
        assert data == "Sent."
