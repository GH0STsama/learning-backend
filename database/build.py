import sqlite3
import os

# Default Admin
USERNAME = "admin"
PASSWORD = "admin"
FIRST_NAME = "admin"
LAST_NAME = "admin"
EMAIL = "admin@host.local"
AGE = 0


try:
    # remove current database if exists
    os.unlink("./database/database.db")
except: pass

# make a connection to the database
db = sqlite3.connect("./database/database.db")

# create table for roles (I don't know the usefulness of this)
db.execute("""\
CREATE TABLE IF NOT EXISTS "roles" (
  "id"  INTEGER NOT NULL,
  "role"  TEXT NOT NULL,
  PRIMARY KEY("id" AUTOINCREMENT)
);\
""")

# create a table for store the users
db.execute("""\
CREATE TABLE IF NOT EXISTS "users" (
  "id"         INTEGER NOT NULL,
  "username"   TEXT NOT NULL UNIQUE,
  "password"   TEXT NOT NULL,
  "firstName"  TEXT NOT NULL,
  "lastName"   TEXT NOT NULL,
  "email"      TEXT NOT NULL UNIQUE,
  "age"        INTEGER NOT NULL,
  "role"       INTEGER NOT NULL,
  PRIMARY KEY("id" AUTOINCREMENT),
  FOREIGN KEY("role") REFERENCES "roles"("id")
);\
""")

# insert the default values in the "roles" table
db.execute("INSERT INTO \"roles\" (\"id\", \"role\") VALUES (1, 'admin');")
db.execute("INSERT INTO \"roles\" (\"id\", \"role\") VALUES (2, 'user');")

# insert a default user with the "admin" role in the users table
db.execute(f"""\
INSERT INTO \"users\" (\"id\", \"username\", \"password\", \"firstName\", \"lastName\", \"email\", \"age\", \"role\")
VALUES (1, '{USERNAME}', '{PASSWORD}', '{FIRST_NAME}', '{LAST_NAME}', '{EMAIL}', {AGE}, 1);\
""")

# save all changes to the database
db.commit()
