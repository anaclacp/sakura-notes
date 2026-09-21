"""Keep reviewed translations; translate only definitions whose source changed."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

from bs4 import BeautifulSoup

from parse_glossary import entries, parse_glossary

ROOT = Path(__file__).resolve().parent
MODEL_VERSION = "1.9"


def source_hash(term):
    payload = json.dumps({"term": term["term"], "html": term["html"]}, sort_keys=True, ensure_ascii=True)
    return sha256(payload.encode()).hexdigest()


def validate_translation(value):
    if not isinstance(value, dict) or not all(isinstance(value.get(key), str) and value[key].strip() for key in ("term", "html")):
        raise ValueError("Translation requires a nonempty name and HTML body")
    soup = BeautifulSoup(value["html"], "html.parser")
    allowed = {"p", "ul", "ol", "li", "strong", "em", "code", "pre", "blockquote", "br", "a", "hr", "h4", "h5", "h6", "img"}
    for tag in soup.find_all(True):
        if tag.name not in allowed:
            raise ValueError(f"Unsafe translation element: {tag.name}")
        for attribute, value in tag.attrs.items():
            if attribute not in {"class", "href", "src", "alt", "title", "start"}:
                raise ValueError(f"Unsafe translation attribute: {attribute}")
            if attribute in {"href", "src"}:
                from urllib.parse import urlsplit
                scheme = urlsplit(str(value).strip()).scheme.lower()
                if scheme not in {"", "http", "https", "mailto"}:
                    raise ValueError("Unsafe translation URL")
    if not soup.get_text(strip=True):
        raise ValueError("Empty translated body")


class ArgosTranslator:
    def __init__(self):
        from argostranslate import package, translate

        installed = package.get_installed_packages()
        if not any(p.from_code == "en" and p.to_code == "pt" and p.package_version == MODEL_VERSION for p in installed):
            package.update_package_index()
            candidates = [p for p in package.get_available_packages() if p.from_code == "en" and p.to_code == "pt" and p.package_version == MODEL_VERSION]
            if not candidates:
                raise RuntimeError("Pinned English-Portuguese translation model is unavailable")
            package.install_from_path(candidates[0].download())
        self.translation = translate.get_translation_from_codes("en", "pt")

    def __call__(self, term):
        from translatehtml import translate_html

        result = {"term": self.translation.translate(term["term"]), "html": str(translate_html(self.translation, term["html"]))}
        source = BeautifulSoup(term["html"], "html.parser")
        target = BeautifulSoup(result["html"], "html.parser")
        if [(t.name, t.attrs) for t in source.find_all(True)] != [(t.name, t.attrs) for t in target.find_all(True)]:
            raise ValueError(f"Translation changed markup: {term['anchor']}")
        if [t.get_text() for t in source.find_all("code")] != [t.get_text() for t in target.find_all("code")]:
            raise ValueError(f"Translation changed code: {term['anchor']}")
        return result


def synchronize(data, translations, state, translator):
    updated, metadata = {}, {}
    changed = []
    for term in entries(data):
        anchor, digest = term["anchor"], source_hash(term)
        if anchor in translations and state.get(anchor, {}).get("source_sha256") == digest:
            value = translations[anchor]
            metadata[anchor] = state[anchor]
        else:
            value = translator(term)
            metadata[anchor] = {"source_sha256": digest, "method": f"argos-en-pt-{MODEL_VERSION}"}
            changed.append(anchor)
        validate_translation(value)
        updated[anchor] = value
    return updated, metadata, changed


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Report missing/outdated translations without downloading a model")
    parser.add_argument("--seed-reviewed", type=Path, help="One-time migration from the reviewed English export")
    args = parser.parse_args()
    data = parse_glossary((ROOT / "content/glossary.md").read_text(encoding="utf-8-sig"))
    translations = json.loads((ROOT / "glossary_pt-BR.json").read_text(encoding="utf-8"))
    state_path = ROOT / "translation_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    if args.seed_reviewed:
        if state:
            raise ValueError("Reviewed migration is only allowed with an empty state")
        original = {term["anchor"]: term for term in entries(json.loads(args.seed_reviewed.read_text(encoding="utf-8")))}
        for term in entries(data):
            old = original[term["anchor"]]
            def words(html):
                return " ".join(BeautifulSoup(html, "html.parser").get_text(" ").split())
            if old["term"] != term["term"] or words(old["html"]) != words(term["html"]):
                raise ValueError(f"Reviewed source mismatch: {term['anchor']}")
            validate_translation(translations[term["anchor"]])
            state[term["anchor"]] = {"source_sha256": source_hash(term), "method": "reviewed"}
        write_json(state_path, state)
        print(f"Seeded {len(state)} reviewed translations")
        return
    pending = [t for t in entries(data) if t["anchor"] not in translations or state.get(t["anchor"], {}).get("source_sha256") != source_hash(t)]
    if args.check:
        import os
        if os.environ.get("GITHUB_OUTPUT"):
            with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
                output.write(f"pending={len(pending)}\n")
        print(f"{len(pending)} translations need updating")
        return
    translator = ArgosTranslator() if pending else None
    updated, metadata, changed = synchronize(data, translations, state, translator)
    # Nothing is written until every translation has passed validation.
    write_json(ROOT / "glossary_pt-BR.json", updated)
    write_json(state_path, metadata)
    write_json(ROOT / "glossary_data.json", data)
    print(f"Updated {len(changed)} translations; {len(updated)} total")


if __name__ == "__main__":
    main()
