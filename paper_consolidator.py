#Author: MarwanMohammed
import os
import re
import pandas as pd
from config import BASE_DIR, RESULT_FOLDER, CONSOLIDATED_FILE, ALLOWED_EXTENSIONS, DOCUMENT_IDENTIFIER_MAPPING


class PaperConsolidator:
    def __init__(self, folder_names):
        self.base_directory = BASE_DIR
        self.folder_list = self._parse_folder_names(folder_names)
        self.allowed_extensions = ALLOWED_EXTENSIONS

    def _parse_folder_names(self, folder_names):
        if isinstance(folder_names, str):
            return [f.strip() for f in folder_names.split(",") if f.strip()]
        elif isinstance(folder_names, list):
            return folder_names
        else:
            raise ValueError("folder_names must be a string or list")

    @staticmethod
    def extract_bibtex_field(field_name, text):
        pattern = rf"{re.escape(field_name)}\s*=\s*\{{(.*?)\}}"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).replace("\n", " ").strip() if match else ""

    @staticmethod
    def extract_ris_field(field_name, entries):
        values = [line[6:].strip() for line in entries if line.startswith(field_name)]
        return "; ".join(values) if values else ""

    @staticmethod
    def extract_multiline_field(start_pattern, lines):
        extracting, extracted_text = False, []
        for line in lines:
            if line.startswith(start_pattern):
                extracting = True
                extracted_text.append(line[len(start_pattern):].strip())
            elif extracting and re.match(r"^[A-Z]{2,4}  -", line):
                break
            elif extracting:
                extracted_text.append(line.strip())
        return " ".join(extracted_text) if extracted_text else ""

    def standardize_document_identifier(self, df):
        def standardize(value):
            if pd.isna(value):
                return value
            value_lower = str(value).strip().lower()
            for category, keywords in DOCUMENT_IDENTIFIER_MAPPING.items():
                if any(kw.lower() == value_lower for kw in keywords):
                    return category
            return value

        df['Document Identifier'] = df['Document Identifier'].apply(standardize)
        return df

    def consolidate(self):
        result_folder_path = os.path.join(self.base_directory, RESULT_FOLDER)
        os.makedirs(result_folder_path, exist_ok=True)
        consolidated_output = os.path.join(result_folder_path, CONSOLIDATED_FILE)
        records = []
        processed_entries = set()
        for folder in self.folder_list:
            subfolder_path = os.path.join(self.base_directory, folder)
            if os.path.isdir(subfolder_path):
                publisher = folder
                for filename in os.listdir(subfolder_path):
                    if filename.endswith(self.allowed_extensions):
                        file_path = os.path.join(subfolder_path, filename)
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read().lstrip()
                        is_bibtex = content.startswith("@")
                        is_ris = bool(re.search(r'^TY  -', content, re.MULTILINE))
                        is_pubmed = content.startswith("PMID-")
                        if is_bibtex:
                            bib_entries = re.findall(r'@(\w+)\s*{\s*([^,]+),\s*(.*?)}\s*\n', content, flags=re.DOTALL)
                            for doc_type, identifier, entry in bib_entries:
                                title = self.extract_bibtex_field("title", entry)
                                doi = self.extract_bibtex_field("doi", entry)
                                unique_key = (title, doi)
                                if unique_key in processed_entries:
                                    continue
                                processed_entries.add(unique_key)
                                records.append({
                                    "Year": self.extract_bibtex_field("year", entry),
                                    "Title": title,
                                    "Abstract": self.extract_bibtex_field("abstract", entry),
                                    "Keywords": self.extract_bibtex_field("keywords", entry).replace(", ", "; "),
                                    "Author": self.extract_bibtex_field("author", entry).replace(" and ", "; "),
                                    "Document Identifier": doc_type,
                                    "Journal": self.extract_bibtex_field("journal", entry),
                                    "DOI": doi,
                                    "Source": publisher
                                })
                        elif is_ris:
                            ris_entries = content.split("ER  -") if "ER  -" in content else content.split("\n\n")
                            for entry in ris_entries:
                                if not entry.strip():
                                    continue
                                lines = entry.strip().split("\n")
                                title = self.extract_ris_field("TI  -", lines) or self.extract_ris_field("T1  -", lines)
                                doi = self.extract_ris_field("DO  -", lines) or self.extract_ris_field("DI  -", lines)
                                unique_key = (title, doi)
                                if unique_key in processed_entries:
                                    continue
                                processed_entries.add(unique_key)
                                records.append({
                                    "Year": self.extract_ris_field("PY  -", lines),
                                    "Title": title,
                                    "Abstract": self.extract_ris_field("AB  -", lines),
                                    "Keywords": self.extract_ris_field("KW  -", lines),
                                    "Author": self.extract_ris_field("AU  -", lines),
                                    "Document Identifier": self.extract_ris_field("TY  -", lines),
                                    "Journal": self.extract_ris_field("JO  -", lines) or self.extract_ris_field("T2  -", lines),
                                    "DOI": doi,
                                    "Source": publisher
                                })
                        elif is_pubmed:
                            pubmed_entries = content.split("\n\n")
                            for entry in pubmed_entries:
                                lines = entry.split("\n")
                                title = self.extract_multiline_field("TI  -", lines)
                                doi_field = self.extract_multiline_field("AID -", lines)
                                doi = doi_field.split(" [doi]")[0] if doi_field else ""
                                unique_key = (title, doi)
                                if unique_key in processed_entries:
                                    continue
                                processed_entries.add(unique_key)
                                full_date = self.extract_multiline_field("DP  -", lines)
                                date_parts = full_date.split()
                                extracted_date = date_parts[0] if date_parts else ""
                                records.append({
                                    "Year": extracted_date,
                                    "Title": title,
                                    "Abstract": self.extract_multiline_field("AB  -", lines),
                                    "Keywords": self.extract_multiline_field("OT  -", lines),
                                    "Author": "",
                                    "Document Identifier": "",
                                    "Journal": self.extract_multiline_field("JT  -", lines),
                                    "DOI": doi,
                                    "Source": publisher
                                })
        df = pd.DataFrame(records, columns=["Year", "Title", "Abstract", "Keywords", "Author", "Document Identifier", "Journal", "DOI", "Source"])
        df = self.standardize_document_identifier(df)
        df.to_excel(consolidated_output, index=False)
        return consolidated_output