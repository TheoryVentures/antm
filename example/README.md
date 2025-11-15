# PDF Parser + LanceDB Demo

Two lightweight scripts show the full workflow from PDF → markdown → vector search.

## 1. `pdf_parser.py` — PDF → Markdown + Assets

Extracts from a PDF:
1. Main body text (markdown)
2. Tables (markdown tables)
3. Images (saved alongside)

### Install dependencies

```bash
pip install -r requirements.txt
```

### Basic usage

```bash
python pdf_parser.py <path_to_pdf_file>
```

Optional flags:
- `-o output.md` — explicit markdown path
- `-d /path/to/output` — specify output directory (defaults to current working directory)

### Output

- `<pdf_name>_parsed.md` — combined text + tables + image references
- `<pdf_name>_images/` — extracted images

---

## 2. `import_to_lancedb.py` — Markdown → LanceDB + Sample Search

This minimal example script:
1. Reads the parsed markdown (defaults to `ProductCatalog_Fall_2023_parsed.md`)
2. Chunks the content with light overlap
3. Embeds each chunk with OpenAI embeddings
4. Stores results in a LanceDB table (`lance_db/product_catalog_chunks`)
5. Runs a demo search query (`"electronic bright red device"`) and prints the top hits

### Run the demo

```bash
export OPENAI_API_KEY=...   # required for embeddings
python import_to_lancedb.py
```

Feel free to edit the constants at the top of the script to point at other markdown files, change chunk sizes, or try new queries.

## Next steps

- You can continue adding more product catalogs and their chunks to the given LanceDB table.
- Once you have multiple LanceDB tables with different kinds of PDF data populated, you can expose each search function as a tool to the FastMCP server.
- Agents can discover tools in various ways, so the key is to make the retrieval layer discoverable to them in some form.