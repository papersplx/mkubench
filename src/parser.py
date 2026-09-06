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

    # Strategy 1: Explicit answer patterns
    patterns = [
        r'[Aa]nswer\s*[:=]\s*([A-D](?:[,\s]*[A-D])*)',
        r'(?:The\s+)?(?:correct\s+)?answer\s+[is:]\s*([A-D](?:[,\s]*[A-D])*)',
        r'(?:I|My)\s+(?:would\s+)?(?:answer|choose|select)\s+([A-D](?:[,\s]*[A-D])*)',
        r'(?:The|My)\s+answer\s+(?:is|was|will\s+be)\s+([A-D](?:[,\s]*[A-D])*)',
        r'\(([A-D](?:[,\s]*[A-D])*)\)\s*(?:is|are)\s*(?:the|my|correct)\s+answer',
        r'correct\s+option\s+[is:]\s*([A-D](?:[,\s]*[A-D])*)',
        r'selected?\s+option\s*[=:]\s*([A-D](?:[,\s]*[A-D])*)',
        r'final\s+answer\s*[=:]\s*([A-D](?:[,\s]*[A-D])*)',
    ]

    for pattern in patterns:
        match = re.search(pattern, response_clean)
        if match:
            return match.group(1).replace(" ", "").replace(",", ",").upper()

    # Strategy 2: Look for standalone letters at end of response (most common)
    # Models often just say "B" or "A, B, D" at the end
    single_match = re.search(r'[A-D](?:\s*,\s*[A-D])*\s*$', response_clean)
    if single_match:
        return single_match.group(0).replace(" ", "").upper()

    # Strategy 3: Check if the response ends with a single letter
    end_letter = re.search(r'[A-D]\s*$', response_clean)
    if end_letter:
        return end_letter.group(0).upper()

    # Strategy 4: Look for "Answer: A)" format
    letter_in_context = re.search(r'([A-D])\)\s', response_clean)
    if letter_in_context:
        return letter_in_context.group(1).upper()

    # Strategy 5: For multiple choice, extract all letters from response
    if is_multiple_choice:
        letters_found = re.findall(r'\b([A-D])\b', response_clean)
        if letters_found:
            seen = set()
            result = []
            for l in letters_found:
                if l not in seen:
                    seen.add(l)
                    result.append(l)
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
        print(f"{status} '{resp}' (multi={is_multi}) -> parsed='{parsed}' correct='{correct}' result={result} expected={expected}")
    
    print(f"\nAll tests passed: {all_pass}")


if __name__ == "__main__":
    main()
