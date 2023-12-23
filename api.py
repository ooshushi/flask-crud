from flask import Flask, make_response, jsonify, request, render_template, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "kokororokorokoko"
app.config["MYSQL_DB"] = "loan_management"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["SECRET_KEY"] = "secretkey"

mysql = MySQL(app)

users = {'username': 'password'}

def data_fetch(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
def home():
    if session.get("username"):
        return redirect(url_for("get_loan_contracts"))
    return render_template("base.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('get_loan_contracts'))

    return render_template("base.html", message="Invalid credentials")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route("/loancontract", methods=["GET"])
def get_loan_contracts():
    query = """SELECT * FROM loancontract;"""
    data = data_fetch(query)
    return make_response(jsonify(data), 200)

@app.route("/loancontract", methods=["POST"])
def add_loan_contract():
    info = request.get_json()
    date_contract_starts = info['dateContractStarts']
    date_contract_ends = info['dateContractEnds']
    interest_rate = info['interestRate']
    loan_amount = info['loanAmount']
    loan_payment_amount_due = info['loanPaymentAmountDue']
    loan_payment_frequency = info['loanPaymentFrequency']
    loan_payment_due_date = info['loanPaymentDueDate']

    query = """INSERT INTO `loan_management`.`loancontract` 
                (`dateContractStarts`, `dateContractEnds`, `interestRate`, `loanAmount`, `loanPaymentAmountDue`, `loanPaymentFrequency`, `loanPaymentDueDate`) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    params = (date_contract_starts, date_contract_ends, interest_rate, loan_amount, loan_payment_amount_due, loan_payment_frequency, loan_payment_due_date)
    data_fetch(query, params)
    mysql.connection.commit()
    return make_response(jsonify({"message": "Loan contract added successfully"}), 201)

@app.route("/loancontract/<int:id>", methods=["PUT"])
def update_loan_contract(id):
    info = request.get_json()
    date_contract_starts = info['dateContractStarts']
    date_contract_ends = info['dateContractEnds']
    interest_rate = info['interestRate']
    loan_amount = info['loanAmount']
    loan_payment_amount_due = info['loanPaymentAmountDue']
    loan_payment_frequency = info['loanPaymentFrequency']
    loan_payment_due_date = info['loanPaymentDueDate']

    query = """UPDATE `loan_management`.`loancontract` SET 
                `dateContractStarts` = %s, 
                `dateContractEnds` = %s, 
                `interestRate` = %s, 
                `loanAmount` = %s, 
                `loanPaymentAmountDue` = %s, 
                `loanPaymentFrequency` = %s, 
                `loanPaymentDueDate` = %s 
                WHERE `contractID` = %s"""
    params = (date_contract_starts, date_contract_ends, interest_rate, loan_amount, loan_payment_amount_due, loan_payment_frequency, loan_payment_due_date, id)
    data_fetch(query, params)
    mysql.connection.commit()
    return make_response(jsonify({"message": "Loan contract updated successfully"}), 200)

@app.route("/loancontract/<int:id>", methods=["DELETE"])
def delete_loan_contract(id):
    query = """DELETE FROM `loan_management`.`loancontract` WHERE (`contractID` = %s);"""
    params = (id,)
    data_fetch(query, params)
    mysql.connection.commit()
    return make_response(jsonify({"message": "Loan contract deleted successfully"}), 200)

if __name__ == "__main__":
    app.run(debug=True)