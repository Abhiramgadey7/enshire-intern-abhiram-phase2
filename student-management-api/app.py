from flask import Flask, jsonify, request

app = Flask(__name__)

students = []

@app.route("/")
def home():
    return jsonify({"message": "Student Management API Running"})

@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)

@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    student = {
        "id": len(students) + 1,
        "name": data["name"],
        "email": data["email"],
        "course": data["course"]
    }

    students.append(student)
    return jsonify(student), 201

if __name__ == "__main__":
    app.run(debug=True)