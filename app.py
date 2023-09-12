from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.Error as err:
        print(err)
    return conn


@app.route("/books", methods=["GET", "POST"])
def books():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM book")
        books = cursor.fetchall()

        if books is not None:
            return jsonify(books)
        else:
            return jsonify({"message": "No books available"})

    if request.method == "POST":
        author = request.form["author"]
        language = request.form["language"]
        title = request.form["title"]

        sql = """INSERT INTO book(author,language,title) VALUES(?,?,?)"""
        cursor = cursor.execute(sql, (author, language, title))
        conn.commit()
        return f"Book With the id: {cursor.lastrowid} created successfully"


# @app.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
# def onebook(id):
#     if request.method == "GET":
#         for book in books_list:
#             if book["id"] == id:
#                 return jsonify(book)
#             pass
#     if request.method == "PUT":
#         for book in books_list:
#             if book["id"] == id:
#                 book["author"] = request.form["author"]
#                 book["language"] = request.form["language"]
#                 book["title"] = request.form["title"]

#                 return jsonify(book)


#     if request.method == "DELETE":
#         for book in books_list:
#             if book["id"] == id:
#                 books_list.remove(book)
#                 return jsonify(books_list)
def find_book_byId(id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor = cursor.execute("SELECT * FROM book WHERE id=?", (id,))
    book = cursor.fetchone()
    if book is not None:
        return book
    else:
        return "no such book"


@app.route("/book/<int:id>", methods=["DELETE", "PATCH", "GET"])
def One(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = find_book_byId(id)

    if request.method == "DELETE":
        if book is not None:
            cursor.execute("DELETE FROM book WHERE id=?", (id,))
            conn.commit()
            return jsonify(
                {"message": "Book deleted successfully", "deleted_book": book}
            )
        else:
            return {"error": "No such Book"}

    if request.method == "PATCH":
        new_id = request.form["id"]
        new_author = request.form["author"]
        new_language = request.form["language"]
        new_title = request.form["title"]
        if book is not None:
            cursor.execute(
                "UPDATE book SET id=?,author=?,language=?, title=? where id=? ",
                (new_id, new_author, new_language, new_title, id),
            )
            conn.commit()
            return jsonify(
                {"message": "Bookd updated successfully", "updated book": book}
            )
        else:
            return {"error": "No such book"}

    if request.method == "GET":
        return jsonify(find_book_byId(id))


if __name__ == "__main__":
    app.run(debug=True)
