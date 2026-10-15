# MMIO sampler caller and peripheral attribution

Reviewed 2026-10-15. Static analysis and public-source comparison only.

The sampling lead from [PR #13](https://github.com/tokim25/nikon-z30-research/pull/13)
now has a caller and a callback registration path. The register pattern strongly
suggests HDMI connection status. That attribution is inference, not a measured
Nikon peripheral identity. Deprioritize these samplers as a subject-tracking
input lead: no evidence connects them to a camera button, reticle or AF action.

## Caller and output consumer

The unchanged verified C1.20 module was read at mapping base `0x10020000`.
SHA-256 remained
`8a99ced2d8220729ba067587b0624bf30c81757abc5d728768134b1c7fd457fa`.
Analysis used Capstone 5.0.6 in Thumb mode. The following are semantic summaries
of bounded static decode; raw listings remain outside this checkout.

| Landmark | Observed static structure | Interpretation and limit |
| --- | --- | --- |
| Candidate routine `0x1028afee`, call at `0x1028b040` | Supplies its stack as the second argument to `0x1029d8aa`, then reads the destination byte and normalizes it to zero or one. | A consumer of the bit-1 sampler, not a tracking-start call. High confidence in the bounded call and data flow. |
| `0x1028b04e`–`0x1028b06e` | Compares the sample with state at `0xc1807ed4`. Differences increment a counter at `0xc1807ef4`; equal samples reset it. A differing sample is accepted only when the unsigned counter exceeds the cached threshold. | Debounce-like filtering is static inference, high confidence. Threshold and pacing values are loaded from configuration; no camera timing is established. |
| `0x1028b06e`–`0x1028b0b2` | Calls intervening helpers on selected paths, normalizes a final state at `0xc1807edc`, compares its previous value and checks a callback slot at `0xc1807ecc`. A changed final state can reach an indirect call at `0x1028b0b2`. | Conditional state notification is inference. The helpers can filter or clear state; a sampled change does not guarantee a callback. |
| Setter `0x1028b134`; caller `0x10396f98` | The setter stores its argument at `0xc1807ecc`. The caller supplies Thumb pointer `0x10396cdf`, corresponding to code at `0x10396cde`. | A statically connected registration path. Initialization, later overwrites and runtime invocation are unverified. |
| Callback `0x10396cde`–`0x10396d06` | Requires first argument 1, calls a helper with size 28, checks the returned pointer, and writes identifier `0x4206101e` plus the incoming payload pointer into a record. The successful path continues through `0x10396cc6`. | Allocation-like and notification behavior are inference. The helper contracts, record ownership and delivery are unresolved. This identifier is not a verified tracking event. |

A scan for 32-bit Thumb BL, B.W and immediate BLX patterns at halfword positions
over `0x10020000`–`0x11f81c94` found the call at
`0x1028b040` to the first sampler. It found no direct branch candidate to
`0x1029d8ea`; whole-module word searches found no exact even or Thumb-pointer
occurrence for either sampler address. These negative results do not prove
that other callers are absent. Mixed code/data, indirect dispatch, constructed
addresses, omitted narrow/conditional branches and incomplete function recovery
limit the scan. The bounded caller
window and registration path were inspected separately from the scan matches.

## Peripheral inference

Using proposed base `0x20160000` and spacing four, several simulator register
addresses match [Linux v6.12 DesignWare HDMI definitions](https://github.com/torvalds/linux/blob/v6.12/drivers/gpu/drm/bridge/synopsys/dw-hdmi.h#L350-L378):

| Simulator address | Register offset | Corresponding public definition |
| --- | --- | --- |
| `0x2016c010` | `0x3004` | PHY status |
| `0x2016c018` | `0x3006` | PHY interrupt mask |
| `0x2016c0a4` | `0x3029` | PHY I2C divider |
| `0x2016c0a8` | `0x302a` | PHY I2C soft reset |
| `0x2016c0ac`–`0x2016c0c8` | `0x302b`–`0x3032` | PHY I2C timing registers |

The same header [defines status bit 1 as hot-plug detect and bits 4–7 as
receiver-sense signals](https://github.com/torvalds/linux/blob/v6.12/drivers/gpu/drm/bridge/synopsys/dw-hdmi.h#L844-L850),
matching the previously observed sampled fields. This multi-register agreement
supports HDMI attribution with high confidence as an inference. It does not
establish the Nikon integration, access-width requirements or runtime behavior.

Local source provenance is
[the pinned simulator register table](https://github.com/WonderLantern/z30-qemu/blob/0ba0c3547ccbec09e7c861eaca35db8e82795f15/qemu/nikon-z30-display.c#L2979-L2996).
Its comment labels `0x2016c0a8` as a zero-error polling value, which conflicts
with the soft-reset analogy. Do not use that comment as a register-name proof.
The simulator's all-low status response remains an unmeasured startup hypothesis.

## Reproduce privately

The owner-confirmed WORK directory contains the newly written verifier and
verified module. Use a fresh `codex-` output name; the command refuses to replace
an existing directory. No firmware instructions are modified or executed.

```sh
WORK=/Users/tonykim/Documents/Codex/2026-10-15/referenced-chatgpt-conversation-this-is-an/work
"$WORK/analysis-env/bin/python" "$WORK/codex_sampler_consumer_verify_private.py" \
  --output "$WORK/private-inputs/codex-sampler-consumer-review-01"
```

To repeat the branch-candidate scan and bounded caller inspection:

```sh
"$WORK/analysis-env/bin/python" "$WORK/codex_tracking_static_private.py" \
  --output "$WORK/private-inputs/codex-sampler-callers-review-01" \
  --target 0x1029d8aa --target 0x1029d8ea --window 0x1028afee:0xe2
```

The verifier passed in `private-inputs/codex-sampler-consumer-verified-01`.
The simulator stayed clean at revision
`0ba0c3547ccbec09e7c861eaca35db8e82795f15`. A Codex subagent independently
checked the caller and callback summaries. These commands depend on private
files and are not CI evidence. Keep all raw output outside the repository.

## Single next step

Trace registration and callers of the known menu dispatcher `0x103ce96e` back
to its shared event router, then check for a separate live-view branch. Treat
every result as menu-only until a live-view connection is demonstrated. Do not
invoke the dispatcher as a substitute for native live-view input.

Written by Codex in collaboration with Tony Kim, with independent Codex subagent review.
