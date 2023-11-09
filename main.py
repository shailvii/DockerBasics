from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


class Note:
    def __init__(self):
        self.notes = {}  # Dictionary to store notes (username -> list of items)

    def add_item(self, username, item):
        if username not in self.notes:
            self.notes[username] = []

        self.notes[username].append(item)
        return item

    def view_items(self, username):
        if username in self.notes:
            items = self.notes[username]
            if items:
                return items
            else:
                return []
        else:
            return f"User '{username}' does not exist."

    def delete_item(self, username, index):
        if username in self.notes:
            items = self.notes[username]
            if items:
                try:
                    index = int(index) - 1
                    if 0 <= index < len(items):
                        deleted_item = items.pop(index)
                        return f"deleted: {deleted_item}"
                    else:
                        return "Invalid item number."
                except ValueError:
                    return "Invalid input. Please enter a valid item number."
            else:
                return []
        else:
            return f"User '{username}' does not exist."


note = Note()


@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    username = data.get('username')
    item = data.get('item')
    response = note.add_item(username, item)
    return jsonify({
        'username': username,
        'message': response
    })


@app.route('/view_items/<username>', methods=['GET'])
def view_items(username):
    response = note.view_items(username)
    return jsonify({
        'username': username,
        'message': response
    })


@app.route('/delete_item/<username>/<index>', methods=['DELETE'])
def delete_item(username, index):
    response = note.delete_item(username, index)
    return jsonify({
        'username': username,
        'message': response
    })


if __name__ == "__main__":
    app.run(debug=True)