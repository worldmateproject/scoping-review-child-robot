import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER_NAMES = "IEEE,WoS,SD,Scopus,ACM,PubMed"

# Output folder and file names
RESULT_FOLDER = "results"
CONSOLIDATED_FILE = "01_consolidated_papers.xlsx"
FILTERED_DUPLICATE_FILE = "02_Papers_without_duplicate.xlsx"
OUTPUT_WITH_FLAGS = "03_output_with_duplicate_flags.xlsx"

# Stage outputs (all rows with flag)
STAGE1_ALL_FILE = "04_stage1_broad_all.xlsx"
STAGE2_ALL_FILE = "04_stage2_narrow_all.xlsx"
STAGE3_ALL_FILE = "04_stage3_specific_all.xlsx"

# Stage filtered outputs (Related only)
STAGE1_FILTERED_FILE = "05_stage1_broad_filtered.xlsx"
STAGE2_FILTERED_FILE = "05_stage2_narrow_filtered.xlsx"
STAGE3_FILTERED_FILE = "05_stage3_specific_filtered.xlsx"

# Backward-compat names (kept for other modules / legacy)
RELATED_PAPERS_FILE = STAGE1_ALL_FILE
FILTERED_RELATED_PAPERS_FILE = STAGE1_FILTERED_FILE

# Logs
STAGE1_QUERY_LOG = "stage1_broad_query_log.txt"
STAGE2_QUERY_LOG = "stage2_narrow_query_log.txt"
STAGE3_QUERY_LOG = "stage3_specific_query_log.txt"
QUERY_LOG_FILE = STAGE1_QUERY_LOG  # legacy alias

CLASSIFIED_PAPERS_FILE = "06_classified_papers.xlsx"


# Allowed file extensions
ALLOWED_EXTENSIONS = (".bib", ".ris", ".txt", ".nbib")

# Mapping for standardizing document identifiers
DOCUMENT_IDENTIFIER_MAPPING = {
    'Conf': ['Inproceedings', 'Cpaper', 'CONF', 'Conference Paper', 'Proc', 'proceeding', 'proceedings', 'Workshop', 'Symposium', 'techreport', 'STD'],
    'Journal': ['Jour', 'Journal', 'Article', 'Journ', 'Jrnl', 'Research Article', 'Review', 'Editorial', 'Magazine', 'E-A-Articles'],
    'Book': ['Book', 'inbook', 'Book Chapter', 'Monograph', 'Edited Volume', 'Handbook', 'Lecture Notes', 'Chap', 'Chapter']
}

# Titles/abstracts to remove
TITLES_TO_REMOVE = ["Index", "INDEX", "Subject Index", "PC-FACS", "Contents", "Preface", "Table of Contents", "ISSID",
                    "Acknowledgement to Reviewers", "Contributors", "Authors’ biographies", "List of Abbreviations"]
ABSTRACTS_TO_REMOVE = ["Background", "Purpose", "Abstract:", "Abstract", "Objective", "Context", "ABSTRACT", "Context:"]

# Analysis outputs
NUMERICAL_ANALYSIS_SUMMARY = "07_numerical_analysis_summary.txt"
PAPERS_PER_YEAR_PLOT = "08_papers_per_year.png"
DOCUMENT_IDENTIFIER_DISTRIBUTION_PLOT = "09_document_identifier_distribution.png"
SOURCE_DISTRIBUTION_PLOT = "10_source_distribution.png"

# Year range for analysis
START_YEAR = 2010
END_YEAR = 2023

# =========================
# Three-stage search queries
# =========================


# Stage 1 — Broad HRI and CRI
STAGE1 = (
    '((Human-Robot OR Human Robot OR Human-robot Interaction OR Human robot Interaction OR HRI OR '
    'Child Robot OR Child-Robot OR Child-robot Interaction OR Child robot Interaction OR CRI OR Interact*) AND '
    '(Robot* OR Robotics) AND '
    '(User* OR Human* OR Person* OR People OR Child* OR Infant* OR Adult* OR Elderly OR Toddler* OR Preschool* OR School* OR Classroom OR Caregiver* OR Parent* OR Family OR Pediatric* ) AND '
    '(Social* OR Communicat* OR Dialogue OR Speech OR Languag* OR Talker OR Convers* OR Play OR Engagement OR Emotion* OR Cognit* OR Joint Attention OR Autism OR Neurodivergent OR Development* OR Interaction* OR Support OR Therapy OR Assistive OR Companion OR Service OR Healthcare OR Educat* OR Learn* OR Teach* OR Child-Directed OR vocaliz* OR vocabular*))'
)

