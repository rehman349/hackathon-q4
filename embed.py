# scripts/embed.py

import sys
from pathlib import Path

# Add the backend directory to the Python path
# This is a bit of a hack to make the imports work from the root directory
# A more robust solution would be to make the backend a proper package
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from rag_service import embed_documentation, get_settings

def main():
    """
    Main function to run the embedding process.
    """
    print("--- Starting Documentation Embedding Process ---")
    
    # Check for necessary settings
    settings = get_settings()
    if not all([settings.get("openai_api_key"), settings.get("qdrant_url"), settings.get("qdrant_api_key")]):
        print("\n[ERROR] Missing environment variables.")
        print("Please ensure your .env file in the 'backend' directory is correctly set up with:")
        print("- OPENAI_API_KEY")
        print("- QDRANT_URL")
        print("- QDRANT_API_KEY")
        sys.exit(1)

    try:
        count = embed_documentation()
        print(f"\n--- Embedding Process Complete ---")
        print(f"Successfully embedded {count} document chunks into Qdrant.")
    except Exception as e:
        print(f"\n[ERROR] An error occurred during the embedding process: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

