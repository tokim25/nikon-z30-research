"""Synthetic tests for the thread-aware call helper. No simulator needed."""

import socket
import struct
import unittest

from nikon_z30_research import guest_call_safe as safe

SENTINEL = safe.DEFAULT_SENTINEL


def context(pc=0, r0=0):
    registers = bytearray(safe.CONTEXT_BYTES)
    struct.pack_into("<I", registers, 0, r0)
    struct.pack_into("<I", registers, 15 * 4, pc)
    return registers.hex()


class FakeSocket:
    def settimeout(self, value):
        self.timeout = value

    def sendall(self, data):
        self.sent = data


class FakeRemote:
    """Replays scripted stop replies: (reply text, pc)."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.sock = FakeSocket()
        self.sent_commands, self.resumes = [], 0
        self.current_pc = 0

    def command(self, text):
        self.sent_commands.append(text)
        return context(pc=0x2000, r0=7) if text == "g" else "OK"

    def send(self, text):
        if text == "c":
            self.resumes += 1

    def receive(self):
        if not self.replies:
            raise socket.timeout()
        reply, self.current_pc = self.replies.pop(0)
        return reply

    def registers(self):
        return {"r15": hex(self.current_pc)}


class CallTests(unittest.TestCase):
    def run_call(self, replies, seconds=5, **kwargs):
        remote = FakeRemote(replies)
        record, _ = safe.call(remote, "T05thread:01;", 0x10477AF3, [1, 2], seconds, **kwargs)
        return remote, record

    def test_completes_when_diverted_thread_reaches_sentinel(self):
        remote, record = self.run_call([("T05thread:01;", SENTINEL)])
        self.assertTrue(record["completed"])
        self.assertTrue(record["context_restored"])
        self.assertEqual(record["ignored_stops"], 0)
        self.assertEqual(remote.sent_commands[-1], "G" + context(pc=0x2000, r0=7))

    def test_unrelated_stop_from_other_thread_is_resumed(self):
        remote, record = self.run_call(
            [("T02thread:02;", 0xC2B1065C), ("T05thread:01;", SENTINEL)])
        self.assertTrue(record["completed"])
        self.assertEqual(record["ignored_stops"], 1)
        self.assertEqual(remote.resumes, 2)

    def test_sentinel_reached_by_other_thread_is_not_completion(self):
        _, record = self.run_call(
            [("T05thread:02;", SENTINEL), ("T05thread:01;", SENTINEL)])
        self.assertTrue(record["completed"])
        self.assertEqual(record["ignored_stops"], 1)

    def test_timeout_does_not_restore_context(self):
        remote, record = self.run_call([("T02thread:02;", 0x1234)], seconds=0.2)
        self.assertFalse(record["completed"])
        self.assertTrue(record["timed_out"])
        writes = [c for c in remote.sent_commands if c.startswith("G")]
        self.assertEqual(len(writes), 1)   # the divert only; no restore
        self.assertEqual(remote.sock.sent, b"\x03")

    def test_too_many_arguments_rejected(self):
        with self.assertRaises(ValueError):
            safe.call(FakeRemote([]), "T05thread:01;", 0, [1, 2, 3, 4, 5])

    def test_observe_hit_on_other_thread_is_recorded_not_completion(self):
        watched = 0xC2B1065C
        _, record = self.run_call(
            [("T02thread:02;", watched), ("T05thread:00;", 0),
             ("T05thread:01;", SENTINEL)],
            observe=(watched,))
        self.assertTrue(record["completed"])
        self.assertEqual(len(record["observations"]), 1)
        self.assertEqual(record["observations"][0]["thread"], "02")
        self.assertEqual(record["observations"][0]["pc"], hex(watched))
        self.assertEqual(record["ignored_stops"], 0)

    def test_capture_receives_remote_and_registers(self):
        watched, seen = 0xC2B1065C, []
        self.run_call(
            [("T02thread:02;", watched), ("T05thread:00;", 0),
             ("T05thread:01;", SENTINEL)],
            observe=(watched,),
            capture=lambda remote, regs: seen.append(regs) or {})
        self.assertEqual(len(seen), 1)
        self.assertEqual(seen[0]["r15"], hex(watched))

    def test_unrelated_stop_still_resumed_with_observe_set(self):
        _, record = self.run_call(
            [("T02thread:02;", 0x9999), ("T05thread:01;", SENTINEL)],
            observe=(0xC2B1065C,))
        self.assertTrue(record["completed"])
        self.assertEqual(record["ignored_stops"], 1)
        self.assertEqual(record["observations"], [])


if __name__ == "__main__":
    unittest.main()
