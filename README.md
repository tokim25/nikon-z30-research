# Nikon Z30 research

An offline Python research scaffold for documenting reproducible methods and testing them with synthetic data. This is newly created work: prior milestone files have not been recovered, and this repository does not represent their recovery.

## Boundaries

- Keep the repository private by default.
- Never publish Nikon firmware, extracted firmware bytes, memory dumps, installable patches, credentials, or proprietary artifacts, including through issues, logs, releases, or attachments.
- Never flash hardware. Analysis runs offline; GitHub is used only for approved project administration and publishing the research scaffold.
- Use synthetic fixtures and publish methods, independently written code, and reviewed findings only.

## Development

Use Python 3.11 or newer; CI tests Python 3.11, 3.12, and 3.13. Package metadata permits Python 3.10, but it is outside the current CI baseline. Python modules live under `src/`; tests live under `tests/` and use the standard library `unittest` framework.

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
python .github/scripts/check_artifacts.py
```

The artifact check examines tracked files, so stage intended changes before running it locally. Passing checks does not establish that content is safe to publish: review every staged change for embedded firmware bytes and sensitive material.

## Command-line examples

Keep firmware inputs outside this repository. These commands report file metadata or compare it with supplied expectations without decoding or modifying the input:

```sh
PYTHONPATH=src python3 -m nikon_z30_research report /path/to/firmware.bin
PYTHONPATH=src python3 -m nikon_z30_research verify /path/to/firmware.bin --sha256 FULL_64_CHARACTER_HASH --size 34496798
PYTHONPATH=src python3 -m nikon_z30_research crop 3840 2160
```

Replace `FULL_64_CHARACTER_HASH` with the complete expected SHA-256 hexadecimal digest. A matching digest and size establish identity against those expectations, not authenticity or hardware compatibility.

The crop command computes basic centered geometry at an exact integer 65:24 ratio. It may trim width as well as height: 3840 × 2160 yields 3835 × 1416. It does not render a live overlay, modify an image, or change camera behavior.

See [the workflow](docs/workflow.md) for integration, publication, and Codex session rules, and [the roadmap](docs/roadmap.md) for proposed work.
