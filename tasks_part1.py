# -*- coding: utf-8 -*-
"""Задачи ПР17–ПР21."""

TASKS = []

# ============================== ПР17 ==============================
TASKS.append({
    "pr": 17, "n": 1,
    "slug": "инкапсуляция_приватные_переменные_ограниченный_счётчик",
    "title": "Инкапсуляция. Ограниченный счётчик",
    "desc": "Фабричная функция <code>createBoundedCounter(min, max)</code>: приватная переменная через замыкание, "
            "блокировка выхода за пределы диапазона, методы <code>getRange()</code>, <code>getValue()</code> и "
            "<code>reset()</code> (сброс до <code>min</code>). Некорректный диапазон (min &gt; max) выбрасывает ошибку.",
    "body": """
<div class="card">
  <h2>1. Создание счётчика</h2>
  <div class="row">
    <label>min</label><input id="min" type="number" value="0" style="width:90px">
    <label>max</label><input id="max" type="number" value="5" style="width:90px">
    <button class="btn green" onclick="createCounter()">Создать</button>
    <button class="btn red" onclick="resetCounter()">reset()</button>
  </div>
  <p class="muted">Попробуйте min = 5, max = 0 — фабрика выбросит ошибку.</p>
</div>

<div class="card">
  <h2>2. Публичный API</h2>
  <div class="row">
    <button class="btn" onclick="doIncrement()">increment()</button>
    <button class="btn orange" onclick="doDecrement()">decrement()</button>
    <button class="btn gray" onclick="showValue()">getValue()</button>
    <button class="btn gray" onclick="showRange()">getRange()</button>
  </div>
  <div class="out" id="out">Сначала создайте счётчик.</div>
</div>
""",
    "script": r"""
function createBoundedCounter(min, max) {
  min = Number(min);
  max = Number(max);
  if (!Number.isFinite(min) || !Number.isFinite(max)) {
    throw new Error('min и max должны быть числами');
  }
  if (min > max) {
    throw new Error(`Некорректный диапазон: min (${min}) больше max (${max})`);
  }

  let count = min;

  function log(operation) {
    console.log(`[${new Date().toLocaleTimeString()}] ${operation}: ${count} (${min}..${max})`);
  }

  return {
    increment() {
      if (count >= max) {
        console.warn(`Достигнут максимум: ${max}`);
        return { value: count, warning: `Достигнут максимум: ${max}` };
      }
      count++;
      log('INCREMENT');
      return { value: count };
    },
    decrement() {
      if (count <= min) {
        console.warn(`Достигнут минимум: ${min}`);
        return { value: count, warning: `Достигнут минимум: ${min}` };
      }
      count--;
      log('DECREMENT');
      return { value: count };
    },
    getValue() {
      return count;
    },
    getRange() {
      return { min, max, current: count };
    },
    reset() {
      count = min;
      log('RESET');
      return { value: count };
    }
  };
}

let counter = null;

function render(extra) {
  const r = counter.getRange();
  out(`<span class="hl">getRange()</span> → ${JSON.stringify(r)}
${extra || ''}
<span class="ok">Приватность:</span> counter.count = ${String(counter.count)} — прямого доступа нет`);
}

function createCounter() {
  try {
    counter = createBoundedCounter($('min').value, $('max').value);
    render(`<span class="ok">Создан счётчик ${counter.getRange().min}..${counter.getRange().max}, текущее = ${counter.getValue()}</span>`);
  } catch (e) {
    counter = null;
    out(`<span class="err">Ошибка: ${esc(e.message)}</span>`);
  }
}

function need() {
  if (!counter) { out('<span class="err">Сначала создайте счётчик</span>'); return false; }
  return true;
}

function doIncrement() {
  if (!need()) return;
  const res = counter.increment();
  render(res.warning ? `<span class="err">${res.warning}</span>` : `increment() → <span class="ok">${res.value}</span>`);
}

function doDecrement() {
  if (!need()) return;
  const res = counter.decrement();
  render(res.warning ? `<span class="err">${res.warning}</span>` : `decrement() → <span class="ok">${res.value}</span>`);
}

function showValue() { if (need()) render(`getValue() → <span class="ok">${counter.getValue()}</span>`); }
function showRange() { if (need()) render(''); }
function resetCounter() { if (need()) render(`reset() → <span class="ok">${counter.reset().value}</span>`); }

createCounter();
""",
})

# ============================== ПР18 ==============================
EXT_PREVIEW = """
<div class="preview" id="page">
  <h3>Демо-страница сайта</h3>
  <p>Это обычная страница, на которую расширение применяет свои действия.</p>
  <h4>Заголовок второго уровня</h4>
  <p>Расширение работает через <code>chrome.scripting.executeScript</code> или контент-скрипт.</p>
  <ul><li>Первый пункт списка</li><li>Второй пункт списка</li></ul>
</div>
"""

TASKS.append({
    "pr": 18, "n": 1,
    "slug": "изменить_приветствие",
    "title": "Изменить приветствие",
    "desc": "Задание 1: заменить текст всплывающего окна «Hello, World!» на собственное приветствие. "
            "Демо имитирует popup расширения: popup отправляет действие в активную вкладку.",
    "body": """
<div class="card">
  <h2>Popup расширения</h2>
  <div class="row">
    <input id="name" placeholder="Ваше имя" value="студент" style="min-width:200px">
    <button class="btn green" onclick="sendHello()">Показать приветствие</button>
  </div>
  <div class="out" id="out">Здесь появится результат действия в активной вкладке.</div>
</div>
""" + EXT_PREVIEW,
    "script": r"""
function showHello(name) {
  const greeting = name ? `Привет, ${name}! 👋` : 'Привет, студент! 👋';
  out(`<span class="ok">${esc(greeting)}</span>`);
  return greeting;
}

function sendHello() {
  const name = $('name').value.trim();
  fakeChrome.scripting.executeScript({ func: showHello, args: [name] });
}

const fakeChrome = {
  scripting: {
    executeScript({ func, args }) {
      func(...args);
    }
  }
};

sendHello();
""",
})

TASKS.append({
    "pr": 18, "n": 2,
    "slug": "добавить_кнопку",
    "title": "Добавить новую кнопку",
    "desc": "Задание 2: добавить в popup четвертую кнопку, которая меняет цвет фона страницы. "
            "В демо цвет применяется к блоку «Демо-страница сайта».",
    "body": """
<div class="card">
  <h2>Popup расширения</h2>
  <div class="row">
    <button class="btn red" onclick="executeInTab(actions.changeRed)">Красный фон</button>
    <button class="btn green" onclick="executeInTab(actions.changeGreen)">Зелёный фон</button>
    <button class="btn orange" onclick="executeInTab(actions.changeOrange)">Оранжевый фон</button>
    <button class="btn" onclick="executeInTab(actions.changeBlue)">Синий фон</button>
    <button class="btn gray" onclick="executeInTab(actions.resetBg)">Сброс</button>
  </div>
  <div class="out" id="out">Нажмите «Синий фон» — новая кнопка из задания.</div>
</div>
""" + EXT_PREVIEW,
    "script": r"""
const actions = {
  changeRed() { setBg('#ffebee', ''); },
  changeGreen() { setBg('#e8f5e9', ''); },
  changeOrange() { setBg('#fff3e0', ''); },
  changeBlue() {
    setBg('#2196F3', '#fff');
    out('<span class="ok">Фон изменён на синий (#2196F3)</span>');
  },
  resetBg() { setBg('', ''); }
};

function setBg(bg, color) {
  const page = $('page');
  page.style.background = bg;
  page.style.color = color;
  page.style.transition = 'background-color 0.5s';
}

function executeInTab(action) {
  action();
}

$('page').addEventListener('click', () => {});
""",
})

TASKS.append({
    "pr": 18, "n": 3,
    "slug": "размер_шрифта",
    "title": "Смена размера шрифта",
    "desc": "Задание 3: кнопки «Увеличить шрифт» и «Уменьшить шрифт» меняют размер текста на странице на ±2px. "
            "Минимальный размер ограничен 8px.",
    "body": """
<div class="card">
  <h2>Popup расширения</h2>
  <div class="row">
    <button class="btn" onclick="executeInTab(actions.increaseFont)">A+ Увеличить шрифт</button>
    <button class="btn orange" onclick="executeInTab(actions.decreaseFont)">A− Уменьшить шрифт</button>
    <button class="btn gray" onclick="executeInTab(actions.resetFont)">Сброс</button>
  </div>
  <div class="out" id="out">Текущий размер: 16px</div>
</div>
""" + EXT_PREVIEW,
    "script": r"""
const actions = {
  increaseFont() {
    const current = parseFloat($('page').style.fontSize) || 16;
    $('page').style.fontSize = (current + 2) + 'px';
    report();
  },
  decreaseFont() {
    const current = parseFloat($('page').style.fontSize) || 16;
    $('page').style.fontSize = Math.max(8, current - 2) + 'px';
    report();
  },
  resetFont() {
    $('page').style.fontSize = '';
    report();
  }
};

function report() {
  out(`Текущий размер: <span class="hl">${parseFloat($('page').style.fontSize) || 16}px</span>`);
}

function executeInTab(action) { action(); }
""",
})

