#!/usr/bin/env python3
"""
PDF Parser Script
Extracts main body text (as markdown), numerical tables, and images from PDF files.
"""

import argparse
import os
import sys
from pathlib import Path
import fitz  # PyMuPDF
import pdfplumber
from typing import List, Dict, Tuple
import re


class PDFParser:
    """Parse PDF files and extract text, tables, and images."""
    
    def __init__(self, pdf_path: str, output_dir: str = None):
        """
        Initialize the PDF parser.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save extracted images (default: current directory)
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create images subdirectory
        self.images_dir = self.output_dir / f"{self.pdf_path.stem}_images"
        self.images_dir.mkdir(exist_ok=True)
        
        self.doc = fitz.open(str(self.pdf_path))
        self.text_content = []
        self.tables = []
        self.images = []
    
    def extract_text(self) -> str:
        """Extract main body text and convert to markdown format."""
        markdown_text = []
        
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text("text")
            
            if text.strip():
                # Add page break for multi-page documents
                if page_num > 0:
                    markdown_text.append("\n---\n")
                
                # Convert to markdown format
                # Preserve paragraphs
                paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
                
                for para in paragraphs:
                    # Check if it's a heading (all caps or short line)
                    lines = para.split('\n')
                    if len(lines) == 1 and (len(para) < 100 and para.isupper()):
                        markdown_text.append(f"## {para}\n")
                    else:
                        # Regular paragraph
                        formatted_para = para.replace('\n', ' ')
                        markdown_text.append(f"{formatted_para}\n\n")
        
        return ''.join(markdown_text)
    
    def extract_tables(self) -> List[Dict]:
        """Extract tables from PDF using pdfplumber."""
        all_tables = []
        
        with pdfplumber.open(str(self.pdf_path)) as pdf:
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                
                for table_num, table in enumerate(tables):
                    if table and len(table) > 0:
                        # Clean up table data
                        cleaned_table = []
                        for row in table:
                            cleaned_row = [str(cell).strip() if cell else "" for cell in row]
                            cleaned_table.append(cleaned_row)
                        
                        all_tables.append({
                            'page': page_num + 1,
                            'table_num': table_num + 1,
                            'data': cleaned_table
                        })
        
        return all_tables
    
    def tables_to_markdown(self, tables: List[Dict]) -> str:
        """Convert extracted tables to markdown format."""
        markdown_tables = []
        
        for table_info in tables:
            table = table_info['data']
            if not table or len(table) < 1:
                continue
            
            markdown_tables.append(f"\n### Table {table_info['table_num']} (Page {table_info['page']})\n\n")
            
            # Use first row as header
            header = table[0]
            markdown_tables.append("| " + " | ".join(header) + " |\n")
            markdown_tables.append("| " + " | ".join(["---"] * len(header)) + " |\n")
            
            # Add data rows
            for row in table[1:]:
                # Pad row if necessary
                while len(row) < len(header):
                    row.append("")
                # Truncate if too long
                row = row[:len(header)]
                markdown_tables.append("| " + " | ".join(row) + " |\n")
            
            markdown_tables.append("\n")
        
        return ''.join(markdown_tables)
    
    def extract_images(self) -> List[Dict]:
        """Extract images from PDF."""
        image_list = []
        image_counter = 0
        
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            image_list_page = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list_page):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_counter += 1
                image_filename = f"image_{image_counter:03d}.{image_ext}"
                image_path = self.images_dir / image_filename
                
                # Save image
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                image_list.append({
                    'page': page_num + 1,
                    'filename': image_filename,
                    'path': str(image_path),
                    'width': base_image.get('width', 0),
                    'height': base_image.get('height', 0)
                })
        
        return image_list
    
    def images_to_markdown(self, images: List[Dict]) -> str:
        """Convert extracted images to markdown format."""
        markdown_images = []
        
        if not images:
            return ""
        
        markdown_images.append("\n## Images\n\n")
        
        for img in images:
            relative_path = os.path.relpath(img['path'], self.output_dir)
            markdown_images.append(
                f"![Image {img['filename']}]({relative_path})  \n"
                f"*Page {img['page']}, {img['width']}x{img['height']} pixels*\n\n"
            )
        
        return ''.join(markdown_images)
    
    def parse(self) -> str:
        """Parse the entire PDF and return markdown output."""
        print(f"Parsing PDF: {self.pdf_path.name}")
        
        # Extract text
        print("Extracting text...")
        text_md = self.extract_text()
        
        # Extract tables
        print("Extracting tables...")
        tables = self.extract_tables()
        tables_md = self.tables_to_markdown(tables)
        print(f"Found {len(tables)} table(s)")
        
        # Extract images
        print("Extracting images...")
        images = self.extract_images()
        images_md = self.images_to_markdown(images)
        print(f"Found {len(images)} image(s)")
        
        # Combine all content
        markdown_output = []
        markdown_output.append(f"# PDF Content: {self.pdf_path.name}\n\n")
        markdown_output.append("## Main Text\n\n")
        markdown_output.append(text_md)
        
        if tables_md:
            markdown_output.append("\n## Tables\n")
            markdown_output.append(tables_md)
        
        if images_md:
            markdown_output.append(images_md)
        
        return ''.join(markdown_output)
    
    def save_output(self, markdown_content: str, output_file: str = None):
        """Save the markdown output to a file."""
        if output_file is None:
            output_file = self.output_dir / f"{self.pdf_path.stem}_parsed.md"
        else:
            output_file = Path(output_file)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"\nOutput saved to: {output_file}")
        print(f"Images saved to: {self.images_dir}")
    
    def close(self):
        """Close the PDF document."""
        self.doc.close()


def main():
    """Main function to run the PDF parser."""
    parser = argparse.ArgumentParser(
        description="Parse PDF files and extract text (markdown), tables, and images"
    )
    parser.add_argument(
        "pdf_file",
        type=str,
        help="Path to the PDF file to parse"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output markdown file path (default: <pdf_name>_parsed.md)"
    )
    parser.add_argument(
        "-d", "--output-dir",
        type=str,
        default=None,
        help="Output directory for images and markdown (default: current working directory)"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize parser
        pdf_parser = PDFParser(args.pdf_file, args.output_dir)
        
        # Parse PDF
        markdown_content = pdf_parser.parse()
        
        # Save output
        pdf_parser.save_output(markdown_content, args.output)
        
        # Close document
        pdf_parser.close()
        
        print("\n✓ PDF parsing completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

