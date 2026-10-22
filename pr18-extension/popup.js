const $ = (id) => document.getElementById(id);

let activeTab = null;
let pageUrl = '';
let notes = [];

const STORAGE_DEFAULTS = {
  clickCount: 0,
  darkMode: false,
  greetingName: 'студент',
  notes: {}
};

function setStatus(text, type) {
  const el = $('status');
  el.textContent = text;
  el.className = 'status' + (type ? ' ' + type : '');
}

function shortUrl(url) {
  try {
    const u = new URL(url);
    const path = u.pathname === '/' ? '' : u.pathname;
    return u.hostname + path;
  } catch (e) {
    return url || 'недоступно';
  }
}

function humanError(error) {
  if (!error) return 'страница недоступна';
  if (/Receiving end does not exist|Could not establish connection/i.test(error)) {
    return 'обновите страницу (F5) — контент-скрипт ещё не загружен';
  }
  return error;
}

function sendRaw(tabId, message) {
  return new Promise((resolve) => {
    chrome.tabs.sendMessage(tabId, message, (response) => {
      if (chrome.runtime.lastError) {
        resolve({ ok: false, error: chrome.runtime.lastError.message });
        return;
      }
      resolve(response || { ok: true });
    });
  });
}

async function sendToTab(message) {
  if (!activeTab || !activeTab.id) {
    return { ok: false, error: 'Нет активной вкладки' };
  }

  let result = await sendRaw(activeTab.id, message);

  if (!result.ok && /Receiving end does not exist|Could not establish connection/i.test(result.error || '')) {
    try {
      await chrome.scripting.executeScript({
        target: { tabId: activeTab.id },
        files: ['content-script.js']
      });
      await new Promise((resolve) => setTimeout(resolve, 80));
      result = await sendRaw(activeTab.id, message);
    } catch (error) {
      result = { ok: false, error: error.message };
    }
  }

  return result;
}

async function readStorage() {
  return chrome.storage.local.get(STORAGE_DEFAULTS);
}

async function writeStorage(data) {
  await chrome.storage.local.set(data);
}

function renderNotes() {
  const box = $('notes-list');
  box.textContent = '';

  if (!notes.length) {
    const empty = document.createElement('p');
    empty.className = 'muted';
    empty.textContent = 'Заметок для этой страницы пока нет.';
    box.appendChild(empty);
    return;
  }

  notes.forEach((note, index) => {
    const row = document.createElement('div');
    row.className = 'note';

    const textWrap = document.createElement('div');
    const text = document.createElement('div');
    text.className = 'note-text';
    text.textContent = note.text;

    const date = document.createElement('div');
    date.className = 'note-date';
    date.textContent = new Date(note.date).toLocaleString('ru-RU');

    textWrap.appendChild(text);
    textWrap.appendChild(date);

    const del = document.createElement('button');
    del.className = 'note-del';
    del.title = 'Удалить заметку';
    del.textContent = '×';
    del.addEventListener('click', () => deleteNote(index));

    row.appendChild(textWrap);
    row.appendChild(del);
    box.appendChild(row);
  });
}

async function saveNote() {
  if (!pageUrl) {
    setStatus('Заметки недоступны на этой странице', 'err');
    return;
  }
  const input = $('note-text');
  const text = input.value.trim();
  if (!text) {
    setStatus('Введите текст заметки', 'err');
    return;
  }

  notes.push({ text, date: new Date().toISOString() });
  const data = await readStorage();
  data.notes[pageUrl] = notes;
  await writeStorage({ notes: data.notes });

  input.value = '';
  renderNotes();
  setStatus('Заметка сохранена для ' + shortUrl(pageUrl), 'ok');
}

async function deleteNote(index) {
  notes.splice(index, 1);
  const data = await readStorage();
  if (notes.length) {
    data.notes[pageUrl] = notes;
  } else {
    delete data.notes[pageUrl];
  }
  await writeStorage({ notes: data.notes });
  renderNotes();
  setStatus('Заметка удалена', 'ok');
}

async function updateCount(value) {
  await writeStorage({ clickCount: value });
  $('count').textContent = value;
}

async function showHello() {
  const name = $('name').value.trim() || 'студент';
  await writeStorage({ greetingName: name });

  const data = await readStorage();
  const next = data.clickCount + 1;
  await updateCount(next);

  const result = await sendToTab({ type: 'toast', text: 'Привет, ' + name + '! 👋' });
  if (!result.ok) {
    setStatus('Нажатий: ' + next + '. Приветствие не показано: ' + (humanError(result.error) || 'обновите вкладку'), 'err');
    return;
  }

  setStatus('Приветствие показано. Нажатий: ' + next, 'ok');
}

function bindColorButtons() {
  document.querySelectorAll('.swatch').forEach((button) => {
    button.addEventListener('click', async () => {
      const color = button.dataset.color;
      const result = await sendToTab({ type: 'setBg', color });
      setStatus(result.ok ? 'Фон страницы изменён: ' + color : 'Ошибка: ' + humanError(result.error), result.ok ? 'ok' : 'err');
    });
  });
}

