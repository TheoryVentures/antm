#!/usr/bin/env python3
"""
Minimal example that chunks markdown content, embeds chunks with OpenAI,
stores them in LanceDB, and runs a sample similarity search.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional

import lancedb
import pandas as pd
from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-large"
DEFAULT_CHUNK_SIZE = 1200  # characters
DEFAULT_CHUNK_OVERLAP = 200
DEFAULT_MARKDOWN_PATH = Path(__file__).resolve().parent / "ProductCatalog_Fall_2023_parsed.md"
DEFAULT_DB_DIR = Path(__file__).resolve().parent / "lance_db"
DEFAULT_TABLE_NAME = "product_catalog_chunks"
DEFAULT_SEARCH_QUERY = "electronic bright red device"
DEFAULT_TOP_K = 5


def load_markdown(markdown_path: Path) -> str:
    if not markdown_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")
    return markdown_path.read_text(encoding="utf-8")


def chunk_markdown(
    markdown_text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> List[str]:
    """
    Chunk markdown while preferring paragraph boundaries and keeping limited overlap.
    Based on a straightforward "buffer of paragraphs" approach which works well for catalog data.
    """
    paragraphs = [p.strip() for p in markdown_text.split("\n\n") if p.strip()]
    if not paragraphs:
        return []

    chunks: List[str] = []
    buffer: List[str] = []
    buffer_len = 0

    for para in paragraphs:
        candidate_len = buffer_len + len(para) + (2 if buffer else 0)
        if candidate_len > chunk_size and buffer:
            chunks.append("\n\n".join(buffer))

            if overlap > 0:
                overlap_paragraphs: List[str] = []
                overlap_len = 0
                for prev_para in reversed(buffer):
                    overlap_paragraphs.insert(0, prev_para)
                    overlap_len += len(prev_para)
                    if overlap_len >= overlap:
                        break
                buffer = overlap_paragraphs
                buffer_len = sum(len(p) for p in buffer)
            else:
                buffer = []
                buffer_len = 0

        buffer.append(para)
        buffer_len += len(para) + 2

    if buffer:
        chunks.append("\n\n".join(buffer))

    return chunks


def infer_section_title(chunk_text: str) -> Optional[str]:
    """Return the first markdown heading found in the chunk, if any."""
    for line in chunk_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return None


def embed_chunks(chunks: List[str], model: str, batch_size: int = 64) -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)
    vectors: List[List[float]] = []

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        response = client.embeddings.create(model=model, input=batch)
        # Preserve ordering to align with chunk indices
        vectors.extend([item.embedding for item in sorted(response.data, key=lambda x: x.index)])

    return vectors


def records_from_chunks(chunks: List[str], embeddings: List[List[float]], source: Path) -> List[Dict]:
    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks and embeddings must match.")

    records: List[Dict] = []
    source_name = source.stem

    for idx, (chunk_text, vector) in enumerate(zip(chunks, embeddings)):
        records.append(
            {
                "id": f"{source_name}-{idx}",
                "source_path": str(source),
                "chunk_index": idx,
                "content": chunk_text,
                "section": infer_section_title(chunk_text),
                "vector": vector,
            }
        )

    return records


def load_into_lancedb(records: List[Dict], db_path: Path, table_name: str):
    if not records:
        raise ValueError("No records to load into LanceDB.")

    db_path.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(str(db_path))
    data = pd.DataFrame.from_records(records)

    if table_name in db.table_names():
        table = db.open_table(table_name)
        source_value = records[0]["source_path"].replace("'", "''")
        table.delete(f"source_path = '{source_value}'")
        table.add(data)
    else:
        db.create_table(table_name, data=data, mode="overwrite")


def search(
    query: str,
    db_path: Path,
    table_name: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
    top_k: int = 5,
) -> List[Dict]:
    """Run a vector similarity search over the product catalog table."""
    if not query or not query.strip():
        raise ValueError("Query text must be provided.")

    db = lancedb.connect(str(db_path))
    if table_name not in db.table_names():
        raise ValueError(f"Table '{table_name}' not found in LanceDB at {db_path}.")

    query_vector = embed_chunks([query], model=model, batch_size=1)[0]
    table = db.open_table(table_name)
    return table.search(query_vector).limit(top_k).to_pandas().to_dict("records")


def ingest_catalog(
    markdown_path: Path,
    db_path: Path,
    table_name: str,
    model: str,
    chunk_size: int,
    overlap: int,
):
    print(f"Loading markdown from {markdown_path}...")
    markdown_text = load_markdown(markdown_path)

    print(f"Chunking markdown (chunk_size={chunk_size}, overlap={overlap})...")
    chunks = chunk_markdown(markdown_text, chunk_size=chunk_size, overlap=overlap)
    if not chunks:
        raise ValueError("No chunks produced from markdown. Check the input file.")
    print(f"Created {len(chunks)} chunk(s).")

    print(f"Creating embeddings with model '{model}'...")
    embeddings = embed_chunks(chunks, model=model)

    print("Building LanceDB records...")
    records = records_from_chunks(chunks, embeddings, source=markdown_path)

    print(f"Writing {len(records)} record(s) to LanceDB at {db_path} (table: {table_name})...")
    load_into_lancedb(records, db_path=db_path, table_name=table_name)


def pretty_print_results(results: List[Dict]):
    if not results:
        print("No results found.")
        return

    for rank, row in enumerate(results, start=1):
        snippet = row["content"].replace("\n", " ")
        if len(snippet) > 500:
            snippet = snippet[:497] + "..."
        print(f"{rank}. chunk #{row['chunk_index']} (section: {row.get('section')}) -> {snippet}")


def main():
    markdown_path = DEFAULT_MARKDOWN_PATH
    db_path = DEFAULT_DB_DIR
    table_name = DEFAULT_TABLE_NAME

    # Comment out the ingest block below if the DB is already populated
    ingest_catalog(
        markdown_path=markdown_path,
        db_path=db_path,
        table_name=table_name,
        model=DEFAULT_EMBEDDING_MODEL,
        chunk_size=DEFAULT_CHUNK_SIZE,
        overlap=DEFAULT_CHUNK_OVERLAP,
    )
    print("✓ Ingest complete.")

    print(f"\nRunning sample search for: {DEFAULT_SEARCH_QUERY!r}")
    results = search(
        query=DEFAULT_SEARCH_QUERY,
        db_path=db_path,
        table_name=table_name,
        model=DEFAULT_EMBEDDING_MODEL,
        top_k=DEFAULT_TOP_K,
    )
    pretty_print_results(results)


if __name__ == "__main__":
    main()
