from flask import Flask, render_template
import sqlalchemy
import db_helper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host:port/dbname'
#FIX URL

db = db_helper.dbHelper()


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")



app.run()