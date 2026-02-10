from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "susu_secret_key"

def get_db():
    return sqlite3.connect("users.db")

@app.route("/")
def home():
   
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()

        if user:
            session["user_id"] = user[0]
            return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        db.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/history", methods=["GET", "POST"])
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        height = float(request.form["height"])
        weight = float(request.form["weight"])

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO history (user_id, height, weight) VALUES (?, ?, ?)",
                    (session["user_id"], height, weight))
        db.commit()

        return redirect(url_for("home"))

    return render_template("history.html")

@app.route("/analyze")
def analyze():
    # if "user_id" not in session:
    #     return redirect(url_for(""))
    return render_template("analyze.html")

@app.route("/doctors")
def doctors():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("doctors.html")

if __name__ == "__main__":
    app.run(debug=True)
