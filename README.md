![website](https://user-images.githubusercontent.com/54593885/117068768-efc53100-ace8-11eb-8fe7-302ccdc80d3f.png)
# web-planner

### Description
a very basic web site that covers most requirements that is expected on a normal site.
It contains basic authorization on top of the login and logout. The site also uses cookies and data encryption.
The website also uses a database to encrypt and store all the data safely.


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

![website](https://user-images.githubusercontent.com/54593885/117068798-f784d580-ace8-11eb-8c80-8f3935667cc3.png)
