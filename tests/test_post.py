from tests.test_basic import BasicTestCase
import json


class PostTestCase(BasicTestCase):

    def get_list(self, user_id, token, offset, size):
        return self.client.post('post/list', headers=dict(userid=user_id, token=token), data=dict(offset=offset, size=size), follow_redirects=True)

    def test_get_list(self):
        rv = self.get_list(1, 'd33341c4-e55c-4e65-8a0b-af39a86a2fce', 2, 4)
        data = json.loads(rv.get_data().decode())
        assert data['offset'] == 2
        assert data['size'] == 4
        assert data['count'] == 4
        assert data['postlist'][0]['pid'] == 13

    def get(self, user_id, token, pid):
        return self.client.post('post/get', headers=dict(userid=user_id, token=token), data=dict(pid=pid), follow_redirects=True)

    def test_get(self):
        rv = self.get(1, 'd33341c4-e55c-4e65-8a0b-af39a86a2fce', 3)
        data = json.loads(rv.get_data().decode())
        print(data)
        assert data['data']['title'] == 'test3'
        assert data['data']['tags'] == 'sad'
        assert data['data']['authorid'] == 1

    def submit_new(self, user_id, token, title, category, tags, content, authorid):
        return self.client.post('/post/submit', headers=dict(userid=user_id, token=token),
                                data=dict(title=title, category=category, tags=tags, content=content, authorid=authorid), follow_redirects=True)

    def test_submit_new(self):
        rv = self.submit_new(1, 'd33341c4-e55c-4e65-8a0b-af39a86a2fce', "test new", "cafeteria", "sad", "There was a bug in my salad....", 1)
        data = json.loads(rv.get_data().decode())
        assert data['data']['pid'] is not None

    def submit_modify(self, user_id, token, title, category, tags, content, pid):
        return self.client.post('/post/submit', headers=dict(userid=user_id, token=token),
                                data=dict(title=title, category=category, tags=tags, content=content, pid=pid), follow_redirects=True)

    def test_submit_modify(self):
        rv = self.submit_modify(1, 'd33341c4-e55c-4e65-8a0b-af39a86a2fce', "test modify", "cafeteria", "happy", "how are you", 1)
        data = json.loads(rv.get_data().decode())
        print(data)
        assert data['data']['pid'] is not None

    def delete(self, user_id, token, pid):
        return self.client.post('post/delete', headers=dict(userid=user_id, token=token), data=dict(pid=pid))

    def delete_test(self):
        self.delete(1, 'd33341c4-e55c-4e65-8a0b-af39a86a2fce', 3)
