BLOCKED_ACTIONS = {
    "delete", "remove", "purchase", "pay", "checkout",
    "send", "transfer", "close_account", "change_password"
}


def check_plan(steps):
    if not isinstance(steps, list) or len(steps) == 0:
        raise ValueError("The test plan is empty.")

    allowed_actions = {
        "navigate", "click", "fill", "select", "check", "uncheck",
        "press", "assert_text", "assert_visible", "assert_title",
        "assert_url", "wait"
    }

    allowed_locators = {
        "label", "placeholder", "role", "text", "test_id", "css"
    }

    has_check = False

    for number, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            raise ValueError("Step " + str(number) + " is not a valid object.")

        action = step.get("action")
        if action not in allowed_actions:
            raise ValueError("Step " + str(number) + " has an unsupported action.")

        target = str(step.get("target", ""))
        value = str(step.get("value", ""))

        combined_text = (target + " " + value).lower()
        for blocked in BLOCKED_ACTIONS:
            if blocked in combined_text and action in {
                "click", "fill", "press", "navigate"
            }:
                raise ValueError(
                    "The plan may perform a sensitive action. "
                    "This tool stops instead of doing it."
                )

        if action in {"click", "fill", "select", "check", "uncheck", "press", "assert_visible"}:
            by = step.get("by", "text")
            if by not in allowed_locators:
                raise ValueError("Step " + str(number) + " has an unsupported locator.")

        if action in {"assert_text", "assert_visible", "assert_title", "assert_url"}:
            has_check = True

        if action == "wait":
            try:
                wait_time = int(value)
            except ValueError as error:
                raise ValueError("Wait time must be a number.") from error

            if wait_time < 0 or wait_time > 5000:
                raise ValueError("Wait time must be between 0 and 5000 milliseconds.")

    if not has_check:
        raise ValueError("The plan must include at least one verification step.")
