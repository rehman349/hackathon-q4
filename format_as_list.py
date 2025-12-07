# .claude/skills/format_as_list.py
# This is a placeholder for a Claude skill.
# This skill could be used by the 'answer_formatter' agent.

def to_bullet_points(text: str) -> str:
    """A simple skill to format text with dashes into bullet points."""
    print("Skill 'format_as_list' is running...")
    items = text.split(' - ')
    if len(items) < 2:
        return text
    
    # Return as a markdown list
    return "\n".join([f"* {item.strip()}" for item in items if item.strip()])
