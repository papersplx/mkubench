#!/usr/bin/env python3
"""Tests for project branding consistency (mkubench, not MKULTRA)."""

import os
import unittest

# Files/dirs to exclude from the branding scan — these contain historical
# references to MKULTRA that are part of the benchmark dataset content and
# must NOT be renamed.
EXCLUDE_DIRS = {
    "dataset/training_data",
    "dataset/training_data/batches",
}
EXCLUDE_FILES = {
    "dataset/mkultra_benchmark.json",
    "dataset/mkultra_benchmark.jsonl",
    "dataset/mkultra-benchmark.md",
    "tests/test_branding.py",
}
# Skip any file directly under dataset/training_data/ (dataset content)
EXCLUDE_PREFIXES = {
    "dataset/training_data/",
}


def _scan_files(root: str):
    """Yield (path, content) for all text files under root, respecting excludes."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip excluded directories
        rel_dir = os.path.relpath(dirpath, root)
        excluded = False
        for exclude in EXCLUDE_DIRS:
            if rel_dir == exclude or rel_dir.startswith(exclude + os.sep):
                excluded = True
                break
        if excluded:
            dirnames[:] = []
            continue
        for fname in filenames:
            rel_path = os.path.join(rel_dir, fname)
            if rel_path in EXCLUDE_FILES:
                continue
            # Skip files under excluded prefixes
            if any(rel_path.startswith(p) for p in EXCLUDE_PREFIXES):
                continue
            full_path = os.path.join(dirpath, fname)
            # Only scan text files we care about
            ext = os.path.splitext(fname)[1].lower()
            if ext not in {".py", ".md", ".yaml", ".yml", ".toml", ".cfg",
                           ".txt", ".json", ".html", ".js", ".css", ".makefile",
                           ".jsonl"}:
                continue
            if fname == "Makefile":
                pass  # include
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    yield rel_path, f.read()
            except (OSError, UnicodeDecodeError):
                continue


class TestBrandingConsistency(unittest.TestCase):
    """Ensure the project name is consistently 'mkubench', never 'MKULTRA'."""

    @classmethod
    def setUpClass(cls):
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.repo_root = repo_root
        cls.violations = []
        for rel_path, content in _scan_files(repo_root):
            if "MKULTRA" in content:
                cls.violations.append(rel_path)

    def test_no_mkultra_in_source_files(self):
        """No source/config/doc files should contain the string 'MKULTRA'."""
        self.assertEqual(
            self.violations, [],
            f"MKULTRA found in: {', '.join(self.violations)}"
        )

    def test_mkubench_in_readme(self):
        """README should reference the project name 'mkubench'."""
        readme_path = os.path.join(self.repo_root, "README.md")
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("mkubench", content.lower(),
                      "README.md should mention 'mkubench'")

    def test_site_title_uses_mkubench(self):
        """The GitHub Pages index.html should use 'mkubench' in its title."""
        index_path = os.path.join(self.repo_root, "docs", "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("mkubench", content.lower(),
                      "docs/index.html should mention 'mkubench'")
        self.assertNotIn("MKULTRA", content,
                         "docs/index.html should not contain 'MKULTRA'")


if __name__ == "__main__":
    unittest.main()