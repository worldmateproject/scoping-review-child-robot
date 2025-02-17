# Systematic-Review
This review examines the role of Human-Robot and Child-Robot Interaction in early childhood education, with a focus on language acquisition. It explores how social robots process multimodal inputs (speech, gaze, gestures) to enhance communication, sustain engagement, and adapt to children’s needs. Key topics include adaptive learning systems, emotion detection, real-time interaction, and ethical considerations such as privacy and emotional well-being. By highlighting current advancements and challenges, this paper provides insights for improving robot-assisted language learning and child development.

## Pre-Query Analysis Report

This report presents an analysis of the queries used in the systematic review process. Each query was assessed for its ability to capture relevant studies, and based on this evaluation, the most comprehensive query was identified. 

| Query ID | Query Key Search | Papers Retrieved (IEEE Xplore) |
|----------|------------------|--------------------------------|
| Q1       | (“Human-Robot Interaction” OR “Child-Robot Interaction”) AND (“Robots”) AND (“Education” OR “School” OR “Learning”) AND (“Child” OR “Childhood” OR “Children”) | 358 |
| Q2       | (“Human-Robot Interaction” OR “Child-Robot Interaction”) AND (“Robots” OR “Social Robots”) AND (“Community” OR “Social”) AND (“Education” OR “School” OR “Learning”) | 1425 |
| Q3       | (“Human-Robot Interaction” OR “Child-Robot Interaction”) AND (“Robots” OR “Social Robots”) AND (“Community” OR “Social”) AND (“Education” OR “School” OR “Learning” OR “Caregiver” OR “Child Directed Speech”) | 1480 |
| Q4       | ((“Human-Robot Interaction” OR “Child-Robot Interaction” OR “Interaction”) AND (“Robot”) AND (“Child* OR “Community” OR “Social”) AND (“Education” OR “School” OR “Learning” OR “Caregiver” OR “Child-Directed Speech” OR “Talker”)) | 2596 |
| Q5       | ((“Human-Robot Interaction” OR “Child-Robot Interaction” OR “Interaction”) AND (“Robot”) AND (“Child*”) AND (“Education” OR “School” OR “Learning” OR “Caregiver” OR “Child-Directed Speech” OR “Talker”)) | 604 |
| Q6       | ((“Human-Robot Interaction” OR “Child-Robot Interaction” OR “Interaction”) AND (“Robot*”) AND (“Child*” OR “Community*” OR “Social*”) AND (“Education*” OR “School*” OR “Learn*” OR “Caregiver” OR “Child-Directed Speech” OR “Speech Interaction” OR “Talker”)) | 3186 |
| Q7       | ((“Human-Robot Interaction” OR “Child-Robot Interaction” OR “Interaction”) AND (“Robot*”) AND (“Child*”) AND (“Education*” OR “School*” OR “Learn*” OR “Caregiver” OR “Child-Directed Speech” OR “Speech Interaction” OR “Talker”)) | 690 |
| Q8       | ((“Human-Robot” OR “Child-Robot”) AND (“Robot”) AND (“Child*” OR “Communit*” OR “Social”) AND (“Education” OR “School” OR “Learn*” OR “Caregiver” OR “Teach*” OR “Child-Directed” OR “Speech” OR “Language” OR “Communication”)) | 2410 |
| Q9       | (((“Human-Robot” OR “Child-Robot” OR “Interaction”) AND (“Robot*”) AND (“Child*” OR “Communit*” OR “Social*”) AND (“Education*” OR “School*” OR “Learn*” OR “Caregiver” OR “Child-Directed Speech” OR “Language” OR “Communication” OR “Teach*” OR “Talker”)) ) | 4065 |
| Q10      | ((“Human-Robot” OR “Child-Robot” OR “Interaction”) AND (“Robot*”) AND (“Child*” OR “Communit*” OR “Social*”) AND (“Education*” OR “School*” OR “Learn*” OR “Caregiver” OR “Child-Directed” OR "Speech" OR “Languag*” OR “Communicat*” OR “Teach*” OR “Talker”)) | **4165** |

