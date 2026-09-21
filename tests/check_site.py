"""Check the deploy artifact, not just the source JSON."""

import json
from pathlib import Path
import sys

from bs4 import BeautifulSoup

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
from parse_glossary import entries

data = json.loads((root / "glossary_data.json").read_text(encoding="utf-8"))
site = BeautifulSoup(Path(sys.argv[1]).read_text(encoding="utf-8"), "html.parser")
ids = [tag["id"] for tag in site.select("[id]")]
assert len(ids) == len(set(ids)), "Duplicate DOM IDs"
assert len(site.select(".term-card")) == len(entries(data)), "Missing definitions"
assert site.html["data-theme"] == "dark"
assert site.select_one(".sidebar #theme-toggle")
assert site.select_one(".sidebar .language-switch")
assert site.select_one(".sakura-art")["src"].startswith("data:image/png;base64,")
translations = json.loads(site.select_one("#translations").string)
assert set(translations["terms"]) == {term["anchor"] for term in entries(data)}
for term in entries(data):
    card = site.find(id=term["anchor"])
    assert card.h3.get_text(strip=True) == term["term"]
    expected = BeautifulSoup(term["html"], "html.parser").get_text()
    assert card.select_one(".term-body").get_text() == expected
print(f"Artifact verified: {len(entries(data))} bilingual definitions")
