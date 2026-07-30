CH ?=

projector:  ; python3 tools/build_blanks.py --dst projector
ledger:  ; python3 tools/build_ledger.py
check:   ; python3 tools/build_blanks.py --dst projector --check && python3 tools/check_sync.py
session: ; @mkdir -p sessions/$(shell date +%F)-$(CH) && cp projector/$(CH).ipynb sessions/$(shell date +%F)-$(CH)/

.PHONY: projector ledger check session
