from flask import Flask, request, jsonify, make_response
import uuid, sqlite3, jwt
#from functools import wraps
#from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey123"
def connect_db():
    conn = None
    try:
        conn = sqlite3.connect("users.sqlite")
    except sqlite3.Error as err:
        print(err)

    return conn

#TODO: create a decorator function that checks if the token is valid

#TODO: migrate database to postgresql


@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/greet/<name>")
def greet(name):
    return f"Hello, {name}!"

@app.route("/users", methods=["GET", "POST"])
def users_method():
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == "GET":
        sql_query = """SELECT * FROM user"""

        response = cursor.execute(sql_query)
        users = []

        for user in response.fetchall():
            user1 = User(id=user[0],first_name=user[1], email=user[2], password=user[3], public_id=user[4])
            users.append(user1.serialize())

        if len(users) >=1:
            return jsonify({"users":users})
        else:
            return "no user found", 404
    
    if request.method == "POST":
        try:
            new_first_name = request.form["first_name"]
            new_email = request.form["email"]
            new_password = request.form["password"]
            hashed_password = generate_password_hash(new_password, method="scrypt")
            public_id = uuid.uuid4().hex

            sql_query = """INSERT INTO user(first_name, email, password, public_id) VALUES(?,?,?,?)"""

            response = cursor.execute(sql_query, (new_first_name, new_email, hashed_password, public_id))
            conn.commit()
            users = [] 

            if response:
                return f"user {response.lastrowid} created successfully"
            else:
                return "An error has occured", 404
        except Exception as err:
            return "An error has occured", 404

        
@app.route("/user/<int:iD>", methods = ["GET", "PUT", "DELETE"])
def user_method(iD):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == "GET":
        user = None
        sql_query = """SELECT * FROM user WHERE id = ?"""

        response = cursor.execute(sql_query, (iD,))

        for user in response.fetchall():
            user1 = User(id=user[0],first_name=user[1], email=user[2], password=user[3], public_id=user[4])

            user = user1.serialize()
        if user is not None:
            return jsonify(user)
        else:
            return "User not found", 404

    if request.method == "PUT":
        new_first_name = request.form["first_name"]
        new_email = request.form["email"]
        new_password = request.form["password"]
        hashed_password = generate_password_hash(new_password, method="scrypt")

        sql_query_1 = """SELECT * FROM user WHERE id = ?"""

        response = cursor.execute(sql_query_1, (iD,))

        user1 = response.fetchone()

        if user1 is not None:
            sql_query_2 = """UPDATE user SET first_name=?, email=?, password=? WHERE id = ?"""

            response = cursor.execute(sql_query_2, (new_first_name, new_email, hashed_password, iD))
            conn.commit()

            if response:
                return f"user{iD} updated successfully"
        else:
            return f"User{iD} not found", 404
       
    if request.method == "DELETE":

        sql_query_1 = """SELECT * FROM user WHERE id = ?"""

        response = cursor.execute(sql_query_1, (iD,))

        user1 = response.fetchone()

        if user1 is not None:
            sql_query_2 = """DELETE FROM user WHERE id = ?"""

            response = cursor.execute(sql_query_2, (iD,))
            conn.commit()

            return f"user{iD} deleted"
        else:
            return f"User{iD} not found", 404

@app.route("/users/search/<string:keyword>", methods = ["GET"])
def search_user(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    sql_query = """SELECT * FROM user WHERE first_name LIKE ? OR email LIKE ?"""

    response = cursor.execute(sql_query, (keyword+'%', keyword+'%'))

    users = []

    for user in response.fetchall():
        user1 = User(id=user[0],first_name=user[1], email=user[2], password=user[3], public_id=user[4])
        users.append(user1.serialize())
    if len(users) >=1:
        return jsonify(users)
    else:
        return "no user found", 404

@app.route("/login", methods = ["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})
    else:
        email = auth.username
        password = auth.password
        print(email, password, generate_password_hash(password, method="scrypt"))
        query = """SELECT * FROM user WHERE email = ?"""

        conn = connect_db()
        cursor = conn.cursor()
        response = cursor.execute(query, (email,))
        
        user = response.fetchone() 
        print(user)
        if user is not None:
            # generate token based on public id
            correct_password = check_password_hash(user[3], password)

            if correct_password:
                token = jwt.encode({"user_token": user[4]}, app.config["SECRET_KEY"], algorithm="HS256") 
                print(token) 
                return jsonify({"token": token})
            else:
                return make_response("Invalid credentials", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})
        else:
            return make_response("Invalid Credentials", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

if __name__ == "__main__":
    app.run(debug=True)