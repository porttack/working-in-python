CH ?=

projector:  ; python3 tools/build_blanks.py --dst projector
ledger:  ; python3 tools/build_ledger.py
check:   ; python3 tools/build_blanks.py --dst projector --check && python3 tools/check_sync.py
session: ; @mkdir -p sessions/$(shell date +%F)-$(CH) && cp projector/$(CH).ipynb sessions/$(shell date +%F)-$(CH)/

jupyterlite:       ; python3 tools/build_jupyterlite_content.py && jupyter lite build --contents jupyterlite/content --output-dir jupyterlite/_output
jupyterlite-serve: ; cd jupyterlite/_output && python3 -m http.server 8123

.PHONY: projector ledger check session jupyterlite jupyterlite-serve
