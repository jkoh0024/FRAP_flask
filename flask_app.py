from flask import Flask
from flask import abort, request

from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

numbers = [
    {'id': 1, 'number': 28, 'description': '2nd perfect number'},
    {'id': 2, 'number': 51, 'description': "Looks prime but isn't"},
    {'id': 3, 'number': 28, 'description': '7th triangle number'},
]
top_number = 3


@api.resource('/')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


todos = {1: "React.js", 2: "Flask", 3: "Flask-Restful", 4: "SQL", 5: "Heroku", 6: "Now you have completed FRAP engineering"}


@api.resource('/todo')
class TodoList(Resource):
    def get(self):
        return {"todo_list": todos}

    def post(self):
        todos[max(todos.keys()) + 1] = request.form['data']
        return "successful"


@api.resource('/todo/<int:todo_id>')
class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


@api.resource('/numbers')
class Numbers(Resource):
    """Get the full list of favorite numbers"""

    def get(self):
        return numbers

    def post(self):
        """Post a new favorite number; server assigns the id"""

        if not ('number' in request.form and 'description' in request.form):
            abort(400, "Payload must include number and description")
        global top_number
        top_number += 1
        numbers.append({'id': top_number,
                        'number': int(request.form['number']),
                        'description': request.form['description']})
        return top_number


@api.resource('/number/<int:id>')
class Number(Resource):
    def get(self, id):
        """Get a single favorite number selected by its id"""
        matches = [number for number in numbers if number['id'] == id]
        # if len(matches) == 0:
        #     abort(404, "Unique id {} not found".format(id))
        return matches[0]


if __name__ == '__main__':
    app.run(debug=True)
