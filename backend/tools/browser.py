from playwright.sync_api import sync_playwright


PORTAL_URL = "http://127.0.0.1:5001"


def save_payment(invoice_number, amount, due_date):

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        print("Opening company portal...")

        page.goto(PORTAL_URL)

        print("Portal opened.")

        # Fill the payment form
        page.locator("#invoice_number").fill(invoice_number)
        page.locator("#amount").fill(amount)
        page.locator("#due_date").fill(due_date)

        print("Payment details entered.")

        # Click Save Payment
        page.get_by_role(
            "button",
            name="Save Payment"
        ).click()

        print("Save Payment clicked.")

        # Give the portal time to save and reload
        page.wait_for_timeout(1500)

        # Verify that the saved payment appears on the page
        page.wait_for_load_state("networkidle")

        payment_text = page.locator("body").inner_text()

        print()
        print("Checking saved payment...")

        if (
            invoice_number in payment_text
            and amount in payment_text
            and due_date in payment_text
        ):

            print("VERIFICATION SUCCESSFUL!")
            print("Invoice:", invoice_number)
            print("Amount:", amount)
            print("Due Date:", due_date)

            verified = True

        else:

            print("VERIFICATION FAILED!")

            verified = False

        print()
        print("Keeping browser open for 5 seconds...")

        page.wait_for_timeout(5000)

        browser.close()

        return verified


if __name__ == "__main__":

    result = save_payment(
        "AC-2026-002",
        "INR 87500",
        "2026-11-05"
    )

    print()
    print("Final verification result:", result)