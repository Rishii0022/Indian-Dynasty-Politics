# Dynasty Politics in India (Data Analysis Project)

## Overview
Analysis of dynasty politics in Indian democracy using automated web scraping, Azure OpenAI API keys, and Tableau visualization. This project maps elected representatives from state and national elections to identify dynastic political patterns across India.

## Problem Statement
India faces a paradox: the world's largest democracy exhibits high rates of dynasty politics. Representatives are often elected based on family lineage rather than qualifications.

## Tableau Dashboard Link
https://public.tableau.com/app/profile/rishi0022/viz/IndianDynastyPolitics/DynastyRateOverYears

---

## Project Components

### 1. Web Scraping
**Location:** `Web scraping code/`

- **AC Elections:** State Assembly elections (VidhanSabha) winning candidates
- **PC Elections:** National elections (LokSabha) winning candidates
- **Tools:** Selenium, BeautifulSoup, Requests, Pandas

**Key Scripts:**
- `Web scraping for AC elections/` - State-level election data of winning candidate details
- `Web scraping for PC elections/` - National-level election data of winning candidate details

### 2. Dynasty Identification through AI 
**Location:** `Multithreading Azure OpenAI/`, `SINGLE PROMPT API key/`

**Process:**
- Prompts through OpenAI/Azure OpenAI API keys
- Pydantic models for response validation (Unstructured to Structured language)
- Grounding through URLs

**Key Scripts:**
- `StructuredOutputSyncAC.py` / `StructuredOutputSyncPC.py` - Assembly/Parliament processing
- `batch_promptsAC_template.py` / `batch_promptsPC_template.py` - Batch prompt generation
- `multiAC_split.py` / `multiPC_combined.py` - Multi-key execution

### 3. Data Processing & Organization
**Location:** `Creating and Parsing Files/`, `Tables and UID keys/`

**Outputs:**
- Dynasty identification tables (family members, sources)
- Source verification tables
- Unique identifier mappings

**Key Scripts:**
- `jsondumpsCOMBINED.py` / `jsondumpsSINGLE_parser.py` - JSON parsing
- `UIDcreatorSplitAC.py` / `UIDcreatorCombinedPC.py` - UID generation

## Data Structure

### Input Data
```
Data/
├── Final parsed tables/
│   ├── family tables(AC recent)/        # AC family data
│   ├── Family tables(PC ALL)/           # PC family data
│   ├── Sources tables(AC recent)/       # AC sources
│   └── Sources tables(PC ALL)/          # PC sources
├── log tables data/                     # Processing logs
└── prompt errors/                       # API error tracking
```

### Processed Data
```
ACPC_json_dumps/
├── outputAC_jsonl_batch/                # AC elections API responses
└── outputPC_jsonl_batch/                # National elections API responses
```

---

## Technology Stack

- **Web Scraping:** Selenium, BeautifulSoup, Requests
- **Data Processing:** Pandas, Python
- **AI/ML:** OpenAI API, Azure OpenAI, Pydantic
- **Visualization:** Tableau

---

## Setup

### 1. Environment Variables:
Create `.env` file with API keys:
```
AZURE_OPENAI_API_KEY=your_key
OPENAI_API_KEY=your_key
```

### 2. Dependencies:
```bash
pip install pandas selenium beautifulsoup4 requests openai pydantic python-dotenv
```

---

## References

### API Keys Documentation
- [OpenAI Documentation](Docs/REFERENCES.md#1-openai-documentation)
- [Azure OpenAI Documentation](Docs/REFERENCES.md#2-azure-openai-documentation)
- [AI Related Articles](Docs/REFERENCES.md#3-ai-related-articles)
- [Research Papers](Docs/REFERENCES.md#4-research-papers)
- [Sources](Docs/REFERENCES.md#5-web-scraping-sources)

### Project Overview (Docs Folder)
- [API Keys Usage](Docs/API%20Keys.md)
- [Project High Level Overview](Docs/Data%20Creation%20Walkthrough.md)
- [Project Walkthrough](Docs/Project%20Rough%20Overview.md)


---

## Repository Structure
```
.
├── ACPC_json_dumps/              # API response dumps
├── Batch api calls/              # Batch API utilities
├── Creating and Parsing Files/   # Data transformation scripts
├── Data/                         # Processed datasets
├── ENV endpoints/                # Environment configuration
├── Multithreading Azure OpenAI/  # Multi-threaded AI processing
├── SINGLE PROMPT API key/        # Single-prompt API tests
├── Tables and UID keys/          # UID and table generation
├── Test files/                   # Test data and scripts
├── Web scraping code/            # Data collection scripts
├── .env                          # Environment variables (not tracked)
├── .gitignore
└── README.md
```
