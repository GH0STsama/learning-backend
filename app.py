import database.database as db
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from status_codes import Status, status_description
from user import User, validate_email, validate_username


app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret" # Change this
jwt = JWTManager(app)


####################################################
# Route to authenticate the users and return JWTs. #
@app.route("/login", methods=["POST"])
def login():

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = db.read_user(username)

    if not user or not password == user.password:
        return status_description[Status.Unauthorized], Status.Unauthorized

    access_token = create_access_token(identity = username)
    return {"token": access_token}


######################################################
# Create (if not exists) a new user in the database. #
@app.route("/user", methods=["POST"])
def register():

    required_keys = User(None, None, None, None, None, None).__dict__
    required_keys.pop("role")

    request_keys = request.json.keys()

    # Verify that the request contains all the required fields
    for key in required_keys:
        if not key in request_keys:
            return status_description[Status.BadRequest], Status.BadRequest

   # Verify that the request contains only the required fields
    for key in request_keys: # Maybe this is not necessary?
        if not key in required_keys:
            return status_description[Status.BadRequest], Status.BadRequest

    if not validate_username(request.json["username"]):
        return status_description[Status.BadRequest], Status.BadRequest

    if not validate_email(request.json["email"]):
        return status_description[Status.BadRequest], Status.BadRequest

    user = User(
        request.json["username"],
        request.json["password"],
        request.json["firstName"],
        request.json["lastName"],
        request.json["email"],
        request.json["age"]
    )

    try:
        # Try insert the user info into the database
        user = db.create_user(user)

        #  If it was created without problems,
        # returns the information to the user,
        # along with an access token
        if user:
            token = create_access_token(identity = user.username)
            user.__dict__["token"] = token
            return user.__dict__

        else:
            return status_description[Status.BadRequest], Status.BadRequest
    except:
        return status_description[Status.BadRequest], Status.BadRequest


######################################################
# Read the information of all users in the database. #
@app.route("/user", methods=["GET"])
@jwt_required()
def read_all():
    return jsonify(db.read_all_users())


#######################################################
# Read the information of a user (if it is athorized) #
@app.route("/user/<username>", methods=["GET"])
@jwt_required()
def read_user(username):

    user = db.read_user(username)

    if not user: # Return error if this user not in the database
        return status_description[Status.NotFound], Status.NotFound

    user.__dict__.pop("password")
    return user.__dict__


##########################################################
# Update the information of a user (if it is authorized) #
@app.route("/user/<username>", methods=["PUT"])
@jwt_required()
def update_user(username):

    user = db.read_user(username)

    if not user: # Return error if this user not in the database
        return status_description[Status.NotFound], Status.NotFound

    # Check if this user has permissions to perform this action
    user_identity = get_jwt_identity()
    if not user_identity == user.username and not db.read_user(user_identity).is_admin():
        return status_description[Status.Unauthorized], Status.Unauthorized

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

        if updated:
            return updated.__dict__
        # else
        return status_description[Status.BadRequest], Status.BadRequest

    except:
        return status_description[Status.BadRequest], Status.BadRequest


##########################################################
# Delete the information of a user (If it is authorized) #
@app.route("/user/<username>", methods=["DELETE"])
@jwt_required()
def delete_user(username):

    user = db.read_user(username)

    if not user: # Return error if this user not in the database
        return status_description[Status.NotFound], Status.NotFound

    # Check if this user has permissions to perform this action
    user_identity = get_jwt_identity()
    if not user_identity == user.username and not db.read_user(user_identity).is_admin():
        return status_description[Status.Unauthorized], Status.Unauthorized

    deleted = db.delete_user(user.username)

    if deleted:
        return "User has been deleted"
    else:
        return status_description[Status.BadRequest], Status.BadRequest
