from locator import LocatorHelper


class TestExecutor:
    def __init__(self, page):
        self.page = page
        self.locators = LocatorHelper(page)

    def run(self, steps, starting_url):
        self.page.goto(starting_url, wait_until="domcontentloaded")

        verified_checks = 0
        completed_steps = []

        for number, step in enumerate(steps, start=1):
            action = step.get("action", "")
            by = step.get("by", "text")
            role = step.get("role", "button")
            target = str(step.get("target", ""))
            value = str(step.get("value", ""))

            try:
                if action == "navigate":
                    self.page.goto(target, wait_until="domcontentloaded")

                elif action == "click":
                    self.locators.get(by, target, role).click()

                elif action == "fill":
                    self.locators.get(by, target, role).fill(value)

                elif action == "select":
                    self.locators.get(by, target, role).select_option(label=value)

                elif action == "check":
                    self.locators.get(by, target, role).check()

                elif action == "uncheck":
                    self.locators.get(by, target, role).uncheck()

                elif action == "press":
                    self.locators.get(by, target, role).press(value)

                elif action == "assert_text":
                    if not self.page.get_by_text(target, exact=False).first.is_visible():
                        raise AssertionError("Expected text is not visible: " + target)
                    verified_checks += 1

                elif action == "assert_visible":
                    if not self.locators.get(by, target, role).is_visible():
                        raise AssertionError("Element is not visible: " + target)
                    verified_checks += 1

                elif action == "assert_title":
                    actual_title = self.page.title()
                    if target.casefold() not in actual_title.casefold():
                        raise AssertionError(
                            "Expected title text '" + target +
                            "', but actual title was '" + actual_title + "'."
                        )
                    verified_checks += 1

                elif action == "assert_url":
                    if target.casefold() not in self.page.url.casefold():
                        raise AssertionError(
                            "Expected URL to contain '" + target +
                            "', but actual URL was '" + self.page.url + "'."
                        )
                    verified_checks += 1

                elif action == "wait":
                    milliseconds = int(value)
                    self.page.wait_for_timeout(milliseconds)

                else:
                    raise ValueError("Unsupported action: " + str(action))

                completed_steps.append({
                    "step": number,
                    "action": action,
                    "status": "PASS"
                })

            except Exception as error:
                completed_steps.append({
                    "step": number,
                    "action": action,
                    "status": "FAIL",
                    "reason": str(error)
                })
                raise RuntimeError(
                    "Step " + str(number) + " (" + action + ") failed: " + str(error)
                ) from error

        if verified_checks == 0:
            raise RuntimeError(
                "No verification step was completed. The test cannot pass."
            )

        return verified_checks, completed_steps
