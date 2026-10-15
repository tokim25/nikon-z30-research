import unittest

from nikon_z30_research.tracking import AcquisitionRequest, TrackingModel


class TrackingTests(unittest.TestCase):
    def model(self, **settings):
        return TrackingModel(**{"target": (0.25, 0.75), **settings})

    def test_each_eligible_configuration_emits_one_target_request(self):
        for focus in ("AF-S", "AF-C", "AF-A"):
            for area in ("auto-area", "auto-area-people", "auto-area-animals"):
                with self.subTest(focus=focus, area=area):
                    model = self.model(focus=focus, area=area)
                    self.assertEqual(model.press(), (AcquisitionRequest(1, (0.25, 0.75)),))
                    self.assertEqual(model.state, "acquiring")
                    self.assertEqual(model.press(), ())
                    self.assertEqual(model.release(), ())
                    self.assertEqual(model.press(), ())
                    self.assertEqual(sum(len(entry.emitted) for entry in model.trace), 1)

    def test_success_trace_and_release_do_not_stop_button_tracking(self):
        model = self.model()
        request, = model.press()
        self.assertEqual(model.acknowledge(request.request_id, success=True), ())
        model.release()
        model.advance(100)
        model.press()
        self.assertEqual(model.state, "tracking")
        self.assertEqual(
            [(entry.event, entry.state) for entry in model.trace],
            [("press", "acquiring"), ("ack-success", "tracking"),
             ("release", "tracking"), ("advance", "tracking"),
             ("press-ignored", "tracking")],
        )
        self.assertTrue(all(isinstance(request, AcquisitionRequest)
                            for entry in model.trace for request in entry.emitted))

    def test_failure_requires_fresh_edge_and_retry_has_new_id(self):
        model = self.model()
        request, = model.press()
        model.acknowledge(request.request_id, success=False)
        self.assertEqual((model.state, model.reason), ("idle", "acquisition-failed"))
        self.assertEqual(model.press(), ())
        model.release()
        retry, = model.press()
        self.assertGreater(retry.request_id, request.request_id)
        model.acknowledge(request.request_id, success=True)
        self.assertEqual(model.state, "acquiring")
        model.acknowledge(retry.request_id, success=True)
        self.assertEqual(model.state, "tracking")

    def test_timeout_boundary_and_late_success(self):
        model = self.model(timeout_ticks=3)
        request, = model.press()
        model.advance(0)
        model.advance(2)
        self.assertEqual(model.state, "acquiring")
        model.advance(1)
        self.assertEqual((model.state, model.reason), ("idle", "timeout"))
        model.acknowledge(request.request_id, success=True)
        self.assertEqual(model.state, "idle")

    def test_mismatched_and_duplicate_acknowledgements(self):
        model = self.model()
        request, = model.press()
        for invalid in (0, 99, True, 1.0, "1", None):
            model.acknowledge(invalid, success=True)
            self.assertEqual(model.state, "acquiring")
        model.acknowledge(request.request_id, success=True)
        model.acknowledge(request.request_id, success=False)
        self.assertEqual(model.state, "tracking")

    def test_ineligible_inputs_expose_reason_without_requests(self):
        cases = [({"focus": "MF"}, "unsupported-focus"),
                 ({"focus": "AF-F"}, "unsupported-focus"),
                 ({"area": "single-point"}, "unsupported-area")]
        for target in (None, (), (0.5,), (0, 0, 0), (-0.1, 0), (0, 1.1),
                       (float("nan"), 0), (float("inf"), 0), (True, 0),
                       ("0", 0), [0, 0]):
            cases.append(({"target": target}, "invalid-target"))
        for settings, reason in cases:
            with self.subTest(settings=settings):
                model = self.model(**settings)
                self.assertEqual(model.press(), ())
                self.assertEqual((model.state, model.reason), ("unavailable", reason))

    def test_cancel_configure_shutdown_invalidate_sessions(self):
        for state in ("acquiring", "tracking"):
            for action in ("cancel", "configure", "shutdown"):
                with self.subTest(state=state, action=action):
                    model = self.model()
                    request, = model.press()
                    if state == "tracking":
                        model.acknowledge(request.request_id, success=True)
                    if action == "configure":
                        model.configure(focus="MF", area="auto-area", target=(0, 0))
                    else:
                        getattr(model, action)()
                    expected = "idle" if action == "cancel" else "unavailable"
                    self.assertEqual(model.state, expected)
                    self.assertIsNone(model.active_request)
                    model.acknowledge(request.request_id, success=True)
                    self.assertEqual(model.state, expected)
                    self.assertEqual(model.press(), ())

    def test_configuration_recovery_and_shutdown_is_terminal(self):
        model = self.model(focus="MF")
        model.configure(focus="AF-C", area="auto-area", target=(1, 0))
        original, = model.press()
        model.configure(focus="AF-S", area="auto-area-people", target=(0, 1))
        model.release()
        replacement, = model.press()
        model.acknowledge(original.request_id, success=True)
        self.assertEqual(model.active_request, replacement.request_id)
        self.assertEqual(model.state, "acquiring")
        model.shutdown()
        model.configure(focus="AF-C", area="auto-area", target=(0, 0))
        model.release()
        self.assertEqual(model.press(), ())
        self.assertEqual((model.state, model.reason), ("unavailable", "shutdown"))

    def test_cancel_repress_and_invalid_clock_inputs(self):
        model = self.model()
        model.press()
        model.cancel()
        model.release()
        self.assertEqual(model.press()[0].request_id, 2)
        for invalid in (-1, True, 1.5, "1"):
            with self.assertRaises(ValueError):
                model.advance(invalid)
        for invalid in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                self.model(timeout_ticks=invalid)
        with self.assertRaises(ValueError):
            model.acknowledge(2, success="yes")


class NikonHalfPressBaselineTests(unittest.TestCase):
    """Documentation fixtures, not executable Nikon behavior or model policy."""

    def test_photo_half_press_release_fixture_is_separate(self):
        baseline = {
            "AF-C": ("tracking", "half-press-release", "ended", "previous-point"),
            "AF-A": ("tracking", "half-press-release", "ended", "previous-point"),
        }
        for focus, documented_trace in baseline.items():
            with self.subTest(focus=focus):
                self.assertEqual(documented_trace[2:], ("ended", "previous-point"))
                model = TrackingModel(focus=focus, target=(0.5, 0.5))
                request, = model.press()
                model.acknowledge(request.request_id, success=True)
                model.release()
                self.assertEqual(model.state, "tracking")


if __name__ == "__main__":
    unittest.main()
