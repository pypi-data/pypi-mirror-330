import pytest
from cleanbib.bib_cleaner import BibCleaner

def test_clean_entries():
    test_bib = """
    @article{test2024,
      author = "john doe",
      title = "a test paper",
      journal = "test journal",
      year = "2024",
      pages = "100--110"
    }
    """
    
    # Save to a temp file
    test_file = "test.bib"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_bib)
    
    cleaner = BibCleaner(test_file)
    cleaner.process()

    # Check if author is formatted correctly
    assert cleaner.entries[0]["fields"]["author"] == "Doe, John"

    # Check if title is formatted correctly
    assert cleaner.entries[0]["fields"]["title"] == "A Test Paper"

    # Check if pages are formatted correctly
    assert cleaner.entries[0]["fields"]["pages"] == "100--110"

def test_remove_empty_fields():
    entry = {
        "type": "article",
        "citation_key": "test2024",
        "fields": {
            "author": "John Doe",
            "title": "A Test Paper",
            "journal": "",
            "year": "2024"
        }
    }
    cleaner = BibCleaner("test.bib")
    cleaner.entries = [entry]  # Mock an entry
    cleaner.clean_entries()

    # Ensure empty fields are removed
    assert "journal" not in cleaner.entries[0]["fields"]
