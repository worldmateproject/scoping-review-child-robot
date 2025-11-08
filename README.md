# 📚 README.md

# Systematic Review: Child-Robot Interaction 

## Introduction

This systematic review examines methodologies and impacts of Child-Robot Interaction (CRI) across various domains, focusing particularly on language acquisition, adaptive learning systems, multimodal communication (speech, gaze, gestures), and emotional and social development. It highlights how social robots enhance engagement, learning outcomes, and developmental progress, along with addressing ethical concerns such as privacy and emotional well-being.

## Comprehensive Search Query

The extensive query used to retrieve relevant studies from academic databases:

```
(
    ("Human-Robot" OR "Child-Robot") AND 
    ("Robot") AND 
    ("Child*"  OR "Communit*" OR "Social") AND 
    ("Education" OR "School" OR "Learn*" OR "Caregiver" OR "Teach*" OR "Child-directed" OR "Speech" OR "Language" OR "Communication")
)
```
## Systematic Review Workflow and Data Processing Pipeline

This document outlines the structured methodology used to conduct a systematic review integrating automated data processing and staged filtering. The workflow ensures transparency, reproducibility, and alignment with systematic review standards such as PRISMA.

---

### Overview

The review process is divided into major procedural stages designed to manage data collection, consolidation, filtering, classification, and analysis in a transparent and replicable way.

The stages are:
1. **Data Collection**
2. **Consolidation**
3. **Duplicate Removal**
4. **Relevance Filtering**
   - Stage 1 – Broad Filtering  
   - Stage 2 – Narrow Filtering  
   - Stage 3 – Specific Filtering
5. **Sorting and Manual Screening**
6. **Classification**
7. **Analysis and Reporting**

---

### 1. Data Collection

#### Databases Searched
The following digital libraries and scientific databases were queried to ensure comprehensive coverage:
- IEEE Xplore  
- Web of Science (WoS)  
- Scopus  
- ScienceDirect  
- ACM Digital Library  
- PubMed 

#### Search Strategy
A unified and structured set of Boolean search queries was developed for each database, targeting literature at the intersection of:
- Human–Robot Interaction (HRI)
- Child–Robot Interaction (CRI)
- Educational, developmental, and communication outcomes

All search strings were adapted for the syntax and field specifications of each database to maximize recall while ensuring conceptual consistency.

---


### 2. Consolidation

All retrieved bibliographic data were merged into a single structured dataset.  
During consolidation:
- Metadata fields (Title, Authors, Year, DOI, Source, Document Type, Abstract, and Keywords) were standardized.  
- Redundant and missing data entries were harmonized.  
- The consolidated dataset formed the foundation for subsequent filtering and classification stages.

The output of this stage represents the total number of publications retrieved before screening.

#### 📈 Paper Retrieval Statistics (2015-2025)

Retrieval statistics from IEEE, Web of Science (WoS), ACM, Scopus, ScienceDirect (SD), and PubMed:

| Year      | IEEE | WoS  | ACM  | Scopus | SD   | PubMed | Total     |
| --------- | ---- | ---- | ---- | ------ | ---- | ------ | --------- |
| 2015      | 233  | 210  | 369  | 447    | 352  | 37     | 1648      |
| 2016      | 294  | 264  | 481  | 431    | 348  | 43     | 1861      |
| 2017      | 309  | 313  | 514  | 545    | 404  | 51     | 2136      |
| 2018      | 350  | 373  | 644  | 577    | 448  | 70     | 2462      |
| 2019      | 401  | 408  | 553  | 648    | 560  | 75     | 2645      |
| 2020      | 373  | 477  | 830  | 1023   | 749  | 108    | 3560      |
| 2021      | 424  | 506  | 924  | 1021   | 925  | 188    | 3988      |
| 2022      | 596  | 550  | 1062 | 859    | 988  | 205    | 4260      |
| 2023      | 563  | 483  | 1258 | 893    | 1109 | 172    | 4478      |
| 2024      | 606  | 592  | 1743 | 1026   | 1430 | 157    | 5554      |
| 2025      | 10   | 24   | 83   | 53     | 439  | 12     | 621       |
| **Total** | 4159 | 4200 | 8461 | 7523   | 7752 | 1118   | **33213** |

---


### 3. Duplicate Removal

The de-duplication process ensured that identical and near-identical records from multiple databases were removed.  
Duplicates were detected through:
- Normalization and comparison of DOI identifiers.  
- Title fingerprinting and fuzzy-matching algorithms to identify slight variations in titles.  

A final unique dataset was produced, containing only one instance of each publication.

- Records After Duplicates Removed (n= 22299) : Involved Python script (10,165) and Manual double-check (749). Total records Excluded: (n =10,914)

---

## 4. Relevance Filtering

Following de-duplication, the dataset underwent three automated relevance filtering stages to progressively refine the corpus of studies.

