from flask import Flask, render_template, url_for, request
import sqlite3 as sq

app = Flask(__name__)

with sq.connect("users.db") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS comments (
        sname TEXT NOT NULL,
        fname TEXT NOT NULL,
        patronymic TEXT,
        region BLOB,
        city BLOB,
        tel TEXT,
        email TEXT,
        text TEXT NOT NULL    
        )""")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/comment', methods=['POST', 'GET'])
def show_form():
    if request.method == "POST":

        con = None
        try:
            second_name = request.form['second_name']
            first_name = request.form['first_name']
            patronymic = request.form['patronymic']
            region = request.form['region']
            city = request.form['city']
            tel = request.form['tel']
            email = request.form['email']
            text = request.form['text']

            con = sq.connect("users.db")
            cur = con.cursor()

            cur.execute(
                "INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (second_name, first_name, patronymic, region, city, tel, email, text))
            con.commit()
            print("Коммент отправлен")
        except sq.Error as e:
            if con:
                con.rollback()
            print("Ошибка выполнения")
        finally:
            if con:
                con.close()
        return render_template("view.html")
    else:
        return render_template("comment.html")


@app.route('/view')
def comment():
    return render_template("view.html")


if __name__ == "__main__":
    app.run(debug=True)
