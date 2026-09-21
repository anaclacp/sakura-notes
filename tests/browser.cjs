const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

(async () => {
  const browser = await chromium.launch({ headless: true, ...(process.env.PLAYWRIGHT_CHANNEL ? { channel: process.env.PLAYWRIGHT_CHANNEL } : {}) });
  try {
    const root = path.resolve(__dirname, '..');
    const source = JSON.parse(fs.readFileSync(path.join(root, 'glossary_data.json'), 'utf8'));
    const terms = [...source.letters.flatMap(group => group.terms), ...source.key_distinctions];
    const translations = JSON.parse(fs.readFileSync(path.join(root, 'glossary_pt-BR.json'), 'utf8'));
    const url = process.env.SITE_URL || pathToFileURL(path.join(root, '_site/index.html')).href;
    const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, reducedMotion: 'reduce' });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(url);
    await page.evaluate(() => document.fonts.ready);
    assert.equal(await page.locator('html').getAttribute('data-theme'), 'dark');
    assert.equal(await page.locator('.term-card').count(), terms.length);
    assert.equal(await page.locator('#adapter .term-body').evaluate(el => getComputedStyle(el).fontSize), '18px');
    assert(await page.locator('.sakura-art').evaluate(el => el.complete && el.naturalWidth > 0));
    for (const language of ['pt-BR', 'en-US']) {
      await page.locator(`input[value="${language}"]`).check();
      assert.equal(await page.locator('html').getAttribute('lang'), language);
      const correct = await page.evaluate(({ terms, translations, language }) => {
        const parser = new DOMParser();
        return terms.every(term => {
          const expected = parser.parseFromString(language === 'pt-BR' ? translations[term.anchor].html : term.html, 'text/html').body.textContent;
          return document.getElementById(term.anchor).querySelector('.term-body').textContent === expected;
        });
      }, { terms, translations, language });
      assert(correct, `All definitions in ${language}`);
    }
    for (const query of ['inferencia', 'infer\u00eancia', 'inference']) {
      await page.locator('#search').fill(query);
      assert(await page.locator('#inference').isVisible());
    }
    const count = await page.locator('.term-card:visible').count();
    await page.locator('input[value="pt-BR"]').check();
    assert.equal(await page.locator('.term-card:visible').count(), count);
    await page.locator('#search').fill('zzzzzznothing');
    assert(await page.locator('#no-results').isVisible());
    await page.locator('#reset-search').click();
    await page.locator('a[data-letter="R"]').click();
    const before = await page.locator('#rag--retrieval-augmented-generation').evaluate(el => el.getBoundingClientRect().top);
    await page.locator('input[value="en-US"]').check();
    const after = await page.locator('#rag--retrieval-augmented-generation').evaluate(el => el.getBoundingClientRect().top);
    assert(Math.abs(before - after) < 2, 'Reading position preserved');
    fs.mkdirSync(path.join(root, '.preview'), { recursive: true });
    for (const language of ['pt-BR', 'en-US']) {
      await page.locator(`input[value="${language}"]`).check();
      for (const theme of ['dark', 'light']) {
        if (await page.locator('html').getAttribute('data-theme') !== theme) await page.locator('#theme-toggle').click();
        await page.reload();
        assert.equal(await page.locator('html').getAttribute('lang'), language);
        assert.equal(await page.locator('html').getAttribute('data-theme'), theme);
        for (const width of [1440, 768, 390, 320]) {
          await page.setViewportSize({ width, height: width > 760 ? 1000 : 844 });
          await page.evaluate(() => window.scrollTo(0, 0));
          const overflow = await page.evaluate(() => [...document.querySelectorAll('h1,h2,h3,p,pre,input,.term-body,.language-switch')].filter(el => el.getClientRects().length && (el.getBoundingClientRect().right > innerWidth + 1 || el.getBoundingClientRect().left < -1 || el.scrollWidth > el.clientWidth + 2)).map(el => el.className));
          assert.deepEqual(overflow, [], `${language} ${theme} ${width}: overflow`);
          await page.screenshot({ path: path.join(root, `.preview/${language}-${theme}-${width}.png`) });
        }
      }
    }
    const blocked = await browser.newPage();
    blocked.on('pageerror', error => errors.push(error.message));
    await blocked.addInitScript(() => Object.defineProperty(window, 'localStorage', { get() { throw new Error('Unavailable'); } }));
    await blocked.goto(url);
    await blocked.locator('input[value="pt-BR"]').check();
    await blocked.locator('#theme-toggle').click();
    assert.equal(await blocked.locator('html').getAttribute('lang'), 'pt-BR');
    assert.deepEqual(errors, []);
    console.log(`Browser verified: ${terms.length} definitions, both languages/themes, four widths, search, persistence, artwork, reading position and blocked storage.`);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
