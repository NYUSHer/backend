import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.test_basic import BasicTestCase


class EmailTestCase(BasicTestCase):

    def send_email(self, user_id, token, subject, recipient, content):
        return self.client.post('/post/sendmail', headers=dict(userid=user_id, token=token),
                                data=dict(subject=subject, recipient=recipient, content=content),
                                follow_redirects=True)

    def test_send_email(self):
        rv = self.send_email(14, '01eb0f5e-1c41-47c4-95cd-7feb20ff11cb', "Test Email",
                             ["mk5986@nyu.edu"], "This is just a test.")
        data = rv.get_data().decode()
