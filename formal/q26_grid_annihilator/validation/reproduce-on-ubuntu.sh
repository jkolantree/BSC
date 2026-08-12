#!/usr/bin/env bash
set -euo pipefail

# Run from the repository root on an Ubuntu host with git, curl, Python 3,
# Cargo/Rust 1.93.1, and a working systemd user manager.
SOURCE_PROJECT="${1:-formal/q26_grid_annihilator}"
RECEIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK="$(mktemp -d -t q26-lean-trust-XXXXXXXX)"
KEEP_WORK="${KEEP_WORK:-0}"
TOOLS="$WORK/tools"
SRC="$WORK/src"
BIN="$WORK/bin"
PROJECT="$WORK/project"
LOG="$WORK/log"
mkdir -p "$TOOLS" "$SRC" "$BIN" "$PROJECT" "$LOG"
printf 'work_dir=%s\n' "$WORK"

cleanup() {
  local status=$?
  if [[ "$KEEP_WORK" == "1" || "$status" -ne 0 ]]; then
    printf 'retained_work_dir=%s\n' "$WORK" >&2
  else
    chmod -R u+w "$WORK" 2>/dev/null || true
    rm -rf -- "$WORK"
  fi
  return "$status"
}
trap cleanup EXIT

export GOPATH="$WORK/go-path"
export GOMODCACHE="$WORK/go-mod-cache"
export GOCACHE="$WORK/go-build-cache"
mkdir -p "$GOPATH" "$GOMODCACHE" "$GOCACHE"

case "$(rustc --version)" in
  'rustc 1.93.1 (01f6ddf75 2026-02-11)'*) ;;
  *) echo 'Rust 1.93.1 (01f6ddf75) is required' >&2; exit 1 ;;
esac
case "$(cargo --version)" in
  'cargo 1.93.1 (083ac5135 2025-12-15)'*) ;;
  *) echo 'Cargo 1.93.1 (083ac5135) is required' >&2; exit 1 ;;
esac

curl -fsSL --retry 3 -o "$WORK/go.tar.gz" \
  https://go.dev/dl/go1.25.12.linux-amd64.tar.gz
printf '%s  %s\n' \
  234828b7a89e0e303d2556310ee549fbcf253d28de937bac3da13d6294262ac1 \
  "$WORK/go.tar.gz" | sha256sum -c -
tar -xzf "$WORK/go.tar.gz" -C "$TOOLS"

curl -fsSL --retry 3 -o "$WORK/lean.zip" \
  https://github.com/leanprover/lean4/releases/download/v4.32.2/lean-4.32.2-linux.zip
printf '%s  %s\n' \
  fb97c65730b22927951dadae964f06b2b0e6cfb2cc60f3abe26d8c99f27aa02b \
  "$WORK/lean.zip" | sha256sum -c -
python3 -m zipfile -e "$WORK/lean.zip" "$TOOLS"
chmod u+x "$TOOLS/lean-4.32.2-linux/bin/"*
export PATH="$TOOLS/lean-4.32.2-linux/bin:$BIN:/usr/bin:/bin"
test "$(lean --version)" = \
  'Lean (version 4.32.2, x86_64-unknown-linux-gnu, commit f3b06c705e6c85f5314019d5d3baab0fec5b580c, Release)'
test "$("$TOOLS/go/bin/go" version)" = 'go version go1.25.12 linux/amd64'

clone_at() {
  local url="$1" commit="$2" dest="$3"
  git clone -q --filter=blob:none --no-checkout "$url" "$dest"
  git -C "$dest" checkout -q --detach "$commit"
  test "$(git -C "$dest" rev-parse HEAD)" = "$commit"
}
clone_at https://github.com/zouuup/landrun.git \
  5ed4a3db3a4ad930d577215c6b9abaa19df7f99f "$SRC/landrun"
clone_at https://github.com/leanprover/lean4export.git \
  4e7915201d3f9f04470d9eae002fa695f7cdc589 "$SRC/lean4export"
clone_at https://github.com/leanprover/comparator.git \
  71b52ec29e06d4b7d882726553b1ceb99a2499e0 "$SRC/comparator"
clone_at https://github.com/robsimmons/nanoda_lib.git \
  68d5ca9db226849b41a6fff59d796ff19d0a8840 "$SRC/nanoda"
grep -F '("unpermitted_axiom_hard_error", true)' "$SRC/comparator/Main.lean"

(cd "$SRC/landrun" && "$TOOLS/go/bin/go" build -trimpath -o "$BIN/landrun" ./cmd/landrun)
# Rust otherwise incorporates the random work-root path into this binary.
# The epoch is the pinned nanoda commit timestamp; the remap makes independent
# mktemp roots produce byte-identical executables.
(cd "$SRC/nanoda" && SOURCE_DATE_EPOCH=1772642132 \
  RUSTFLAGS="--remap-path-prefix=$WORK=/q26-lean-trust" \
  CARGO_HOME="$WORK/cargo-home" CARGO_TARGET_DIR="$WORK/nanoda-target" \
  cargo build --release --locked)
