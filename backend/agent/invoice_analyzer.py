from datetime import datetime
from backend.tools.file_reader import list_invoice_files, read_invoice


def extract_invoice_data(content):
    """Extract important fields from invoice text."""

    data = {}

    for line in content.splitlines():

        if line.startswith("Invoice Number:"):
            data["invoice_number"] = line.split(":", 1)[1].strip()

        elif line.startswith("Invoice Date:"):
            data["invoice_date"] = line.split(":", 1)[1].strip()

        elif line.startswith("Amount Due:"):
            data["amount"] = line.split(":", 1)[1].strip()

        elif line.startswith("Due Date:"):
            data["due_date"] = line.split(":", 1)[1].strip()

        elif line.startswith("Status:"):
            data["status"] = line.split(":", 1)[1].strip()

    return data


def find_latest_invoice(company_name):
    """Find the latest invoice for a company."""

    invoices = []

    for file in list_invoice_files():

        content = read_invoice(file)
        data = extract_invoice_data(content)

        if company_name.lower() in content.lower():

            data["file"] = str(file)
            invoices.append(data)

    if not invoices:
        return None

    invoices.sort(
        key=lambda x: datetime.strptime(
            x["invoice_date"],
            "%Y-%m-%d"
        ),
        reverse=True
    )

    return invoices[0]


if __name__ == "__main__":

    result = find_latest_invoice("Acme Corp")

    if result:
        print("Latest invoice found:")
        print()
        print(f"Invoice Number: {result['invoice_number']}")
        print(f"Invoice Date: {result['invoice_date']}")
        print(f"Amount: {result['amount']}")
        print(f"Due Date: {result['due_date']}")
        print(f"File: {result['file']}")
    else:
        print("No invoice found.")