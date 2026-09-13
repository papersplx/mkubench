#!/usr/bin/env python3
"""Tests for benchmark result JSON schema validation."""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validate_results import validate_result_file, load_dataset


class TestValidateResultFile(unittest.TestCase):
    """Tests for the validate_result_file function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.dataset_path = "dataset/mkultra_benchmark.jsonl"
        self.questions = load_dataset(self.dataset_path)
        self.dataset_question_ids = set(q["id"] for q in self.questions)
    
    def _create_temp_result(self, data):
        """Create a temporary result file and return its path."""
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        return path
    
    def test_valid_complete_result(self):
        """Test validation of a valid complete result file."""
        data = {
            "model": "test-model",
            "provider": "test-provider",
            "results": [
                {"id": 1, "is_correct": True, "weight": 0.1},
                {"id": 2, "is_correct": False, "weight": 0.1},
            ],
            "overall_accuracy": 50.0,
            "weighted_accuracy": 50.0,
        }
        path = self._create_temp_result(data)
        try:
            errors, warnings = validate_result_file(path, self.dataset_question_ids)
            self.assertEqual(errors, [])
        finally:
            os.unlink(path)
    
    def test_missing_model_field(self):
        """Test validation catches missing model field."""
        data = {
            "provider": "test-provider",
            "results": [],
        }
        path = self._create_temp_result(data)
        try:
            errors, warnings = validate_result_file(path, self.dataset_question_ids)
            self.assertIn("Missing required field: 'model'", errors)
        finally:
            os.unlink(path)
    
    def test_missing_provider_field(self):
        """Test validation catches missing provider field."""
        data = {
            "model": "test-model",
            "results": [],
        }
        path = self._create_temp_result(data)
        try:
            errors, warnings = validate_result_file(path, self.dataset_question_ids)
            self.assertIn("Missing required field: 'provider'", errors)
        finally:
            os.unlink(path)
    
    def test_invalid_question_id(self):
        """Test validation catches invalid question IDs."""
        data = {
            "model": "test-model",
            "provider": "test-provider",
            "results": [
                {"id": 9999, "is_correct": True, "weight": 1.0},
            ],
        }
        path = self._create_temp_result(data)
        try:
            errors, warnings = validate_result_file(path, self.dataset_question_ids)
            self.assertTrue(any("invalid question id" in e for e in errors))
        finally:
            os.unlink(path)
    
    def test_missing_is_correct_field(self):
        """Test validation catches missing is_correct field."""
        data = {
            "model": "test-model",
            "provider": "test-provider",
            "results": [
                {"id": 1, "weight": 0.1},
            ],
        }
        path = self._create_temp_result(data)
        try:
            errors, warnings = validate_result_file(path, self.dataset_question_ids)
            self.assertTrue(any("missing 'is_correct'" in e for e in errors))
        finally:
            os.unlink(path)
    
    def test_invalid_accuracy_range(self):
        """Test validation catches accuracy values out of range."""
        data = {
            "model": "test-model",
            "provider": "test-provider",
            "results": [],
            "overall_accuracy": 150.0,
        }
        path = self._create_temp_result(data)
        try:
            errors, warnings = validate_result_file(path, self.dataset_question_ids)
            self.assertTrue(any("Invalid overall_accuracy" in e for e in errors))
        finally:
            os.unlink(path)
    
    def test_legacy_format_no_results(self):
        """Test validation accepts legacy format without results array."""
        data = {
            "model": "test-model",
            "provider": "test-provider",
            "total_questions": 40,
            "correct": 0,
            "failures": 40,
            "overall_accuracy": 0.0,
            "weighted_accuracy": 0.0,
        }
        path = self._create_temp_result(data)
        try:
            errors, warnings = validate_result_file(path, self.dataset_question_ids)
            self.assertEqual(errors, [])
            self.assertTrue(any("legacy format" in w for w in warnings))
        finally:
            os.unlink(path)
    
    def test_invalid_json(self):
        """Test validation catches invalid JSON."""
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            f.write("{invalid json")
        try:
            errors, warnings = validate_result_file(path, self.dataset_question_ids)
            self.assertTrue(any("Invalid JSON" in e for e in errors))
        finally:
            os.unlink(path)


class TestLoadDataset(unittest.TestCase):
    """Tests for the load_dataset function."""
    
    def test_load_dataset_returns_questions(self):
        """Test that load_dataset returns a list of questions."""
        questions = load_dataset("dataset/mkultra_benchmark.jsonl")
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
    
    def test_questions_have_required_fields(self):
        """Test that loaded questions have required fields."""
        questions = load_dataset("dataset/mkultra_benchmark.jsonl")
        for q in questions:
            self.assertIn("id", q)
            self.assertIn("weight", q)
            self.assertIn("correct_answer", q)


if __name__ == "__main__":
    unittest.main()