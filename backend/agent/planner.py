def create_plan(task):
    """
    Convert a natural-language task into a sequence
    of actions for the autonomous worker.
    """

    task_lower = task.lower()

    plan = []

    if "invoice" in task_lower:

        plan.append({
            "step": 1,
            "action": "find_latest_invoice",
            "description": "Find the latest invoice for the requested company."
        })

        plan.append({
            "step": 2,
            "action": "extract_invoice_data",
            "description": "Extract invoice number, amount and due date."
        })

        if "payment" in task_lower or "save" in task_lower:

            plan.append({
                "step": 3,
                "action": "save_payment",
                "description": "Enter invoice payment information into the internal portal."
            })

        if "verify" in task_lower or "check" in task_lower:

            plan.append({
                "step": 4,
                "action": "verify_result",
                "description": "Verify that the payment was successfully saved."
            })

    return plan


if __name__ == "__main__":

    task = (
        "Find the latest invoice from Acme Corp, "
        "save the payment in the internal system, "
        "and verify that it was saved."
    )

    plan = create_plan(task)

    print("Generated plan:")
    print()

    for step in plan:
        print(
            f"{step['step']}. "
            f"{step['action']} - "
            f"{step['description']}"
        )