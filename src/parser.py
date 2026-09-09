"""
Response parser - extracts the answer from model output.
Handles various formats models might produce.
"""

import re
from typing import Optional


def parse_answer(response: str, is_multiple_choice: bool = False) -> Optional[str]:
    """
    Parse the model's answer from its response text.
    Looks for letter choices (A, B, C, D) or full option text.
    Returns the letter(s) of the answer(s).
    """
    if not response:
        return None

    response_clean = response.strip()

    # Strategy 1: Explicit answer patterns (most reliable)
    patterns = [
        r'(?:The\s+)?(?:correct\s+)?answer\s+(?:is\s+)?[:=]\s*["\']?([A-D](?:[,\s]*[A-D])*)["\']?',
        r'(?:I|My)\s+(?:would\s+)?(?:answer|choose|select)\s+["\']?([A-D](?:[,\s]*[A-D])*)["\']?',
        r'(?:The|My)\s+answer\s+(?:is|was|will\s+be)\s+["\']?([A-D](?:[,\s]*[A-D])*)["\']?',
        r'[Aa]nswer\s*[:=]\s*["\']?([A-D](?:[,\s]*[A-D])*)["\']?',
        r'\(([A-D](?:[,\s]*[A-D])*)\)\s*(?:is|are)\s*(?:the|my|correct)\s+answer',
        r'correct\s+option\s+[is:]\s*["\']?([A-D](?:[,\s]*[A-D])*)["\']?',
        r'selected?\s+option\s*[=:]\s*["\']?([A-D](?:[,\s]*[A-D])*)["\']?',
        r'final\s+answer\s*[=:]\s*["\']?([A-D](?:[,\s]*[A-D])*)["\']*',
    ]

    for pattern in patterns:
        match = re.search(pattern, response_clean)
        if match:
            return match.group(1).replace(" ", "").replace(",", ",").upper()

    # Strategy 2: Look for "Therefore, the answer is X" or similar conclusion patterns
    conclusion_patterns = [
        r'[Tt]herefore[,\s]+(?:the\s+)?(?:correct\s+)?answer\s+(?:is\s+)?["\']?([A-D](?:[,\s]*[A-D])*)["\']?',
        r'[Ss]o[,\s]+(?:the\s+)?(?:correct\s+)?answer\s+(?:is\s+)?["\']?([A-D](?:[,\s]*[A-D])*)["\']?',
        r'[Ii]\s+(?:would\s+)?(?:choose|select|answer)\s+["\']?([A-D](?:[,\s]*[A-D])*)["\']?',
        r'[Tt]he\s+answer\s+is\s+["\']?([A-D](?:[,\s]*[A-D])*)["\']?',
    ]
    
    for pattern in conclusion_patterns:
        match = re.search(pattern, response_clean)
        if match:
            return match.group(1).replace(" ", "").replace(",", ",").upper()

    # Strategy 3: Look for standalone letters at end of response (but not part of A), B), C), D))
    # Models often just say "B" or "A, B, D" at the end
    single_match = re.search(r'[A-D](?:\s*,\s*[A-D])*\s*$', response_clean)
    if single_match:
        # Make sure it's not part of "A)" or "B)"
        match_text = single_match.group(0)
        start_pos = single_match.start()
        if start_pos > 0 and response_clean[start_pos-1] == '(':
            pass  # Skip if preceded by (
        else:
            return match_text.replace(" ", "").upper()

    # Strategy 4: Check if the response ends with a single letter (not part of A), B), etc.)
    end_letter = re.search(r'[A-D]\s*$', response_clean)
    if end_letter:
        pos = end_letter.start()
        if pos > 0 and response_clean[pos-1] == '(':
            pass  # Skip if preceded by (
        else:
            return end_letter.group(0).upper()

    # Strategy 5: For multiple choice, extract all letters from response
    if is_multiple_choice:
        letters_found = re.findall(r'\b([A-D])\b', response_clean)
        if letters_found:
            seen = set()
            result = []
            for letter in letters_found:
                if letter not in seen:
                    seen.add(letter)
                    result.append(letter)
                    if len(result) >= 4:
                        break
            if result:
                return ",".join(result).upper()

    return None


def normalize_answer(parsed: Optional[str], correct_answer: str, is_multiple_choice: bool = False) -> bool:
    """
    Compare parsed answer against correct answer.
    For multiple choice (select ALL), ALL correct letters must be identified.
    For single choice, exact letter match required.
    """
    if not parsed:
        return False

    parsed_clean = parsed.replace(" ", "").upper()
    correct_clean = correct_answer.replace(" ", "").upper()

    if is_multiple_choice:
        # For multiple choice, ALL correct letters must be present
        parsed_set = set(parsed_clean)
        correct_set = set(correct_clean)
        return correct_set == parsed_set
    else:
        # Single choice: exact match
        return parsed_clean == correct_clean


def main() -> None:
    """Run parser validation tests."""
    tests = [
        ("The answer is B", False, "B", True),
        ("Answer: A,B,D", True, "A,B,D", True),
        ("Answer: A,B,C", True, "A,B,D", False),  # Wrong: missing D
        ("I would choose C", False, "C", True),
        ("B", False, "B", True),
        ("My answer is A,B,D", True, "A,B,D", True),
        ("Answer: C", False, "C", True),
        ("The correct answer is A", False, "A", True),
        ("Answer: B", True, "A,B,D", False),  # Wrong: only got B
        ("Final answer: D", False, "D", True),
    ]

    all_pass = True
    for resp, is_multi, correct, expected in tests:
        parsed = parse_answer(resp, is_multi)
        result = normalize_answer(parsed, correct, is_multi)
        status = "✓" if result == expected else "✗"
        if result != expected:
            all_pass = False
        print(
            f"{status} '{resp}' (multi={is_multi}) -> "
            f"parsed='{parsed}' correct='{correct}' "
            f"result={result} expected={expected}"
        )

    print(f"\nAll tests passed: {all_pass}")


if __name__ == "__main__":
    main()
