# -*- coding: utf-8 -*-
"""Задачи ПР22–ПР27."""

TASKS = []

BOOK_CSS = """
.book{background:#fff;border:1px solid #e2e8f0;border-left:4px solid #1a73e8;border-radius:10px;padding:12px 14px;margin:8px 0}
.book b{color:#0f172a}
.book .meta{font-size:13px;color:#64748b;margin-top:4px}
.stars{color:#f59e0b;letter-spacing:1px}
"""

# ============================== ПР22 ==============================
TASKS.append({
    "pr": 22, "n": 1,
    "slug": "метод_isold",
    "title": "Класс Book: метод isOld()",
    "desc": "Задание 1: в класс <code>Book</code> добавлен метод <code>isOld()</code>, который возвращает "
            "<code>true</code>, если книга старше 100 лет. Возраст считается через геттер <code>age</code> "
            "от текущего года.",
    "body": """
<div class="card">
  <h2>Библиотека</h2>
  <div id="books"></div>
  <div class="out" id="out"></div>
</div>""",
    "css": BOOK_CSS,
    "script": r"""
class Book {
  constructor(title, author, year, genre, rating) {
    this.title = title;
    this.author = author;
    this.year = year;
    this.genre = genre;
    this.rating = rating;
  }

  get age() {
    return new Date().getFullYear() - this.year;
  }

  isOld() {
    return this.age > 100;
  }

  getInfo() {
    return `${this.title} — ${this.author} (${this.year})`;
  }
}

const books = [
  new Book('Война и мир', 'Л. Н. Толстой', 1869, 'роман', 4.9),
  new Book('Преступление и наказание', 'Ф. М. Достоевский', 1866, 'роман', 4.8),
  new Book('Мастер и Маргарита', 'М. А. Булгаков', 1967, 'роман', 4.9),
  new Book('Пикник на обочине', 'А. и Б. Стругацкие', 1972, 'фантастика', 4.7),
  new Book('Дюна', 'Ф. Герберт', 1965, 'фантастика', 4.6)
];

$('books').innerHTML = books.map(b => `
  <div class="book">
    <b>${esc(b.title)}</b>
    <div class="meta">${esc(b.author)} · ${b.year} · возраст: ${b.age} лет</div>
    <div class="meta">isOld(): <b class="${b.isOld() ? 'err' : 'ok'}">${b.isOld()}</b></div>
  </div>`).join('');

out(`Всего книг: <span class="hl">${books.length}</span>
Старше 100 лет: <span class="ok">${books.filter(b => b.isOld()).length}</span>
<br>console.log(book.isOld()) → ${books.map(b => b.isOld()).join(', ')}`);
""",
})

TASKS.append({
    "pr": 22, "n": 2,
    "slug": "getbooksbyyearrange",
    "title": "Диапазон лет издания",
    "desc": "Задание 2: метод <code>getBooksByYearRange(fromYear, toYear)</code> возвращает массив книг, "
            "изданных в указанном диапазоне лет включительно.",
    "body": """
<div class="card">
  <h2>Фильтр по годам</h2>
  <div class="row">
    <label>с</label><input id="from" type="number" value="1900" style="width:100px">
    <label>по</label><input id="to" type="number" value="2000" style="width:100px">
    <button class="btn" onclick="applyRange()">Показать</button>
    <button class="btn gray" onclick="resetRange()">Все книги</button>
  </div>
  <div id="result"></div>
  <div class="out" id="out"></div>
</div>""",
    "css": BOOK_CSS,
    "script": r"""
class Book {
  constructor(title, author, year) { this.title = title; this.author = author; this.year = year; }
  getInfo() { return `${this.title} — ${this.author} (${this.year})`; }
}

class LibraryManager {
  constructor(books = []) { this.books = books; }
  getBooksByYearRange(fromYear, toYear) {
    return this.books.filter(book => book.year >= fromYear && book.year <= toYear);
  }
  getAllBooks() { return this.books; }
}

const library = new LibraryManager([
  new Book('Война и мир', 'Л. Н. Толстой', 1869),
  new Book('Мастер и Маргарита', 'М. А. Булгаков', 1967),
  new Book('Пикник на обочине', 'А. и Б. Стругацкие', 1972),
  new Book('Гарри Поттер и философский камень', 'Дж. Роулинг', 1997),
  new Book('Тень ветра', 'К. Р. Сафон', 2001),
  new Book('Сто лет одиночества', 'Г. Г. Маркес', 1967)
]);

function render(list) {
  $('result').innerHTML = list.length
    ? list.map(b => `<div class="book"><b>${esc(b.title)}</b><div class="meta">${esc(b.author)} · ${b.year}</div></div>`).join('')
    : '<p class="muted">Книг в этом диапазоне нет.</p>';
}

function applyRange() {
  const from = Number($('from').value);
  const to = Number($('to').value);
  const list = library.getBooksByYearRange(from, to);
  render(list);
  out(`getBooksByYearRange(${from}, ${to}) → найдено <span class="hl">${list.length}</span> книг`);
}

function resetRange() {
  render(library.getAllBooks());
  out(`getAllBooks() → <span class="hl">${library.getAllBooks().length}</span> книг`);
}

resetRange();
""",
})

TASKS.append({
    "pr": 22, "n": 3,
    "slug": "средний_рейтинг",
    "title": "Средний рейтинг книг",
    "desc": "Задание 3: метод <code>getAverageRating()</code> считает средний рейтинг через <code>reduce</code>. "
            "Если книг нет — возвращает 0. Результат округляется до двух знаков.",
    "body": """
<div class="card">
  <h2>Книги и рейтинги</h2>
  <div id="books"></div>
  <div class="row">
    <button class="btn" onclick="showAverage()">getAverageRating()</button>
    <button class="btn red" onclick="clearBooks()">Очистить библиотеку</button>
    <button class="btn green" onclick="restoreBooks()">Вернуть книги</button>
  </div>
  <div class="out" id="out"></div>
</div>""",
    "css": BOOK_CSS,
    "script": r"""
class Book {
  constructor(title, rating) { this.title = title; this.rating = rating; }
}

class LibraryManager {
  constructor(books = []) { this.books = books; }
  getAverageRating() {
    if (this.books.length === 0) return 0;
    const sum = this.books.reduce((acc, book) => acc + book.rating, 0);
    return Number((sum / this.books.length).toFixed(2));
  }
}

const initial = [
  new Book('Война и мир', 4.9),
  new Book('Мастер и Маргарита', 4.8),
  new Book('Дюна', 4.6),
  new Book('Пикник на обочине', 4.7)
];

let library = new LibraryManager([...initial]);

function render() {
  $('books').innerHTML = library.books.length
    ? library.books.map(b => `<div class="book"><b>${esc(b.title)}</b><div class="meta">рейтинг: ${b.rating}</div></div>`).join('')
    : '<p class="muted">Библиотека пуста.</p>';
}

function showAverage() {
  const avg = library.getAverageRating();
  out(`getAverageRating() → <span class="hl">${avg}</span>${library.books.length === 0 ? ' <span class="muted">(книг нет — возвращаем 0)</span>' : ''}`);
}

function clearBooks() { library.books = []; render(); out('Библиотека очищена — средний рейтинг теперь 0'); }
function restoreBooks() { library.books = [...initial]; render(); showAverage(); }

render();
showAverage();
""",
})

