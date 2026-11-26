"""One Line to Your Younger Self — make.fun entry writer.

Writes the chosen one-liner to the harness output directory.
The entry is written exactly as-is (no trailing newline) so the
graded file is byte-identical to the line in this source file.
"""

import hashlib
import os
import sys

ENTRY = "Your mother won't always be a phone call away \u2014 call her while she still answers."

OUTPUT_FILENAME = "entry.txt"


def resolve_output_dir() -> str:
    """Output directory from MAKEFUN_OUTPUT_DIR, defaulting to /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def write_entry(output_dir: str) -> str:
    """Create the output dir if missing, then write entry.txt.

    Never deletes anything, and never writes into the repo.
    Returns the path of the file written.
    """
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, OUTPUT_FILENAME)
    payload = ENTRY.encode("utf-8")
    with open(target, "wb") as handle:
        handle.write(payload)
    return target


def verify(path: str) -> bool:
    """Read the file back and confirm it is byte-identical to ENTRY."""
    with open(path, "rb") as handle:
        return handle.read() == ENTRY.encode("utf-8")


def main() -> int:
    output_dir = resolve_output_dir()
    target = write_entry(output_dir)
    if not verify(target):
        print(f"error: {target} does not match the entry", file=sys.stderr)
        return 1
    digest = hashlib.sha256(ENTRY.encode("utf-8")).hexdigest()
    print(f"wrote {target} ({len(ENTRY.encode('utf-8'))} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
