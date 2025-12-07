# .claude/subagents/answer_formatter.py
# This is a placeholder for a Claude subagent.
# In a real scenario, this agent could take the raw output
# from the language model and format it nicely for the user,
# for example, by adding markdown or highlighting key terms.

def format_answer(raw_answer: str) -> str:
    """Formats a raw answer into a user-friendly response."""
    print("Subagent 'answer_formatter' is running...")
    return f"**Answer:**\n\n{raw_answer}"