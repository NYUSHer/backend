import abc

class User:

    def __init__(self, Uid=000000, username='' , token='', email=''):
    	self.Uid = Uid
    	self.username = username
    	self.token = token
    	self.email = email

    # Getter and Setters


    @abc.abstractmethod
    def authenticate_with_token(token):
    	pass

    @abc.abstractmethod
    def authenticate_with_email():
    	pass

    @abc.abstractmethod
    def reset_token():
    	pass

class post:
	def __init__(self, Pid=000000, Uid=000000, tags=[],\
	 timestamp=0000000, modified=False, comments=[]):
		self.Pid = Pid
		self.Uid = Uid
		self.tags = tags
		self.timestamp = timestamp
		self.modified  = modified
