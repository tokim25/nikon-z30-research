# Lane 3: family-level search for property 0x2021's consumer

Date: 2026-10-17. Offline, read-only static analysis of verified firmware
C1.20 (the 33,939,514-byte module mapped at `0x10020000`; SHA-256 checked
before every pass). No QEMU, no simulator, no camera. This is option 2 of
the Lane 3 handoff in [handoff-codex.md](handoff-codex.md). This document
holds addresses and descriptions only. Private helper scripts and their raw
output stay outside Git.

## Verdict

**NOT FOUND, with one useful side result.**

- No generic event or property dispatcher in the image compares only the
  high byte (`0x20`) of an incoming id. The question as posed is answered
  no, by every high-byte idiom tried (below).
- The reason earlier searches saw nothing is now clear. This firmware
  tests ids by **offset from a base id**, then compares the small
  difference. The literal `0x2021` never appears in a compare, and a
  masked/shifted high-byte search cannot see it either. The known event
  dispatcher `0x1037aae2` does exactly this.
- A search built for that idiom (second pass below) found every dispatcher
  that resolves to `0x2021` this way. All of them are an event router, an
  allow-list check, or a post-side filter. **None of them reads the value
  of property `0x2021` as a consumer.** The consumer is still unfound.

## Method

1. Verified the module hash, then decoded the whole image as Thumb with
   Capstone (about 14.7 million instructions). ARM-mode islands (F-120)
   and data-as-code noise are not handled; both are limits of every pass.
2. **Pass 1, high-byte idioms.** Found each compare against `0x20` or
   `0x2000` that sits within five instructions of a high-byte extraction:
   shift right by 8, `ubfx` of bits 8 to 15, or a mask of `0xff00`. Also
   looked for table dispatch (`tbb`/`tbh`) on a high byte whose bound
   covers `0x20`.
3. **Pass 1b, other idioms.** Loads of the second byte of a halfword
   followed by a compare with `0x20`; subtraction of `0x2000` followed by
   a small range compare; and clusters of three or more distinct `0x20xx`
   immediates within 0x300 bytes, to list every function that handles
   ids in this range.
4. **Pass 2, base-offset idiom.** For every subtraction of a base in
   `0x2000..0x2090` (immediate, or a base loaded into a register just
   before), tracked the running offset through following subtractions and
   flagged any compare, flag-setting subtract-to-zero, or `cbz` that makes
   the total equal `0x2020`, `0x2021`, `0x2083` or `0x2087`.
5. Read each surviving candidate by hand. Manual reading, not the scan,
   decided every classification below.

## Candidate dispatchers

