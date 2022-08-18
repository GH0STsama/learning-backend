from flask import Flask, request, jsonify
import database.database as db
from user import User, Roles, validate_email, validate_username

app = Flask(__name__)


def contains_required_fields(fields: dict) -> bool:
    """Verify that it contain the required fields"""

    for key in ["username", "password", "firstName", "lastName", "email", "age"]:
        if not key in fields.keys():
            return False
    return True


@app.route("/", methods=["GET", "POST"])
def create_or_readall():
    """Create a field, or read the info of all users in the database"""

    ####################################
    # On post request, insert new user #
    if request.method == "POST":
        if not contains_required_fields(request.json):
            return "", 400

        if not validate_username(request.json["username"]):
            return "", 400

        if not validate_email(request.json["email"]):
            return "", 400

        user = User(
            request.json["username"],
            request.json["password"],
            request.json["firstName"],
            request.json["lastName"],
            request.json["email"],
            request.json["age"],
            Roles.user
        )

        try:
            user = db.create_user(user)
            return user.__dict__ if user else "", 400

        except:
            return "", 400

    ################################################
    # On get request, return the info of all users #
    elif request.method == "GET":
        return jsonify(db.read_all_users())


@app.route("/<username>", methods=["GET", "PUT", "DELETE"])
def manage_user_info(username):
    """Get, update, or delete, the info of the specific user in the database"""

    ########################################
    # On get request, return the user info #
    if request.method == "GET":
        user = db.read_user(username)
        return user.__dict__ if user else "", 404

    ########################################
    # On put request, update the user info #
    if request.method == "PUT":

        try:
            keys = request.json.keys()
            user = User(
                request.json["username"] if "username" in keys else None,
                request.json["password"] if "password" in keys else None,
                request.json["firstName"] if "firstName" in keys else None,
                request.json["lastName"] if "lastName" in keys else None,
                request.json["email"] if "email" in keys else None,
                request.json["age"] if "age" in keys else None,
                request.json["role"] if "role" in keys else None
            )

            updated = db.update_user(username, user)

            return updated.__dict__ if updated else "", 400

        except:
            return "", 400

    ##########################################
    # On delete request, delete de user info #
    if request.method == "DELETE":
        deleted = db.delete_user(username)
        return "User has been deleted" if deleted else "", 400
