from flask import Flask, request, jsonify, render_template, abort
from flask import make_response, redirect, url_for
from flask_wtf import FlaskForm
from models import books
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config["SECRET_KEY"] = "tralala"
csrf = CSRFProtect()


#def create_app():
#    app = Flask(__name__)
#    csrf.init_app(app)


@app.route("/api/books/", methods=["GET"])
@csrf.exempt
def books_api():
    return jsonify(books.all())

@app.route("/api/books/", methods=["POST"])
@csrf.exempt
def add_book():
    if not request.json:
        abort(400)
    book = {
    'id': books.all()[-1]['id'] + 1,
    'title': request.json.get('title'),
    'author': request.json.get('author', ""),
    'read': False,
    'recommend': False
    }
    books.create(book)
    return jsonify({'book': book}), 201


@app.route("/books/<int:books_id>", methods=["GET"])
def get_book(books_id):
    book = books.get(books_id)
    if not book:
        abort(404)
    return jsonify({"book": book})


@app.route("/book/<int:book_id>", methods=['DELETE'])
def remove_books(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_books(book_id):
    book = books.get(book_id)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        ]):
        abort(400)
        book = {
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        }
        books.update(book_id, book)
        return jsonify({'book': book})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)
