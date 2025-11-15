
<img width="1920" height="1080" alt="antm" src="https://github.com/user-attachments/assets/ebadc9fe-b383-4df7-a319-52ca88631c70" />

# Hackathon Starter Kit

Build systems that can extract, transform, and reason over complex retail data.

> **All official questions, submissions, and leaderboard access live at [hack.theoryvc.com](https://hack.theoryvc.com).**
> ⚠️ **You must sign in with the exact email you used to register via Luma—other accounts will not be recognized.**


---

## The Challenge

We all have our favorite frameworks and "hobby horses." Are you convinced that DSPy, LangGraph, or LlamaIndex is the true secret sauce? Do you believe that running 10 agents in parallel is the key to productivity? It's time to find out.

**The challenge:** Reliably extract, transform, and reason over complex, messy, and diverse data that simulates real enterprise environments.

You'll work with:
- Structured data (Tables in Parquet format)
- Unstructured data (PDFs with contracts, invoices, policies)  
- Logs (JSONL event streams)

**Your goal:** Answer business questions accurately and efficiently. Use whatever approach works.

**Competition Platform:** [hack.theoryvc.com](https://hack.theoryvc.com)
---

## Quick Start

### 1. Download the Dataset (REQUIRED FIRST STEP)

**Run this script to download the complete dataset from Cloud Storage:**

```bash
./download_dataset.sh
```

This script will:
- Create a Python virtual environment
- Install required packages (`google-cloud-storage`)
- Download all dataset files to `./dataset/`

**The dataset is NOT included in this Git repository.** You must run this script before proceeding.

### 2. Verify the Dataset

Check that the dataset downloaded correctly:

```bash
ls dataset/
```

You should see parquet files, logs, and PDFs

### 3. (Optional) Open the Tools Guide

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

### 5. (Optional) Use the MCP Server

Contestants have access to a pre-configured **MCP (Model Context Protocol) server** that provides direct access to the hackathon dataset via MotherDuck. This allows you to integrate the dataset directly into AI assistants (Claude, ChatGPT, etc.) or custom agents.

**MCP Server URL:** `https://antm-hack-example.fastmcp.app/mcp`

**Quick Setup:** Visit [https://antm-hack-example.fastmcp.app](https://antm-hack-example.fastmcp.app) for easy integration with OpenAI SDK, Codex CLI, Claude Desktop, Claude Code, Cursor, or Gemini CLI.

**Connectors:** If you visit the base URL (`https://antm-hack-example.fastmcp.app`) without the `/mcp` path, you'll see a list of connectors to make it easy to add the server to your custom agents or chat clients.

**Source Code:** The MCP server source code is available at [github.com/tdoehmen/mcp-server-motherduck-example](https://github.com/tdoehmen/mcp-server-motherduck-example) if you want to deploy your own instance or understand how it works.

**Features:**
- Execute SQL queries on the hackathon dataset
- List all tables in the database
- Access DuckDB SQL syntax reference
- Read-only access with query timeouts and result limits

> ✅ **Next step:** Head back to [hack.theoryvc.com](https://hack.theoryvc.com) for the live question set, submission portal, and leaderboard. This repo just gives you the local tooling—the competition itself runs entirely on the platform.

---

## Repository Contents

```
modeler-hackathon-starter/
├── README.md                      # This file
├── download_dataset.sh            # Script to download dataset (RUN THIS FIRST!)
├── sample_submission.csv          # Template for your answers
├── example/                       # Self-contained setup + notebook
│   ├── SETUP.md                   # Detailed installation instructions
│   ├── requirements.txt           # Minimal deps for the quick example
│   └── tools_guide.ipynb          # Getting started with the tools
│
├── dataset/                       # Downloaded dataset (created by script)
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

## Important Links

- **Competition Platform:** [hack.theoryvc.com](https://hack.theoryvc.com)
- **OpenRouter (AI Models):** [openrouter.ai](https://openrouter.ai)
- **MCP Server:** [fastmcp.cloud/app/antm-hack-example](https://fastmcp.cloud/app/antm-hack-example) | [Source Code](https://github.com/tdoehmen/mcp-server-motherduck-example)
- **This Repo:** [github.com/TheoryVentures/modeler-hackathon-starter](https://github.com/TheoryVentures/modeler-hackathon-starter)

---

## Competition Structure

### Rounds Overview

**Training Round** (12:30 PM - 3:00 PM)
- Questions with answers provided
- Practice understanding the dataset
- Test your approach
- No submission required

**Round 1** (3:00 PM - 4:15 PM)
- Questions without answers
- Submit your answers via the platform
- Real-time leaderboard

**Round 2** (4:15 PM - 5:30 PM)
- Questions without answers
- Submit your answers via the platform
- Real-time leaderboard

**Round 3** (5:30 PM - 6:00 PM)
- Questions without answers
- Submit your answers via the platform
- Real-time leaderboard
- Determines final rankings

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
