# #Author: MarwanMohammed
# import os
# import pandas as pd
# import re
# from config import BASE_DIR, RESULT_FOLDER, CLASSIFIED_PAPERS_FILE, CLASSIFICATION_QUERIES

# class PaperClassifier:
#     def __init__(self, input_file):
#         self.input_file = input_file
#         self.output_file = CLASSIFIED_PAPERS_FILE
#         self.result_folder = RESULT_FOLDER
#         self.query_dataset = CLASSIFICATION_QUERIES
#         self.base_directory = BASE_DIR
#         self.result_folder_path = os.path.join(self.base_directory, self.result_folder)

#     def _create_output_folder(self):
#         """Create the output folder if it doesn't exist."""
#         os.makedirs(self.result_folder_path, exist_ok=True)

#     def _get_entry_fields(self, entry):
#         """
#         Returns the category and query string from an entry.
#         If the keys 'Category' and 'Query' are not found,
#         it assumes the entry is a single-key dictionary.
#         """
#         if "Category" in entry and "Query" in entry:
#             return entry["Category"], entry["Query"]
#         else:
#             for key, value in entry.items():
#                 return key, value

#     def _match_term(self, term, text):
#         """
#         Checks if a term is found in text.
#         Supports:
#         - Exact matches when enclosed in quotes (e.g., "machine learning").
#         - Substring search for normal words.
#         - Wildcard * at the end of words (e.g., robot* matches robotics, robots, robotic).
#         """
#         term = term.strip()

#         if ((term.startswith('"') and term.endswith('"')) or 
#             (term.startswith("'") and term.endswith("'"))):
#             term_clean = term[1:-1].strip().lower()
#             # Use regex with word boundaries for an exact phrase match.
#             pattern = r'\b' + re.escape(term_clean) + r'\b'
#             return bool(re.search(pattern, text, flags=re.IGNORECASE))

#         elif term.endswith("*"):  # Handle wildcard at the end
#             term_clean = re.escape(term[:-1])  # Remove '*' and escape regex special characters
#             pattern = r'\b' + term_clean + r'\w*'  # Match any word starting with term_clean
#             return bool(re.search(pattern, text, flags=re.IGNORECASE))

#         else:
#             return term.lower() in text

#     def _evaluate_query(self, query, text):
#         """
#         Evaluates the Boolean query against the given text.
#         Supports AND, OR, and negative conditions (using ANDNOT).
#         Exact phrases enclosed in quotes are matched using word boundaries.
#         """
#         # Ensure case-insensitive matching.
#         text = text.lower()
#         query = query.strip().replace("NotAND", "ANDNOT")
#         # Remove outer parentheses if present.
#         if query.startswith("(") and query.endswith(")"):
#             query = query[1:-1].strip()
#         # Split query into groups based on 'AND' (ignoring those with 'ANDNOT').
#         groups = re.split(r'\s+AND\s+(?!NOT)', query, flags=re.IGNORECASE)
#         for group in groups:
#             group = group.strip()
#             if "ANDNOT" in group:
#                 # Split group into positive and negative parts.
#                 pos_neg = re.split(r'\s+ANDNOT\s+', group, flags=re.IGNORECASE)
#                 pos_part = pos_neg[0].strip()
#                 neg_part = pos_neg[1].strip() if len(pos_neg) > 1 else ""
#                 if pos_part.startswith("(") and pos_part.endswith(")"):
#                     pos_part = pos_part[1:-1].strip()
#                 if neg_part.startswith("(") and neg_part.endswith(")"):
#                     neg_part = neg_part[1:-1].strip()
#                 pos_terms = re.split(r'\s+OR\s+', pos_part, flags=re.IGNORECASE)
#                 pos_match = any(self._match_term(term, text) for term in pos_terms if term.strip())
#                 neg_terms = re.split(r'\s+OR\s+', neg_part, flags=re.IGNORECASE)
#                 neg_match = any(self._match_term(term, text) for term in neg_terms if term.strip())
#                 if not pos_match or neg_match:
#                     return False
#             else:
#                 group_clean = group.strip()
#                 if group_clean.startswith("(") and group_clean.endswith(")"):
#                     group_clean = group_clean[1:-1].strip()
#                 terms = re.split(r'\s+OR\s+', group_clean, flags=re.IGNORECASE)
#                 if not any(self._match_term(term, text) for term in terms if term.strip()):
#                     return False
#         return True

#     def classify(self):
#         """
#         Reads the input Excel file, applies classification queries on Title and Abstract,
#         and writes the results to a new Excel file. Supports multi-classification by accumulating
#         all matching categories.
#         """
#         self._create_output_folder()

#         # Read the input file
#         df = pd.read_excel(self.input_file)