### STAGE 1 — Broad Filtering
Involved Python script (looking at Config.py using STAGE1 (n =9735). Total Records Excluded: (n=12564) 
# Stage 1 — Broad HRI and CRI
STAGE1 = (
    '((Human-Robot OR Human Robot OR Human-robot Interaction OR Human robot Interaction OR HRI OR '
    'Child Robot OR Child-Robot OR Child-robot Interaction OR Child robot Interaction OR CRI OR Interact*) AND '
    '(Robot* OR Robotics) AND '
    '(User* OR Human* OR Person* OR People OR Child* OR Infant* OR Adult* OR Elderly OR Toddler* OR Preschool* OR School* OR Classroom OR Caregiver* OR Parent* OR Family OR Pediatric* ) AND '
    '(Social* OR Communicat* OR Dialogue OR Speech OR Languag* OR Talker OR Convers* OR Play OR Engagement OR Emotion* OR Cognit* OR Joint Attention OR Autism OR Neurodivergent OR Development* OR Interaction* OR Support OR Therapy OR Assistive OR Companion OR Service OR Healthcare OR Educat* OR Learn* OR Teach* OR Child-Directed OR vocaliz* OR vocabular*))'
)

---

### STAGE 2 — Narrow Filtering
- Involved Python script (looking at Config.py using STAGE2) (n = 5097). Total Records Excluded: (n= 4638) 
STAGE2 = (
    '((Child Robot OR Child-Robot OR Child-robot Interaction OR Child robot Interaction OR CRI OR Interact*) AND '
    '(Robot* OR Robotics) AND '
    '(User* OR Adult* OR Child* OR Infant* OR Toddler* OR Preschool* OR School* OR Classroom OR Caregiver* OR Parent* OR Family OR Pediatric* ) AND '
    '(Social* OR Communicat* OR Dialogue OR Speech OR Languag* OR Talker OR Play OR Engagement OR Emotion* OR Cognit* OR Joint Attention OR Development* OR Interaction* OR Support OR Assistive OR  Educat* OR Learn* OR Teach* OR Child-Directed OR vocaliz* OR vocabular*))'
)

---

### STAGE 3 — Specific Filtering
- Involved Python script (looking at Config.py using STAGE3) (n = 2292). Total Records Excluded: (n= 2,805) 
STAGE3 = (
    '((Child Robot OR Child-Robot OR Child-robot Interaction OR Child robot Interaction OR CRI OR Interact*) AND '
    '(Robot* OR Robotics) AND '
    '(Child* OR Infant* OR Toddler* OR Caregiver* OR Parent*) AND '
    '(Social* OR Communicat* OR Dialogue OR Speech OR Languag* OR Talker OR Play OR Engagement OR Emotion* OR Cognit* OR Joint Attention OR Development* OR Interaction* OR Support OR Assistive OR  Educat* OR Learn* OR Teach* OR Child-Directed OR vocaliz* OR vocabular*))'
)

---

Each filtering stage produced two datasets:
- **Full Output:** All records labeled as either “Related” or “Not Related.”  
- **Filtered Output:** Only records labeled “Related,” forwarded to the next stage of analysis.

---

## 5. Full-text Articles Assessed
In this satge, two ways have been invovled 
First,  Python Script script (looking at Config.py using Sorting_Stage) was used to exclude papers not directly relevant to the research focus. Specifically, records were removed if they primarily involved topics such as Neurodivergence (e.g., Autism), Review articles, Ethics, Healthcare applications, Exoskeletons, Swarm Robotics, or Surgical Robotics. 
Total Records Excluded: (n = 393), 
Total Records Included:(n = 1899)

The second is LLM Prompt along side the Manual Double check (Involved OpenAI GPT-based API (gpt-4.1, and gpt-4o) Refer to LLM_Screening.py and Manual double-Check).

### Child–Robot Interaction Paper Screening (LLM-Based)
The tool employs a Large Language Model (LLM) to classify papers as **related** or **not related** according to strict inclusion criteria.
The pipeline reads research papers in PDF format, extracts text, and screens each document using an OpenAI model.  
It outputs an Excel file summarizing whether each paper meets the eligibility criteria for inclusion in the review.

**Goal:**  
Filter approximately **1,899 candidate papers** to about **207 eligible studies** for detailed data extraction.

**Features:**
- ✅ Fully automated screening of PDFs — no manual tagging required  
- ✅ Applies consistent, transparent eligibility criteria  
- ✅ Produces clear output with:
  - `"Related"` → “Yes” / “No”  
  - `"Justification"` → one-line rationale for inclusion/exclusion  
- ✅ Compatible with GPT-4.1-mini or GPT-4-turbo via the OpenAI API  
- ✅ Exports results to `Screening_Results.xlsx` for filtering and review  


Refer to LLM_Screening.py

---

## 6. Included Sources of Evidence
 Included Sources of Evidence (n=207)



