# .claude/subagents/doc_parser.py
# This is a placeholder for a Claude subagent.
# In a real scenario, this agent could be responsible for
# parsing and understanding the structure of documentation files.

def parse_document(file_content: str) -> dict:
    """Parses a document and extracts key sections."""
    print("Subagent 'doc_parser' is running...")
    return {
        "title": "Parsed Title",
        "sections": ["Section 1", "Section 2"],
        "content_length": len(file_content),
    }
