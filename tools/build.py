import json, os, textwrap, sys
from xml.sax.saxutils import escape as esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, "profile.json"), encoding="utf-8"))

THEMES = {
  "dark":  dict(bg="#0b0f13", bg2="#121920", fg="#e6edf3", mut="#8b98a5", acc="#2dd4bf", acc2="#fbbf24", line="#26313c", chip="#16202a", ondark="#0b0f13"),
  "light": dict(bg="#fbf8f3", bg2="#f3eee6", fg="#1f2328", mut="#6b6258", acc="#0f766e", acc2="#b45309", line="#ddd4c6", chip="#ece5d9", ondark="#fbf8f3"),
}
SANS = "Segoe UI, Helvetica, Arial, sans-serif"
MONO = "Consolas, Menlo, monospace"
W = 900

def wrap(s, n): return textwrap.wrap(s, n) or [""]

def svg(w, h, body, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<rect width="{w}" height="{h}" rx="14" fill="{t["bg"]}"/>{body}</svg>')

def head(num, label, t, y=44):
    return (f'<text x="40" y="{y}" font-family="{MONO}" font-size="14" letter-spacing="3" fill="{t["acc"]}">{num} / {esc(label.upper())}</text>'
            f'<rect x="40" y="{y+12}" width="48" height="3" rx="1.5" fill="{t["acc2"]}"/>')

def hero(t):
    grid = "".join(f'<path d="M{x} 0V300" stroke="{t["line"]}" stroke-width="1" opacity=".5"/>' for x in range(0, W, 45))
    grid += "".join(f'<path d="M0 {y}H{W}" stroke="{t["line"]}" stroke-width="1" opacity=".5"/>' for y in range(0, 300, 45))
    b = (f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{t["acc"]}" stop-opacity=".0"/><stop offset="1" stop-color="{t["acc"]}" stop-opacity=".28"/></linearGradient></defs>'
         f'{grid}<rect width="{W}" height="300" rx="14" fill="url(#g)"/>'
         f'<text x="48" y="92" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{t["acc"]}">&gt; HELLO, WORLD</text>'
         f'<text x="48" y="170" font-family="{SANS}" font-size="64" font-weight="700" fill="{t["fg"]}">{esc(P["name"])}</text>'
         f'<text x="48" y="212" font-family="{SANS}" font-size="24" fill="{t["fg"]}">{esc(P["role"])}</text>'
         f'<text x="48" y="248" font-family="{MONO}" font-size="15" fill="{t["mut"]}">{esc(P["location"])}</text>'
         f'<rect x="48" y="266" width="120" height="4" rx="2" fill="{t["acc2"]}"/>')
    return svg(W, 300, b, t)

def about(t):
    lines = wrap(P["about"], 70)
    y0 = 140 + 30 * len(lines)
    b = head("01", "About", t)
    b += f'<text x="40" y="96" font-family="{SANS}" font-size="30" font-weight="700" fill="{t["fg"]}">{esc(P["tagline"])}</text>'
    for i, l in enumerate(lines):
        b += f'<text x="40" y="{132+i*28}" font-family="{SANS}" font-size="17" fill="{t["mut"]}">{esc(l)}</text>'
    n = len(P["stats"]); cw = (W - 80 - (n-1)*16) // n
    for i, (v, lab) in enumerate(P["stats"]):
        x = 40 + i*(cw+16)
        b += (f'<rect x="{x}" y="{y0-10}" width="{cw}" height="92" rx="10" fill="{t["bg2"]}" stroke="{t["line"]}"/>'
              f'<text x="{x+20}" y="{y0+36}" font-family="{SANS}" font-size="36" font-weight="700" fill="{t["acc"]}">{esc(v)}</text>'
              f'<text x="{x+20}" y="{y0+64}" font-family="{MONO}" font-size="13" fill="{t["mut"]}">{esc(lab)}</text>')
    return svg(W, y0 + 100, b, t)

def work_head(t):
    b = head("02", "Selected work", t) + f'<text x="40" y="96" font-family="{SANS}" font-size="30" font-weight="700" fill="{t["fg"]}">Things I have shipped</text>'
    return svg(W, 120, b, t)

def card(p, i, t):
    cw, ch = 440, 120
    b = (f'<rect x="1" y="1" width="{cw-2}" height="{ch-2}" rx="12" fill="{t["bg2"]}" stroke="{t["line"]}"/>'
         f'<text x="24" y="40" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{t["acc2"]}">{i+1:02d}</text>'
         f'<text x="24" y="70" font-family="{SANS}" font-size="22" font-weight="700" fill="{t["fg"]}">{esc(p["title"])}</text>'
         f'<text x="24" y="94" font-family="{SANS}" font-size="14" fill="{t["mut"]}">{esc(p["desc"])}</text>'
         f'<rect x="{cw-24-len(p["tag"])*8-20}" y="22" width="{len(p["tag"])*8+20}" height="26" rx="13" fill="{t["chip"]}"/>'
         f'<text x="{cw-24-len(p["tag"])*8-10}" y="40" font-family="{MONO}" font-size="12" fill="{t["acc"]}">{esc(p["tag"])}</text>')
    return svg(cw, ch, b, t)

def how(t):
    b = head("03", "How I work", t) + f'<text x="40" y="96" font-family="{SANS}" font-size="30" font-weight="700" fill="{t["fg"]}">Process, not luck</text>'
    y = 140
    for i, s in enumerate(P["how"]):
        b += (f'<circle cx="52" cy="{y-5}" r="13" fill="{t["acc"]}"/><text x="52" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{t["ondark"]}">{i+1}</text>'
              f'<text x="80" y="{y}" font-family="{SANS}" font-size="17" fill="{t["fg"]}">{esc(s)}</text>')
        y += 42
    return svg(W, y + 10, b, t)

def toolkit(t):
    b = head("04", "Toolkit", t) + f'<text x="40" y="96" font-family="{SANS}" font-size="30" font-weight="700" fill="{t["fg"]}">What I build with</text>'
    y = 140
    for grp, items in P["toolkit"]:
        b += f'<text x="40" y="{y+18}" font-family="{MONO}" font-size="13" letter-spacing="1" fill="{t["mut"]}">{esc(grp.upper())}</text>'
        x = 250
        for it in items:
            wd = len(it) * 9 + 28
            b += (f'<rect x="{x}" y="{y}" width="{wd}" height="30" rx="15" fill="{t["chip"]}" stroke="{t["line"]}"/>'
                  f'<text x="{x+wd/2}" y="{y+20}" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{t["fg"]}">{esc(it)}</text>')
            x += wd + 10
        y += 50
    return svg(W, y + 10, b, t)

def path(t):
    b = head("05", "Path", t) + f'<text x="40" y="96" font-family="{SANS}" font-size="30" font-weight="700" fill="{t["fg"]}">Where I have been</text>'
    y = 142; n = len(P["path"])
    b += f'<path d="M62 {y-4}V{y+(n-1)*66+4}" stroke="{t["line"]}" stroke-width="2"/>'
    for when, what, sub in P["path"]:
        b += (f'<circle cx="62" cy="{y-4}" r="7" fill="{t["acc"]}"/>'
              f'<text x="90" y="{y-6}" font-family="{MONO}" font-size="13" fill="{t["acc2"]}">{esc(when)}</text>'
              f'<text x="90" y="{y+16}" font-family="{SANS}" font-size="19" font-weight="700" fill="{t["fg"]}">{esc(what)}</text>'
              f'<text x="90" y="{y+38}" font-family="{SANS}" font-size="14" fill="{t["mut"]}">{esc(sub)}</text>')
        y += 66
    return svg(W, y + 10, b, t)

def signal(t):
    b = head("06", "Signal", t) + f'<text x="40" y="96" font-family="{SANS}" font-size="30" font-weight="700" fill="{t["fg"]}">Live from GitHub</text>'
    return svg(W, 120, b, t)

def contact_head(t):
    b = head("07", "Contact", t) + f'<text x="40" y="96" font-family="{SANS}" font-size="30" font-weight="700" fill="{t["fg"]}">Let us build something</text>'
    return svg(W, 120, b, t)

def button(label, t):
    w = len(label) * 10 + 60
    b = (f'<rect x="1" y="1" width="{w-2}" height="46" rx="23" fill="{t["acc"]}"/>'
         f'<text x="{w/2}" y="30" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{t["ondark"]}">{esc(label)}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="48" viewBox="0 0 {w} 48" role="img">{b}</svg>'

def footer(t):
    b = (f'<text x="{W/2}" y="64" text-anchor="middle" font-family="{SANS}" font-size="24" font-style="italic" fill="{t["fg"]}">&#8220;{esc(P["quote"])}&#8221;</text>'
         f'<rect x="{W/2-30}" y="86" width="60" height="3" rx="1.5" fill="{t["acc2"]}"/>')
    return svg(W, 120, b, t)

def out(mode, name, content):
    d = os.path.join(ROOT, "assets", mode); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, name + ".svg"), "w", encoding="utf-8").write(content)

