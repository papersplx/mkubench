#!/usr/bin/env python3
"""
Validate benchmark result JSON files against expected schema.

Usage:
    python validate_results.py

This script validates that all result JSON files in results/all_models_benchmarks/
conform to the expected schema, checking for:
- Required fields (model, provider, results array)
- Correct data types
- Valid question IDs matching the dataset
- Valid accuracy ranges (0-100)
"""

import json
import glob
import os
import sys

DATASET_PATH = "dataset/mkultra_benchmark.jsonl"
RESULTS_DIR = "results/all_models_benchmarks"


def load_dataset(path):
    """Load benchmark dataset from JSONL file."""
    questions = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                questions.append(json.loads(line))
    return questions


def validate_result_file(filepath, dataset_question_ids):
    """Validate a single result file. Returns list of errors."""
    errors = []
    warnings = []
    filename = os.path.basename(filepath)
    
    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            return [f"Invalid JSON: {e}"], warnings
    
    # Check required top-level fields
    required_fields = ["model", "provider"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")
    
    # Results array is optional (legacy files may not have it)
    has_results = "results" in data and isinstance(data.get("results"), list)
    
    if not has_results:
        warnings.append("No 'results' array (legacy format)")
    
    if not has_results:
        # Validate summary-only format
        if "overall_accuracy" in data:
            acc = data["overall_accuracy"]
            if not isinstance(acc, (int, float)) or acc < 0 or acc > 100:
                errors.append(f"Invalid overall_accuracy: {acc}")
        return errors, warnings
    
    if has_results:
        # Validate each result entry
        for i, result in enumerate(data["results"]):
            # Check required result fields
            if "id" not in result:
                errors.append(f"Result {i}: missing 'id' field")
            elif result["id"] not in dataset_question_ids:
                errors.append(f"Result {i}: invalid question id {result['id']}")
            
            if "is_correct" not in result:
                errors.append(f"Result {i}: missing 'is_correct' field")
            elif not isinstance(result["is_correct"], bool):
                errors.append(f"Result {i}: 'is_correct' must be boolean")
            
            if "weight" not in result:
                errors.append(f"Result {i}: missing 'weight' field")
            elif not isinstance(result["weight"], (int, float)):
                errors.append(f"Result {i}: 'weight' must be numeric")
    
    # Validate accuracy fields
    if "overall_accuracy" in data:
        acc = data["overall_accuracy"]
        if not isinstance(acc, (int, float)) or acc < 0 or acc > 100:
            errors.append(f"Invalid overall_accuracy: {acc}")
    
    if "weighted_accuracy" in data:
        acc = data["weighted_accuracy"]
        if not isinstance(acc, (int, float)) or acc < 0 or acc > 100:
            errors.append(f"Invalid weighted_accuracy: {acc}")
    
    return errors, warnings


def validate_all_results():
    """Validate all result files and report status."""
    questions = load_dataset(DATASET_PATH)
    dataset_question_ids = set(q["id"] for q in questions)
    
    result_files = glob.glob(os.path.join(RESULTS_DIR, "*.json"))
    
    if not result_files:
        print("No result files found")
        return True
    
    all_valid = True
    total_errors = 0
    total_warnings = 0
    
    print(f"Validating {len(result_files)} result files...")
    print()
    
    for filepath in sorted(result_files):
        if "combined.json" in filepath:
            continue
        
        filename = os.path.basename(filepath)
        errors, warnings = validate_result_file(filepath, dataset_question_ids)
        
        if errors:
            all_valid = False
            total_errors += len(errors)
            print(f"FAIL: {filename}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK:   {filename}")
        
        if warnings:
            total_warnings += len(warnings)
            for warning in warnings:
                print(f"  ⚠ {warning}")
    
    print()
    if all_valid:
        print(f"All {len(result_files)} result files are valid!")
        if total_warnings:
            print(f"({total_warnings} warnings)")
        return True
    else:
        print(f"Found {total_errors} validation errors across {len(result_files)} files")
        return False


if __name__ == "__main__":
    success = validate_all_results()
    sys.exit(0 if success else 1)