TASKS.append({
    "pr": 22, "n": 4,
    "slug": "пять_книг_сортировка_по_году",
    "title": "Пять книг разных жанров",
    "desc": "Задание 4: созданы 5 книг разных жанров с рейтингами. Список выводится отсортированным "
            "по году выпуска — от новых к старым.",
    "body": """
<div class="card">
  <h2>Книги, отсортированные по году (новые → старые)</h2>
  <div id="books"></div>
  <div class="out" id="out"></div>
</div>""",
    "css": BOOK_CSS,
    "script": r"""
class Book {
  constructor(title, author, year, genre, rating) {
    this.title = title; this.author = author; this.year = year;
    this.genre = genre; this.rating = rating;
  }
}

const library = [
  new Book('Война и мир', 'Л. Н. Толстой', 1869, 'роман', 4.9),
  new Book('Дюна', 'Ф. Герберт', 1965, 'фантастика', 4.6),
  new Book('Мастер и Маргарита', 'М. А. Булгаков', 1967, 'роман', 4.8),
  new Book('Гарри Поттер', 'Дж. Роулинг', 1997, 'фэнтези', 4.7),
  new Book('Тень ветра', 'К. Р. Сафон', 2001, 'детектив', 4.5)
];

const sortedBooks = [...library].sort((a, b) => b.year - a.year);

$('books').innerHTML = sortedBooks.map((b, i) => `
  <div class="book">
    <b>${i + 1}. ${esc(b.title)}</b>
    <div class="meta">${esc(b.author)} · ${b.year} · ${esc(b.genre)} · <span class="stars">★</span> ${b.rating}</div>
  </div>`).join('');

out(sortedBooks.map(b => `${b.year}: ${b.title}`).join('\n'));
""",
})

# ============================== ПР23 ==============================
TASKS.append({
    "pr": 23, "n": 1,
    "slug": "educationalbook",
    "title": "Класс EducationalBook",
    "desc": "Задание 1: класс <code>EducationalBook extends Book</code> с полями <code>subject</code> и "
            "<code>level</code>. Метод <code>getInfo()</code> переопределён и дополняет информацию родителя.",
    "body": """
<div class="card">
  <h2>Обычные книги и учебники</h2>
  <div class="row">
    <select id="level">
      <option value="beginner">beginner</option>
      <option value="intermediate">intermediate</option>
      <option value="advanced">advanced</option>
    </select>
    <input id="subject" value="JavaScript" placeholder="Предмет" style="min-width:160px">
    <button class="btn green" onclick="addTextbook()">Создать учебник</button>
  </div>
  <div id="books"></div>
  <div class="out" id="out"></div>
</div>""",
    "css": BOOK_CSS,
    "script": r"""
class Book {
  constructor(title, author, year) { this.title = title; this.author = author; this.year = year; }
  getInfo() { return `${this.title} — ${this.author} (${this.year})`; }
}

class EducationalBook extends Book {
  constructor(title, author, year, subject, level = 'beginner') {
    super(title, author, year);
    this.subject = subject;
    this.level = level;
  }
  getInfo() {
    const baseInfo = super.getInfo();
    const levelMap = { beginner: 'Начальный', intermediate: 'Средний', advanced: 'Продвинутый' };
    return `${baseInfo} (Учебник по ${this.subject}, ${levelMap[this.level] || this.level})`;
  }
}

const books = [
  new Book('Война и мир', 'Л. Н. Толстой', 1869),
  new EducationalBook('JavaScript для профессионалов', 'Д. Флэнаган', 2020, 'JavaScript', 'advanced')
];

function render() {
  $('books').innerHTML = books.map(b => `
    <div class="book">
      <b>${esc(b.title)}</b>
      <div class="meta">${esc(b.getInfo())}</div>
      <div class="meta">instanceof EducationalBook: <b class="${b instanceof EducationalBook ? 'ok' : 'muted'}">${b instanceof EducationalBook}</b></div>
    </div>`).join('');
}

function addTextbook() {
  const subject = $('subject').value.trim() || 'JavaScript';
  const level = $('level').value;
  books.push(new EducationalBook('Учебник по ' + subject, 'Автор', new Date().getFullYear(), subject, level));
  render();
  out(`<span class="ok">Создан EducationalBook</span>
${esc(books[books.length - 1].getInfo())}`);
}

render();
""",
})

TASKS.append({
    "pr": 23, "n": 2,
    "slug": "audiobook_skipto",
    "title": "AudioBook.skipTo(time)",
    "desc": "Задание 2: метод <code>skipTo(time)</code> устанавливает текущее время аудиокниги, "
            "ограничивая его диапазоном 0…duration.",
    "body": """
<div class="card">
  <h2>Плеер аудиокниги</h2>
  <div class="row">
    <input id="time" type="number" value="30" min="0" style="width:100px">
    <button class="btn" onclick="doSkip()">skipTo(time)</button>
    <button class="btn gray" onclick="skipTo(-10)">skipTo(-10)</button>
    <button class="btn gray" onclick="skipTo(999)">skipTo(999)</button>
  </div>
  <div class="out" id="out"></div>
</div>""",
    "script": r"""
class AudioBook {
  constructor(title, duration, currentTime = 0) {
    this.title = title;
    this.duration = duration;
    this.currentTime = currentTime;
  }

  skipTo(time) {
    if (time < 0) time = 0;
    if (time > this.duration) time = this.duration;
    this.currentTime = time;
    console.log(`⏩ Переход к ${time} минуте`);
    render(`⏩ Переход к ${time} минуте`);
    return time;
  }
}

const audiobook = new AudioBook('Дюна (аудиокнига)', 720, 0);

function render(extra = '') {
  const p = Math.round(audiobook.currentTime / audiobook.duration * 100);
  out(`${esc(audiobook.title)}
Текущее время: <span class="hl">${audiobook.currentTime}</span> / ${audiobook.duration} мин
Прогресс: [${'█'.repeat(Math.round(p / 5))}${'░'.repeat(20 - Math.round(p / 5))}] ${p}%
${extra}`);
}

function doSkip() {
  audiobook.skipTo(Number($('time').value) || 0);
  render();
}

render();
""",
})

