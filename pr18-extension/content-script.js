(() => {
  if (window.__pageHelperInjected) return;
  window.__pageHelperInjected = true;

  const DARK_STYLE_ID = '__ph-dark-style';
  const BANNER_ID = '__ph-banner';
  const TOAST_HOST_ID = '__ph-toast-host';
  const PANEL_HOST_ID = '__ph-notes-host';
  const HL_ATTR = 'data-ph-highlight';

  let panel = null;

  const pageKey = () => location.origin + location.pathname + location.search;

  let fontLevel = 16;

  function currentFontSize() {
    return fontLevel;
  }

  function applyFont() {
    const scale = fontLevel / 16;
    if (typeof CSS !== 'undefined' && CSS.supports && CSS.supports('zoom', '1.25')) {
      document.documentElement.style.zoom = scale === 1 ? '' : String(scale);
    } else if (document.body) {
      document.body.style.setProperty('font-size', fontLevel + 'px', 'important');
    }
  }

  function changeFont(delta) {
    fontLevel = Math.min(32, Math.max(8, fontLevel + Number(delta || 0)));
    applyFont();
    return fontLevel;
  }

  function resetFont() {
    fontLevel = 16;
    document.documentElement.style.zoom = '';
    if (document.body) document.body.style.removeProperty('font-size');
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
    const nodes = document.querySelectorAll('h1,h2,h3,h4,h5,h6');
    let count = 0;
    nodes.forEach((heading) => {
      if (heading.hasAttribute(HL_ATTR)) return;
      heading.setAttribute(HL_ATTR, '1');
      heading.dataset.phPrevStyle = heading.getAttribute('style') || '';
      heading.style.background = '#fff59d';
      heading.style.color = '#111';
      heading.style.padding = '4px 8px';
      heading.style.borderRadius = '4px';
      heading.style.outline = '1px solid #fbc02d';
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
    host.style.cssText = 'all:initial;position:fixed;right:18px;bottom:18px;z-index:2147483647;';

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

  chrome.storage.local.get({ darkMode: false }, (data) => {
    if (data.darkMode) setDark(true, false);
  });

  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== 'local') return;
    if (changes.notes && panel && panel.visible) {
      renderPanelNotes();
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
            fontSize: currentFontSize(),
            dark: !!document.getElementById(DARK_STYLE_ID),
            url: pageKey()
          });
          break;
        case 'toast':
          showToast(String(message.text || ''));
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
