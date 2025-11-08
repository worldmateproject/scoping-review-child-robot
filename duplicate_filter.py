# import os
# import pandas as pd
# from rapidfuzz import process, fuzz
# from joblib import Parallel, delayed
# from config import BASE_DIR, RESULT_FOLDER, FILTERED_DUPLICATE_FILE, OUTPUT_WITH_FLAGS, TITLES_TO_REMOVE, ABSTRACTS_TO_REMOVE

# class DuplicateFilter:
#     def __init__(self, input_excel):
#         self.input_excel = input_excel
#         self.base_directory = BASE_DIR
#         self.result_folder_path = os.path.join(self.base_directory, RESULT_FOLDER)

#     def _create_output_folder(self):
#         """Create the output folder if it doesn't exist."""
#         os.makedirs(self.result_folder_path, exist_ok=True)

#     def _flag_duplicates(self, df):
#         """Flag duplicates based on DOI and Title."""
#         df["DuplicateFlag"] = ""
#         df["Keep"] = True

#         # Clean and normalize data
#         df["DOI"] = df["DOI"].astype(str).str.strip().str.lower()
#         df["Title"] = df["Title"].astype(str).str.strip().str.lower()

#         # Remove non-printable characters
#         df["DOI"] = df["DOI"].str.replace(r"[\n\t\r]", "", regex=True)
#         df["Title"] = df["Title"].str.replace(r"[\n\t\r]", "", regex=True)

#         # Flag duplicates based on DOI
#         doi_duplicates = df.duplicated(subset=["DOI"], keep="first")
#         df.loc[doi_duplicates, "DuplicateFlag"] = "Duplicate DOI"
#         df.loc[doi_duplicates, "Keep"] = False

#         # Flag duplicates based on Title
#         title_duplicates = df.duplicated(subset=["Title"], keep="first")
#         df.loc[title_duplicates & (df["DuplicateFlag"] == ""), "DuplicateFlag"] = "Duplicate Title"
#         df.loc[title_duplicates & (df["DuplicateFlag"] == ""), "Keep"] = False

#         # Optional: Flag fuzzy duplicates (commented out for performance)
#         # df = self.flag_fuzzy_duplicates(df)

#         return df

#     def flag_fuzzy_duplicates(self, df, threshold=90):
#         """Flag near-duplicates using fuzzy matching."""
#         titles = df["Title"].tolist()
#         def process_title(i, title):
#             matches = process.extract(title, titles, scorer=fuzz.ratio, limit=None)
#             for match, score, _ in matches:
#                 if score > threshold and match != title:
#                     df.loc[df["Title"] == match, "DuplicateFlag"] = "Fuzzy Duplicate Title"
#                     df.loc[df["Title"] == match, "Keep"] = False

#         # Use parallel processing for large datasets
#         Parallel(n_jobs=-1)(delayed(process_title)(i, title) for i, title in enumerate(titles))
#         return df

#     def _remove_unwanted_rows(self, df):
#         """Remove rows with unwanted titles, abstracts, or document identifiers."""
#         # Remove rows with unwanted titles
#         df = df[~df["Title"].isin(TITLES_TO_REMOVE)]

#         # Remove rows with unwanted abstracts
#         df = df[~df["Abstract"].isin(ABSTRACTS_TO_REMOVE) & df["Abstract"].notna() & (df["Abstract"].str.strip() != "")]

#         # Remove rows where 'Document Identifier' is 'Book' or 'book'
#         df = df[~df["Document Identifier"].str.lower().eq("book")]

#         return df

#     def filter_duplicates(self):
#         """Main method to filter duplicates and save the results."""
#         self._create_output_folder()

#         # Read the input Excel file
#         df = pd.read_excel(self.input_excel)

#         # Flag duplicates
#         df_with_flags = self._flag_duplicates(df)

