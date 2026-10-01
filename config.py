"""Central settings: models, goals, agent labels, sample data."""

MODELS = {
    "Llama 3.3 70B (best quality)": "groq/llama-3.3-70b-versatile",
    "Llama 3.1 8B (fast, higher rate limits)": "groq/llama-3.1-8b-instant",
}

GOALS = [
    "Reduce cycle time",
    "Reduce cost",
    "Reduce errors and rework",
    "Improve employee/customer experience",
    "Improve compliance and control",
]

# Order matters: this is the order the agents run in.
AGENT_STEPS = [
    "Process Mapper",
    "Bottleneck Analyst",
    "Automation Scorer",
    "Roadmap Writer",
]

SAMPLE_PROCESS = """Employee leave approval process:
1. Employee fills a leave request on a paper/Word form and emails it to their line manager.
2. Manager reads the email (often after 2-3 days), prints the form, signs it and scans it back.
3. Employee forwards the signed form to HR.
4. HR officer manually checks the leave balance in an Excel sheet.
5. If balance is insufficient, HR emails the employee back; otherwise HR updates the Excel sheet.
6. HR sends a confirmation email to the employee and the manager.
7. At month end, HR manually compiles all leave data for payroll.
Average cycle time: 5 days. About 300 requests per month. Frequent errors in balances and lost emails."""