async function changeFont(delta) {
  const result = await sendToTab({ type: 'font', delta });
  if (result.ok) {
    $('font-size').textContent = result.size + ' px';
    setStatus('Размер шрифта: ' + result.size + ' px', 'ok');
  } else {
    setStatus('Ошибка: ' + humanError(result.error), 'err');
  }
}

async function setDark(on) {
  const result = await sendToTab({ type: 'setDark', on });
  if (result.ok) {
    $('dark-label').textContent = on ? 'включён' : 'выключен';
    setStatus('Тёмный режим ' + (on ? 'включён' : 'выключен'), 'ok');
  } else {
    setStatus('Ошибка: ' + humanError(result.error), 'err');
  }
}

async function init() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  activeTab = tab;

  const data = await readStorage();
  $('count').textContent = data.clickCount;
  $('name').value = data.greetingName || 'студент';
  $('hello').textContent = 'Привет, ' + ($('name').value || 'студент') + '! 👋';
  $('dark').checked = !!data.darkMode;
  $('dark-label').textContent = data.darkMode ? 'включён' : 'выключен';

  const state = await sendToTab({ type: 'getState' });
  const pageReady = state.ok && state.url;

  if (pageReady) {
    pageUrl = state.url;
    $('page-url').textContent = shortUrl(pageUrl);
    $('page-url').title = pageUrl;
    $('font-size').textContent = (state.fontSize || 16) + ' px';
    notes = (data.notes && data.notes[pageUrl]) ? data.notes[pageUrl].slice() : [];
    renderNotes();
    setStatus('Готово. Страница: ' + shortUrl(pageUrl), 'ok');
  } else {
    $('page-url').textContent = 'недоступно';
    notes = [];
    renderNotes();
    setStatus('На служебных страницах браузера (chrome://, edge://, about:, Chrome Web Store) расширение не работает. Откройте обычный сайт и обновите вкладку.', 'err');
  }

  $('hello').addEventListener('click', showHello);
  $('name').addEventListener('input', () => {
    $('hello').textContent = 'Привет, ' + ($('name').value.trim() || 'студент') + '! 👋';
  });

  bindColorButtons();

  $('bg-reset').addEventListener('click', async () => {
    const result = await sendToTab({ type: 'resetBg' });
    setStatus(result.ok ? 'Фон страницы сброшен' : 'Ошибка: ' + humanError(result.error), result.ok ? 'ok' : 'err');
  });

  $('font-inc').addEventListener('click', () => changeFont(2));
  $('font-dec').addEventListener('click', () => changeFont(-2));
  $('font-reset').addEventListener('click', async () => {
    const result = await sendToTab({ type: 'resetFont' });
    if (result.ok) {
      $('font-size').textContent = result.size + ' px';
      setStatus('Размер шрифта сброшен', 'ok');
    }
  });

  $('count-reset').addEventListener('click', async () => {
    await updateCount(0);
    setStatus('Счётчик сброшен', 'ok');
  });

  $('dark').addEventListener('change', (event) => setDark(event.target.checked));

  $('highlight').addEventListener('click', async () => {
    const result = await sendToTab({ type: 'highlight' });
    if (!result.ok) {
      setStatus('Ошибка: ' + humanError(result.error), 'err');
    } else if (!result.count) {
      setStatus('На этой странице не найдено заголовков h1–h6', 'err');
    } else {
      setStatus('Выделено заголовков: ' + result.count, 'ok');
    }
  });

  $('banner').addEventListener('click', async () => {
    const result = await sendToTab({ type: 'banner', text: '📢 ПР18: контент-скрипт работает' });
    setStatus(result.ok ? 'Баннер добавлен' : 'Ошибка: ' + humanError(result.error), result.ok ? 'ok' : 'err');
  });

  $('clear').addEventListener('click', async () => {
    const result = await sendToTab({ type: 'clearEffects' });
    setStatus(result.ok ? 'Эффекты убраны' : 'Ошибка: ' + humanError(result.error), result.ok ? 'ok' : 'err');
  });

  $('note-save').addEventListener('click', saveNote);
  $('notes-toggle').addEventListener('click', async () => {
    const result = await sendToTab({ type: 'toggleNotes' });
    setStatus(result.ok ? 'Панель заметок переключена' : 'Ошибка: ' + humanError(result.error), result.ok ? 'ok' : 'err');
  });

}

chrome.storage.onChanged.addListener((changes, area) => {
  if (area !== 'local') return;

  if (changes.clickCount) {
    $('count').textContent = changes.clickCount.newValue || 0;
  }

  if (changes.darkMode) {
    const value = !!changes.darkMode.newValue;
    $('dark').checked = value;
    $('dark-label').textContent = value ? 'включён' : 'выключен';
  }

  if (changes.notes) {
    const all = changes.notes.newValue || {};
    notes = all[pageUrl] ? all[pageUrl].slice() : [];
    renderNotes();
  }
});

init().catch((error) => setStatus('Ошибка инициализации: ' + error.message, 'err'));