TASKS.append({
    "pr": 18, "n": 4,
    "slug": "счетчик_кликов",
    "title": "Счётчик кликов",
    "desc": "Задание 4: счётчик нажатий кнопки «Hello World!». Значение хранится в "
            "<code>chrome.storage.local</code> (в демо — <code>localStorage</code>), поэтому переживает перезапуск popup.",
    "body": """
<div class="card">
  <h2>Popup расширения</h2>
  <div class="row">
    <button class="btn" onclick="handleHello()">Hello World! 🌍</button>
    <button class="btn red" onclick="resetCount()">Сбросить</button>
  </div>
  <div class="out" id="out"></div>
  <p class="muted">Закройте и откройте страницу заново — счётчик сохранится.</p>
</div>
""",
    "script": r"""
const STORAGE_KEY = 'pr18_clickCount';
let count = Number(localStorage.getItem(STORAGE_KEY) || 0);

function render() {
  out(`Кнопка нажата <span class="hl">${count}</span> раз(а).
<span class="ok">helloWorld()</span> выполнен, значение сохранено в storage.local`);
}

function save() {
  localStorage.setItem(STORAGE_KEY, String(count));
}

function handleHello() {
  count++;
  save();
  render();
}

function resetCount() {
  count = 0;
  save();
  render();
}

render();
""",
})

TASKS.append({
    "pr": 18, "n": 5,
    "slug": "темный_режим",
    "title": "Тёмный режим",
    "desc": "Задание 5: переключатель тёмного режима. Меняет фон на #1a1a1a и цвет текста на белый, "
            "состояние сохраняется в storage (здесь — <code>localStorage</code>).",
    "body": """
<div class="card">
  <h2>Popup расширения</h2>
  <div class="row">
    <label class="pill" id="toggle"><input type="checkbox" id="dark" onchange="applyDark()"> Включить тёмный режим</label>
  </div>
  <div class="out" id="out"></div>
</div>
""" + EXT_PREVIEW,
    "script": r"""
const KEY = 'pr18_darkMode';

function applyDark() {
  const isDark = $('dark').checked;
  const page = $('page');
  page.dataset.dark = String(isDark);
  page.style.backgroundColor = isDark ? '#1a1a1a' : '';
  page.style.color = isDark ? '#ffffff' : '';
  localStorage.setItem(KEY, isDark ? 'true' : 'false');
  out(`Тёмный режим: <span class="hl">${isDark ? 'включён' : 'выключен'}</span>
Сохранено в storage: ${isDark}`);
}

$('dark').checked = localStorage.getItem(KEY) === 'true';
applyDark();
""",
})

TASKS.append({
    "pr": 18, "n": 6,
    "slug": "контент_скрипт",
    "title": "Расширение с контент-скриптом",
    "desc": "Задание 6: отдельный файл <code>content-script.js</code> вместо внедрения кода из popup. "
            "Popup отправляет сообщение через <code>runtime.sendMessage</code>, контент-скрипт принимает его "
            "в <code>runtime.onMessage</code>. Демо показывает обмен сообщениями.",
    "body": """
<div class="card">
  <h2>Popup расширения</h2>
  <div class="row">
    <button class="btn" onclick="send('highlight')">Выделить заголовки</button>
    <button class="btn green" onclick="send('banner')">Добавить баннер</button>
    <button class="btn gray" onclick="send('clear')">Убрать эффекты</button>
  </div>
  <div class="out" id="out">content-script.js подключён через manifest.json → content_scripts.</div>
</div>
""" + EXT_PREVIEW,
    "script": r"""
const contentScript = {
  onMessage(message, sender, sendResponse) {
    const page = $('page');
    if (message.action === 'highlight') {
      page.querySelectorAll('h3, h4').forEach(h => {
        h.style.background = '#fff59d';
        h.style.padding = '4px 8px';
        h.style.borderRadius = '4px';
      });
      sendResponse('Заголовки выделены');
    } else if (message.action === 'banner') {
      if (!$('cs-banner')) {
        const banner = document.createElement('div');
        banner.id = 'cs-banner';
        banner.textContent = '📢 Баннер добавлен контент-скриптом';
        banner.style.cssText = 'background:#1a73e8;color:#fff;padding:10px 14px;border-radius:8px;margin-bottom:10px';
        page.prepend(banner);
      }
      sendResponse('Баннер добавлен');
    } else {
      page.querySelectorAll('h3, h4').forEach(h => {
        h.style.background = '';
        h.style.padding = '';
      });
      const banner = $('cs-banner');
      if (banner) banner.remove();
      sendResponse('Эффекты убраны');
    }
  }
};

function send(action) {
  const message = { action };
  console.log('popup → content-script:', message);
  const response = contentScript.onMessage(message, {}, () => {});
  out(`popup отправил <span class="hl">${action}</span>
content-script ответил: <span class="ok">${esc(response)}</span>`);
}
""",
})

TASKS.append({
    "pr": 18, "n": 7,
    "slug": "заметки",
    "title": "Заметки на странице",
    "desc": "Задание 7: заметки привязываются к URL страницы и хранятся в <code>localStorage</code>. "
            "При повторном открытии страницы заметки восстанавливаются.",
    "body": """
<div class="card">
  <h2>Заметки к странице</h2>
  <p class="muted">📍 URL: <span id="current-url" class="kv"></span></p>
  <div class="row">
    <textarea id="note-text" placeholder="Текст заметки..." style="flex:1;min-width:240px;min-height:70px"></textarea>
  </div>
  <div class="row">
    <button class="btn green" onclick="saveNote()">💾 Сохранить заметку</button>
    <button class="btn red" onclick="clearNotes()">Очистить все</button>
  </div>
  <div id="notes"></div>
  <div class="out" id="out"></div>
</div>
""",
    "script": r"""
const URL_KEY = 'notes_' + location.pathname;
$('current-url').textContent = location.pathname;

function loadNotes() {
  try {
    return JSON.parse(localStorage.getItem(URL_KEY) || '[]');
  } catch (e) {
    return [];
  }
}

function renderNotes() {
  const notes = loadNotes();
  const box = $('notes');
  if (!notes.length) {
    box.innerHTML = '<p class="muted">Заметок пока нет.</p>';
    return;
  }
  box.innerHTML = notes.map((note, i) => `
    <div class="item">
      <div>
        <div>${esc(note.text)}</div>
        <div class="muted">${new Date(note.date).toLocaleString('ru-RU')}</div>
      </div>
      <button class="btn red" onclick="removeNote(${i})">×</button>
    </div>`).join('');
}

function saveNote() {
  const text = $('note-text').value.trim();
  if (!text) { out('<span class="err">Введите текст заметки</span>'); return; }
  const notes = loadNotes();
  notes.push({ text, date: new Date().toISOString() });
  localStorage.setItem(URL_KEY, JSON.stringify(notes));
  $('note-text').value = '';
  renderNotes();
  out(`<span class="ok">Заметка сохранена для ${esc(location.pathname)}</span>`);
}

function removeNote(i) {
  const notes = loadNotes();
  notes.splice(i, 1);
  localStorage.setItem(URL_KEY, JSON.stringify(notes));
  renderNotes();
  out('<span class="ok">Заметка удалена</span>');
}

function clearNotes() {
  localStorage.removeItem(URL_KEY);
  renderNotes();
  out('<span class="ok">Все заметки удалены</span>');
}

renderNotes();
""",
})

# ============================== ПР19 ==============================
def chat_body(hint, placeholder="Введите сообщение..."):
    return """
<div class="card">
  <h2>Чат с ботом</h2>
  <p class="muted">%s</p>
  <div class="out" id="chat" style="min-height:220px;max-height:320px;overflow:auto"></div>
  <div class="row">
    <input id="msg" placeholder="%s" style="flex:1;min-width:200px" onkeydown="if(event.key==='Enter')send()">
    <button class="btn" onclick="send()">Отправить</button>
  </div>
  <div class="out" id="out" style="min-height:auto"></div>
</div>
""" % (hint, placeholder)


