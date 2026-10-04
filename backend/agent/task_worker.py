import re


from backend.agent.planner import create_plan
from backend.agent.invoice_analyzer import find_latest_invoice
from backend.tools.browser import save_payment


def execute_task(task):
    print("=" * 60)
    print("AUTONOMOUS AI TASK WORKER")
    print("=" * 60)
    print()
    print("Task received:")
    print(task)

    # ---------------------------------------------------------
    # STEP 1: CREATE PLAN
    # ---------------------------------------------------------
    print()
    print("[1] Creating task plan...")

    plan = create_plan(task)

    if not plan:
        return {
            "success": False,
            "message": "I could not create a plan for this task."
        }

    print("Plan created:")

    for step in plan:
        print(
            f"  {step['step']}. "
            f"{step['action']} - "
            f"{step['description']}"
        )

    # ---------------------------------------------------------
    # STEP 2: FIND LATEST INVOICE
    # ---------------------------------------------------------
    print()
    print("[2] Searching for latest invoice...")

    company_match = re.search(
        r"invoice from ([A-Za-z0-9 &.-]+?)(?:,| and|\.|$)",
        task,
        re.IGNORECASE
    )

    company_name = company_match.group(1).strip() if company_match else "Acme Corp"

    print(f"Company identified: {company_name}")

    invoice = find_latest_invoice(company_name)

    if not invoice:
        return {
            "success": False,
            "message": "No Acme Corp invoice was found."
        }

    print("Latest invoice found:")
    print(f"Invoice: {invoice['invoice_number']}")
    print(f"Date: {invoice['invoice_date']}")
    print(f"Amount: {invoice['amount']}")
    print(f"Due Date: {invoice['due_date']}")

    # ---------------------------------------------------------
    # STEP 3: SAVE PAYMENT WITH RETRY
    # ---------------------------------------------------------
    print()
    print("[3] Executing payment action...")
    
    print()
    print("SAFETY CHECK")
    print("-" * 60)
    print("The worker is about to submit a payment:")
    print(f"Invoice: {invoice['invoice_number']}")
    print(f"Amount: {invoice['amount']}")
    print(f"Due Date: {invoice['due_date']}")
    print()

    approval = input("Approve this payment? (yes/no): ").strip().lower()

    if approval not in ("yes", "y"):
        print()
        print("Payment action cancelled by user.")

        return {
            "success": False,
            "invoice_number": invoice["invoice_number"],
            "plan": plan,
            "attempts": 0,
            "message": "Payment was not submitted because user approval was not provided."
        }
    verified = False
    last_error = None
    max_attempts = 2

    for attempt in range(1, max_attempts + 1):

        print()
        print(f"Attempt {attempt} of {max_attempts}...")

        try:
            verified = save_payment(
                invoice["invoice_number"],
                invoice["amount"],
                invoice["due_date"]
            )

            if verified:
                print("Payment action completed successfully.")
                break

            print("Payment verification failed.")

        except Exception as error:
            last_error = str(error)

            print("Payment action failed.")
            print(f"Error: {error}")

        if not verified and attempt < max_attempts:
            print("Retrying with the same task...")

    # ---------------------------------------------------------
    # STEP 4: FINAL VERIFICATION
    # ---------------------------------------------------------
    print()
    print("[4] Verifying final result...")

    if verified:

        print("VERIFICATION SUCCESSFUL!")
        print("Payment successfully saved and verified.")

        evidence = {
            "invoice_found": True,
            "invoice_source": invoice["file"],
            "payment_submitted": True,
            "payment_verified": True,
            "verified_invoice_number": invoice["invoice_number"],
            "verified_amount": invoice["amount"],
            "verified_due_date": invoice["due_date"]
        }

        return {
            "success": True,
            "invoice_number": invoice["invoice_number"],
            "amount": invoice["amount"],
            "due_date": invoice["due_date"],
            "plan": plan,
            "attempts": attempt,
            "evidence": evidence,
            "message": "Task completed and verified successfully."
        }

    print("VERIFICATION FAILED!")

    return {
        "success": False,
        "invoice_number": invoice["invoice_number"],
        "plan": plan,
        "attempts": attempt,
        "error": last_error,
        "message": "Task failed after retry attempts."
    }


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("AUTONOMOUS AI TASK WORKER")
    print("=" * 60)
    print()
    print("Enter a task for the worker.")
    print("Example:")
    print(
        "Find the latest invoice from Acme Corp, "
        "save the payment in the internal system, "
        "and verify that it was saved."
    )
    print()

    task = input("Enter task: ").strip()

    if not task:
        print("No task was provided.")
        exit()

    result = execute_task(task)

    print()
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    if result["success"]:
        print()
        print("TASK COMPLETION REPORT")
        print("=" * 60)
        print("Status: VERIFIED")
        print(f"Invoice: {result['invoice_number']}")
        print(f"Amount: {result['amount']}")
        print(f"Due Date: {result['due_date']}")
        print(f"Attempts: {result['attempts']}")
        print()
        print("Evidence:")
        print("- Invoice successfully located")
        print(f"- Source: {result['evidence']['invoice_source']}")
        print("- Payment submitted to internal portal")
        print("- Payment presence verified")
        print("- Invoice number, amount and due date matched")
        print()
        print("FINAL STATUS: TASK COMPLETED AND VERIFIED")

    else:
        print()
        print("TASK COMPLETION REPORT")
        print("=" * 60)
        print("Status: FAILED")
        print(result["message"])

    print()
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    if result["success"]:
        print()
        print("TASK COMPLETION REPORT")
        print("=" * 60)
        print(f"Status: VERIFIED")
        print(f"Invoice: {result['invoice_number']}")
        print(f"Amount: {result['amount']}")
        print(f"Due Date: {result['due_date']}")
        print(f"Attempts: {result['attempts']}")
        print()
        print("Evidence:")
        print("- Invoice successfully located")
        print(f"- Source: {result['evidence']['invoice_source']}")
        print("- Payment submitted to internal portal")
        print("- Payment presence verified")
        print("- Invoice number, amount and due date matched")
        print()
        print("FINAL STATUS: TASK COMPLETED AND VERIFIED")
    else:
        print()
        print("TASK COMPLETION REPORT")
        print("=" * 60)
        print("Status: FAILED")
        print(result["message"])