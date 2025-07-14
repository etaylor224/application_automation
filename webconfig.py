from flask import Flask, render_template
import sqlalchemy
import db_helper

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home_page():
    return render_template("index.html")

@app.route("/api/positions", methods=["GET","POST"])
def position_manager():
    if request.method == "POST":
        data = request.get_json()
        print("adding to database")
        try:
            row_id = db_helper.insert_into_search(data['position'], data['location'])
            data['id'] = row_id
            return jsonify(data), 201
        except Exception as e:
            print(f"Error: {e}")
            return "Error", 500
    if request.method == "GET":
        print("position call")
        #db_helper.populate_table_call("searchquery")


@app.route("/api/high-rated")
def high_rated_api():
    print("high table call")
    jobs = db_helper.populate_table_call("high_results")
    if len(jobs) > 0:
        data = db_helper.job_data_helper(jobs)
        return jsonify(data), 200
    else:
        return [{}], 204

@app.route("/api/low-rated")
def low_rated_api():
    print("low table call")
    jobs = db_helper.populate_table_call("low_results")
    if len(jobs) > 0:
        data = db_helper.job_data_helper(jobs)
        return jsonify(data), 200
    else:
        return [{}], 204

@app.route("/api/applied")
def applied_api():
    print("applied table call")
    jobs = db_helper.populate_table_call("applied")
    data = db_helper.job_data_helper(jobs)
    return jsonify(data), 200

app.run()
