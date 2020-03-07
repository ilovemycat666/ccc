from flask import Flask, render_template, request, url_for, current_app, g, redirect, session
import mysql.connector
from passlib.hash import pbkdf2_sha256
from werkzeug.debug import DebuggedApplication
from nba_api.stats.static import players, teams

app = Flask(__name__)


app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
app.debug = True
app.secret_key = "SushiMan1"



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        job = request.form.get("job")
        notes = request.form.get("notes")

        return f"got em {job}, {notes}!"
    else:
        if "user" in session:
            user = session["user"]
            return render_template("index.html", user=user)
        else:
            return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        mydb = mysql.connector.connect(
            host="localhost",
            user="ed",
            passwd="Se!nf3ld1",
            database="ccc"
            )
        mycursor = mydb.cursor()

        sql = "SELECT password FROM clients WHERE username = %s"
        val = (username,)
        mycursor.execute(sql, val)

        data = mycursor.fetchone()
        data = str(data)
        mydb.commit()

        meta = (data.strip("('',)"))


        if pbkdf2_sha256.verify(password, meta):
            session["user"] = username
            session ["pass"] = password
            return redirect (url_for("index"))
        else:
            return "your account credentials don't match our records"
    else:
        return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user", None)
    session.pop("pass", None)
    return redirect (url_for("index"))


@app.route("/administrator", methods=["GET", "POST"])
def administrator():
    if request.method == "POST":
        mydb = mysql.connector.connect(
            host="localhost",
            user="ed",
            passwd="Se!nf3ld1",
            database="ccc"
            )
        mycursor = mydb.cursor()

        userinfo = request.form.get("userinfo")
        all = str(userinfo)
        all = all.lower()
        if all == 'all':
            mycursor.execute("SELECT id,name1,name2,phone,email,username,pet,notes FROM clients")
            query = mycursor.fetchall()
            return render_template("admin.html", query=query, userinfo="All")
        mycursor.execute(f"SELECT id,name1,name2,phone,email,username,pet,notes FROM clients WHERE id = %s OR name1 = %s OR name2 = %s OR phone = %s OR email = %s OR username = %s OR pet = %s OR notes = %s", (userinfo, userinfo, userinfo, userinfo, userinfo, userinfo, userinfo, userinfo))
        query = mycursor.fetchall()
        return render_template("admin.html", query=query, userinfo=userinfo)
    else:
        return render_template("admin.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name1 = request.form.get('name1')
        name2 = request.form.get('name2')
        phone = request.form.get('phone')
        email = request.form.get('email')
        username = request.form.get('username')
        unhash = request.form.get('password')
        password = pbkdf2_sha256.hash(unhash)
        confirm = request.form.get("confirm")

        if name1 == True:
            return "Please complete all fields"
        if confirm != unhash:
            return "Passwords don't match"

        mydb = mysql.connector.connect(
            host="localhost",
            user="ed",
            passwd="Se!nf3ld1",
            database="ccc"
            )

        mycursor = mydb.cursor()


        sql = "INSERT INTO clients (name1, name2, phone, email, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name1, name2, phone, email, username, password)
        mycursor.execute(sql, val)

        mydb.commit()
        session["user"] = username
        session ["pass"] = password
        return redirect (url_for("index"))
    else:
        return render_template("test.html")

@app.route('/nba', methods=["POST", "GET"])
def nba():
    if request.method == "POST":
        nba_player = request.form.get('nba_player')
        player_dict = players.get_players()
        for player in player_dict:
            if player["full_name"] == nba_player:
                nba_player_values = []
                for value in player.values():
                    nba_player_values.append(value)
                    

                return render_template("nba.html", nba_player_values=nba_player_values, nba_player=nba_player)

        
    else:
        return render_template("nba.html")







if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')

