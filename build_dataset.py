#!/usr/bin/env python3
"""
MKULTRA Benchmark - Training Dataset Builder

Extracts text from PDFs, EPUBs, TXTs in dataset/training/, fetches URLs from
dataset/targeted_links.txt (skipping shopping/EMF/gadget links), cleans text,
and produces properly batched JSONL training data.

Usage:
    python build_dataset.py
    python build_dataset.py --output-dir dataset/training_data
    python build_dataset.py --batch-size 20
"""

# Copyright (c) 2026 defnlnotme
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import re
import json
import zipfile
import glob
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

# URL fetching
try:
    import requests
except ImportError:
    requests = None
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# PDF & EPUB extraction
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
try:
    import pdfplumber
except ImportError:
    pdfplumber = None
try:
    import ebooklib
    from ebooklib import epub
    ITEM_DOCUMENT = ebooklib.ITEM_DOCUMENT
except ImportError:
    epub = None
    ITEM_DOCUMENT = 9

logger = logging.getLogger(__name__)

# URL filtering patterns - shopping, EMF gadgets, and unrelated tools
SHOPPING_PATTERNS = [
    r'aliexpress\.com',
    r'amazon\.com',
    r'etsy\.com',
    r'shopify\.com',
    r'ebay\.com',
    r'safespaceprotection\.com',
    r'saticshield\.com',
    r'greatscottgadgets\.com',
    r'lab401\.com',
    r'narda-sts\.com',
    r'ds2nano\.com',
    r'store\.',
    r'\.com/products',
    r'\.com/shop',
]

# Domains to completely skip
SKIP_DOMAINS = [
    'aliexpress.com',
    'amazon.com',
    'safespaceprotection.com',
    'saticshield.com',
    'greatscottgadgets.com',
    'lab401.com',
    'narda-sts.com',
    'ds2nano.com',
]

BATCH_SIZE = 20
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset', 'training_data')


def setup_logging() -> None:
    """Configure logging format and level."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def should_skip_url(url: str) -> bool:
    """Check if a URL should be skipped (shopping, EMF gadgets, etc.)."""
    url_lower = url.lower()
    for domain in SKIP_DOMAINS:
        if domain in url_lower:
            return True
    for pattern in SHOPPING_PATTERNS:
        if re.search(pattern, url_lower):
            return True
    return False


def clean_text(text: str) -> str:
    """Clean extracted text using regex."""
    if not text:
        return ""
    # Remove tactiq.io timestamps and navigation
    text = re.sub(r'\[tactiq\.io.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    # Remove navigation menus and footer content patterns
    text = re.sub(r'(Skip to content|Main navigation|Breadcrumb|Footer|Sidebar).*?(?=\n\n|\Z)', '', text, flags=re.DOTALL)
    # Remove timestamps
    text = re.sub(r'\(\d+:\d+\)\s*', '', text)
    # Remove page numbers
    text = re.sub(r'\bPage \d+\b', '', text)
    # Clean up again
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


def extract_pdf_text(filepath: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    try:
        if pdfplumber:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif PyPDF2:
            reader = PyPDF2.PdfReader(filepath)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        else:
            logger.error("No PDF library available (install PyPDF2 or pdfplumber)")
    except Exception as e:
        logger.error(f"Error reading PDF {filepath}: {e}")
    return text


def extract_epub_text(filepath: str) -> str:
    """Extract text from an EPUB file."""
    text = ""
    try:
        if epub:
            book = epub.read_epub(filepath)
            for item in book.get_items():
                if item.get_type() == ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text += soup.get_text() + "\n"
        else:
            logger.error("No EPUB library available (install ebooklib)")
    except Exception as e:
        logger.error(f"Error reading EPUB {filepath}: {e}")
    return text


def extract_txt_text(filepath: str) -> str:
    """Extract text from a TXT file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading TXT {filepath}: {e}")
        return ""


def extract_zip_text(filepath: str, base_source: str) -> List[Dict[str, Any]]:
    """Extract text from a ZIP file containing PDFs."""
    results = []
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            pdf_files = [f for f in z.namelist() if f.endswith('.pdf')]
            for pdf_file in pdf_files:
                try:
                    with z.open(pdf_file) as f:
                        text = f.read().decode('utf-8', errors='replace')
                        # Try to extract from PDF bytes
                        temp_path = f'/tmp/{os.path.basename(pdf_file)}'
                        with open(temp_path, 'wb') as tf:
                            tf.write(z.read(pdf_file))
                        pdf_text = extract_pdf_text(temp_path)
                        os.remove(temp_path)
                        if pdf_text:
                            doc_name = os.path.basename(pdf_file).replace('.pdf', '')
                            results.append({
                                'text': pdf_text,
                                'name': doc_name,
                                'source': f"{base_source}/{pdf_file}"
                            })
                except Exception as e:
                    logger.warning(f"Error extracting {pdf_file} from {filepath}: {e}")
    except Exception as e:
        logger.error(f"Error reading ZIP {filepath}: {e}")
    return results


