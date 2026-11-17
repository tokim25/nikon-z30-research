#!/bin/sh
# Build the auto-arm dry-run kit on the owner's Mac: upstream PR #36 research
# firmware (EG209020.BIN) plus this module as Z30/CORE.ZMOD. Nothing here
# touches a camera or an SD card.
#
# Usage: prepare_mac.sh /path/to/Z_30_0120.bin [WORK_DIR] [--remap] [--diag] [--direct]
#   WORK_DIR defaults to ~/z30-auto-arm. Firmware and outputs stay there,
#   outside this repository. --remap builds the version that presses OK;
#   the default is the dry run, which presses nothing. --diag adds a state
#   sample about once a second to the log (see auto_arm.c). --direct (implies
#   --remap) calls the stock enter-tracking-mode function instead of pressing OK.
set -eu

PR_MIN=8715c25
STOCK_SHA=1a5449ef505f1f347ed4e066a6a3f588ea542240680e83f4ebcae3b16da3434a
STOCK_SIZE=34496798
UPSTREAM=https://github.com/WonderLantern/wonder-lantern-z30

here=$(cd "$(dirname "$0")" && pwd)
[ $# -ge 1 ] || { echo "usage: $0 /path/to/Z_30_0120.bin [WORK_DIR] [--remap] [--diag] [--direct]" >&2; exit 2; }
firmware=$(cd "$(dirname "$1")" && pwd)/$(basename "$1"); shift
work=$HOME/z30-auto-arm
remap=
diag=
direct=
for arg in "$@"; do
  case $arg in
    --remap) remap=-DREMAP ;;
    --diag) diag=-DDIAG ;;
    --direct) remap=-DREMAP; direct=-DDIRECT ;;
    *) work=$arg ;;
  esac
done

step() { printf '\n== %s\n' "$*"; }

step "Checking the stock firmware"
[ -f "$firmware" ] || { echo "not found: $firmware" >&2; exit 1; }
size=$(wc -c < "$firmware" | tr -d ' ')
sha=$(shasum -a 256 "$firmware" | cut -d' ' -f1)
[ "$size" = "$STOCK_SIZE" ] && [ "$sha" = "$STOCK_SHA" ] || {
  echo "not the unmodified Z30 C 1.20 firmware (size $size, sha256 $sha)" >&2; exit 1; }
echo "ok: Z_30_0120.bin, C 1.20"

step "Checking tools"
command -v arm-none-eabi-gcc >/dev/null || {
  echo "arm-none-eabi-gcc missing: brew install --cask gcc-arm-embedded" >&2; exit 1; }
arm-none-eabi-gcc --version | head -1
python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))' || {
  echo "Python 3.10 or newer is required" >&2; exit 1; }
python3 --version

step "Fetching upstream PR #36 into $work/wonder-lantern-z30"
mkdir -p "$work"
up=$work/wonder-lantern-z30
[ -d "$up/.git" ] || git clone -q "$UPSTREAM" "$up"
git -C "$up" fetch -q origin pull/36/head
git -C "$up" checkout -q --detach FETCH_HEAD
git -C "$up" merge-base --is-ancestor "$PR_MIN" HEAD 2>/dev/null || {
  echo "PR #36 head does not contain $PR_MIN; stop and check the PR" >&2; exit 1; }
git -C "$up" log -1 --format='using %h %cs %s'

step "Installing upstream's Python dependencies (venv in $work/venv)"
[ -d "$work/venv" ] || python3 -m venv "$work/venv"
"$work/venv/bin/pip" install -q --upgrade pip
(cd "$up" && "$work/venv/bin/pip" install -q '.[sound,verify]')
py=$work/venv/bin/python

step "Running upstream's unit tests"
(cd "$up" && PYTHONPATH=src "$py" -m unittest discover -s tests 2>&1 | tail -3)

out=$work/OUT
step "Building the research firmware into $out"
if [ -e "$out/EG209020.BIN" ]; then
  echo "kept the existing $out/EG209020.BIN (move OUT away to rebuild it)"
else
  (cd "$up" && "$py" tools/build_af_log.py --source "$firmware" --output "$out" --no-zmod)
fi

step "Building the auto-arm module (${remap:-dry run}${direct:+, direct call}${diag:+, diagnostic})"
sh "$here/build.sh" "$work/auto_arm.bin" $remap $direct $diag
mkdir -p "$out/Z30"
rm -f "$out/Z30/CORE.ZMOD"
(cd "$up" && "$py" tools/prepare_module.py --code "$work/auto_arm.bin" --output "$out/Z30/CORE.ZMOD")

step "Done"
shasum -a 256 "$out/EG209020.BIN" "$out/Z30/CORE.ZMOD"
cat <<EOF

Copy to the root of a card formatted in the camera:
  $out/EG209020.BIN
  $out/Z30/            (the folder, with CORE.ZMOD inside)
Then follow "On the camera" in docs/auto-arm-handoff.md.
Keep $firmware: it is how you go back to stock firmware.
EOF