# Stage 2 
STAGE2 = (
    '((Child Robot OR Child-Robot OR Child-robot Interaction OR Child robot Interaction OR CRI OR Interact*) AND '
    '(Robot* OR Robotics) AND '
    '(User* OR Adult* OR Child* OR Infant* OR Toddler* OR Preschool* OR School* OR Classroom OR Caregiver* OR Parent* OR Family OR Pediatric* ) AND '
    '(Social* OR Communicat* OR Dialogue OR Speech OR Languag* OR Talker OR Play OR Engagement OR Emotion* OR Cognit* OR Joint Attention OR Development* OR Interaction* OR Support OR Assistive OR  Educat* OR Learn* OR Teach* OR Child-Directed OR vocaliz* OR vocabular*))'
)


# # Stage 3 — Specific
STAGE3 = (
    '((Child Robot OR Child-Robot OR Child-robot Interaction OR Child robot Interaction OR CRI OR Interact*) AND '
    '(Robot* OR Robotics) AND '
    '(Child* OR Infant* OR Toddler* OR Caregiver* OR Parent*) AND '
    '(Social* OR Communicat* OR Dialogue OR Speech OR Languag* OR Talker OR Play OR Engagement OR Emotion* OR Cognit* OR Joint Attention OR Development* OR Interaction* OR Support OR Assistive OR  Educat* OR Learn* OR Teach* OR Child-Directed OR vocaliz* OR vocabular*))'
)



# Bundle for convenience (optional)
SEARCH_STAGES = {
    "Stage 1 – Broad Search": STAGE1,
    "Stage 2 – Narrow Search": STAGE2,
    "Stage 3 – Specific Search": STAGE3,
}


