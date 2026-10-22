# -*- coding: utf-8 -*-
"""Задачи ПР28–ПР32."""

TASKS = []

# ============================== ПР28 ==============================
THEME_CSS = """
.theme-page{border-radius:14px;padding:18px;transition:background .5s,color .5s}
.theme-card{border-radius:12px;padding:14px 16px;margin:10px 0;box-shadow:0 2px 8px rgba(0,0,0,.06);transition:all .5s cubic-bezier(.4,0,.2,1)}
.switch{position:relative;display:inline-block;width:52px;height:28px;vertical-align:middle}
.switch input{display:none}
.slider{position:absolute;inset:0;background:#cbd5e1;border-radius:999px;cursor:pointer;transition:.3s}
.slider:before{content:'';position:absolute;width:22px;height:22px;left:3px;top:3px;background:#fff;border-radius:50%;transition:.3s}
.switch input:checked + .slider{background:#1a73e8}
.switch input:checked + .slider:before{transform:translateX(24px)}
.theme-icon{display:inline-block;transition:transform .5s}
.theme-icon.dark{transform:rotate(180deg)}
.swatches{display:flex;gap:10px;flex-wrap:wrap}
.swatch{width:34px;height:34px;border-radius:50%;border:3px solid transparent;cursor:pointer}
.swatch.active{border-color:#0f172a;box-shadow:0 0 0 2px #fff inset}
"""