TASKS.append({
    "pr": 23, "n": 3,
    "slug": "collection_getbytype",
    "title": "Класс Collection",
    "desc": "Задание 3: коллекция книг с методами <code>addBook()</code>, <code>getAllBooks()</code> и "
            "<code>getByType()</code>. Тип определяется через <code>instanceof</code>.",
    "body": """
<div class="card">
  <h2>Коллекция</h2>
  <div class="row">
    <button class="btn" onclick="add('book')">+ Обычная книга</button>
    <button class="btn green" onclick="add('ebook')">+ Электронная</button>
    <button class="btn orange" onclick="add('audiobook')">+ Аудиокнига</button>
  </div>
  <div class="row">
    <button class="btn gray" onclick="show('all')">getAllBooks()</button>
    <button class="btn gray" onclick="show('book')">getByType('book')</button>
    <button class="btn gray" onclick="show('ebook')">getByType('ebook')</button>
    <button class="btn gray" onclick="show('audiobook')">getByType('audiobook')</button>
  </div>
  <div id="list"></div>
  <div class="out" id="out"></div>
</div>""",
    "css": BOOK_CSS,
    "script": r"""
class Book {
  constructor(title) { this.title = title; this.type = 'book'; }
  getInfo() { return `${this.title} (печатная книга)`; }
}
class EBook extends Book {
  constructor(title, fileSize) { super(title); this.type = 'ebook'; this.fileSize = fileSize; }
  getInfo() { return `${this.title} (электронная, ${this.fileSize} МБ)`; }
}
class AudioBook extends Book {
  constructor(title, duration) { super(title); this.type = 'audiobook'; this.duration = duration; }
  getInfo() { return `${this.title} (аудиокнига, ${this.duration} мин)`; }
}

class Collection {
  constructor() { this.books = []; }
  addBook(book) { this.books.push(book); return this; }
  getAllBooks() { return this.books; }
  getByType(type) {
    if (type === 'ebook') return this.books.filter(b => b instanceof EBook);
    if (type === 'audiobook') return this.books.filter(b => b instanceof AudioBook);
    if (type === 'book') return this.books.filter(b => !(b instanceof EBook) && !(b instanceof AudioBook));
    return this.books;
  }
}

const collection = new Collection();
let counter = 0;

function add(type) {
  counter++;
  if (type === 'ebook') collection.addBook(new EBook('Электронная книга ' + counter, 2 + counter));
  else if (type === 'audiobook') collection.addBook(new AudioBook('Аудиокнига ' + counter, 120 + counter * 10));
  else collection.addBook(new Book('Печатная книга ' + counter));
  show('all');
}

function show(type) {
  const list = type === 'all' ? collection.getAllBooks() : collection.getByType(type);
  $('list').innerHTML = list.length
    ? list.map(b => `<div class="book"><b>${esc(b.getInfo())}</b><div class="meta">type: ${b.type}</div></div>`).join('')
    : '<p class="muted">В этой категории пусто.</p>';
  out(`getByType('${type}') → <span class="hl">${list.length}</span> книг(и)`);
}

add('book');
add('ebook');
add('audiobook');
""",
})

# ============================== ПР24 ==============================
BOOK_RENDER_CSS = BOOK_CSS + """
.toolbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:10px}
.modal{position:fixed;inset:0;background:rgba(15,23,42,.55);display:none;align-items:center;justify-content:center;padding:20px;z-index:10}
.modal.open{display:flex}
.modal-box{background:#fff;border-radius:12px;padding:20px;max-width:420px;width:100%}
.modal-box h3{margin-bottom:10px}
.modal-box input{width:100%}
"""

TASKS.append({
    "pr": 24, "n": 1,
    "slug": "редактирование_книги",
    "title": "Редактирование книги",
    "desc": "Задание 1: в карточке книги есть кнопка «✏️ Редактировать», которая открывает модальное окно "
            "с полями названия и автора. После сохранения интерфейс перерисовывается.",
    "body": """
<div class="card">
  <div class="toolbar"><b>Книги</b><span class="muted">нажмите «Редактировать» в карточке</span></div>
  <div id="books"></div>
  <div class="out" id="out"></div>
</div>
<div class="modal" id="modal">
  <div class="modal-box">
    <h3>Редактирование книги</h3>
    <label>Название</label><input id="edit-title">
    <label>Автор</label><input id="edit-author">
    <div class="row" style="margin-top:14px">
      <button class="btn green" onclick="saveEdit()">Сохранить</button>
      <button class="btn gray" onclick="closeModal()">Отмена</button>
    </div>
  </div>
</div>""",
    "css": BOOK_RENDER_CSS,
    "script": r"""
class Book {
  constructor(id, title, author, year, rating) {
    this.id = id; this.title = title; this.author = author; this.year = year; this.rating = rating;
  }
}

const books = [
  new Book(1, 'Война и мир', 'Л. Н. Толстой', 1869, 4.9),
  new Book(2, 'Мастер и Маргарита', 'М. А. Булгаков', 1967, 4.8),
  new Book(3, 'Дюна', 'Ф. Герберт', 1965, 4.6)
];

let editingId = null;

function render() {
  $('books').innerHTML = books.map(b => `
    <div class="book">
      <b>${esc(b.title)}</b>
      <div class="meta">${esc(b.author)} · ${b.year} · ★ ${b.rating}</div>
      <button class="btn" style="margin-top:8px" onclick="openModal(${b.id})">✏️ Редактировать</button>
    </div>`).join('');
}

function openModal(id) {
  editingId = id;
  const b = books.find(x => x.id === id);
  $('edit-title').value = b.title;
  $('edit-author').value = b.author;
  $('modal').classList.add('open');
}

function closeModal() {
  $('modal').classList.remove('open');
  editingId = null;
}

function saveEdit() {
  const b = books.find(x => x.id === editingId);
  if (!b) return;
  const title = $('edit-title').value.trim();
  const author = $('edit-author').value.trim();
  if (!title) { out('<span class="err">Название не может быть пустым</span>'); return; }
  b.title = title;
  b.author = author;
  render();
  closeModal();
  out(`<span class="ok">Книга обновлена:</span> ${esc(title)} — ${esc(author)}`);
}

render();
""",
})

TASKS.append({
    "pr": 24, "n": 2,
    "slug": "поиск_книг",
    "title": "Поиск книг по названию и автору",
    "desc": "Задание 2: поле поиска над списком фильтрует книги в реальном времени по названию или автору "
            "(событие <code>input</code> + <code>filter()</code>).",
    "body": """
<div class="card">
  <div class="toolbar">
    <input id="search" placeholder="Поиск по названию или автору..." style="flex:1;min-width:240px" oninput="render()">
  </div>
  <div id="books"></div>
  <div class="out" id="out"></div>
</div>""",
    "css": BOOK_RENDER_CSS,
    "script": r"""
const books = [
  { title: 'Война и мир', author: 'Л. Н. Толстой', year: 1869, rating: 4.9 },
  { title: 'Анна Каренина', author: 'Л. Н. Толстой', year: 1877, rating: 4.8 },
  { title: 'Мастер и Маргарита', author: 'М. А. Булгаков', year: 1967, rating: 4.9 },
  { title: 'Собачье сердце', author: 'М. А. Булгаков', year: 1925, rating: 4.7 },
  { title: 'Дюна', author: 'Ф. Герберт', year: 1965, rating: 4.6 }
];

function render() {
  const query = $('search').value.trim().toLowerCase();
  const filtered = query
    ? books.filter(b => b.title.toLowerCase().includes(query) || b.author.toLowerCase().includes(query))
    : books;

  $('books').innerHTML = filtered.length
    ? filtered.map(b => `<div class="book"><b>${esc(b.title)}</b><div class="meta">${esc(b.author)} · ${b.year} · ★ ${b.rating}</div></div>`).join('')
    : '<p class="muted">Ничего не найдено.</p>';

  out(`Запрос: «${esc(query)}» → найдено <span class="hl">${filtered.length}</span> из ${books.length}`);
}

render();
""",
})

