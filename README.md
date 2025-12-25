# Scoping Review: Child-Robot Interaction 

## Introduction

This scoping review examines methodologies and impacts of Child-Robot Interaction (CRI) across various domains, focusing particularly on language acquisition, adaptive learning systems, multimodal communication (speech, gaze, gestures), and emotional and social development. It highlights how social robots enhance engagement, learning outcomes, and developmental progress, along with addressing ethical concerns such as privacy and emotional well-being.

## Boolean Search Query

The extensive query used to retrieve relevant studies from academic databases:

```
(
    ("Human-Robot" OR "Child-Robot") AND 
    ("Robot") AND 
    ("Child*"  OR "Communit*" OR "Social") AND 
    ("Education" OR "School" OR "Learn*" OR "Caregiver" OR "Teach*" OR "Child-directed" OR "Speech" OR "Language" OR "Communication")
)
```
## Scoping Review Workflow and Data Processing Pipeline

This repo outlines the structured methodology used to conduct a scoping review integrating automated data processing and staged filtering. The workflow ensures transparency, reproducibility, and alignment with scoping review standards such as PRISMA.

---

### Overview

The review process is divided into major procedural stages designed to manage data collection, consolidation, Scanning (Title and abstract), Full text screening, and analysis in a transparent and replicable way.

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

## 4. Scanning Title and Abstract (Relevance Filtering)

Following de-duplication, the dataset underwent three automated relevance filtering stages to progressively refine the corpus of studies.

### STAGE 1
STAGE 1 is a broad scanning stage that is focussed on the general context of the terms of HRI and CRI. It is involved Python script (see Config.py using STAGE1)

STAGE1 = (
    '((Human-Robot OR Human Robot OR Human-robot Interaction OR Human robot Interaction OR HRI OR '
    'Child Robot OR Child-Robot OR Child-robot Interaction OR Child robot Interaction OR CRI OR Interact*) AND '
    '(Robot* OR Robotics) AND '
    '(User* OR Human* OR Person* OR People OR Child* OR Infant* OR Adult* OR Elderly OR Toddler* OR Preschool* OR School* OR Classroom OR Caregiver* OR Parent* OR Family OR Pediatric* ) AND '
    '(Social* OR Communicat* OR Dialogue OR Speech OR Languag* OR Talker OR Convers* OR Play OR Engagement OR Emotion* OR Cognit* OR Joint Attention OR Autism OR Neurodivergent OR Development* OR Interaction* OR Support OR Therapy OR Assistive OR Companion OR Service OR Healthcare OR Educat* OR Learn* OR Teach* OR Child-Directed OR vocaliz* OR vocabular*))'
)

- Excluded: 12564  papers
- hncluded: 9735 papers 


---

### STAGE 2
STAGE 2 is a narrow scanning stage which is scoped to the papers that certainly cover user groups of children or paediatrics with educational, communicative, or social outcomes (see Config.py using STAGE2).

STAGE2 = (
    '((Child Robot OR Child-Robot OR Child-robot Interaction OR Child robot Interaction OR CRI OR Interact*) AND '
    '(Robot* OR Robotics) AND '
    '(User* OR Adult* OR Child* OR Infant* OR Toddler* OR Preschool* OR School* OR Classroom OR Caregiver* OR Parent* OR Family OR Pediatric* ) AND '
    '(Social* OR Communicat* OR Dialogue OR Speech OR Languag* OR Talker OR Play OR Engagement OR Emotion* OR Cognit* OR Joint Attention OR Development* OR Interaction* OR Support OR Assistive OR  Educat* OR Learn* OR Teach* OR Child-Directed OR vocaliz* OR vocabular*))'
)

- Excluded: 4638  papers
- hncluded: 5097 papers
---

### STAGE 3
STAGE 3 is a more specific scanning stage, where the specific query was applied to the retained papers in stage 2. In this stage, the papers in which robots and children or their caregivers are directly interacting with each other in educational, clinical, developmental, or support contexts were retained (see Config.py using STAGE3).

STAGE3 = (
    '((Child Robot OR Child-Robot OR Child-robot Interaction OR Child robot Interaction OR CRI OR Interact*) AND '
    '(Robot* OR Robotics) AND '
    '(Child* OR Infant* OR Toddler* OR Caregiver* OR Parent*) AND '
    '(Social* OR Communicat* OR Dialogue OR Speech OR Languag* OR Talker OR Play OR Engagement OR Emotion* OR Cognit* OR Joint Attention OR Development* OR Interaction* OR Support OR Assistive OR  Educat* OR Learn* OR Teach* OR Child-Directed OR vocaliz* OR vocabular*))'
)

- Excluded: 4638  papers
- hncluded: 2805 papers

---

## 5. Full-text Articles Assessed
In this satge, two levels have been invovled 

### A. Python Script-Based and Manual Check 
Python Script (see Config.py using Sorting_Stage) was used to exclude papers not directly relevant to the research focus. Specifically, records were removed if they primarily involved topics such as Neurodivergence (e.g., Autism), Review articles, Ethics, Healthcare applications, Exoskeletons, Swarm Robotics, or Surgical Robotics.

- Excluded: 393  papers
- hncluded: 1899 papers

---
### B. LLM-Based and Manual Check 
Second is Large Language Model (LLM) Prompt along side the Manual Double check (Involved OpenAI GPT-based API (gpt-4.1, and gpt-4o) Refer to LLM_Screening.py and Manual double-Check).

LLMs were used to assess the remaining papers as implemented in LLM_Screening.py. Specifically, OpenAI GPT-based APIs (gpt-4.1 and gpt-4o) classified full-text papers as “related” or “not related” based on the criteria outlined in the Eligibility and Inclusion section. Each classification included a justification statement to ensure transparency.
Using LLMs significantly scaled the screening process, enabling faster and more consistent evaluation of a large volume of papers for a comprehensive literature review. To maintain reliability, all LLM outputs were manually reviewed by two researchers to confirm alignment with inclusion criteria.
Outcome:

- Excluded: 1693 papers
- hncluded: 206 papers (final evidence base for this scoping review)

Potential drawbacks, such as occasional misclassification or over-reliance on prior testing, were mitigated through manual verification and found to be negligible.

---

## 6. Data Extraction: Coding of Study Characteristics
The coding process and extracted features are documented in Final_Full_Features_ScRi.xlsx. Below are the key study characteristics and their rationale:

1. Sample Size: Indicates methodological maturity and research scope. Smaller samples often reflect exploratory studies, while larger samples suggest more rigorous designs.
2. Participant Age: Captures developmental stage; coded as minimum, maximum, and range due to frequent omission of mean/median ages.
3. Research/Application Domain: Categorized into three global domains:
    - Academic Support & Tutoring
    - Language & Literacy Development
    - Social & Emotional Development
    Sub-topics were identified based on learning domain or interaction type.

4. Country of Research: Assigned based on all authors’ affiliations; multi-country studies coded as “Multiple.”
5. Robot Role: Classified as Tutor, Peer, Tutee, Assistant, Storyteller, or Other (double-checked by two coders).
6. Interaction Control Approach: Categories include Rule-Based/Scripted, Wizard of Oz, Toolkit/Platform-Based, Reinforcement Learning, Other ML (Non-LLM), LLM, and Not Specified.
7. Robot Type (Platform): Recorded by brand/type (e.g., NAO, custom-built) and analyzed by Type Frequency (NAO vs. others) and Humanoid Status (humanoid vs. non-humanoid).
