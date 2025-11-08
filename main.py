# Author: MarwanMohammed
import argparse
import os
import pandas as pd
from config import (
    FOLDER_NAMES, CONSOLIDATED_FILE, FILTERED_DUPLICATE_FILE,
    RESULT_FOLDER, START_YEAR, END_YEAR, CLASSIFIED_PAPERS_FILE,
    # staged outputs (for existence checks)
    STAGE1_FILTERED_FILE, STAGE2_FILTERED_FILE, STAGE3_FILTERED_FILE,
    # legacy names (still referenced later) 
)
from paper_consolidator import PaperConsolidator
from duplicate_filter import DuplicateFilter
from related_paper_filter import RelatedPaperFilter
from paper_classifier import PaperClassifier
from matrices_evaluation import MatricesEvaluation
from Numerical_Analysis import NumericalAnalysisSummary
from classification_stats import write_classification_summaries

def _analyze_step(file_path, label, start_year, end_year, result_folder_path):
    if file_path and os.path.exists(file_path):
        analysis = MatricesEvaluation(file_path)
        analysis.analyze(query=label, start_year=int(start_year), end_year=int(end_year))
        print(f"[Analysis] {label} → results saved in: {result_folder_path}")
    else:
        print(f"[Analysis] Skipped ({label}) — no valid file.")

