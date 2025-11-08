#Author: MarwanMohammed
import matplotlib.pyplot as plt
import os
from config import RESULT_FOLDER, NUMERICAL_ANALYSIS_SUMMARY
import re
from collections import defaultdict

class NumericalAnalysisSummary:
    def __init__(self):
        # Define the folder path and file path
        base_directory = os.path.dirname(os.path.abspath(__file__))  # Get the current script's directory
        self.result_folder_path = os.path.join(base_directory, RESULT_FOLDER)
        os.makedirs(self.result_folder_path, exist_ok=True)  # Ensure the folder exists
        self.output_path = os.path.join(self.result_folder_path, NUMERICAL_ANALYSIS_SUMMARY)

    def process_and_plot_paper_trends(self):
        # Check if the summary file exists
        if not os.path.exists(self.output_path):
            print("No summary file found.")
            return

        # Dictionary to store query data
        query_data = defaultdict(dict)
        current_query = None

        # Read and parse the file
        with open(self.output_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                # Detect query headers
                if line.startswith("Query:"):
                    current_query = line.split("Query:")[1].strip()
                    query_data[current_query] = {}

                # Detect year-based paper counts
                match = re.match(r"(\d{4}):\s*(\d+)", line)
                if match and current_query:
                    year, count = match.groups()
                    query_data[current_query][int(year)] = int(count)

        # If no valid data was found
        if not query_data:
            print("No valid data found in the summary file.")
            return

        # Generate shorter labels for long query names
        short_labels = {query: f"Q{i+1}" for i, query in enumerate(query_data.keys())}

        # Create the figure and adjust its height to fit long query names
        fig, ax = plt.subplots(figsize=(12, 7))
        
        for query, yearly_counts in query_data.items():
            years = sorted(yearly_counts.keys())
            counts = [yearly_counts[year] for year in years]
            ax.plot(years, counts, marker='o', label=short_labels[query])  # Use short labels

        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Papers")
        ax.set_title("Research Paper Trends by Query")
        ax.legend(title="Short Labels")
        ax.grid(True)

        # Build the query legend text
        full_query_text = "\n".join([f"{short_labels[q]}: {q}" for q in query_data.keys()])

        # Adjust figure to make space for query labels under the plot
        fig.subplots_adjust(bottom=0.35)  # Reserve extra space at the bottom

        # Add the query legend below the figure
        plt.figtext(0.1, 0.02, full_query_text, wrap=True, horizontalalignment='left', fontsize=10)

        # Save the plot as an image
        plot_path = os.path.join(self.result_folder_path, "Numerical_plot.png")
        plt.savefig(plot_path, bbox_inches="tight")

        print(f"Plot saved to {plot_path}")