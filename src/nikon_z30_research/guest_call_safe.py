"""Thread-aware diagnostic call for the simulator's debugger connection.

The simulator tools' own call helper treats the first stop reply after a resume
as the end of the call. When the other virtual CPU stops for any unrelated
reason mid-call, that misreads the stop as completion, leaves the diverted
thread's registers unrestored, and can strand a lock. This helper resumes on
every stop except the diverted thread reaching the return sentinel. It only
talks to a debugger connection object; it knows nothing about firmware bytes.
"""

import socket
import struct
import time

DEFAULT_SENTINEL = 0x100200AC
CONTEXT_BYTES = 68          # r0-r15, then cpsr, as negotiated with the simulator
THUMB_BIT = 0x20


def _thread_of(reply):
    return reply.split("thread:")[1].split(";")[0] if "thread:" in reply else None


def call(remote, packet, function, arguments, seconds=30, *,
         observe=(), capture=None, stack_pointer=None, sentinel=DEFAULT_SENTINEL):
    """Run `function` on the thread that produced `packet`, then restore it.

    `observe`/`capture` match the simulator tools' own helper: a stop at one
    of these addresses, on either thread, is recorded and stepped over
    rather than treated as completion. Unlike that helper, a stop elsewhere
    on the OTHER thread is resumed, not misread as completion. Returns
    (record, last_reply); record["completed"] is true only when the
    diverted thread itself reached the sentinel.
    """
    if len(arguments) > 4:
        raise ValueError("only register arguments are supported")
    thread = _thread_of(packet)
    assert remote.command("Hg" + thread) == "OK"
    saved = remote.command("g")
    registers = bytearray.fromhex(saved)
    if len(registers) != CONTEXT_BYTES:
        raise ValueError("unexpected register context size")
    for index, value in enumerate(arguments):
        struct.pack_into("<I", registers, index * 4, value)
    if stack_pointer is not None:
        struct.pack_into("<I", registers, 13 * 4, stack_pointer)
    struct.pack_into("<I", registers, 14 * 4, sentinel)
    struct.pack_into("<I", registers, 15 * 4, function & ~1)
    status = struct.unpack_from("<I", registers, 64)[0]
    struct.pack_into("<I", registers, 64, status | THUMB_BIT)
    assert remote.command(f"Z1,{sentinel:x},4") == "OK"
    for address in observe:
        assert remote.command(f"Z1,{address:x},2") == "OK"
    assert remote.command("G" + registers.hex()) == "OK"

    deadline = time.monotonic() + seconds
    ignored, completed, timed_out = 0, False, False
    observations = []
    last_reply, last_stop, after = packet, None, {}
    remote.send("c")
    while True:
        remote.sock.settimeout(max(0.05, deadline - time.monotonic()))
        try:
            reply = remote.receive()
        except (socket.timeout, TimeoutError):
            timed_out = True
            break
        last_reply = reply
        stopped = _thread_of(reply)
        if stopped is not None:
            remote.command("Hg" + stopped)
        after = remote.registers()
        pc = int(after["r15"], 16)
        last_stop = (stopped, pc)
        if stopped == thread and pc == sentinel:
            completed = True
            break

        if pc in observe and len(observations) < 256:
            item = {"pc": hex(pc), "thread": stopped, "registers": after}
            if capture:
                item.update(capture(remote, after))
            observations.append(item)
            assert remote.command(f"z1,{pc:x},2") == "OK"
            assert remote.command("Hc" + stopped) == "OK"
            remote.send("s")
            remote.sock.settimeout(5)
            remote.receive()
            assert remote.command(f"Z1,{pc:x},2") == "OK"
            assert remote.command("Hc-1") == "OK"
            remote.send("c")
            continue

        if stopped == thread:
            break   # diverted thread stopped somewhere unexpected; report it

        ignored += 1   # an unrelated stop on the other thread; just resume
        if time.monotonic() >= deadline:
            timed_out = True
            break
        remote.send("c")

    if timed_out:
        try:
            remote.sock.sendall(b"\x03")
        except OSError:
            pass
    for address in observe:
        remote.command(f"z1,{address:x},2")
    remote.command(f"z1,{sentinel:x},4")
    if completed:
        assert remote.command("Hg" + thread) == "OK"
        assert remote.command("G" + saved) == "OK"
    record = {
        "completed": completed,
        "context_restored": completed,
        "timed_out": timed_out,
        "ignored_stops": ignored,
        "last_stop": last_stop,
        "registers": after,
    }
    if observe:
        record["observations"] = observations
    return record, last_reply
