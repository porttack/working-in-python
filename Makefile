CH ?=

projector:  ; python3 tools/build_blanks.py --dst projector
ledger:  ; python3 tools/build_ledger.py
glossary: ; python3 tools/build_vocabulary_glossary.py
check:   ; python3 tools/build_blanks.py --dst projector --check && python3 tools/check_sync.py && python3 tools/build_jupyterlite_content.py --check
session: ; @mkdir -p sessions/$(shell date +%F)-$(CH) && cp projector/$(CH).ipynb sessions/$(shell date +%F)-$(CH)/

jupyterlite:       ; rm -rf jupyterlite/_output .jupyterlite.doit.db && python3 tools/build_blanks.py --dst projector && python3 tools/build_jupyterlite_content.py && jupyter lite build --contents jupyterlite/content --output-dir jupyterlite/_output
jupyterlite-serve: ; cd jupyterlite/_output && python3 -m http.server 8123

.PHONY: projector ledger glossary check session jupyterlite jupyterlite-serve