#         # Prepare lower-case text for matching.
#         df["TitleText"] = df["Title"].fillna("").astype(str).str.lower()
#         df["AbstractText"] = df["Abstract"].fillna("").astype(str).str.lower()

#         final_labels = []
#         for _, row in df.iterrows():
#             labels = set()
#             # Evaluate classification on Title.
#             for entry in self.query_dataset:
#                 category, query = self._get_entry_fields(entry)
#                 if self._evaluate_query(query, row["TitleText"]):
#                     labels.add(category)
#             # Evaluate classification on combined Title + Abstract.
#             combined_text = row["TitleText"] + " " + row["AbstractText"]
#             for entry in self.query_dataset:
#                 category, query = self._get_entry_fields(entry)
#                 if self._evaluate_query(query, combined_text):
#                     labels.add(category)
#             if not labels:
#                 labels.add("Unclassified")
#             # Join multiple labels into a comma-separated string.
#             final_labels.append(", ".join(sorted(labels)))
#         df["Classification"] = final_labels
#         # Clean up temporary columns.
#         df.drop(columns=["TitleText", "AbstractText"], inplace=True)

#         # Save the output file
#         output_file = os.path.join(self.result_folder_path, self.output_file)
#         df.to_excel(output_file, index=False)
#         return output_file

#     def print_queries(self):
#         """
#         Prints all classification queries for debugging.
#         """
#         for entry in self.query_dataset:
#             category, query = self._get_entry_fields(entry)
#             print(f"{category} : {query}")


# Author: MarwanMohammed
# Single-label classifier: picks exactly ONE best label per paper.

# Author: MarwanMohammed
# Single-label classifier with selectable text fields: title | abstract | both

import os
import re
import pandas as pd
from typing import List, Dict, Tuple

from config import (
    BASE_DIR,
    RESULT_FOLDER,
    CLASSIFIED_PAPERS_FILE,
    Sorting_Stage,
)

