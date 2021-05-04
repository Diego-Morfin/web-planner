import os, base64

class SessionStore:
	# TODO:
	# need a dictionary (of dictionarys)
	# add a new session to the session store
	# retrieve an existing session from the session store
	# we need to create a new session ID

	# setting up session stores
	def __init__(self):
		# self.sessions is a dictionary (of dictionarys)
		self.sessions = {}

	# add a new session to the sesssion store
	def createSession(self):
		newSessionId = self.generateSessionId()
		# well start out empty eventually put another empty dictionary
		self.sessions[newSessionId] = {}
		return newSessionId

	# retrieve an existing session from the session store
	def getSession(self, sessionId):
		# check if it exists to avoid getting an iternal error
		if sessionId in self.sessions:
			return self.sessions[sessionId]
		else:
			return None

	# create a new session ID
	def generateSessionId(self):
		# 32 random bytes
		# chances of getting a repeat are extremely low
		rnum = os.urandom(32)
		# encoding the rnum with base64 num
		rstr = base64.b64encode(rnum).decode("utf-8")
		return rstr