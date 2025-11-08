#Author: MarwanMohammed
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from config import BASE_DIR, RESULT_FOLDER, NUMERICAL_ANALYSIS_SUMMARY, PAPERS_PER_YEAR_PLOT, DOCUMENT_IDENTIFIER_DISTRIBUTION_PLOT, SOURCE_DISTRIBUTION_PLOT, START_YEAR, END_YEAR


class MatricesEvaluation:
    def __init__(self, related_file):
        self.related_file = related_file
        self.df = pd.read_excel(self.related_file)
        self.result_folder_path = os.path.join(BASE_DIR, RESULT_FOLDER)
        os.makedirs(self.result_folder_path, exist_ok=True)

    def _filter_by_year(self, df, start_year=None, end_year=None):
        """
        Filters the DataFrame by the specified year range.
        If no range is provided, uses the default values from config.
        """
        print(start_year)
        if start_year is None:
            start_year = START_YEAR
        if end_year is None:
            end_year = END_YEAR
        return df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

    def _plot_papers_per_year(self, df):
        """
        Plots the number of papers per year and saves the figure.
        """
        if 'Year' in df.columns:
            papers_per_year = df['Year'].value_counts().sort_index()
            plt.figure(figsize=(10, 5))
            plt.bar(papers_per_year.index, papers_per_year.values, color='royalblue')
            plt.xlabel("Year")
            plt.ylabel("Number of Papers")
            plt.title("Number of Papers Per Year")
            plt.xticks(rotation=45)
            plt.savefig(os.path.join(self.result_folder_path, PAPERS_PER_YEAR_PLOT))
            plt.close()

    def _plot_document_identifier_distribution(self, df):
        """
        Plots the distribution of document identifiers and saves the figure.
        """
        if 'Document Identifier' in df.columns:
            doc_identifier_counts = df['Document Identifier'].value_counts()
            colors = plt.cm.Paired.colors[:len(doc_identifier_counts)]  # Generate distinct colors
            plt.figure(figsize=(8, 5))
            plt.pie(doc_identifier_counts, labels=doc_identifier_counts.index, autopct='%1.1f%%', 
                    startangle=90, colors=colors)
            plt.title("Distribution of Document Identifiers")
            plt.legend(doc_identifier_counts.index, title="Document Types", loc="best")
            plt.savefig(os.path.join(self.result_folder_path, DOCUMENT_IDENTIFIER_DISTRIBUTION_PLOT))
            plt.close()

    def _plot_source_distribution(self, df):
        """
        Plots the distribution of sources and saves the figure.
        """
        if 'Source' in df.columns:
            source_counts = df['Source'].value_counts().head(10)  # Show top 10 sources
            colors = plt.cm.Set3.colors[:len(source_counts)]  # Generate distinct colors
            plt.figure(figsize=(10, 5))
            plt.bar(source_counts.index, source_counts.values, color=colors)
            plt.xlabel("Source")
            plt.ylabel("Number of Papers")
            plt.title("Sources of Papers")
            plt.xticks(rotation=45)
            plt.savefig(os.path.join(self.result_folder_path, SOURCE_DISTRIBUTION_PLOT))
            plt.close()

    def _save_paper_summary(self, query, df, papers_per_year):
        """
        Saves a summary of the analysis to a text file.
        """
        output_path = os.path.join(self.result_folder_path, NUMERICAL_ANALYSIS_SUMMARY)
        with open(output_path, 'a', encoding='utf-8') as file:
            file.write(f"Query: {query}\n")
            file.write(f"Total Papers: {len(df)}\n")
            file.write("Papers Per Year:\n")
            for year, count in sorted(papers_per_year.items()):  # Ensure years are in order
                file.write(f"{year}: {count}\n")
            file.write("\n")  # Add a newline for separation
        print(f"Summary successfully saved to {output_path}")

    def analyze(self, query, start_year=None, end_year=None):
        """
        Analyzes and visualizes:
        1. Number of papers per year (filtered by user input or config defaults).
        2. Distribution of Document Identifiers (Conf, Journal, Book, etc.).
        3. Analysis of the Source column.
        """
        df = self.df.copy()

        # Ensure 'Year' column is numeric
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

        # Filter by user-specified year range or config defaults
        df = self._filter_by_year(df, start_year, end_year)

        # --- Plot 1: Papers per Year ---
        if 'Year' in df.columns:
            papers_per_year = df['Year'].value_counts().sort_index()
            self._plot_papers_per_year(df)

        # --- Plot 2: Document Identifier Distribution ---
        if 'Document Identifier' in df.columns:
            self._plot_document_identifier_distribution(df)

        # --- Plot 3: Source Distribution ---
        if 'Source' in df.columns:
            self._plot_source_distribution(df)

        # Save numerical analysis summary
        if 'Year' in df.columns:
            self._save_paper_summary(query, df, papers_per_year )

        print(f"\n✅ Plots saved in: {self.result_folder_path}")