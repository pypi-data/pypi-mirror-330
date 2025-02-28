# BibCleaner

BibCleaner is a Python package designed to parse, clean, and format .bib files for better LaTeX bibliography management. It ensures consistency in formatting, validates DOIs, and helps detect missing or incorrect fields. It facilitates integrations between citation management tools such as zotero and latex editor. 

## Features

Parses .bib files and structures them properly
Cleans and formats author names (handles capitalization, prefixes like "van", "de", etc.)
Ensures proper title capitalization (preserving LaTeX commands)
Customize fields and remove duplicate authors
Detects and fixes formatting issues in pages, DOIs, dates, etc.  
Validates DOIs and warns if they are broken  
Auto-generates citation keys based on author, title, and year  
Categorizes warnings:  
- Critical Issues: Missing author, title, year, etc.  
- Soft Warnings: Broken DOI, minor inconsistencies  

## Installation

Install the package using pip:
```sh
pip install bibcleaner
```

Or, clone the repository and install it manually:
```sh
git clone https://github.com/harryziyuhe/bibcleaner.git
cd bibcleaner
pip install .
```

## Usage

### Basic Usage (CLI)
```python
from bibcleaner import BibCleaner

cleaner = BibCleaner("references.bib")
cleaner.process()
cleaner.save_as_bib("cleaned_references.bib")
```

## Example Input & Output

### Example .bib File (Before Cleaning)
```bibtex
@article{einstein1923,
  author = "albert einstein",
  title = "the theory of relativity",
  journal = "journal of physics",
  year = "1923",
  doi = "10.1000/xyz123"
}
```

### Cleaned Output
```bibtex
@article{Einstein_Theory_1923,
  author = {Albert Einstein},
  title = {The Theory of Relativity},
  journal = {Journal of Physics},
  year = {1923},
  doi = {10.1000/xyz123}
}
```

### Warning Output
```
Critical Issues Found:
  Missing required field 'author' in @article{sample2024}

Soft Warnings:
  DOI '10.1000/broken' in @article{sample2023} may be broken (HTTP 404).
```

## Advanced Features

### Cleaning Options
You can specify which fields to keep when cleaning. Example:
```python
keep_fields = {
    "article": ["author", "title", "journal", "year"],
    "book": ["author", "title", "publisher", "year"]
}
cleaner = BibCleaner("references.bib", keep_fields)
cleaner.process()
```

### Export to JSON
```python
cleaner.save_as_json("cleaned_references.json")
```
## License

This project is licensed under the MIT License.  
See [LICENSE](LICENSE) for details.

## Contact

For suggestions or issues, feel free to open an issue on GitHub or contact zih028@ucsd.edu