TASKS.append({
    "pr": 19, "n": 1,
    "slug": "новая_команда",
    "title": "Новая команда для бота",
    "desc": "Задание 1: в <code>botResponses</code> добавлены новые команды «имя» и «возраст». "
            "Бот отвечает случайной фразой из массива.",
    "body": chat_body("Попробуйте: привет, имя, возраст, пока."),
    "script": r"""
const botResponses = {
  'привет': ['Привет! 😊', 'Здравствуй! 👋', 'Приветствую! 🤖'],
  'имя': ['Меня зовут Бот! А тебя? 😊', 'Я безымянный бот! Можешь придумать мне имя! 🤖'],
  'возраст': ['Мне ровно 1 день — я родился вместе с этой страницей 🎂', 'Возраст бота — понятие относительное 🙂'],
  'пока': ['Пока! 👋', 'До встречи! 😊']
};

function getBotResponse(text) {
  const lower = text.toLowerCase().trim();
  for (const [keyword, answers] of Object.entries(botResponses)) {
    if (lower.includes(keyword)) {
      return answers[Math.floor(Math.random() * answers.length)];
    }
  }
  return 'Я не совсем понял. Спросите «имя» или «возраст» 🤔';
}

function addMessage(text, who) {
  const chat = $('chat');
  const prev = chat.innerHTML;
  chat.innerHTML = prev + `<div style="margin:6px 0"><b class="${who === 'user' ? 'hl' : 'ok'}">${who === 'user' ? 'Вы' : 'Бот'}:</b> ${esc(text)}</div>`;
  chat.scrollTop = chat.scrollHeight;
}

function send() {
  const input = $('msg');
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  input.value = '';
  setTimeout(() => addMessage(getBotResponse(text), 'bot'), 300);
}

addMessage('Привет! Я бот. Спросите «имя» или «возраст».', 'bot');
""",
})

TASKS.append({
    "pr": 19, "n": 2,
    "slug": "день_рождения",
    "title": "Обработка дня рождения",
    "desc": "Задание 2: бот поздравляет, если в сообщении есть «день рождения» или «с днём рождения».",
    "body": chat_body("Напишите: день рождения, с днём рождения, привет."),
    "script": r"""
function getBotResponse(text) {
  const lower = text.toLowerCase();
  if (lower.includes('день рождения') || lower.includes('днём рождения') || lower.includes('днем рождения')) {
    return ['С днём рождения! 🎉🎂🎁', 'Поздравляю! Желаю счастья и здоровья! 🌟'][Math.floor(Math.random() * 2)];
  }
  if (lower.includes('привет')) return 'Привет! У кого-то день рождения? 🎈';
  return 'Напишите «день рождения» — и я поздравлю! 🎂';
}

function addMessage(text, who) {
  const chat = $('chat');
  chat.innerHTML += `<div style="margin:6px 0"><b class="${who === 'user' ? 'hl' : 'ok'}">${who === 'user' ? 'Вы' : 'Бот'}:</b> ${esc(text)}</div>`;
  chat.scrollTop = chat.scrollHeight;
}

function send() {
  const input = $('msg');
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  input.value = '';
  setTimeout(() => addMessage(getBotResponse(text), 'bot'), 300);
}

addMessage('Привет! У кого-то сегодня праздник? 🎉', 'bot');
""",
})

TASKS.append({
    "pr": 19, "n": 3,
    "slug": "счетчик_сообщений",
    "title": "Счётчик сообщений",
    "desc": "Задание 3: в конце каждого ответа бот показывает номер сообщения (сколько сообщений уже отправлено).",
    "body": chat_body("Отправьте несколько сообщений — номер будет расти."),
    "script": r"""
let messageCount = 0;
let userMessages = 0;

function getBotResponse(text) {
  if (/привет/i.test(text)) return 'Привет! 👋';
  if (/как дела/i.test(text)) return 'Отлично! А у тебя? 😊';
  return 'Интересно! Расскажи ещё 🤔';
}

function addMessage(text, who) {
  const chat = $('chat');
  chat.innerHTML += `<div style="margin:6px 0"><b class="${who === 'user' ? 'hl' : 'ok'}">${who === 'user' ? 'Вы' : 'Бот'}:</b> ${esc(text)}</div>`;
  chat.scrollTop = chat.scrollHeight;
}

function send() {
  const input = $('msg');
  const text = input.value.trim();
  if (!text) return;
  userMessages++;
  addMessage(text, 'user');
  input.value = '';

  setTimeout(() => {
    messageCount = userMessages;
    addMessage(`${getBotResponse(text)} (Сообщение #${messageCount})`, 'bot');
  }, 300);
}

addMessage('Напишите что-нибудь — я посчитаю сообщения.', 'bot');
""",
})

TASKS.append({
    "pr": 19, "n": 4,
    "slug": "несколько_слов",
    "title": "Обработка нескольких слов",
    "desc": "Задание 4: бот реагирует на фразу «как тебя зовут» целиком. Ключи проверяются от длинных к коротким, "
            "поэтому «как тебя зовут» имеет приоритет над «зовут».",
    "body": chat_body("Проверьте: «как тебя зовут», «как зовут», «привет»."),
    "script": r"""
const botResponses = {
  'как тебя зовут': ['Меня зовут ЧатБот-2000 🤖', 'У меня пока нет имени — придумай! 😊'],
  'зовут': ['Меня зовут Бот 🙂', 'Зови меня просто Бот.'],
  'привет': ['Привет! 👋']
};

function getBotResponse(text) {
  const lower = text.toLowerCase();
  const keys = Object.keys(botResponses).sort((a, b) => b.length - a.length);
  for (const key of keys) {
    if (lower.includes(key)) {
      const answers = botResponses[key];
      return answers[Math.floor(Math.random() * answers.length)];
    }
  }
  return 'Не понял. Спросите «как тебя зовут».';
}

function addMessage(text, who) {
  const chat = $('chat');
  chat.innerHTML += `<div style="margin:6px 0"><b class="${who === 'user' ? 'hl' : 'ok'}">${who === 'user' ? 'Вы' : 'Бот'}:</b> ${esc(text)}</div>`;
  chat.scrollTop = chat.scrollHeight;
}

function send() {
  const input = $('msg');
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  input.value = '';
  setTimeout(() => addMessage(getBotResponse(text), 'bot'), 300);
}

addMessage('Спросите «как тебя зовут» — отвечу целиком на фразу.', 'bot');
""",
})

TASKS.append({
    "pr": 19, "n": 5,
    "slug": "калькулятор",
    "title": "Режим «Калькулятор»",
    "desc": "Задание 5: бот вычисляет простые выражения вида «2+2», «5*3», «(4+6)/2». "
            "Выражение проверяется регуляркой перед вычислением.",
    "body": chat_body("Введите 2+2, 5*3, (4+6)/2 или привет."),
    "script": r"""
function getBotResponse(text) {
  const expr = text.replace(/,/g, '.').trim();
  if (/^[0-9+\-*/().\s]+$/.test(expr) && /[0-9]/.test(expr)) {
    try {
      const result = Function('"use strict"; return (' + expr + ')')();
      if (typeof result !== 'number' || !Number.isFinite(result)) throw new Error('bad result');
      return `Результат: ${result} 🧮`;
    } catch (e) {
      return 'Не могу вычислить это выражение. Попробуй что-то проще! 🤔';
    }
  }
  if (/привет/i.test(text)) return 'Привет! Дай мне пример, например 2+2 🧮';
  return 'Я умею считать. Напиши выражение, например 5*3.';
}

function addMessage(text, who) {
  const chat = $('chat');
  chat.innerHTML += `<div style="margin:6px 0"><b class="${who === 'user' ? 'hl' : 'ok'}">${who === 'user' ? 'Вы' : 'Бот'}:</b> ${esc(text)}</div>`;
  chat.scrollTop = chat.scrollHeight;
}

function send() {
  const input = $('msg');
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  input.value = '';
  setTimeout(() => addMessage(getBotResponse(text), 'bot'), 300);
}

addMessage('Калькулятор включён. Напишите выражение, например 2+2.', 'bot');
""",
})

