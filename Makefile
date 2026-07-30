CH ?=

blanks:  ; python3 tools/build_blanks.py
ledger:  ; python3 tools/build_ledger.py
check:   ; python3 tools/build_blanks.py --check && python3 tools/check_sync.py
session: ; @mkdir -p sessions/$(shell date +%F)-$(CH) && cp blanks/$(CH).ipynb sessions/$(shell date +%F)-$(CH)/

.PHONY: blanks ledger check session
