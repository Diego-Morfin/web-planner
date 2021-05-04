# ASSIGNMENT 4: Authentication

## Resource

**Planner**

Attributes:

* name (string)
* description (string)
* date (string)
* rating (integer)

**Users**

Attributes:

* firstname (string)
* lastname (string)
* username (string)
* password (string)

## Schema

```sql
CREATE TABLE plans (
id INTEGER PRIMARY KEY,
name TEXT,
description TEXT,
date TEXT,
rating INTEGER);

CREATE TABLE users (
id INTEGER PRIMARY KEY,
firstname TEXT,
lastname TEXT,
username TEXT,
password TEXT);
```

## REST Endpoints

Name                           | Method | Path
-------------------------------|--------|------------------
Retrieve plan collection | GET    | /plans
Retrieve plan member     | GET    | /plans/*\<id\>*
Create plan member       | POST   | /plans
Update plan member       | PUT    | /plans/*\<id\>*
Delete plan member       | DELETE | /plans/*\<id\>*
Create user member		 | POST   | /users
Retrieve user member	 | POST	  | /sessions
Logout user member	     | POST   | /logoutUsers

## Relevant Data

The method of hashing used by my server is bcrypt encryption.