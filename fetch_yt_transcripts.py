#!/usr/bin/env python3
"""
MKULTRA Benchmark - YouTube Transcript Fetcher

Fetches transcripts from YouTube videos listed in dataset/targeted_links.txt.
Handles videos without captions gracefully and logs results.

Usage:
    python fetch_yt_transcripts.py
    python fetch_yt_transcripts.py --output transcripts/
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
import logging
from pathlib import Path

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import NoTranscriptFound, VideoUnavailable
except ImportError:
    print("Error: youtube-transcript-api not installed. Run: pip install youtube-transcript-api")
    exit(1)

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure logging format and level."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'watch\?v=([^&]+)',
        r'youtu\.be/([^?]+)',
        r'embed/([^/?]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_transcript(video_url: str, language: str = 'en') -> Optional[str]:
    """Fetch transcript for a YouTube video URL."""
    video_id = extract_video_id(video_url)
    if not video_id:
        logger.warning(f"Could not extract video ID from: {video_url}")
        return None

    try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=[language])
        text = ' '.join([t['text'] for t in transcript])
        return text.strip() if text else None
    except NoTranscriptFound:
        logger.info(f"No transcript found for video {video_id}")
        return None
    except VideoUnavailable:
        logger.info(f"Video unavailable: {video_id}")
        return None
    except Exception as e:
        logger.warning(f"Error fetching transcript for {video_id}: {e}")
        return None


def load_video_urls(links_path: str) -> list:
    """Load YouTube URLs from the targeted links file."""
    videos = []
    if not os.path.exists(links_path):
        return videos
    with open(links_path, 'r') as f:
        for line in f:
            url = line.strip()
            if url and ('youtube.com' in url or 'youtu.be' in url):
                videos.append(url)
    return videos


def main() -> None:
    """Fetch YouTube transcripts for benchmark videos."""
    import argparse
    parser = argparse.ArgumentParser(description="Fetch YouTube transcripts for MKULTRA benchmark")
    parser.add_argument("--links-path", default=None, help="Path to targeted_links.txt")
    parser.add_argument("--output", default="transcripts", help="Output directory")
    parser.add_argument("--language", default="en", help="Transcript language")
    args = parser.parse_args()

    setup_logging()

    if args.links_path is None:
        args.links_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset', 'targeted_links.txt')

    videos = load_video_urls(args.links_path)
    logger.info(f"Found {len(videos)} YouTube videos to process")

    os.makedirs(args.output, exist_ok=True)
    results = []
    success_count = 0

    for url in videos:
        logger.info(f"Processing: {url[:80]}")
        transcript = fetch_transcript(url, args.language)
        if transcript:
            video_id = extract_video_id(url) or url
            output_path = os.path.join(args.output, f"{video_id}.txt")
            with open(output_path, 'w') as f:
                f.write(transcript)
            success_count += 1
            results.append({"url": url, "status": "success", "video_id": video_id})
            logger.info(f"  Success: {output_path}")
        else:
            results.append({"url": url, "status": "no_transcript"})
            logger.info(f"  No transcript available")

    # Save summary
    summary = {
        "total_videos": len(videos),
        "successful": success_count,
        "no_transcript": len(videos) - success_count,
        "results": results
    }
    summary_path = os.path.join(args.output, 'transcript_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    logger.info(f"Summary saved to {summary_path}: {success_count}/{len(videos)} transcripts fetched")


if __name__ == "__main__":
    main()
