"""Explicit integration test; run in Actions with test_translation=true."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sync_translations import ArgosTranslator, validate_translation

result = ArgosTranslator()({"anchor": "test", "term": "Context Window", "html": '<p>A model processes <strong>information</strong> from the input.</p><ul><li>Training data</li></ul><pre class="code-block"><code>model.predict(x)</code></pre><p>Use <code>max_tokens</code>.</p>'})
validate_translation(result)
assert "model.predict(x)" in result["html"]
assert "max_tokens" in result["html"]
assert "A model processes" not in result["html"]
print(result)
