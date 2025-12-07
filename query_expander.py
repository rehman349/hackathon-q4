# .claude/subagents/query_expander.py
# This is a placeholder for a Claude subagent.
# In a real scenario, this agent could take a user's query
# and expand it with synonyms or related concepts to improve
# retrieval results.

def expand_query(query: str) -> list[str]:
    """Expands a query with related terms."""
    print("Subagent 'query_expander' is running...")
    return [
        query,
        f"{query} basics",
        f"details about {query}",
    ]