cp "$WORK/nanoda-target/release/nanoda_bin" "$BIN/nanoda_bin"
(cd "$SRC/lean4export" && lake build lean4export)
cp "$SRC/lean4export/.lake/build/bin/lean4export" "$BIN/lean4export"
(cd "$SRC/comparator" && lake build comparator)
cp "$SRC/comparator/.lake/build/bin/comparator" "$BIN/comparator"
(
  cd "$BIN"
  printf '%s\n' \
    '7336cc5bee32dc4fd47755eb2cc19a846c63f7abc1484bd0594a39eb8a2811de  landrun' \
    'd5a4291fa53476cfd3de4ef225e4021bd82c4dee1731320c128585b098cc7db9  lean4export' \
    '67c9282dcda8bf769e0170adaf292d99620cf5efa7a27247853128d5755748d2  comparator' \
    'f1df9d253b030b068066b531906bcdae565a3adfe1a58fecf4982b981ff715ce  nanoda_bin' \
    | sha256sum -c -
)

cp -a "$SOURCE_PROJECT/Q26GridAnnihilator" "$PROJECT/"
cp "$SOURCE_PROJECT/Q26GridAnnihilator.lean" "$PROJECT/"
(cd "$PROJECT" && {
  find Q26GridAnnihilator -type f -name '*.lean' -print0 | sort -z | xargs -0 sha256sum
  sha256sum Q26GridAnnihilator.lean
}) > "$LOG/lean-source-projection-sha256.txt"
printf '%s  %s\n' \
  358f8fcdcea4ae5255f62cb399d57e9addafc8adc54e24f222ad3732a1c5b764 \
  "$LOG/lean-source-projection-sha256.txt" | sha256sum -c -
cmp "$LOG/lean-source-projection-sha256.txt" \
  "$RECEIPT_DIR/evidence/lean-source-projection-sha256.txt"

cp "$SOURCE_PROJECT/lakefile.toml" "$PROJECT/lakefile.toml"
cp "$SOURCE_PROJECT/lake-manifest.json" "$PROJECT/lake-manifest.json"
cp "$SOURCE_PROJECT/lean-toolchain" "$PROJECT/lean-toolchain"
cp "$RECEIPT_DIR/TrustedChallenge.lean" \
  "$PROJECT/Q26GridAnnihilator/TrustedChallenge.lean"
cp "$RECEIPT_DIR/comparator-config.json" "$PROJECT/comparator-config.json"
(cd "$PROJECT" && printf '%s\n' \
  '8e57b02d00ce5d59244edf91cdff5396ff44a692efba535a49caaffd9401514c  Q26GridAnnihilator/TrustedChallenge.lean' \
  '03aacc69c02f1a6edb56216de96aa2485f1e4adfd3c348cf7c1db6e4624c13b5  comparator-config.json' \
  '26c9b9c924728993040e43bebc56740e8e6dd3d9d65471072a47e3df6ccd9fea  lakefile.toml' \
  '9ffcadb0b01034ce2511c62c55ea324d34184150458c8478cd79c739f727836a  lake-manifest.json' \
  '2bdc48adfa58d0017e538a0ad117c5d73d35deec879978f909406a80c8037273  lean-toolchain' \
  | sha256sum -c -)

(cd "$PROJECT" && lake update && lake exe cache get)
test "$(git -C "$PROJECT/.lake/packages/mathlib" rev-parse HEAD)" = \
  905b95818eb32af7874a58b427f50c1711a5e96c

mkdir -p "$WORK/probe/.lake"
if "$BIN/landrun" --best-effort --ro / --rw /dev --ldd --add-exec \
    --env PATH --env HOME --rwx "$WORK/probe/.lake" \
    /usr/bin/touch "$WORK/probe/outside"; then
  echo 'landrun unexpectedly allowed an outside write' >&2
  exit 1
fi
"$BIN/landrun" --best-effort --ro / --rw /dev --ldd --add-exec \
  --env PATH --env HOME --rwx "$WORK/probe/.lake" \
  /usr/bin/touch "$WORK/probe/.lake/inside"
test -f "$WORK/probe/.lake/inside"
systemd-run --user --wait --pipe /usr/bin/true

timeout --signal=TERM --kill-after=30s 50m \
  systemd-run --user --wait --pipe --collect \
    --property=RuntimeMaxSec=49m \
    --property=RestrictAddressFamilies=~AF_UNIX \
    --setenv="PATH=$PATH" --setenv=LEAN_ABORT_ON_PANIC=1 \
    --working-directory="$PROJECT" \
    "$TOOLS/lean-4.32.2-linux/bin/lake" env "$BIN/comparator" comparator-config.json \
    2>&1 | tee "$LOG/comparator-q26.txt"
grep -Fx 'Nanoda kernel accepts the solution' "$LOG/comparator-q26.txt"
grep -Fx 'Lean default kernel accepts the solution' "$LOG/comparator-q26.txt"
grep -Fx 'Your solution is okay!' "$LOG/comparator-q26.txt"
sha256sum "$LOG/comparator-q26.txt"
