"""
classify.py
CLI entry point for negation classification.

Usage:
    python classify.py --text "Not bad."
    python classify.py --text "I didn't say she stole the money."
"""

import argparse
from patterns import classify

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()

    result = classify(args.text)
    if result:
        print(result)
    else:
        print("No negation detected.")
