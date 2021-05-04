from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
from urllib.parse import parse_qs
from mydb import PlansDB
from session_store import SessionStore
from passlib.hash import bcrypt
import json
import sys

SESSION_STORE = SessionStore()

class MyRequestHandler(BaseHTTPRequestHandler):

	def do_OPTIONS(self):
		# implements preflighted request
		self.load_session()
		self.send_response(200)
		self.send_header("Access-Control-Allow-Methods","GET, POST, PUT, DELETE, OPTIONS")
		self.send_header("Access-Control-Allow-Headers","Content-Type")
		self.end_headers()
		pass

	# server aks for data from user
	def do_GET(self):
		self.load_session()
		print("The PATH is: ", self.path)
		# use a noun for the resource instead of "hello"
		# always use a collection/plural name
		if self.path == "/plans":
			self.handlePlansRetrieveCollection()
		elif self.path.startswith("/plans/"):
			self.handlePlanRetrieveMember()
		else:
			self.handleNotFound()

	def do_POST(self):
		self.load_session()
		if self.path == "/users":
			self.handleNewUser()
		elif self.path == "/plans":
			self.handlePostMember()
		elif self.path == "/sessions":
			self.handleUserRetrieveID()
		elif self.path == "/logoutUsers":
			self.handleUserLogout()
		else:
			self.handleNotFound()

	def do_PUT(self):
		self.load_session()
		if self.path.startswith("/plans/"):
			self.handlePlanUpateMember()
		else:
			self.handleNotFound()

	def do_DELETE(self):
		self.load_session()
		if self.path.startswith("/plans/"):
			self.handlePlanDeleteMember()
		else:
			self.handleNotFound()
		pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def handleNotFound(self):
		self.send_response(404, "page not found")
		self.end_headers()

	def handleNotAuthorized(self):
		self.send_response(401, "user not authenticated")
		self.end_headers()

	def end_headers(self):
		self.send_cookie()
		self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
		self.send_header("Access-Control-Allow-Credentials", "true")
		BaseHTTPRequestHandler.end_headers(self)

	# session id goes inside the cookie
	# goal: load cookie into self.cookie
	def load_cookie(self):
		if "Cookie" in self.headers:
			self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
		else:
			self.cookie = cookies.SimpleCookie()

	def send_cookie(self):
		for morsel in self.cookie.values():
			self.send_header("Set-Cookie", morsel.OutputString())

	# goal load session into self.session
	# self.cookie is a dictionary from the sessions dictionary of dictionarys
	def load_session(self):
		self.load_cookie()
		
		# if sessionID is in the cookie
		if "sessionId" in self.cookie:
			sessionId = self.cookie["sessionId"].value
			# save the session into self.session for use later
			self.session = SESSION_STORE.getSession(sessionId)
			# if sessionID is not in the session store
			if self.session == None:
				# create a new session
				sessionId = SESSION_STORE.createSession()
				self.session = SESSION_STORE.getSession(sessionId)
				# set a new sessionID into the cookie
				self.cookie["sessionId"] = sessionId
		# otherwise, if sessionID is NOT in the cookies
		else:
			# create a new session
			sessionId = SESSION_STORE.createSession()
			self.session = SESSION_STORE.getSession(sessionId)
			# set a new sessionID into the cookie
			self.cookie["sessionId"] = sessionId

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def handleUserRetrieveID(self):
		length = self.headers["Content-length"]
		body = self.rfile.read(int(length)).decode("utf-8")
		parsed_body = parse_qs(body)

		username = parsed_body["username"][0]
		password = parsed_body["password"][0]

		db = PlansDB()
		user = db.getUsernameAndPassword(username)

		if user != None:
			if bcrypt.verify(password, user["password"]):
				self.send_response(200)
				self.session["userId"] = user["id"]
				self.send_header("Content-Type", "application/json")
				self.end_headers()
			else:
				self.send_response(401, "wrong password")
				self.end_headers()
		else:
			self.send_response(401, "wrong email")
			self.end_headers()


	def handleNewUser(self):
		length = self.headers["Content-length"]
		body = self.rfile.read(int(length)).decode("utf-8")
		print("BODY:", body)
		parsed_body = parse_qs(body)
		print("PARSED BODY:", parsed_body)

		firstname = parsed_body["firstname"][0]
		lastname = parsed_body["lastname"][0]
		username = parsed_body["username"][0]
		password = parsed_body["password"][0]

		for i in range(10):
			Epassword = bcrypt.hash(password)

		db = PlansDB()
		user = db.getUsernameAndPassword(username)

		if user == None:
			db.insertUsernameAndPassword(firstname, lastname, username, Epassword)
			self.send_response(201)
			self.end_headers()
		else:
			self.send_response(422, "Email is already in use")
			self.end_headers()

	def handleUserLogout(self):
		print("logging out")
		self.session.pop("userId", None)
		self.send_response(200)
		self.end_headers()

	def handlePostMember(self):
		if "userId" not in self.session:
			self.handleNotAuthorized()
			return

		length = self.headers["Content-length"]
		# this read the file from the request 
		# read the body (data)
		body = self.rfile.read(int(length)).decode("utf-8")
		print("BODY:", body)

		# parse the body into a dictionary using a parse_qs()
		parsed_body = parse_qs(body)
		print("PARSED BODY:", parsed_body)

		# save the plan into our database
		name = parsed_body["name"][0]
		description = parsed_body["description"][0]
		date = parsed_body["date"][0]
		rating = parsed_body["rating"][0]

		db = PlansDB()
		db.insertPlan(name, description, date, rating)

		# respond to the client
		self.send_response(201)
		# make sure this kind of header is every where to avoid errors
		self.end_headers()


	def handlePlanUpateMember(self):
		if "userId" not in self.session:
			self.handleNotAuthorized()
			return

		parts = self.path.split("/")
		plan_id = parts[2]

		length = self.headers["Content-length"]
		# this read the file from the request 
		# read the body (data)
		body = self.rfile.read(int(length)).decode("utf-8")
		print("BODY:", body)

		# parse the body into a dictionary using a parse_qs()
		parsed_body = parse_qs(body)
		print("PARSED BODY:", parsed_body)

		name = parsed_body["name"][0]
		description = parsed_body["description"][0]
		date = parsed_body["date"][0]
		rating = parsed_body["rating"][0]

		db = PlansDB()
		plan = db.getOnePlan(plan_id)

		if plan != None:
			db.updateOnePlan(plan_id, name, description, date, rating)
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.end_headers()
			self.wfile.write(bytes(json.dumps(plan), "utf-8"))
		else:
			self.handleNotFound()

	def handlePlansRetrieveCollection(self):
		if "userId" not in self.session:
			self.handleNotAuthorized()
			return

		# respond accordingly
		# status code is always first
		self.send_response(200)
		# lets the client know what kind of data we're sending
		self.send_header("Content-Type", "application/json")
		# allows access to anyone because of cors policy
		# there's different type of headers
		# end of headers is always last
		self.end_headers()
		# send a body
		# sends the post
		db = PlansDB()
		plans = db.getPlans()
		self.wfile.write(bytes(json.dumps(plans), "utf-8"))

	def handlePlanRetrieveMember(self):
		if "userId" not in self.session:
			self.handleNotAuthorized()
			return

		parts = self.path.split("/")
		plan_id = parts[2]

		db = PlansDB()
		plan = db.getOnePlan(plan_id)

		if plan != None:
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.end_headers()
			self.wfile.write(bytes(json.dumps(plan), "utf-8"))
		else:
			self.handleNotFound()

	def handlePlanDeleteMember(self):
		if "userId" not in self.session:
			self.handleNotAuthorized()
			return

		parts = self.path.split("/")
		plan_id = parts[2]

		db = PlansDB()
		plan = db.getOnePlan(plan_id)

		# before deleting check if it exists then delete, otherwise return a 404s
		if plan != None:
			db.deleteOnePlan(plan_id)
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.end_headers()
			self.wfile.write(bytes(json.dumps(plan), "utf-8"))
		else:
			self.handleNotFound()


def run():
	db = PlansDB()
	db.createPlansTable()
	db = None # disconnect

	port = 8080
	if len(sys.argv) > 1:
		port = int(sys.argv[1])

	listen = ("0.0.0.0", port)
	server = HTTPServer(listen, MyRequestHandler)

	print("Server listening on", "{}:{}".format(*listen))
	server.serve_forever()

run()


# sends the cookie to the client via headers
# TODO: put send_cookie after ending headers

#		make sure they're self.session["userId"] = user_id
#		user_id is from the database
#		same as we did for the password
#		figure out where to put it ourselves
#		should be after they've been (logged in) authenticated (after a 201)
#		postman should be saved and shouldn't change the session ID

#		use status code 422 if email is repeated or password doesn't work

"""
page loads
~~~~~~~~~~
1.
GET / plans
200 OK
BODY: list of plans (json)
(data is displayed by client)
user submits a new entry

2.
POST / plans
BODY: new plan data(form urlencoded)
201 created
(server saves new data)

[immediately]
3.
GET / plans
200 OK
BODY: list of plans (json)
(new data is refreshed)
"""