
import argparse

from ai_planner import AIPlanner
from browser_manager import BrowserManager
from executor import TestExecutor
from reporter import save_report
from safety import check_plan


def read_arguments():
    parser = argparse.ArgumentParser(
        description="Run plain-English browser tests."
    )

    parser.add_argument(
        "--url",
        required=True,
        help="Website URL where the test should start."
    )

    parser.add_argument(
        "--test",
        required=True,
        help="Test case written in plain English."
    )

    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run the browser without showing its window."
    )

    return parser.parse_args()


def main():
    args = read_arguments()

    result = {
        "test_case": args.test,
        "starting_url": args.url,
        "status": "FAIL",
        "reason": "",
        "planned_steps": [],
        "completed_steps": [],
        "verified_checks": 0,
        "final_url": "",
        "page_title": "",
        "screenshot": ""
    }

    browser = BrowserManager()
    page = None

    try:
        print("\nMaking a test plan with AI...")

        planner = AIPlanner()
        steps = planner.create_plan(args.test, args.url)

        check_plan(steps)
        result["planned_steps"] = steps

        print("AI created", len(steps), "steps.")

        print("\nStarting browser...")

        page = browser.start(headless=args.headless)

        executor = TestExecutor(page)
        checks, completed = executor.run(steps, args.url)

        result["verified_checks"] = checks
        result["completed_steps"] = completed
        result["status"] = "PASS"
        result["reason"] = "All planned actions and checks passed."

    except Exception as error:
        result["reason"] = str(error)
        print("\nTEST FAILED:", error)

        if page is not None:
            try:
                result["final_url"] = page.url
                result["page_title"] = page.title()

                screenshot = browser.save_failure_screenshot()
                result["screenshot"] = screenshot

            except Exception:
                pass

    finally:
        if page is not None:
            try:
                result["final_url"] = page.url
                result["page_title"] = page.title()
            except Exception:
                pass

        try:
            report_file = save_report(result)

            print("\n===================================")
            print("TEST RESULT:", result["status"])
            print("Verified checks:", result["verified_checks"])
            print("Report:", report_file)

            if result["screenshot"]:
                print("Screenshot:", result["screenshot"])

            print("===================================\n")

            if page is not None and not args.headless:
                try:
                    input(
                        "Browser is still open. "
                        "Press ENTER when you want to close it..."
                    )
                except (EOFError, KeyboardInterrupt):
                    print("\nClosing browser...")

        finally:
            browser.close()

    if result["status"] == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