TASKS.append({
    "pr": 28, "n": 1,
    "slug": "четвертая_карточка",
    "title": "React: четвёртая карточка",
    "desc": "Задание 1: добавлена четвёртая карточка с уникальным заголовком и описанием. Все карточки — "
            "один компонент <code>Card</code>, получающий пропсы <code>isDark</code>, <code>title</code> и "
            "<code>description</code>.",
    "body": '<div id="root"></div>',
    "css": THEME_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const themes = {
  light: { background: '#f0f2f5', text: '#111827', cardBg: '#ffffff', cardText: '#333333' },
  dark: { background: '#111827', text: '#f9fafb', cardBg: '#1f2937', cardText: '#e5e7eb' }
};

function Card({ isDark, title, description }) {
  const t = themes[isDark ? 'dark' : 'light'];
  return (
    <div className="theme-card" style={{ background: t.cardBg, color: t.cardText }}>
      <h3 style={{ marginBottom: 6 }}>{title}</h3>
      <p style={{ fontSize: 14, lineHeight: 1.55 }}>{description}</p>
    </div>
  );
}

function App() {
  const [isDark, setIsDark] = useState(false);
  const t = themes[isDark ? 'dark' : 'light'];

  return (
    <div className="theme-page" style={{ background: t.background, color: t.text }}>
      <div className="card" style={{ background: t.cardBg, color: t.cardText, border: 'none' }}>
        <h2>Карточки и тема</h2>
        <label>
          <span className={isDark ? 'theme-icon dark' : 'theme-icon'}>{isDark ? '🌙' : '☀️'}</span>{' '}
          Тёмная тема
        </label>
        <label className="switch" style={{ marginLeft: 10 }}>
          <input type="checkbox" checked={isDark} onChange={() => setIsDark(!isDark)} />
          <span className="slider"></span>
        </label>
      </div>

      <Card isDark={isDark} title="Карточка 1" description="Первая карточка с описанием. Она автоматически меняет тему." />
      <Card isDark={isDark} title="Карточка 2" description="Вторая карточка использует те же пропсы и тот же компонент." />
      <Card isDark={isDark} title="Карточка 3" description="Третья карточка — ещё один экземпляр компонента Card." />
      <Card isDark={isDark} title="Карточка 4" description="Четвёртая карточка добавлена в задании 1: любое количество карточек меняет тему одновременно." />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 28, "n": 2,
    "slug": "кнопка_переключения_темы",
    "title": "React: кнопка переключения темы",
    "desc": "Задание 2: помимо ползунка добавлена обычная кнопка «Переключить тему». Её текст зависит от "
            "текущей темы.",
    "body": '<div id="root"></div>',
    "css": THEME_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const themes = {
  light: { background: '#f0f2f5', text: '#111827', cardBg: '#ffffff' },
  dark: { background: '#111827', text: '#f9fafb', cardBg: '#1f2937' }
};

function App() {
  const [isDark, setIsDark] = useState(false);
  const t = themes[isDark ? 'dark' : 'light'];
  const toggleTheme = () => setIsDark(prev => !prev);

  return (
    <div className="theme-page" style={{ background: t.background, color: t.text }}>
      <div className="card" style={{ background: t.cardBg, color: t.text, border: 'none' }}>
        <h2>Переключение темы</h2>
        <div className="btn-row" style={{ justifyContent: 'flex-start' }}>
          <label className="switch">
            <input type="checkbox" checked={isDark} onChange={toggleTheme} />
            <span className="slider"></span>
          </label>
          <button
            onClick={toggleTheme}
            style={{
              padding: '10px 20px',
              backgroundColor: isDark ? '#555' : '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: 5,
              cursor: 'pointer'
            }}
          >
            {isDark ? 'Переключить на светлую' : 'Переключить на тёмную'}
          </button>
        </div>
        <p style={{ marginTop: 14 }}>Текущая тема: <b>{isDark ? 'тёмная' : 'светлая'}</b></p>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 28, "n": 3,
    "slug": "тема_в_localstorage",
    "title": "React: сохранение темы в localStorage",
    "desc": "Задание 3: выбранная тема сохраняется в <code>localStorage</code> и восстанавливается при загрузке "
            "через <code>useEffect</code>.",
    "body": '<div id="root"></div>',
    "css": THEME_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

const themes = {
  light: { background: '#f0f2f5', text: '#111827', cardBg: '#ffffff' },
  dark: { background: '#111827', text: '#f9fafb', cardBg: '#1f2937' }
};

function App() {
  const [isDark, setIsDark] = useState(() => localStorage.getItem('pr28_theme') === 'dark');

  useEffect(() => {
    localStorage.setItem('pr28_theme', isDark ? 'dark' : 'light');
  }, [isDark]);

  const t = themes[isDark ? 'dark' : 'light'];

  return (
    <div className="theme-page" style={{ background: t.background, color: t.text }}>
      <div className="card" style={{ background: t.cardBg, color: t.text, border: 'none' }}>
        <h2>Тема с сохранением</h2>
        <div className="btn-row" style={{ justifyContent: 'flex-start' }}>
          <label className="switch">
            <input type="checkbox" checked={isDark} onChange={(e) => setIsDark(e.target.checked)} />
            <span className="slider"></span>
          </label>
          <span>Тёмная тема</span>
        </div>
        <p className="muted" style={{ marginTop: 12 }}>
          В localStorage: <code>pr28_theme = {isDark ? 'dark' : 'light'}</code>. Перезагрузите страницу — тема сохранится.
        </p>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 28, "n": 4,
    "slug": "анимация_темы",
    "title": "React: анимация при смене темы",
    "desc": "Задание 4: плавные CSS-переходы для фона и карточек, иконка темы поворачивается на 180°.",
    "body": '<div id="root"></div>',
    "css": THEME_CSS + """
@keyframes themeFade{from{opacity:.35;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.theme-card{animation:themeFade .45s ease both}
""",
    "react": True,
    "jsx": r"""
const { useState } = React;

const themes = {
  light: { background: '#f0f2f5', text: '#111827', cardBg: '#ffffff' },
  dark: { background: '#111827', text: '#f9fafb', cardBg: '#1f2937' }
};

function App() {
  const [isDark, setIsDark] = useState(false);
  const t = themes[isDark ? 'dark' : 'light'];

  return (
    <div className="theme-page" style={{ background: t.background, color: t.text }}>
      <div className="card" style={{ background: t.cardBg, color: t.text, border: 'none' }}>
        <h2>
          <span className={isDark ? 'theme-icon dark' : 'theme-icon'} style={{ fontSize: 26 }}>
            {isDark ? '🌙' : '☀️'}
          </span>{' '}
          Анимация темы
        </h2>
        <div className="btn-row" style={{ justifyContent: 'flex-start' }}>
          <label className="switch">
            <input type="checkbox" checked={isDark} onChange={(e) => setIsDark(e.target.checked)} />
            <span className="slider"></span>
          </label>
          <span>Плавный переход: .5s cubic-bezier(.4,0,.2,1)</span>
        </div>
      </div>
      <div className="theme-card" key={String(isDark)} style={{ background: t.cardBg, color: t.text }}>
        <h3>Карточка с анимацией появления</h3>
        <p style={{ fontSize: 14 }}>При смене темы карточка плавно появляется заново, а иконка поворачивается.</p>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 28, "n": 5,
    "slug": "настройки_акцентного_цвета",
    "title": "React: компонент ThemeSettings",
    "desc": "Задание 5: отдельный компонент <code>ThemeSettings</code> позволяет выбрать акцентный цвет; "
            "цвет применяется к заголовку, кнопке и полосе акцента.",
    "body": '<div id="root"></div>',
    "css": THEME_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function ThemeSettings({ accentColor, setAccentColor }) {
  const colors = ['#4CAF50', '#2196F3', '#f44336', '#FF9800', '#9C27B0'];
  return (
    <div>
      <p style={{ marginBottom: 8 }}>Выберите акцентный цвет:</p>
      <div className="swatches">
        {colors.map(color => (
          <button
            key={color}
            className={accentColor === color ? 'swatch active' : 'swatch'}
            onClick={() => setAccentColor(color)}
            style={{ backgroundColor: color }}
            title={color}
          />
        ))}
      </div>
    </div>
  );
}

function App() {
  const [accentColor, setAccentColor] = useState('#4CAF50');

  return (
    <div className="card">
      <h2 style={{ color: accentColor }}>Настройки темы</h2>
      <ThemeSettings accentColor={accentColor} setAccentColor={setAccentColor} />
      <div style={{ height: 6, background: accentColor, borderRadius: 999, margin: '16px 0' }}></div>
      <button style={{ background: accentColor, color: '#fff', border: 'none', borderRadius: 8, padding: '10px 18px', cursor: 'pointer' }}>
        Кнопка с акцентным цветом
      </button>
      <p className="muted" style={{ marginTop: 12 }}>Акцент: <code>{accentColor}</code></p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 28, "n": 6,
    "slug": "три_темы",
    "title": "React: три темы",
    "desc": "Задание 6: вместо булева <code>isDark</code> используется строка "
            "<code>theme: 'light' | 'dark' | 'blue'</code>. Для каждой темы свои цвета.",
    "body": '<div id="root"></div>',
    "css": THEME_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const themes = {
  light: { background: '#f0f2f5', text: '#000000', cardBg: '#ffffff', cardText: '#333333' },
  dark: { background: '#1a1a1a', text: '#ffffff', cardBg: '#2d2d2d', cardText: '#ffffff' },
  blue: { background: '#e3f2fd', text: '#0d47a1', cardBg: '#ffffff', cardText: '#0d47a1' }
};

const names = { light: 'Светлая', dark: 'Тёмная', blue: 'Синяя' };

function App() {
  const [theme, setTheme] = useState('light');
  const currentTheme = themes[theme];

  return (
    <div className="theme-page" style={{ background: currentTheme.background, color: currentTheme.text }}>
      <div className="card" style={{ background: currentTheme.cardBg, color: currentTheme.cardText, border: 'none' }}>
        <h2>Три темы</h2>
        <div className="btn-row" style={{ justifyContent: 'flex-start' }}>
          {Object.keys(themes).map(key => (
            <button
              key={key}
              className="pill"
              onClick={() => setTheme(key)}
              style={theme === key ? { background: currentTheme.text, color: currentTheme.cardBg, borderColor: currentTheme.text } : {}}
            >
              {names[key]}
            </button>
          ))}
        </div>
        <p style={{ marginTop: 14 }}>Текущая тема: <b>{names[theme]}</b> (<code>{theme}</code>)</p>
      </div>
      <div className="theme-card" style={{ background: currentTheme.cardBg, color: currentTheme.cardText }}>
        Карточка автоматически получает цвета выбранной темы.
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 28, "n": 7,
    "slug": "авто_тема_по_времени",
    "title": "React: тема по времени суток",
    "desc": "Задание 7: с 6:00 до 18:00 — светлая тема, иначе тёмная. Есть переключатель «Авто / Ручной режим».",
    "body": '<div id="root"></div>',
    "css": THEME_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

const themes = {
  light: { background: '#f0f2f5', text: '#111827', cardBg: '#ffffff' },
  dark: { background: '#111827', text: '#f9fafb', cardBg: '#1f2937' }
};

function isNightNow() {
  const hour = new Date().getHours();
  return hour < 6 || hour >= 18;
}

function App() {
  const [auto, setAuto] = useState(true);
  const [isDark, setIsDark] = useState(isNightNow);
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    if (auto) setIsDark(isNightNow());
  }, [auto]);

  const t = themes[isDark ? 'dark' : 'light'];
  const hour = now.getHours();

  return (
    <div className="theme-page" style={{ background: t.background, color: t.text }}>
      <div className="card" style={{ background: t.cardBg, color: t.text, border: 'none' }}>
        <h2>Тема по времени суток</h2>
        <div className="btn-row" style={{ justifyContent: 'flex-start' }}>
          <button className={auto ? 'pill active' : 'pill'} onClick={() => setAuto(true)}>Авто</button>
          <button className={!auto ? 'pill active' : 'pill'} onClick={() => setAuto(false)}>Ручной режим</button>
          {!auto && (
            <label className="switch">
              <input type="checkbox" checked={isDark} onChange={(e) => setIsDark(e.target.checked)} />
              <span className="slider"></span>
            </label>
          )}
        </div>
        <p style={{ marginTop: 14 }}>Сейчас: <b>{now.toLocaleTimeString('ru-RU')}</b> (час: {hour})</p>
        <p>Правило: 6:00–18:00 — светлая, 18:00–6:00 — тёмная.</p>
        <p className="muted">Режим: {auto ? 'автоматический' : 'ручной'} · тема: {isDark ? 'тёмная' : 'светлая'}</p>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

# ============================== ПР29 ==============================
TIMER_CSS = """
.timer{max-width:460px;margin:0 auto;text-align:center}
.time{font-size:58px;font-weight:700;font-variant-numeric:tabular-nums;color:#1a73e8;line-height:1.1;margin:8px 0}
.timer-btns{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:12px 0}
.timer-row{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;align-items:center;margin:10px 0}
.finished{color:#f44336}
.multi-timer{border:1px solid #e2e8f0;border-radius:10px;padding:10px 14px;margin:8px 0;text-align:left}
.phase{display:inline-block;padding:4px 14px;border-radius:999px;font-weight:600;font-size:14px}
.phase.work{background:#dcfce7;color:#166534}
.phase.rest{background:#e0f2fe;color:#075985}
"""

TASKS.append({
    "pr": 29, "n": 1,
    "slug": "звук_по_завершении",
    "title": "React: звук при завершении таймера",
    "desc": "Задание 1: при достижении нуля проигрывается звук через Web Audio API (осциллятор 800 Гц, 0.5 c).",
    "body": '<div id="root"></div>',
    "css": TIMER_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect, useRef } = React;

function playSound() {
  try {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    gainNode.gain.value = 0.3;
    oscillator.start();
    setTimeout(() => { oscillator.stop(); audioContext.close(); }, 500);
  } catch (e) {
    console.warn('Звук недоступен:', e);
  }
}

function App() {
  const [time, setTime] = useState(10);
  const [initial, setInitial] = useState(10);
  const [active, setActive] = useState(false);
  const [finished, setFinished] = useState(false);

  useEffect(() => {
    if (!active) return;
    const id = setInterval(() => setTime(t => Math.max(0, t - 1)), 1000);
    return () => clearInterval(id);
  }, [active]);

  useEffect(() => {
    if (time === 0 && active) {
      setActive(false);
      setFinished(true);
      playSound();
    }
  }, [time, active]);

  const start = () => {
    if (time === 0) setTime(initial);
    setFinished(false);
    setActive(true);
  };

  return (
    <div className="card timer">
      <h2>Таймер со звуком</h2>
      <div className={finished ? 'time finished' : 'time'}>
        {String(Math.floor(time / 60)).padStart(2, '0')}:{String(time % 60).padStart(2, '0')}
      </div>
      <div className="timer-row">
        <button className="rbtn" onClick={() => setInitial(i => { const v = Math.min(99, i + 5); if (!active) setTime(v); return v; })}>+5 сек</button>
        <button className="rbtn" onClick={() => setInitial(i => { const v = Math.max(5, i - 5); if (!active) setTime(v); return v; })}>−5 сек</button>
      </div>
      <div className="timer-btns">
        <button className="rbtn green" onClick={start} disabled={active}>Старт</button>
        <button className="rbtn gray" onClick={() => setActive(false)} disabled={!active}>Пауза</button>
        <button className="rbtn red" onClick={() => { setActive(false); setTime(initial); setFinished(false); }}>Сброс</button>
      </div>
      <p className="muted">{finished ? '⏰ Время вышло — звуковой сигнал проигран' : 'При достижении 0 прозвучит сигнал 800 Гц'}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 29, "n": 2,
    "slug": "быстрые_кнопки_времени",
    "title": "React: быстрая установка времени",
    "desc": "Задание 2: кнопки 5, 10, 30 и 60 секунд мгновенно устанавливают время таймера.",
    "body": '<div id="root"></div>',
    "css": TIMER_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

function App() {
  const [time, setTime] = useState(10);
  const [initial, setInitial] = useState(10);
  const [active, setActive] = useState(false);

  useEffect(() => {
    if (!active) return;
    const id = setInterval(() => setTime(t => Math.max(0, t - 1)), 1000);
    return () => clearInterval(id);
  }, [active]);

  useEffect(() => {
    if (time === 0 && active) setActive(false);
  }, [time, active]);

  const setPreset = (seconds) => {
    setInitial(seconds);
    if (!active) setTime(seconds);
  };

  return (
    <div className="card timer">
      <h2>Таймер с пресетами</h2>
      <div className="time">{String(Math.floor(time / 60)).padStart(2, '0')}:{String(time % 60).padStart(2, '0')}</div>
      <div className="timer-row">
        {[5, 10, 30, 60].map(seconds => (
          <button key={seconds} className="rbtn gray" onClick={() => setPreset(seconds)}>{seconds}с</button>
        ))}
      </div>
      <div className="timer-btns">
        <button className="rbtn green" onClick={() => { if (time === 0) setTime(initial); setActive(true); }} disabled={active}>Старт</button>
        <button className="rbtn gray" onClick={() => setActive(false)} disabled={!active}>Пауза</button>
        <button className="rbtn red" onClick={() => { setActive(false); setTime(initial); }}>Сброс</button>
      </div>
      <p className="muted">Выбрано: {initial} сек · осталось: {time} сек</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 29, "n": 3,
    "slug": "минуты_и_секунды",
    "title": "React: установка минут и секунд",
    "desc": "Задание 3: два поля ввода — минуты (0–99) и секунды (0–59). Формат отображения MM:SS с валидацией.",
    "body": '<div id="root"></div>',
    "css": TIMER_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

function App() {
  const [minutes, setMinutes] = useState(0);
  const [seconds, setSeconds] = useState(10);
  const [time, setTime] = useState(10);
  const [active, setActive] = useState(false);

  useEffect(() => {
    const total = minutes * 60 + seconds;
    if (!active) setTime(total);
  }, [minutes, seconds]);

  useEffect(() => {
    if (!active) return;
    const id = setInterval(() => setTime(t => Math.max(0, t - 1)), 1000);
    return () => clearInterval(id);
  }, [active]);

  useEffect(() => {
    if (time === 0 && active) setActive(false);
  }, [time, active]);

  return (
    <div className="card timer">
      <h2>Таймер MM:SS</h2>
      <div className="time">{String(Math.floor(time / 60)).padStart(2, '0')}:{String(time % 60).padStart(2, '0')}</div>
      <div className="timer-row">
        <input
          type="number" min="0" max="99" value={minutes}
          onChange={(e) => setMinutes(Math.max(0, Math.min(99, parseInt(e.target.value) || 0)))}
          style={{ width: 70, textAlign: 'center' }}
        />
        <b>:</b>
        <input
          type="number" min="0" max="59" value={seconds}
          onChange={(e) => setSeconds(Math.max(0, Math.min(59, parseInt(e.target.value) || 0)))}
          style={{ width: 70, textAlign: 'center' }}
        />
      </div>
      <div className="timer-btns">
        <button className="rbtn green" onClick={() => setActive(true)} disabled={active || time === 0}>Старт</button>
        <button className="rbtn gray" onClick={() => setActive(false)} disabled={!active}>Пауза</button>
        <button className="rbtn red" onClick={() => { setActive(false); setTime(minutes * 60 + seconds); }}>Сброс</button>
      </div>
      <p className="muted">Минуты 0–99, секунды 0–59</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 29, "n": 4,
    "slug": "круговой_прогресс",
    "title": "React: круговой прогресс таймера",
    "desc": "Задание 4: SVG-индикатор с <code>strokeDashoffset</code>. Цвет меняется в зависимости от остатка времени.",
    "body": '<div id="root"></div>',
    "css": TIMER_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

function App() {
  const [initial, setInitial] = useState(30);
  const [time, setTime] = useState(30);
  const [active, setActive] = useState(false);

  useEffect(() => {
    if (!active) return;
    const id = setInterval(() => setTime(t => Math.max(0, t - 1)), 1000);
    return () => clearInterval(id);
  }, [active]);

  useEffect(() => {
    if (time === 0 && active) setActive(false);
  }, [time, active]);

  const progress = initial > 0 ? (time / initial) * 100 : 0;
  const radius = 90;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference * (1 - progress / 100);
  const color = time > initial * 0.5 ? '#4CAF50' : time > initial * 0.2 ? '#FF9800' : '#f44336';

  return (
    <div className="card timer">
      <h2>Круговой таймер</h2>
      <svg width="220" height="220">
        <circle cx="110" cy="110" r={radius} fill="none" stroke="#e0e0e0" strokeWidth="10" />
        <circle
          cx="110" cy="110" r={radius} fill="none" stroke={color} strokeWidth="10"
          strokeDasharray={circumference} strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset .5s ease, stroke .3s', transform: 'rotate(-90deg)', transformOrigin: '50% 50%' }}
        />
        <text x="110" y="118" textAnchor="middle" fontSize="34" fontWeight="700" fill="#1a73e8">
          {String(Math.floor(time / 60)).padStart(2, '0')}:{String(time % 60).padStart(2, '0')}
        </text>
      </svg>
      <div className="timer-row">
        <input
          type="number" min="5" max="300" value={initial}
          onChange={(e) => { const v = Math.max(5, Math.min(300, parseInt(e.target.value) || 5)); setInitial(v); if (!active) setTime(v); }}
          style={{ width: 90, textAlign: 'center' }}
        />
        <span>секунд</span>
      </div>
      <div className="timer-btns">
        <button className="rbtn green" onClick={() => { if (time === 0) setTime(initial); setActive(true); }} disabled={active}>Старт</button>
        <button className="rbtn gray" onClick={() => setActive(false)} disabled={!active}>Пауза</button>
        <button className="rbtn red" onClick={() => { setActive(false); setTime(initial); }}>Сброс</button>
      </div>
      <p className="muted">Прогресс: {Math.round(progress)}%</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 29, "n": 5,
    "slug": "несколько_таймеров",
    "title": "React: несколько таймеров",
    "desc": "Задание 5: кнопка «Добавить таймер» создаёт независимый таймер. Каждый работает со своим временем.",
    "body": '<div id="root"></div>',
    "css": TIMER_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

let nextId = 3;

function App() {
  const [timers, setTimers] = useState([
    { id: 1, time: 10, initial: 10, active: false },
    { id: 2, time: 20, initial: 20, active: false }
  ]);

  useEffect(() => {
    const id = setInterval(() => {
      setTimers(list => list.map(t => t.active && t.time > 0 ? { ...t, time: Math.max(0, t.time - 1), active: t.time - 1 > 0 } : t));
    }, 1000);
    return () => clearInterval(id);
  }, []);

  const update = (id, updates) => setTimers(list => list.map(t => t.id === id ? { ...t, ...updates } : t));

  const addTimer = () => setTimers(list => [...list, { id: nextId++, time: 10, initial: 10, active: false }]);

  return (
    <div className="card">
      <h2>Несколько таймеров</h2>
      <button className="rbtn green" onClick={addTimer}>+ Добавить таймер</button>
      {timers.map(t => (
        <div className="multi-timer" key={t.id}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 8 }}>
            <b>Таймер #{t.id}</b>
            <span style={{ fontSize: 26, fontWeight: 700, color: t.time === 0 ? '#f44336' : '#1a73e8' }}>
              {String(Math.floor(t.time / 60)).padStart(2, '0')}:{String(t.time % 60).padStart(2, '0')}
            </span>
          </div>
          <div className="timer-btns" style={{ justifyContent: 'flex-start' }}>
            <button className="rbtn" onClick={() => update(t.id, { active: !t.active })}>
              {t.active ? 'Пауза' : 'Старт'}
            </button>
            <button className="rbtn gray" onClick={() => update(t.id, { active: false, time: t.initial })}>Сброс</button>
            <button className="rbtn red" onClick={() => setTimers(list => list.filter(x => x.id !== t.id))}>Удалить</button>
          </div>
        </div>
      ))}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 29, "n": 6,
    "slug": "таймер_в_localstorage",
    "title": "React: сохранение таймера",
    "desc": "Задание 6: текущее время, исходное время и состояние сохраняются в <code>localStorage</code> и "
            "восстанавливаются после перезагрузки.",
    "body": '<div id="root"></div>',
    "css": TIMER_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;
const KEY = 'pr29_timerState';

function loadState() {
  try {
    const saved = localStorage.getItem(KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      return { time: parsed.time ?? 10, initial: parsed.initialTime ?? 10, active: false, finished: !!parsed.finished };
    }
  } catch (e) { /* ignore */ }
  return { time: 10, initial: 10, active: false, finished: false };
}

function App() {
  const [state, setState] = useState(loadState);

  useEffect(() => {
    localStorage.setItem(KEY, JSON.stringify({ time: state.time, initialTime: state.initial, finished: state.finished }));
  }, [state.time, state.initial, state.finished]);

  useEffect(() => {
    if (!state.active) return;
    const id = setInterval(() => {
      setState(s => {
        if (s.time <= 1) return { ...s, time: 0, active: false, finished: true };
        return { ...s, time: s.time - 1 };
      });
    }, 1000);
    return () => clearInterval(id);
  }, [state.active]);

  return (
    <div className="card timer">
      <h2>Таймер с сохранением</h2>
      <div className="time">{String(Math.floor(state.time / 60)).padStart(2, '0')}:{String(state.time % 60).padStart(2, '0')}</div>
      <div className="timer-btns">
        <button className="rbtn green" onClick={() => setState(s => ({ ...s, time: s.time === 0 ? s.initial : s.time, active: true, finished: false }))} disabled={state.active}>Старт</button>
        <button className="rbtn gray" onClick={() => setState(s => ({ ...s, active: false }))} disabled={!state.active}>Пауза</button>
        <button className="rbtn red" onClick={() => setState(s => ({ ...s, time: s.initial, active: false, finished: false }))}>Сброс</button>
      </div>
      <p className="muted">Состояние сохраняется при каждом изменении. Перезагрузите страницу — время восстановится.{state.finished ? ' Таймер завершён.' : ''}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 29, "n": 7,
    "slug": "интервальная_тренировка",
    "title": "React: интервальная тренировка",
    "desc": "Задание 7: чередование работы и отдыха (30 с / 10 с) по циклу. Текущий этап отображается "
            "подписью «Работа» / «Отдых» и меняет цвет.",
    "body": '<div id="root"></div>',
    "css": TIMER_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

function App() {
  const [workTime, setWorkTime] = useState(30);
  const [restTime, setRestTime] = useState(10);
  const [phase, setPhase] = useState('work');
  const [time, setTime] = useState(30);
  const [active, setActive] = useState(false);
  const [round, setRound] = useState(1);

  useEffect(() => {
    if (!active) return;
    const id = setInterval(() => {
      setTime(prev => {
        if (prev <= 1) {
          if (phase === 'work') { setPhase('rest'); return restTime; }
          setPhase('work');
          setRound(r => r + 1);
          return workTime;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [active, phase, workTime, restTime]);

  return (
    <div className="card timer">
      <h2>Интервальная тренировка</h2>
      <div className={`phase ${phase}`}>{phase === 'work' ? '🏋️ Работа' : '😌 Отдых'}</div>
      <div className="time">{String(Math.floor(time / 60)).padStart(2, '0')}:{String(time % 60).padStart(2, '0')}</div>
      <p className="muted">Круг: {round} · работа {workTime}с / отдых {restTime}с</p>
      <div className="timer-row">
        <label>Работа</label>
        <input type="number" min="5" max="300" value={workTime} onChange={(e) => setWorkTime(Math.max(5, Number(e.target.value) || 5))} style={{ width: 70 }} />
        <label>Отдых</label>
        <input type="number" min="5" max="300" value={restTime} onChange={(e) => setRestTime(Math.max(5, Number(e.target.value) || 5))} style={{ width: 70 }} />
      </div>
      <div className="timer-btns">
        <button className="rbtn green" onClick={() => setActive(!active)}>{active ? 'Пауза' : 'Старт'}</button>
        <button className="rbtn red" onClick={() => { setActive(false); setPhase('work'); setTime(workTime); setRound(1); }}>Сброс</button>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

# ============================== ПР30 ==============================
QUOTES_CSS = """
.quote{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px 18px;margin:10px 0;position:relative}
.quote-text{font-size:16px;line-height:1.6;font-style:italic}
.quote-author{margin-top:8px;color:#64748b;font-size:14px;text-align:right}
.quote-actions{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.suggest{position:absolute;background:#fff;border:1px solid #cbd5e1;border-radius:8px;box-shadow:0 8px 20px rgba(0,0,0,.12);z-index:5;max-height:220px;overflow:auto;min-width:240px}
.suggest div{padding:8px 12px;cursor:pointer;font-size:14px}
.suggest div:hover{background:#eef6ff}
.rel{position:relative}
.fade{animation:fadeIn .35s ease both}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
"""

TASKS.append({
    "pr": 30, "n": 1,
    "slug": "кнопка_поделиться",
    "title": "React: кнопка «Поделиться»",
    "desc": "Задание 1: цитату можно скопировать в буфер обмена через <code>navigator.clipboard.writeText()</code> "
            "(с запасным вариантом через textarea) и отправить через <code>navigator.share</code>.",
    "body": '<div id="root"></div>',
    "css": QUOTES_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const QUOTES = [
  { _id: 'q1', content: 'Мы то, что мы делаем постоянно. Совершенство — не действие, а привычка.', author: 'Аристотель' },
  { _id: 'q2', content: 'Единственный способ сделать великую работу — любить то, что делаешь.', author: 'Стив Джобс' },
  { _id: 'q3', content: 'Жизнь — это то, что происходит с тобой, пока ты строишь планы.', author: 'Джон Леннон' }
];

function App() {
  const [index, setIndex] = useState(0);
  const [message, setMessage] = useState('');
  const quote = QUOTES[index];

  const copyText = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (e) {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand('copy');
      document.body.removeChild(ta);
      return ok;
    }
  };

  const shareQuote = async () => {
    const text = `${quote.content} — ${quote.author}`;
    if (navigator.share) {
      try {
        await navigator.share({ title: 'Цитата дня', text });
        setMessage('Отправлено через системный Share API');
        return;
      } catch (e) { /* пользователь отменил */ }
    }
    const ok = await copyText(text);
    setMessage(ok ? '✅ Цитата скопирована в буфер обмена' : '❌ Не удалось скопировать');
  };

  return (
    <div className="card">
      <h2>Цитата дня</h2>
      <div className="quote fade" key={quote._id}>
        <div className="quote-text">«{quote.content}»</div>
        <div className="quote-author">— {quote.author}</div>
      </div>
      <div className="quote-actions">
        <button className="rbtn" onClick={shareQuote}>📋 Поделиться</button>
        <button className="rbtn gray" onClick={() => setIndex((index + 1) % QUOTES.length)}>Другая цитата</button>
      </div>
      <p className="muted" style={{ marginTop: 10 }}>{message}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 30, "n": 2,
    "slug": "выбор_количества_цитат",
    "title": "React: выбор количества цитат",
    "desc": "Задание 2: выпадающий список на 1/3/5/10 цитат; загружается указанное количество и выводится списком.",
    "body": '<div id="root"></div>',
    "css": QUOTES_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

const ALL = [
  ['Мы то, что мы делаем постоянно.', 'Аристотель'],
  ['Единственный способ сделать великую работу — любить то, что делаешь.', 'Стив Джобс'],
  ['Жизнь — это то, что происходит с тобой, пока ты строишь планы.', 'Джон Леннон'],
  ['Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.', 'Уинстон Черчилль'],
  ['Знание — сила.', 'Фрэнсис Бэкон'],
  ['Сложнее всего начать действовать, всё остальное зависит только от упорства.', 'Амелия Эрхарт'],
  ['Всё, что мы видим, — лишь точка зрения.', 'Анаис Нин'],
  ['Будь тем изменением, которое хочешь видеть в мире.', 'Махатма Ганди'],
  ['Воображение важнее знания.', 'Альберт Эйнштейн'],
  ['Счастье зависит от нас самих.', 'Аристотель']
];

const QUOTES = ALL.map(([content, author], i) => ({ _id: 'q' + i, content, author }));

function fetchQuotes(limit) {
  return new Promise(resolve => setTimeout(() => resolve(QUOTES.slice(0, limit)), 250));
}

function App() {
  const [count, setCount] = useState(1);
  const [quotes, setQuotes] = useState([]);
  const [loading, setLoading] = useState(false);

  const load = async (limit) => {
    setLoading(true);
    const results = await fetchQuotes(limit);
    setQuotes(results);
    setLoading(false);
  };

  useEffect(() => { load(count); }, []);

  return (
    <div className="card">
      <h2>Несколько цитат</h2>
      <div className="row">
        <select value={count} onChange={(e) => setCount(Number(e.target.value))}>
          {[1, 3, 5, 10].map(n => <option key={n} value={n}>{n} {n === 1 ? 'цитата' : 'цитат'}</option>)}
        </select>
        <button className="rbtn" onClick={() => load(count)} disabled={loading}>{loading ? 'Загрузка...' : 'Загрузить'}</button>
      </div>
      {quotes.map(q => (
        <div className="quote fade" key={q._id}>
          <div className="quote-text">«{q.content}»</div>
          <div className="quote-author">— {q.author}</div>
        </div>
      ))}
      <p className="muted">Загружено цитат: {quotes.length}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 30, "n": 3,
    "slug": "автодополнение_авторов",
    "title": "React: поиск по авторам",
    "desc": "Задание 3: при вводе текста показываются подходящие авторы; по клику загружается цитата автора.",
    "body": '<div id="root"></div>',
    "css": QUOTES_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const ALL = [
  { _id: '1', content: 'Мы то, что мы делаем постоянно.', author: 'Аристотель' },
  { _id: '2', content: 'Счастье зависит от нас самих.', author: 'Аристотель' },
  { _id: '3', content: 'Воображение важнее знания.', author: 'Альберт Эйнштейн' },
  { _id: '4', content: 'Успех — это способность идти от неудачи к неудаче.', author: 'Уинстон Черчилль' },
  { _id: '5', content: 'Знание — сила.', author: 'Фрэнсис Бэкон' },
  { _id: '6', content: 'Будь тем изменением, которое хочешь видеть в мире.', author: 'Махатма Ганди' }
];

const AUTHORS = [...new Set(ALL.map(q => q.author))];

function searchAuthors(query) {
  const lower = query.toLowerCase();
  return AUTHORS.filter(a => a.toLowerCase().includes(lower))
    .map(name => ({ name, quoteCount: ALL.filter(q => q.author === name).length }));
}

function App() {
  const [author, setAuthor] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [quote, setQuote] = useState(null);

  const onChange = (value) => {
    setAuthor(value);
    setSuggestions(value.trim().length >= 2 ? searchAuthors(value.trim()) : []);
  };

  const pick = (name) => {
    setAuthor(name);
    setSuggestions([]);
    setQuote(ALL.find(q => q.author === name));
  };

  return (
    <div className="card">
      <h2>Поиск по авторам</h2>
      <div className="rel">
        <input value={author} onChange={(e) => onChange(e.target.value)} placeholder="Начните вводить автора..." style={{ width: '100%' }} />
        {suggestions.length > 0 && (
          <div className="suggest">
            {suggestions.map(s => (
              <div key={s.name} onClick={() => pick(s.name)}>{s.name} ({s.quoteCount} цитат)</div>
            ))}
          </div>
        )}
      </div>
      {quote && (
        <div className="quote fade" style={{ marginTop: 14 }}>
          <div className="quote-text">«{quote.content}»</div>
          <div className="quote-author">— {quote.author}</div>
        </div>
      )}
      <p className="muted" style={{ marginTop: 10 }}>Минимум 2 символа для подсказок</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 30, "n": 4,
    "slug": "избранные_цитаты",
    "title": "React: избранные цитаты",
    "desc": "Задание 4: кнопка «⭐» добавляет цитату в избранное, список хранится в <code>localStorage</code>, "
            "повторное нажатие удаляет цитату.",
    "body": '<div id="root"></div>',
    "css": QUOTES_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

const QUOTES = [
  { _id: 'q1', content: 'Мы то, что мы делаем постоянно.', author: 'Аристотель' },
  { _id: 'q2', content: 'Единственный способ сделать великую работу — любить то, что делаешь.', author: 'Стив Джобс' },
  { _id: 'q3', content: 'Жизнь — это то, что происходит с тобой, пока ты строишь планы.', author: 'Джон Леннон' }
];

function App() {
  const [favorites, setFavorites] = useState(() => {
    try { return JSON.parse(localStorage.getItem('pr30_favorites') || '[]'); }
    catch (e) { return []; }
  });

  useEffect(() => {
    localStorage.setItem('pr30_favorites', JSON.stringify(favorites));
  }, [favorites]);

  const toggleFavorite = (quote) => {
    const isFavorite = favorites.some(f => f._id === quote._id);
    setFavorites(isFavorite ? favorites.filter(f => f._id !== quote._id) : [...favorites, quote]);
  };

  return (
    <div className="card">
      <h2>Цитаты и избранное</h2>
      {QUOTES.map(q => (
        <div className="quote" key={q._id}>
          <div className="quote-text">«{q.content}»</div>
          <div className="quote-author">— {q.author}</div>
          <div className="quote-actions">
            <button className="rbtn gray" onClick={() => toggleFavorite(q)}>
              {favorites.some(f => f._id === q._id) ? '⭐ В избранном' : '☆ В избранное'}
            </button>
          </div>
        </div>
      ))}
      <h3 style={{ marginTop: 16 }}>Избранное ({favorites.length})</h3>
      {favorites.length === 0 && <p className="muted">Пока пусто.</p>}
      {favorites.map(q => (
        <div className="item" key={q._id}>
          <span>«{q.content}» — {q.author}</span>
          <button className="icon-btn" onClick={() => toggleFavorite(q)}>×</button>
        </div>
      ))}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 30, "n": 5,
    "slug": "пагинация_цитат",
    "title": "React: пагинация цитат",
    "desc": "Задание 5: постраничная загрузка (по 3 цитаты) с кнопками «Назад» и «Вперёд» и счётчиком страниц.",
    "body": '<div id="root"></div>',
    "css": QUOTES_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

const ALL = Array.from({ length: 13 }, (_, i) => ({
  _id: 'q' + i,
  content: `Цитата №${i + 1}: небольшая мысль, которая иллюстрирует пагинацию.`,
  author: ['Аристотель', 'Стив Джобс', 'Джон Леннон', 'Альберт Эйнштейн'][i % 4]
}));
const LIMIT = 3;

function fetchPage(page) {
  const start = (page - 1) * LIMIT;
  return new Promise(resolve => setTimeout(() => resolve({
    results: ALL.slice(start, start + LIMIT),
    totalPages: Math.ceil(ALL.length / LIMIT)
  }), 200));
}

function App() {
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [quotes, setQuotes] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadPage = async (pageNum) => {
    setLoading(true);
    const data = await fetchPage(pageNum);
    setQuotes(data.results);
    setTotalPages(data.totalPages);
    setPage(pageNum);
    setLoading(false);
  };

  useEffect(() => { loadPage(1); }, []);

  return (
    <div className="card">
      <h2>Цитаты по страницам</h2>
      {loading && <p className="muted">Загрузка...</p>}
      {quotes.map(q => (
        <div className="quote fade" key={q._id}>
          <div className="quote-text">«{q.content}»</div>
          <div className="quote-author">— {q.author}</div>
        </div>
      ))}
      <div className="row" style={{ justifyContent: 'center' }}>
        <button className="rbtn gray" onClick={() => loadPage(page - 1)} disabled={page === 1 || loading}>← Назад</button>
        <span style={{ alignSelf: 'center' }}>Страница {page} из {totalPages}</span>
        <button className="rbtn" onClick={() => loadPage(page + 1)} disabled={page === totalPages || loading}>Вперёд →</button>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 30, "n": 6,
    "slug": "кэширование_запросов",
    "title": "React: кэширование запросов",
    "desc": "Задание 6: полученные цитаты кэшируются в объекте. Повторный запрос того же автора берёт данные "
            "из кэша — счётчик обращений к «API» не растёт.",
    "body": '<div id="root"></div>',
    "css": QUOTES_CSS,
    "react": True,
    "jsx": r"""
const { useState, useRef } = React;

const DB = {
  'Аристотель': { content: 'Мы то, что мы делаем постоянно.', author: 'Аристотель' },
  'Стив Джобс': { content: 'Единственный способ сделать великую работу — любить то, что делаешь.', author: 'Стив Джобс' },
  'Джон Леннон': { content: 'Жизнь — это то, что происходит с тобой, пока ты строишь планы.', author: 'Джон Леннон' }
};

let apiCalls = 0;

function apiFetch(author) {
  apiCalls++;
  return new Promise(resolve => setTimeout(() => resolve(DB[author]), 250));
}

function App() {
  const [quote, setQuote] = useState(null);
  const [log, setLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const cache = useRef({});

  const load = async (author) => {
    const key = author || 'random';
    if (cache.current[key]) {
      setQuote(cache.current[key]);
      setLog(l => [`${author}: взято из кэша`, ...l]);
      return;
    }
    setLoading(true);
    const data = await apiFetch(author);
    cache.current[key] = data;
    setQuote(data);
    setLoading(false);
    setLog(l => [`${author}: запрос к API (всего вызовов: ${apiCalls})`, ...l]);
  };

  return (
    <div className="card">
      <h2>Кэширование запросов</h2>
      <div className="row">
        {Object.keys(DB).map(a => (
          <button className="rbtn gray" key={a} onClick={() => load(a)}>{a}</button>
        ))}
      </div>
      {loading && <p className="muted">Загрузка...</p>}
      {quote && (
        <div className="quote fade" key={quote.content}>
          <div className="quote-text">«{quote.content}»</div>
          <div className="quote-author">— {quote.author}</div>
        </div>
      )}
      <div className="out" style={{ minHeight: 70 }}>{log.slice(0, 6).join('\n')}</div>
      <p className="muted">Нажмите одного и того же автора дважды — второй раз данные придут из кэша.</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 30, "n": 7,
    "slug": "цитата_дня_печатная_машинка",
    "title": "React: «Цитата дня» с печатной машинкой",
    "desc": "Задание 7: градиентный фон, смена темы оформления, анимированное появление и эффект печатной "
            "машинки при выводе цитаты.",
    "body": '<div id="root"></div>',
    "css": QUOTES_CSS + """
.scene{border-radius:16px;padding:26px;color:#fff;transition:background .6s;min-height:300px;display:flex;flex-direction:column;justify-content:center}
.scene p{font-size:22px;line-height:1.55;min-height:96px;font-family:Georgia,serif}
.scene .author{text-align:right;margin-top:12px;opacity:.85}
.scene .cursor{display:inline-block;width:2px;height:1em;background:currentColor;vertical-align:-2px;animation:blink 1s step-end infinite}
@keyframes blink{50%{opacity:0}}
""",
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

const QUOTES = [
  'Мы то, что мы делаем постоянно. Совершенство — не действие, а привычка.',
  'Единственный способ сделать великую работу — любить то, что делаешь.',
  'Жизнь — это то, что происходит с тобой, пока ты строишь планы.'
];

const THEMES = [
  { name: 'Закат', bg: 'linear-gradient(135deg,#ff7e5f,#feb47b)' },
  { name: 'Океан', bg: 'linear-gradient(135deg,#2193b0,#6dd5ed)' },
  { name: 'Ночь', bg: 'linear-gradient(135deg,#0f2027,#203a43,#2c5364)' }
];

function App() {
  const [index, setIndex] = useState(0);
  const [theme, setTheme] = useState(0);
  const [displayText, setDisplayText] = useState('');

  useEffect(() => {
    const text = QUOTES[index];
    let i = 0;
    setDisplayText('');
    const id = setInterval(() => {
      if (i < text.length) {
        setDisplayText(prev => prev + text[i]);
        i++;
      } else {
        clearInterval(id);
      }
    }, 30);
    return () => clearInterval(id);
  }, [index]);

  return (
    <div className="card">
      <div className="scene" style={{ background: THEMES[theme].bg }}>
        <p>
          «{displayText}<span className="cursor"></span>»
        </p>
        <div className="author">— Цитата дня</div>
      </div>
      <div className="row" style={{ marginTop: 12 }}>
        <button className="rbtn" onClick={() => setIndex((index + 1) % QUOTES.length)}>Следующая цитата</button>
        {THEMES.map((t, i) => (
          <button key={t.name} className="rbtn gray" onClick={() => setTheme(i)}>{t.name}</button>
        ))}
      </div>
      <p className="muted">Тема оформления: {THEMES[theme].name}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

# ============================== ПР31 ==============================
CALC_CSS = """
.calc{max-width:520px;margin:0 auto}
.calc-result{background:#0f172a;color:#4ade80;font-family:Consolas,monospace;font-size:26px;padding:16px;border-radius:10px;text-align:right;min-height:64px;margin:12px 0}
.calc-error{color:#fca5a5;font-size:14px;min-height:20px}
.keypad{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:10px}
.keypad button{padding:14px 0;border:1px solid #cbd5e1;border-radius:8px;background:#f8fafc;font-size:17px;cursor:pointer}
.keypad button:hover{background:#eef6ff}
.keypad button.op{background:#e0f2fe}
.keypad button.eq{background:#1a73e8;color:#fff;border-color:#1a73e8}
.mem-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
"""

TASKS.append({
    "pr": 31, "n": 1,
    "slug": "операция_остаток_от_деления",
    "title": "React: операция «%»",
    "desc": "Задание 1: в калькулятор добавлена операция «остаток от деления». Деление на ноль и остаток "
            "от нуля обрабатываются сообщением об ошибке.",
    "body": '<div id="root"></div>',
    "css": CALC_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function App() {
  const [a, setA] = useState('10');
  const [b, setB] = useState('3');
  const [op, setOp] = useState('+');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const calculate = (e) => {
    e.preventDefault();
    const x = Number(a);
    const y = Number(b);
    if (!Number.isFinite(x) || !Number.isFinite(y)) {
      setError('Введите числа');
      setResult(null);
      return;
    }
    let value;
    switch (op) {
      case '+': value = x + y; break;
      case '-': value = x - y; break;
      case '*': value = x * y; break;
      case '/':
        if (y === 0) { setError('На ноль делить нельзя!'); setResult(null); return; }
        value = x / y; break;
      case '%':
        if (y === 0) { setError('Остаток от деления на ноль невозможен!'); setResult(null); return; }
        value = x % y; break;
      default: value = 0;
    }
    setError('');
    setResult(value);
  };

  return (
    <div className="card calc">
      <h2>Калькулятор: %</h2>
      <form onSubmit={calculate}>
        <div className="row">
          <input type="number" value={a} onChange={(e) => setA(e.target.value)} style={{ width: 120 }} />
          <select value={op} onChange={(e) => setOp(e.target.value)}>
            <option value="+">+</option>
            <option value="-">−</option>
            <option value="*">×</option>
            <option value="/">÷</option>
            <option value="%">%</option>
          </select>
          <input type="number" value={b} onChange={(e) => setB(e.target.value)} style={{ width: 120 }} />
          <button className="rbtn" type="submit">=</button>
        </div>
      </form>
      <div className="calc-result">{result === null ? '—' : result}</div>
      <div className="calc-error">{error}</div>
      <p className="muted">Пример: 10 % 3 = 1</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 31, "n": 2,
    "slug": "операция_возведение_в_степень",
    "title": "React: операция «^»",
    "desc": "Задание 2: добавлена операция возведения в степень. Вычисляется через <code>Math.pow(a, b)</code>.",
    "body": '<div id="root"></div>',
    "css": CALC_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function App() {
  const [a, setA] = useState('2');
  const [b, setB] = useState('10');
  const [op, setOp] = useState('^');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const calculate = (e) => {
    e.preventDefault();
    const x = Number(a);
    const y = Number(b);
    if (!Number.isFinite(x) || !Number.isFinite(y)) { setError('Введите числа'); return; }
    if (op === '/' && y === 0) { setError('На ноль делить нельзя!'); return; }
    const value = op === '^' ? Math.pow(x, y)
      : op === '+' ? x + y
      : op === '-' ? x - y
      : op === '*' ? x * y
      : x / y;
    if (!Number.isFinite(value)) { setError('Результат слишком велик'); return; }
    setError('');
    setResult(value);
  };

  return (
    <div className="card calc">
      <h2>Калькулятор: ^</h2>
      <form onSubmit={calculate}>
        <div className="row">
          <input type="number" value={a} onChange={(e) => setA(e.target.value)} style={{ width: 110 }} />
          <select value={op} onChange={(e) => setOp(e.target.value)}>
            <option value="+">+</option>
            <option value="-">−</option>
            <option value="*">×</option>
            <option value="/">÷</option>
            <option value="^">^</option>
          </select>
          <input type="number" value={b} onChange={(e) => setB(e.target.value)} style={{ width: 110 }} />
          <button className="rbtn" type="submit">=</button>
        </div>
      </form>
      <div className="calc-result">{result === null ? '—' : result}</div>
      <div className="calc-error">{error}</div>
      <p className="muted">2 ^ 10 = {Math.pow(2, 10)}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 31, "n": 3,
    "slug": "клавиатурные_сокращения",
    "title": "React: клавиатурные сокращения",
    "desc": "Задание 3: Esc сбрасывает калькулятор, цифры и точка вводятся в активное поле, клавиши "
            "операций переключают операцию, Enter вычисляет.",
    "body": '<div id="root"></div>',
    "css": CALC_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;

function App() {
  const [a, setA] = useState('');
  const [b, setB] = useState('');
  const [op, setOp] = useState('+');
  const [active, setActive] = useState('a');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const resetCalculator = () => { setA(''); setB(''); setOp('+'); setResult(null); setError(''); setActive('a'); };

  const calculate = () => {
    const x = Number(a), y = Number(b);
    if (a === '' || b === '') { setError('Введите оба числа'); return; }
    if (op === '/' && y === 0) { setError('На ноль делить нельзя!'); return; }
    const value = op === '+' ? x + y : op === '-' ? x - y : op === '*' ? x * y : op === '^' ? Math.pow(x, y) : x / y;
    setError(''); setResult(value);
  };

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') { resetCalculator(); return; }
      if (e.key === 'Enter') { calculate(); return; }
      if (/^[0-9.]$/.test(e.key)) {
        if (active === 'a') setA(v => v + e.key); else setB(v => v + e.key);
        return;
      }
      if (['+', '-', '*', '/', '^'].includes(e.key)) setOp(e.key);
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [a, b, op, active]);

  return (
    <div className="card calc">
      <h2>Клавиатурный калькулятор</h2>
      <div className="row">
        <input value={a} onFocus={() => setActive('a')} onChange={(e) => setA(e.target.value)} placeholder="A" style={{ width: 110 }} />
        <select value={op} onChange={(e) => setOp(e.target.value)}>
          <option value="+">+</option><option value="-">−</option><option value="*">×</option>
          <option value="/">÷</option><option value="^">^</option>
        </select>
        <input value={b} onFocus={() => setActive('b')} onChange={(e) => setB(e.target.value)} placeholder="B" style={{ width: 110 }} />
        <button className="rbtn" onClick={calculate}>=</button>
      </div>
      <div className="calc-result">{result === null ? '—' : result}</div>
      <div className="calc-error">{error}</div>
      <p className="muted">Esc — сброс · Enter — вычисление · цифры и точка — ввод · + − * / ^ — операция. Активное поле: <b>{active === 'a' ? 'A' : 'B'}</b></p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 31, "n": 4,
    "slug": "цифровая_клавиатура",
    "title": "React: кнопки быстрого ввода",
    "desc": "Задание 4: цифровая клавиатура (0–9, точка, операции, «=»). Кнопки добавляют символы в активное "
            "поле, есть очистка текущего поля.",
    "body": '<div id="root"></div>',
    "css": CALC_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function App() {
  const [num1, setNum1] = useState('');
  const [num2, setNum2] = useState('');
  const [activeField, setActiveField] = useState('num1');
  const [op, setOp] = useState('+');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const appendNumber = (value) => {
    const setter = activeField === 'num1' ? setNum1 : setNum2;
    setter(prev => prev + value);
  };

  const clearField = () => {
    if (activeField === 'num1') setNum1(''); else setNum2('');
  };

  const chooseOp = (value) => {
    setOp(value);
    setActiveField('num2');
  };

  const compute = () => {
    const x = Number(num1), y = Number(num2);
    if (num1 === '' || num2 === '') { setError('Введите оба числа'); return; }
    if ((op === '/' || op === '%') && y === 0) { setError('На ноль делить нельзя!'); return; }
    const value = op === '+' ? x + y : op === '-' ? x - y : op === '*' ? x * y : op === '/' ? x / y : x % y;
    setError(''); setResult(value);
  };

  return (
    <div className="card calc">
      <h2>Клавиатура калькулятора</h2>
      <div className="row">
        <input value={num1} onFocus={() => setActiveField('num1')} onChange={(e) => setNum1(e.target.value)} placeholder="Число 1" style={{ width: 120, borderColor: activeField === 'num1' ? '#1a73e8' : undefined }} />
        <b>{op}</b>
        <input value={num2} onFocus={() => setActiveField('num2')} onChange={(e) => setNum2(e.target.value)} placeholder="Число 2" style={{ width: 120, borderColor: activeField === 'num2' ? '#1a73e8' : undefined }} />
        <button className="rbtn gray" onClick={clearField}>C</button>
      </div>
      <div className="calc-result">{result === null ? '—' : result}</div>
      <div className="calc-error">{error}</div>
      <div className="keypad">
        {['7','8','9','/','4','5','6','*','1','2','3','-','0','.','%','+'].map(btn => (
          btn === '/' || btn === '*' || btn === '-' || btn === '%' || btn === '+'
            ? <button key={btn} className="op" onClick={() => chooseOp(btn)}>{btn}</button>
            : <button key={btn} onClick={() => appendNumber(btn)}>{btn}</button>
        ))}
        <button className="eq" style={{ gridColumn: 'span 2' }} onClick={compute}>=</button>
        <button onClick={() => { setNum1(''); setNum2(''); setResult(null); setError(''); setActiveField('num1'); }} style={{ gridColumn: 'span 2' }}>Сброс</button>
      </div>
      <p className="muted">Активное поле: <b>{activeField === 'num1' ? 'Число 1' : 'Число 2'}</b></p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 31, "n": 5,
    "slug": "конвертация_систем_счисления",
    "title": "React: системы счисления",
    "desc": "Задание 5: переключение DEC / BIN / OCT / HEX. Число вводится в выбранной системе, результат "
            "показывается во всех четырёх.",
    "body": '<div id="root"></div>',
    "css": CALC_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const BASES = [
  { value: 2, label: 'BIN' },
  { value: 8, label: 'OCT' },
  { value: 10, label: 'DEC' },
  { value: 16, label: 'HEX' }
];

function App() {
  const [base, setBase] = useState(10);
  const [value, setValue] = useState('255');

  const parse = () => {
    const cleaned = value.trim().toUpperCase();
    if (!cleaned) return null;
    const allowed = base === 2 ? /^[01]+$/ : base === 8 ? /^[0-7]+$/ : base === 10 ? /^\d+$/ : /^[0-9A-F]+$/;
    if (!allowed.test(cleaned)) return NaN;
    return parseInt(cleaned, base);
  };

  const decimal = parse();
  const valid = decimal !== null && !Number.isNaN(decimal);

  return (
    <div className="card calc">
      <h2>Конвертер систем счисления</h2>
      <div className="row">
        <select value={base} onChange={(e) => setBase(Number(e.target.value))}>
          {BASES.map(b => <option key={b.value} value={b.value}>{b.label}</option>)}
        </select>
        <input value={value} onChange={(e) => setValue(e.target.value)} style={{ flex: 1, minWidth: 180, fontFamily: 'Consolas,monospace' }} />
      </div>
      <div className="calc-result" style={{ fontSize: 18 }}>
        {valid ? (
          <div style={{ textAlign: 'left', lineHeight: 1.8 }}>
            <div>DEC: {decimal}</div>
            <div>BIN: {decimal.toString(2)}</div>
            <div>OCT: {decimal.toString(8)}</div>
            <div>HEX: {decimal.toString(16).toUpperCase()}</div>
          </div>
        ) : '—'}
      </div>
      <div className="calc-error">{decimal !== null && Number.isNaN(decimal) ? 'Недопустимые символы для выбранной системы' : ''}</div>
      <p className="muted">parseInt(value, base).toString(base)</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 31, "n": 6,
    "slug": "память_калькулятора",
    "title": "React: память калькулятора",
    "desc": "Задание 6: кнопки M+, M−, MR, MC. Память хранит число и участвует в последующих вычислениях.",
    "body": '<div id="root"></div>',
    "css": CALC_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function App() {
  const [a, setA] = useState('10');
  const [b, setB] = useState('5');
  const [op, setOp] = useState('+');
  const [result, setResult] = useState(null);
  const [memory, setMemory] = useState(0);
  const [message, setMessage] = useState('');

  const compute = () => {
    const x = Number(a), y = Number(b);
    if (op === '/' && y === 0) { setMessage('На ноль делить нельзя!'); return; }
    const value = op === '+' ? x + y : op === '-' ? x - y : op === '*' ? x * y : x / y;
    setResult(value);
    setMessage('');
  };

  const memoryAdd = () => { if (result !== null) { setMemory(memory + result); setMessage(`M+ → ${memory + result}`); } };
  const memorySubtract = () => { if (result !== null) { setMemory(memory - result); setMessage(`M− → ${memory - result}`); } };
  const memoryRecall = () => { setA(String(memory)); setMessage(`MR → в поле A подставлено ${memory}`); };
  const memoryClear = () => { setMemory(0); setMessage('Память очищена'); };

  return (
    <div className="card calc">
      <h2>Калькулятор с памятью</h2>
      <div className="row">
        <input type="number" value={a} onChange={(e) => setA(e.target.value)} style={{ width: 110 }} />
        <select value={op} onChange={(e) => setOp(e.target.value)}>
          <option value="+">+</option><option value="-">−</option><option value="*">×</option><option value="/">÷</option>
        </select>
        <input type="number" value={b} onChange={(e) => setB(e.target.value)} style={{ width: 110 }} />
        <button className="rbtn" onClick={compute}>=</button>
      </div>
      <div className="calc-result">{result === null ? '—' : result}</div>
      <div className="mem-row">
        <button className="rbtn gray" onClick={memoryAdd}>M+</button>
        <button className="rbtn gray" onClick={memorySubtract}>M−</button>
        <button className="rbtn gray" onClick={memoryRecall}>MR</button>
        <button className="rbtn red" onClick={memoryClear}>MC</button>
        <span style={{ alignSelf: 'center' }}>Память: <b>{memory}</b></span>
      </div>
      <p className="muted">{message}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 31, "n": 7,
    "slug": "научный_калькулятор",
    "title": "React: научный калькулятор",
    "desc": "Задание 7: функции sin, cos, tan, log, ln, sqrt, факториал, константы π и e, скобки. "
            "Выражение проверяется и вычисляется через <code>Function</code>.",
    "body": '<div id="root"></div>',
    "css": CALC_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function factorial(n) {
  if (n < 0 || !Number.isInteger(n)) return NaN;
  return n <= 1 ? 1 : n * factorial(n - 1);
}

function evaluate(raw) {
  let expr = raw.replace(/\s+/g, '');
  if (!/^[0-9+\-*/().^!a-zπ]*$/i.test(expr)) throw new Error('Недопустимые символы');
  expr = expr
    .replace(/π/g, 'Math.PI')
    .replace(/(?<![a-z])e(?![a-z])/g, 'Math.E')
    .replace(/sqrt\(/g, 'Math.sqrt(')
    .replace(/sin\(/g, 'Math.sin(')
    .replace(/cos\(/g, 'Math.cos(')
    .replace(/tan\(/g, 'Math.tan(')
    .replace(/log\(/g, 'Math.log10(')
    .replace(/ln\(/g, 'Math.log(')
    .replace(/fact\(/g, 'FACT(')
    .replace(/(\d+(?:\.\d+)?)!/g, 'FACT($1)')
    .replace(/\^/g, '**');
  if (expr.includes('!')) throw new Error('Факториал поддерживается только для чисел: 5! или fact(5)');
  if (!/^[0-9+\-*/().,\sMathPIEsqrtincoglfFACT*]+$/.test(expr)) throw new Error('Недопустимое выражение');
  const result = Function('FACT', '"use strict"; return (' + expr + ')')(factorial);
  if (typeof result !== 'number' || !Number.isFinite(result)) throw new Error('Результат не является числом');
  return result;
}

function App() {
  const [expression, setExpression] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const calc = () => {
    try {
      const value = evaluate(expression);
      setResult(Number(value.toFixed(6)));
      setError('');
    } catch (e) {
      setResult(null);
      setError(e.message);
    }
  };

  const add = (text) => setExpression(prev => prev + text);

  return (
    <div className="card calc">
      <h2>Научный калькулятор</h2>
      <input
        value={expression}
        onChange={(e) => setExpression(e.target.value)}
        placeholder="Например: sin(π/2)+sqrt(16)"
        style={{ width: '100%', fontFamily: 'Consolas,monospace', fontSize: 16 }}
        onKeyDown={(e) => { if (e.key === 'Enter') calc(); }}
      />
      <div className="row">
        {['sin(', 'cos(', 'tan(', 'log(', 'ln(', 'sqrt(', 'π', 'e', '^', '(', ')'].map(fn => (
          <button key={fn} className="rbtn gray" onClick={() => add(fn)}>{fn.replace('(', '')}</button>
        ))}
        <button className="rbtn gray" onClick={() => add('fact(')}>n!</button>
      </div>
      <div className="row">
        <button className="rbtn green" onClick={calc}>=</button>
        <button className="rbtn red" onClick={() => { setExpression(''); setResult(null); setError(''); }}>C</button>
      </div>
      <div className="calc-result">{result === null ? '—' : result}</div>
      <div className="calc-error">{error}</div>
      <p className="muted">Степень записывается как ^ · факториал: fact(5)</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

# ============================== ПР32 ==============================
FILTER_CSS = """
.people{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.person{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:10px 14px;animation:fadeIn .3s ease both}
.person b{display:block}
.person span{font-size:13px;color:#64748b}
.letters{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0}
.letters button{width:30px;height:30px;border:1px solid #cbd5e1;border-radius:6px;background:#fff;cursor:pointer;font-size:13px}
.letters button.active{background:#1a73e8;color:#fff;border-color:#1a73e8}
@keyframes fadeIn{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:none}}
"""

NAMES = [
    'Анна Иванова', 'Борис Петров', 'Мария Федорова', 'Алексей Смирнов',
    'Екатерина Кузнецова', 'Владимир Попов', 'Ирина Соколова', 'Андрей Морозов',
    'Наталья Волкова', 'Максим Алексеев', 'Юлия Лебедева', 'Константин Козлов',
    'Ольга Новикова', 'Дмитрий Орлов', 'Светлана Зайцева', 'John Smith',
    'Emily Johnson', 'Michael Brown', '李 娜', 'Anna Müller'
]

TASKS.append({
    "pr": 32, "n": 1,
    "slug": "больше_элементов_в_списке",
    "title": "React: расширенный список имён",
    "desc": "Задание 1: в список добавлено более 10 новых имён и фамилий, включая имена на других языках.",
    "body": '<div id="root"></div>',
    "css": FILTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const NAMES = %s;

function App() {
  const [allItems] = useState(NAMES);
  const [query, setQuery] = useState('');

  const filtered = allItems.filter(name => name.toLowerCase().includes(query.toLowerCase()));

  return (
    <div className="card">
      <h2>Список имён ({allItems.length})</h2>
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Поиск..." style={{ width: '100%%', marginBottom: 12 }} />
      <div className="people">
        {filtered.map(name => <div className="person" key={name}><b>{name}</b><span>длина: {name.replace(/\\s/g, '').length}</span></div>)}
      </div>
      <p className="muted">Показано {filtered.length} из {allItems.length}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""" % (repr(NAMES).replace("'", '"'),),
})

TASKS.append({
    "pr": 32, "n": 2,
    "slug": "фильтр_по_длине_имени",
    "title": "React: фильтр по длине имени",
    "desc": "Задание 2: фильтр «Все / Короткие (≤5) / Длинные (&gt;5)». Длина считается без пробелов, "
            "включая фамилию.",
    "body": '<div id="root"></div>',
    "css": FILTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const NAMES = ["Анна Иванова", "Борис Петров", "Мария Федорова", "Алексей Смирнов", "Екатерина Кузнецова", "Владимир Попов", "Ирина Соколова", "Андрей Морозов", "Наталья Волкова", "Максим Алексеев", "Ли Я", "John Smith", "Anna Lee"];

function App() {
  const [allItems] = useState(NAMES);
  const [lengthFilter, setLengthFilter] = useState('all');

  let result = allItems;
  if (lengthFilter === 'short') result = result.filter(name => name.replace(/\s/g, '').length <= 5);
  else if (lengthFilter === 'long') result = result.filter(name => name.replace(/\s/g, '').length > 5);

  return (
    <div className="card">
      <h2>Фильтр по длине</h2>
      <select value={lengthFilter} onChange={(e) => setLengthFilter(e.target.value)}>
        <option value="all">Все</option>
        <option value="short">Короткие (≤5)</option>
        <option value="long">Длинные (&gt;5)</option>
      </select>
      <div className="people" style={{ marginTop: 12 }}>
        {result.map(name => (
          <div className="person" key={name}>
            <b>{name}</b>
            <span>длина без пробелов: {name.replace(/\s/g, '').length}</span>
          </div>
        ))}
      </div>
      <p className="muted">Найдено: {result.length}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 32, "n": 3,
    "slug": "поиск_по_первой_букве",
    "title": "React: поиск по первой букве",
    "desc": "Задание 3: алфавитный указатель А–Я. Клик по букве фильтрует имена, активная буква выделяется, "
            "повторный клик сбрасывает фильтр.",
    "body": '<div id="root"></div>',
    "css": FILTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const NAMES = ["Анна Иванова", "Алексей Смирнов", "Андрей Морозов", "Борис Петров", "Владимир Попов", "Екатерина Кузнецова", "Ирина Соколова", "Константин Козлов", "Мария Федорова", "Максим Алексеев", "Наталья Волкова", "Ольга Новикова", "Светлана Зайцева", "Юлия Лебедева"];

const LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'.split('');

function App() {
  const [allItems] = useState(NAMES);
  const [letter, setLetter] = useState('');

  const filtered = letter ? allItems.filter(name => name.startsWith(letter)) : allItems;

  return (
    <div className="card">
      <h2>Алфавитный указатель</h2>
      <div className="letters">
        {LETTERS.map(char => (
          <button key={char} className={letter === char ? 'active' : ''} onClick={() => setLetter(letter === char ? '' : char)}>
            {char}
          </button>
        ))}
      </div>
      {filtered.length === 0 && <p className="muted">Нет имён на букву «{letter}».</p>}
      <div className="people">
        {filtered.map(name => <div className="person" key={name}><b>{name}</b></div>)}
      </div>
      <p className="muted">Буква: {letter || 'все'} · найдено: {filtered.length}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 32, "n": 4,
    "slug": "расширенный_поиск_по_полям",
    "title": "React: поиск по нескольким полям",
    "desc": "Задание 4: массив объектов с полями имя, фамилия, возраст, город. Поиск по всем полям или "
            "по выбранному полю.",
    "body": '<div id="root"></div>',
    "css": FILTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const PEOPLE = [
  { firstName: 'Анна', lastName: 'Иванова', age: 25, city: 'Москва' },
  { firstName: 'Борис', lastName: 'Петров', age: 30, city: 'Санкт-Петербург' },
  { firstName: 'Мария', lastName: 'Федорова', age: 22, city: 'Москва' },
  { firstName: 'Алексей', lastName: 'Смирнов', age: 41, city: 'Новосибирск' },
  { firstName: 'Ирина', lastName: 'Соколова', age: 35, city: 'Казань' },
  { firstName: 'John', lastName: 'Smith', age: 28, city: 'London' }
];

const FIELDS = [
  { value: 'all', label: 'Все поля' },
  { value: 'firstName', label: 'Имя' },
  { value: 'lastName', label: 'Фамилия' },
  { value: 'age', label: 'Возраст' },
  { value: 'city', label: 'Город' }
];

function App() {
  const [allItems] = useState(PEOPLE);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchField, setSearchField] = useState('all');

  let result = allItems;
  if (searchTerm.trim()) {
    const term = searchTerm.trim().toLowerCase();
    result = allItems.filter(item => {
      if (searchField === 'all') {
        return Object.values(item).some(value => String(value).toLowerCase().includes(term));
      }
      return String(item[searchField]).toLowerCase().includes(term);
    });
  }

  return (
    <div className="card">
      <h2>Расширенный поиск</h2>
      <div className="row">
        <input value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} placeholder="Что ищем?" style={{ flex: 1, minWidth: 200 }} />
        <select value={searchField} onChange={(e) => setSearchField(e.target.value)}>
          {FIELDS.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
        </select>
      </div>
      <div className="people" style={{ marginTop: 12 }}>
        {result.map(p => (
          <div className="person" key={p.firstName + p.lastName}>
            <b>{p.firstName} {p.lastName}</b>
            <span>{p.age} лет · {p.city}</span>
          </div>
        ))}
      </div>
      <p className="muted">Найдено: {result.length} из {allItems.length}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 32, "n": 5,
    "slug": "множественный_выбор_фильтров",
    "title": "React: несколько фильтров одновременно",
    "desc": "Задание 5: чекбоксы фильтров (моложе 30, 30+, Москва, длинное имя). Все выбранные фильтры "
            "применяются одновременно, активные фильтры выводятся списком.",
    "body": '<div id="root"></div>',
    "css": FILTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const PEOPLE = [
  { name: 'Анна Иванова', age: 25, city: 'Москва' },
  { name: 'Борис Петров', age: 30, city: 'Санкт-Петербург' },
  { name: 'Мария Федорова', age: 22, city: 'Москва' },
  { name: 'Алексей Смирнов', age: 41, city: 'Новосибирск' },
  { name: 'Ирина Соколова', age: 35, city: 'Казань' },
  { name: 'John Smith', age: 28, city: 'Москва' }
];

const FILTERS = [
  { id: 'young', label: 'Моложе 30' },
  { id: 'adult', label: '30 и старше' },
  { id: 'moscow', label: 'Москва' },
  { id: 'long', label: 'Длинное имя (>10)' }
];

function App() {
  const [activeFilters, setActiveFilters] = useState([]);

  const toggleFilter = (id) => {
    setActiveFilters(prev => prev.includes(id) ? prev.filter(f => f !== id) : [...prev, id]);
  };

  let result = PEOPLE;
  if (activeFilters.includes('young')) result = result.filter(p => p.age < 30);
  if (activeFilters.includes('adult')) result = result.filter(p => p.age >= 30);
  if (activeFilters.includes('moscow')) result = result.filter(p => p.city === 'Москва');
  if (activeFilters.includes('long')) result = result.filter(p => p.name.replace(/\s/g, '').length > 10);

  return (
    <div className="card">
      <h2>Множественные фильтры</h2>
      <div className="row">
        {FILTERS.map(f => (
          <label key={f.id} className="pill" style={{ cursor: 'pointer' }}>
            <input type="checkbox" checked={activeFilters.includes(f.id)} onChange={() => toggleFilter(f.id)} />
            {f.label}
          </label>
        ))}
      </div>
      <p className="muted">Активные фильтры: {activeFilters.length ? activeFilters.join(', ') : 'нет'}</p>
      <div className="people">
        {result.map(p => (
          <div className="person" key={p.name}>
            <b>{p.name}</b><span>{p.age} лет · {p.city}</span>
          </div>
        ))}
      </div>
      <p className="muted">Найдено: {result.length} из {PEOPLE.length}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 32, "n": 6,
    "slug": "экспорт_результатов",
    "title": "React: экспорт результатов",
    "desc": "Задание 6: кнопка «Экспортировать» скачивает отфильтрованный список в CSV через "
            "<code>Blob</code> и <code>URL.createObjectURL</code>.",
    "body": '<div id="root"></div>',
    "css": FILTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const NAMES = ["Анна Иванова", "Борис Петров", "Мария Федорова", "Алексей Смирнов", "Екатерина Кузнецова", "Владимир Попов", "Ирина Соколова", "Андрей Морозов", "Наталья Волкова", "Максим Алексеев"];

function App() {
  const [allItems] = useState(NAMES);
  const [query, setQuery] = useState('');
  const [format, setFormat] = useState('csv');

  const filtered = allItems.filter(name => name.toLowerCase().includes(query.trim().toLowerCase()));

  const exportResults = () => {
    let content, type, ext;
    if (format === 'json') {
      content = JSON.stringify(filtered, null, 2);
      type = 'application/json';
      ext = 'json';
    } else {
      content = 'Имя\n' + filtered.map(n => '"' + n.replace(/"/g, '""') + '"').join('\n');
      type = 'text/csv;charset=utf-8';
      ext = 'csv';
    }
    const blob = new Blob(['\ufeff' + content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `filtered_results.${ext}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="card">
      <h2>Экспорт результатов</h2>
      <div className="row">
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Фильтр перед экспортом..." style={{ flex: 1, minWidth: 200 }} />
        <select value={format} onChange={(e) => setFormat(e.target.value)}>
          <option value="csv">CSV</option>
          <option value="json">JSON</option>
        </select>
        <button className="rbtn green" onClick={exportResults} disabled={filtered.length === 0}>
          📥 Экспортировать ({filtered.length})
        </button>
      </div>
      <div className="people" style={{ marginTop: 12 }}>
        {filtered.map(name => <div className="person" key={name}><b>{name}</b></div>)}
      </div>
      <p className="muted">Файл скачивается средствами браузера, сервер не нужен.</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 32, "n": 7,
    "slug": "анимация_фильтрации",
    "title": "React: анимация при фильтрации",
    "desc": "Задание 7: элементы списка плавно появляются при смене фильтра — CSS-анимация перезапускается "
            "за счёт смены <code>key</code> у контейнера и элементов.",
    "body": '<div id="root"></div>',
    "css": FILTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const NAMES = ["Анна Иванова", "Борис Петров", "Мария Федорова", "Алексей Смирнов", "Екатерина Кузнецова", "Владимир Попов", "Ирина Соколова", "Андрей Морозов", "Наталья Волкова", "Максим Алексеев", "Юлия Лебедева", "Константин Козлов"];

function App() {
  const [query, setQuery] = useState('');
  const [lengthFilter, setLengthFilter] = useState('all');

  let result = NAMES.filter(name => name.toLowerCase().includes(query.trim().toLowerCase()));
  if (lengthFilter === 'short') result = result.filter(n => n.replace(/\s/g, '').length <= 10);
  if (lengthFilter === 'long') result = result.filter(n => n.replace(/\s/g, '').length > 10);

  const animationKey = `${query}|${lengthFilter}`;

  return (
    <div className="card">
      <h2>Анимация фильтрации</h2>
      <div className="row">
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Поиск..." style={{ flex: 1, minWidth: 180 }} />
        <select value={lengthFilter} onChange={(e) => setLengthFilter(e.target.value)}>
          <option value="all">Все</option>
          <option value="short">Короткие (≤10)</option>
          <option value="long">Длинные (&gt;10)</option>
        </select>
      </div>
      <div className="people" style={{ marginTop: 12 }} key={animationKey}>
        {result.map(name => (
          <div className="person" key={animationKey + name}><b>{name}</b></div>
        ))}
      </div>
      <p className="muted">Элементы появляются заново при каждом изменении фильтра · найдено: {result.length}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})
