#!/bin/sh
# The gate. Everything this repo claims about itself, checked in one command.
#
#   ./tools/gate.sh
#
# Same idea as power-service-toolbox/tools/gate.sh: a rule that lives only in a README is a wish.
# The rules are different here because the risk is different. That repo can ship a wrong number.
# This one can ship a wrong FACT, or somebody else's copyrighted PDF.
#
# THIS GATE IS OFFLINE AND FAST ON PURPOSE. Link checking lives in tools/check_links.py and is not
# run here. A gate that needs the network gives different answers on different wifi, and a check
# that flakes is a check that gets bypassed with --no-verify, and a gate with a habitual bypass is
# worse than no gate at all: everyone still believes the repo is checked.
#
# Three checks:
#   1. catalog  - no row claims more than it earned. Legal clearances are real licenses.
#   2. mirrors  - nothing published that is not cleared, and the file is the file the row names.
#   3. indexes  - every rendered index matches the catalog.
#                 (The toolbox README said "no tool is live yet" after 01 went live. A copy rots.)
#
# Incomplete rows do NOT fail this gate. Incorrect rows do. See tools/check_catalog.py for why that
# split is the whole design.
set -u
cd "$(dirname "$0")/.." || exit 2
fail=0

echo "GATE"
echo ""

echo "[1/3] catalog"
python3 tools/check_catalog.py || fail=1

echo ""
echo "[2/3] mirrors (copyright boundary)"
python3 tools/check_mirrors.py || fail=1

echo ""
echo "[3/3] indexes match the catalog"
python3 tools/build_indexes.py --check || fail=1

echo ""
if [ "$fail" -ne 0 ]; then
  echo "GATE FAILED. Do not ship."
  exit 1
fi
echo "GATE PASSED."
echo ""
echo "Not checked here, run it separately and on a schedule:"
echo "  ./tools/check_links.py    which canonical URLs have rotted, which rows are unsnapshotted"
echo "  ./tools/archive.py        snapshot the exposed ones before the vendor deletes them"