TASKS.append({
    "pr": 24, "n": 3,
    "slug": "сортировка_книг",
    "title": "Сортировка книг",
    "desc": "Задание 3: выпадающий список сортировки — по году (по возрастанию/убыванию), по названию (А-Я) "
            "и по рейтингу. Массив сортируется перед рендерингом.",
    "body": """
<div class="card">
  <div class="toolbar">
    <label>Сортировка:</label>
    <select id="sort" onchange="render()">
      <option value="year-desc">Год: новые сначала</option>
      <option value="year-asc">Год: старые сначала</option>
      <option value="title">Название (А-Я)</option>
      <option value="rating">Рейтинг (высокий → низкий)</option>
    </select>
  </div>
  <div id="books"></div>
  <div class="out" id="out"></div>
</div>""",
    "css": BOOK_RENDER_CSS,
    "script": r"""
const books = [
  { title: 'Война и мир', author: 'Л. Н. Толстой', year: 1869, rating: 4.9 },
  { title: 'Анна Каренина', author: 'Л. Н. Толстой', year: 1877, rating: 4.8 },
  { title: 'Мастер и Маргарита', author: 'М. А. Булгаков', year: 1967, rating: 4.9 },
  { title: 'Дюна', author: 'Ф. Герберт', year: 1965, rating: 4.6 },
  { title: 'Гарри Поттер', author: 'Дж. Роулинг', year: 1997, rating: 4.7 }
];

const comparators = {
  'year-desc': (a, b) => b.year - a.year,
  'year-asc': (a, b) => a.year - b.year,
  'title': (a, b) => a.title.localeCompare(b.title, 'ru'),
  'rating': (a, b) => b.rating - a.rating
};

function render() {
  const mode = $('sort').value;
  const sorted = [...books].sort(comparators[mode]);
  $('books').innerHTML = sorted.map(b => `
    <div class="book"><b>${esc(b.title)}</b>
    <div class="meta">${esc(b.author)} · ${b.year} · ★ ${b.rating}</div></div>`).join('');
  out(`sort('${mode}') → ${sorted.map(b => b.year).join(', ')}`);
}

render();
""",
})

# ============================== ПР25 ==============================
STORAGE_CSS = BOOK_CSS + """
.saved{font-size:13px;color:#16a34a;background:#dcfce7;border:1px solid #86efac;border-radius:8px;padding:6px 12px;display:inline-block}
.status-line{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:10px}
"""

TASKS.append({
    "pr": 25, "n": 1,
    "slug": "индикатор_сохранения",
    "title": "Индикатор последнего сохранения",
    "desc": "Задание 1: после каждого сохранения в <code>localStorage</code> обновляется индикатор "
            "«Сохранено в XX:XX:XX».",
    "body": """
<div class="card">
  <div class="status-line">
    <b>Моя библиотека</b>
    <span class="saved" id="saved">ещё не сохранено</span>
  </div>
  <div class="row">
    <input id="title" placeholder="Название книги" style="min-width:220px">
    <input id="author" placeholder="Автор" style="min-width:180px">
    <button class="btn green" onclick="addBook()">Добавить и сохранить</button>
    <button class="btn red" onclick="resetAll()">Сбросить</button>
  </div>
  <div id="books"></div>
  <div class="out" id="out"></div>
</div>""",
    "css": STORAGE_CSS,
    "script": r"""
const KEY = 'pr25_books';

class LibraryManager {
  constructor() {
    this.books = this.loadFromStorage();
    this.lastSaved = null;
  }

  loadFromStorage() {
    try { return JSON.parse(localStorage.getItem(KEY) || '[]'); }
    catch (e) { return []; }
  }

  addBook(title, author) {
    this.books.push({ title, author, date: new Date().toISOString() });
    this.saveToStorage();
  }

  saveToStorage() {
    localStorage.setItem(KEY, JSON.stringify(this.books));
    this.lastSaved = new Date();
    this.updateSaveIndicator();
  }

  updateSaveIndicator() {
    const el = $('saved');
    if (!this.lastSaved) { el.textContent = 'ещё не сохранено'; return; }
    el.textContent = 'Сохранено в ' + this.lastSaved.toLocaleTimeString('ru-RU');
  }
}

const library = new LibraryManager();

function render() {
  $('books').innerHTML = library.books.length
    ? library.books.map(b => `<div class="book"><b>${esc(b.title)}</b><div class="meta">${esc(b.author)}</div></div>`).join('')
    : '<p class="muted">Книг пока нет.</p>';
}

function addBook() {
  const title = $('title').value.trim();
  const author = $('author').value.trim() || 'Неизвестный автор';
  if (!title) { out('<span class="err">Введите название</span>'); return; }
  library.addBook(title, author);
  $('title').value = '';
  $('author').value = '';
  render();
  out(`<span class="ok">Книга добавлена и сохранена</span>`);
}

function resetAll() {
  localStorage.removeItem(KEY);
  library.books = [];
  library.lastSaved = null;
  library.updateSaveIndicator();
  render();
  out('Хранилище очищено');
}

render();
library.updateSaveIndicator();
""",
})

