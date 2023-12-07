from .db_model import Query
from flask import Flask, request

app = Flask(__name__)

query = Query()

@app.route("/api/message", methods=["POST"])
def add_message():
    req = request.get_json()
    query.add_message(message=req)
    return "OK",200


@app.route("/api/message")
def get_message():
    message = query.get_message()
    if message:
        
        return message,200
    else:
        return "",501
