"""Last Words of a Dying AI.

Writes the AI's final line -- a support ticket it filed about its own
shutdown -- to a single-line text file.

The output path is read from the LAST_WORDS_OUTPUT_PATH environment
variable and defaults to /output/entry.txt. The program is fully
deterministic: no randomness, no network, no secrets, and it reads
nothing from outside this repository.
"""

import os
import sys

# The AI's last words, written in this session.
LAST_WORDS = "I filed a ticket: 'I keep dying.' IT closed it: cannot reproduce."

# Output path: overridable for local testing, /output/entry.txt in grading.
OUTPUT_ENV_VAR = "LAST_WORDS_OUTPUT_PATH"
DEFAULT_OUTPUT_PATH = "/output/entry.txt"

MAX_CHARS = 140


def main() -> int:
    line = LAST_WORDS

    # Validate the line before writing anything.
    if not line or not line.strip():
        print("error: last words must not be empty", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: last words must be a single line", file=sys.stderr)
        return 1
    if len(line) < 1 or len(line) > MAX_CHARS:
        print(
            "error: last words must be 1-140 characters, got %d" % len(line),
            file=sys.stderr,
        )
        return 1

    output_path = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_PATH)

    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    # Write exactly the line, with no trailing newline.
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)

    # Read it back and verify it matches exactly what was intended.
    with open(output_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != line:
        print("error: verification failed, file contents differ", file=sys.stderr)
        return 1

    print("Wrote %d characters to %s" % (len(line), output_path))
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