# # Classification queries
# CLASSIFICATION_QUERIES = [
#     {"REVIEW": "((Review Paper OR Systematic Review OR State of the Art OR Survey OR Meta-Analysis OR Theoretical Framework OR Comprehensive Study OR Bibliometric Analysis OR Challenges OR Future Trends OR Scope Review))"},
#     {"CASE_STUDY": "((case study))"},
#     {"HRI": "((human-robot interaction OR hri OR human robot interaction OR human-robot OR human robot))"},
#     {"HCI": "((human-computer interaction OR hci OR human computer interaction OR human-computer OR human computer))"},
#     {"CRI": "((child-robot interaction OR cri OR child robot interaction OR child robot OR child-robot))"},
#     {"CRI": "((social robot* OR assistive robot OR social OR Robot*) AND (child*))"},
#     {"CRI": "((child* OR Infant* OR Interact*) AND (Robot*) AND (Educat* OR School* OR Learn* OR Caregiver OR Child-Directed OR Speech OR Languag* OR Communicat* OR Teach* OR Talker OR vocaliz* OR vocabulary))"},
#     {"SR": "((social robot* OR assistive robot OR social) NotAND (child*))"},
#     {"AUTISM": "((autis*))"},
#     {"Editorial": "((Editor*))"},
#     {"EDUCATION": "((robot* OR Child*) AND (educat* OR learning OR teaching OR classroom OR school* OR curriculum OR training)))"},
#     {"HEALTHCARE": "((robot*) AND (health* OR assistive OR therapy OR rehabilitation OR medical OR hospital)))"},
#     {"INDUSTRIAL": "((robot*) AND (manufactur* OR industry OR automation OR assembly OR robotic arm OR factory)))"},
#     {"ASSISTIVE_TECH": "((assistive technology OR assistive robot* OR accessibility OR disability OR rehabilitation))"},
#     {"SPEECH_PROCESSING": "((speech* OR vocaliz* OR voice OR linguistic OR talker OR phonetics OR communicat*))"},
#     {"ETHICS": "((ethic* OR moral* OR responsible AI OR bias OR fairness OR transparency OR accountability))"},
#     {"SOCIAL_IMPACT": "((robot*) AND (societal impact OR policy OR acceptance OR adoption OR integration OR trust)))"},
#     {"NEUROROBOTICS": "((neurorobot* OR cognitive robotics OR brain-inspired robotics OR neural network OR bio-inspired OR perception-action OR predictive coding))"},
#     {"AUGMENTED_REALITY": "((augmented reality OR AR OR virtual reality OR VR OR mixed reality OR XR OR immersive technology))"},
#     {"PERCEPTION": "((robot* AND (perception OR vision OR recognition OR sensory OR object detection OR image processing)))"},
#     {"EMOTION_RECOGNITION": "((emotion recognition OR affective computing OR sentiment analysis OR facial expression OR emotion AI OR mood detection))"},
#     {"AUTONOMOUS_SYSTEMS": "((autonomous system* OR self-driving OR navigation OR decision-making OR reinforcement learning OR planning))"},
#     {"SWARM_ROBOTICS": "((swarm robotics OR collective intelligence OR multi-robot* OR decentralized control OR distributed systems))"},
#     {"SECURITY_PRIVACY": "((robot* AND (cybersecurity OR privacy OR hacking OR data protection OR authentication OR encryption)))"},
#     {"EXOSKELETONS": "((exoskeleton* OR wearable robot* OR assistive mobility OR prosthetic OR rehabilitation robot*))"},
#     {"HUMAN_FACTORS": "((human factors OR usability OR user experience OR ergonomics OR cognitive load OR workload OR affordances))"},
#     {"MACHINE_LEARNING": "((machine learning OR deep learning OR artificial intelligence OR AI OR reinforcement learning OR neural networks))"},
#     {"SURGICAL_ROBOTICS": "((robot assisted surgery OR surgical robotics OR robotic surgery OR minimally invasive surgery OR orthopedic surgery OR neurosurgery OR reconstructive surgery OR colorectal surgery OR knee surgery OR total knee arthroplasty))"},
#     {"MEDICAL_EDUCATION": "((medical education OR surgical training OR simulation training OR healthcare training OR interprofessional education OR patient safety OR medical literature))"},
#     {"GERIATRIC_ROBOTICS": "((robot* AND (aging OR geriatric care OR elderly care OR nursing home OR patient transport OR assistive technology OR robotic caregivers)))"},
#     {"AGRICULTURAL_ROBOTICS": "((agriculture OR agricultural robot* OR autonomous farming OR precision farming OR smart agriculture OR fruit picker OR crop production))"},
#     {"TECHNOLOGY_IMPACT": "((technology AND (social impact OR political system OR government OR democracy OR legal aspect OR public opinion OR ethics)))"},
#     {"SOCIAL_MEDIA": "((robot* AND (social media OR web interaction OR online system OR mass communication OR human-computer interaction)))"},
#     {"USER_AUTONOMY": "((user autonomy OR human autonomy OR decision-making OR independence OR personalized AI OR self-learning systems))"},
#     {"METAVERSE_ROBOTICS": "((metaverse OR virtual reality OR augmented reality OR immersive technology OR 3D imaging OR digital twin OR simulation training))"}
# ]

# One consolidated CRI rule (union of your three CRI rules)
# CRI_QUERY = (
#     '('
#     ' ("child-robot interaction" OR "child robot interaction" OR "child-robot" OR "child robot" OR CRI)'
#     ' OR ( (social robot* OR "assistive robot" OR social OR robot*) AND child* )'
#     ' OR ( (child* OR infant* OR interact*) AND robot* AND '
#     '      (educat* OR school* OR learn* OR caregiver OR "child-directed" OR speech OR languag* '
#     '       OR communicat* OR teach* OR talker OR vocaliz* OR vocabulary) )'
#     ')'
# )