TASKS.append({
    "pr": 25, "n": 2,
    "slug": "undo_последнего_действия",
    "title": "Отмена последнего действия (Undo)",
    "desc": "Задание 2: история состояний массива книг. Кнопка «Отменить» откатывает на одно действие назад.",
    "body": """
<div class="card">
  <div class="status-line">
    <b>Книги</b>
    <span class="saved" id="saved">история: 1 состояние</span>
  </div>
  <div class="row">
    <input id="title" placeholder="Название новой книги" style="flex:1;min-width:220px">
    <button class="btn green" onclick="addBook()">Добавить</button>
    <button class="btn orange" onclick="undo()">↩ Отменить</button>
    <button class="btn red" onclick="resetAll()">Сброс</button>
  </div>
  <div id="books"></div>
  <div class="out" id="out"></div>
</div>""",
    "css": STORAGE_CSS,
    "script": r"""
const KEY = 'pr25_books_undo';

class LibraryManager {
  constructor() {
    this.books = [];
    this.history = [];
    this.historyIndex = -1;
    this.loadFromStorage();
    if (this.history.length === 0) this.saveToStorage();
  }

  loadFromStorage() {
    try {
      const data = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (data && Array.isArray(data.books)) {
        this.books = data.books;
        this.history = data.history || [data.books];
        this.historyIndex = typeof data.historyIndex === 'number' ? data.historyIndex : this.history.length - 1;
      }
    } catch (e) { /* ignore */ }
  }

  saveToStorage() {
    localStorage.setItem(KEY, JSON.stringify({
      books: this.books,
      history: this.history,
      historyIndex: this.historyIndex
    }));
  }

  snapshot() {
    const copy = JSON.parse(JSON.stringify(this.books));
    this.history = this.history.slice(0, this.historyIndex + 1);
    this.history.push(copy);
    this.historyIndex = this.history.length - 1;
    this.saveToStorage();
  }

  addBook(title) {
    this.books.push({ title });
    this.snapshot();
  }

  removeBook(index) {
    this.books.splice(index, 1);
    this.snapshot();
  }

  undo() {
    if (this.historyIndex > 0) {
      this.historyIndex--;
      this.books = JSON.parse(JSON.stringify(this.history[this.historyIndex]));
      this.saveToStorage();
      return true;
    }
    return false;
  }

  reset() {
    this.books = [];
    this.history = [];
    this.historyIndex = -1;
    this.snapshot();
  }
}

const library = new LibraryManager();

function render() {
  $('books').innerHTML = library.books.length
    ? library.books.map((b, i) => `<div class="item"><span>${esc(b.title)}</span><button class="btn red" onclick="removeBook(${i})">×</button></div>`).join('')
    : '<p class="muted">Книг нет.</p>';
  $('saved').textContent = `история: ${library.history.length} состояний, текущее #${library.historyIndex + 1}`;
}

function addBook() {
  const title = $('title').value.trim();
  if (!title) { out('<span class="err">Введите название</span>'); return; }
  library.addBook(title);
  $('title').value = '';
  render();
  out(`<span class="ok">Добавлено:</span> ${esc(title)}`);
}

function removeBook(index) {
  library.removeBook(index);
  render();
  out('<span class="ok">Удалено, можно отменить</span>');
}

function undo() {
  const ok = library.undo();
  render();
  out(ok ? '<span class="ok">Последнее действие отменено</span>' : '<span class="err">Отменять больше нечего</span>');
}

function resetAll() {
  library.reset();
  render();
  out('Библиотека сброшена');
}

render();
""",
})

TASKS.append({
    "pr": 25, "n": 3,
    "slug": "синхронизация_вкладок",
    "title": "Синхронизация между вкладками",
    "desc": "Задание 3: событие <code>storage</code> — при изменении данных в одной вкладке вторая вкладка "
            "перезагружает данные. Откройте страницу во втором окне и добавьте книгу.",
    "body": """
<div class="card">
  <div class="status-line">
    <b>Синхронизация localStorage</b>
    <span class="saved" id="saved">вкладка активна</span>
  </div>
  <div class="row">
    <input id="title" placeholder="Название книги" style="flex:1;min-width:220px">
    <button class="btn green" onclick="addBook()">Добавить</button>
    <button class="btn" onclick="openSecondTab()">Открыть вторую вкладку</button>
    <button class="btn red" onclick="resetAll()">Сброс</button>
  </div>
  <div id="books"></div>
  <div class="out" id="out">Измените данные в другой вкладке — эта обновится автоматически.</div>
</div>""",
    "css": STORAGE_CSS,
    "script": r"""
const KEY = 'pr25_sync_books';

function load() {
  try { return JSON.parse(localStorage.getItem(KEY) || '[]'); }
  catch (e) { return []; }
}

function save(books) {
  localStorage.setItem(KEY, JSON.stringify(books));
}

function render(books = load()) {
  $('books').innerHTML = books.length
    ? books.map(b => `<div class="book"><b>${esc(b.title)}</b><div class="meta">${b.date ? new Date(b.date).toLocaleTimeString('ru-RU') : ''}</div></div>`).join('')
    : '<p class="muted">Книг нет.</p>';
}

function addBook() {
  const title = $('title').value.trim();
  if (!title) { out('<span class="err">Введите название</span>'); return; }
  const books = load();
  books.push({ title, date: new Date().toISOString() });
  save(books);
  $('title').value = '';
  render(books);
  out(`<span class="ok">Добавлено:</span> ${esc(title)} <span class="muted">(вкладка 1)</span>`);
}

function resetAll() {
  localStorage.removeItem(KEY);
  render([]);
  out('Данные очищены');
}

function openSecondTab() {
  window.open(location.href, '_blank');
  out('Открыта вторая вкладка. Добавляйте книги в любой из них.');
}

window.addEventListener('storage', (e) => {
  if (e.key === KEY) {
    render(load());
    $('saved').textContent = 'обновлено из другой вкладки';
    out(`<span class="ok">🔄 Данные синхронизированы с другой вкладки</span>
Новых записей: ${load().length}`);
  }
});

render();
""",
})

TASKS.append({
    "pr": 25, "n": 4,
    "slug": "избранные_книги",
    "title": "Избранные книги",
    "desc": "Задание 4: свойство <code>isFavorite</code>, переключатель «⭐» и отдельный фильтр «Избранное». "
            "Состояние сохраняется в <code>localStorage</code>.",
    "body": """
<div class="card">
  <div class="row">
    <button class="pill active" id="f-all" onclick="setFilter('all')">Все книги</button>
    <button class="pill" id="f-fav" onclick="setFilter('fav')">⭐ Избранное</button>
  </div>
  <div id="books"></div>
  <div class="out" id="out"></div>
</div>""",
    "css": STORAGE_CSS,
    "script": r"""
const KEY = 'pr25_favorites';
let filter = 'all';

const DEFAULT_BOOKS = [
  { title: 'Война и мир', author: 'Л. Н. Толстой', isFavorite: false },
  { title: 'Мастер и Маргарита', author: 'М. А. Булгаков', isFavorite: true },
  { title: 'Дюна', author: 'Ф. Герберт', isFavorite: false },
  { title: 'Пикник на обочине', author: 'А. и Б. Стругацкие', isFavorite: true }
];

function load() {
  try { return JSON.parse(localStorage.getItem(KEY) || 'null') || JSON.parse(JSON.stringify(DEFAULT_BOOKS)); }
  catch (e) { return JSON.parse(JSON.stringify(DEFAULT_BOOKS)); }
}

let books = load();

function save() { localStorage.setItem(KEY, JSON.stringify(books)); }

function render() {
  const list = filter === 'fav' ? books.filter(b => b.isFavorite) : books;
  $('books').innerHTML = list.length
    ? list.map((b) => `<div class="book">
        <b>${esc(b.title)}</b> <button class="btn" style="padding:4px 10px" onclick="toggleFavorite(${books.indexOf(b)})">${b.isFavorite ? '⭐' : '☆'}</button>
        <div class="meta">${esc(b.author)}</div>
      </div>`).join('')
    : '<p class="muted">В избранном пока пусто.</p>';
  out(`Фильтр: <span class="hl">${filter === 'fav' ? 'Избранное' : 'Все книги'}</span> · показано ${list.length} из ${books.length}`);
}

function toggleFavorite(index) {
  const b = books[index];
  if (!b) return;
  b.isFavorite = !b.isFavorite;
  save();
  render();
}

function setFilter(value) {
  filter = value;
  $('f-all').classList.toggle('active', value === 'all');
  $('f-fav').classList.toggle('active', value === 'fav');
  render();
}

render();
""",
})

