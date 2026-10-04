from pathlib import Path


INVOICE_FOLDER = Path("mock_company/invoices")


def list_invoice_files():
    """Return all invoice files in the invoice folder."""
    return list(INVOICE_FOLDER.glob("*.txt"))


def read_invoice(file_path):
    """Read and return the contents of an invoice."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Invoice not found: {file_path}")

    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    files = list_invoice_files()

    print("Available invoices:")

    for file in files:
        print(f"- {file}")

        content = read_invoice(file)

        print(content)
        print("-" * 40)