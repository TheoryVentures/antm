

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
├── tools_guide.ipynb              # Getting started with the tools
├── sample_submission.csv          # Template for your answers
│
├── data/                          # Dataset (download separately)
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
pip install -r requirements.txt
python -m ipykernel install --user --name "modeler-starter" --display-name "Python 3 (Modeler Starter)"
```

**Alternative:** System-wide installation (may fail on macOS):
```bash
pip install -r requirements.txt
```

See [SETUP.md](SETUP.md) for detailed instructions and troubleshooting.

### 2. Download the Dataset

```bash
# Download from the platform (500 MB compressed)
wget https://hack.theoryvc.com/dataset.zip
unzip dataset.zip -d data/
```

### 3. Open the Tools Guide

```bash
jupyter notebook tools_guide.ipynb
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

Your answers go in a CSV file with this format:

```csv
question_id,answer_type,answer_value,confidence,explanation
1,customer_sk,12345,high,"Found using aggregation query"
1,revenue,125000.50,high,"Calculated with SUM()"
2,category,Electronics,medium,"Identified from analysis"
```

**Key Points:**
- Multiple rows per question if it has multiple parts
- `confidence`: high | medium | low
- `explanation`: One sentence explaining your reasoning

See `sample_submission.csv` for the template.

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
- **Dataset Source:** [github.com/TheoryVentures/Retail-Universe](https://github.com/TheoryVentures/Retail-Universe)

---

## Getting Help

**During the Event:**
- Technical issues: Ask event staff
- Data questions: Check `data/README.md`
- Platform issues: Contact judges

---

## Timeline

**11:00 AM** - Doors open  
**11:30 AM** - Kickoff  
**12:00 PM** - Setup time  
**12:30 PM** - Round 1: Training (25 questions with answers)  
**2:00 PM** - Round 2: Test (30 questions, no answers)  
**6:00 PM** - Submissions due  
**6:00-7:30 PM** - Judging (Round 3: Holdout)  
**7:30 PM** - Winners announced  

---

## Final Checklist

Before Round 2:
- [ ] Completed at least 10 training questions
- [ ] Understand DuckDB basics
- [ ] Can parse logs with LanceDB or pandas
- [ ] Know how to fill out submission CSV
- [ ] Have your approach ready to test

During Round 2:
- [ ] Answer as many of 30 questions as possible
- [ ] Fill out `sample_submission.csv`
- [ ] Upload to platform before 6:00 PM

---

**May the best approach win.**

---

*Dataset powered by [Retail Universe](https://github.com/TheoryVentures/Retail-Universe)*  
*Built by Theory Ventures*
