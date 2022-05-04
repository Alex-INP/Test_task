import json
import requests
import sys

sys.path.append("..")

from flask import Flask, request
from sqlalchemy.exc import IntegrityError

from database.database import DatabaseOperator

app = Flask(__name__)
DB = DatabaseOperator()

@app.route('/', methods=["POST"])
def index():
	data = json.loads(request.get_data())
	if "questions_num" in data.keys() and type(data["questions_num"]) == int:
		for i in range(data["questions_num"]):
			while True:
				result = make_side_request()
				data = prepare_data(result)
				try:
					DB.add_question(data)
					break
				except IntegrityError:
					DB.session.rollback()

	return create_response_data(DB.get_last_record())


def make_side_request():
	return json.loads(requests.get("https://jservice.io/api/random?count=1").content)[0]


def prepare_data(data):
	return {"question_id": data["id"], "text": data["question"], "answer": data["answer"], "creation_date": data["created_at"]}


def create_response_data(db_object):
	return json.dumps({
		"question_id": db_object.question_id,
		"text": db_object.text,
		"answer": db_object.answer,
		"creation_date": db_object.creation_date.strftime("%d/%m/%Y, %H:%M:%S")
	})


app.run(host="0.0.0.0", port=5000)