#         # Save the output with flags
#         output_with_flags_path = os.path.join(self.result_folder_path, OUTPUT_WITH_FLAGS)
#         df_with_flags.to_excel(output_with_flags_path, index=False)

#         # Filter out duplicates and unwanted rows
#         df_unique = df_with_flags[df_with_flags["Keep"]].copy().drop(columns=["Keep", "DuplicateFlag"])
#         df_unique = self._remove_unwanted_rows(df_unique)

#         # Save the filtered output
#         output_filtered_path = os.path.join(self.result_folder_path, FILTERED_DUPLICATE_FILE)
#         df_unique.to_excel(output_filtered_path, index=False)

#         return output_with_flags_path, output_filtered_path
    
# duplicate_filter.py

import os
import re
import pandas as pd
import unicodedata
from urllib.parse import unquote
from rapidfuzz import fuzz, process
from joblib import Parallel, delayed
from config import BASE_DIR, RESULT_FOLDER, FILTERED_DUPLICATE_FILE, OUTPUT_WITH_FLAGS, TITLES_TO_REMOVE, ABSTRACTS_TO_REMOVE

PREFERRED_SOURCES = ["WoS", "Scopus", "IEEE", "ACM", "SD", "PubMed"]  # tweak to your liking

def _normalize_doi(value: str) -> str:
    if pd.isna(value):
        return ""
    v = str(value).strip()
    v = unquote(v)
    v = re.sub(r'^(https?://(dx\.)?doi\.org/)', '', v, flags=re.IGNORECASE)  # strip resolver
    v = v.strip().rstrip(' .;,)')
    return v.lower()

def _nfkc(text: str) -> str:
    return unicodedata.normalize("NFKC", text)

def _strip_diacritics(text: str) -> str:
    # normalize to NFKD and drop combining marks
    s = unicodedata.normalize('NFKD', text)
    return "".join(ch for ch in s if not unicodedata.combining(ch))

STOPWORDS = set("""
a an the of and for in on to with from into by study analysis review
""".split())

def _title_fingerprint(title: str) -> str:
    if pd.isna(title):
        return ""
    t = _nfkc(str(title).lower())
    t = _strip_diacritics(t)
    t = re.sub(r'[\u2010-\u2015\-–—]+', ' ', t)          # dashes → space
    t = re.sub(r'[^\w\s]', ' ', t)                      # drop punctuation
    tokens = [w for w in t.split() if w and w not in STOPWORDS]
    # sort to make word order irrelevant; keep only alphanumerics
    tokens = [re.sub(r'_', '', w) for w in tokens]
    key = " ".join(sorted(tokens))
    # shorten very long keys to keep Excel reasonable
    return key[:180]

def _first_author_last(author_field: str) -> str:
    if not isinstance(author_field, str) or not author_field.strip():
        return ""
    # your consolidator uses '; ' between names for bibtex and AU  - for RIS; both end up as strings
    first = author_field.split(';')[0].strip()
    last = first.split()[-1].lower() if first else ""
    return last

