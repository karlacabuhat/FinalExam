from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "IT5"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "conan_library"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/members", methods=["GET"])
def get_member():
    data = data_fetch("""select * from members""")
    return make_response(jsonify(data), 200)


@app.route("/members/<int:id>", methods=["GET"])
def get_member_by_id(id):
    data = data_fetch("""SELECT * FROM members where idmembers = {}""".format(id))
    return make_response(jsonify(data), 200)


@app.route("/members/<int:id>/categories", methods=["GET"])
def get_members_by_categories(id):
    data = data_fetch(
        """
        SELECT categories.categories, categories.idcategories
        FROM members 
        INNER JOIN c
        ON member.idmembers = libraries.idlibraries 
        INNER JOIN books
        ON libraries.idlibraries = books.isbn 
        WHERE members.idmembers = {}
    """.format(
            id
        )
    )
    return make_response(
        jsonify({"idmembers": id, "count": len(data), "books": data}), 200
    )


@app.route("/members", methods=["POST"])
def add_members():
    cur = mysql.connection.cursor()
    info = request.get_json()
    firstname = info["firstname"]
    lastname = info["lastname"]
    cur.execute(
        """ INSERT INTO members (firstname, lastname) VALUE (%s, %s)""",
        (firstname, lastname),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "members added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


@app.route("/members/<int:id>", methods=["PUT"])
def update_members(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    firstname = info["firstname"]
    lastname = info["lastname"]
    cur.execute(
        """ UPDATE members SET firstname = %s, lastname = %s WHERE idmembers = %s """,
        (firstname, lastname, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "members updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/members/<int:id>", methods=["DELETE"])
def delete_members(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM members where idmembers = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "members deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/members/format", methods=["GET"])
def get_params():
    param1 = request.args.get('idmembers')
    param2 = request.args.get('aaaa')
    return make_response(jsonify({"format":param1, "foo":param2}),200)


if __name__ == "__main__":
    app.run(debug=True)
