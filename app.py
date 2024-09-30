# Task 2:
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required = True)
    age = fields.String(required = True)
    id = fields.Integer()
    class meta:
        fields = ("name", "age", "id")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True) 

class SessionSchema(ma.Schema):
    session_id = fields.Integer()
    member_id = fields.Integer(required = True)
    session_date = fields.String(required = True)
    session_time = fields.String()
    activity = fields.String()
    class meta:
        fields = ("session_id", "member_id", "session_date", "session_time", "activity")

session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True) 

def get_db_connection():
    db_name = "fitness_center_db"
    user = "root"
    password = "Umbr3ll@4850"
    host = "localhost"
    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        print("Connected to MySQL database successfully.")
        return conn

    except Error as e:
        print(f"Error: {e}")
        return None


@app.route('/')
def home():
    return "Welcome to the Fitness Center!"

@app.route("/members", methods=["GET"])
def get_all_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM members;"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:id>", methods=["GET"])
def get_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        member_id = (id,)

        query = "SELECT * FROM members WHERE id = %s;"

        cursor.execute(query, member_id)

        member = cursor.fetchone()

        return member_schema.jsonify(member)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    

@app.route("/members", methods=["POST"])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_member = (member_data['name'], member_data['age'])

        query = "INSERT INTO Members (name, age) VALUES (%s, %s)"

        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({"message": "New member added successfully."}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_member = (member_data['name'], member_data["age"], id)

        query = 'UPDATE Members SET name = %s, age = %s WHERE id = %s'

        cursor.execute(query, updated_member)
        conn.commit()

        return jsonify({"message": "Member updated successfully."}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        member_to_remove = (id,)
        
        cursor.execute("SELECT * FROM members WHERE id = %s", member_to_remove)
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error": "Member not found"}), 404
        
        query = "DELETE FROM members WHERE id = %s"

        cursor.execute(query, member_to_remove)
        conn.commit()

        return jsonify({"message": "Member removed successfully."}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/workoutsessions", methods=["GET"])
def get_all_sessions():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM workoutsessions;"

        cursor.execute(query)

        sessions = cursor.fetchall()

        return sessions_schema.jsonify(sessions)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/workoutsessions/<int:member_id>", methods=["GET"])
def get_member_sessions(member_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        member_id_tuple = (member_id,)

        query = "SELECT * FROM workoutsessions WHERE member_id = %s;"

        cursor.execute(query, member_id_tuple)

        session = cursor.fetchall()
        if not session:
            return jsonify({"error": "Sessions not found"}), 404
        else:
            return session_schema.jsonify(session)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/workoutsessions", methods=["POST"])
def add_session():
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        
        new_session = (session_data['member_id'], session_data['session_date'], session_data['session_time'])

        query = "INSERT INTO workoutsessions (member_id, session_date, session_time) VALUES (%s, %s, %s)"

        cursor.execute(query, new_session)
        conn.commit()

        return jsonify({"message": "Session added successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
@app.route("/workoutsessions/<int:session_id>", methods=["PUT"])
def update_session(session_id):
    try:
        session_data = session_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_session = (session_data['member_id'], session_data["session_date"], session_data["session_time"], session_data["activity"], session_id)

        query = 'UPDATE workoutsessions SET member_id = %s, session_date = %s, session_time = %s, activity = %s WHERE session_id = %s;'

        cursor.execute(query, updated_session)
        conn.commit()

        return jsonify({"message": "Workout Session updated successfully."}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)