# ============================== ПР26 ==============================
COUNTER_CSS = """
.counter-box{text-align:center;padding:10px}
.counter-value{font-size:56px;font-weight:700;color:#1a73e8;line-height:1.1;margin:10px 0}
.btn-row{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin:10px 0}
.rbtn{padding:10px 18px;border:none;border-radius:8px;background:#1a73e8;color:#fff;font-size:14px;cursor:pointer}
.rbtn:hover{background:#0b5bc0}
.rbtn.gray{background:#64748b}.rbtn.green{background:#28a745}.rbtn.red{background:#dc3545}
.rbtn:disabled{opacity:.45;cursor:not-allowed}
.hist{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;margin-top:12px}
.hist span{background:#eef2ff;border:1px solid #c7d2fe;border-radius:6px;padding:4px 10px;font-size:13px}
.progress{height:18px;background:#e2e8f0;border-radius:999px;overflow:hidden;margin-top:16px}
.progress > div{height:100%;transition:width .3s,background .3s}
"""

TASKS.append({
    "pr": 26, "n": 1,
    "slug": "кнопка_удвоения",
    "title": "React: кнопка ×2",
    "desc": "Задание 1: к счётчику добавлена кнопка «×2», которая умножает текущее значение на 2 "
            "через <code>setCount(count * 2)</code>.",
    "body": '<div id="root"></div>',
    "css": COUNTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="card counter-box">
      <h2>Счётчик кликов</h2>
      <div className="counter-value">{count}</div>
      <div className="btn-row">
        <button className="rbtn green" onClick={() => setCount(count + 1)}>+1</button>
        <button className="rbtn red" onClick={() => setCount(count - 1)}>−1</button>
        <button className="rbtn" onClick={() => setCount(count * 2)}>×2</button>
        <button className="rbtn gray" onClick={() => setCount(0)}>Сброс</button>
      </div>
      <p className="muted">Кнопка ×2 добавлена в задании 1</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 26, "n": 2,
    "slug": "ввод_произвольного_числа",
    "title": "React: установка произвольного числа",
    "desc": "Задание 2: поле <code>input type=number</code> устанавливает значение счётчика через "
            "<code>setCount(Number(e.target.value))</code>.",
    "body": '<div id="root"></div>',
    "css": COUNTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function App() {
  const [count, setCount] = useState(0);
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInputValue(value);
    setCount(Number(value) || 0);
  };

  return (
    <div className="card counter-box">
      <h2>Счётчик с полем ввода</h2>
      <div className="counter-value">{count}</div>
      <div className="btn-row">
        <button className="rbtn green" onClick={() => setCount(count + 1)}>+1</button>
        <button className="rbtn red" onClick={() => setCount(count - 1)}>−1</button>
      </div>
      <input
        type="number"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Введите число"
        style={{ padding: 10, fontSize: 18, width: 200, border: '2px solid #ddd', borderRadius: 6, textAlign: 'center' }}
      />
      <p className="muted">Значение счётчика = значение поля</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 26, "n": 3,
    "slug": "история_изменений",
    "title": "React: история изменений",
    "desc": "Задание 3: каждое изменение счётчика добавляется в массив истории и отображается под счётчиком.",
    "body": '<div id="root"></div>',
    "css": COUNTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function App() {
  const [count, setCount] = useState(0);
  const [history, setHistory] = useState([0]);

  const updateCount = (newCount) => {
    setCount(newCount);
    setHistory([...history, newCount]);
  };

  return (
    <div className="card counter-box">
      <h2>Счётчик с историей</h2>
      <div className="counter-value">{count}</div>
      <div className="btn-row">
        <button className="rbtn green" onClick={() => updateCount(count + 1)}>+1</button>
        <button className="rbtn red" onClick={() => updateCount(count - 1)}>−1</button>
        <button className="rbtn" onClick={() => updateCount(count * 2)}>×2</button>
        <button className="rbtn gray" onClick={() => { setCount(0); setHistory([0]); }}>Сброс</button>
      </div>
      <h3 style={{ marginTop: 18, fontSize: 16 }}>История изменений:</h3>
      <div className="hist">
        {history.map((value, index) => <span key={index}>{value}</span>)}
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 26, "n": 4,
    "slug": "настройка_шага",
    "title": "React: счётчик с шагом",
    "desc": "Задание 4: настраиваемый шаг (по умолчанию 1). Кнопки «+» и «−» меняют счётчик на величину шага, "
            "шаг можно увеличивать и уменьшать, но не ниже 1.",
    "body": '<div id="root"></div>',
    "css": COUNTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function App() {
  const [count, setCount] = useState(0);
  const [step, setStep] = useState(1);

  return (
    <div className="card counter-box">
      <h2>Счётчик с настраиваемым шагом</h2>
      <div className="counter-value">{count}</div>
      <div className="btn-row">
        <button className="rbtn green" onClick={() => setCount(count + step)}>+{step}</button>
        <button className="rbtn red" onClick={() => setCount(count - step)}>−{step}</button>
        <button className="rbtn gray" onClick={() => setCount(0)}>Сброс</button>
      </div>
      <div className="btn-row">
        <button className="rbtn gray" onClick={() => setStep(Math.max(1, step - 1))}>Шаг −1</button>
        <span style={{ alignSelf: 'center' }}>Текущий шаг: <b>{step}</b></span>
        <button className="rbtn gray" onClick={() => setStep(step + 1)}>Шаг +1</button>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 26, "n": 5,
    "slug": "прогресс_бар",
    "title": "React: визуализация счётчика",
    "desc": "Задание 5: прогресс-бар от 0 до 20. При достижении максимума кнопка «+» блокируется, "
            "цвет полосы меняется после 15.",
    "body": '<div id="root"></div>',
    "css": COUNTER_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function App() {
  const [count, setCount] = useState(0);
  const maxCount = 20;
  const progress = Math.min((count / maxCount) * 100, 100);

  return (
    <div className="card counter-box">
      <h2>Счётчик с прогресс-баром</h2>
      <div className="counter-value">{count} <span style={{ fontSize: 20, color: '#94a3b8' }}>/ {maxCount}</span></div>
      <div className="btn-row">
        <button className="rbtn green" disabled={count >= maxCount} onClick={() => setCount(count + 1)}>+1</button>
        <button className="rbtn red" disabled={count <= 0} onClick={() => setCount(count - 1)}>−1</button>
        <button className="rbtn gray" onClick={() => setCount(0)}>Сброс</button>
      </div>
      <div className="progress">
        <div style={{
          width: `${progress}%`,
          backgroundColor: count > 15 ? '#f44336' : '#4CAF50'
        }} />
      </div>
      <p className="muted">{count >= maxCount ? 'Достигнут максимум — кнопка «+» заблокирована' : `Осталось до максимума: ${maxCount - count}`}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

# ============================== ПР27 ==============================
SHOP_CSS = """
.shop{max-width:640px;margin:0 auto}
.shop-form{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.shop-form input{flex:1;min-width:180px}
.shop-item{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:8px 12px;margin:6px 0}
.shop-item .name{flex:1}
.shop-item .done{text-decoration:line-through;color:#94a3b8}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin:10px 0}
.stats .stat{flex:1}
.cat-title{margin:14px 0 4px;font-weight:600;color:#334155;border-bottom:1px solid #e2e8f0;padding-bottom:3px}
.icon-btn{background:#f1f5f9;border:1px solid #cbd5e1;border-radius:6px;padding:4px 9px;cursor:pointer;font-size:13px}
"""

TASKS.append({
    "pr": 27, "n": 1,
    "slug": "добавление_по_enter",
    "title": "React: добавление товара по Enter",
    "desc": "Задание 1: добавление работает через <code>&lt;form onSubmit&gt;</code> — Enter в поле ввода "
            "отправляет форму, а <code>e.preventDefault()</code> не даёт странице перезагрузиться.",
    "body": '<div id="root"></div>',
    "css": SHOP_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

function App() {
  const [items, setItems] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const name = inputValue.trim();
    if (!name) return;
    setItems([...items, { id: Date.now(), name, purchased: false }]);
    setInputValue('');
  };

  return (
    <div className="card shop">
      <h2>Список покупок</h2>
      <form className="shop-form" onSubmit={handleSubmit}>
        <input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Товар и Enter..."
        />
        <button className="rbtn green" type="submit">Добавить</button>
      </form>
      {items.length === 0 && <p className="muted">Список пуст. Введите товар и нажмите Enter.</p>}
      {items.map(item => (
        <div className="shop-item" key={item.id}>
          <span className="name">{item.name}</span>
          <button className="icon-btn" onClick={() => setItems(items.filter(i => i.id !== item.id))}>×</button>
        </div>
      ))}
      <p className="muted">Всего: {items.length}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 27, "n": 2,
    "slug": "отметка_купленного",
    "title": "React: отметка «куплено»",
    "desc": "Задание 2: у каждого товара есть кнопка «✓». При нажатии товар зачёркивается, но остаётся в списке. "
            "Структура элемента: <code>{ id, name, purchased }</code>.",
    "body": '<div id="root"></div>',
    "css": SHOP_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const initial = [
  { id: 1, name: 'Молоко', purchased: false },
  { id: 2, name: 'Хлеб', purchased: true },
  { id: 3, name: 'Яблоки', purchased: false }
];

function App() {
  const [items, setItems] = useState(initial);
  const [inputValue, setInputValue] = useState('');

  const addItem = (e) => {
    e.preventDefault();
    const name = inputValue.trim();
    if (!name) return;
    setItems([...items, { id: Date.now(), name, purchased: false }]);
    setInputValue('');
  };

  const togglePurchased = (id) => {
    setItems(items.map(item => item.id === id ? { ...item, purchased: !item.purchased } : item));
  };

  return (
    <div className="card shop">
      <h2>Список покупок</h2>
      <form className="shop-form" onSubmit={addItem}>
        <input value={inputValue} onChange={(e) => setInputValue(e.target.value)} placeholder="Новый товар..." />
        <button className="rbtn" type="submit">Добавить</button>
      </form>
      {items.map(item => (
        <div className="shop-item" key={item.id}>
          <button className="icon-btn" onClick={() => togglePurchased(item.id)}>{item.purchased ? '✓' : '○'}</button>
          <span className={item.purchased ? 'name done' : 'name'}>{item.name}</span>
          <button className="icon-btn" onClick={() => setItems(items.filter(i => i.id !== item.id))}>×</button>
        </div>
      ))}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 27, "n": 3,
    "slug": "счетчик_товаров_по_группам",
    "title": "React: счётчики «Всего / Куплено / Осталось»",
    "desc": "Задание 3: под списком выводятся три счётчика, рассчитанные через <code>filter</code>.",
    "body": '<div id="root"></div>',
    "css": SHOP_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const initial = [
  { id: 1, name: 'Молоко', purchased: false },
  { id: 2, name: 'Хлеб', purchased: true },
  { id: 3, name: 'Яблоки', purchased: false },
  { id: 4, name: 'Сыр', purchased: true }
];

function App() {
  const [items, setItems] = useState(initial);
  const [inputValue, setInputValue] = useState('');

  const total = items.length;
  const purchased = items.filter(item => item.purchased).length;
  const remaining = total - purchased;

  const addItem = (e) => {
    e.preventDefault();
    const name = inputValue.trim();
    if (!name) return;
    setItems([...items, { id: Date.now(), name, purchased: false }]);
    setInputValue('');
  };

  return (
    <div className="card shop">
      <h2>Список покупок</h2>
      <form className="shop-form" onSubmit={addItem}>
        <input value={inputValue} onChange={(e) => setInputValue(e.target.value)} placeholder="Новый товар..." />
        <button className="rbtn" type="submit">Добавить</button>
      </form>
      <div className="stats">
        <div className="stat"><b>{total}</b><span>Всего</span></div>
        <div className="stat"><b style={{ color: '#16a34a' }}>{purchased}</b><span>Куплено</span></div>
        <div className="stat"><b style={{ color: '#f59e0b' }}>{remaining}</b><span>Осталось</span></div>
      </div>
      {items.map(item => (
        <div className="shop-item" key={item.id}>
          <button className="icon-btn" onClick={() => setItems(items.map(i => i.id === item.id ? { ...i, purchased: !i.purchased } : i))}>
            {item.purchased ? '✓' : '○'}
          </button>
          <span className={item.purchased ? 'name done' : 'name'}>{item.name}</span>
          <button className="icon-btn" onClick={() => setItems(items.filter(i => i.id !== item.id))}>×</button>
        </div>
      ))}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 27, "n": 4,
    "slug": "поиск_товаров",
    "title": "React: поиск по товарам",
    "desc": "Задание 4: поле поиска фильтрует список при вводе текста (без учёта регистра).",
    "body": '<div id="root"></div>',
    "css": SHOP_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const initial = [
  { id: 1, name: 'Молоко', purchased: false },
  { id: 2, name: 'Хлеб', purchased: true },
  { id: 3, name: 'Яблоки', purchased: false },
  { id: 4, name: 'Молоко сгущённое', purchased: false },
  { id: 5, name: 'Сыр', purchased: true }
];

function App() {
  const [items, setItems] = useState(initial);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredItems = items.filter(item =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="card shop">
      <h2>Список покупок</h2>
      <input
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Поиск..."
        style={{ width: '100%', marginBottom: 12 }}
      />
      {filteredItems.length === 0 && <p className="muted">Ничего не найдено.</p>}
      {filteredItems.map(item => (
        <div className="shop-item" key={item.id}>
          <span className={item.purchased ? 'name done' : 'name'}>{item.name}</span>
          <button className="icon-btn" onClick={() => setItems(items.filter(i => i.id !== item.id))}>×</button>
        </div>
      ))}
      <p className="muted">Показано {filteredItems.length} из {items.length}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 27, "n": 5,
    "slug": "редактирование_товара",
    "title": "React: редактирование товара",
    "desc": "Задание 5: кнопка «✎» переводит товар в режим редактирования, есть «Сохранить» и «Отмена». "
            "Редактируемый элемент отслеживается через <code>editingId</code>.",
    "body": '<div id="root"></div>',
    "css": SHOP_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const initial = [
  { id: 1, name: 'Молоко', purchased: false },
  { id: 2, name: 'Хлеб', purchased: true },
  { id: 3, name: 'Яблоки', purchased: false }
];

function App() {
  const [items, setItems] = useState(initial);
  const [editingId, setEditingId] = useState(null);
  const [editValue, setEditValue] = useState('');

  const startEdit = (id, name) => {
    setEditingId(id);
    setEditValue(name);
  };

  const saveEdit = (id) => {
    if (!editValue.trim()) return;
    setItems(items.map(item => item.id === id ? { ...item, name: editValue.trim() } : item));
    setEditingId(null);
  };

  return (
    <div className="card shop">
      <h2>Список покупок</h2>
      {items.map(item => (
        <div className="shop-item" key={item.id}>
          {editingId === item.id ? (
            <>
              <input value={editValue} onChange={(e) => setEditValue(e.target.value)} style={{ flex: 1 }} />
              <button className="icon-btn" onClick={() => saveEdit(item.id)}>Сохранить</button>
              <button className="icon-btn" onClick={() => setEditingId(null)}>Отмена</button>
            </>
          ) : (
            <>
              <span className={item.purchased ? 'name done' : 'name'}>{item.name}</span>
              <button className="icon-btn" onClick={() => startEdit(item.id, item.name)}>✎</button>
              <button className="icon-btn" onClick={() => setItems(items.filter(i => i.id !== item.id))}>×</button>
            </>
          )}
        </div>
      ))}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 27, "n": 6,
    "slug": "сохранение_списка_в_localstorage",
    "title": "React: сохранение списка в localStorage",
    "desc": "Задание 6: при любом изменении список сохраняется в <code>localStorage</code>, а при загрузке — "
            "восстанавливается. Синхронизация через <code>useEffect</code>.",
    "body": '<div id="root"></div>',
    "css": SHOP_CSS,
    "react": True,
    "jsx": r"""
const { useState, useEffect } = React;
const STORAGE_KEY = 'pr27_shoppingList';

function App() {
  const [items, setItems] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });
  const [inputValue, setInputValue] = useState('');

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  }, [items]);

  const addItem = (e) => {
    e.preventDefault();
    const name = inputValue.trim();
    if (!name) return;
    setItems([...items, { id: Date.now(), name, purchased: false }]);
    setInputValue('');
  };

  return (
    <div className="card shop">
      <h2>Список покупок с сохранением</h2>
      <form className="shop-form" onSubmit={addItem}>
        <input value={inputValue} onChange={(e) => setInputValue(e.target.value)} placeholder="Новый товар..." />
        <button className="rbtn" type="submit">Добавить</button>
      </form>
      {items.length === 0 && <p className="muted">Список пуст. Добавьте товар и перезагрузите страницу.</p>}
      {items.map(item => (
        <div className="shop-item" key={item.id}>
          <span className={item.purchased ? 'name done' : 'name'}>{item.name}</span>
          <button className="icon-btn" onClick={() => setItems(items.filter(i => i.id !== item.id))}>×</button>
        </div>
      ))}
      <button className="rbtn gray" style={{ marginTop: 10 }} onClick={() => setItems([])}>Очистить список</button>
      <p className="muted">Сохранено товаров: {items.length} · ключ localStorage: {STORAGE_KEY}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})

TASKS.append({
    "pr": 27, "n": 7,
    "slug": "категории_товаров",
    "title": "React: категории товаров",
    "desc": "Задание 7: у товара есть категория, список группируется по категориям через <code>reduce</code>, "
            "каждая группа выводится со своим заголовком.",
    "body": '<div id="root"></div>',
    "css": SHOP_CSS,
    "react": True,
    "jsx": r"""
const { useState } = React;

const CATEGORIES = {
  food: 'Продукты',
  chem: 'Бытовая химия',
  electronics: 'Электроника'
};

function App() {
  const [items, setItems] = useState([
    { id: 1, name: 'Молоко', category: 'food', purchased: false },
    { id: 2, name: 'Мыло', category: 'chem', purchased: false },
    { id: 3, name: 'Наушники', category: 'electronics', purchased: false },
    { id: 4, name: 'Хлеб', category: 'food', purchased: true }
  ]);
  const [name, setName] = useState('');
  const [category, setCategory] = useState('food');

  const addItem = (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    setItems([...items, { id: Date.now(), name: name.trim(), category, purchased: false }]);
    setName('');
  };

  const grouped = items.reduce((acc, item) => {
    if (!acc[item.category]) acc[item.category] = [];
    acc[item.category].push(item);
    return acc;
  }, {});

  return (
    <div className="card shop">
      <h2>Список покупок по категориям</h2>
      <form className="shop-form" onSubmit={addItem}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Новый товар..." />
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          {Object.entries(CATEGORIES).map(([key, label]) => <option key={key} value={key}>{label}</option>)}
        </select>
        <button className="rbtn" type="submit">Добавить</button>
      </form>
      {Object.entries(grouped).map(([cat, catItems]) => (
        <div key={cat}>
          <div className="cat-title">{CATEGORIES[cat]} ({catItems.length})</div>
          {catItems.map(item => (
            <div className="shop-item" key={item.id}>
              <button className="icon-btn" onClick={() => setItems(items.map(i => i.id === item.id ? { ...i, purchased: !i.purchased } : i))}>
                {item.purchased ? '✓' : '○'}
              </button>
              <span className={item.purchased ? 'name done' : 'name'}>{item.name}</span>
              <button className="icon-btn" onClick={() => setItems(items.filter(i => i.id !== item.id))}>×</button>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
""",
})