TASKS.append({
    "pr": 19, "n": 6,
    "slug": "localstorage",
    "title": "История в localStorage",
    "desc": "Задание 6: все сообщения сохраняются в <code>localStorage</code> и восстанавливаются после перезагрузки. "
            "Есть кнопка очистки истории.",
    "body": chat_body("Отправьте сообщения, перезагрузите страницу — история сохранится.") + """
<div class="row"><button class="btn red" onclick="clearChat()">Очистить историю</button></div>""",
    "script": r"""
const HISTORY_KEY = 'pr19_chatHistory';

function loadHistory() {
  try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]'); }
  catch (e) { return []; }
}

function saveHistory(history) {
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
}

function render() {
  const history = loadHistory();
  $('chat').innerHTML = history.map(m =>
    `<div style="margin:6px 0"><b class="${m.who === 'user' ? 'hl' : 'ok'}">${m.who === 'user' ? 'Вы' : 'Бот'}:</b> ${esc(m.text)}</div>`
  ).join('');
  $('chat').scrollTop = $('chat').scrollHeight;
}

function addMessage(text, who) {
  const history = loadHistory();
  history.push({ text, who, date: new Date().toISOString() });
  saveHistory(history);
  render();
}

function getBotResponse(text) {
  if (/привет/i.test(text)) return 'Привет! История уже сохраняется 💾';
  if (/очист/i.test(text)) return 'Кнопка очистки — над чатом.';
  return 'Записал в историю. Перезагрузите страницу — сообщения останутся.';
}

function send() {
  const input = $('msg');
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  input.value = '';
  setTimeout(() => addMessage(getBotResponse(text), 'bot'), 300);
}

function clearChat() {
  localStorage.removeItem(HISTORY_KEY);
  render();
  out('<span class="ok">История очищена</span>');
}

if (!loadHistory().length) {
  addMessage('Привет! Я сохраняю историю в localStorage.', 'bot');
}
render();
""",
})

TASKS.append({
    "pr": 19, "n": 7,
    "slug": "выбор_языка",
    "title": "Выбор языка",
    "desc": "Задание 7: переключатель языка бота (русский / английский). Наборы ответов хранятся в "
            "<code>botResponses.ru</code> и <code>botResponses.en</code>.",
    "body": """
<div class="card">
  <h2>Чат с ботом</h2>
  <div class="row">
    <button class="pill active" id="btn-ru" onclick="switchLanguage('ru')">🇷🇺 Русский</button>
    <button class="pill" id="btn-en" onclick="switchLanguage('en')">🇬🇧 English</button>
  </div>
  <div class="out" id="chat" style="min-height:220px;max-height:320px;overflow:auto"></div>
  <div class="row">
    <input id="msg" placeholder="Введите сообщение..." style="flex:1;min-width:200px" onkeydown="if(event.key==='Enter')send()">
    <button class="btn" onclick="send()">Отправить</button>
  </div>
  <div class="out" id="out" style="min-height:auto"></div>
</div>
""",
    "script": r"""
let currentLanguage = 'ru';

const botResponses = {
  ru: {
    'привет': ['Привет! 😊', 'Здравствуй! 👋'],
    'пока': ['Пока! 👋', 'До встречи! 😊'],
    'как дела': ['Отлично! 🌟', 'Прекрасно! 💫']
  },
  en: {
    'hello': ['Hello! 😊', 'Hi there! 👋'],
    'bye': ['Bye! 👋', 'See you! 😊'],
    'how are you': ['Great! 🌟', 'Wonderful! 💫']
  }
};

function getBotResponse(msg) {
  const lower = msg.toLowerCase();
  const responses = botResponses[currentLanguage];
  for (const [keyword, answers] of Object.entries(responses)) {
    if (lower.includes(keyword)) return answers[Math.floor(Math.random() * answers.length)];
  }
  return currentLanguage === 'ru' ? 'Я не совсем понял. 🤔' : "I don't quite understand. 🤔";
}

function addMessage(text, who) {
  const chat = $('chat');
  chat.innerHTML += `<div style="margin:6px 0"><b class="${who === 'user' ? 'hl' : 'ok'}">${who === 'user' ? 'Вы' : 'Bot'}:</b> ${esc(text)}</div>`;
  chat.scrollTop = chat.scrollHeight;
}

function switchLanguage(lang) {
  currentLanguage = lang;
  $('btn-ru').classList.toggle('active', lang === 'ru');
  $('btn-en').classList.toggle('active', lang === 'en');
  addMessage(lang === 'ru' ? 'Язык переключен на русский' : 'Language switched to English', 'bot');
}

function send() {
  const input = $('msg');
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  input.value = '';
  setTimeout(() => addMessage(getBotResponse(text), 'bot'), 300);
}

addMessage('Привет! Я многоязычный бот 🌍', 'bot');
""",
})

# ============================== ПР20 ==============================
CARD_CSS = """
.card3d{width:100%;max-width:360px;aspect-ratio:1.586;border-radius:16px;padding:20px;color:#fff;
background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);box-shadow:0 12px 30px rgba(0,0,0,.25);
display:flex;flex-direction:column;justify-content:space-between;transition:transform .6s,background .3s;transform-style:preserve-3d}
.card3d.visa{background:linear-gradient(135deg,#1a1a2e,#0f3460)}
.card3d.mastercard{background:linear-gradient(135deg,#3a1c1c,#8e2de2)}
.card3d.mir{background:linear-gradient(135deg,#0f5132,#1e7e34)}
.card3d.unionpay{background:linear-gradient(135deg,#d52b1e,#b71c1c)}
.card3d.flip{transform:rotateY(180deg)}
.card3d .num{font:600 20px/1.4 Consolas,monospace;letter-spacing:2px}
.card3d .lbl{font-size:10px;letter-spacing:2px;opacity:.7;text-transform:uppercase}
.card3d .brand{font-size:22px;font-weight:700;text-align:right}
"""

CARD_FIELDS = """
<div class="row">
  <div class="card3d" id="card">
    <div class="row" style="justify-content:space-between;margin:0">
      <span class="brand" id="brand">CARD</span>
      <span class="brand" id="currency-badge"></span>
    </div>
    <div>
      <div class="lbl">Номер карты</div>
      <div class="num" id="num">•••• •••• •••• ••••</div>
    </div>
    <div class="row" style="justify-content:space-between;margin:0">
      <div><div class="lbl">Владелец</div><div id="holder">ИМЯ ФАМИЛИЯ</div></div>
      <div><div class="lbl">Срок</div><div id="expiry">MM/YY</div></div>
      <div><div class="lbl">CVV</div><div id="cvv">•••</div></div>
    </div>
  </div>
</div>
<div class="row">
  <input id="number" placeholder="0000 0000 0000 0000" maxlength="19" style="flex:1;min-width:220px">
  <input id="holder-input" placeholder="IVAN IVANOV" style="flex:1;min-width:160px">
  <input id="expiry-input" placeholder="MM/YY" maxlength="5" style="width:100px">
  <input id="cvv-input" placeholder="CVV" maxlength="4" style="width:80px">
</div>
"""

TASKS.append({
    "pr": 20, "n": 1,
    "slug": "unionpay",
    "title": "Поддержка карты UnionPay",
    "desc": "Задание 1: определение платёжной системы по префиксу. Номер, начинающийся с «62», — UnionPay "
            "со своим красно-градиентным оформлением карточки.",
    "body": CARD_FIELDS + '<div class="out" id="out"></div>',
    "css": CARD_CSS,
    "script": r"""
function getCardType(digits) {
  if (!digits) return 'unknown';
  if (digits[0] === '4') return 'visa';
  if (digits.startsWith('62')) return 'unionpay';
  if (/^5[1-5]/.test(digits)) return 'mastercard';
  if (/^220[0-4]/.test(digits)) return 'mir';
  return 'unknown';
}

const CARD_INFO = {
  visa: { icon: '💳', name: 'VISA' },
  mastercard: { icon: '💳', name: 'MasterCard' },
  mir: { icon: '💳', name: 'МИР' },
  unionpay: { icon: '💳', name: 'UnionPay' },
  unknown: { icon: '💳', name: 'CARD' }
};

function formatNumber(value) {
  const digits = value.replace(/\D/g, '').slice(0, 19);
  return digits.replace(/(.{4})/g, '$1 ').trim();
}

function maskNumber(value) {
  const digits = String(value).replace(/\D/g, '');
  let out = '';
  for (let i = 0; i < 16; i++) {
    out += digits[i] || '•';
    if (i % 4 === 3 && i < 15) out += ' ';
  }
  return out;
}

function update() {
  const digits = $('number').value.replace(/\D/g, '');
  const type = getCardType(digits);
  const info = CARD_INFO[type];
  $('num').textContent = maskNumber(digits);
  $('brand').textContent = info.icon + ' ' + info.name;
  $('card').className = 'card3d ' + type;
  $('holder').textContent = ($('holder-input').value || 'ИМЯ ФАМИЛИЯ').toUpperCase();
  $('expiry').textContent = $('expiry-input').value || 'MM/YY';
  $('cvv').textContent = '•'.repeat($('cvv-input').value.length) || '•••';
  out(`Префикс: <span class="hl">${esc(digits.slice(0, 2) || '—')}</span> → тип карты: <span class="ok">${esc(info.name)}</span>`);
}

['number', 'holder-input', 'expiry-input', 'cvv-input'].forEach(id => $(id).addEventListener('input', update));
$('number').addEventListener('input', function () { this.value = formatNumber(this.value); update(); });
$('expiry-input').addEventListener('input', function () {
  const d = this.value.replace(/\D/g, '').slice(0, 4);
  this.value = d.length > 2 ? d.slice(0, 2) + '/' + d.slice(2) : d;
});
$('number').value = '6212 3456 7890 1234';
update();
""",
})