def pic(name, alt, w=None):
    wa = f' width="{w}"' if w else ""
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/dark/{name}.svg">\n'
            f'  <img src="assets/light/{name}.svg" alt="{esc(alt)}"{wa}>\n</picture>')

for mode, t in THEMES.items():
    out(mode, "hero", hero(t)); out(mode, "about", about(t)); out(mode, "work", work_head(t))
    for i, p in enumerate(P["projects"]): out(mode, f"card{i+1}", card(p, i, t))
    out(mode, "how", how(t)); out(mode, "toolkit", toolkit(t)); out(mode, "path", path(t))
    out(mode, "signal", signal(t)); out(mode, "contact", contact_head(t)); out(mode, "footer", footer(t))
    for i, (lab, _) in enumerate(P["contact"]): out(mode, f"btn{i+1}", button(lab, t))

u = P["username"]
rows = []
cards = [f'<a href="{p["url"]}">{pic(f"card{i+1}", p["title"], 440)}</a>' for i, p in enumerate(P["projects"])]
for i in range(0, len(cards), 2):
    pair = cards[i:i+2]
    rows.append("  <tr>\n" + "\n".join(f"    <td>\n{c}\n    </td>" for c in pair) + "\n  </tr>")
table = '<table align="center" width="900">\n' + "\n".join(rows) + "\n</table>"
btns = " ".join(f'<a href="{url}">{pic(f"btn{i+1}", lab)}</a>' for i, (lab, url) in enumerate(P["contact"]))
stats = (f'<img src="https://github-readme-stats.vercel.app/api?username={u}&show_icons=true&hide_border=true&bg_color=0b0f13&title_color=2dd4bf&icon_color=fbbf24&text_color=e6edf3" height="170" alt="GitHub stats">\n'
         f'<img src="https://github-readme-stats.vercel.app/api/top-langs/?username={u}&layout=compact&hide_border=true&bg_color=0b0f13&title_color=2dd4bf&text_color=e6edf3" height="170" alt="Top languages">')
md = f"""<div align="center">

{pic("hero", P["name"] + " - " + P["role"], 900)}

{pic("about", "About", 900)}

{pic("work", "Selected work", 900)}

{table}

{pic("how", "How I work", 900)}

{pic("toolkit", "Toolkit", 900)}

{pic("path", "Path", 900)}

{pic("signal", "Signal", 900)}

{stats}

{pic("contact", "Contact", 900)}

{btns}

{pic("footer", P["quote"], 900)}

</div>
"""
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(md)
print("built", len(os.listdir(os.path.join(ROOT, "assets", "dark"))), "assets per theme")
