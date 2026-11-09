class LocatorHelper:
    def __init__(self, page):
        self.page = page

    def get(self, by, target, role="button"):
        if not target:
            raise ValueError("The element target is empty.")

        if by == "label":
            locator = self.page.get_by_label(target, exact=False)
        elif by == "placeholder":
            locator = self.page.get_by_placeholder(target, exact=False)
        elif by == "role":
            locator = self.page.get_by_role(role, name=target, exact=False)
        elif by == "text":
            locator = self.page.get_by_text(target, exact=False)
        elif by == "test_id":
            locator = self.page.get_by_test_id(target)
        elif by == "css":
            locator = self.page.locator(target)
        else:
            raise ValueError("Unknown locator type: " + str(by))

        count = locator.count()
        if count != 1:
            raise ValueError(
                "Expected one matching element for '" + target +
                "', but found " + str(count) + "."
            )

        return locator