class PaperClassifier:
    def __init__(self, input_file: str, mode: str = "both"):
        """
        mode:
          - "title"    -> use Title only
          - "abstract" -> use Abstract only
          - "both"     -> prefer Title matches; else Title+Abstract (default)
        """
        self.input_file = input_file
        self.output_file = CLASSIFIED_PAPERS_FILE
        self.result_folder = RESULT_FOLDER
        self.base_directory = BASE_DIR
        self.result_folder_path = os.path.join(self.base_directory, self.result_folder)

        self.query_dataset = Sorting_Stage
        self.mode = (mode or "both").strip().lower()
        if self.mode not in {"title", "abstract", "both"}:
            self.mode = "both"  # safety

        # Priority order (edit to taste)
        self.PRIORITY_ORDER: List[str] = [
            "REVIEW", "CRI", "HRI", "HCI", "EDUCATION", "HEALTHCARE", "INDUSTRIAL",
            "ASSISTIVE_TECH", "SPEECH_PROCESSING", "ETHICS", "SOCIAL_IMPACT",
            "NEUROROBOTICS", "AUGMENTED_REALITY", "PERCEPTION", "EMOTION_RECOGNITION",
            "AUTONOMOUS_SYSTEMS", "SWARM_ROBOTICS", "SECURITY_PRIVACY", "EXOSKELETONS",
            "HUMAN_FACTORS", "MACHINE_LEARNING", "SURGICAL_ROBOTICS", "MEDICAL_EDUCATION",
            "GERIATRIC_ROBOTICS", "AGRICULTURAL_ROBOTICS", "TECHNOLOGY_IMPACT",
            "SOCIAL_MEDIA", "USER_AUTONOMY", "METAVERSE_ROBOTICS", "SR", "AUTISM",
            "Editorial",
        ]

    # ------------------------- filesystem -------------------------

    def _create_output_folder(self):
        os.makedirs(self.result_folder_path, exist_ok=True)

    # ------------------------- query utilities -------------------------

    def _get_entry_fields(self, entry: Dict[str, str]) -> Tuple[str, str]:
        if "Category" in entry and "Query" in entry:
            return entry["Category"], entry["Query"]
        for k, v in entry.items():
            return k, v
        return "UNKNOWN", ""

    def _collapse_duplicate_categories(self):
        grouped: Dict[str, List[str]] = {}
        for entry in self.query_dataset:
            cat, q = self._get_entry_fields(entry)
            grouped.setdefault(cat, []).append(q)

        collapsed = []
        for cat, qs in grouped.items():
            if len(qs) == 1:
                collapsed.append({cat: qs[0]})
            else:
                merged = "(" + ") OR (".join(q.strip() for q in qs if q.strip()) + ")"
                collapsed.append({cat: merged})
        self.query_dataset = collapsed

    # ------------------------- boolean matching -------------------------

    def _match_term(self, term: str, text: str) -> bool:
        term = term.strip()
        if ((term.startswith('"') and term.endswith('"')) or
            (term.startswith("'") and term.endswith("'"))):
            phrase = term[1:-1].strip()
            pattern = r'\b' + re.escape(phrase) + r'\b'
            return bool(re.search(pattern, text, flags=re.IGNORECASE))
        if term.endswith("*"):
            stem = re.escape(term[:-1])
            pattern = r'\b' + stem + r'\w*'
            return bool(re.search(pattern, text, flags=re.IGNORECASE))
        return term.lower() in text

    def _evaluate_query(self, query: str, text: str) -> bool:
        text = text.lower()
        query = query.strip().replace("NotAND", "ANDNOT")
        if query.startswith("(") and query.endswith(")"):
            query = query[1:-1].strip()
        groups = re.split(r'\s+AND\s+(?!NOT)', query, flags=re.IGNORECASE)

        for group in groups:
            group = group.strip()
            if "ANDNOT" in group:
                pos_neg = re.split(r'\s+ANDNOT\s+', group, flags=re.IGNORECASE)
                pos_part = pos_neg[0].strip() if pos_neg else ""
                neg_part = pos_neg[1].strip() if len(pos_neg) > 1 else ""
                if pos_part.startswith("(") and pos_part.endswith(")"):
                    pos_part = pos_part[1:-1].strip()
                if neg_part.startswith("(") and neg_part.endswith(")"):
                    neg_part = neg_part[1:-1].strip()
                pos_terms = re.split(r'\s+OR\s+', pos_part, flags=re.IGNORECASE)
                neg_terms = re.split(r'\s+OR\s+', neg_part, flags=re.IGNORECASE)
                pos_match = any(self._match_term(t, text) for t in pos_terms if t.strip())
                neg_match = any(self._match_term(t, text) for t in neg_terms if t.strip())
                if not pos_match or neg_match:
                    return False
            else:
                grp = group
                if grp.startswith("(") and grp.endswith(")"):
                    grp = grp[1:-1].strip()
                terms = re.split(r'\s+OR\s+', grp, flags=re.IGNORECASE)
                if not any(self._match_term(t, text) for t in terms if t.strip()):
                    return False
        return True

    # ------------------------- ranking utilities -------------------------

    def _priority_index(self, category: str) -> int:
        try:
            return self.PRIORITY_ORDER.index(category)
        except ValueError:
            return len(self.PRIORITY_ORDER)

    def _specificity(self, query: str) -> int:
        return sum(ch.isalnum() for ch in query)

    # ------------------------- main API -------------------------

    def classify(self) -> str:
        """
        Single-label classification with selectable fields:
          mode="title":    evaluate only Title
          mode="abstract": evaluate only Abstract
          mode="both":     prefer Title match; else Title+Abstract
        """
        self._create_output_folder()
        self._collapse_duplicate_categories()

        df = pd.read_excel(self.input_file)
        if "Title" not in df.columns:
            df["Title"] = ""
        if "Abstract" not in df.columns:
            df["Abstract"] = ""

        df["TitleText"] = df["Title"].fillna("").astype(str).str.lower()
        df["AbstractText"] = df["Abstract"].fillna("").astype(str).str.lower()

        best_labels: List[str] = []

        for _, row in df.iterrows():
            title_text = row["TitleText"]
            abstract_text = row["AbstractText"]
            combined_text = (title_text + " " + abstract_text).strip()

            best_key = None
            best_cat = "Unclassified"

            for entry in self.query_dataset:
                category, query = self._get_entry_fields(entry)

                if self.mode == "title":
                    matched = self._evaluate_query(query, title_text)
                    title_match = matched
                elif self.mode == "abstract":
                    matched = self._evaluate_query(query, abstract_text)
                    title_match = False  # no title preference in this mode
                else:  # both
                    title_match = self._evaluate_query(query, title_text)
                    matched = title_match or self._evaluate_query(query, combined_text)

                if not matched:
                    continue

                key = (
                    self._priority_index(category),
                    0 if (self.mode == "title" and matched) or (self.mode == "both" and title_match) else 1,
                    -self._specificity(query),
                    category
                )

                if (best_key is None) or (key < best_key):
                    best_key = key
                    best_cat = category

            best_labels.append(best_cat)

        df["Classification"] = best_labels
        df.drop(columns=["TitleText", "AbstractText"], inplace=True)

        output_path = os.path.join(self.result_folder_path, self.output_file)
        df.to_excel(output_path, index=False)
        return output_path

    def print_queries(self):
        self._collapse_duplicate_categories()
        for entry in self.query_dataset:
            cat, q = self._get_entry_fields(entry)
            print(f"{cat} : {q}")