TASKS.append({
    "pr": 20, "n": 2,
    "slug": "маска_cvv",
    "title": "Маска для CVV",
    "desc": "Задание 2: при вводе CVV показываются точки, а реальные цифры хранятся в отдельной переменной "
            "и на карточке не отображаются.",
    "body": CARD_FIELDS + """
<div class="row">
  <button class="btn gray" onclick="revealCvv()">Показать реальное значение</button>
  <button class="btn red" onclick="clearCvv()">Очистить CVV</button>
</div>
<div class="out" id="out"></div>""",
    "css": CARD_CSS,
    "script": r"""
function maskNumber(value) {
  const digits = String(value).replace(/\D/g, '');
  let out = '';
  for (let i = 0; i < 16; i++) {
    out += digits[i] || '•';
    if (i % 4 === 3 && i < 15) out += ' ';
  }
  return out;
}

let actualCvv = '';

function updateCard() {
  $('holder').textContent = ($('holder-input').value || 'ИМЯ ФАМИЛЯ').toUpperCase();
  $('expiry').textContent = $('expiry-input').value || 'MM/YY';
  $('cvv').textContent = '•'.repeat(actualCvv.length) || '•••';
  const digits = $('number').value.replace(/\D/g, '');
  $('num').textContent = maskNumber(digits);
  $('brand').textContent = '💳 CARD';
  out(`В поле ввода: <span class="hl">${'•'.repeat(actualCvv.length) || '—'}</span>
Реальных цифр сохранено: <span class="ok">${actualCvv.length}</span> (в DOM они не попадают)`);
}

$('cvv-input').addEventListener('input', function () {
  actualCvv = this.value.replace(/\D/g, '').slice(0, 4);
  this.value = '•'.repeat(actualCvv.length);
  updateCard();
});

$('number').addEventListener('input', function () {
  this.value = this.value.replace(/\D/g, '').slice(0, 19).replace(/(.{4})/g, '$1 ').trim();
  updateCard();
});
['holder-input', 'expiry-input'].forEach(id => $(id).addEventListener('input', updateCard));

function revealCvv() {
  out(`Реальное значение CVV: <span class="hl">${esc(actualCvv || '—')}</span> (хранится только в переменной)`);
}

function clearCvv() {
  actualCvv = '';
  $('cvv-input').value = '';
  updateCard();
}

updateCard();
""",
})

TASKS.append({
    "pr": 20, "n": 3,
    "slug": "автопереход",
    "title": "Автоматический переход между полями",
    "desc": "Задание 3: как только номер карты заполнен (19 символов с пробелами), фокус автоматически "
            "переходит на поле «Владелец». Аналогично — с CVV на кнопку.",
    "body": CARD_FIELDS + '<div class="out" id="out">Начните вводить номер карты.</div>',
    "css": CARD_CSS,
    "script": r"""
function maskNumber(value) {
  const digits = String(value).replace(/\D/g, '');
  let out = '';
  for (let i = 0; i < 16; i++) {
    out += digits[i] || '•';
    if (i % 4 === 3 && i < 15) out += ' ';
  }
  return out;
}

let focusLog = [];

function noteFocus(field) {
  focusLog.push(field);
  out(`Фокус перешёл на: <span class="hl">${esc(field)}</span>
История переходов: ${focusLog.map(esc).join(' → ')}`);
}

['number', 'holder-input', 'expiry-input', 'cvv-input'].forEach(id => {
  $(id).addEventListener('focus', () => noteFocus(id));
});

$('number').addEventListener('input', function () {
  this.value = this.value.replace(/\D/g, '').slice(0, 19).replace(/(.{4})/g, '$1 ').trim();
  $('num').textContent = maskNumber(this.value);
  if (this.value.length === 19) {
    $('holder-input').focus();
  }
});

$('holder-input').addEventListener('input', function () {
  $('holder').textContent = (this.value || 'ИМЯ ФАМИЛИЯ').toUpperCase();
});

$('expiry-input').addEventListener('input', function () {
  const d = this.value.replace(/\D/g, '').slice(0, 4);
  this.value = d.length > 2 ? d.slice(0, 2) + '/' + d.slice(2) : d;
  $('expiry').textContent = this.value || 'MM/YY';
});

$('cvv-input').addEventListener('input', function () {
  const d = this.value.replace(/\D/g, '').slice(0, 3);
  this.value = '•'.repeat(d.length);
  $('cvv').textContent = this.value || '•••';
  if (d.length === 3) $('number').focus();
});
""",
})

TASKS.append({
    "pr": 20, "n": 4,
    "slug": "темная_тема",
    "title": "Тёмная тема формы",
    "desc": "Задание 4: переключатель светлой и тёмной темы формы. Тема применяется к контейнеру через "
            "переключение CSS-класса.",
    "body": """
<div class="row" style="justify-content:flex-end">
  <button class="btn gray" id="theme-toggle" onclick="toggleTheme()">🌙 Тёмная тема</button>
</div>
<div id="form-wrap">
""" + CARD_FIELDS + """
</div>
<div class="out" id="out">Тема: светлая</div>""",
    "css": CARD_CSS + """
#form-wrap{border-radius:12px;padding:14px;transition:background .4s,color .4s;background:#f8fafc}
#form-wrap.dark-theme{background:#151a26;color:#e2e8f0}
#form-wrap.dark-theme input{background:#1f2937;color:#fff;border-color:#374151}
""",
    "script": r"""
function maskNumber(value) {
  const digits = String(value).replace(/\D/g, '');
  let out = '';
  for (let i = 0; i < 16; i++) {
    out += digits[i] || '•';
    if (i % 4 === 3 && i < 15) out += ' ';
  }
  return out;
}

function updateCard() {
  const digits = $('number').value.replace(/\D/g, '');
  $('num').textContent = maskNumber(digits);
  $('holder').textContent = ($('holder-input').value || 'ИМЯ ФАМИЛИЯ').toUpperCase();
  $('expiry').textContent = $('expiry-input').value || 'MM/YY';
  $('cvv').textContent = '•'.repeat($('cvv-input').value.length) || '•••';
  $('brand').textContent = '💳 CARD';
}

function toggleTheme() {
  const wrap = $('form-wrap');
  wrap.classList.toggle('dark-theme');
  const dark = wrap.classList.contains('dark-theme');
  $('theme-toggle').textContent = dark ? '☀️ Светлая тема' : '🌙 Тёмная тема';
  out(`Тема: <span class="hl">${dark ? 'тёмная' : 'светлая'}</span>`);
}

['number', 'holder-input', 'expiry-input', 'cvv-input'].forEach(id => $(id).addEventListener('input', updateCard));
$('number').addEventListener('input', function () {
  this.value = this.value.replace(/\D/g, '').slice(0, 19).replace(/(.{4})/g, '$1 ').trim();
});
$('cvv-input').addEventListener('input', function () {
  const d = this.value.replace(/\D/g, '').slice(0, 4);
  this.value = '•'.repeat(d.length);
});
updateCard();
""",
})

