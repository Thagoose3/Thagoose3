#!/usr/bin/env python3
"""Generate animated SVG assets for the Thagoose3 GitHub profile README.

GitHub renders README images through its image proxy as <img>, so SVGs may use
inline <style> with CSS keyframes and SMIL, but no scripts and no web fonts.
"""
import html
import os
import random
import sys

OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)

BG = "#07090d"
SURF = "#0e1219"
INK = "#eef1f5"
MUTED = "#7d8696"
BEAK = "#ff6a1a"
BEAK_SOFT = "#ffa66b"
POND = "#5ee6ff"
SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
DISPLAY = "'Arial Black', 'Segoe UI Black', 'Helvetica Neue', Arial, sans-serif"
MONO = "Consolas, 'SFMono-Regular', Menlo, 'Courier New', monospace"
E = html.escape


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


# --------------------------------------------------------------------- hero
def hero():
    W, H = 1200, 440
    hz = 300  # horizon y
    rnd = random.Random(7)

    # perspective floor: vertical lines converging to vanishing point
    vx = W / 2
    verts = []
    for i in range(-16, 17):
        x_bottom = vx + i * 95
        verts.append(f'<line x1="{vx:.1f}" y1="{hz}" x2="{x_bottom:.1f}" y2="{H}" />')
    # horizontal lines that scroll toward the viewer (each animates y + opacity)
    hlines = []
    n = 9
    for i in range(n):
        delay = -i * (3.6 / n)
        hlines.append(
            f'<line class="h" x1="0" x2="{W}" y1="{hz}" y2="{hz}" style="animation-delay:{delay:.2f}s" />'
        )

    # rising embers
    embers = []
    for i in range(46):
        x = rnd.uniform(20, W - 20)
        r = rnd.uniform(0.8, 2.6)
        dur = rnd.uniform(5, 11)
        delay = -rnd.uniform(0, dur)
        col = BEAK if rnd.random() < 0.6 else (POND if rnd.random() < 0.5 else BEAK_SOFT)
        drift = rnd.uniform(-40, 40)
        embers.append(
            f'<circle cx="{x:.1f}" cy="{H + 10}" r="{r:.1f}" fill="{col}" class="e" '
            f'style="--dx:{drift:.0f}px;animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s" />'
        )

    # starfield above horizon
    stars = []
    for i in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(0, hz - 20)
        stars.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(0.4, 1.3):.1f}" fill="{INK}" class="s" '
            f'style="animation-delay:{-rnd.uniform(0, 4):.1f}s;opacity:{rnd.uniform(0.15, 0.7):.2f}" />'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Thagoose — web apps, games and AI agents">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG}"/><stop offset="0.68" stop-color="#0d1220"/><stop offset="1" stop-color="{BG}"/>
  </linearGradient>
  <radialGradient id="sun" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{BEAK_SOFT}" stop-opacity="0.95"/>
    <stop offset="0.45" stop-color="{BEAK}" stop-opacity="0.55"/>
    <stop offset="1" stop-color="{BEAK}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{BEAK}"/><stop offset="0.5" stop-color="{BEAK_SOFT}"/><stop offset="1" stop-color="{POND}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-0.4 0;0.4 0;-0.4 0" dur="9s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="floorFade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG}" stop-opacity="1"/><stop offset="0.35" stop-color="{BG}" stop-opacity="0"/>
  </linearGradient>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="9" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="floor"><rect x="0" y="{hz}" width="{W}" height="{H - hz}"/></clipPath>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<style>
  .grid line {{ stroke: {POND}; stroke-opacity: .22; stroke-width: 1; }}
  .h {{ animation: fwd 3.6s linear infinite; }}
  @keyframes fwd {{
    0%   {{ transform: translateY(0); stroke-opacity: 0; }}
    15%  {{ stroke-opacity: .25; }}
    100% {{ transform: translateY({H - hz}px); stroke-opacity: .55; }}
  }}
  .h {{ transform-box: view-box; }}
  .e {{ animation: rise linear infinite; }}
  @keyframes rise {{
    0% {{ transform: translate(0,0); opacity: 0; }}
    10% {{ opacity: .95; }}
    100% {{ transform: translate(var(--dx), -{H + 20}px); opacity: 0; }}
  }}
  .s {{ animation: tw 4s ease-in-out infinite alternate; }}
  @keyframes tw {{ to {{ opacity: .05; }} }}
  .sun {{ animation: pulse 6s ease-in-out infinite; transform-origin: {vx}px {hz}px; }}
  @keyframes pulse {{ 50% {{ transform: scale(1.08); opacity: .85; }} }}
  .scan {{ animation: scan 5s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateY(-40px); }} to {{ transform: translateY({H}px); }} }}
  .blink {{ animation: blink 1.1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .in {{ animation: in 1.4s cubic-bezier(.2,.9,.1,1) both; }}
  .in2 {{ animation: in 1.4s .25s cubic-bezier(.2,.9,.1,1) both; }}
  .in3 {{ animation: in 1.4s .5s cubic-bezier(.2,.9,.1,1) both; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateY(18px); }} }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <g>{"".join(stars)}</g>
  <ellipse class="sun" cx="{vx}" cy="{hz}" rx="300" ry="150" fill="url(#sun)"/>
  <g class="grid" clip-path="url(#floor)">{"".join(verts)}{"".join(hlines)}</g>
  <rect x="0" y="{hz}" width="{W}" height="{H - hz}" fill="url(#floorFade)"/>
  <line x1="0" y1="{hz}" x2="{W}" y2="{hz}" stroke="{BEAK}" stroke-opacity=".7" stroke-width="1.2"/>
  <g>{"".join(embers)}</g>
  <rect class="scan" x="0" y="0" width="{W}" height="40" fill="{POND}" opacity=".035"/>

  <g font-family="{MONO}" font-size="13" fill="{MUTED}" letter-spacing="2">
    <text x="36" y="44">[ <tspan fill="{BEAK}">●</tspan> THAGOOSE.SYS ]</text>
    <text x="{W - 36}" y="44" text-anchor="end">13.7563° N · 100.5018° E</text>
    <text x="36" y="{H - 28}">WEB APPS · GAMES · AI AGENTS</text>
    <text x="{W - 36}" y="{H - 28}" text-anchor="end">BANGKOK, TH <tspan class="blink" fill="{BEAK}">▮</tspan></text>
  </g>
  <path d="M24 66 V24 H66 M{W - 66} 24 H{W - 24} V66 M24 {H - 66} V{H - 24} H66 M{W - 66} {H - 24} H{W - 24} V{H - 66}" fill="none" stroke="{BEAK}" stroke-width="2" opacity=".8"/>

  <g text-anchor="middle">
    <text class="in" x="{vx}" y="136" font-family="{MONO}" font-size="15" letter-spacing="6" fill="{INK}" opacity=".75">HI, I'M THAKUN — BUT ONLINE I'M</text>
    <text class="in2" x="{vx}" y="232" font-family="{DISPLAY}" font-weight="900" font-size="104" letter-spacing="2" fill="url(#title)" filter="url(#glow)">THAGOOSE</text>
    <text class="in3" x="{vx}" y="276" font-family="{SANS}" font-size="21" fill="{INK}" opacity=".85">I build small tools you actually use every day — and the odd goose game.</text>
  </g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="22" fill="none" stroke="{INK}" stroke-opacity=".1"/>
</svg>'''
    write("hero.svg", svg)


# ------------------------------------------------------------ section header
def header(slug, num, title, sub):
    W, H = 1200, 96
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{E(title)}">
<defs>
  <linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{BEAK}"/><stop offset=".6" stop-color="{POND}" stop-opacity=".5"/><stop offset="1" stop-color="{POND}" stop-opacity="0"/></linearGradient>
  <linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<style>
  .sw {{ animation: sw 3.8s cubic-bezier(.6,0,.3,1) infinite; }}
  @keyframes sw {{ from {{ transform: translateX(-200px); }} to {{ transform: translateX({W}px); }} }}
  .d {{ animation: d 1.6s ease-in-out infinite; }}
  @keyframes d {{ 50% {{ opacity: .2; }} }}
</style>
<text x="8" y="40" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{BEAK}">[{num}]<tspan fill="{MUTED}"> — {E(sub.upper())}</tspan></text>
<text x="8" y="76" font-family="{DISPLAY}" font-weight="900" font-size="30" letter-spacing="1" fill="#e6e9ee">{E(title.upper())}</text>
<circle class="d" cx="{W - 14}" cy="35" r="5" fill="{BEAK}"/>
<rect x="8" y="88" width="{W - 16}" height="2" fill="url(#ln)"/>
<rect class="sw" x="0" y="87" width="200" height="4" fill="url(#sweep)" opacity=".7"/>
</svg>'''
    write(f"header-{slug}.svg", svg)


# --------------------------------------------------------------- project card
PROJECTS = [
    ("morning-pulse-ai", "MorningPulse AI", "🍵", "#22d3ee", "AI morning market & news briefing, rebuilt daily by GitHub Actions", ["React", "TypeScript", "Actions"], "LIVE"),
    ("goose-survivor", "Goose Survivor", "🦆", "#f87171", "Roguelite bullet-hell: dodge, feather-fire, egg bombs, Mega Honk", ["Canvas 2D", "Web Audio"], "PLAY"),
    ("kopknob", "KopKnob", "🎛️", "#e879f9", "A tiny Windows notch: Pomodoro, media, clipboard, Thai OCR, QR", ["C# .NET 8", "WPF"], "WINDOWS"),
    ("memonote", "MEMONOTE", "📝", "#2dd4bf", "Notes with pasted images & code, [[links]] and a board mode", ["Electron", "React"], "WINDOWS"),
    ("ai-office", "AI Office", "🏢", "#a3e635", "Pixel office that shows what your AI agent team is doing, live", ["Pixel art", "Node", "Agents"], "DEMO"),
    ("goosefocus", "GooseFocus", "🪿", "#ff6a1a", "Focus timer where your goose farm grows with every hour", ["Canvas 2D", "Leaderboard"], "LIVE"),
    ("timeflow", "TimeFlow Widget", "⏳", "#818cf8", "How much of the year, month, week and day is already gone", ["Python", "Widget"], "LIVE"),
    ("papervault", "PaperVault", "📚", "#a78bfa", "Thesis studio: PDF highlights, literature matrix, citations", ["PDF.js", "IndexedDB"], "LIVE"),
    ("money-memo", "Money Memo", "💸", "#34d399", "Fast income & expense log with auto category charts", ["PWA", "Charts"], "LIVE"),
    ("exercise", "Exercise Tracker", "🏋️", "#f472b6", "Workout routines, sets and rest timers", ["PWA", "Routines"], "LIVE"),
    ("calories", "Calories Tracker", "🥗", "#fbbf24", "Daily calories, BMR/TDEE and macro balance", ["Nutrition", "Macros"], "LIVE"),
]


def card(i, slug, title, icon, accent, desc, tags, cta):
    W, H = 580, 250
    num = f"{i + 1:02d}"
    rnd = random.Random(slug)
    dots = "".join(
        f'<circle cx="{rnd.uniform(300, 560):.0f}" cy="{rnd.uniform(20, 230):.0f}" r="{rnd.uniform(.6, 1.6):.1f}" fill="{accent}" class="p" style="animation-delay:{-rnd.uniform(0, 4):.1f}s"/>'
        for _ in range(14)
    )
    chip_x = 28
    chips = []
    for t in tags:
        w = 16 + len(t) * 7.4
        chips.append(
            f'<rect x="{chip_x:.0f}" y="190" width="{w:.0f}" height="26" rx="13" fill="none" stroke="{INK}" stroke-opacity=".16"/>'
            f'<text x="{chip_x + w / 2:.0f}" y="207" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{MUTED}">{E(t)}</text>'
        )
        chip_x += w + 8
    # wrap description to two lines (~44 chars)
    words, lines, cur = desc.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > 44:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    desc_svg = "".join(
        f'<text x="28" y="{128 + k * 22}" font-family="{SANS}" font-size="15.5" fill="{INK}" opacity=".72">{E(l)}</text>' for k, l in enumerate(lines[:2])
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{E(title)}: {E(desc)}">
<defs>
  <radialGradient id="g" cx=".82" cy=".25" r=".75"><stop offset="0" stop-color="{accent}" stop-opacity=".55"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2" cx="0" cy="1.1" r=".7"><stop offset="0" stop-color="{POND}" stop-opacity=".16"/><stop offset="1" stop-color="{POND}" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{accent}" stop-opacity=".9"/><stop offset=".5" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="{accent}" stop-opacity=".5"/></linearGradient>
  <clipPath id="c"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
  .glow {{ animation: br 5s ease-in-out infinite; transform-origin: 470px 70px; }}
  @keyframes br {{ 50% {{ transform: scale(1.15); opacity: .7; }} }}
  .fl {{ animation: fl 4.5s ease-in-out infinite; }}
  @keyframes fl {{ 50% {{ transform: translateY(-8px) rotate(-4deg); }} }}
  .fl {{ transform-box: fill-box; transform-origin: center; }}
  .p {{ animation: tw 3s ease-in-out infinite alternate; }}
  @keyframes tw {{ to {{ opacity: .1; }} }}
  .ring {{ animation: spin 18s linear infinite; transform-origin: 470px 100px; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
</style>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{SURF}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect class="glow" width="{W}" height="{H}" fill="url(#g)"/>
  <rect width="{W}" height="{H}" fill="url(#g2)"/>
  {dots}
  <text x="{W - 20}" y="{H - 14}" text-anchor="end" font-family="{DISPLAY}" font-weight="900" font-size="120" fill="none" stroke="{accent}" stroke-opacity=".28" stroke-width="1.2">{num}</text>
  <circle class="ring" cx="470" cy="100" r="62" fill="none" stroke="{accent}" stroke-opacity=".45" stroke-dasharray="4 9"/>
  <circle cx="470" cy="100" r="48" fill="#000" fill-opacity=".28" stroke="#fff" stroke-opacity=".12"/>
  <text class="fl" x="470" y="118" text-anchor="middle" font-size="50">{icon}</text>
  <text x="28" y="44" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="{accent}">{num} / {cta}</text>
  <text x="28" y="88" font-family="{DISPLAY}" font-weight="900" font-size="30" fill="{INK}">{E(title.upper())}</text>
  {desc_svg}
  {"".join(chips)}
  <text x="{W - 28}" y="44" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{INK}" opacity=".8">{"CODE ↗" if cta == "WINDOWS" else "OPEN ↗"}</text>
</g>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
</svg>'''
    write(f"cards/{slug}.svg", svg)


# ------------------------------------------------------------------ footer
def footer():
    W, H = 1200, 120
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Peace was never an option.">
<defs><linearGradient id="t" x1="0" x2="1"><stop offset="0" stop-color="{BEAK}"/><stop offset="1" stop-color="{POND}"/></linearGradient></defs>
<style>
  .w {{ animation: walk 14s linear infinite; }}
  @keyframes walk {{ from {{ transform: translateX(-120px); }} to {{ transform: translateX({W + 40}px); }} }}
  .b {{ animation: bob .45s ease-in-out infinite alternate; }}
  @keyframes bob {{ to {{ transform: translateY(-3px); }} }}
</style>
<line x1="0" y1="96" x2="{W}" y2="96" stroke="#fff" stroke-opacity=".1"/>
<text x="{W / 2}" y="52" text-anchor="middle" font-family="{MONO}" font-size="15" letter-spacing="5" fill="url(#t)">PEACE WAS NEVER AN OPTION.</text>
<g class="w"><g class="b">
  <ellipse cx="40" cy="84" rx="22" ry="11" fill="#fff"/>
  <path d="M52 80 C 58 66, 50 58, 54 46" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round"/>
  <circle cx="55" cy="44" r="8" fill="#fff"/>
  <path d="M62 42 l11 3 -11 4z" fill="{BEAK}"/>
  <circle cx="57" cy="42" r="1.6" fill="{BG}"/>
  <path d="M34 95 v6 M44 95 v6" stroke="{BEAK}" stroke-width="3" stroke-linecap="round"/>
</g></g>
</svg>'''
    write("footer.svg", svg)


def more():
    W, H = 580, 250
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="See everything on the portfolio">
<style>
  .a {{ animation: a 1.6s ease-in-out infinite; }}
  @keyframes a {{ 50% {{ transform: translateX(10px); }} }}
  .dash {{ animation: m 20s linear infinite; }}
  @keyframes m {{ to {{ stroke-dashoffset: -400; }} }}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="{BG}" />
<rect class="dash" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="{BEAK}" stroke-opacity=".6" stroke-dasharray="8 10" />
<text x="28" y="44" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="{MUTED}">+ MORE</text>
<text x="28" y="120" font-family="{DISPLAY}" font-weight="900" font-size="34" fill="{INK}">THE FULL</text>
<text x="28" y="160" font-family="{DISPLAY}" font-weight="900" font-size="34" fill="{BEAK}">PORTFOLIO</text>
<text x="28" y="205" font-family="{SANS}" font-size="15.5" fill="{INK}" opacity=".7">WebGL, scroll effects &amp; every project in one place</text>
<text class="a" x="{W - 40}" y="160" text-anchor="end" font-family="{SANS}" font-size="44" fill="{BEAK}">→</text>
</svg>'''
    write("cards/more.svg", svg)


hero()
more()
header("work", "01", "Selected work", "11 projects · web, games & windows apps")
header("stack", "02", "Toolbox", "what I build with")
header("activity", "03", "Activity", "the goose eats my contributions")
header("support", "04", "Support", "buy the goose a coffee")
for i, p in enumerate(PROJECTS):
    card(i, *p)
footer()
print("ok")
