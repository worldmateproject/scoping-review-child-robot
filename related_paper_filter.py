# #Author: MarwanMohammed

import pandas as pd
import os
import re
from config import (
    BASE_DIR, RESULT_FOLDER,
    # staged queries
    STAGE1, STAGE2, STAGE3,
    # filenames
    STAGE1_ALL_FILE, STAGE2_ALL_FILE, STAGE3_ALL_FILE,
    STAGE1_FILTERED_FILE, STAGE2_FILTERED_FILE, STAGE3_FILTERED_FILE,
    STAGE1_QUERY_LOG, STAGE2_QUERY_LOG, STAGE3_QUERY_LOG,
    # legacy compatibility
    QUERY_LOG_FILE
)

STAGE_TO_QUERY = {1: STAGE1, 2: STAGE2, 3: STAGE3}
STAGE_TO_ALL = {1: STAGE1_ALL_FILE, 2: STAGE2_ALL_FILE, 3: STAGE3_ALL_FILE}
STAGE_TO_FILTERED = {1: STAGE1_FILTERED_FILE, 2: STAGE2_FILTERED_FILE, 3: STAGE3_FILTERED_FILE}
STAGE_TO_LOG = {1: STAGE1_QUERY_LOG, 2: STAGE2_QUERY_LOG, 3: STAGE3_QUERY_LOG}

class RelatedPaperFilter:
    def __init__(self, input_file, debug=False):
        self.input_file = input_file
        self.debug = debug
        self.base_directory = BASE_DIR
        self.result_folder_path = os.path.join(self.base_directory, RESULT_FOLDER)


    def _create_output_folder(self):
        os.makedirs(self.result_folder_path, exist_ok=True)

    def _build_condition(self, df, query, col_name):
        q = query.strip()
        if q.startswith("(") and q.endswith(")"):
            q = q[1:-1].strip()
        groups = [group.strip() for group in q.split("AND")]

        overall_condition = None
        processed_groups = []

        for group in groups:
            if group.startswith("(") and group.endswith(")"):
                group = group[1:-1].strip()

            keywords = [kw.strip() for kw in group.split("OR")]
            processed_keywords = []
            group_condition = None

            for kw in keywords:
                if (kw.startswith('"') and kw.endswith('"')) or (kw.startswith("'") and kw.endswith("'")):
                    kw_clean = kw[1:-1]
                    kw_regex = r'\b' + re.escape(kw_clean) + r'\b'
                else:
                    kw_clean = kw
                    escaped_kw = re.escape(kw_clean)
                    kw_regex = escaped_kw.replace(r'\*', r'\w*')
                    if '*' not in kw:
                        kw_regex = r'\b' + kw_regex + r'\b'

                processed_keywords.append(kw_regex)
                cond = df[col_name].str.contains(kw_regex, case=False, na=False, regex=True)
                group_condition = cond if group_condition is None else (group_condition | cond)

            processed_groups.append("({})".format(" OR ".join(processed_keywords)))
            overall_condition = group_condition if overall_condition is None else (overall_condition & group_condition)

            if self.debug:
                print(f"  Group: {group} => Keywords: {processed_keywords}")

        processed_query = " AND ".join(processed_groups)
        return overall_condition, processed_query

    def _save_query_log(self, stage, original_query, processed_query):
        log_file_path = os.path.join(self.result_folder_path, STAGE_TO_LOG.get(stage, QUERY_LOG_FILE))
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write(f"Stage: {stage}\n\n")
            f.write("User Provided Query:\n")
            f.write(original_query + "\n\n")
            f.write("Processed Query:\n")
            f.write(processed_query + "\n")
        if self.debug:
            print(f"Query log saved to {log_file_path}")

    @staticmethod
    def _combine_cols(df):
        df = df.copy()
        for c in ("Title", "Abstract", "Keywords"):
            if c not in df.columns:
                df[c] = ""
        df["combined"] = df["Title"].fillna('') + " " + df["Abstract"].fillna('') + " " + df["Keywords"].fillna('')
        return df

    def _apply_stage(self, df, stage: int):
        if stage not in (1, 2, 3):
            raise ValueError("Stage must be 1, 2, or 3.")

        query = STAGE_TO_QUERY[stage]
        df = self._combine_cols(df)

        related_condition, processed_query = self._build_condition(df, query, 'combined')
        self._save_query_log(stage, query, processed_query)

        df_out = df.copy()
        df_out["Related"] = related_condition.map({True: "Related", False: "Not Related"})

        all_path = os.path.join(self.result_folder_path, STAGE_TO_ALL[stage])
        df_out.to_excel(all_path, index=False)

        related_df = df_out[df_out["Related"] == "Related"].drop(columns=["combined"])
        filtered_path = os.path.join(self.result_folder_path, STAGE_TO_FILTERED[stage])
        related_df.to_excel(filtered_path, index=False)

        if self.debug:
            print(f"[Stage {stage}] Saved all -> {all_path}")
            print(f"[Stage {stage}] Saved related-only -> {filtered_path}")

        return all_path, filtered_path

    # ---------- public methods (kept + new) ----------


    # New staged interface
    def run_single_stage(self, stage: int):
        self._create_output_folder()
        df = pd.read_excel(self.input_file)
        return self._apply_stage(df, stage)

    def run_chained(self, stages=(1, 2, 3)):
        self._create_output_folder()
        df = pd.read_excel(self.input_file)
        outputs = {}
        for s in stages:
            all_p, filt_p = self._apply_stage(df, s)
            outputs[s] = (all_p, filt_p)
            df = pd.read_excel(filt_p)  # chain filtered into next stage
        return outputs


    def run_from_dedup(self, dedup_path: str = None):
        """
        Run Stage 1 -> Stage 2 -> Stage 3 starting explicitly from the
        de-duplicated file (02_Papers_without_duplicate.xlsx by default).

        Returns a dict {1: (all1, filt1), 2: (all2, filt2), 3: (all3, filt3)}.
        """
        # Default to the standard de-duplicated file path in results/
        if dedup_path is None:
            from config import FILTERED_DUPLICATE_FILE
            dedup_path = os.path.join(self.result_folder_path, FILTERED_DUPLICATE_FILE)

        if not os.path.exists(dedup_path):
            raise FileNotFoundError(f"De-duplicated file not found at: {dedup_path}")

        # Re-bind the input file to the de-duplicated file and chain all stages
        self.input_file = dedup_path
        return self.run_chained((1, 2, 3))