TASKS.append({
    "pr": 20, "n": 5,
    "slug": "сохранение_в_localstorage",
    "title": "Сохранение данных в localStorage",
    "desc": "Задание 5: введённые данные карты сохраняются в <code>localStorage</code> и восстанавливаются "
            "после перезагрузки страницы. CVV в хранилище не пишется.",
    "body": CARD_FIELDS + """
<div class="row">
  <button class="btn green" onclick="saveCardData()">💾 Сохранить</button>
  <button class="btn red" onclick="clearCardData()">Удалить сохранённое</button>
</div>
<div class="out" id="out"></div>""",
    "css": CARD_CSS,
    "script": r"""
function maskNumber(value) {
  const digits = String(value).replace(/\D/g, '');
  let out = '';
  for (let i = 0; i < 16; i++) {
    out += digits[i] || '•';
    if (i % 4 === 3 && i < 15) out += ' ';
  }
  return out;
}

const CARD_KEY = 'pr20_cardData';

function updateCard() {
  const digits = $('number').value.replace(/\D/g, '');
  $('num').textContent = maskNumber(digits);
  $('holder').textContent = ($('holder-input').value || 'ИМЯ ФАМИЛИЯ').toUpperCase();
  $('expiry').textContent = $('expiry-input').value || 'MM/YY';
  $('cvv').textContent = '•'.repeat($('cvv-input').value.length) || '•••';
  $('brand').textContent = '💳 CARD';
}

function saveCardData() {
  const data = {
    number: $('number').value,
    holder: $('holder-input').value,
    expiry: $('expiry-input').value
  };
  localStorage.setItem(CARD_KEY, JSON.stringify(data));
  out(`<span class="ok">Сохранено в localStorage:</span> ${esc(JSON.stringify(data))}
<span class="muted">CVV намеренно не сохраняется.</span>`);
}

function loadCardData() {
  try {
    const data = JSON.parse(localStorage.getItem(CARD_KEY) || 'null');
    if (!data) return;
    $('number').value = data.number || '';
    $('holder-input').value = data.holder || '';
    $('expiry-input').value = data.expiry || '';
    updateCard();
    out('<span class="ok">Данные восстановлены из localStorage</span>');
  } catch (e) {
    localStorage.removeItem(CARD_KEY);
  }
}

function clearCardData() {
  localStorage.removeItem(CARD_KEY);
  ['number', 'holder-input', 'expiry-input', 'cvv-input'].forEach(id => $(id).value = '');
  updateCard();
  out('<span class="ok">Сохранённые данные удалены</span>');
}

['number', 'holder-input', 'expiry-input', 'cvv-input'].forEach(id => $(id).addEventListener('input', updateCard));
$('number').addEventListener('input', function () {
  this.value = this.value.replace(/\D/g, '').slice(0, 19).replace(/(.{4})/g, '$1 ').trim();
});
loadCardData();
updateCard();
""",
})

TASKS.append({
    "pr": 20, "n": 6,
    "slug": "несколько_валют",
    "title": "Поддержка нескольких валют",
    "desc": "Задание 6: переключатель валют RUB / USD / EUR — выбранный символ отображается на карточке.",
    "body": """
<div class="row">
  <label>Валюта:</label>
  <select id="currency">
    <option value="₽">RUB</option>
    <option value="$">USD</option>
    <option value="€">EUR</option>
  </select>
</div>
""" + CARD_FIELDS + '<div class="out" id="out"></div>',
    "css": CARD_CSS,
    "script": r"""
function maskNumber(value) {
  const digits = String(value).replace(/\D/g, '');
  let out = '';
  for (let i = 0; i < 16; i++) {
    out += digits[i] || '•';
    if (i % 4 === 3 && i < 15) out += ' ';
  }
  return out;
}

function updateCard() {
  const digits = $('number').value.replace(/\D/g, '');
  $('num').textContent = maskNumber(digits);
  $('holder').textContent = ($('holder-input').value || 'ИМЯ ФАМИЛИЯ').toUpperCase();
  $('expiry').textContent = $('expiry-input').value || 'MM/YY';
  $('cvv').textContent = '•'.repeat($('cvv-input').value.length) || '•••';
  $('brand').textContent = '💳 CARD';
  $('currency-badge').textContent = $('currency').value;
  out(`Валюта карточки: <span class="hl">${esc($('currency').value)}</span>
Код: <span class="ok">${esc($('currency').selectedOptions[0].textContent)}</span>`);
}

$('currency').addEventListener('change', updateCard);
['number', 'holder-input', 'expiry-input', 'cvv-input'].forEach(id => $(id).addEventListener('input', updateCard));
$('number').addEventListener('input', function () {
  this.value = this.value.replace(/\D/g, '').slice(0, 19).replace(/(.{4})/g, '$1 ').trim();
});
$('cvv-input').addEventListener('input', function () {
  const d = this.value.replace(/\D/g, '').slice(0, 4);
  this.value = '•'.repeat(d.length);
});
updateCard();
""",
})

TASKS.append({
    "pr": 20, "n": 7,
    "slug": "3d_анимация",
    "title": "3D-анимация карточки",
    "desc": "Задание 7: карточка поворачивается в 3D при наведении и переворачивается на 180° по кнопке "
            "(показывает «оборот» с CVV).",
    "body": """
<div class="row">
  <button class="btn" onclick="flip()">🔄 Перевернуть карточку</button>
  <button class="btn gray" onclick="reset()">Сброс</button>
</div>
""" + CARD_FIELDS + """
<div class="out" id="out">Наведите курсор на карточку или нажмите «Перевернуть».</div>""",
    "css": CARD_CSS + """
.card3d{transform-style:preserve-3d;perspective:1000px}
#card:hover{transform:rotateY(12deg) rotateX(6deg) scale(1.02)}
""",
    "script": r"""
function maskNumber(value) {
  const digits = String(value).replace(/\D/g, '');
  let out = '';
  for (let i = 0; i < 16; i++) {
    out += digits[i] || '•';
    if (i % 4 === 3 && i < 15) out += ' ';
  }
  return out;
}

let flipped = false;

function flip() {
  flipped = !flipped;
  $('card').classList.toggle('flip', flipped);
  out(`Карточка перевёрнута: <span class="hl">${flipped ? 'да' : 'нет'}</span>`);
}

function reset() {
  flipped = false;
  $('card').classList.remove('flip');
  $('card').style.transform = '';
  out('Анимация сброшена');
}

function updateCard() {
  const digits = $('number').value.replace(/\D/g, '');
  $('num').textContent = maskNumber(digits);
  $('holder').textContent = ($('holder-input').value || 'ИМЯ ФАМИЛИЯ').toUpperCase();
  $('expiry').textContent = $('expiry-input').value || 'MM/YY';
  $('cvv').textContent = '•'.repeat($('cvv-input').value.length) || '•••';
  $('brand').textContent = '💳 CARD';
}

['number', 'holder-input', 'expiry-input', 'cvv-input'].forEach(id => $(id).addEventListener('input', updateCard));
$('number').addEventListener('input', function () {
  this.value = this.value.replace(/\D/g, '').slice(0, 19).replace(/(.{4})/g, '$1 ').trim();
});
$('cvv-input').addEventListener('input', function () {
  const d = this.value.replace(/\D/g, '').slice(0, 4);
  this.value = '•'.repeat(d.length);
});
updateCard();
""",
})

# ============================== ПР21 ==============================
GOS_BASE = """
<div class="card">
  <h2>Вход через Госуслуги</h2>
  <div class="row">
    <input id="login" placeholder="Логин" value="user123" style="min-width:150px">
    <input id="password" placeholder="Пароль" type="password" value="password" style="min-width:150px">
    <button class="btn" onclick="login()">Войти</button>
    <span id="auth-status" class="muted">не авторизован</span>
  </div>
</div>
"""

GOS_CSS = """
.service{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:12px;margin:8px 0;cursor:pointer;transition:.2s}
.service:hover{border-color:#1a73e8;background:#eef6ff}
.service.active{border-color:#1a73e8;box-shadow:0 0 0 2px #c7d2fe}
.badge-status{font-size:12px;padding:2px 10px;border-radius:999px;background:#e0f2fe;color:#075985}
.badge-status.done{background:#dcfce7;color:#166534}
"""

