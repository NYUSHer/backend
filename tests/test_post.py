import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.test_basic import BasicTestCase
import json


class PostTestCase(BasicTestCase):

    def get_list(self, user_id, token, offset, size):
        return self.client.post('post/list', headers=dict(userid=user_id, token=token), data=dict(offset=offset, size=size), follow_redirects=True)

    def test_get_list(self):
        rv = self.get_list(1, 'b8ef7162-9078-407f-ad97-b236afc9e11a', 2, 4)
        data = json.loads(rv.get_data().decode())
        assert data['data']['offset'] == 2
        assert data['data']['size'] == 4
        assert data['data']['count'] == '4'

    def get(self, user_id, token, pid):
        return self.client.post('post/get', headers=dict(userid=user_id, token=token), data=dict(pid=pid), follow_redirects=True)

    def test_get(self):
        rv = self.get(1, 'b8ef7162-9078-407f-ad97-b236afc9e11a', )
        data = json.loads(rv.get_data().decode())
        print(data)
        assert data['data']['title'] != ' '
        assert data['data']['tags'] != ' '

    def submit_new(self, user_id, token, title, category, tags, content, authorid):
        return self.client.post('/post/submit', headers=dict(userid=user_id, token=token),
                                data=dict(title=title, category=category, tags=tags, content=content, authorid=authorid), follow_redirects=True)

    def test_submit_new(self):
        rv = self.submit_new(1, 'b8ef7162-9078-407f-ad97-b236afc9e11a', "test new", "cafeteria", "sad", "There was a bug in my salad....", 1)
        data = json.loads(rv.get_data().decode())
        assert data['data']['pid'] is not None

    def submit_modify(self, user_id, token, title, category, tags, content, pid):
        return self.client.post('/post/submit', headers=dict(userid=user_id, token=token),
                                data=dict(title=title, category=category, tags=tags, content=content, pid=pid), follow_redirects=True)

    def test_submit_modify(self):
        rv = self.submit_modify(1, 'b8ef7162-9078-407f-ad97-b236afc9e11a', "test modify", "cafeteria", "happy", "how are you", 2)
        data = json.loads(rv.get_data().decode())
        assert data['data']['pid'] is not None

    def delete(self, user_id, token, pid):
        return self.client.post('post/delete', headers=dict(userid=user_id, token=token), data=dict(pid=pid))

    def delete_test(self):
        self.delete(1, 'b8ef7162-9078-407f-ad97-b236afc9e11a', 3)