class DuplicateFilter:
    def __init__(self, input_excel):
        self.input_excel = input_excel
        self.base_directory = BASE_DIR
        self.result_folder_path = os.path.join(self.base_directory, RESULT_FOLDER)

    def _create_output_folder(self):
        os.makedirs(self.result_folder_path, exist_ok=True)

    def _flag_duplicates(self, df):
        """Flag duplicates using DOI, title fingerprint, and blocked fuzzy matching."""
        df["DuplicateFlag"] = ""
        df["Keep"] = True

        # --- Canonical columns ---
        df["DOI_raw"] = df["DOI"].astype(str)
        df["DOI_norm"] = df["DOI_raw"].apply(_normalize_doi)

        df["Title_raw"] = df["Title"].astype(str)
        df["Title_fp"] = df["Title_raw"].apply(_title_fingerprint)

        # Make sure Year is numeric to allow blocking by year ±1
        df["Year_num"] = pd.to_numeric(df["Year"], errors="coerce")
        df["FirstAuthorLast"] = df["Author"].astype(str).apply(_first_author_last)

        # --- Exact duplicate pass ---
        # 1) DOI
        doi_dups = df.duplicated(subset=["DOI_norm"], keep="first") & df["DOI_norm"].ne("")
        df.loc[doi_dups, ["DuplicateFlag","Keep"]] = ["Duplicate DOI", False]

        # 2) Title fingerprint
        title_dups = df.duplicated(subset=["Title_fp"], keep="first")
        df.loc[title_dups & (df["DuplicateFlag"] == ""), ["DuplicateFlag","Keep"]] = ["Duplicate Title (fingerprint)", False]

        # --- Fuzzy pass (blocked) ---
        # only consider rows not already marked and without DOI matches
        candidates = df[df["Keep"]].copy()

        def fuzzy_block(group):
            idx = group.index.tolist()
            titles = group["Title_raw"].tolist()
            # token_set_ratio is robust to word order
            # build lookup to mark near-dups
            for i in range(len(idx)):
                if not group.at[idx[i], "Keep"]:
                    continue
                for j in range(i+1, len(idx)):
                    if not group.at[idx[j], "Keep"]:
                        continue
                    score = fuzz.token_set_ratio(titles[i], titles[j])
                    if score >= 95:  # tune if needed
                        # prefer row with DOI, else longer abstract, else preferred source
                        a, b = idx[i], idx[j]
                        def score_row(k):
                            has_doi = 1 if df.at[k, "DOI_norm"] else 0
                            abs_len = len(str(df.at[k,"Abstract"])) if pd.notna(df.at[k,"Abstract"]) else 0
                            src_score = (len(PREFERRED_SOURCES) - PREFERRED_SOURCES.index(df.at[k,"Source"])) if df.at[k,"Source"] in PREFERRED_SOURCES else 0
                            return (has_doi, abs_len, src_score)
                        keep, drop = (a,b) if score_row(a) >= score_row(b) else (b,a)
                        df.at[drop, "DuplicateFlag"] = f"Fuzzy Title ({score})"
                        df.at[drop, "Keep"] = False

        # block by first-author last name and year window (year, year±1)
        for yr in candidates["Year_num"].dropna().unique():
            for delta in (-1, 0, 1):
                sub = candidates[(candidates["Year_num"] == yr + delta)]
                if sub.empty: 
                    continue
                for last in sub["FirstAuthorLast"].unique():
                    block = sub[sub["FirstAuthorLast"] == last]
                    if len(block) > 1:
                        fuzzy_block(block)

        return df

    def _remove_unwanted_rows(self, df):
        df = df[~df["Title"].isin(TITLES_TO_REMOVE)]
        df = df[~df["Abstract"].isin(ABSTRACTS_TO_REMOVE) & df["Abstract"].notna() & (df["Abstract"].str.strip() != "")]
        df = df[~df["Document Identifier"].astype(str).str.lower().eq("book")]
        return df

    def filter_duplicates(self):
        self._create_output_folder()
        df = pd.read_excel(self.input_excel)

        df_with_flags = self._flag_duplicates(df)

        # Save the audit file with flags
        output_with_flags_path = os.path.join(self.result_folder_path, OUTPUT_WITH_FLAGS)
        df_with_flags.to_excel(output_with_flags_path, index=False)

        # Keep the best representative of each duplicate cluster: Keep==True
        df_unique = df_with_flags[df_with_flags["Keep"]].copy().drop(columns=["Keep", "DuplicateFlag", "DOI_raw","Title_raw","Year_num","FirstAuthorLast"])
        df_unique = self._remove_unwanted_rows(df_unique)

        output_filtered_path = os.path.join(self.result_folder_path, FILTERED_DUPLICATE_FILE)
        df_unique.to_excel(output_filtered_path, index=False)

        return output_with_flags_path, output_filtered_path