def fetch_url_content(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch content from a URL."""
    if requests is None or BeautifulSoup is None:
        logger.error("requests or BeautifulSoup not available — install beautifulsoup4 and requests")
        return None
    if should_skip_url(url):
        logger.info(f"Skipping URL (shopping/gadget): {url}")
        return None
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; mkubench/1.0)'}
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Remove script and style elements
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()
        text = soup.get_text(separator='\n', strip=True)
        return clean_text(text)
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None


def fetch_youtube_transcript(url: str) -> Optional[str]:
    """Fetch YouTube video transcript."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        video_id = re.search(r'watch\?v=([^&]+)', url)
        if not video_id:
            return None
        transcript = YouTubeTranscriptApi.get_transcript(video_id.group(1))
        text = ' '.join([t['text'] for t in transcript])
        return clean_text(text) if text else None
    except Exception as e:
        logger.info(f"No transcript available for {url}: {e}")
        return None


def process_file(filepath: str, rel_path: str) -> Optional[Dict[str, Any]]:
    """Process a single file and extract text."""
    source = rel_path
    ext = os.path.splitext(filepath)[1].lower()

    text = ""
    title = ""
    doc_type = ""

    if ext == '.pdf':
        text = extract_pdf_text(filepath)
        doc_type = "pdf"
        title = os.path.basename(filepath).replace('.pdf', '')
    elif ext == '.epub':
        text = extract_epub_text(filepath)
        doc_type = "epub"
        title = os.path.basename(filepath).replace('.epub', '')
    elif ext == '.txt':
        text = extract_txt_text(filepath)
        doc_type = "txt"
        title = os.path.basename(filepath)
    elif ext == '.zip':
        zip_docs = extract_zip_text(filepath, rel_path)
        if not zip_docs:
            return None
        # Process the first document from the zip as the primary
        first = zip_docs[0]
        text = first['text']
        title = first['name']
        doc_type = "pdf"
        source = first['source']
        # Add remaining docs from zip as separate entries
        results = []
        for zd in zip_docs:
            results.append({
                'id': f"doc_{hash(zd['source']) & 0xFFFFFFFF:08d}",
                'title': zd['name'],
                'text': clean_text(zd['text']),
                'source': zd['source'],
                'type': 'pdf',
                'metadata': {'category': 'mkultra_benchmark', 'topic': 'mind_control_research'}
            })
        return results
    elif ext in ['.md', '.csv']:
        text = extract_txt_text(filepath)
        doc_type = ext.lstrip('.')
        title = os.path.basename(filepath)
    else:
        return None

    if not text or len(text) < 50:
        return None

    return {
        'id': f"doc_{hash(source) & 0xFFFFFFFF:08d}",
        'title': title[:200],
        'text': clean_text(text),
        'source': source,
        'type': doc_type,
        'metadata': {'category': 'mkultra_benchmark', 'topic': 'mind_control_research'}
    }


def load_targeted_links(links_path: str) -> List[str]:
    """Load URLs from targeted_links.txt."""
    urls = []
    if os.path.exists(links_path):
        with open(links_path, 'r') as f:
            for line in f:
                url = line.strip()
                if url and not url.startswith('#'):
                    urls.append(url)
    return urls


def build_dataset(
    training_dir: Optional[str] = None,
    links_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    batch_size: int = BATCH_SIZE,
    skip_urls: bool = False
) -> None:
    """Build the complete training dataset."""
    setup_logging()

    if training_dir is None:
        training_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset', 'training')
    if links_path is None:
        links_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset', 'targeted_links.txt')
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'batches'), exist_ok=True)

    documents = []

    # Process local training files
    logger.info(f"Processing files from {training_dir}...")
    for root, dirs, files in os.walk(training_dir):
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, training_dir)
            # Skip zip files here (they're handled separately)
            if filename.endswith('.zip'):
                continue
            logger.info(f"Processing: {rel_path}")
            try:
                result = process_file(filepath, rel_path)
                if isinstance(result, list):
                    documents.extend(result)
                elif result:
                    documents.append(result)
            except Exception as e:
                logger.error(f"Error processing {rel_path}: {e}")

    # Process targeted links
    logger.info(f"Processing URLs from {links_path}...")
    urls = load_targeted_links(links_path)
    fetched_count = 0
    for url in urls:
        if should_skip_url(url):
            logger.info(f"Skipping URL (filtered): {url}")
            continue
        if skip_urls:
            continue

        # Check if YouTube
        if 'youtube.com' in url or 'youtu.be' in url:
            text = fetch_youtube_transcript(url)
            if text:
                documents.append({
                    'id': f"doc_{hash(url) & 0xFFFFFFFF:08d}",
                    'title': f"YouTube: {url.split('v=')[-1][:50]}",
                    'text': text,
                    'source': url,
                    'type': 'youtube_transcript',
                    'metadata': {'category': 'mkultra_benchmark', 'topic': 'mind_control_research'}
                })
                fetched_count += 1
                logger.info(f"Fetched YouTube transcript: {url[:60]}")
            else:
                logger.info(f"No YouTube transcript for: {url[:60]}")
            continue

        # Skip if it's a shopping/gadget URL
        if should_skip_url(url):
            continue

        # Fetch web content
        text = fetch_url_content(url)
        if text and len(text) > 100:
            documents.append({
                'id': f"doc_{hash(url) & 0xFFFFFFFF:08d}",
                'title': f"Article: {url[:80]}",
                'text': text,
                'source': url,
                'type': 'article',
                'metadata': {'category': 'mkultra_benchmark', 'topic': 'mind_control_research'}
            })
            fetched_count += 1
            logger.info(f"Fetched article: {url[:60]}")
        elif text:
            logger.info(f"Content too short for: {url[:60]}")

    logger.info(f"Total documents: {len(documents)} (fetched {fetched_count} URLs)")

    # Remove documents with very short content
    documents = [d for d in documents if len(d['text']) > 50]

    # Sort by title for consistency
    documents.sort(key=lambda d: d['title'].lower())

    # Assign new IDs
    for i, doc in enumerate(documents):
        doc['id'] = f"doc_{i:08d}"

    # Create training_dataset.jsonl
    dataset_path = os.path.join(output_dir, 'training_dataset.jsonl')
    with open(dataset_path, 'w') as f:
        for doc in documents:
            f.write(json.dumps(doc) + '\n')
    logger.info(f"Wrote {len(documents)} documents to {dataset_path}")

    # Create batches
    batches_dir = os.path.join(output_dir, 'batches')
    num_batches = (len(documents) + batch_size - 1) // batch_size
    for batch_idx in range(num_batches):
        start = batch_idx * batch_size
        end = min(start + batch_size, len(documents))
        batch_docs = documents[start:end]
        batch_path = os.path.join(batches_dir, f'batch_{batch_idx + 1:03d}.jsonl')
        with open(batch_path, 'w') as f:
            for doc in batch_docs:
                f.write(json.dumps(doc) + '\n')
        logger.info(f"Wrote batch {batch_idx + 1}/{num_batches} ({len(batch_docs)} docs)")

    # Create dataset summary
    file_count = sum(1 for f in os.listdir(training_dir) if os.path.isfile(os.path.join(training_dir, f)))
    summary = {
        "total_documents": len(documents),
        "files": file_count,
        "urls": fetched_count,
        "types": {},
        "batch_size": batch_size,
        "num_batches": num_batches
    }
    for doc in documents:
        t = doc['type']
        summary['types'][t] = summary['types'].get(t, 0) + 1

    summary_path = os.path.join(output_dir, 'dataset_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    logger.info(f"Dataset summary written to {summary_path}")

    return documents, summary


def main() -> None:
    """Build the MKULTRA training dataset."""
    import argparse
    parser = argparse.ArgumentParser(description="Build MKULTRA training dataset")
    parser.add_argument("--training-dir", default=None, help="Path to training files")
    parser.add_argument("--links-path", default=None, help="Path to targeted_links.txt")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Documents per batch")
    parser.add_argument("--skip-urls", action="store_true", help="Skip URL fetching (rebuild only from local files)")
    args = parser.parse_args()

    build_dataset(
        training_dir=args.training_dir,
        links_path=args.links_path,
        output_dir=args.output_dir,
        batch_size=args.batch_size,
        skip_urls=args.skip_urls
    )


if __name__ == "__main__":
    main()
