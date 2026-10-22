#!/usr/bin/env python3
"""Сборка страниц самостоятельных работ ПР17-ПР32 и хаба index.html.

Каждая задача — отдельная автономная HTML-страница. Общая оболочка
(стили, навигация, шапка) формируется здесь, содержимое задач лежит
в модулях tasks_part1.py, tasks_part2.py, tasks_part3.py.
"""
import os
import re
import html
import glob

from tasks_part1 import TASKS as T1
from tasks_part2 import TASKS as T2
from tasks_part3 import TASKS as T3

BASE = os.path.dirname(os.path.abspath(__file__))
TASKS = sorted(T1 + T2 + T3, key=lambda t: (t["pr"], t["n"]))

PR_TITLES = {
    17: "Инкапсуляция",
    18: "Расширение браузера",
    19: "Чат-бот",
    20: "Форма кредитной карты",
    21: "API Госуслуг",
    22: "Основы классов",
    23: "Наследование и полиморфизм",
    24: "DOM: рендеринг и события",
    25: "LocalStorage",
    26: "React: счётчик",
    27: "React: списки",
    28: "React: props и темы",
    29: "React: таймеры",
    30: "React: API",
    31: "React: калькулятор",
    32: "React: фильтрация",
}

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Arial,sans-serif;background:#f0f2f5;color:#222;padding:24px;line-height:1.55}
.wrap{max-width:900px;margin:0 auto}
.topnav{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.topnav a{color:#1a73e8;text-decoration:none;font-size:14px}
.topnav a:hover{text-decoration:underline}
.navbtns{display:flex;gap:8px;flex-wrap:wrap}
.navbtns .btn{background:#fff;border:1px solid #cbd5e1;border-radius:8px;padding:8px 14px;font-size:13px;cursor:pointer;color:#0b57d0;text-decoration:none}
.navbtns .btn:hover{background:#eef6ff}
.navbtns .btn:disabled{opacity:.4;cursor:default}
h1{color:#1a73e8;margin-bottom:4px;font-size:24px}
.pr-tag{display:inline-block;background:#1a73e8;color:#fff;border-radius:12px;padding:2px 12px;font-size:13px;margin-bottom:10px}
.desc{background:#eef6ff;border:1px solid #c9e3ff;border-radius:10px;padding:12px 16px;margin:14px 0;color:#1a56a0;font-size:14px}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:20px 22px;margin:16px 0;box-shadow:0 2px 6px rgba(0,0,0,0.05)}
.card h2{font-size:17px;color:#333;margin-bottom:10px}
.btn{background:#1a73e8;color:#fff;border:none;border-radius:8px;padding:10px 18px;font-size:14px;cursor:pointer;margin:6px 6px 0 0;transition:all .2s}
.btn:hover{background:#0b5bc0}
.btn.green{background:#28a745}.btn.green:hover{background:#1e7e34}
.btn.red{background:#dc3545}.btn.red:hover{background:#c82333}
.btn.orange{background:#f39c12}.btn.orange:hover{background:#d68910}
.btn.gray{background:#64748b}.btn.gray:hover{background:#475569}
.btn:disabled{opacity:.45;cursor:not-allowed}
input,select,textarea{padding:9px 12px;border:2px solid #e0e0e0;border-radius:8px;font-size:14px;margin:4px 6px 4px 0;font-family:inherit}
input:focus,select:focus,textarea:focus{border-color:#1a73e8;outline:none}
label{font-size:14px;color:#555}
.out{background:#0f172a;color:#e2e8f0;padding:14px;border-radius:8px;font-family:Consolas,monospace;font-size:13px;margin:12px 0;white-space:pre-wrap;min-height:40px}
.ok{color:#2ecc71}.err{color:#ff6b6b}.hl{color:#f1c40f}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:14px}
th,td{border:1px solid #cbd5e1;padding:8px;text-align:left}
th{background:#eef2ff}
footer{margin-top:24px;font-size:12px;color:#999;text-align:center}
ol{padding-left:20px}
ol li{margin:6px 0}
ol a{color:#0b57d0;text-decoration:none;font-size:15px}
ol a:hover{text-decoration:underline}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:8px 0}
.grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.item{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px 12px;margin:6px 0;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.muted{color:#777;font-size:13px}
.chip{display:inline-block;background:#eef2ff;border:1px solid #c7d2fe;border-radius:999px;padding:2px 10px;font-size:12px;color:#3730a3;margin:2px}
pre.code{background:#0f172a;color:#e2e8f0;padding:14px;border-radius:8px;overflow:auto;font-size:12px;line-height:1.5;max-height:420px}
details{margin:14px 0}
summary{cursor:pointer;color:#0b57d0;font-size:14px;user-select:none}
.preview{background:#f8fafc;border:1px dashed #cbd5e1;border-radius:10px;padding:14px;margin:12px 0}
.preview.dark{background:#1a1a1a;color:#fff;border-color:#444}
.preview.dark input,.preview.dark select{background:#2d2d2d;color:#fff;border-color:#555}
.pill{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid #cbd5e1;border-radius:999px;padding:6px 12px;font-size:13px;cursor:pointer}
.pill.active{background:#1a73e8;color:#fff;border-color:#1a73e8}
.stat{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:10px 14px;text-align:center;min-width:90px}
.stat b{display:block;font-size:20px;color:#1a73e8}
.stat span{font-size:12px;color:#777}
.rbtn{padding:10px 18px;border:none;border-radius:8px;background:#1a73e8;color:#fff;font-size:14px;cursor:pointer}
.rbtn:hover{background:#0b5bc0}
.rbtn.gray{background:#64748b}.rbtn.gray:hover{background:#475569}
.rbtn.green{background:#28a745}.rbtn.green:hover{background:#1e7e34}
.rbtn.red{background:#dc3545}.rbtn.red:hover{background:#c82333}
.rbtn:disabled{opacity:.45;cursor:not-allowed}
"""


def esc(text):
    return html.escape(text)


def nav_buttons(prev_task, next_task, klass=""):
    if prev_task:
        prev = ('<button class="btn" onclick="location.href=\'%s\'">← Пред.</button>'
                % prev_task["file"])
    else:
        prev = '<button class="btn" disabled>← Пред.</button>'
    if next_task:
        nxt = ('<button class="btn" onclick="location.href=\'%s\'">След. →</button>'
               % next_task["file"])
    else:
        nxt = ('<button class="btn" onclick="location.href=\'index.html\'">След. →</button>')
    return '<div class="navbtns %s">%s%s</div>' % (klass, prev, nxt)


def build_page(task, prev_task, next_task, number, total):
    head_title = "ПР%02d • Зад.%d • %s" % (task["pr"], task["n"], task["title"])
    details = ""
    code = task.get("script") or task.get("jsx")
    if code and task.get("show_code", True):
        details = ('<details><summary>Показать код решения</summary>'
                   '<pre class="code">%s</pre></details>' % esc(code.strip()))

    if task.get("react"):
        scripts = ("""<script crossorigin src="https://unpkg.com/react@18.3.1/umd/react.development.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone@7.26.4/babel.min.js"></script>
<script type="text/babel" data-presets="react">
%s
</script>""" % task["jsx"])
    else:
        scripts = ("<script>\nconst $ = (id) => document.getElementById(id);\n"
                   "function out(html) { const el = $('out'); if (el) el.innerHTML = html; }\n"
                   "function esc(s) { return String(s).replace(/[&<>\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c])); }\n"
                   "%s\n</script>" % task["script"])

    return """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{head_title}</title>
<style>{css}{extra_css}</style>
</head>
<body>
<div class="wrap">
<div class="topnav">
  <a href="index.html">« Хаб самостоятельных работ</a>
  {nav_top}
</div>
<span class="pr-tag">ПР{pr:02d} • Зад.{n}</span>
<h1>{title}</h1>
<div class="desc">{desc}</div>
{body}
{details}
{nav_bottom}
<footer>Хаб самостоятельных работ JavaScript · ПР{pr:02d} · страница {number} из {total}</footer>
</div>
{scripts}
</body>
</html>
""".format(
        head_title=head_title,
        css=CSS,
        extra_css=task.get("css", ""),
        nav_top=nav_buttons(prev_task, next_task),
        pr=task["pr"],
        n=task["n"],
        title=task["title"],
        desc=task["desc"],
        body=task["body"],
        details=details,
        nav_bottom=nav_buttons(prev_task, next_task, "st"),
        number=number,
        total=total,
        scripts=scripts,
    )


def title_from_file(path):
    try:
        text = open(path, encoding="utf-8").read()
    except Exception:
        return None
    m = re.search(r"<title>(.*?)</title>", text, re.S)
    if not m:
        return None
    title = html.unescape(m.group(1)).strip()
    title = re.sub(r"^ПР\d+\s*•\s*Зад\.?\s*\d+\s*•\s*", "", title)
    return title


def build_index():
    entries = []
    for path in glob.glob(os.path.join(BASE, "пр*.html")):
        name = os.path.basename(path)
        m = re.match(r"пр(\d{2})_зад(\d+)_(.+)\.html$", name)
        if not m:
            continue
        pr, n = int(m.group(1)), int(m.group(2))
        title = title_from_file(path) or m.group(3).replace("_", " ")
        entries.append((pr, n, name, title))
    entries.sort(key=lambda e: (e[0], e[1]))

    total = len(entries)
    cards = []
    by_pr = {}
    for pr, n, name, title in entries:
        by_pr.setdefault(pr, []).append((n, name, title))

    counter = 0
    for pr in sorted(by_pr):
        items = []
        for n, name, title in sorted(by_pr[pr], key=lambda x: x[0]):
            counter += 1
            items.append('<li><a href="%s">%d. %s</a></li>' % (name, counter, esc(title)))
        cards.append(
            '<div class="card"><h2>ПР%02d <span style="font-weight:normal;color:#999;font-size:14px">'
            '(%d)</span> <span style="font-weight:normal;color:#999;font-size:14px">— %s</span></h2>'
            '<ol>%s</ol></div>' % (pr, len(items), esc(PR_TITLES.get(pr, "")), "".join(items))
        )

    index = """<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Самостоятельные работы — index</title><style>%s</style></head>
<body><div class="wrap"><h1>Самостоятельные работы по JavaScript</h1>
<p class="desc">Все самостоятельные задачи из практических работ ПР03–ПР32 — %d страниц. Каждая задача открывается отдельно; переход между страницами — кнопками «← Пред.» и «След. →».</p>
<div class='card' style='background:#fff7e6;border-color:#f5e6a8'><b>Как пользоваться:</b> index.html — хаб со ссылками на все самостоятельные задачи. Страницы ПР17–ПР32 собраны скриптом <code>make_selfwork.py</code>. Задачи ПР26–ПР32 используют React 18 через CDN (нужен интернет), остальные работают полностью офлайн.</div>
%s
</div></body></html>
""" % (CSS, total, "\n".join(cards))
    open(os.path.join(BASE, "index.html"), "w", encoding="utf-8").write(index)
    return total


def main():
    total = len(TASKS)
    keep = set()
    for i, task in enumerate(TASKS):
        task["file"] = "пр%02d_зад%d_%s.html" % (task["pr"], task["n"], task["slug"])
        keep.add(task["file"])

    removed = []
    for path in glob.glob(os.path.join(BASE, "пр*.html")):
        name = os.path.basename(path)
        m = re.match(r"пр(\d{2})_", name)
        if m and int(m.group(1)) >= 17 and name not in keep:
            os.remove(path)
            removed.append(name)

    for i, task in enumerate(TASKS):
        prev_task = TASKS[i - 1] if i > 0 else {"file": "пр16_зад4_экспорт_данных_в_json.html"}
        next_task = TASKS[i + 1] if i + 1 < total else None
        page = build_page(task, prev_task, next_task, i + 1, total)
        open(os.path.join(BASE, task["file"]), "w", encoding="utf-8").write(page)

    pages = build_index()
    print("Страниц задач: %d" % total)
    print("Страниц в хабе: %d" % pages)
    if removed:
        print("Удалены старые файлы:")
        for name in sorted(removed):
            print("  -", name)


if __name__ == "__main__":
    main()
