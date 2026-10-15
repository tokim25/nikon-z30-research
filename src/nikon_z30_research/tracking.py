"""Original offline interaction model; no camera or autofocus implementation."""

from dataclasses import dataclass
import math


ELIGIBLE_AREAS = frozenset({"auto-area", "auto-area-people", "auto-area-animals"})
ELIGIBLE_FOCUS = frozenset({"AF-S", "AF-C", "AF-A"})


@dataclass(frozen=True)
class AcquisitionRequest:
    request_id: int
    target: tuple[float, float]


@dataclass(frozen=True)
class Transition:
    event: str
    state: str
    reason: str | None
    active_request: int | None
    emitted: tuple[AcquisitionRequest, ...]


def _valid_target(target):
    return (
        isinstance(target, tuple)
        and len(target) == 2
        and all(
            type(coordinate) in (int, float)
            and 0 <= coordinate <= 1
            and math.isfinite(coordinate)
            for coordinate in target
        )
    )


class TrackingModel:
    """Photo-mode proposal with explicit input edges and integer clock ticks.

    Methods return only mock acquisition requests. A caller may supply an
    acknowledgement, but no backend, callback, or device is invoked.
    """

    def __init__(self, *, focus="AF-C", area="auto-area", target=None, timeout_ticks=5):
        if type(timeout_ticks) is not int or timeout_ticks <= 0:
            raise ValueError("timeout_ticks must be a positive integer")
        self.focus = focus
        self.area = area
        self.target = target
        self.timeout_ticks = timeout_ticks
        self.state = "idle"
        self.reason = None
        self.active_request = None
        self._remaining = None
        self._next_id = 1
        self._held = False
        self._shutdown = False
        self._trace = []
        self._reset()

    @property
    def trace(self):
        return tuple(self._trace)

    def _eligibility_reason(self):
        if self._shutdown:
            return "shutdown"
        if self.focus not in ELIGIBLE_FOCUS:
            return "unsupported-focus"
        if self.area not in ELIGIBLE_AREAS:
            return "unsupported-area"
        if not _valid_target(self.target):
            return "invalid-target"
        return None

    def _reset(self, reason=None):
        self.active_request = None
        self._remaining = None
        unavailable = self._eligibility_reason()
        self.state = "unavailable" if unavailable else "idle"
        self.reason = unavailable or reason

    def _record(self, event, emitted=()):
        self._trace.append(Transition(event, self.state, self.reason, self.active_request, emitted))
        return emitted

    def press(self):
        if self._held:
            return self._record("repeat")
        self._held = True
        if self.state != "idle":
            return self._record("press-ignored")
        self._reset()
        if self.state == "unavailable":
            return self._record("press-unavailable")
        request = AcquisitionRequest(self._next_id, self.target)
        self._next_id += 1
        self.active_request = request.request_id
        self._remaining = self.timeout_ticks
        self.state = "acquiring"
        return self._record("press", (request,))

    def release(self):
        self._held = False
        return self._record("release")

    def acknowledge(self, request_id, *, success):
        if type(success) is not bool:
            raise ValueError("success must be a boolean")
        if (
            type(request_id) is not int
            or self.state != "acquiring"
            or request_id != self.active_request
        ):
            return self._record("ack-ignored")
        if success:
            self.state = "tracking"
            self.reason = None
            self._remaining = None
        else:
            self._reset("acquisition-failed")
        return self._record("ack-success" if success else "ack-failure")

    def advance(self, ticks=1):
        if type(ticks) is not int or ticks < 0:
            raise ValueError("ticks must be a nonnegative integer")
        if self.state == "acquiring":
            self._remaining -= ticks
            if self._remaining <= 0:
                self._reset("timeout")
        return self._record("advance")

    def cancel(self):
        self._reset("cancelled")
        return self._record("cancel")

    def configure(self, *, focus, area, target):
        """Invalidate the session, even when supplied settings are unchanged."""
        self.focus = focus
        self.area = area
        self.target = target
        self._reset("configuration-changed")
        return self._record("configure")

    def shutdown(self):
        self._shutdown = True
        self._reset()
        return self._record("shutdown")
