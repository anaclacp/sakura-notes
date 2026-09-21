import unittest

from parse_glossary import entries, parse_glossary, slugify
from sync_translations import source_hash, synchronize, validate_translation


class PipelineTests(unittest.TestCase):
    def data(self, body="A small **adapter**.", name="Adapter"):
        return parse_glossary(f"# AI Glossary\n\n## Index\n\n[Adapter](#adapter)\n\n## A\n\n### {name}\n\n{body}\n\n---\n")

    def test_known_anchors(self):
        self.assertEqual(slugify("T&Cs \u2014 Terms and Conditions"), "tcs--terms-and-conditions")
        self.assertEqual(slugify("Signed \u2260 Safe"), "signed--safe")

    def test_index_ignored_and_crlf_supported(self):
        self.assertEqual(len(entries(self.data())), 1)
        self.assertEqual(len(entries(parse_glossary("## A\r\n\r\n### Adapter\r\n\r\nDefinition."))), 1)

    def test_fenced_headings_are_code(self):
        term = entries(self.data("Text.\n\n```text\n## B\n### Bad\n<&>\n```"))[0]
        self.assertIn("## B", term["html"])
        self.assertIn("&lt;&amp;&gt;", term["html"])

    def test_raw_html_and_script_links_cannot_execute(self):
        html = entries(self.data('<script>alert(1)</script>\n\n[link](javascript:alert(1))'))[0]["html"]
        self.assertNotIn("<script>", html)
        self.assertNotIn('href="javascript:', html)

    def test_lists_emphasis_links_and_blockquotes(self):
        html = entries(self.data("1. *One*\n2. [Two](https://example.com)\n\n> Quote"))[0]["html"]
        for tag in ("<ol>", "<em>", "<blockquote>", 'href="https://example.com"'):
            self.assertIn(tag, html)

    def test_duplicate_anchor_empty_and_unknown_sections_fail(self):
        for source in ("## A\n### Adapter\nText\n### Adapter\nMore", "## A\n### Adapter\n---", "## Appendix\n### Adapter\nText", "## A", "# Only title"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                parse_glossary(source)

    def test_wrong_letter_fails(self):
        with self.assertRaises(ValueError):
            self.data(name="Backdoor")

    def test_unchanged_source_reuses_reviewed_translation(self):
        data = self.data()
        value = {"term": "Adaptador", "html": "<p>Um adaptador.</p>"}
        state = {"adapter": {"source_sha256": source_hash(entries(data)[0]), "method": "reviewed"}}
        result, metadata, changed = synchronize(data, {"adapter": value}, state, None)
        self.assertEqual(result["adapter"], value)
        self.assertEqual(metadata, state)
        self.assertEqual(changed, [])

    def test_new_changed_and_removed_entries(self):
        calls = []
        def translate(term):
            calls.append(term["anchor"])
            return {"term": "Adaptador", "html": "<p>Atualizado.</p>"}
        old_state = {"adapter": {"source_sha256": source_hash(entries(self.data())[0])}}
        translations = {"adapter": {"term": "Old", "html": "<p>Old</p>"}, "deleted": {}}
        result, metadata, changed = synchronize(self.data("Changed."), translations, old_state, translate)
        self.assertEqual(calls, ["adapter"])
        self.assertEqual(changed, ["adapter"])
        self.assertNotIn("deleted", result)
        self.assertNotIn("deleted", metadata)
        self.assertIn("deleted", translations)
        self.assertEqual(translations["adapter"]["term"], "Old")
        _, _, changed = synchronize(self.data(), {}, {}, translate)
        self.assertEqual(changed, ["adapter"])

    def test_failed_translation_does_not_mutate_cache(self):
        original = {"adapter": {"term": "Old", "html": "<p>Old</p>"}}
        with self.assertRaises(ValueError):
            synchronize(self.data(), original, {}, lambda _: {"term": "", "html": ""})
        self.assertEqual(original["adapter"]["term"], "Old")

    def test_unsafe_translation_is_rejected(self):
        for html in ('<script>x</script>', '<p onclick="evil()">Text</p>', '<a href="javascript:evil()">Text</a>', '<iframe>Text</iframe>', '<a href="java\nscript:evil()">Text</a>'):
            with self.subTest(html=html), self.assertRaises(ValueError):
                validate_translation({"term": "Test", "html": html})


if __name__ == "__main__":
    unittest.main()