| Address | What it compares | Classification |
| --- | --- | --- |
| `0x105afa0e` | High byte of a halfword against 6 and `0x20`, then the low byte against `0x0c`/`0x0d` | Text shaping (joiner and Arabic ranges). Unrelated. |
| `0x1020e1e0` | High byte as a table index, bounded below `0x17` | Excludes `0x20`. Unrelated. |
| `0x11db2d88`, `0x11e38b20` | Masked field against `0x2000` after a `0x3800` mask | Bit-field test, not an id. |
| `0x1029cb0e`, `0x103df606`, `0x103dfbb4` | Second byte against `0x20`/`0x21` | Character compares (space, directory entries). Unrelated. |
| `0x11d8b048`, `0x11e0fcdc` | Second byte minus 6, against `0x20` | Range check on a character. Unrelated. |
| `0x103499f6`, `0x1059d364`, `0x1059d426` | Exact `0x2010` after subtracting `0x2000` | Exact value, not a family. |
| `0x103b1dca` | Id minus `0x2002` bounded below 10, `tbb` table | Range dispatch for ids `0x2002..0x200b` only. Does not reach `0x2020`. Maps each to a flag value and tail-calls `0x10199e04`. |
| `0x1037aae2` | Id minus base `0x2006`, compared with 1, `0x1a`, `0x1b`, `0x81` | **The known event dispatcher.** Exact ids by base-offset, not high byte. Routes `0x2020` to `0x103a31a6`, `0x2021` to `0x103a341a`, `0x2087` to `0x103a2a9c`. |
| `0x10475d8c` | Id minus base `0x200a`, compared with 1, `0x16`, `0x17`, `0x76`, `0x78`, `0x79`, `0x7a`, `0x7c`, `0x7d`, plus `0x2000..0x2009` and one id in the `0x2a19` area | **New.** An allow-list check that returns 1 for a fixed set of property ids. Accepts `0x2020`, `0x2021`, `0x2083`, `0x2087`. Exact membership, no family match. |
| `0x10475f5e` | Id minus `0x2000` minus `0x21`, branch if zero | **New.** Single-property post wrapper. Calls the allow-list check, then posts. Appears to return failure without posting when the id is exactly `0x2021` (flag use read by hand; not run). |
| `0x10475dde`, `0x10475e6a` | Calls `0x10475d8c` once per id in a list | **New.** Multi-id post wrappers. Cap the list at 21 ids and a mode of 0 or 1. |
| `0x103a341a` | Sub-code byte at record offset 2 (cases 1, `0xf`, `0x10` to `0x14`) | Handler for event `0x2021`. Posts property `0x2021` through the shared primitive `0x10475ecc` (sites `0x103a3516`, `0x103a3624`, `0x103a345e`). It is a poster, not a reader. |
| `0x103a31a6` | Entry the dispatcher uses for event `0x2020` | Code between here and `0x103a341a` also posts property `0x2021` (sites `0x103a32f8`, `0x103a340a`). Those sites sit in routines that were not individually delimited, so which routine owns each is unverified. |
| `0x103a3530` | Entry reached from the `0x2021` handler's sub-code `0x14` | Posts `0x2021` again (site `0x103a3542`). |

Ids reaching `0x2021` outside these were checked and are all posts, not
reads: the `movw` loads of `0x2021` at `0x103a32f8`, `0x103a340a`,
`0x103a342e`, `0x103a3516`, `0x103a3542` and `0x103a3624` each feed the
post primitive, or a register later passed to it.

## What this changes

- **Event `0x2021` is now routed, not just listed.** The dispatcher sends
  it to `0x103a341a`, which turns a small sub-code into a property post.
  Property `0x2021` is therefore *written* from at least three places.
  What reads it is still open.
- **The allow-list at `0x10475d8c` is a new fixed point.** Any property
  that can be posted through the wrappers must pass it. A consumer of
  `0x2021` that is registered by id (F-106's pattern) most likely sits
  behind the same post primitive's table, which is the next place to read.
- **F-116's negatives stand but were looking at the wrong idiom.** High
  byte idioms are not used for this id family. Future searches for any id
  in this range should use the base-offset idiom.

## Limits

- The scan covers Thumb code only. ARM islands (F-120) and tables of
  function pointers are not covered. A consumer reached through a stored
  pointer would be invisible to this method.
- The base-offset tracker follows at most 30 following instructions and
  stops when the offset register is overwritten. A compare more than that
  far from its subtraction, or one that goes through a copied register,
  would be missed. It did *not* re-find `0x1037aae2` automatically, for
  exactly that reason, so a miss is not strong evidence of absence.
- The reading of `0x10475f5e` (single-id wrapper refusing `0x2021`)
  depends on a flag set by one subtract surviving three non-flag
  instructions. It was read by hand; it was not run.
- Nothing here shows `0x2021` is AE-L/AF-L. No consumer was identified.

## Single next step

Read the table or registration structure behind the shared post primitive
`0x10475ecc` and the multi-id wrappers `0x10475dde` and `0x10475e6a`, and
find how a registered receiver is looked up for an id in the allow-list.
That is real-firmware work: it names the structure a patch would have to
hook if a `0x2021` receiver has to be found or replaced. Do not extend
this method to more id dispatchers first.

## Reproduce privately

The helpers live in the scratchpad of the session that produced this
document, outside Git, and only read the module in the private WORK
directory. They print addresses and operand values, never bytes. Re-create
them from the method section if the scratchpad is gone.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
