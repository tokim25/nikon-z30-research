# Review of Claude's live-view guard conclusion

2026-10-17. Static/read-only review; no simulator run, encoding, overlay
build, patch modification or hardware access.

Reviewed `claude/sharp-bartik-ed4fb7` at
`9a60deba0b2718c524dc3f59d517ff9151bfd562` against main
`8802ab748ebcace4f4f7ffa5ca9723e6f9114062`. The remote main hash matched
at review time. The branch adds only a fact and Claude handoff text; its
worktree is clean. The implementation reference is the existing F-148
overlay, manifest SHA-256
`5a933892e98effb0ba114adc1ad0e3a4be40daf2cac021df73e8bc1661ef37c9`.

## Finding

**Supported:** no proven still-photo eligibility guard is available at
`0x102f5810` in the reviewed evidence. Independent bounded decoding of the
hash-verified original confirms the branch's local control-flow account:

- The bit-6 test on the byte at `0xc181b4b4` chooses whether to call
  `0x104bd3c0`. Both local paths join at `0x102f580c`, assuming called
  helpers return.
- The next call supplies live-view object `0xc1821d44` and selector 1 to
  `0x104b9116`. The setter writes the object selector; it does not establish
  still-photo semantics.
- The existing overlay guard checks screen-stack count zero and that same
  selector equal to 1. Its mask helper checks image-area choice 1. None of
  those fields has a proven still/movie eligibility mapping here.
- Earlier helper results retained in registers, the bit-6 byte, upstream
  routing and mode-object constants supply no already-proven replacement
  predicate in the reviewed record. Their presence is not permission to
  invent a field/value guard.

F-012/F-015 and the static worker-chain report already distinguish selector
routing from shooting eligibility. F-148/F-160's bounded ABI results do not
add that missing semantic guarantee.

**Qualification:** the guard is insufficient to certify exclusion of movie,
playback, warnings or unavailable states. That is not proof that each such
state reaches this worker, nor a demonstrated harmful execution. Claude's
movie-admission claim is correctly labelled conditional inference; its
handoff should preserve that qualification rather than imply observed
reachability. No alternative static guard is established by this review.

## GO / NO-GO and single decision

**NO-GO for a camera-ready or certified stills-only implementation.** Native
lifecycle acceptance and the remaining build/hardware gates stay open.

**GO only for the already-authorized bounded offline stills prototype.**
The owner's subsequent [scope clarification](owner-direction-2026-10-17.md)
removed movie-transition/exclusion evidence as a prerequisite for that
prototype. It did not establish movie exclusion, waive stills cleanup or
authorize hardware. The branch's instruction to exclude the hook from all
build decisions until a movie predicate is found therefore overstates the
current blocker under that narrower scope.

Single next decision: retain the existing hook only as a bounded offline
stills prototype; do not promote its UI guard to an eligibility guarantee
or a camera-ready GO. No hook rewrite or new movie research is justified
by this review alone.

## Documentation before integration

The branch's fact number **F-150** is now on main. The local stills-controls
finding was renumbered from F-150 to **F-156** for publication, resolving
that collision without changing the merged fact. This review allocates no
additional fact number.

The branch handoff also needs the later owner scope clarification, and
“unsafe” should mean “insufficient for the claimed exclusion guarantee,”
not “a demonstrated failure in every excluded state.” Keep the historical
movie-off design requirement distinct from the narrower current prototype
acceptance scope. Claude-owned files were not edited by this review.

No commit, push, PR or merge. Raw firmware and concrete overlay material
remain private. Review stopped here as requested.
