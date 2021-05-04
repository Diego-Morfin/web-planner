import os
import psycopg2
import psycopg2.extras
import urllib.parse

class PlansDB:

	def __init__(self):
		urllib.parse.uses_netloc.append("postgres")
		url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

		self.connection = psycopg2.connect(
			cursor_factory=psycopg2.extras.RealDictCursor,
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)

		self.cursor = self.connection.cursor()

	def __del__(self):
		self.connection.close()

	def insertPlan(self, name, description, date1, rating):
		data = [name, description, date1, rating]
		self.cursor.execute("INSERT INTO plans(name, description, date, rating) VALUES (%s, %s, %s, %s)", data)
		self.connection.commit()

	def getPlans(self):
		self.cursor.execute("SELECT * FROM plans ORDER BY id")
		return self.cursor.fetchall()

	def getOnePlan(self, plan_id):
		data = [plan_id]
		self.cursor.execute("SELECT * FROM plans WHERE ID = %s", data)
		return self.cursor.fetchone()

	def deleteOnePlan(self, plan_id):
		data = [plan_id]
		self.cursor.execute("DELETE FROM plans WHERE ID = %s", data)
		self.connection.commit()
		return None

	def updateOnePlan(self, ID, name, description, date1, rating):
		data = [name, description, date1, rating, ID]
		self.cursor.execute("UPDATE plans SET name=%s, description=%s, date=%s, rating=%s WHERE ID=%s", data)
		self.connection.commit()

	def insertUsernameAndPassword(self, firstname, lastname, username, Epassword):
		data = [firstname, lastname, username, Epassword]
		self.cursor.execute("INSERT INTO users(firstname, lastname, username, password) VALUES (%s,%s, %s, %s)", data)
		self.connection.commit()

	def getUsernameAndPassword(self, username):
		data = [username]
		self.cursor.execute("SELECT * FROM users WHERE username = %s", data)
		result = self.cursor.fetchone()
		return result

	def createPlansTable(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS plans (id SERIAL PRIMARY KEY, name TEXT, description TEXT, date TEXT, rating INTEGER)")
		self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, firstname TEXT, lastname TEXT, username TEXT, password TEXT)")
		self.connection.commit()


# CREATE TABLE users (
# id INTEGER PRIMARY KEY,
# firstname TEXT,
# lastname TEXT,
# username TEXT,
# password TEXT);

"""
SQL injection is one of the most common types of hack in sql python code. (bobby table comic).
Search for row_factory so we can return dictionarys instead of tuples.

1. dlete - DB, client, REST
2. update - DB, client, REST
3. CORS - preflight
"""