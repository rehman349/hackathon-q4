# .claude/skills/parse_markdown.py
# This is a placeholder for a Claude skill.
# A skill is a more granular, reusable tool that a subagent might use.
# This skill could be used by the 'doc_parser' agent.

def extract_headings(markdown_text: str) -> list[str]:
    """A simple skill to extract H1 and H2 headings from markdown."""
    print("Skill 'parse_markdown' is running...")
    headings = []
    for line in markdown_text.split('\n'):
        if line.startswith('# '):
            headings.append(line[2:])
        elif line.startswith('## '):
            headings.append(line[3:])
    return headings