TASKS.append({
    "pr": 21, "n": 1,
    "slug": "новая_услуга",
    "title": "Новая услуга в каталоге",
    "desc": "Задание 1: в <code>servicesDB</code> добавлена услуга «Запись к врачу» с описанием, статусом, "
            "списком поликлиник и количеством свободных слотов.",
    "body": GOS_BASE + """
<div class="card">
  <h2>Каталог услуг</h2>
  <div id="services"></div>
  <div class="out" id="out">Выберите услугу.</div>
</div>""",
    "css": GOS_CSS,
    "script": r"""
let authorized = false;

const servicesDB = {
  passport: {
    name: 'Замена паспорта',
    description: 'Замена паспорта гражданина РФ по достижении 20 или 45 лет',
    status: 'доступно',
    offices: ['МФЦ Центральный', 'МФЦ Северный'],
    free_slots: 8
  },
  doctor: {
    name: 'Запись к врачу',
    description: 'Запись на приём к врачу через электронную регистратуру',
    status: 'доступно',
    clinics: ['Поликлиника №1', 'Поликлиника №2'],
    free_slots: 15
  },
  driver: {
    name: 'Замена водительского удостоверения',
    description: 'Замена водительского удостоверения по истечении срока действия',
    status: 'доступно',
    offices: ['МРЭО ГИБДД №1'],
    free_slots: 4
  }
};

function renderServices() {
  $('services').innerHTML = Object.entries(servicesDB).map(([id, s]) => `
    <div class="service" onclick="showService('${id}')" id="svc-${id}">
      <b>${esc(s.name)}</b>
      <span class="badge-status">${esc(s.status)}</span>
      <div class="muted">Свободных слотов: ${s.free_slots}</div>
    </div>`).join('');
}

function login() {
  authorized = $('login').value === 'user123' && $('password').value === 'password';
  $('auth-status').textContent = authorized ? 'авторизован' : 'не авторизован';
  $('auth-status').className = authorized ? 'ok' : 'muted';
  out(authorized ? '<span class="ok">Вход выполнен</span>' : '<span class="err">Неверный логин или пароль</span>');
}

function showService(id) {
  document.querySelectorAll('.service').forEach(el => el.classList.remove('active'));
  $('svc-' + id).classList.add('active');
  const s = servicesDB[id];
  const places = s.clinics || s.offices || [];
  out(`<b>${esc(s.name)}</b>
${esc(s.description)}
Статус: <span class="ok">${esc(s.status)}</span> · свободных слотов: <span class="hl">${s.free_slots}</span>
${places.map(p => '• ' + esc(p)).join('\n')}`);
}

renderServices();
""",
})

TASKS.append({
    "pr": 21, "n": 2,
    "slug": "статус_заявок",
    "title": "Отображение статуса заявок",
    "desc": "Задание 2: при выборе услуги показывается не только описание, но и статус заявки из "
            "<code>historyDB</code>, если заявка по этой услуге уже есть.",
    "body": GOS_BASE + """
<div class="card">
  <h2>Услуги и статус заявок</h2>
  <div id="services"></div>
  <div class="out" id="out">Выберите услугу.</div>
</div>""",
    "css": GOS_CSS,
    "script": r"""
let authorized = false;

const servicesDB = {
  passport: { name: 'Замена паспорта', description: 'Замена паспорта гражданина РФ', status: 'доступно' },
  doctor: { name: 'Запись к врачу', description: 'Запись через электронную регистратуру', status: 'доступно' },
  benefits: { name: 'Детские выплаты', description: 'Ежемесячная выплата на ребёнка', status: 'доступно' }
};

const historyDB = [
  { id: 1, service: 'Замена паспорта', date: '12.10.2026', status: 'в обработке' },
  { id: 2, service: 'Детские выплаты', date: '01.10.2026', status: 'исполнено' }
];

function renderServices() {
  $('services').innerHTML = Object.entries(servicesDB).map(([id, s]) => {
    const app = historyDB.find(h => h.service === s.name);
    return `<div class="service" onclick="showService('${id}')">
      <b>${esc(s.name)}</b>
      ${app ? `<span class="badge-status ${app.status === 'исполнено' ? 'done' : ''}">${esc(app.status)}</span>` : '<span class="muted">заявок нет</span>'}
    </div>`;
  }).join('');
}

function login() {
  authorized = $('login').value === 'user123' && $('password').value === 'password';
  $('auth-status').textContent = authorized ? 'авторизован' : 'не авторизован';
  $('auth-status').className = authorized ? 'ok' : 'muted';
}

function showService(id) {
  const s = servicesDB[id];
  const apps = historyDB.filter(h => h.service === s.name);
  out(`<b>${esc(s.name)}</b>
${esc(s.description)}

<span class="hl">Заявки по услуге:</span>
${apps.length ? apps.map(a => `№${a.id} от ${a.date} — <span class="ok">${esc(a.status)}</span>`).join('\n') : 'Заявок пока нет.'}`);
}

renderServices();
""",
})

TASKS.append({
    "pr": 21, "n": 3,
    "slug": "отправка_заявления",
    "title": "Отправка заявления",
    "desc": "Задание 3: в деталях услуги есть кнопка «Подать заявление». Проверяется авторизация, "
            "запись добавляется в <code>historyDB</code>, показывается уведомление об успехе.",
    "body": GOS_BASE + """
<div class="card">
  <h2>Услуги</h2>
  <div id="services"></div>
  <div id="details"></div>
  <div class="out" id="out">Войдите и выберите услугу.</div>
</div>""",
    "css": GOS_CSS,
    "script": r"""
let authorized = false;
let selected = null;

const servicesDB = {
  passport: { name: 'Замена паспорта', description: 'Замена паспорта гражданина РФ' },
  doctor: { name: 'Запись к врачу', description: 'Запись через электронную регистратуру' },
  benefits: { name: 'Детские выплаты', description: 'Ежемесячная выплата на ребёнка' }
};

const historyDB = [
  { id: 1, service: 'Детские выплаты', date: '01.10.2026', status: 'исполнено' }
];

function renderServices() {
  $('services').innerHTML = Object.entries(servicesDB).map(([id, s]) =>
    `<div class="service" onclick="selectService('${id}')"><b>${esc(s.name)}</b><div class="muted">${esc(s.description)}</div></div>`
  ).join('');
}

function login() {
  authorized = $('login').value === 'user123' && $('password').value === 'password';
  $('auth-status').textContent = authorized ? 'авторизован' : 'не авторизован';
  $('auth-status').className = authorized ? 'ok' : 'muted';
  if (selected) selectService(selected);
}

function selectService(id) {
  selected = id;
  const s = servicesDB[id];
  $('details').innerHTML = `
    <div class="item">
      <div><b>${esc(s.name)}</b><div class="muted">${esc(s.description)}</div></div>
      <button class="btn green" onclick="submitApplication('${id}')">Подать заявление</button>
    </div>`;
  out(`Выбрана услуга: <span class="hl">${esc(s.name)}</span>`);
}

function submitApplication(id) {
  if (!authorized) {
    out('<span class="err">Сначала авторизуйтесь через Госуслуги</span>');
    return;
  }
  const app = {
    id: Date.now(),
    service: servicesDB[id].name,
    date: new Date().toLocaleDateString('ru-RU'),
    status: 'подано'
  };
  historyDB.unshift(app);
  out(`<span class="ok">✅ Заявление подано!</span>
${esc(app.service)} · №${app.id} · ${app.date} · статус: ${esc(app.status)}`);
}

renderServices();
""",
})

TASKS.append({
    "pr": 21, "n": 4,
    "slug": "вход_по_снилс",
    "title": "Вход по СНИЛС",
    "desc": "Задание 4: альтернативная форма входа по СНИЛС вместо логина и пароля. "
            "Номер проверяется по маске и контрольной сумме (упрощённо — по эталону).",
    "body": """
<div class="card">
  <h2>Вход по СНИЛС</h2>
  <div class="row">
    <input id="snils" placeholder="123-456-789 00" value="123-456-789 00" style="min-width:220px">
    <button class="btn" onclick="loginSnils()">Войти по СНИЛС</button>
  </div>
  <p class="muted">Эталон для демо: 123-456-789 00</p>
  <div class="out" id="out">Введите СНИЛС.</div>
</div>
<div class="card">
  <h2>Доступные услуги</h2>
  <div id="services"></div>
</div>""",
    "css": GOS_CSS,
    "script": r"""
const ETALON = '123-456-789 00';
let authorized = false;

const services = ['Замена паспорта', 'Запись к врачу', 'Детские выплаты'];

function formatSnils(value) {
  const d = value.replace(/\D/g, '').slice(0, 11);
  if (d.length <= 3) return d;
  if (d.length <= 6) return d.slice(0, 3) + '-' + d.slice(3);
  if (d.length <= 9) return d.slice(0, 3) + '-' + d.slice(3, 6) + '-' + d.slice(6);
  return d.slice(0, 3) + '-' + d.slice(3, 6) + '-' + d.slice(6, 9) + ' ' + d.slice(9);
}

$('snils').addEventListener('input', function () {
  this.value = formatSnils(this.value);
});

function loginSnils() {
  const value = $('snils').value.trim();
  authorized = value === ETALON;
  $('services').innerHTML = authorized
    ? services.map(s => `<div class="item"><span>${esc(s)}</span><span class="ok">доступно</span></div>`).join('')
    : '';
  out(authorized
    ? '<span class="ok">Авторизация по СНИЛС успешна</span>'
    : '<span class="err">СНИЛС не найден в ЕСИА (для демо: 123-456-789 00)</span>');
}
""",
})

