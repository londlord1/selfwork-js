(() => {
  if (window.__pageHelperInjected) return;
  window.__pageHelperInjected = true;

  const DARK_STYLE_ID = '__ph-dark-style';
  const BANNER_ID = '__ph-banner';
  const TOAST_HOST_ID = '__ph-toast-host';
  const PANEL_HOST_ID = '__ph-notes-host';
  const WIDGET_HOST_ID = '__ph-widget-host';
  const MODAL_HOST_ID = '__ph-modal-host';
  const HL_ATTR = 'data-ph-highlight';

  let panel = null;
  let widget = null;

  const pageKey = () => location.origin + location.pathname + location.search;

  let fontLevel = 16;
  let fontRecords = [];

  function collectFontRecords() {
    fontRecords = [];
    if (!document.body) return;

    const nodes = [document.body];
    document.body.querySelectorAll('*').forEach((el) => nodes.push(el));

    nodes.forEach((el) => {
      if (/^(SCRIPT|STYLE|LINK|META|TITLE|NOSCRIPT|HEAD)$/.test(el.tagName)) return;
      if (!el.getClientRects().length) return;
      const size = parseFloat(getComputedStyle(el).fontSize);
      if (!size) return;
      fontRecords.push({
        el,
        base: size,
        inline: el.style.getPropertyValue('font-size'),
        priority: el.style.getPropertyPriority('font-size')
      });
    });
  }

  function applyFont() {
    if (!fontRecords.length) collectFontRecords();
    const scale = fontLevel / 16;
    fontRecords.forEach((record) => {
      if (!record.el.isConnected) return;
      record.el.style.setProperty('font-size', (record.base * scale).toFixed(2) + 'px', 'important');
    });
  }

  function changeFont(delta) {
    fontLevel = Math.min(32, Math.max(8, fontLevel + Number(delta || 0)));
    applyFont();
    return fontLevel;
  }

  function resetFont() {
    fontRecords.forEach((record) => {
      if (!record.el.isConnected) return;
      if (record.inline) record.el.style.setProperty('font-size', record.inline, record.priority);
      else record.el.style.removeProperty('font-size');
    });
    fontRecords = [];
    fontLevel = 16;
    document.documentElement.style.removeProperty('zoom');
    return fontLevel;
  }

  function setBackground(color) {
    document.documentElement.style.setProperty('background-color', color, 'important');
    if (document.body) document.body.style.setProperty('background-color', color, 'important');
  }

  function resetBackground() {
    document.documentElement.style.removeProperty('background-color');
    if (document.body) document.body.style.removeProperty('background-color');
  }

  function setDark(on, persist = true) {
    let style = document.getElementById(DARK_STYLE_ID);
    if (on) {
      resetBackground();
      if (!style) {
        style = document.createElement('style');
        style.id = DARK_STYLE_ID;
        style.textContent = [
          'html,body{background-color:#1a1a1a !important;color:#f1f5f9 !important;}',
          'a{color:#8ab4f8 !important;}',
          'input,textarea,select,button{background-color:#2d2d2d !important;color:#f1f5f9 !important;border-color:#555 !important;}',
          'img,video{opacity:.9;}'
        ].join('\n');
        document.documentElement.appendChild(style);
      }
      document.documentElement.style.colorScheme = 'dark';
    } else {
      if (style) style.remove();
      document.documentElement.style.colorScheme = '';
    }
    if (persist) chrome.storage.local.set({ darkMode: !!on });
  }

  function highlightHeadings() {
    const nodes = document.querySelectorAll('h1,h2,h3,h4,h5,h6,[role="heading"]');
    let count = 0;
    nodes.forEach((heading) => {
      if (heading.hasAttribute(HL_ATTR)) return;
      heading.setAttribute(HL_ATTR, '1');
      heading.dataset.phPrevStyle = heading.getAttribute('style') || '';
      heading.style.setProperty('background', '#fff59d', 'important');
      heading.style.setProperty('color', '#111111', 'important');
      heading.style.setProperty('padding', '4px 8px', 'important');
      heading.style.setProperty('border-radius', '4px', 'important');
      heading.style.setProperty('outline', '2px solid #f59e0b', 'important');
      heading.style.setProperty('box-shadow', '0 0 0 3px rgba(245, 158, 11, 0.25)', 'important');
      count++;
    });
    return count;
  }

  function clearHighlight() {
    document.querySelectorAll('[' + HL_ATTR + ']').forEach((heading) => {
      const prev = heading.dataset.phPrevStyle;
      if (prev) heading.setAttribute('style', prev);
      else heading.removeAttribute('style');
      heading.removeAttribute(HL_ATTR);
      delete heading.dataset.phPrevStyle;
    });
  }

  function addBanner(text) {
    let banner = document.getElementById(BANNER_ID);
    if (!banner) {
      banner = document.createElement('div');
      banner.id = BANNER_ID;
      document.documentElement.appendChild(banner);
    }
    banner.textContent = text;
    Object.assign(banner.style, {
      position: 'fixed',
      top: '0',
      left: '0',
      right: '0',
      zIndex: '2147483646',
      background: '#1a73e8',
      color: '#ffffff',
      padding: '10px 16px',
      font: '14px/1.4 "Segoe UI", Arial, sans-serif',
      textAlign: 'center',
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.25)'
    });
  }

  function removeBanner() {
    const banner = document.getElementById(BANNER_ID);
    if (banner) banner.remove();
  }

  function showToast(text) {
    const old = document.getElementById(TOAST_HOST_ID);
    if (old) old.remove();

    const host = document.createElement('div');
    host.id = TOAST_HOST_ID;
    host.style.cssText = 'all:initial;position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:2147483647;';
    const shadow = host.attachShadow({ mode: 'open' });

    const style = document.createElement('style');
    style.textContent = [
      '.toast{background:#111827;color:#fff;padding:10px 18px;border-radius:10px;',
      'font:14px/1.4 "Segoe UI",Arial,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.35);',
      'animation:ph-in .2s ease both;}',
      '@keyframes ph-in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}'
    ].join('');

    const box = document.createElement('div');
    box.className = 'toast';
    box.textContent = text;

    shadow.appendChild(style);
    shadow.appendChild(box);
    document.documentElement.appendChild(host);

    setTimeout(() => host.remove(), 2600);
  }

  function getNotes(callback) {
    chrome.storage.local.get({ notes: {} }, (data) => {
      const all = data.notes || {};
      callback(all[pageKey()] || []);
    });
  }

  function writeNotes(list, callback) {
    chrome.storage.local.get({ notes: {} }, (data) => {
      const all = data.notes || {};
      if (list.length) all[pageKey()] = list;
      else delete all[pageKey()];
      chrome.storage.local.set({ notes: all }, callback);
    });
  }

  function removeNote(index) {
    getNotes((list) => {
      list.splice(index, 1);
      writeNotes(list, renderPanelNotes);
    });
  }

  function renderPanelNotes() {
    if (!panel) return;
    getNotes((list) => {
      const box = panel.list;
      box.textContent = '';

      if (!list.length) {
        const empty = document.createElement('div');
        empty.className = 'empty';
        empty.textContent = 'Заметок пока нет.';
        box.appendChild(empty);
        return;
      }

      list.forEach((note, index) => {
        const item = document.createElement('div');
        item.className = 'item';

        const body = document.createElement('div');
        body.className = 'body';

        const text = document.createElement('div');
        text.className = 'text';
        text.textContent = note.text;

        const meta = document.createElement('div');
        meta.className = 'meta';
        meta.textContent = new Date(note.date).toLocaleString('ru-RU');

        body.appendChild(text);
        body.appendChild(meta);

        const del = document.createElement('button');
        del.className = 'del';
        del.textContent = '×';
        del.title = 'Удалить';
        del.addEventListener('click', () => removeNote(index));

        item.appendChild(body);
        item.appendChild(del);
        box.appendChild(item);
      });
    });
  }

  function addNoteFromPanel() {
    const text = panel.input.value.trim();
    if (!text) return;
    getNotes((list) => {
      list.push({ text, date: new Date().toISOString() });
      writeNotes(list, () => {
        panel.input.value = '';
        renderPanelNotes();
      });
    });
  }

  function createPanel() {
    const host = document.createElement('div');
    host.id = PANEL_HOST_ID;
    host.style.cssText = 'all:initial;position:fixed;right:18px;bottom:76px;z-index:2147483647;';

    const shadow = host.attachShadow({ mode: 'open' });
    const style = document.createElement('style');
    style.textContent = [
      '.panel{width:300px;max-height:320px;display:flex;flex-direction:column;background:#fff;',
      'border:1px solid #cbd5e1;border-radius:12px;box-shadow:0 12px 30px rgba(15,23,42,.25);',
      'font:13px/1.4 "Segoe UI",Arial,sans-serif;color:#1f2937;overflow:hidden;}',
      '.head{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;',
      'background:#1a73e8;color:#fff;font-weight:600;}',
      '.head button{background:transparent;border:none;color:#fff;font-size:18px;cursor:pointer;line-height:1;}',
      '.list{overflow-y:auto;padding:8px 10px;flex:1;}',
      '.item{display:flex;gap:8px;justify-content:space-between;background:#f8fafc;',
      'border:1px solid #e2e8f0;border-radius:8px;padding:6px 8px;margin-bottom:6px;}',
      '.text{word-break:break-word;}',
      '.meta{color:#94a3b8;font-size:10px;margin-top:2px;}',
      '.del{border:none;background:transparent;color:#dc3545;font-size:16px;cursor:pointer;line-height:1;}',
      '.empty{color:#94a3b8;text-align:center;padding:12px 0;}',
      '.add{display:flex;gap:6px;padding:8px;border-top:1px solid #e2e8f0;background:#f8fafc;}',
      '.add input{flex:1;min-width:0;padding:6px 8px;border:1px solid #cbd5e1;border-radius:6px;font:inherit;}',
      '.add button{border:none;background:#1a73e8;color:#fff;border-radius:6px;padding:0 12px;cursor:pointer;font-size:16px;}'
    ].join('');

    const panelEl = document.createElement('div');
    panelEl.className = 'panel';
    panelEl.innerHTML = [
      '<div class="head"><span>📝 Заметки к странице</span><button id="close" title="Закрыть">×</button></div>',
      '<div class="list" id="list"></div>',
      '<div class="add"><input id="input" placeholder="Новая заметка…" maxlength="1000">',
      '<button id="add" title="Добавить">+</button></div>'
    ].join('');

    shadow.appendChild(style);
    shadow.appendChild(panelEl);
    document.documentElement.appendChild(host);

    host.style.display = 'none';

    panel = {
      host,
      visible: false,
      list: shadow.getElementById('list'),
      input: shadow.getElementById('input')
    };

    shadow.getElementById('close').addEventListener('click', () => {
      host.style.display = 'none';
      panel.visible = false;
    });

    shadow.getElementById('add').addEventListener('click', addNoteFromPanel);
    shadow.getElementById('input').addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        addNoteFromPanel();
      }
    });

    renderPanelNotes();
  }

  function toggleNotes() {
    if (!panel) createPanel();
    panel.visible = !panel.visible;
    panel.host.style.display = panel.visible ? 'block' : 'none';
    if (panel.visible) renderPanelNotes();
    return panel.visible;
  }

  function showGreetingModal(text) {
    const old = document.getElementById(MODAL_HOST_ID);
    if (old) old.remove();

    const host = document.createElement('div');
    host.id = MODAL_HOST_ID;
    host.style.cssText = 'all:initial;position:fixed;inset:0;z-index:2147483647;';
    const shadow = host.attachShadow({ mode: 'open' });

    const style = document.createElement('style');
    style.textContent = [
      '.overlay{position:fixed;inset:0;background:rgba(15,23,42,.45);display:flex;',
      'align-items:center;justify-content:center;padding:20px;animation:ph-fade .15s ease both;}',
      '.modal{background:#fff;border-radius:16px;padding:24px;max-width:340px;width:100%;',
      'text-align:center;box-shadow:0 20px 50px rgba(0,0,0,.3);',
      'font:14px/1.5 "Segoe UI",Arial,sans-serif;color:#1f2937;animation:ph-pop .2s ease both;}',
      '.modal h3{font-size:18px;color:#1a73e8;margin-bottom:10px;}',
      '.modal p{font-size:16px;margin-bottom:18px;word-break:break-word;}',
      '.modal button{border:none;background:#1a73e8;color:#fff;border-radius:8px;',
      'padding:10px 22px;font:inherit;cursor:pointer;}',
      '.modal button:hover{background:#0b5bc0;}',
      '@keyframes ph-fade{from{opacity:0}to{opacity:1}}',
      '@keyframes ph-pop{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:none}}'
    ].join('');

    const overlay = document.createElement('div');
    overlay.className = 'overlay';
    const modal = document.createElement('div');
    modal.className = 'modal';

    const title = document.createElement('h3');
    title.textContent = 'Приветствие';
    const body = document.createElement('p');
    body.textContent = text;
    const ok = document.createElement('button');
    ok.textContent = 'Закрыть';

    modal.appendChild(title);
    modal.appendChild(body);
    modal.appendChild(ok);
    overlay.appendChild(modal);
    shadow.appendChild(style);
    shadow.appendChild(overlay);
    document.documentElement.appendChild(host);

    const close = () => {
      host.remove();
      document.removeEventListener('keydown', onKey);
    };
    const onKey = (event) => {
      if (event.key === 'Escape') close();
    };

    ok.addEventListener('click', close);
    overlay.addEventListener('click', (event) => {
      if (event.target === overlay) close();
    });
    document.addEventListener('keydown', onKey);
  }

  function updateWidget() {
    if (!widget) return;
    chrome.storage.local.get({ clickCount: 0, notes: {} }, (data) => {
      if (!widget) return;
      const list = (data.notes || {})[pageKey()] || [];
      widget.clicks.textContent = data.clickCount || 0;
      widget.notes.textContent = list.length;
    });
  }

  function pageHello() {
    chrome.storage.local.get({ greetingName: 'студент', clickCount: 0 }, (data) => {
      const name = data.greetingName || 'студент';
      chrome.storage.local.set({ clickCount: (data.clickCount || 0) + 1 });
      showGreetingModal('Привет, ' + name + '! 👋');
      updateWidget();
    });
  }

  function createWidget() {
    if (document.getElementById(WIDGET_HOST_ID)) return;

    const host = document.createElement('div');
    host.id = WIDGET_HOST_ID;
    host.style.cssText = 'all:initial;position:fixed;right:18px;bottom:18px;z-index:2147483646;';
    const shadow = host.attachShadow({ mode: 'open' });

    const style = document.createElement('style');
    style.textContent = [
      '.bar{display:flex;gap:8px;align-items:center;font:13px/1 "Segoe UI",Arial,sans-serif;}',
      'button,.pill{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid #cbd5e1;',
      'border-radius:999px;padding:9px 13px;box-shadow:0 6px 18px rgba(15,23,42,.18);',
      'color:#1f2937;font:inherit;}',
      'button{cursor:pointer;}',
      'button:hover{background:#eef6ff;border-color:#93c5fd;}',
      '.pill{background:#f8fafc;color:#475569;cursor:default;}',
      'b{color:#1a73e8;}'
    ].join('');

    const bar = document.createElement('div');
    bar.className = 'bar';

    const hello = document.createElement('button');
    hello.title = 'Показать приветствие';
    hello.textContent = '👋 Приветствие';

    const clicksPill = document.createElement('span');
    clicksPill.className = 'pill';
    clicksPill.append('Клики: ');
    const clicks = document.createElement('b');
    clicksPill.appendChild(clicks);

    const notes = document.createElement('button');
    notes.title = 'Заметки к этой странице';
    notes.append('📝 Заметки: ');
    const notesCount = document.createElement('b');
    notes.appendChild(notesCount);

    bar.appendChild(hello);
    bar.appendChild(clicksPill);
    bar.appendChild(notes);
    shadow.appendChild(style);
    shadow.appendChild(bar);
    document.documentElement.appendChild(host);

    widget = { host, clicks, notes: notesCount };

    hello.addEventListener('click', pageHello);
    notes.addEventListener('click', () => toggleNotes());
    updateWidget();
  }

  function initPageUi() {
    createWidget();
    updateWidget();

    chrome.storage.local.get({ notes: {} }, (data) => {
      const list = (data.notes || {})[pageKey()] || [];
      if (list.length) {
        setTimeout(() => showToast('Восстановлено заметок: ' + list.length), 700);
      }
    });
  }

  initPageUi();

  chrome.storage.local.get({ darkMode: false }, (data) => {
    if (data.darkMode) setDark(true, false);
  });

  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== 'local') return;
    if (changes.notes) {
      if (panel && panel.visible) renderPanelNotes();
      updateWidget();
    }
    if (changes.clickCount) {
      updateWidget();
    }
    if (changes.darkMode) {
      setDark(!!changes.darkMode.newValue, false);
    }
  });

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    try {
      switch (message && message.type) {
        case 'getState':
          sendResponse({
            ok: true,
            fontSize: fontLevel,
            dark: !!document.getElementById(DARK_STYLE_ID),
            url: pageKey()
          });
          break;
        case 'toast':
          showToast(String(message.text || ''));
          sendResponse({ ok: true });
          break;
        case 'greeting':
          showGreetingModal(String(message.text || 'Привет! 👋'));
          sendResponse({ ok: true });
          break;
        case 'setBg':
          setBackground(message.color);
          sendResponse({ ok: true });
          break;
        case 'resetBg':
          resetBackground();
          sendResponse({ ok: true });
          break;
        case 'font':
          sendResponse({ ok: true, size: changeFont(message.delta) });
          break;
        case 'resetFont':
          sendResponse({ ok: true, size: resetFont() });
          break;
        case 'setDark':
          setDark(!!message.on);
          sendResponse({ ok: true });
          break;
        case 'highlight':
          sendResponse({ ok: true, count: highlightHeadings() });
          break;
        case 'banner':
          addBanner(String(message.text || 'ПР18'));
          sendResponse({ ok: true });
          break;
        case 'clearEffects':
          clearHighlight();
          removeBanner();
          resetBackground();
          resetFont();
          setDark(false);
          sendResponse({ ok: true });
          break;
        case 'toggleNotes':
          sendResponse({ ok: true, visible: toggleNotes() });
          break;
        default:
          sendResponse({ ok: false, error: 'Неизвестная команда' });
      }
    } catch (error) {
      sendResponse({ ok: false, error: error.message });
    }
    return true;
  });
})();
