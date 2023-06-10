from flask import Flask, request, jsonify
import sqlite3
from models.user_model import User
app = Flask(__name__)

def connect_db():
    conn = None
    try:
        conn = sqlite3.connect("users.sqlite")
    except sqlite3.Error as err:
        print(err)

    return conn

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
            user1 = User(id=user[0],first_name=user[1], email=user[2], password=user[3])
            users.append(user1.serialize())
        if len(users) >=1:
            return jsonify(users)
        else:
            return "no user found", 404
    
    if request.method == "POST":

        new_first_name = request.form["first_name"]
        new_email = request.form["email"]
        new_password = request.form["password"]

        sql_query = """INSERT INTO user(first_name, email, password) VALUES(?,?,?)"""

        response = cursor.execute(sql_query, (new_first_name,new_email,new_password))
        conn.commit()
        users = []

        if response:
            return f"user {response.lastrowid} created successfully"
        else:
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
            user1 = User(id=user[0],first_name=user[1], email=user[2], password=user[3])

            user = user1.serialize()
        if user is not None:
            return jsonify(user)
        else:
            return "User not found", 404

    if request.method == "PUT":

        new_first_name = request.form["first_name"]
        new_email = request.form["email"]
        new_password = request.form["password"]

        sql_query = """UPDATE user SET first_name=?, email=?, password=? WHERE id = ?"""

        response = cursor.execute(sql_query, (new_first_name, new_email, new_password, iD))
        conn.commit()
        if response:
            user1 = User(id=iD,first_name= new_first_name, email= new_email, password=new_password)
            user = user1.serialize()
            return jsonify(user)
        else:
            return "User not found", 404
       
    if request.method == "DELETE":

        sql_query = """DELETE FROM user WHERE id = ?"""

        response = cursor.execute(sql_query, (iD,))
        conn.commit()
        if response:
            return f"user{iD} deleted"
        else:
            return "User not found", 404

if __name__ == "__main__":
    app.run(debug=True)