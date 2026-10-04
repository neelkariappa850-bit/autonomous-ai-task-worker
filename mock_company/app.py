from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

invoices = [
    {
        "company": "Acme Corp",
        "invoice_number": "AC-2026-001",
        "amount": 125000,
        "due_date": "2026-10-15",
        "date": "2026-09-28"
    },
    {
        "company": "Acme Corp",
        "invoice_number": "AC-2026-002",
        "amount": 87500,
        "due_date": "2026-11-05",
        "date": "2026-10-01"
    }
]

payments = []


failure_injected = False


@app.route("/")
def home():
    return render_template("index.html", invoices=invoices, payments=payments)


@app.route("/api/invoices")
def get_invoices():
    return jsonify(invoices)


@app.route("/api/payments", methods=["POST"])
def create_payment():
    global failure_injected

    if not failure_injected:
        failure_injected = True
        return jsonify({
            "success": False,
            "error": "Temporary internal system failure"
        }), 500

    data = request.json

    payment = {
        "invoice_number": data.get("invoice_number"),
        "amount": data.get("amount"),
        "due_date": data.get("due_date"),
        "status": "Saved"
    }

    payments.append(payment)

    return jsonify({
        "success": True,
        "payment": payment
    })


@app.route("/api/payments")
def get_payments():
    return jsonify(payments)


if __name__ == "__main__":
    app.run(port=5001, debug=True)