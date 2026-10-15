# Native guides across simulator UI states

Date: 2026-10-15. Simulator only, unchanged firmware. Results come from a
helper (five live-view runs, a few menu runs); I have not repeated the menu
runs.

## Live view: works

The per-cycle call (see [native-guides-simulator.md](native-guides-simulator.md))
drew the bars on screen rows 107 to 108 and 371 to 372, completing every time
but once. They overlapped no stock graphics: the info button, touch and menu
icons and focus brackets sit elsewhere. The bars showed two stops after the
first call and were gone one stop after the last. Opening the stock menu first,
then live view, behaved the same.

## Menu: does not carry over

- At idle, in the plain menu and in the menu over live view, the compose
  function never fired, so there is no cycle to hook.
- It fired only during redraws caused by key events, with different source
  layers each time.
- Calls made then returned as complete after up and down keys, but no bars
  appeared.
- With the OK and Back keys, the calls stalled the transition in every run.
  The cause is unknown.

## Not reachable

Touch input and an information-overlay toggle had no effect in live view. The
focus brackets and icons are already part of the stock live-view scene.

## Implication

Guides can be drawn in live view only, with a debugger hook. A menu-safe design
needs a different hook point.

Written by Claude (Sonnet 5.5) in collaboration with Tony Kim.
