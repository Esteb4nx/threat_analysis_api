# api.py
from flask import Flask, jsonify
from analysis import (
    analyze_risk, analyze_summary, analyze_user_behavior, load_data, analyze_unauthorized_access, analyze_out_of_hours_activity,
    analyze_external_transfers, analyze_login_failures, cross_reference_out_of_hours_and_external_transfers,
    cross_reference_failed_logins_and_unauthorized_access, cross_reference_multiple_logins_and_external_transfers,
)

app = Flask(__name__)

@app.route('/analyze/unauthorized_access', methods=['GET'])
def unauthorized_access():
    data = load_data()
    analysis = analyze_unauthorized_access(data)
    return jsonify(analysis)

@app.route('/analyze/out_of_hours', methods=['GET'])
def out_of_hours():
    data = load_data()
    analysis = analyze_out_of_hours_activity(data)
    return jsonify(analysis)

@app.route('/analyze/external_transfers', methods=['GET'])
def external_transfers():
    data = load_data()
    analysis = analyze_external_transfers(data)
    return jsonify(analysis)

@app.route('/analyze/login_failures', methods=['GET'])
def login_failures():
    data = load_data()
    analysis = analyze_login_failures(data)
    return jsonify(analysis)

@app.route('/cross_reference/out_of_hours_external_transfers', methods=['GET'])
def out_of_hours_external_transfers():
    data = load_data()
    analysis = cross_reference_out_of_hours_and_external_transfers(data)
    return jsonify(analysis)

@app.route('/cross_reference/failed_logins_unauthorized_access', methods=['GET'])
def failed_logins_unauthorized_access():
    data = load_data()
    analysis = cross_reference_failed_logins_and_unauthorized_access(data)
    return jsonify(analysis)

@app.route('/cross_reference/multiple_logins_external_transfers', methods=['GET'])
def multiple_logins_external_transfers():
    data = load_data()
    analysis = cross_reference_multiple_logins_and_external_transfers(data)
    return jsonify(analysis)

@app.route('/analyze/risk', methods=['GET'])
def risk_analysis():
    data = load_data()
    analysis = analyze_risk(data)
    return jsonify(analysis)

@app.route('/analyze/summary', methods=['GET'])
def summary():
    data = load_data()
    analysis = analyze_summary(data)
    return jsonify(analysis)

@app.route('/analyze/user_behavior', methods=['GET'])
def user_behavior():
    data = load_data()
    analysis = analyze_user_behavior(data)
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True)
