# %%
import re, json, requests
from tqdm import tqdm
from .warning_handler import WarningHandler

# %%
class BibCleaner:
    REQUIRED_FIELDS = {
        "article": ["author", "title", "journal", "year"],
        "book": ["author", "title", "publisher", "year"],
        "inbook": ["author", "title", "chapter", "publisher", "year"],
        "incollection": ["author", "title", "booktitle", "publisher", "year"],
        "inproceedings": ["author", "title", "booktitle", "year"],
        "manual": ["title"],
        "phdthesis": ["author", "title", "school", "year"],
        "proceedings": ["title", "year"]
    }
    LOWERCASE_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "nor", 
                                "of", "on", "or", "so", "the", "to", "up", "yet", "with"}

    def __init__(self, file_path: str, keep_fields = None):
        self.file_path = file_path
        self.entries = []
        self.keep_fields = self._load_keep_fields(keep_fields)
        self.authors = set()
        self.cite_keys = list()
        self.warning_hander = WarningHandler()

    def _load_keep_fields(self, keep_fields):
        if isinstance(keep_fields, dict):
            return keep_fields
        elif isinstance(keep_fields, str):
            try:
                with open(keep_fields, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading keep_fields JSON file: {e}")
                return {}
        else:
            return {}

    def load_bib_file(self):
        with open(self.file_path, "r", encoding = "utf-8") as bib_file:
            content = bib_file.read()

        pattern = r'@(\w+)\s*{\s*([^,]+),\s*((?:.|\n)*?)\n\s*}'

        raw_entries  = re.findall(pattern, content, re.DOTALL)

        print(raw_entries)

        for entry in raw_entries:
            entry_type, citation_key, raw_fields = entry
            fields = self._parse_fields(raw_fields)

            if entry_type.lower() in self.keep_fields:
                allowed_fields = set(self.keep_fields[entry_type.lower()])
                fields = {key: value for key, value in fields.items() if key in allowed_fields}

            self.entries.append({
                "type": entry_type,
                "citation_key": citation_key,
                "fields": fields
            })

    def _parse_fields(self, raw_fields: str) -> dict:
        fields = {}
        for match in re.finditer(r'(\w+)\s*=\s*({(.*?)},|"(.*?)"),?', raw_fields, re.DOTALL):
            key = match.group(1).lower()
            value = match.group(3) if match.group(3) else match.group(4)  # Handles {value} or "value"
            fields[key] = self._clean_latex(value)
        return fields
    
    def clean_entries(self):
        for entry in tqdm(self.entries):
            fields = entry["fields"].copy()
            # Required Fields
            fields["author"] = self._format_authors(fields.get("author", ""))
            fields["title"] = self._clean_latex(fields.get("title", ""))
            fields["year"], fields["month"], fields["day"] = self._format_date(fields.get("date", ""))
            if fields["year"] == "":
                fields["year"] = self._format_year(entry["fields"].get("year", ""))
            fields["journal"] = self._clean_latex(fields.get("journal", ""))
            fields["booktitle"] = self._clean_latex(fields.get("booktitle", ""))
            entry["citation_key"] = self._format_citation_key(fields["author"], fields["title"], fields["year"])
            self._validate_entry(entry["citation_key"], entry["type"], fields)

            # Optional Fields
            fields["editor"] = self._format_authors(fields.get("editor", ""))
            fields["organization"] = self._clean_latex(fields.get("organization", ""))
            fields["urlyear"], fields["urlmonth"], fields["urlday"] = self._format_date(fields.get("urldate", ""))
            fields["pages"] = self._format_pages(fields.get("pages", ""))
            fields["doi"] = self._clean_doi(entry["citation_key"], fields.get("doi", ""))
            entry["fields"] = {key: value for key, value in fields.items() if value != ""}
            
    def _validate_entry(self, citation_key: str, entry_type: str, fields: dict):
        required_fields = self.REQUIRED_FIELDS.get(entry_type, [])
        for field in required_fields:
            if field not in fields or not fields[field].strip():
                self.warning_hander.add_critical(
                    f"Missing required field '{field}' in @{entry_type}{{{citation_key}}}"
                )

    def _format_authors(self, authors: str) -> str:
        if not authors:
            return ""
        
        processed_authors = list()

        prefixes = {"von", "van", "de", "del", "da", "di", "la", "le", "der"}

        def capitalize_name(name: str) -> str:
            name = "-".join([part.capitalize() for part in name.split("-")])
            name = "'".join([part.capitalize() for part in name.split("'")])
            return name
        
        for author in authors.split(" and "):
            author = author.strip()

            if "," in author:
                last_name, first_name = author.split(",", 1)
                first_name = first_name.strip().replace("{", "").replace("}", "")
                last_name = last_name.strip().replace("{", "").replace("}", "")
            else:
                author = author.replace("{", "").replace("}", "")
                name_parts = author.split()
                last_name_start = None
                for i in range(len(name_parts) - 1, 1, -1):
                    if name_parts[i - 1].lower() in prefixes:
                        last_name_start = i - 1
                    elif last_name_start is not None:
                        break

                if last_name_start is None:
                    first_name = " ".join(name_parts[:-1])
                    last_name = name_parts[-1]
                else:
                    first_name = " ".join(name_parts[:last_name_start])
                    last_name = " ".join(name_parts[last_name_start:])
            
            first_name = " ".join([capitalize_name(part) for part in first_name.split()])
            last_name_parts = last_name.split()
            formatted_last_name = []

            for part in last_name_parts:
                if part.lower() in prefixes:
                    formatted_last_name.append(part.lower())
                else:
                    formatted_last_name.append(capitalize_name(part))
            
            last_name = " ".join(formatted_last_name)

            
            self.authors.add((first_name, last_name))
            formatted_name = f"{last_name}, {first_name}"
            if formatted_name not in processed_authors:
                processed_authors.append(formatted_name)
        
        processed_authors = list(processed_authors)
        return " and ".join(processed_authors)
            
    def _clean_latex(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r"\\textit{(.*?)}", r"\1", text)
        text = re.sub(r"\\textbf{(.*?)}", r"\1", text)
        text = text.replace("{", "").replace("}", "")    
        text = text.strip()
        
        words = text.split()
        formatted_words = [words[0].capitalize()]

        for word in words[1:]:
            if word.lower() in self.LOWERCASE_WORDS:
                formatted_words.append(word.lower())
            else:
                formatted_words.append(word.capitalize())

        return " ".join(formatted_words)
    
    def _format_year(self, year_str: str) -> str:
        year_str = year_str.strip()
        match = re.fullmatch(r"(\d{4})", year_str)
        if match:
            return match.group(1)
        
        match = re.fullmatch(r"(\d{2})", year_str)
        if match:
            try:
                if int(match) <= 25:
                    return f"20{match.group(1)}"
                else:
                    return f"19{match.group(1)}"
            except:
                return ""
        
        return ""
    
    def _format_date(self, date_str: str) -> str:
        date_str = date_str.strip()

        match = re.fullmatch(r"(\d{4})", date_str)
        if match:
            return match.group(1), "", ""
        
        match = re.fullmatch(r"(\d{4})[-/](\d{1,2})", date_str)
        if match:
            return match.group(1), match.group(2), ""
        
        match = re.fullmatch(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", date_str)
        if match:
            return match.group(1), match.group(2), match.group(3)

        # Case 4: MM/DD/YYYY (U.S. format)
        match = re.fullmatch(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", date_str)
        if  match:
            try:
                if int(match.group(2)) > 12:
                    return match.group(3), match.group(1), match.group(2)
                else:
                    return match.group(3), match.group(2), match.group(1)
            except:
                return "", "", ""
        return "", "", ""
    
    def _format_pages(self, pages: str) -> str:
        if not pages:
            return ""
        pages = re.sub(r"\s*[-–—]+\s*", "--", pages)
        
        return pages

    def _clean_doi(self, citation_key: str, doi: str) -> str:
        if not doi or not doi.startswith("10."):
            return ""
        
        doi = doi.strip()
        doi_url = f"https://doi.org/{doi}"
        
        try:
            response = requests.head(doi_url, allow_redirects=True, timeout = 5)
            if response.status_code in {200, 301, 302}:
                return doi
            else:
                self.warning_hander.add_soft(f"DOI '{doi}' in @{citation_key} may be broken (HTTP {response.status_code}).")
                return ""
        except requests.RequestException:
            return doi

    def _format_citation_key(self, author, title, year):
        last_name = author.split(",")[0].strip().replace(" ", "_").lower()
        for word in title.split():
            if word.lower() not in self.LOWERCASE_WORDS:
                return f"{last_name}_{word.lower()}_{year}"
    
    def save_as_json(self, output_path: str):
        with open(output_path, "w", encoding = "utf-8") as f:
            json.dump(self.entries, f, indent = 4)

    def save_as_bib(self, output_path: str):
        with open(output_path, "w", encoding = "utf-8") as f:
            for entry in self.entries:
                f.write(f"@{entry['type']}{{{entry['citation_key']}, \n")
                for key, value in entry["fields"].items():
                    f.write(f"    {key} = {{{value}}},\n")
                f.write("}\n\n")

    def print_warnings(self):
        print(self.warning_hander.get_warnings_text())
    
    def process(self, progress = True, warning = True):
        self.load_bib_file()
        self.clean_entries()


# %%
if not "".strip():
    print("YES")
# %%
