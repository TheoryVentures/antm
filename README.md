
<img width="1920" height="1080" alt="antm" src="https://github.com/user-attachments/assets/ebadc9fe-b383-4df7-a319-52ca88631c70" />

# Hackathon Starter Kit

Build systems that can extract, transform, and reason over complex retail data.

**Competition Platform:** [hack.theoryvc.com](https://hack.theoryvc.com)

---

## The Challenge

We all have our favorite frameworks and "hobby horses." Are you convinced that DSPy, LangGraph, or LlamaIndex is the true secret sauce? Do you believe that running 10 agents in parallel is the key to productivity? It's time to find out.

**The challenge:** Reliably extract, transform, and reason over complex, messy, and diverse data that simulates real enterprise environments.

You'll work with:
- Structured data (24 database tables in Parquet format)
- Unstructured data (PDFs with contracts, invoices, policies)  
- Logs (JSONL event streams)

**Your goal:** Answer business questions accurately and efficiently. Use whatever approach works.

---

## Competition Structure

### Three Rounds

**Round 1: Training Round** (12:30 PM - 2:00 PM)
- 25 questions with answers provided
- Practice understanding the dataset
- Test your approach
- No submission required

**Round 2: Test Round** (2:00 PM - 5:00 PM)
- 30 questions without answers
- Submit your answers via the platform
- Real-time leaderboard
- This is the main competition

**Round 3: Holdout Evaluation** (After 6:00 PM)
- 20 secret questions run against your system
- Prevents overfitting
- Determines final rankings
- Winners announced at 7:30 PM

### Scoring
- **Test Round:** 70% of final score
- **Holdout Round:** 30% of final score
- **Criteria:** Correctness (50%), Efficiency (25%), Explanation (25%)

---

## Repository Contents

```
modeler-hackathon-starter/
├── README.md                      # This file
├── sample_submission.csv          # Template for your answers
├── example/                       # Self-contained setup + notebook
│   ├── SETUP.md                   # Detailed installation instructions
│   ├── requirements.txt           # Minimal deps for the quick example
│   └── tools_guide.ipynb          # Getting started with the tools
│
├── dataset/                       # Full retail dataset (parquet/logs/pdfs)
│   ├── parquet/                   # 24 dimension and fact tables
│   ├── logs/                      # 19 log files (JSONL)
│   └── pdfs/                      # Contracts, policies, invoices
│
└── training_evals/                # 25 practice questions with answers
    ├── README.md
    ├── question_01.md
    └── ... (25 total)
```

---

## Quick Start

### 1. Install Dependencies

**Recommended:** Use a virtual environment to avoid common issues (especially on macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r example/requirements.txt
python -m ipykernel install --user --name "modeler-starter" --display-name "Python 3 (Modeler Starter)"
```

**Alternative:** System-wide installation (may fail on macOS):
```bash
pip install -r example/requirements.txt
```

See [`example/SETUP.md`](example/SETUP.md) for detailed instructions and troubleshooting.

### 2. Inspect the Dataset

All required files ship inside this repo under `dataset/`:

```bash
ls dataset
```

You'll use these Parquet tables, logs, and PDFs directly in the notebook—no extra generation steps needed.

### 3. Open the Tools Guide

```bash
jupyter notebook example/tools_guide.ipynb
```

This notebook demonstrates:
- Loading and querying data with DuckDB
- Searching logs and PDFs with LanceDB
- Understanding the question format
- Creating your submission file

### 4. (Optional) Set Up OpenRouter for AI Models

OpenRouter provides access to Claude, GPT-4, Gemini, and other models through one API.

Get your API key: [openrouter.ai/keys](https://openrouter.ai/keys)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_KEY"
)

response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[
        {"role": "user", "content": "Write a SQL query to get the first 5 rows from a table"}
    ]
)

print(response.choices[0].message.content)
```
---

## Understanding the Data

### Three Types of Data

**1. Structured Data (Parquet Files)**
- 24 tables: customers, sales, items, stores, etc.
- Query with DuckDB (fast SQL on Parquet)
- Example questions: Aggregations, joins, time-series analysis

**2. Unstructured Data (PDFs)**
- Contracts, policies, invoices
- Extract with PDF parsers or LanceDB (semantic search)
- Example questions: Extract costs, dates, terms

**3. Logs (JSONL Files)**
- Clickstreams, experiments, events
- Parse with pandas, DuckDB, or LanceDB
- Example questions: Count events, analyze patterns, correlations

### Tool Selection

| Tool | Use For | Example |
|------|---------|---------|
| **DuckDB** | Tabular data, SQL queries | Aggregations, joins, filters |
| **LanceDB** | Logs, PDFs, semantic search | Finding events, extracting text |
| **Both** | Complex multi-source queries | Combining PDFs + logs + tables |

---

## Submission Format

Submissions must follow the leaderboard schema:

```csv
index,a1,a2,a3,a4,a5
0,9104725,TRUE,42.1875,vpm2k6zqf,Avery
```

**Key Points:**
- `index` starts at 0 and increments with each question.
- `a1`–`a5` correspond to the five answer slots per question (numeric, boolean, float, string, string).
- Fill unused slots with an empty string if a question requires fewer answers.

See `sample_submission.csv` for the up-to-date template.

---

## Strategy Tips

### Recommendations
- Start with training evals - they include answers
- Use the tools notebook to learn DuckDB and LanceDB
- Explore different approaches and find what works
- Test your system on various question types

### Common Pitfalls
- Hardcoding answers (holdout eval will catch this)
- Skipping logs/PDFs (many questions require them)
- Waiting until the last minute

### Time Management
- **12:30-1:30 PM:** Training round - explore the data
- **1:30-2:30 PM:** Build your approach/system
- **2:30-5:00 PM:** Answer test questions
- **5:00-6:00 PM:** Final checks and submit

---

## Important Links

- **Competition Platform:** [hack.theoryvc.com](https://hack.theoryvc.com)
- **OpenRouter (AI Models):** [openrouter.ai](https://openrouter.ai)
- **This Repo:** [github.com/TheoryVentures/modeler-hackathon-starter](https://github.com/TheoryVentures/modeler-hackathon-starter)

---

## Getting Help

**During the Event:**
- Technical issues: Ask event staff
- Data questions: Check `data/README.md`
- Platform issues: Contact judges

---

## Timeline
 
**10:00 AM – 11:00 AM** - Check-In / Coffee & Breakfast  
**11:00 AM – 12:30 PM** - Opening Remarks & Interviews  
**12:30 PM** - Hacking Begins  
**1:00 PM** - Lunch  
**6:30 PM – 7:00 PM** - Winner Interviews  
**7:00 PM – 8:00 PM** - Dinner & Closing Remarks  

---

**May the best approach win.**

---

*Built by Theory Ventures*
