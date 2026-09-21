(() => {
  const translations = JSON.parse(document.getElementById('translations').textContent);
  let locale = 'en-US';
  try {
    const saved = localStorage.getItem('ai-glossary-language');
    if (saved === 'en-US' || saved === 'pt-BR') locale = saved;
  } catch (_) { /* English remains available without storage. */ }
  const t = key => translations.ui[locale][key];
  const themeToggle = document.getElementById('theme-toggle');
  function updateThemeButton() {
    const action = t(document.documentElement.dataset.theme === 'dark' ? 'lightMode' : 'darkMode');
    themeToggle.setAttribute('aria-label', action);
    themeToggle.title = action;
  }
  themeToggle.addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = theme;
    try {
      localStorage.setItem('ai-glossary-theme', theme);
    } catch (_) { /* Theme switching still works without storage. */ }
    updateThemeButton();
  });
  updateThemeButton();

  const input = document.getElementById('search');
  const clear = document.getElementById('clear-search');
  const reset = document.getElementById('reset-search');
  const count = document.getElementById('search-count');
  const label = document.getElementById('results-label');
  const empty = document.getElementById('no-results');
  const emptyQuery = document.getElementById('empty-query');
  const cards = [...document.querySelectorAll('.term-card')];
  const sections = [...document.querySelectorAll('.letter-section')];
  const links = [...document.querySelectorAll('a[data-letter]')];
  const termCount = cards.filter(card => !card.closest('.distinctions')).length;
  const noteCount = cards.length - termCount;
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const parser = new DOMParser();
  const searchable = cards.map(card => {
    const body = card.querySelector('.term-body');
    const pt = translations.terms[card.id];
    const ptText = parser.parseFromString(pt.html, 'text/html').body.textContent;
    return {
      card, body, englishHtml: body.innerHTML, portugueseHtml: pt.html,
      text: normalize([card.querySelector('h3').textContent, body.textContent, pt.term, ptText].join(' ')),
    };
  });

  function applyLocale(nextLocale, preservePosition = false) {
    const toolbarBottom = document.querySelector('.search-toolbar').getBoundingClientRect().bottom;
    const reading = preservePosition && window.scrollY > 0
      ? cards.find(card => !card.hidden && card.getBoundingClientRect().bottom > toolbarBottom + 40)
      : null;
    const previousTop = reading?.getBoundingClientRect().top;
    locale = nextLocale;
    document.documentElement.lang = locale;
    document.title = t('title');
    document.querySelector('meta[name="description"]').content = t('metaDescription');
    document.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
    for (const [attribute, key] of [['aria-label', 'data-i18n-label'], ['title', 'data-i18n-title'], ['placeholder', 'data-i18n-placeholder']]) {
      document.querySelectorAll(`[${key}]`).forEach(el => {
        el.setAttribute(attribute, t(el.getAttribute(key)));
      });
    }
    document.querySelectorAll('[data-count]').forEach(el => {
      const value = Number(el.dataset.count);
      const unit = t(el.dataset.unit + (value === 1 ? '' : 's'));
      el.textContent = `${el.classList.contains('section-count') ? String(value).padStart(2, '0') : value} ${unit}`;
    });
    document.querySelectorAll('.nav-letter[data-letter]').forEach(link => {
      link.setAttribute('aria-label', `${t('letter')} ${link.dataset.letter}`);
    });
    document.querySelectorAll('input[name="language"]').forEach(radio => { radio.checked = radio.value === locale; });
    searchable.forEach(({ card, body, englishHtml, portugueseHtml }) => {
      body.innerHTML = locale === 'pt-BR' ? portugueseHtml : englishHtml;
      body.lang = locale;
      card.querySelector('.term-translation').hidden = locale !== 'pt-BR';
    });
    updateThemeButton();
    search();
    if (reading) {
      window.scrollBy({ top: reading.getBoundingClientRect().top - previousTop, behavior: 'instant' });
      updateActive();
    }
  }

  function updateActive() {
    const top = document.querySelector('.search-toolbar').getBoundingClientRect().bottom + 65;
    const visibleSections = sections.filter(section => !section.hidden);
    let active = visibleSections[0];
    for (const section of visibleSections) {
      if (section.getBoundingClientRect().top <= top) active = section;
    }
    links.forEach(link => {
      const current = !!active && link.dataset.letter === active.dataset.letter;
      link.classList.toggle('active', current);
      if (current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }

  function search() {
    const query = input.value.trim();
    const words = normalize(query).split(/\s+/).filter(Boolean);
    let visible = 0;
    searchable.forEach(({ card, text }) => {
      card.hidden = !words.every(word => text.includes(word));
      if (!card.hidden) visible++;
    });
    sections.forEach(section => {
      section.hidden = !section.querySelector('.term-card:not([hidden])');
      const link = links.find(link => link.dataset.letter === section.dataset.letter);
      if (section.hidden) link.setAttribute('aria-disabled', 'true');
      else link.removeAttribute('aria-disabled');
    });
    clear.hidden = !input.value;
    count.textContent = query ? `${visible} ${t(visible === 1 ? 'match' : 'matches')}` : `${termCount} ${t('terms')} \u00b7 ${noteCount} ${t('notes')}`;
    label.textContent = t(query ? 'searchResults' : 'allTerms');
    empty.hidden = visible !== 0;
    emptyQuery.textContent = query;
    updateActive();
  }

  function clearSearch() {
    input.value = '';
    search();
    input.focus({ preventScroll: true });
  }

  input.addEventListener('input', search);
  input.addEventListener('keydown', event => {
    if (event.key === 'Escape') clearSearch();
  });
  clear.addEventListener('click', clearSearch);
  reset.addEventListener('click', clearSearch);
  document.querySelectorAll('input[name="language"]').forEach(radio => {
    radio.addEventListener('change', () => {
      applyLocale(radio.value, true);
      try {
        localStorage.setItem('ai-glossary-language', locale);
      } catch (_) { /* Language switching still works without storage. */ }
    });
  });
  links.forEach(link => link.addEventListener('click', event => {
    if (link.getAttribute('aria-disabled') === 'true') event.preventDefault();
  }));

  // Keep direct links usable even when the destination was filtered out.
  function revealHash() {
    const target = document.getElementById(location.hash.slice(1));
    if (target && (target.hidden || target.closest('[hidden]'))) {
      clearSearch();
      target.scrollIntoView();
    }
    updateActive();
  }
  window.addEventListener('hashchange', revealHash);
  let scheduled = false;
  window.addEventListener('scroll', () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => { updateActive(); scheduled = false; });
  }, { passive: true });
  window.addEventListener('resize', updateActive);
  applyLocale(locale);
})();