The analysis showed that Query Q10 retrieved the largest number of papers (4,165), including all papers captured by the previous nine queries (Q1–Q9) from IEEE Xplore. As a result, Q10 is considered the most comprehensive query for this systematic review and will be used as the final query to ensure that no relevant papers are overlooked.
![Image](https://github.com/user-attachments/assets/29ef2ab1-f8d5-4cc6-860c-0f37f38fcbd2)


# Research Paper Retrieval Statistics

## Overview
This section presents data on the number of research papers retrieved using **Q10** across six major academic databases: IEEE, Web of Science (WoS), ACM, Scopus, ScienceDirect (SD), and PubMed. The data covers the years **2015 to 2025**, showing the trend of research paper retrieval over time. The primary objective of this study is to analyze the availability and growth of research articles in various academic databases, providing insights into publication trends in recent years. The table below displays the number of research papers retrieved from each database for the years  **2015 to 2025**. 

| Year  | IEEE | WoS  | ACM  | Scopus | SD   | PubMed | Total  |
|-------|------|------|------|--------|------|--------|--------|
| 2015  | 233  | 210  | 369  | 447    | 352  | 37     |        |
| 2016  | 294  | 264  | 481  | 431    | 348  | 43     |        |
| 2017  | 309  | 313  | 514  | 545    | 404  | 51     |        |
| 2018  | 350  | 373  | 644  | 577    | 448  | 70     |        |
| 2019  | 401  | 408  | 553  | 648    | 560  | 75     |        |
| 2020  | 373  | 477  | 830  | 1023   | 749  | 108    |        |
| 2021  | 424  | 506  | 924  | 1021   | 925  | 188    |        |
| 2022  | 596  | 550  | 1062 | 859    | 988  | 205    |        |
| 2023  | 563  | 483  | 1258 | 893    | 1109 | 172    |        |
| 2024  | 606  | 592  | 1743 | 1026   | 1430 | 157    |        |
| 2025  | 10   | 24   | 83   | 53     | 439  | 12     |        |
| **Total** | **4159** | **4200** | **8461** | **7523** | **7752** | **1118** | **33213** |

This dataset represents the **retrieval of research papers** using Q10 from **six different academic databases**. The numbers indicate how many papers were found in each database for a given year. 
![Illustration](Survey.png)

## Key Observations:
1. **Overall Growth**:  
   - The number of retrieved papers increased significantly from 2015 to 2024.
   - The highest number of papers retrieved was in **2024**, showing a peak in research publications.
2. **Database Differences**:  
   - **ACM** has the highest number of retrieved papers (**8,461 total**).
   - **PubMed** has the lowest count (**1,118 total**), likely due to its focus on medical and life sciences.
3. **Decrease in 2025**:  
   - A sudden drop in 2025 may indicate incomplete data collection or a shift in research trends.

The data highlights the increasing volume of academic research over the years, particularly in **ACM, Scopus, and SD** databases. The significant rise in papers retrieved suggests that more research is being published and indexed across multiple databases.



# Research Paper Processing

## Removing Duplicates

In this stage, duplicate papers are removed based on DOI and Title across multiple search engines, including IEEE, WoS, SD, Scopus, ACM, and PubMed. Additionally, review papers and those primarily presenting literature reviews are excluded. After this stage, the remaining papers are as follows:

| Source  | Papers Remaining |
|---------|----------------|
| IEEE    | 3,954          |
| WoS     | 2,852          |
| Scopus  | 2,267          |
| SD      | 7,131          |
| ACM     | 5,672          |
| PubMed  | 423            |
| **Total** | **22,299** |

## Filtering by Abstract, Title, and Keywords

In the next stage, the remaining papers will be screened based on their Abstract, Title, and Author Keywords to filter those relevant to the study scope.
This project involves processing a CSV file containing metadata for over 20,000 research papers on child-robot interaction in education, language learning, and social development. Using the metadata (Title, Abstract, and Keywords), each paper will be assigned a **Relevance Score (0-100%)** based on predefined **inclusion** and **exclusion** criteria.

## Relevance Criteria

### **Inclusion Criteria (Highly Relevant Papers)**
A paper is considered **highly relevant (80-100%)** if it meets one or more of the following criteria:
- **Empirical or experimental research** involving child-robot interaction (not just conceptual models or theoretical discussions).
- **Education-focused applications**, such as:
  - **Robot tutors & AI-driven learning** (personalized education, engagement, cognitive development).
  - **Socialization & well-being** (robot-assisted therapy, emotional support, companionship, developmental assistance).
  - **Language acquisition** (robots aiding in vocabulary development, communication skills).
  - **Adaptive AI-powered interactions** (machine learning models tailoring robotic responses to a child’s progress).
  - **Children with special needs** (robot-assisted therapy for autism, speech delays, or cognitive disabilities).
- Studies that provide **measurable outcomes** in learning, engagement, cognitive development, or socialization.
- Research leveraging **AI, machine learning, or adaptive models** to enhance child-robot educational experiences.

### **Exclusion Criteria (Less or Not Relevant Papers)**
A paper is excluded (**scored below 60%**) if:
- It is a **literature review, meta-analysis, or theoretical framework** rather than an empirical study.
- It **lacks measurable outcomes** (e.g., opinion pieces, purely technical system descriptions).
- It focuses on **general human-robot interaction (HRI)** without a clear emphasis on child-robot interaction.
- It discusses robots in **non-relevant domains** (e.g., military, industrial applications, banking chatbots).

Papers containing the following keywords are automatically marked as **Not Relevant (<60%)**:
- “Systematic review”
- “Meta-analysis”
- “Survey of studies”
- “Overview of research”
- “Theoretical framework”
- “Trends in research”
- “Analysis of previous work”

Even if such papers discuss child-robot interaction, they are **excluded** due to their lack of original empirical insights.

## Scoring Guidelines

After filtering, each paper will be assigned a **Relevance Score (0-100%)** based on the depth of empirical evidence, measurable outcomes, and direct relevance to child-robot interaction.

- **80-100% (Highly Relevant)**: Papers that strongly align with the **inclusion criteria**, demonstrating clear **empirical results** in education, language learning, or child development. These studies typically present well-defined experiments, measurable impacts, and AI-driven innovations for children’s learning and interaction.
  - **Example**: _“This paper scored 90% because it presents a randomized controlled trial showing improved language acquisition in preschoolers using an AI-driven robot tutor.”_

- **60-79% (Moderately Relevant)**: Papers that are **somewhat related** but may **lack strong empirical validation**, have an **indirect focus** on child-robot interaction, or provide only **exploratory insights** without clear experimental evidence.
  - **Example**: _“This paper scored 70% because it discusses child-robot interactions in therapy settings but lacks concrete experimental results.”_

- **Below 60% (Not Relevant)**: Papers that are **theoretical, literature reviews, or focus on broader HRI** without specific child-related applications. These papers often fail to provide **measurable outcomes** or **direct experimental evidence**.
  - **Example**: _“This paper scored 50% because it is a review of past studies without introducing new empirical findings.”_

## Output Format

The final CSV file will retain all original metadata (**Title, Abstract, Keywords**) and add the following fields:
- **Relevance Score (0-100%)**
- **Relevant (Yes/No)**
- **Reason for Score**:
  - **Main idea of the study** – What the research is about.
  - **Primary focus** – How it relates to child-robot interaction.
  - **What it does not focus on** – Why it might be less relevant or not fully aligned.







