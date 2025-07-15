from flask import Flask, render_template, request, jsonify
import db_helper
import main

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
        titles = db_helper.populate_table_call("searchquery")
        if len(titles) > 0:
            data = db_helper.positions_data_helper(titles)
            return jsonify(data), 200
        else:
            return [{}], 204

@app.route("/api/high-rated")
def high_rated_api():
    jobs = db_helper.populate_table_call("high_results")
    if len(jobs) > 0:
        data = db_helper.job_data_helper(jobs)
        return jsonify(data), 200
    else:
        return [{}], 204

@app.route("/api/low-rated")
def low_rated_api():
    jobs = db_helper.populate_table_call("low_results")
    if len(jobs) > 0:
        data = db_helper.job_data_helper(jobs)
        return jsonify(data), 200
    else:
        return [{}], 204

@app.route("/api/applied")
def applied_api():
    jobs = db_helper.populate_table_call("applied")
    data = db_helper.job_data_helper(jobs)
    return jsonify(data), 200

@app.route("/api/apply/<table>/<row_id>", methods=["POST"])
def apply_job(table, row_id):
    data = db_helper.get_row_by_id(table, row_id)
    applied = db_helper.insert_into_applied(data)
    if applied:
        db_helper.remove_row(table, row_id)
        return "", 200

@app.route("/api/remove/<table>/<row_id>", methods=["POST"])
def delete_row(table, row_id):
    try:
        db_helper.remove_row(table, row_id)
        return "", 200
    except Exception as e:
        print("ERROR")
        print(e)
        return "", 400

@app.route("/api/update-data", methods=["POST"])
def match_api():
    search_data = db_helper.populate_table_call("searchquery")
    for row in search_data:
        if row[2] != None or "":
            query = f"{row[1]} in {row[2]}"
        else:
            query = f"{row[1]}"
        main.run_matching(query)
    return "", 200

app.run(debug=True)