Sorting_Stage = [
    {"REVIEW": "((\"systematic review\" OR \"meta-analysis\" OR \"scoping review\" OR \"umbrella review\" OR \"rapid review\" "
            "OR \"literature review\" OR \"review article\" OR \"review of\" OR \"a review\" "
            "OR \"systematic mapping\" OR \"systematic mapping study\" OR \"mapping study\" "
            "OR \"bibliometric analysis\" OR \"literature survey\" OR \"survey of\" OR \"survey on\" "
            "OR \"state of the art\" OR \"state-of-the-art\"))"}, 
    {"CASE_STUDY": "((case study))"},
    {"HRI": "((human-robot interaction OR hri OR human robot interaction OR human-robot OR human robot))"},
    {"HCI": "((human-computer interaction OR hci OR human computer interaction OR human-computer OR human computer))"},

    # # ---- merged CRI (single label) ----
    # {"CRI": CRI_QUERY},

    {"SR": "((social robot* OR assistive robot OR social) ANDNOT (child*))"},
    {"AUTISM": "((autis*))"},
    {"Editorial": "((editor*))"},
    {"EDUCATION": "((robot* OR child*) AND (educat* OR learning OR teaching OR classroom OR school* OR curriculum OR training))"},
    {"HEALTHCARE": "((robot*) AND (health* OR assistive OR therapy OR rehabilitation OR medical OR hospital))"},
    {"INDUSTRIAL": "((robot*) AND (manufactur* OR industry OR automation OR assembly OR robotic arm OR factory))"},
    {"ASSISTIVE_TECH": "((assistive technology OR assistive robot* OR accessibility OR disability OR rehabilitation))"},
    {"SPEECH_PROCESSING": "((speech* OR vocaliz* OR voice OR linguistic OR talker OR phonetics OR communicat*))"},
    {"ETHICS": "((ethic* OR moral* OR responsible AI OR bias OR fairness OR transparency OR accountability))"},
    {"SOCIAL_IMPACT": "((robot*) AND (societal impact OR policy OR acceptance OR adoption OR integration OR trust))"},
    {"NEUROROBOTICS": "((neurorobot* OR cognitive robotics OR brain-inspired robotics OR neural network OR bio-inspired OR perception-action OR predictive coding))"},
    {"AUGMENTED_REALITY": "((augmented reality OR AR OR virtual reality OR VR OR mixed reality OR XR OR immersive technology))"},
    {"PERCEPTION": "((robot* AND (perception OR vision OR recognition OR sensory OR object detection OR image processing)))"},
    {"EMOTION_RECOGNITION": "((emotion recognition OR affective computing OR sentiment analysis OR facial expression OR emotion AI OR mood detection))"},
    {"AUTONOMOUS_SYSTEMS": "((autonomous system* OR self-driving OR navigation OR decision-making OR reinforcement learning OR planning))"},
    {"SWARM_ROBOTICS": "((swarm robotics OR collective intelligence OR multi-robot* OR decentralized control OR distributed systems))"},
    {"SECURITY_PRIVACY": "((robot* AND (cybersecurity OR privacy OR hacking OR data protection OR authentication OR encryption)))"},
    {"EXOSKELETONS": "((exoskeleton* OR wearable robot* OR assistive mobility OR prosthetic OR rehabilitation robot*))"},
    {"HUMAN_FACTORS": "((human factors OR usability OR user experience OR ergonomics OR cognitive load OR workload OR affordances))"},
    {"MACHINE_LEARNING": "((machine learning OR deep learning OR artificial intelligence OR AI OR reinforcement learning OR neural networks))"},
    {"SURGICAL_ROBOTICS": "((robot assisted surgery OR surgical robotics OR robotic surgery OR minimally invasive surgery OR orthopedic surgery OR neurosurgery OR reconstructive surgery OR colorectal surgery OR knee surgery OR total knee arthroplasty))"},
    {"MEDICAL_EDUCATION": "((medical education OR surgical training OR simulation training OR healthcare training OR interprofessional education OR patient safety OR medical literature))"},
    {"GERIATRIC_ROBOTICS": "((robot* AND (aging OR geriatric care OR elderly care OR nursing home OR patient transport OR assistive technology OR robotic caregivers)))"},
    {"AGRICULTURAL_ROBOTICS": "((agriculture OR agricultural robot* OR autonomous farming OR precision farming OR smart agriculture OR fruit picker OR crop production))"},
    {"TECHNOLOGY_IMPACT": "((technology AND (social impact OR political system OR government OR democracy OR legal aspect OR public opinion OR ethics)))"},
    {"SOCIAL_MEDIA": "((robot* AND (social media OR web interaction OR online system OR mass communication OR human-computer interaction)))"},
    {"USER_AUTONOMY": "((user autonomy OR human autonomy OR decision-making OR independence OR personalized AI OR self-learning systems))"},
    {"METAVERSE_ROBOTICS": "((metaverse OR virtual reality OR augmented reality OR immersive technology OR 3D imaging OR digital twin OR simulation training))"},
]
