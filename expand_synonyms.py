# .claude/skills/expand_synonyms.py
# This is a placeholder for a Claude skill.
# This skill could be used by the 'query_expander' agent.

def get_synonyms(term: str) -> list[str]:
    """A simple skill to return hardcoded synonyms for a term."""
    print("Skill 'expand_synonyms' is running...")
    synonym_map = {
        "sun": ["star", "sol"],
        "earth": ["world", "globe"],
    }
    return synonym_map.get(term.lower(), [])
