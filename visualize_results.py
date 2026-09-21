#!/usr/bin/env python3
"""
Generate visualizations from leaderboard.json.

Usage:
    python visualize_results.py

This script generates:
1. A text-based histogram of weighted scores (printed to console)
2. An HTML file with an interactive bar chart (saved to results/score_distribution.html)
"""

import json
import os

LEADERBOARD_PATH = "leaderboard.json"
OUTPUT_HTML = "results/score_distribution.html"


def load_leaderboard():
    """Load leaderboard data from JSON file."""
    with open(LEADERBOARD_PATH, "r") as f:
        return json.load(f)


def print_histogram(leaderboard):
    """Print a text-based histogram of weighted scores."""
    # Filter to completed models only
    completed = [e for e in leaderboard if e["status"] == "complete"]
    completed.sort(key=lambda x: x["weighted_accuracy"], reverse=True)
    
    if not completed:
        print("No completed models to display")
        return
    
    print("=" * 70)
    print("BENCHMARK SCORE DISTRIBUTION (Weighted Accuracy)")
    print("=" * 70)
    print()
    
    max_bar_width = 40
    max_score = 100
    
    for entry in completed:
        model = entry["model"]
        score = entry["weighted_accuracy"]
        
        # Create bar
        bar_length = int(score / max_score * max_bar_width)
        bar = "█" * bar_length
        
        # Format model name (truncate if too long)
        display_name = model[:40].ljust(40)
        
        print(f"{display_name} {bar} {score}%")
    
    print()
    print("-" * 70)
    print("Scale: 0%  10%  20%  30%  40%  50%  60%  70%  80%  90% 100%")
    print("       ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────|")


def generate_html_chart(leaderboard):
    """Generate an HTML bar chart visualization."""
    completed = [e for e in leaderboard if e["status"] == "complete"]
    completed.sort(key=lambda x: x["weighted_accuracy"], reverse=True)
    
    if not completed:
        return
    
    # Generate HTML
    html_parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "    <title>mkubench Results</title>",
        "    <style>",
        "        body { font-family: monospace; margin: 40px; background: #1a1a2e; color: #eee; }",
        "        h1 { color: #e94560; }",
        "        .chart { margin: 20px 0; }",
        "        .bar-row { display: flex; align-items: center; margin: 4px 0; }",
        "        .model-name { width: 300px; text-align: right; padding-right: 10px; font-size: 12px; }",
        "        .bar-container { flex: 1; display: flex; align-items: center; }",
        "        .bar { height: 20px; background: linear-gradient(90deg, #e94560, #0f3460); border-radius: 3px; }",
        "        .score { margin-left: 10px; font-size: 12px; }",
        "        .summary { background: #16213e; padding: 20px; border-radius: 8px; margin: 20px 0; }",
        "        .summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }",
        "        .summary-item { text-align: center; }",
        "        .summary-value { font-size: 24px; color: #e94560; font-weight: bold; }",
        "        .summary-label { font-size: 12px; color: #888; }",
        "    </style>",
        "</head>",
        "<body>",
        "    <h1>mkubench Results</h1>",
        "",
        "    <div class='summary'>",
        "        <div class='summary-grid'>",
        f"            <div class='summary-item'><div class='summary-value'>{len(completed)}</div><div class='summary-label'>Models Tested</div></div>",
        f"            <div class='summary-item'><div class='summary-value'>{completed[0]['weighted_accuracy']}%</div><div class='summary-label'>Best Weighted Score</div></div>",
        f"            <div class='summary-item'><div class='summary-value'>{sum(e['weighted_accuracy'] for e in completed) / len(completed):.1f}%</div><div class='summary-label'>Average Weighted Score</div></div>",
        "        </div>",
        "    </div>",
        "",
        "    <div class='chart'>",
    ]
    
    # Add bars
    for entry in completed:
        model = entry["model"]
        score = entry["weighted_accuracy"]
        width = score * 4  # Scale to max 400px
        
        html_parts.append(f"        <div class='bar-row'>")
        html_parts.append(f"            <div class='model-name'>{model}</div>")
        html_parts.append(f"            <div class='bar-container'>")
        html_parts.append(f"                <div class='bar' style='width: {width}px;'></div>")
        html_parts.append(f"                <span class='score'>{score}%</span>")
        html_parts.append(f"            </div>")
        html_parts.append(f"        </div>")
    
    html_parts.extend([
        "    </div>",
        "",
        "</body>",
        "</html>",
    ])
    
    # Write HTML file
    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    with open(OUTPUT_HTML, "w") as f:
        f.write("\n".join(html_parts))
    
    print(f"HTML chart saved to {OUTPUT_HTML}")


def main():
    """Main function to generate visualizations."""
    if not os.path.exists(LEADERBOARD_PATH):
        print(f"Error: {LEADERBOARD_PATH} not found")
        print("Run 'python regenerate_leaderboard.py' first")
        return
    
    data = load_leaderboard()
    leaderboard = data["leaderboard"]
    
    print_histogram(leaderboard)
    print()
    generate_html_chart(leaderboard)


if __name__ == "__main__":
    main()