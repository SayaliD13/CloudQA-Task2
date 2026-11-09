# 5-Minute Screen Recording Guide

Record your own screen after the project runs successfully. Do not show your API key.

Suggested order:

1. **0:00-0:40 - Introduction**
   - Say that this project accepts plain-English browser test cases.
   - Mention Python, Playwright, Chromium, and Gemini AI.

2. **0:40-1:20 - Project structure**
   - Open the project in VS Code.
   - Briefly show `main.py`, `ai_planner.py`, `browser_manager.py`,
     `locator.py`, `executor.py`, `safety.py`, and `reporter.py`.
   - Explain that each file has one main responsibility.

3. **1:20-2:00 - Setup**
   - Show `requirements.txt` and `.env.example`.
   - Do not reveal the real API key in `.env`.

4. **2:00-3:40 - Live run**
   - Run the PHPTravels demo test from the README.
   - Show the browser actions and the terminal result.
   - If the live page has changed, use a test that matches its current visible
     title or text. Do not claim PASS if the tool reports FAIL.

5. **3:40-4:30 - Report**
   - Open the generated JSON file in `reports`.
   - If a test failed, show the failure screenshot if one was saved.

6. **4:30-5:00 - Limitations**
   - Explain that AI may misunderstand unclear test cases.
   - Mention that websites change and login, CAPTCHA, OTP, and protected pages
     may need extra setup.
   - Explain that the tool stops if it cannot find one unique matching element.

Keep the recording close to five minutes and speak in your own words.
