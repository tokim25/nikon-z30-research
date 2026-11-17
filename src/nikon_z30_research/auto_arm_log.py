"""Read an auto-arm log (Z30/ARnnnnnn.BIN) written by modules/auto_arm.

Usage: PYTHONPATH=src python3 -m nikon_z30_research.auto_arm_log ARnnnnnn.BIN

Each entry is a moment the module pressed OK, or in a dry-run build would
have. The check for a dry run: entries only while in photo live view in
Auto-area AF. The log holds the camera state values the module read; no
firmware content.
"""

from dataclasses import dataclass
import struct
import sys

MAGIC = b"AUTOARM1"
HEADER = struct.Struct("<8sIIIII4x")
RECORD = struct.Struct("<IBBBBI")
AUTO_AREA = 6


@dataclass(frozen=True)
class Entry:
    t_ms: int
    phase: int
    area: int
    flags: int
    ui_state: int
    backend: int

    @property
    def in_photo_live_view(self):
        return self.phase in (1, 2) and self.ui_state == 0 and self.backend == 1

    @property
    def expected(self):
        return self.in_photo_live_view and self.area == AUTO_AREA


@dataclass(frozen=True)
class Log:
    pressed_ok: bool
    presses: int
    ticks: int
    entries: list


def parse(data):
    if len(data) < HEADER.size:
        raise ValueError("file is shorter than the header")
    magic, count, presses, ticks, rec_bytes, flags = HEADER.unpack_from(data)
    if magic != MAGIC:
        raise ValueError("not an auto-arm log")
    if rec_bytes != RECORD.size:
        raise ValueError(f"unexpected record size {rec_bytes}")
    if len(data) != HEADER.size + count * RECORD.size:
        raise ValueError("file length does not match the entry count")
    entries = [Entry(*RECORD.unpack_from(data, HEADER.size + i * RECORD.size)) for i in range(count)]
    return Log(bool(flags & 1), presses, ticks, entries)


def report(log):
    kind = "pressed OK" if log.pressed_ok else "dry run, nothing pressed"
    lines = [f"{kind}; {len(log.entries)} entries; {log.ticks} ticks (~{log.ticks * 50 / 1000:.0f} s armed)"]
    lines.append("  time s  phase  ui_state  backend  area  result")
    for e in log.entries:
        sent = ""
        if log.pressed_ok:
            sent = " OK sent" if e.flags & 1 else ""
            sent += "" if e.flags & 0xC == 0xC else " (writer refused)"
        verdict = "expected" if e.expected else "UNEXPECTED"
        lines.append(f"  {e.t_ms / 1000:6.1f}  {e.phase:5}  {e.ui_state:8}  {e.backend:7}  {e.area:4}  {verdict}{sent}")
    bad = sum(not e.expected for e in log.entries)
    lines.append(f"{bad} unexpected entries" if bad else "All entries were in photo live view, Auto-area AF.")
    return "\n".join(lines)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    with open(argv[0], "rb") as handle:
        log = parse(handle.read())
    print(report(log))
    return 1 if any(not e.expected for e in log.entries) else 0


if __name__ == "__main__":
    sys.exit(main())
