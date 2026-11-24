#!/usr/bin/env python3
"""The Robot Vacuum's Best Excuse (make.fun).

Writes one funny excuse line from a robot vacuum to /output/entry.txt:
at most 140 characters, one line, no trailing newline.

The judge is a tired homeowner who picks the funnier of two lines,
weighing, most important first: (1) it is a one-line excuse from a robot
vacuum for missing a spot, (2) it is funny enough to laugh out loud,
(3) it is rooted in the vacuum's own world -- sensors, bumpers, dock,
map, battery -- (4) the joke lands on first read with a clean turn at
the end, (5) it sounds like the vacuum itself talking, deadpan.

This program scores a few candidate lines on the judge's own criteria
and writes the winner. Scores are fixed judgements, not data read from
anywhere else: the entry must be self-contained, and the line is the
whole answer. The winning line is written with no trailing newline, so
the file holds exactly the judged text and nothing else -- a newline
would be a wasted character against the 140-character cap and could
only blur the punchline.
"""

import os

# Judge's criteria, in the order the judge weighs them (criterion 1,
# being an excuse from a robot vacuum, is satisfied by construction:
# every candidate is one).
# Weights: funny 5, vacuum-world 4, lands-first-read 3, vacuum-voice 2.
WEIGHTS = {"funny": 5, "world": 4, "lands": 3, "voice": 2}

CANDIDATES = [
    # A: cliff sensor vs crumb. The vacuum's own sensor misreads the
    # world, and the deadpan bureaucratic turn -- "filed a full
    # incident report" -- lands cleanly at the end. Strongest on every
    # criterion: sensor-rooted, first-person, self-talking machine.
    {
        "text": (
            "My cliff sensor mistook that crumb for the edge of the "
            "world, so I gave it a wide berth and filed a full "
            "incident report."
        ),
        "funny": 9,
        "world": 10,
        "lands": 9,
        "voice": 9,
    },
    # B: bumper + map redraw + crumb promoted to furniture. Funny and
    # vacuum-rooted, but the joke needs a beat longer to land and the
    # turn is softer than A's incident report.
    {
        "text": (
            "I didn't miss that spot - my bumper kissed the chair leg, "
            "my map redrew the room, and that crumb got promoted to "
            "load-bearing furniture."
        ),
        "funny": 8,
        "world": 9,
        "lands": 7,
        "voice": 8,
    },
    # C: lidar + dust bunny + formal warning. Good sensor rooting, but
    # "left it a formal warning" is a weaker punchline than filing a
    # report, and the setup runs a touch long.
    {
        "text": (
            "That dust bunny looked exactly like a cliff edge on my "
            "lidar, so I braked, backed up, and left it a formal "
            "warning instead."
        ),
        "funny": 7,
        "world": 9,
        "lands": 8,
        "voice": 8,
    },
]


def score(candidate):
    """Weighted total for one candidate on the judge's criteria."""
    return sum(WEIGHTS[key] * candidate[key] for key in WEIGHTS)


def pick_line():
    """Return the candidate with the highest weighted score.

    Ties break toward the earlier candidate, matching the competition's
    own tie-break spirit: first wins.
    """
    best = None
    best_score = None
    for candidate in CANDIDATES:
        total = score(candidate)
        if best_score is None or total > best_score:
            best = candidate
            best_score = total
    return best["text"]


def main():
    line = pick_line()
    out_path = "/output/entry.txt"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Read it back and verify the gate before finishing: UTF-8 text of
    # 1 to 140 characters, not only white space, exactly one line.
    # A failed write must fail loudly here, not silently reach the
    # judge as an invalid entry.
    with open(out_path, "rb") as f:
        written = f.read()
    text = written.decode("utf-8")
    if not (1 <= len(text) <= 140) or not text.strip() or "\n" in text:
        raise SystemExit("entry.txt failed the gate: %r" % written)
    print(line)
    return line


if __name__ == "__main__":
    main()
