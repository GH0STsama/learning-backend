from flask import Flask, request
import uuid

app = Flask(__name__)
database = {}


@app.route("/create")
def create():
    """Create a field for the user in the database"""

    uid = uuid.uuid4()

    database.update({
        uid: {
            "uid": uid,
            "firstName": request.json["firstName"],
            "lastName": request.json["lastName"],
            "email": request.json["email"],
            "age": request.json["age"]
        }
    })

    return {"response": "inserted user"}


@app.route("/read")
def read():
    """Read a user info in database"""

    for uid in database.keys():
        if request.json["firstName"] == database[uid]["firstName"]:

            return {
                "uid": uid,
                "firstName": database[uid]["firstName"],
                "lastName": database[uid]["lastName"],
                "email": database[uid]["email"],
                "age": database[uid]["age"]
            }

    # If user not in database
    return "", 404


@app.route("/read-all")
def read_all():
    """Read the info of the all user in database"""

    users_info = []
    for uid in database:
        users_info.append({
            "uid": uid,
            "firstName": database[uid]["firstName"],
            "lastName": database[uid]["lastName"],
            "email": database[uid]["email"],
            "age": database[uid]["age"]
        })

    return {"users": users_info}


@app.route("/update")
def update():
    """Update a user info in database"""

    for uid in database:
        if request.json["firstName"] == database[uid]["firstName"]:

            # Update user info if exists
            database[uid].update({
                "uid": uid,
                "firstName": request.json["new_firstName"],
                "lastName": request.json["new_lastName"],
                "email": request.json["new_email"],
                "age": request.json["new_age"]
            })

            return {"response": "the info has been updated"}

    # If user not in database
    return "", 404


@app.route("/delete")
def delete():
    """Delete all info of the user in database"""

    for uid in database:
        if request.json["firstName"] == database[uid]["firstName"]:
            # Delete all info of this user
            database.pop(uid)

            return {"response": "the info has been deleted"}
 
    # If user not in database
    return "", 404
