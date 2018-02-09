from tests.test_basic import BasicTestCase


class PostTestCase(BasicTestCase):

    def submit(self, user_id, token, title, category, tags, content):
        return self.client.post('/post/submit', headers=dict(userid=user_id, token=token),
                                data=dict(title=title, category=category, tags=tags, content=content), follow_redirects=True)

    def test_post_submit(self):
        rv = self.submit(1, '4f3424ea-edb8-4a78-a120-e04973ae12fe', "test post", "cafeteria", "sad", "There was a bug in my salad....")
        data = rv.get_data().decode()

