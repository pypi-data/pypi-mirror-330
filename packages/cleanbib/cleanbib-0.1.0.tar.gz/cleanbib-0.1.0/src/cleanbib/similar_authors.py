# %%
from difflib import SequenceMatcher
import re

# %%
def find_author_inconsistencies(bib_cleaner):
    """
    Identifies potential inconsistencies in author names.

    :param bib_cleaner: An instance of BibCleaner with loaded entries.
    :return: A list of detected inconsistencies.
    """
    authors = list(bib_cleaner.authors)  # List of (first name, last name) tuples
    issues = []

    for i, (first1, last1) in enumerate(authors):
        for first2, last2 in authors[i + 1:]:

            if last1 == last2 and _has_initialized_name(first1, first2):
                issues.append(f"Possible initialized first name inconsistency: '{first1} {last1}' vs. '{first2} {last2}'")

    return issues

# %%
def _has_initialized_name(name1, name2):
    """
    Checks if one name has initialized components of the other OR both have abbreviations
    that must match in structure.

    Example cases:
    - "David Ethan Hogan" vs. "David E. Hogan" (Valid)
    - "David E. Hogan" vs. "D. E. Hogan" (Valid)
    - "David J. Hogan" vs. "D. Hogan" (Invalid)
    """
    parts1 = name1.split()
    parts2 = name2.split()

    # If both have abbreviations, they must have the same number of elements and match each part
    if _contains_abbreviations(parts1) and _contains_abbreviations(parts2):
        if len(parts1) != len(parts2):
            return False
        return all(_is_abbreviated_match(p1, p2) for p1, p2 in zip(parts1, parts2))

    # Otherwise, check if one is an abbreviation of the other
    if len(parts1) > len(parts2):
        long_name, short_name = parts1, parts2
    else:
        long_name, short_name = parts2, parts1

    match_count = 0
    for short_part in short_name:
        for long_part in long_name:
            if short_part == long_part or _is_abbreviated_version(short_part, long_part):
                match_count += 1
                break

    return match_count == len(short_name)


def _contains_abbreviations(parts):
    """Checks if a name has any abbreviated components."""
    return any(len(p) == 2 and p.endswith('.') for p in parts)


def _is_abbreviated_match(part1, part2):
    """Checks if two parts match as abbreviations or full names."""
    return (part1 == part2) or _is_abbreviated_version(part1, part2) or _is_abbreviated_version(part2, part1)


def _is_abbreviated_version(short, long):
    """Checks if a short name is an initial or abbreviation of a longer name."""
    return (len(short) == 2 and short.endswith('.') and long.startswith(short[0])) or (short + "." == long)
# %%
