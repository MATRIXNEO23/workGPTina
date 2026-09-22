#!/usr/bin/env python3
"""Fail-closed repository mutation guard."""
import argparse
import re
import sys

ALLOWED = "MATRIXNEO23/workGPTina"

def normalize(target: str) -> str:
    value = target.strip().removesuffix(".git").rstrip("/")
    value = re.sub(r"^https://github\.com/", "", value, flags=re.I)
    value = re.sub(r"^git@github\.com:", "", value, flags=re.I)
    return value

def assert_write_target(target: str) -> str:
    normalized = normalize(target)
    if normalized.casefold() != ALLOWED.casefold():
        raise PermissionError(f"ABORT: repository write target not authorized: {target}")
    return ALLOWED

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    args = parser.parse_args()
    try:
        print(assert_write_target(args.target))
    except PermissionError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(77)

if __name__ == "__main__":
    main()

