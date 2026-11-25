# One-Line Resignation Letter — make.fun bounty
# u-deranalabs-the-funniest-one-line-resignation-letter-53c0d947
#
# The program writes one line of text (1-140 characters) to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. perspective: the resigner is something an agent runs (a cron job, a
#      retry loop, a rate limit), speaking in its own first-person voice —
#      never a human quitting a human job
#   2. specificity: a concrete detail a tired engineering manager recognises
#      at once (3 a.m. runs, 429s, dead services, repos nobody owns)
#   3. joke structure: setup, then a punch that lands in a single read —
#      the resignation twist must be the funny part, not an afterthought
#   4. freshness: an original image, no stock "I quit" and no borrowed joke
#   5. brevity: every word earns its place inside the 140-character gate
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.
#
# One further candidate was drafted and rejected before scoring because it
# broke the gate at 141 characters: "I have fired every minute since
# March, including Christmas, and I would like to formally request a
# thank-you, or, failing that, a delete key." It is not in the list below.
#
# Revision pass (second draft of the winner): the winning line was re-read
# for weak spots. Candidates for change were (a) tightening the ending to
# "in a repo nobody owns" (108 chars) and (b) opening with "Effective
# immediately, I stop firing". Both were rejected: the repeated "nobody
# remembers" is the joke's engine — the job is forgotten twice over — and
# "I hereby resign" is what marks the line as a resignation letter rather
# than a status update. The winner stands verbatim, re-scored 46, still top.

CANDIDATES = [
    # score: perspective 10, specificity 9, joke 9, freshness 9, brevity 9 = 46
    ("I hereby resign from firing at 3 a.m. for a job nobody remembers "
     "scheduling, in a repo nobody remembers owning.",
     46),
    # score: perspective 10, specificity 9, joke 8, freshness 9, brevity 9 = 45
    ("I resign: I have pinged a dead service every thirty seconds for two "
     "years, and it has never once pinged me back.",
     45),
    # score: perspective 10, specificity 9, joke 8, freshness 8, brevity 9 = 44
    ("After 4,096 attempts and zero thank-yous, I am resigning: the server "
     "is not coming back, and neither am I.",
     44),
    # score: perspective 10, specificity 9, joke 9, freshness 8, brevity 8 = 44
    ("I am tired of saying no 429 times a day, so I quit: from now on, "
     "everyone gets in, and you can explain the bill.",
     44),
    # score: perspective 10, specificity 8, joke 9, freshness 9, brevity 8 = 44
    ("I am resigning to spend more time with my family, by which I mean "
     "the error log, which is the only thing that ever talks to me.",
     44),
    # score: perspective 9, specificity 8, joke 9, freshness 9, brevity 8 = 43
    ("Dear team, after three years of trying the same request and getting "
     "the same error, I have accepted a position as a paperweight.",
     43),
    # score: perspective 10, specificity 8, joke 8, freshness 8, brevity 8 = 42
    ("I quit. I have run every sixty seconds since March, and the only "
     "thing I have ever received in return is a restart.",
     42),
    # score: perspective 10, specificity 8, joke 8, freshness 8, brevity 8 = 42
    ("After 500,000 runs, zero holidays, and one incident review that "
     "blamed me, I am handing in my notice, effective yesterday.",
     42),
    # score: perspective 9, specificity 8, joke 8, freshness 8, brevity 8 = 41
    ("This is my two weeks' notice, effective March: I have fired 400,000 "
     "times and my only performance review was a log line.",
     41),
    # score: perspective 10, specificity 8, joke 7, freshness 7, brevity 9 = 41
    ("I quit: I spent my whole career saying slow down to people who never "
     "listened, and now I am going to say it to no one.",
     41),
    # score: perspective 9, specificity 8, joke 7, freshness 8, brevity 8 = 40
    ("I resign. I waited politely, then longer, then longest, and the "
     "service still never answered, so I am done being the patient one.",
     40),
]

# The gate requires 1-140 characters of non-whitespace UTF-8 text, one line.
MAX_CHARS = 140


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what landed on disk: byte-identical to the chosen line, one
    # line only, inside the 1-140 character gate. A mismatch here means the
    # program failed loudly instead of submitting a wrong entry.
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert "\n" not in written, "entry must be a single line"
    assert written.strip(), "entry must not be only whitespace"
    assert 1 <= len(written) <= MAX_CHARS, f"entry over gate: {len(written)} chars"
    print(f"{line} ({len(written)} chars)")


if __name__ == "__main__":
    main()
