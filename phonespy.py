#!/usr/bin/env python3
"""
Phone Lookup Tool (Offline‑First)
--------------------------------
A lightweight phone‑number OSINT helper that works entirely offline using the
`phonenumbers` library. It parses and validates numbers, then extracts:
  • Canonical E.164 & international formats
  • Region / country description
  • Carrier (where available)
  • Number type (mobile, fixed_line, toll‑free, etc.) – handled compatibly with
    both old and new `phonenumbers` releases so you don’t hit enum errors.
  • Associated time‑zones

Results can be printed to stdout and/or exported to JSON or CSV for easy
import into the rest of your OSINT workflows.

Optional online enrichers (disabled by default) are stubbed out so you can add
OpenCNAM, Numverify, Twilio Lookup, or any other API later without touching the
core logic.

Usage examples
--------------
$ python3 phone_lookup.py +12025550123 +447911123456

# Export to JSON
$ python3 phone_lookup.py +12025550123 -o results.json

# Export to CSV
$ python3 phone_lookup.py +12025550123 +16175551234 -o results.csv -f csv
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

import phonenumbers
from phonenumbers import geocoder, carrier, timezone, NumberParseException

# ------------------------------------------------------------
# Optional API placeholders – populate & uncomment if you later
# want live CNAM / spam‑score / reputation lookups.
# ------------------------------------------------------------
# OPTIONAL_API_CONFIG = {
#     "opencnam_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "opencnam_token": "your_auth_token",
# }


# --------------------------- Utility helpers --------------------------- #

def _phone_type_name(parsed) -> str:
    """Return the phone‑number type as a string, compatible with all versions."""
    num_type = phonenumbers.number_type(parsed)

    # Newer releases expose an Enum (IntEnum) so we can .name it
    try:
        from phonenumbers import PhoneNumberType  # noqa: WPS433 (local import for fallback)
        return PhoneNumberType(num_type).name  # type: ignore[arg‑type]
    except Exception:  # older pkg: enum isn’t callable – fall back to lookup dict
        try:
            return phonenumbers.PhoneNumberType._VALUES_TO_NAMES.get(num_type, "UNKNOWN")  # type: ignore[attr‑defined]
        except Exception:
            return str(num_type)


# --------------------------- Core Look‑up Logic --------------------------- #

def basic_lookup(raw_number: str) -> Dict[str, Any]:
    """Parse & enrich a single phone number using *offline* data only."""
    try:
        parsed = phonenumbers.parse(raw_number, None)
    except NumberParseException as exc:
        return {"input": raw_number, "valid": False, "error": str(exc)}

    valid = phonenumbers.is_valid_number(parsed)
    possible = phonenumbers.is_possible_number(parsed)

    info = {
        "input": raw_number,
        "valid": valid and possible,
        "possible": possible,
        "international_format": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        "e164_format": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
        "country_code": parsed.country_code,
        "region": geocoder.description_for_number(parsed, "en"),
        "carrier": carrier.name_for_number(parsed, "en"),
        "timezones": list(timezone.time_zones_for_number(parsed)),
        "type": _phone_type_name(parsed),
    }

    # ----- Stubs for future online enrichments (spam score, CNAM, etc.) -----
    # if OPTIONAL_API_CONFIG.get("opencnam_sid"):
    #     info.update({"caller_name": lookup_opencnam(info["e164_format"])})

    return info


# --------------------------- Helpers / I/O --------------------------- #

def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    """Write results to CSV."""
    if not rows:
        return
    fieldnames = rows[0].keys()
    with path.open("w", newline="", encoding="utf‑8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf‑8")


# --------------------------- CLI Entrypoint --------------------------- #

def cli() -> None:
    parser = argparse.ArgumentParser(
        prog="phone_lookup",
        description="Offline phone‑number OSINT helper",
    )
    parser.add_argument("numbers", nargs="+", help="Phone numbers to look up (e.g. +12025550123)")
    parser.add_argument("-o", "--output", help="Write results to FILE (json or csv)")
    parser.add_argument(
        "-f", "--format",
        choices=["json", "csv"],
        default="json",
        help="Output format when --output is used (default: json)",
    )

    args = parser.parse_args()

    results = [basic_lookup(num) for num in args.numbers]

    # Pretty‑print to stdout
    for res in results:
        if not res.get("valid"):
            print(f"[!] {res['input']}: Invalid – {res.get('error', '')}")
            continue

        print("\n" + res["international_format"])
        print(f"  Region      : {res['region']} ( +{res['country_code']} )")
        print(f"  Carrier     : {res['carrier'] or 'Unknown'}")
        print(f"  Type        : {res['type']}")
        print(f"  Time‑zones  : {', '.join(res['timezones']) if res['timezones'] else 'Unknown'}")

    # Optional file export
    if args.output:
        out_path = Path(args.output).expanduser()
        if args.format == "csv":
            write_csv(out_path, results)
        else:
            write_json(out_path, results)
        print(f"\n[+] Results written to {out_path.resolve()}")


if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        sys.exit("[!] Interrupted by user")
