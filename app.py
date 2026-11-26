from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

# MongoDB connection
client = MongoClient(
    os.getenv("MONGO_URI"),
    serverSelectionTimeoutMS=5000
)

db = client["flask_db"]
collection = db["students"]


# Task 1 - JSON API
@app.route("/api")
def api():
    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


# Task 2 - Student Registration
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        try:
            name = request.form["name"].strip()
            email = request.form["email"].strip()
            course = request.form["course"].strip()

            if not name or not email or not course:
                return render_template(
                    "index.html",
                    error="All fields are required"
                ), 400

            student = {
                "name": name,
                "email": email,
                "course": course
            }

            collection.insert_one(student)

            return redirect(url_for("success"))

        except Exception:
            app.logger.exception("Submission failed")

            return render_template(
                "index.html",
                error="Unable to submit data. Please try again."
            ), 500

    return render_template("index.html")


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
