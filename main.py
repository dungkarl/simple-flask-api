from flask import Flask, jsonify, request
from flask import abort, make_response, url_for
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

app = Flask(__name__)

users = [
	{
		"id":1,
		"name":"Dung Karl",
		"age":30,
		"university": "Thuy Loi",
		"major":"Computer Science",
		"updated": False
	},
	{
		"id":2,
		"name":"John Doe",
		"age":25,
		"university": "MIT",
		"major":"Software Engineer",
		"updated": False
	}

]


def make_public_user(user):
	new_user = {}
	for field in user:
		if field == 'id':
			new_user["uri"] == url_for("get_user", user_id=user["id"], _external=True)
		else:
			new_user[field] == user[field]
	return new_user

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not Found'}), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error':'Bad Request'}), 400)

@app.errorhandler(500)
def internal_server(error):
	return make_response(jsonify({'error':'Internal Server Error'}), 500)

@app.route('/')
def index():
	return "Home Page"

@app.route('/api/1.0/users', methods=['POST'])
def create_user():
	if not request.json or not "name" in request.json:
		abort(400)

	user = {
		"id": users[-1]["id"] + 1,
		"name":request.json["name"],
		"age":request.json.get("age", 0),
		"university":request.json.get("university", ""),
		"major":request.json.get("major", ""),
		"updated":False
	}
	users.append(user)
	return jsonify({'user':user}, 201)


@app.route('/api/1.0/users', methods=['GET'])
def get_users():

	return jsonify({'users':users})


@app.route('/api/1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
	user = [user for user in users if user['id'] == user_id]

	if len(user)== 0:
		abort(404)
	return jsonify({'user': user[0]})


@app.route('/api/1.0/users/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
	user = [user for user in users if user['id'] == user_id]

	if len(user) == 0:
		abort(404)
	# if not request.json:
	# 	abort(400)
	# if "name" in request.json and type(request.json["name"])is not unicode:
	# 	abort(400)
	# if "age" in request.json and type(request.json["age"]) is not unicode:
	# 	abort(400)
	# if "university" in request.json and type(request.json["university"]) is not unicode:
	# 	abort(400)
	# if "major" in request.json and type(request.json["major"]) is not unicode:
	# 	abort(400)
	

	user[0]["name"] = request.json.get("name", user[0]["name"])
	user[0]["age"] = request.json.get("age", user[0]["age"])
	user[0]["university"] = request.json.get("university", user[0]["university"])
	user[0]["major"] = request.json.get("major", user[0]["major"])
	user[0]["updated"] = True
	return jsonify({'user':user[0]})

@app.route('/api/1.0/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	user = [user for user in users if user['id'] == user_id]
	if len(user) == 0:
		abort(404)
	users.remove(user[0])
	return jsonify({'Deleted': True})

if __name__ == '__main__':
	app.run(debug=True)