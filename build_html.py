import argparse
import json
import base64
from hashlib import sha256
from html import escape
from pathlib import Path
from string import Template


ROOT = Path(__file__).resolve().parent
arguments = argparse.ArgumentParser()
arguments.add_argument("--output", type=Path, default=ROOT / "index.html")
output = arguments.parse_args().output


def embedded_asset(name, mime):
    encoded = base64.b64encode((ROOT / "assets" / name).read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


font_faces = "\n".join(
    f"@font-face {{ font-family: '{family}'; font-style: normal; font-weight: {weight}; font-display: swap; src: url('{embedded_asset(filename, 'font/ttf')}') format('truetype'); }}"
    for family, weight, filename in [
        ("Lora", 500, "lora-medium.ttf"),
        ("DM Sans", 400, "dm-sans-regular.ttf"),
        ("DM Sans", 600, "dm-sans-semibold.ttf"),
    ]
)
data = json.loads((ROOT / "glossary_data.json").read_text(encoding="utf-8"))
letters = data["letters"]
distinctions = data["key_distinctions"]
total = sum(len(group["terms"]) for group in letters)
portuguese = json.loads((ROOT / "glossary_pt-BR.json").read_text(encoding="utf-8"))
ui = json.loads((ROOT / "glossary_ui.json").read_text(encoding="utf-8"))
anchors = {term["anchor"] for group in letters for term in group["terms"]}
anchors.update(term["anchor"] for term in distinctions)
if anchors != set(portuguese):
    raise ValueError(f"Translation mismatch: missing={anchors - set(portuguese)}, extra={set(portuguese) - anchors}")
if set(ui["en-US"]) != set(ui["pt-BR"]):
    raise ValueError("UI translation keys must match")


def icon(name):
    paths = {
        "book": '<path d="M12 7v14m-9-3V3h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5v15h-5a4 4 0 0 0-4 3 4 4 0 0 0-4-3Z"/>',
        "flower": '<path d="M12 5a3 3 0 1 1 3 3m-3-3a3 3 0 1 0-3 3m3-3v1M9 8a3 3 0 1 0 3 3M9 8h1m5 0a3 3 0 1 1-3 3m3-3h-1m-2 3v-1"/><circle cx="12" cy="8" r="2"/><path d="M12 10v12M12 22c4.2 0 7-1.667 7-5-4.2 0-7 1.667-7 5ZM12 22c-4.2 0-7-1.667-7-5 4.2 0 7 1.667 7 5Z"/>',
        "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
        "close": '<path d="m18 6-12 12M6 6l12 12"/>',
        "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42"/>',
        "moon": '<path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6.25 6.25 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"/>',
        "arrow": '<path d="M7 17 17 7M7 7h10v10"/>',
        "compare": '<path d="M3 6h18M3 18h18m-4-4 4 4-4 4M7 2 3 6l4 4"/>',
        "link": '<path d="M10 13a5 5 0 0 0 7 .5l3-3a5 5 0 0 0-7-7l-1.7 1.7M14 11a5 5 0 0 0-7-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
    }
    return f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def term_row(term, number):
    name = escape(term["term"])
    anchor = escape(term["anchor"], quote=True)
    return f'''<article class="term-card" id="{anchor}">
      <div class="term-label"><span class="term-number">{number:02d}</span>
        <div class="term-heading"><h3 lang="en-US"><a href="#{anchor}" class="term-link">{name}<span class="anchor-icon">{icon("link")}</span></a></h3>
        <p class="term-translation" lang="pt-BR" hidden>{escape(portuguese[term['anchor']]['term'])}</p></div>
      </div>
      <div class="term-body">{term["html"]}</div>
    </article>'''


sections = []
number = 0
for group in letters:
    rows = []
    for term in group["terms"]:
        number += 1
        rows.append(term_row(term, number))
    letter = escape(group["letter"])
    count = len(rows)
    sections.append(f'''<section class="letter-section" id="letter-{letter}" data-letter="{letter}" aria-labelledby="heading-{letter}">
      <div class="section-heading"><h2 id="heading-{letter}">{letter}</h2><span class="section-count" data-count="{count}" data-unit="term">{count:02d} {"term" if count == 1 else "terms"}</span></div>
      {"".join(rows)}
    </section>''')

sections.append(f'''<section class="letter-section distinctions" id="letter-Key" data-letter="Key" aria-labelledby="heading-Key">
    <div class="section-heading"><h2 id="heading-Key" data-i18n="distinctions">Key distinctions</h2><span class="section-count" data-count="{len(distinctions)}" data-unit="note">{len(distinctions):02d} notes</span></div>
    {"".join(term_row(term, i + 1) for i, term in enumerate(distinctions))}
  </section>''')

available = {group["letter"] for group in letters}
nav = "".join(
    f'<a class="nav-letter" href="#letter-{letter}" data-letter="{letter}" aria-label="Letter {letter}">{letter}</a>'
    if letter in available else f'<span class="nav-letter unavailable" aria-hidden="true">{letter}</span>'
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)

template = Template('''<!DOCTYPE html>
<html lang="en-US" data-theme="dark">
<!-- $notices -->
<head>
  <meta charset="UTF-8">
  <meta name="glossary-source-sha256" content="$source_hash">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script>
    // Restore the saved theme before the first paint.
    try {
      const theme = localStorage.getItem('ai-glossary-theme');
      if (theme === 'light' || theme === 'dark') document.documentElement.dataset.theme = theme;
    } catch (_) { /* Keep the default when storage is unavailable. */ }
  </script>
  <title>AI Glossary | Field Notes</title>
  <meta name="description" content="A glossary of Responsible AI, OWASP GenAI and AI Engineering terms.">
  <style>$font_faces
$css</style>
</head>
<body>
  <a class="skip-link" href="#main" data-i18n="skip">Skip to glossary</a>
  <aside class="sidebar">
    <a class="brand" href="#top" aria-label="AI field notes, top of page" data-i18n-label="brandTop"><span class="brand-icon">$flower_icon</span><span><span data-i18n="brand">sakura notes</span><span class="brand-subtitle" data-i18n="subtitle">AI / a study journal</span></span></a>
    <div class="sidebar-settings">
      <fieldset class="language-switch" aria-label="Language" data-i18n-label="language">
        <label lang="en-US" title="English (United States)"><input type="radio" name="language" value="en-US" aria-label="English (United States)" checked><span>EN-US</span></label>
        <label lang="pt-BR" title="Portugu&#234;s (Brasil)"><input type="radio" name="language" value="pt-BR" aria-label="Portugu&#234;s (Brasil)"><span>PT-BR</span></label>
      </fieldset>
      <button id="theme-toggle" class="icon-button theme-toggle" type="button" aria-label="Switch to light mode" title="Switch to light mode"><span class="theme-thumb"></span><span class="sun-icon">$sun_icon</span><span class="moon-icon">$moon_icon</span></button>
    </div>
    <div class="sidebar-index">
      <p class="sidebar-label"><span data-i18n="index">THE INDEX</span><span>A &mdash; Z</span></p>
      <nav class="alphabet" aria-label="Alphabetical index" data-i18n-label="alphabet">$nav</nav>
      <a class="distinction-link" href="#letter-Key" data-letter="Key" aria-label="Key distinctions" title="Key distinctions" data-i18n-label="distinctions" data-i18n-title="distinctions">$compare_icon<span data-i18n="distinctions">Key distinctions</span><span class="note-count">$note_count</span></a>
    </div>
    <div class="sidebar-bottom"><span class="sidebar-label" data-i18n="collection">STUDY COLLECTION</span><p><span data-i18n="responsible">Responsible AI</span><br>OWASP GenAI<br><span data-i18n="engineering">AI Engineering</span></p><a class="source-link" href="https://github.com/anaclacp/ai-agents-in-action" target="_blank" rel="noopener noreferrer">anaclacp / GitHub $arrow_icon</a></div>
  </aside>
  <div class="workspace" id="top">
    <header class="page-header">
      <img class="sakura-art" src="$sakura_image" alt="" width="1536" height="1024" aria-hidden="true" fetchpriority="high">
      <div class="eyebrow"><span class="edition" data-i18n="reference">STUDY JOURNAL / 01</span></div>
      <div class="title-row"><h1><span data-i18n="heading">AI Glossary</span><span class="title-dot">.</span></h1></div>
      <p class="description"><span data-i18n="description1">Notes on the language of AI.</span><br><span data-i18n="description2">Models, security, and everything in between.</span></p>
      <div class="topics"><span data-i18n="responsible">Responsible AI</span><span>OWASP GenAI</span><span data-i18n="engineering">AI Engineering</span></div>
    </header>
    <div class="search-toolbar">
      <div class="search-box">$search_icon<label class="sr-only" for="search" data-i18n="searchLabel">Search terms and definitions</label><input type="search" id="search" placeholder="Search glossary" data-i18n-placeholder="searchPlaceholder" autocomplete="off" spellcheck="false"><button id="clear-search" class="icon-button" type="button" aria-label="Clear search" title="Clear search" data-i18n-label="clear" data-i18n-title="clear" hidden>$close_icon</button></div>
      <div class="results-line">
        <span id="results-label" role="status" aria-live="polite">ALL TERMS</span><span id="search-count" role="status" aria-live="polite">$total terms &middot; $note_count notes</span>
      </div>
    </div>
    <main id="main" tabindex="-1">$sections
      <div class="no-results" id="no-results" hidden><span class="empty-symbol">$search_icon</span><h2 data-i18n="noMatches">No matches</h2><p><span data-i18n="noMatchIntro">No terms or definitions match</span> <strong id="empty-query"></strong>.</p><button type="button" id="reset-search" data-i18n="clear">Clear search</button></div>
    </main>
    <footer><span data-i18n="brand">AI / field notes</span><span>anaclacp &middot; <span data-i18n="footerCollection">An evolving collection</span></span><a href="#top"><span data-i18n="backTop">Back to top</span> &uarr;</a></footer>
  </div>
  <script type="application/json" id="translations">$translations</script>
  <script>$js</script>
</body>
</html>
''')

html = template.substitute(
    source_hash=sha256((ROOT / "content/glossary.md").read_bytes()).hexdigest(),
    font_faces=font_faces,
    notices=(ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8"),
    sakura_image=embedded_asset("sakura-branch.png", "image/png"),
    css=(ROOT / "glossary.css").read_text(encoding="utf-8"),
    js=(ROOT / "glossary.js").read_text(encoding="utf-8"),
    nav=nav, total=total, note_count=len(distinctions), sections="".join(sections),
    translations=json.dumps({"ui": ui, "terms": portuguese}, ensure_ascii=True).replace("<", "\\u003c"),
    **{f"{name}_icon": icon(name) for name in ("book", "flower", "search", "close", "arrow", "compare", "sun", "moon")},
)
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(html, encoding="utf-8")
print(f"Built index.html: {total} terms, {len(distinctions)} notes, {len(html.encode('utf-8'))} bytes")
