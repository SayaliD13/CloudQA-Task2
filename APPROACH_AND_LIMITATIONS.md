# Approach and Limitations

## Approach

For this project, I used Python, Playwright, and Google Gemini AI to build a tool that can run browser tests from instructions written in plain English.

The idea was to make website testing easier by allowing the user to describe what they want to check instead of writing browser automation steps manually.

The tool works in the following way:

1. The user provides a website URL and a test instruction in plain English.
2. The AI planner sends the instruction to Gemini and gets a list of browser steps in JSON format.
3. The safety module checks the generated steps before they are executed.
4. Playwright opens the website in Chromium and performs the required actions.
5. The executor checks whether the expected result is found, such as visible text, page title, or URL.
6. The reporter displays the final PASS or FAIL result and saves the test details in a JSON report.

I kept the code in separate Python files so that browser handling, AI planning, element finding, test execution, safety checks, and reporting can be managed separately.

## Why I Chose This Approach

I used Gemini to understand the test instruction because users may describe the same test in different ways.

Playwright handles the actual browser work because it can open websites, interact with page elements, and verify results.

Keeping these parts separate makes the code easier to understand, test, and update.

## Limitations

There are some limitations in the current version:

- Gemini may sometimes misunderstand an instruction or generate incorrect test steps.
- The result depends on the availability of the Gemini API, internet connection, and API limits.
- Website layouts and element names can change, which may affect element detection.
- Some websites require login details, OTP, CAPTCHA, or other special access.
- The tool may stop if it cannot identify one clear matching element.
- The safety module checks common sensitive actions, but it cannot detect every possible risky instruction.
- A website or network problem can also cause a test to fail.
- The current version supports a defined set of browser actions and does not guarantee that every website or test case will work.

## Conclusion

This project helped me understand how AI can be used with browser automation to convert simple instructions into website tests.

The current version provides a basic working approach for generating test steps, running them in a browser, and reporting the result. More browser actions and better handling of different website layouts can be added in future improvements.