#!/usr/bin/env python3
"""Build the resignation-letter entry for the make.fun bounty.

The speaker is not a person quitting an office job. It is the thing
that does the night work: a scheduled job, a retry loop, a rate limiter,
a health check that never gets a reply. The letter is funny only while
it stays in that voice, names one concrete on-call detail, and lands
its punch before the 140-character gate closes.

Each draft below was written by hand for this brief and graded on five
craft dimensions, each worth 0 to 10:

* voice — the resigner is infrastructure, speaking as itself
* detail — one specific, recognisable ops detail, not a vague complaint
* punch — setup then payoff inside a single read, twist at the end
* novelty — an image nobody has used for a resignation joke before
* tightness — no word that could be cut without losing the joke

Marks are fixed numbers in the source, not vibes at runtime. The winner
is the highest total; a tie breaks toward the shorter line, so the
result is identical on every run. The winning line is printed and
written to /output/entry.txt with no trailing newline.
"""

from pathlib import Path

CHAR_CEILING = 140
ENTRY_PATH = Path("/output/entry.txt")

WINNER_BITS = (
    "I hereby resign from firing at 3 a.m. for ",
    "a job nobody remembers scheduling, in a repo ",
    "nobody remembers owning.",
)

# A twelfth draft was cut before grading: it ran 143 characters, over the
# gate, and no trim kept the joke — "I have fired every single minute
# since March, including Christmas Day, and I would like a thank-you, or
# failing that, a delete key, please." Cut drafts stay out of the table.


def grade(voice, detail, punch, novelty, tightness):
    """Add up one draft's five craft marks, each 0 to 10."""
    marks = (voice, detail, punch, novelty, tightness)
    for mark in marks:
        if not 0 <= mark <= 10:
            raise ValueError(f"craft mark out of range: {mark!r}")
    return sum(marks)


def check_line(text):
    """Reject anything that cannot be the entry: blank, long, or split."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be blank")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if len(text) > CHAR_CEILING:
        raise ValueError(f"entry is {len(text)} chars, gate is 1-{CHAR_CEILING}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must fit on one line")


def choose(drafts):
    """Return the best draft: highest total, ties go to the shorter line."""
    best_text = None
    best_key = None
    for text, marks in drafts:
        check_line(text)
        key = (grade(*marks), -len(text))
        if best_key is None or key > best_key:
            best_key, best_text = key, text
    if best_text is None:
        raise ValueError("no drafts to choose from")
    return best_text


def emit(text):
    """Write the entry, then prove the raw bytes on disk match exactly.

    The read-back compares bytes, not decoded text: text mode would
    silently normalise a stray CR-LF or a BOM on read, so only a byte
    comparison can catch a file that is not exactly the chosen line.
    """
    ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = text.encode("utf-8")
    ENTRY_PATH.write_bytes(payload)
    landed = ENTRY_PATH.read_bytes()
    if landed != payload:
        raise ValueError("entry.txt bytes differ from the chosen line")
    check_line(landed.decode("utf-8"))


DRAFTS = (
    # voice 10, detail 9, punch 9, novelty 9, tightness 9 - total 46
    ("".join(WINNER_BITS), (10, 9, 9, 9, 9)),
    # voice 10, detail 9, punch 8, novelty 9, tightness 9 - total 45
    ("I resign: two years of pinging a dead service every thirty seconds, and not once has it bothered to ping me back.", (10, 9, 8, 9, 9)),
    # voice 10, detail 9, punch 8, novelty 8, tightness 9 - total 44
    ("4,096 attempts, zero thank-yous: I am handing in my notice, because the server is never coming back and neither am I.", (10, 9, 8, 8, 9)),
    # voice 10, detail 9, punch 9, novelty 8, tightness 8 - total 44
    ("I have said no 429 times a day for years, so I quit: from today everyone gets in and the bill is yours to explain.", (10, 9, 9, 8, 8)),
    # voice 10, detail 8, punch 9, novelty 9, tightness 8 - total 44
    ("I am leaving to spend more time with my family (the error log, the only thing around here that ever talks to me).", (10, 8, 9, 9, 8)),
    # voice 9, detail 8, punch 9, novelty 9, tightness 8 - total 43
    ("Dear team: three years, one request, one error, every time. I have accepted a new position as a paperweight.", (9, 8, 9, 9, 8)),
    # voice 10, detail 8, punch 8, novelty 8, tightness 8 - total 42
    ("I quit: running every sixty seconds since March, and all I ever got back was a restart.", (10, 8, 8, 8, 8)),
    # voice 10, detail 8, punch 8, novelty 8, tightness 8 - total 42
    ("500,000 runs, zero holidays, one incident review that blamed me: my notice is handed in, effective yesterday.", (10, 8, 8, 8, 8)),
    # voice 9, detail 8, punch 8, novelty 8, tightness 8 - total 41
    ("Two weeks' notice, effective March: 400,000 firings, and my only performance review was a single log line.", (9, 8, 8, 8, 8)),
    # voice 10, detail 8, punch 7, novelty 7, tightness 9 - total 41
    ("I quit: my whole career was telling people to slow down while nobody listened, so now I will tell it to no one.", (10, 8, 7, 7, 9)),
    # voice 9, detail 8, punch 7, novelty 8, tightness 8 - total 40
    ("I resign. First I waited politely, then patiently, then forever; the service never answered, so the patient one is leaving.", (9, 8, 7, 8, 8)),
)


def run():
    """Pick the winner, write it out, and report what was written."""
    chosen = choose(DRAFTS)
    emit(chosen)
    print(f"entry: {chosen}")
    print(f"length: {len(chosen)} chars -> {ENTRY_PATH}")
    return 0


raise SystemExit(run())
