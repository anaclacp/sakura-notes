"""Parse the source document without treating headings in code as entries."""

import argparse
from html import escape
import json
from pathlib import Path
import re

from markdown_it import MarkdownIt


def slugify(text):
    return re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")


def parser():
    md = MarkdownIt("commonmark", {"html": False, "breaks": False})

    def fence(tokens, index, options, env):
        code = escape(tokens[index].content.rstrip("\n"))
        return f'<pre class="code-block"><code>{code}</code></pre>\n'

    md.renderer.rules["fence"] = fence
    md.renderer.rules["code_block"] = fence
    md.renderer.rules["softbreak"] = lambda *args: " "
    return md


def parse_glossary(content):
    md = parser()
    tokens = md.parse(content.replace("\r\n", "\n"))
    letters, distinctions, seen = [], [], set()
    section = None
    current = None
    body = []

    def finish():
        nonlocal current, body
        if current is None:
            return
        while body and body[-1].type == "hr":
            body.pop()
        if not body:
            raise ValueError(f"Empty definition: {current['term']}")
        current["html"] = md.renderer.render(body, md.options, {}).strip()
        if section == "Key Distinctions":
            distinctions.append(current)
        else:
            letters[-1]["terms"].append(current)
        current, body = None, []

    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.type == "heading_open" and token.level == 0 and token.tag in ("h1", "h2", "h3"):
            name = tokens[index + 1].content.strip()
            if token.tag in ("h1", "h2"):
                finish()
                if token.tag == "h1" or name == "Index":
                    section = None
                elif re.fullmatch("[A-Z]", name):
                    if any(group["letter"] == name for group in letters):
                        raise ValueError(f"Duplicate letter: {name}")
                    section = name
                    letters.append({"letter": name, "terms": []})
                elif name == "Key Distinctions":
                    section = name
                else:
                    raise ValueError(f"Unsupported glossary section: {name}")
            elif section is not None:
                finish()
                anchor = slugify(name)
                if not anchor or anchor in seen or anchor.startswith("letter-"):
                    raise ValueError(f"Empty, duplicate or reserved anchor: {name}")
                if section != "Key Distinctions" and name[0].upper() != section:
                    raise ValueError(f"{name} is in the wrong letter section: {section}")
                seen.add(anchor)
                current = {"term": name, "anchor": anchor}
            index += 3
            continue
        if current is not None:
            body.append(token)
        index += 1
    finish()
    if not letters or not any(group["terms"] for group in letters):
        raise ValueError("The glossary has no terms")
    if any(not group["terms"] for group in letters):
        raise ValueError("Empty letter section")
    letters.sort(key=lambda group: group["letter"])
    return {"letters": letters, "key_distinctions": distinctions}


def entries(data):
    return [term for group in data["letters"] for term in group["terms"]] + data["key_distinctions"]


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("source", type=Path, nargs="?", default=Path("content/glossary.md"))
    args.add_argument("--output", type=Path, default=Path("glossary_data.json"))
    options = args.parse_args()
    data = parse_glossary(options.source.read_text(encoding="utf-8-sig"))
    options.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Parsed {len(entries(data))} definitions")
