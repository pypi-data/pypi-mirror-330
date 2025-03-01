"""
Utilities for handling right-to-left (RTL) text in subtitles.
"""
import os
from collections import Counter

import pysrt
import unicodedata as ud


def remove_unicode_control_chars(input_text: str) -> str:
    """
    Removes Unicode control characters and converts no-break spaces to regular spaces.
    
    Args:
        input_text: The text to process
        
    Returns:
        Text with control characters removed
    """
    control_chars = {
        "\u200E": "",  # LRM (Left-to-Right Mark)
        "\u200F": "",  # RLM (Right-to-Left Mark)
        "\u202A": "",  # LRE (Left-to-Right Embedding)
        "\u202B": "",  # RLE (Right-to-Left Embedding)
        "\u202C": "",  # PDF (Pop Directional Formatting)
        "\u202D": "",  # LRO (Left-to-Right Override)
        "\u202E": "",  # RLO (Right-to-Left Override)
        "\u00A0": " "  # NBSP (Non-Breaking Space)
    }

    for char, replacement in control_chars.items():
        input_text = input_text.replace(char, replacement)
    return input_text


def determine_text_direction(text: str) -> str:
    """
    Detects the dominant writing direction of a string.
    
    Based on: https://stackoverflow.com/a/75739782/10327858
    
    Args:
        text: The text to analyze
        
    Returns:
        "rtl" if right-to-left is dominant, otherwise "ltr"
    """
    char_directions = Counter([ud.bidirectional(c) for c in text])
    rtl_count = char_directions['R'] + char_directions['AL'] + char_directions['RLE'] + char_directions["RLI"]
    ltr_count = char_directions['L'] + char_directions['LRE'] + char_directions["LRI"]
    return "rtl" if rtl_count > ltr_count else "ltr"


def fix_rtl_via_unicode_chars(input_text: str) -> str:
    """
    Adds RTL mark at the start of each line to ensure proper display of RTL text.
    
    Args:
        input_text: The text to process
        
    Returns:
        Text with RTL marks inserted
    """
    rtl_mark = "\u202B"  # RLE (Right-to-Left Embedding)
    text = input_text.replace(rtl_mark, "")  # Remove any existing marks
    text = rtl_mark + text.replace("\n", "\n" + rtl_mark)  # Add mark at start of each line
    return text


def fix_rtl(filename: str) -> None:
    """
    Processes a subtitle file to properly display RTL text.
    
    For each subtitle entry, if the text is predominantly RTL:
    1. Remove any existing control characters
    2. Add RTL marks at the beginning of each line
    
    Args:
        filename: Path to the subtitle file
    """
    # Normalize the path for the current OS
    filename = os.path.normpath(filename)

    # Load subtitles
    subs = pysrt.open(filename)
    
    # Process each subtitle
    for sub in subs:
        if determine_text_direction(sub.text) == "rtl":
            # Clean text and add RTL markers
            cleaned_text = remove_unicode_control_chars(sub.text)
            sub.text = fix_rtl_via_unicode_chars(cleaned_text)

    # Save the modified subtitles
    subs.save(filename, encoding='utf-8')