def _looks_like_related_file(path: str) -> bool:
    try:
        cols = pd.read_excel(path, nrows=0).columns
        # Many of your staged files have a 'Related' flag; keep it lenient:
        return "Title" in cols or "Related" in cols
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="Process and classify papers.")
    parser.add_argument("--folder_names", type=str, default=FOLDER_NAMES, help="Comma-separated source folders, e.g., 'IEEE,WoS,SD'.")
    parser.add_argument("--start_year", type=str, default=START_YEAR, help="Start year.")
    parser.add_argument("--end_year", type=str, default=END_YEAR, help="End year.")

    # legacy steps
    parser.add_argument("--run_consolidate", action="store_true", help="Run consolidation step.")
    parser.add_argument("--run_duplicates", action="store_true", help="Run duplicate filtering step.")
    # new staged options
    parser.add_argument("--run_stage1", action="store_true", help="Run Stage 1 (Broad) on current input.")
    parser.add_argument("--run_stage2", action="store_true", help="Run Stage 2 (Narrow) on current input.")
    parser.add_argument("--run_stage3", action="store_true", help="Run Stage 3 (Specific) on current input.")

    parser.add_argument("--run_staged", action="store_true", help="Run Stage 1 -> Stage 2 -> Stage 3 chained.")
    parser.add_argument("--run_staged_from_dedup", action="store_true", help="Run Stage 1 -> 2 -> 3 starting from the de-duplicated file.")

    parser.add_argument("--run_classification", action="store_true", help="Run classification step.")
    parser.add_argument("--classify_from",type=str, help="Explicit path to the Excel to classify (overrides last_output).")
    parser.add_argument("--classify_using", choices=["title","abstract","both"], default="both", help="Pick which text to use for classification.")

    parser.add_argument("--run_analysis", action="store_true", help="Run analysis step.")
    parser.add_argument("--run_numerical", action="store_true", help="Run numerical analysis step.")
    parser.add_argument("--summarize_classes", action="store_true", help="After classification, write label summaries (overall and by year).")


    args = parser.parse_args()

    result_folder_path = os.path.join(os.getcwd(), RESULT_FOLDER)
    os.makedirs(result_folder_path, exist_ok=True)
    last_output = None

    # Step 1: Consolidation
    consolidated_output = os.path.join(result_folder_path, CONSOLIDATED_FILE)
    
    if args.run_consolidate:
        consolidator = PaperConsolidator(folder_names=args.folder_names)
        consolidated_output = consolidator.consolidate()
        print("Consolidation complete. Output at:", consolidated_output)
        last_output = consolidated_output

        if args.run_analysis:
            _analyze_step(last_output, "After Consolidation", args.start_year, args.end_year, result_folder_path)

    elif os.path.exists(consolidated_output):
        print("Using existing consolidated file at:", consolidated_output)
        last_output = consolidated_output
    else:
        print("Error: No consolidated file found. Please run consolidation first.")
        return

    # Step 2: Duplicate Filtering
    filtered_file = os.path.join(result_folder_path, FILTERED_DUPLICATE_FILE)
    if args.run_duplicates:
        dup_filter = DuplicateFilter(input_excel=last_output)
        _, filtered_file = dup_filter.filter_duplicates()
        print("Duplicate filtering complete. Output at:", filtered_file)
        last_output = filtered_file
        if args.run_analysis:
            _analyze_step(last_output, "After Duplicate Filtering", args.start_year, args.end_year, result_folder_path)

    elif os.path.exists(filtered_file):
        print("Using existing duplicate filtered file at:", filtered_file)
        last_output = filtered_file
    else:
        print("Warning: No duplicate filtered file found. Proceeding without duplicate filtering.")

    # Step 3: Related Filtering — staged options
    rpf = RelatedPaperFilter(input_file=last_output, debug=True)

    if args.run_staged_from_dedup:
        outputs = rpf.run_from_dedup()  # starts from the standard dedup file in results/
        last_output = os.path.join(result_folder_path, STAGE3_FILTERED_FILE)
        print("Staged-from-dedup filtering complete. Final output at:", last_output)

    # Full chained stages 1->2->3
    elif args.run_staged:
        outputs = rpf.run_chained((1, 2, 3))
        last_output = os.path.join(result_folder_path, STAGE3_FILTERED_FILE)
        print("Staged filtering complete. Final output at:", last_output)
        if args.run_analysis:
            _analyze_step(last_output, "Full chained stages 1->2->3", args.start_year, args.end_year, result_folder_path)
    else:
        # Single stages (new flags)
        if args.run_stage1:
            _, stage1_filtered = rpf.run_single_stage(1)
            last_output = stage1_filtered
            print("Stage 1 complete. Output at:", stage1_filtered)
            if args.run_analysis:
                _analyze_step(last_output, "run_stage1", args.start_year, args.end_year, result_folder_path)
        if args.run_stage2:
            # if stage2 requested without stage1, we use current last_output
            rpf = RelatedPaperFilter(input_file=last_output, debug=True)
            _, stage2_filtered = rpf.run_single_stage(2)
            last_output = stage2_filtered
            print("Stage 2 complete. Output at:", stage2_filtered)
            if args.run_analysis:
                _analyze_step(last_output, "run_stage2", args.start_year, args.end_year, result_folder_path)

        if args.run_stage3:
            rpf = RelatedPaperFilter(input_file=last_output, debug=True)
            _, stage3_filtered = rpf.run_single_stage(3)
            last_output = stage3_filtered
            print("Stage 3 complete. Output at:", stage3_filtered)
            if args.run_analysis:
                _analyze_step(last_output, "run_stage3", args.start_year, args.end_year, result_folder_path)

        
        # If none of the above flags, but prior stage files exist, choose latest available
        if last_output is None:
            for candidate in (STAGE3_FILTERED_FILE, STAGE2_FILTERED_FILE, STAGE1_FILTERED_FILE):
                p = os.path.join(result_folder_path, candidate)
                if os.path.exists(p):
                    last_output = p
                    print("Using existing related file at:", p)
                    break
            if last_output is None:
                print("Warning: No related filtering performed.")

    # # Step 4: Classification
    # classified_output = os.path.join(result_folder_path, CLASSIFIED_PAPERS_FILE)
    # if args.run_classification:
    #     classifier = PaperClassifier(input_file=last_output)
    #     classified_output = classifier.classify()
    #     print("Classification complete. Output at:", classified_output)
    #     last_output = classified_output
    #     if args.run_analysis:
    #         _analyze_step(last_output, "After Classification", args.start_year, args.end_year, result_folder_path)
    # elif os.path.exists(classified_output):
    #     print("Using existing classified papers file at:", classified_output)
    #     last_output = classified_output
    #     if args.run_analysis:
    #         _analyze_step(last_output, "After Classification", args.start_year, args.end_year, result_folder_path)
    # else:
    #     print("Warning: No classified file found. Proceeding without classification.")


    # Step 4: Classification
    classified_output = os.path.join(result_folder_path, CLASSIFIED_PAPERS_FILE)
    if args.run_classification:
        classify_input = None
        # 1) If user explicitly provided a file, use it (with a quick sanity check)
        if args.classify_from:
            if os.path.exists(args.classify_from) and _looks_like_related_file(args.classify_from):
                classify_input = args.classify_from
            else:
                print(f"Error: --classify_from not usable: {args.classify_from}")
                classify_input = None

        # 2) Otherwise, fall back to whatever the pipeline last produced
        if classify_input is None:
            classify_input = last_output

        if not classify_input or not os.path.exists(classify_input):
            print("Error: No suitable input found for classification.")
        else:
            # classifier = PaperClassifier(input_file=classify_input)
            classifier = PaperClassifier(input_file=classify_input, mode=args.classify_using)
            classified_output = classifier.classify()
            print("Classification complete.")
            print("  Input :", classify_input)
            print("  Output:", classified_output)
            last_output = classified_output
            # Auto-summary (guarded by flag, or make it always-on if you prefer)
            try:
                if getattr(args, "summarize_classes", False):
                    overall_path, by_year_path = write_classification_summaries(
                        classified_output, result_folder_path
                    )
                    print("Classification summaries written:")
                    print("  Overall:", overall_path)
                    print("  By year:", by_year_path)
            except Exception as e:
                print("Warning: could not write classification summaries:", e)

            if args.run_analysis:
                _analyze_step(last_output, "After Classification",
                            args.start_year, args.end_year, result_folder_path)

    elif os.path.exists(classified_output):
        print("Using existing classified papers file at:", classified_output)
        last_output = classified_output
        if args.run_analysis:
            _analyze_step(last_output, "After Classification",
                        args.start_year, args.end_year, result_folder_path)
    else:
        print("Warning: No classified file found. Proceeding without classification.")


    # Step 5: Analysis
    if args.run_analysis:
        if last_output and os.path.exists(last_output):
            analysis = MatricesEvaluation(last_output)
            # Keep the previous behavior but simplify "query" label:
            analysis_query = "Staged Filtering / Latest Output"
            analysis.analyze(query=analysis_query, start_year=int(args.start_year), end_year=int(args.end_year))
            print("Analysis complete. Results saved in:", result_folder_path)
        else:
            print("Error: No valid input file for analysis.")
    else:
        print("Analysis step skipped.")

    # Step 6: Numerical Analysis
    if args.run_numerical:
        numerical_analysis = NumericalAnalysisSummary()
        numerical_analysis.process_and_plot_paper_trends()
        print("Numerical analysis complete. Results saved in:", result_folder_path)
    else:
        print("Numerical analysis step skipped.")

if __name__ == "__main__":
    main()