TASKS.append({
    "pr": 21, "n": 5,
    "slug": "личный_кабинет",
    "title": "Личный кабинет пользователя",
    "desc": "Задание 5: блок с личными данными — ФИО, контакты, СНИЛС, паспортные данные и история обращений "
            "из <code>userDB</code> и <code>historyDB</code>.",
    "body": GOS_BASE + """
<div class="card" id="cabinet" style="display:none">
  <h2>Личный кабинет</h2>
  <div id="user"></div>
  <h2 style="margin-top:16px">История обращений</h2>
  <div id="history"></div>
</div>
<div class="out" id="out">Войдите, чтобы увидеть личный кабинет.</div>""",
    "css": GOS_CSS,
    "script": r"""
const userDB = {
  fio: 'Иванов Иван Иванович',
  birth: '15.03.1990',
  email: 'ivanov@example.ru',
  phone: '+7 (900) 123-45-67',
  snils: '123-456-789 00',
  passport: '45 12 № 345678, выдан ОВД Тверского района 20.04.2010'
};

const historyDB = [
  { id: 101, service: 'Замена паспорта', date: '12.10.2026', status: 'в обработке' },
  { id: 102, service: 'Детские выплаты', date: '01.10.2026', status: 'исполнено' },
  { id: 103, service: 'Запись к врачу', date: '25.09.2026', status: 'исполнено' }
];

function login() {
  const ok = $('login').value === 'user123' && $('password').value === 'password';
  $('auth-status').textContent = ok ? 'авторизован' : 'не авторизован';
  $('auth-status').className = ok ? 'ok' : 'muted';
  if (!ok) {
    $('cabinet').style.display = 'none';
    out('<span class="err">Неверный логин или пароль</span>');
    return;
  }
  $('cabinet').style.display = 'block';
  $('user').innerHTML = `
    <div class="item"><span class="muted">ФИО</span><b>${esc(userDB.fio)}</b></div>
    <div class="item"><span class="muted">Дата рождения</span><b>${esc(userDB.birth)}</b></div>
    <div class="item"><span class="muted">Телефон</span><b>${esc(userDB.phone)}</b></div>
    <div class="item"><span class="muted">E-mail</span><b>${esc(userDB.email)}</b></div>
    <div class="item"><span class="muted">СНИЛС</span><b>${esc(userDB.snils)}</b></div>
    <div class="item"><span class="muted">Паспорт</span><b>${esc(userDB.passport)}</b></div>`;
  $('history').innerHTML = historyDB.map(h =>
    `<div class="item"><span>№${h.id} · ${esc(h.service)} · ${h.date}</span><span class="badge-status ${h.status === 'исполнено' ? 'done' : ''}">${esc(h.status)}</span></div>`
  ).join('');
  out('<span class="ok">Личный кабинет загружен</span>');
}
""",
})

TASKS.append({
    "pr": 21, "n": 6,
    "slug": "система_оповещений",
    "title": "Система оповещений",
    "desc": "Задание 6: имитация уведомлений Госуслуг — о новой заявке и об изменении статуса, "
            "со счётчиком непрочитанных и отметкой «прочитано».",
    "body": GOS_BASE + """
<div class="card">
  <h2>Уведомления <span class="badge-status" id="unread">0</span></h2>
  <div class="row">
    <button class="btn" onclick="pushNotification('new')">Новая заявка</button>
    <button class="btn orange" onclick="pushNotification('status')">Изменение статуса</button>
    <button class="btn gray" onclick="readAll()">Прочитать все</button>
  </div>
  <div id="list"></div>
  <div class="out" id="out"></div>
</div>""",
    "css": GOS_CSS,
    "script": r"""
const notifications = [];
let seq = 0;

const templates = {
  new: () => ({ title: 'Новая заявка', text: 'Заявление №' + (1000 + seq) + ' зарегистрировано' }),
  status: () => ({ title: 'Статус изменён', text: 'Заявление №' + (1000 + seq) + ' перешло в статус «в обработке»' })
};

function render() {
  const unread = notifications.filter(n => !n.read).length;
  $('unread').textContent = unread;
  $('unread').className = 'badge-status' + (unread ? '' : ' done');
  $('list').innerHTML = notifications.length ? notifications.map(n => `
    <div class="item" style="${n.read ? 'opacity:.6' : ''}">
      <div><b>${esc(n.title)}</b><div class="muted">${esc(n.text)} · ${n.time}</div></div>
      ${n.read ? '<span class="ok">прочитано</span>' : `<button class="btn" onclick="markRead(${n.id})">Прочитать</button>`}
    </div>`).join('') : '<p class="muted">Уведомлений нет.</p>';
}

function pushNotification(kind) {
  seq++;
  const t = templates[kind]();
  notifications.unshift({ id: seq, ...t, read: false, time: new Date().toLocaleTimeString('ru-RU') });
  render();
  out(`<span class="ok">Добавлено уведомление: ${esc(t.title)}</span>`);
}

function markRead(id) {
  const n = notifications.find(x => x.id === id);
  if (n) n.read = true;
  render();
}

function readAll() {
  notifications.forEach(n => n.read = true);
  render();
  out('<span class="ok">Все уведомления прочитаны</span>');
}

render();
""",
})

TASKS.append({
    "pr": 21, "n": 7,
    "slug": "виджет_для_встраивания",
    "title": "Виджет для встраивания",
    "desc": "Задание 7: самовызывающаяся функция (IIFE), которая находит контейнер <code>#gosuslugi-widget</code> "
            "и рендерит виджет ПОС. Такой код можно скопировать и вставить на любой сайт.",
    "body": """
<div class="card">
  <h2>Предпросмотр виджета</h2>
  <div id="gosuslugi-widget"></div>
  <div class="row">
    <button class="btn" onclick="showCode()">Показать код для вставки</button>
  </div>
  <div class="out" id="out"></div>
</div>
<div class="card">
  <h2>Отправка обращения</h2>
  <div class="row">
    <input id="fb-name" placeholder="Ваше имя" style="min-width:180px">
    <input id="fb-text" placeholder="Текст обращения" style="flex:1;min-width:240px">
    <button class="btn green" onclick="sendFeedback()">Отправить</button>
  </div>
</div>""",
    "css": GOS_CSS + """
#gosuslugi-widget{background:#eef6ff;border:1px solid #c9e3ff;border-radius:12px;padding:16px}
#gosuslugi-widget h3{color:#1a56a0;margin-bottom:6px}
""",
    "script": r"""
let widgetCounter = 0;

(function initWidget() {
  const container = document.getElementById('gosuslugi-widget');
  if (!container) return;

  container.innerHTML = `
    <h3>Платформа обратной связи</h3>
    <p class="muted">Виджет встроен на страницу сайта. Сообщений отправлено: <b id="fb-count">0</b></p>
    <div class="row">
      <span class="pill active">Сообщить о проблеме</span>
      <span class="pill">Задать вопрос</span>
    </div>`;
})();

function sendFeedback() {
  const name = $('fb-name').value.trim() || 'Аноним';
  const text = $('fb-text').value.trim();
  if (!text) { out('<span class="err">Введите текст обращения</span>'); return; }
  widgetCounter++;
  $('fb-count').textContent = widgetCounter;
  $('fb-text').value = '';
  out(`<span class="ok">Обращение принято</span>
От: ${esc(name)}
Текст: ${esc(text)}
Номер обращения: ПОС-${String(widgetCounter).padStart(4, '0')}`);
}

function showCode() {
  out(`<pre class="code" style="max-height:240px">&lt;div id="gosuslugi-widget"&gt;&lt;/div&gt;
&lt;script&gt;
(function() {
  const container = document.getElementById('gosuslugi-widget');
  if (!container) return;
  container.innerHTML = renderWidget();
})();
&lt;/script&gt;</pre>`);
}
""",
})
