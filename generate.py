# -*- coding: utf-8 -*-
import math, html

# ---------- palette ----------
CREAM="#FBF6EE"; CARD="#FFFFFF"; INK="#1F2A37"; NAVY="#22344B"; MUTED="#6B7280"
LINE="#ECE3D5"; TEAL="#5FBEAC"; PINK="#EC5C93"; YELLOW="#EBB84D"; GREEN="#68C29A"
PURPLE="#B98FD9"; ORANGE="#E4933D"; BLUE="#7C83E0"; MAUVE="#A9789B"; RED="#E06A5A"

def esc(s): return html.escape(str(s))

# ---------- components ----------
def eyebrow(text, color=ORANGE):
    return f'<span class="eyebrow" style="background:{color}22;color:{color}">{esc(text)}</span>'

def tile(num, label, accent=TEAL, sub=""):
    subhtml=f'<div class="t-sub">{esc(sub)}</div>' if sub else ""
    return (f'<div class="tile" style="border-top:3px solid {accent}">'
            f'<div class="t-num">{esc(num)}</div>'
            f'<div class="t-lab">{esc(label)}</div>{subhtml}</div>')

def tiles(items):
    return '<div class="tiles">'+''.join(tile(*i) for i in items)+'</div>'

def hbars(items, maxv=None, unit="", height_per=34, fmt=None, labw=190, valw=70):
    # items: list of (label, value, color)
    # labw = left gutter for labels, valw = right reserve for the value text.
    # Widen both when labels carry locations or the unit string is long.
    if maxv is None: maxv=max(v for _,v,_ in items) or 1
    if fmt is None: fmt=lambda v: f"{v:,}"
    W=680; barw=W-labw-valw; H=len(items)*height_per+8
    rows=[]
    for i,(lab,val,col) in enumerate(items):
        y=i*height_per+6; bw=max(2,(val/maxv)*barw)
        rows.append(f'<text x="{labw-10}" y="{y+16}" text-anchor="end" class="bl">{esc(lab)}</text>')
        rows.append(f'<rect x="{labw}" y="{y+4}" width="{bw:.1f}" height="20" rx="5" fill="{col}"/>')
        rows.append(f'<text x="{labw+bw+8:.1f}" y="{y+19}" class="bv">{esc(fmt(val))}{esc(unit)}</text>')
    return f'<svg viewBox="0 0 {W} {H}" class="chart" role="img">{"".join(rows)}</svg>'

def vbars(items, maxv=None, unit="", fmt=None, note_hi=None):
    # items list of (label,value,color)
    if maxv is None: maxv=max(v for _,v,_ in items) or 1
    if fmt is None: fmt=lambda v:f"{v:,}"
    W=680; H=230; pad_l=44; pad_b=40; plot_h=H-pad_b-24; plot_w=W-pad_l-20
    n=len(items); slot=plot_w/n; bw=min(54, slot*0.6)
    rows=[]
    # gridlines
    for g in range(0,5):
        gy=24+plot_h-(g/4)*plot_h; gval=maxv*g/4
        rows.append(f'<line x1="{pad_l}" y1="{gy:.1f}" x2="{W-20}" y2="{gy:.1f}" stroke="{LINE}"/>')
        rows.append(f'<text x="{pad_l-8}" y="{gy+4:.1f}" text-anchor="end" class="ax">{gval:,.0f}</text>')
    for i,(lab,val,col) in enumerate(items):
        cx=pad_l+slot*i+slot/2; bh=(val/maxv)*plot_h; y=24+plot_h-bh
        rows.append(f'<rect x="{cx-bw/2:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="5" fill="{col}"/>')
        rows.append(f'<text x="{cx:.1f}" y="{y-6:.1f}" text-anchor="middle" class="bv">{esc(fmt(val))}</text>')
        rows.append(f'<text x="{cx:.1f}" y="{H-14:.1f}" text-anchor="middle" class="ax2">{esc(lab)}</text>')
    return f'<svg viewBox="0 0 {W} {H}" class="chart" role="img">{"".join(rows)}</svg>'

def area(values, labels, color=TEAL, unit="", markevery=None, hi_idx=None):
    W=680; H=220; pad_l=44; pad_b=34; plot_h=H-pad_b-20; plot_w=W-pad_l-16
    maxv=max(values) or 1; n=len(values)
    def X(i): return pad_l+(i/(n-1))*plot_w
    def Y(v): return 20+plot_h-(v/maxv)*plot_h
    pts=[(X(i),Y(v)) for i,v in enumerate(values)]
    line=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    areapath=f"M{pts[0][0]:.1f},{20+plot_h:.1f} "+" ".join(f"L{x:.1f},{y:.1f}" for x,y in pts)+f" L{pts[-1][0]:.1f},{20+plot_h:.1f} Z"
    rows=[]
    for g in range(0,5):
        gy=20+plot_h-(g/4)*plot_h; gval=maxv*g/4
        rows.append(f'<line x1="{pad_l}" y1="{gy:.1f}" x2="{W-16}" y2="{gy:.1f}" stroke="{LINE}"/>')
        rows.append(f'<text x="{pad_l-8}" y="{gy+4:.1f}" text-anchor="end" class="ax">{gval:,.0f}</text>')
    rows.append(f'<path d="{areapath}" fill="{color}22"/>')
    rows.append(f'<polyline points="{line}" fill="none" stroke="{color}" stroke-width="2.5"/>')
    # markers on highlights
    if hi_idx:
        for i in hi_idx:
            rows.append(f'<circle cx="{X(i):.1f}" cy="{Y(values[i]):.1f}" r="3.5" fill="{color}"/>')
            rows.append(f'<text x="{X(i):.1f}" y="{Y(values[i])-8:.1f}" text-anchor="middle" class="bv">{values[i]:,}</text>')
    # x labels
    step=max(1,n//8)
    for i in range(0,n,step):
        rows.append(f'<text x="{X(i):.1f}" y="{H-12:.1f}" text-anchor="middle" class="ax2">{esc(labels[i])}</text>')
    return f'<svg viewBox="0 0 {W} {H}" class="chart" role="img">{"".join(rows)}</svg>'

def donut(segments, center_num="", center_lab=""):
    # segments list of (label,value,color)
    total=sum(v for _,v,_ in segments) or 1
    W=430; cx=115; cy=115; r=88; sw=30
    rows=[]; ang=-90
    for lab,val,col in segments:
        frac=val/total; a2=ang+frac*360
        large=1 if frac>0.5 else 0
        x1=cx+r*math.cos(math.radians(ang)); y1=cy+r*math.sin(math.radians(ang))
        x2=cx+r*math.cos(math.radians(a2)); y2=cy+r*math.sin(math.radians(a2))
        rows.append(f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 {large} 1 {x2:.1f},{y2:.1f}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
        ang=a2
    if center_num:
        rows.append(f'<text x="{cx}" y="{cy-2}" text-anchor="middle" class="dnum">{esc(center_num)}</text>')
        rows.append(f'<text x="{cx}" y="{cy+18}" text-anchor="middle" class="dlab">{esc(center_lab)}</text>')
    leg=[]
    for lab,val,col in segments:
        pct=val/total*100
        leg.append(f'<div class="lg"><span class="dot" style="background:{col}"></span><span class="lgl">{esc(lab)}</span><span class="lgv">{val:,} · {pct:.0f}%</span></div>')
    return (f'<div class="donutwrap"><svg viewBox="0 0 240 240" class="donut" role="img">{"".join(rows)}</svg>'
            f'<div class="legend">{"".join(leg)}</div></div>')

def table(headers, rows, aligns=None, hi_cols=None, hi_color=PINK):
    hi_cols=hi_cols or []
    aligns=aligns or ["left"]+["right"]*(len(headers)-1)
    th="".join(f'<th style="text-align:{aligns[i]}">{esc(h)}</th>' for i,h in enumerate(headers))
    trs=[]
    for r in rows:
        tds=[]
        for i,c in enumerate(r):
            style=f"text-align:{aligns[i]}"
            if i in hi_cols: style+=f";color:{hi_color};font-weight:700"
            tds.append(f'<td style="{style}">{esc(c)}</td>')
        trs.append("<tr>"+"".join(tds)+"</tr>")
    return f'<table class="tbl"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table>'

def stepper(steps):
    items=[]
    for i,s in enumerate(steps):
        items.append(f'<div class="step"><span class="stepn">{i+1}</span><span class="steptxt">{esc(s)}</span></div>')
        if i<len(steps)-1: items.append('<span class="steparr">→</span>')
    return '<div class="stepper">'+''.join(items)+'</div>'

def funnel(steps):
    # steps: (label, value, color) rendered as descending stat blocks
    out=[]
    for i,(lab,val,col) in enumerate(steps):
        out.append(f'<div class="fstep" style="border-left:4px solid {col}"><div class="fval">{esc(val)}</div><div class="flab">{esc(lab)}</div></div>')
        if i<len(steps)-1: out.append('<div class="farr">▼</div>')
    return '<div class="funnel">'+''.join(out)+'</div>'

def card(inner, klass=""):
    return f'<div class="card {klass}">{inner}</div>'

def chart_card(title, chart, sub=""):
    subhtml=f'<p class="csub">{esc(sub)}</p>' if sub else ""
    return card(f'<h3 class="ctitle">{esc(title)}</h3>{subhtml}{chart}')

def legend_inline(items):
    return '<div class="ilegend">'+''.join(f'<span class="il"><span class="dot" style="background:{c}"></span>{esc(l)}</span>' for l,c in items)+'</div>'

def callout(title, bullets, kicker=""):
    lis="".join(f"<li>{b}</li>" for b in bullets)
    kh=f'<div class="co-kick">{esc(kicker)}</div>' if kicker else ""
    return f'<div class="callout">{kh}<h3 class="co-title">{esc(title)}</h3><ul class="co-list">{lis}</ul></div>'

def section(id_, eb_text, eb_color, title_html, lede, body):
    return (f'<section id="{id_}">'
            f'<div class="sec-head">{eyebrow(eb_text, eb_color)}<h2 class="sec-title">{title_html}</h2>'
            f'<p class="lede">{lede}</p></div>{body}</section>')


# ---------- additional components ----------
def mline(series, labels, maxv=None, hi=None):
    """series: list of (name, [values], color). hi = name to emphasise."""
    W=680; H=250; pad_l=40; pad_b=42; plot_h=H-pad_b-20; plot_w=W-pad_l-16
    if maxv is None: maxv=max(max(v) for _,v,_ in series)
    n=len(series[0][1])
    def X(i): return pad_l+(i/(n-1))*plot_w
    def Y(v): return 20+plot_h-(v/maxv)*plot_h
    rows=[]
    for g in range(0,5):
        gy=20+plot_h-(g/4)*plot_h; gval=maxv*g/4
        rows.append(f'<line x1="{pad_l}" y1="{gy:.1f}" x2="{W-16}" y2="{gy:.1f}" stroke="{LINE}"/>')
        rows.append(f'<text x="{pad_l-8}" y="{gy+4:.1f}" text-anchor="end" class="ax">{gval:,.0f}</text>')
    for name,vals,col in series:
        emph = (hi is None or name==hi)
        pts=" ".join(f"{X(i):.1f},{Y(v):.1f}" for i,v in enumerate(vals))
        sw = 3.2 if emph else 1.6
        op = 1 if emph else 0.45
        rows.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{op}" stroke-linejoin="round"/>')
        if emph:
            for i,v in enumerate(vals):
                rows.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="3.2" fill="{col}"/>')
    step=max(1,n//6)
    for i in range(0,n,step):
        rows.append(f'<text x="{X(i):.1f}" y="{H-14:.1f}" text-anchor="middle" class="ax2">{esc(labels[i])}</text>')
    leg="".join(f'<span class="il"><span class="dot" style="background:{c}"></span>{esc(nm)}</span>' for nm,_,c in series)
    return (f'<svg viewBox="0 0 {W} {H}" class="chart" role="img">{"".join(rows)}</svg>'
            f'<div class="ilegend">{leg}</div>')

def pairbars(items, unit="", fmt=None):
    """items: (label, start_value, end_value, color) — shows movement start -> end."""
    if fmt is None: fmt=lambda v:f"{v:.1f}"
    maxv=max(max(a,b) for _,a,b,_ in items) or 1
    W=680; labw=215; barw=W-labw-175; hp=42; H=len(items)*hp+10
    rows=[]
    for i,(lab,a,b,col) in enumerate(items):
        y=i*hp+8
        wa=max(2,(a/maxv)*barw); wb=max(2,(b/maxv)*barw)
        rows.append(f'<text x="{labw-10}" y="{y+21}" text-anchor="end" class="bl">{esc(lab)}</text>')
        rows.append(f'<rect x="{labw}" y="{y+2}" width="{wa:.1f}" height="13" rx="4" fill="{col}" opacity="0.32"/>')
        rows.append(f'<rect x="{labw}" y="{y+18}" width="{wb:.1f}" height="13" rx="4" fill="{col}"/>')
        arrow="▲" if b>a else ("▼" if b<a else "—")
        acol=GREEN if b>a else (RED if b<a else MUTED)
        vtxt=f'{fmt(a)}{unit} \u2192 {fmt(b)}{unit}'
        vx=min(labw+max(wa,wb)+9, W-34-len(vtxt)*7.0)
        rows.append(f'<text x="{vx:.1f}" y="{y+21}" class="bv">{esc(vtxt)}</text>')
        rows.append(f'<text x="{W-14}" y="{y+21}" text-anchor="end" class="bv" fill="{acol}">{arrow}</text>')
    return f'<svg viewBox="0 0 {W} {H}" class="chart" role="img">{"".join(rows)}</svg>'

def updatecard(tag, tagcolor, title, body):
    return (f'<div class="upd"><div class="upd-tag" style="background:{tagcolor}1f;color:{tagcolor}">{esc(tag)}</div>'
            f'<h3 class="upd-title">{esc(title)}</h3><p class="upd-body">{body}</p></div>')

def note(text):
    return f'<p class="fnote">{text}</p>'

def wowrow(label, weeks, color, fmt=None, caveat=""):
    """label, list of weekly values (oldest->newest), colour."""
    if fmt is None: fmt=lambda v:f"{v:,}"
    cur=weeks[-1]; prev=weeks[-2]
    d=(cur-prev)/prev*100 if prev else 0
    arrow="\u25b2" if d>0.05 else ("\u25bc" if d<-0.05 else "\u2014")
    acol=GREEN if d>0.05 else (RED if d<-0.05 else MUTED)
    mx=max(weeks) or 1
    bw=26; gap=7; H=44
    bars=[]
    for i,v in enumerate(weeks):
        h=max(3,(v/mx)*H); x=i*(bw+gap); y=H-h
        op = 1 if i==len(weeks)-1 else 0.3
        bars.append(f'<rect x="{x}" y="{y:.1f}" width="{bw}" height="{h:.1f}" rx="3" fill="{color}" opacity="{op}"/>')
    spark=f'<svg viewBox="0 0 {len(weeks)*(bw+gap)-gap} {H}" class="spark" role="img">{"".join(bars)}</svg>'
    cav=f'<div class="wow-cav">{caveat}</div>' if caveat else ""
    return (f'<div class="wowrow"><div class="wow-lab">{esc(label)}{cav}</div>'
            f'<div class="wow-spark">{spark}</div>'
            f'<div class="wow-cur">{esc(fmt(cur))}</div>'
            f'<div class="wow-d" style="color:{acol}">{arrow} {abs(d):.1f}%</div></div>')

def wowcard(title, sub, rows, foot=""):
    head=('<div class="wowrow wowhead"><div class="wow-lab">Metric</div><div class="wow-spark">'
          'Jul 22 &middot; Jul 29 &middot; Aug 5 &middot; Aug 12</div>'
          '<div class="wow-cur">Aug 12&ndash;18</div><div class="wow-d">WoW</div></div>')
    ft=f'<p class="fnote">{foot}</p>' if foot else ""
    return card(f'<h3 class="ctitle">{esc(title)}</h3><p class="csub">{esc(sub)}</p>{head}{"".join(rows)}{ft}')

# ================= BUILD =================
# chart_card()'s signature is (title, chart, sub). This wrapper takes the
# order the sections are written in: title, then the descriptive line, then
# the chart itself.
def cc(title, sub, chart):
    return chart_card(title, chart, sub)

# Reporting spine: Aug 12-18, 2026. 14d = Aug 5-18. 30d = Jul 20-Aug 18.
# Aug 12 also appeared in the prior report (Aug 6-12).
#
# Normalization rule: rates per 1,000 sessions are computed on EVENT COUNTS,
# never on unique-user counts. GA4 dedupes users inside each window, so a
# user/session ratio drifts downward as the window widens regardless of what
# happened. Unique-user figures appear only as absolutes on the spine window.

def pivot(rows, note_html=""):
    """rows: list of (label, v7, v14, v30, fmt) — a three-window comparison table."""
    trs = []
    for lab, v7, v14, v30, f in rows:
        trs.append(f'<tr><td class="pv-lab">{esc(lab)}</td>'
                   f'<td class="pv-v pv-spine">{f(v7)}</td>'
                   f'<td class="pv-v">{f(v14)}</td>'
                   f'<td class="pv-v">{f(v30)}</td></tr>')
    nt = f'<p class="fnote">{note_html}</p>' if note_html else ""
    return (f'<table class="pvt"><thead><tr><th></th>'
            f'<th class="pv-spine-h">7 days<span>Aug 12&ndash;18</span></th>'
            f'<th>14 days<span>Aug 5&ndash;18</span></th>'
            f'<th>30 days<span>Jul 20&ndash;Aug 18</span></th></tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table>{nt}')

I = lambda v: f"{v:,}"
F1 = lambda v: f"{v:,.1f}"
F2 = lambda v: f"{v:,.2f}"

day_labels = ["Aug 12","Aug 13","Aug 14","Aug 15","Aug 16","Aug 17","Aug 18"]
plat_days  = [958, 946, 706, 284, 314, 3151, 1062]

# ============ HERO ============
hero_tiles = tiles([
    ("34","Pros accepted offers",TEAL,"GA4 tag event \u00b7 unique users"),
    ("23","Shifts filled on promo",GREEN,"10 worked, $500 issued"),
    ("97","Darby widget viewers",PURPLE,"14.4% used a filter"),
    ("4,166","Marketing site views",BLUE,"from 3,559 \u00b7 +17.1%"),
    ("18","Google reviews",YELLOW,"4.6\u2605 \u00b7 from 16 at 4.3"),
    ("366","LinkedIn clicks",PINK,"from 1 post published"),
])

# ============ SECTION W: WEEK OVER WEEK ============
wow_rows = [
    wowrow("Platform active users",[7869,7616,7118,7421],TEAL,
           caveat="Daily actives summed. A pro active on three days counts three times."),
    wowrow("Marketing site views",[3369,3169,3461,3980],BLUE,
           caveat="From the daily top-page export, which runs about 3% under the property total of 4,166 for the same "
                  "week. Same basis in all four buckets, so the trend holds."),
    wowrow("Paid search impressions",[740,724,739,728],ORANGE,
           caveat="Brand campaign only. Google reports Jul 21\u2013Aug 19. The last bucket is Aug 12\u201318."),
    wowrow("Short.io clicks",[294,36,59,42],GREEN,
           caveat="Human clicks, rebuilt from the daily series. The first bucket is the Jul 24 ADA send."),
]
s_wow = section("wow","Momentum",NAVY,
    'Week over <span class="hl" style="background:'+NAVY+'22">week</span>',
    "Four trailing weeks for the metrics with daily series. Lighter bars are prior weeks. The solid bar is Aug 12\u201318.",
    wowcard("Trailing four weeks","Weeks beginning Jul 22, Jul 29, Aug 5 and Aug 12.",wow_rows,
        foot="Site views up a third week running, 18.1% above late July. Platform actives up 4.3% after two down weeks. "
             "Paid impressions flat all month, inside a 16-impression band.<br><br>"
             "<b>Short.io needs its context.</b> The 294 in the first bucket is one ADA email on Jul 24. Without it, weekly "
             "clicks ran between 36 and 59.<br><br>"
             "<b>Not shown:</b> AI visibility is measured weekly and ends Aug 9 on complete data. Social, campaign and review "
             "numbers are period totals and sit in their own sections."))

def widemodule(tag, tagcolor, title, lead_html, chart, foot_html=""):
    """A full-width card: tag, title, short lead, chart, optional footnote.
    Used where a diagram and its commentary belong to the same item."""
    ft = f'<p class="fnote">{foot_html}</p>' if foot_html else ""
    return card(f'<div class="upd-tag" style="background:{tagcolor}1f;color:{tagcolor}">{esc(tag)}</div>'
                f'<h3 class="wm-title">{esc(title)}</h3>'
                f'<p class="wm-lead">{lead_html}</p>{chart}{ft}', klass="widemod")


def reviewflow():
    """Google review request automation, drawn as a left-to-right flow with a
    stop branch and a funnel band underneath. Self-contained SVG."""
    W, BW, GAP = 680, 128, 40
    xs = [20 + i * (BW + GAP) for i in range(4)]
    steps = [("Chat or ticket", "closes", "#FFFFFF", INK, LINE),
             ("Satisfaction", "survey sent", "#FFFFFF", INK, LINE),
             ("Happy", "response", TEAL, "#FFFFFF", TEAL),
             ("Google review", "request email", NAVY, "#FFFFFF", NAVY)]
    o = ['<defs><marker id="ah" markerWidth="7" markerHeight="7" refX="6" refY="3.5" '
         f'orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="{MUTED}"/></marker></defs>']

    for x, (l1, l2, fill, fg, stroke) in zip(xs, steps):
        cx = x + BW / 2
        o.append(f'<rect x="{x}" y="20" width="{BW}" height="64" rx="10" fill="{fill}" stroke="{stroke}"/>')
        o.append(f'<text x="{cx}" y="46" text-anchor="middle" font-size="12.5" font-weight="700" fill="{fg}">{esc(l1)}</text>')
        o.append(f'<text x="{cx}" y="63" text-anchor="middle" font-size="12.5" font-weight="700" fill="{fg}">{esc(l2)}</text>')

    for i in range(3):
        o.append(f'<line x1="{xs[i]+BW+6}" y1="52" x2="{xs[i+1]-9}" y2="52" '
                 f'stroke="{MUTED}" stroke-width="1.6" marker-end="url(#ah)"/>')
    mid = xs[2] + BW + GAP / 2
    o.append(f'<text x="{mid}" y="42" text-anchor="middle" font-size="10" fill="{MUTED}">1 day</text>')

    # stop branch off the happy step
    bx, by = xs[2] - 16, 116
    o.append(f'<line x1="{xs[2]+BW/2}" y1="84" x2="{xs[2]+BW/2}" y2="{by}" stroke="{LINE}" stroke-width="1.6" stroke-dasharray="4 4"/>')
    o.append(f'<rect x="{bx}" y="{by}" width="160" height="34" rx="8" fill="none" stroke="{LINE}" stroke-dasharray="4 4"/>')
    o.append(f'<text x="{bx+80}" y="{by+22}" text-anchor="middle" font-size="11" fill="{MUTED}">Unhappy or neutral \u2014 no ask</text>')

    # funnel band
    band_y, band_h = 174, 70
    o.append(f'<rect x="20" y="{band_y}" width="{W-40}" height="{band_h}" rx="12" fill="{CREAM}" stroke="{LINE}"/>')
    stats = [("46", "requests sent"), ("14", "opened"), ("5", "clicked through"),
             ("9", "new reviews"), ("3.7 \u2192 4.6", "rating")]
    seg = (W - 40) / len(stats)
    for i, (num, lab) in enumerate(stats):
        cx = 20 + seg * (i + 0.5)
        o.append(f'<text x="{cx:.1f}" y="{band_y+34}" text-anchor="middle" font-size="{19 if len(num) > 4 else 22}" font-weight="700" fill="{NAVY}" font-family="Georgia,serif">{esc(num)}</text>')
        o.append(f'<text x="{cx:.1f}" y="{band_y+54}" text-anchor="middle" font-size="10.5" fill="{MUTED}">{esc(lab)}</text>')
        if i < len(stats) - 1:
            dx = 20 + seg * (i + 1)
            o.append(f'<line x1="{dx:.1f}" y1="{band_y+14}" x2="{dx:.1f}" y2="{band_y+band_h-14}" stroke="{LINE}"/>')

    return f'<svg viewBox="0 0 {W} 256" class="chart" role="img">{"".join(o)}</svg>'

# ============ SECTION 0: UPDATES ============
u1 = updatecard("Live",GREEN,"Partner widget on the Darby site",
    "The Pro Availability widget is live on darbydental.com. First traffic <b>Aug 14</b>. Guests see it about three-quarters "
    "down the homepage so the \u201cWhy Darby\u201d content stays up top. Signed-in customers see it under the hero ad. "
    "Built by Logan and Darya. <b>97 Darby-referred users</b> viewed it this week.")
u2 = updatecard("Converting",GREEN,"August $50 gift-card promo",
    "Codes have produced <b>23 filled shifts</b>, 14 RDH and 9 DA. Ten worked and approved. <b>$500 in gift cards issued "
    "Aug 14</b>. Starbucks and DoorDash carried the volume. The Amazon code has not been used once. Runs to Aug 31.")
u3 = updatecard("Shipped",BLUE,"Schema on the core pages",
    "Structured data added to the home, professionals and practices pages. This is what search engines and AI assistants read "
    "to work out what onDiem is and who it serves. It sits alongside last period's sitemap indexing fix, which shows up in "
    "the website section.")
s0 = section("updates","What shipped",NAVY,
    'Updates <span class="hl" style="background:'+NAVY+'22">this period</span>',
    "Four items. The widget and the promo both produced outcomes we can count.",
    '<div class="updgrid">'+u1+u2+u3+'</div>'
    + widemodule("Working",YELLOW,"Google review automation",
        "<b>18 reviews at 4.6\u2605</b>, up from 16 at 4.3 last period and 9 at 3.7 in early July. This is an automated ask, "
        "not organic drift. Built by Angie Trogstad with Dee Lopez, it now runs on closed email tickets as well as live chat. "
        "Before it, onDiem had not had a review in about a year.",
        reviewflow(),
        "Counts are the first batch, sent Jul 2\u201327. Nine reviews came in over the same stretch, more than the 5 recorded "
        "click-throughs, so the email-ticket version of the ask is likely contributing volume we are not measuring separately. "
        "No bounces, no unsubscribes, no spam reports across the 46 sends. Review totals captured Aug 20, so they are current "
        "state rather than a windowed number."))

# ============ SECTION 1: CAMPAIGNS ============
s1_tiles = tiles([
    ("23","Shifts filled",GREEN,"14 RDH \u00b7 9 DA"),
    ("10","Worked and approved",TEAL,"$500 issued Aug 14"),
    ("44","Listings created",BLUE,"on promo codes"),
    ("89%","Portland metro",ORANGE,"39 of 44 listings"),
])

s1_codes = table(
    ["Promo code","Times used","Filled","Notes"],
    [["#EARN50STARBUCKS","15","10","9 RDH, 1 DA \u00b7 3 active applicants, 2 cancelled"],
     ["#EARN50DOORDASH","5","5","1 RDH, 4 DA"],
     ["#EARN50TARGET","\u2014","8","Target and DoorDash split the remainder"],
     ["#EARN50AMAZON","0","0","Never used"]],
    aligns=["left","right","right","left"])

s1_practices = hbars([
    ("Timber Dental \u2013 Bethany (Portland, OR)",14,GREEN),
    ("Bronitsky Family Dentistry (Aloha, OR)",7,GREEN),
    ("Brio Dental (Portland, OR)",6,GREEN),
    ("King City Dental (King City, OR)",4,TEAL),
    ("Timeless Family Dental (Portland, OR)",3,TEAL),
    ("Hunter Dental Care (Portland, OR)",3,TEAL),
    ("4M Dental Implant (Newport Beach, CA)",3,MUTED),
    ("ComfortCare Dental (Milwaukie, OR)",2,TEAL),
    ("Washington Square Dental (White Bear Lake, MN)",2,MUTED),
], unit=" listings", labw=330, valw=92)

s1_sends = hbars([
    ("Portland, OR",272,GREEN),
    ("Minneapolis, MN",169,MUTED),
    ("Chicago, IL",152,MUTED),
    ("All six cities",138,MUTED),
    ("Atlanta, GA",64,MUTED),
    ("Houston, TX",40,MUTED),
    ("Miami, FL",16,MUTED),
], unit=" practices")

s1_mailer = pairbars([
    ("Spring mailer \u2014 booked shifts",15,48,GREEN),
], fmt=lambda v:f"{v:.0f}")

s1 = section("campaigns","Campaigns",GREEN,
    'The promo <span class="hl" style="background:'+GREEN+'33">converted</span>',
    "The August gift-card campaign converted. Almost all of it is Portland.",
    s1_tiles
    + cc("Redemption by promo code","Four codes, one offer. Redemption is the metric, not clicks.",s1_codes)
    + '<div class="grid2">'
    + cc("Listings created, by practice","All 9 practices. Portland metro in green and teal, the two outside Oregon in gray.",s1_practices)
    + cc("Who the campaign was sent to","851 practices across six cities plus an all-cities list.",s1_sends)
    + '</div>'
    + cc("Spring mailer, final reconciliation",
        "Reported at 15 last period while timecards were still clearing. Final count is 69 codes redeemed and 48 booked "
        "shifts across Portland and Minneapolis. Reconciliation, not new activity.",s1_mailer)
    )

# ============ SECTION 2: MARKETPLACE ============
s2_tiles = tiles([
    ("34","Pros accepted offers",TEAL,"GA4 event \u00b7 46 fires"),
    ("9,332","Sessions",BLUE,"app.ondiem.com"),
    ("4.93","Acceptances per 1k sessions",PINK,"30-day rate 5.98"),
    ("37.0%","Mobile share",PURPLE,"30-day share 29.2%"),
])

s2_pivot = pivot([
    ("Sessions", 9332, 18589, 44630, I),
    ("Shift views per 1,000 sessions", 454.67, 421.97, 378.74, F1),
    ("Job searches per 1,000 sessions", 262.43, 257.95, 221.98, F1),
    ("Listings created per 1,000 sessions", 59.26, 68.91, 62.25, F1),
    ("Offers accepted per 1,000 sessions", 4.93, 5.49, 5.98, F2),
], note_html="Rates are event counts per 1,000 sessions. Unique-user counts do not compare across windows: GA4 dedupes "
             "users inside each window, so a user-based rate falls as the window widens whatever the activity does.")

s2_daily = area(plat_days, day_labels, color=TEAL, hi_idx=[5])

s2_funnel = funnel([
    ("Sessions","9,332",BLUE),
    ("Viewed a shift","2,182 users",TEAL),
    ("Initiated a job search","936 users",GREEN),
    ("Accepted an offer","34 users",PINK),
])

s2 = section("marketplace","Marketplace \u00b7 app.ondiem.com",TEAL,
    'Browsing up, <span class="hl" style="background:'+TEAL+'33">converting flat</span>',
    "More shift viewing and searching per session than the 30-day baseline. Slightly fewer acceptances per session.",
    s2_tiles
    + cc("The three windows, normalized","Rates per 1,000 sessions. The 7-day column is the reporting spine.",s2_pivot)
    + '<div class="grid2">'
    + cc("Daily active users","Aug 17 is 3,151 of the week's 7,421.",s2_daily)
    + cc("Where the week narrows","Unique users at each step, Aug 12\u201318.",s2_funnel)
    + '</div>'
    + note("<b>Shift views ran 20% above the 30-day rate, job searches 18% above.</b> Acceptances per session sat 18% below "
           "it, and listings per session below both the 14-day and 30-day rates. More people looked. About the same number "
           "committed.<br><br>"
           "<b>Aug 17 is 42% of the week's active users.</b> Mondays run high all month \u2014 3,151, 2,956, 3,722, 3,877 "
           "\u2014 but this one is the largest. Any week-level average is carrying it.<br><br>"
           "<b>Mobile is 37.0% of active users</b> against 29.2% across thirty days. The window bias runs the other way, so "
           "the shift is real.<br><br>"
           "<b>Everything here is a GA4 tag event</b>, not a platform database record. "
           "<code>professional_accepted_offer</code> fired 46 times from 34 users this week. Where a tag fails to fire the "
           "action still happened, so these are a floor, not an exact count.<br><br>"
           "<code>temp_shift_offered</code> is out of every rate: 27,875 events from 12 users this week. It is an activity "
           "counter dominated by a few accounts, not a booking count."))

# ============ SECTION 3: MARKETING SITE ============
s3_tiles = tiles([
    ("4,166","Views",BLUE,"ondiem.com \u00b7 Aug 12\u201318"),
    ("2,158","From organic search",GREEN,"51.8% of views"),
    ("253","/practices views",TEAL,"from 121 \u00b7 +109%"),
    ("123","/shifts views",PURPLE,"from 46 \u00b7 +167%"),
])

s3_pages = hbars([
    ("/",2538,BLUE),("/professionals",791,TEAL),("/practices",253,GREEN),
    ("/shifts",123,GREEN),("/contact-us",98,MUTED),("/ondiem-darby",81,PURPLE),
    ("/dso-shifts/sonrava-health",46,MUTED),("/partners/cdha",37,MUTED),
], unit=" views")

s3_channels = donut([
    ("Organic Search",2158,GREEN),("Direct",1670,BLUE),("Referral",264,TEAL),
    ("Paid Search",42,ORANGE),("AI Assistant",14,PURPLE),("Organic Social",13,PINK),
], center_num="4,166", center_lab="views")

s3_widget = table(
    ["Widget event","Darby-referred","All sources","Darby rate","All-source rate"],
    [["Saw the widget","97 users","839 users","\u2014","\u2014"],
     ["Used a filter","14","66","14.4%","7.9%"],
     ["Navigated between weeks","6","30","6.2%","3.6%"],
     ["Opened \u2018show more\u2019","8","17","8.2%","2.0%"]],
    aligns=["left","right","right","right","right"], hi_cols=[3])

s3 = section("website","Marketing site \u00b7 ondiem.com",BLUE,
    'The indexing fix <span class="hl" style="background:'+BLUE+'33">landed</span>',
    "Site views up a third week running. The two pages behind the sitemap fix more than doubled.",
    s3_tiles
    + '<div class="grid2">'
    + cc("Top pages","Aug 12\u201318.",s3_pages)
    + cc("How people arrive","First user channel group.",s3_channels)
    + '</div>'
    + cc("Partner widget: Darby-referred against the whole property",
        "Darby-referred users against all traffic on the property as a control. Rates are of those who saw the widget.",
        s3_widget)
    + note("<b>/practices went 121 to 253 and /shifts 46 to 123</b> after the Webflow sitemap indexing toggle was switched "
           "on last period. Organic search is now 51.8% of site views.<br><br>"
           "<b>Darby-referred visitors use the widget at about double the overall rate</b> \u2014 14.4% filter against 7.9%. "
           "Over thirty days it is 18.5% against 7.0%. Volume from Darby is small, but those visitors use the tool more. "
           "Placement is likely part of it: signed-in Darby customers see the widget under the hero.<br><br>"
           "<b>The \u2018show more\u2019 counts are not reliable yet.</b> Across the property 68 users closed the modal and 17 "
           "opened it, and 61 of the 68 closes are Darby-referred against 8 opens. The close event fires where nothing was "
           "opened. Filter and week navigation are the measures to use until that is fixed."))

# ============ SECTION 4: PAID SEARCH ============
s4_tiles = tiles([
    ("$1,536","Spend",ORANGE,"Jul 21 \u2013 Aug 19"),
    ("1,709","Clicks",BLUE,"$0.90 average CPC"),
    ("51.98%","Click-through rate",TEAL,"brand terms only"),
    ("0","Recorded conversions",RED,"no signup event exists"),
])

s4_landing = hbars([
    ("hub.ondiem.com",1591,ORANGE),
    ("ondiem.com",29,MUTED),
    ("ondiem.com/professionals",26,MUTED),
    ("ondiem.com/practices",1,MUTED),
    ("ondiem.com/ada",1,MUTED),
], unit=" clicks")

s4_auction = table(
    ["Advertiser","Impression share","Overlap rate","Position above rate"],
    [["onDiem","64.38%","\u2014","\u2014"],
     ["teero.com","40.81%","42.23%","23.62%"],
     ["clouddentistry.com","31.43%","31.20%","19.23%"],
     ["gotu.com","18.21%","19.87%","18.04%"],
     ["dentalmatch.ai","< 10%","7.91%","8.87%"],
     ["directdental.com","< 10%","6.70%","15.12%"]],
    aligns=["left","right","right","right"])

s4 = section("paid","Paid search",ORANGE,
    'One campaign, <span class="hl" style="background:'+ORANGE+'33">brand only</span>',
    "One enabled campaign, defending the onDiem name. It runs last here because the conversion tracking behind it is "
    "still being built, so the numbers describe traffic rather than outcome.",
    s4_tiles
    + cc("Where the spend lands","Clicks by landing page. 93% of clicks and 90% of spend reach one destination.",s4_landing)
    + cc("Who else bids on the onDiem name","Auction insights, Jul 21 \u2013 Aug 19.",s4_auction)
    + note("<b>The 52% click-through rate is about what people are searching, not campaign strength.</b> Every term is "
           "navigational \u2014 <code>ondiem</code>, <code>odiem</code>, <code>onediem</code>, <code>ondium</code> \u2014 and "
           "two of them, <code>ondiem customer service number</code> and <code>ondiem phone number</code>, are existing users "
           "looking for support.<br><br>"
           "<b>Conversions read zero because no signup event exists on the site.</b> The registration and login pages also "
           "fire events before the Google tag loads. Both are known defects with engineering owners, so the zero is a "
           "measurement gap, not a result. Do not read it as campaign performance until the signup event ships.<br><br>"
           "<b>Three competitors bid on the onDiem name.</b> Teero shows up alongside onDiem in 42.23% of these auctions.<br><br>"
           "Google reports this account on Jul 21 \u2013 Aug 19 and only impressions come daily, so cost and clicks cannot be "
           "cut to the reporting spine."))

# ============ SECTION 5: AI VISIBILITY ============
aeo_weeks = ["Jul 19","Jul 26","Aug 2","Aug 9"]
s5_tiles = tiles([
    ("14%","Share of voice",PURPLE,"4th of 8 \u00b7 Jul 20\u2013Aug 18"),
    ("6.6%","onDiem citation rate",GREEN,"from 6.0 \u00b7 3rd of 8"),
    ("496","Owned citations",TEAL,"across 18 pages"),
    ("8.8%","Brand mention rate",RED,"GoTu 24.1%"),
])

s5_compet = mline([
    ("GoTu",[59.0,51.4,50.5,48.6],ORANGE),
    ("Cloud Dentistry",[46.7,46.7,48.6,45.7],BLUE),
    ("Kwikly",[47.6,41.9,43.3,42.4],TEAL),
    ("onDiem",[41.0,31.4,38.1,27.6],PINK),
    ("Toothio",[39.0,34.3,32.4,31.9],MUTED),
], aeo_weeks, maxv=60, hi="onDiem")

s5_engines = mline([
    ("Gemini",[60.0,45.7,50.0,38.6],BLUE),
    ("ChatGPT",[32.9,28.6,34.3,32.9],GREEN),
    ("Perplexity",[30.0,20.0,30.0,11.4],RED),
], aeo_weeks, maxv=65, hi="Perplexity")

s5_owned = pairbars([
    ("gotu.com",8.2,13.2,ORANGE),
    ("clouddentistry.com",4.9,7.6,BLUE),
    ("onDiem.com",6.0,6.6,PINK),
    ("toothio.com",4.5,4.6,MUTED),
    ("joinkwikly.com",4.9,2.9,TEAL),
], unit="%")

s5_pages = hbars([
    ("ondiem.com (homepage)",222,PINK),
    ("hub.ondiem.com/ondiem-darby",41,PURPLE),
    ("hub.ondiem.com",32,PURPLE),
    ("ondiem.com/ada",32,TEAL),
    ("hub.ondiem.com/ba_practice",22,PURPLE),
    ("hub.ondiem.com/hire-a-professional",19,PURPLE),
    ("ondiem.com/ondiem-darby",17,TEAL),
    ("hub.ondiem.com/care-benefits-adha",16,PURPLE),
], unit=" citations", labw=260)

s5_gloss = table(
    ["Term","What it measures"],
    [["Visibility","Share of the tracked prompts where an AI engine names the brand in its answer. onDiem tracks 10 prompts across ChatGPT, Gemini and Perplexity."],
     ["Share of voice","Of every mention of a dental staffing brand across those answers, the share that is onDiem."],
     ["onDiem citation rate","How often ondiem.com is the source an answer links to, as a share of all sources cited."],
     ["Owned citations","The number of times a page onDiem controls \u2014 ondiem.com, hub.ondiem.com, help.ondiem.com \u2014 was cited as a source."],
     ["Brand mention rate","Of the pages cited in these answers, the share that name onDiem anywhere on the page. A page can be cited without mentioning the brand."]],
    aligns=["left","left"])

s5 = section("aeo","AI visibility",PURPLE,
    'The decline <span class="hl" style="background:'+PURPLE+'33">slowed</span>',
    "Four complete weeks of prompt testing across ChatGPT, Gemini and Perplexity. onDiem ends the period lower than it started, but is no longer alone in that.",
    s5_tiles
    + cc("What these terms mean","AI visibility is new to this report. Definitions first.",s5_gloss)
    + '<div class="grid2">'
    + cc("Visibility against competitors","Share of tracked prompts returning each brand.",s5_compet)
    + cc("By AI engine","onDiem's visibility in each engine.",s5_engines)
    + '</div>'
    + cc("Owned domain citation rate","How often each brand's own site is cited. Faded bar is Jul 20, solid is Aug 10.",s5_owned)
    + cc("Which onDiem pages get cited","496 citations across 18 owned pages, Jul 23 \u2013 Aug 20.",s5_pages)
    + note("<b>onDiem fell 13.4 points over the four weeks. GoTu fell 10.4.</b> Toothio and Kwikly also declined and Cloud "
           "Dentistry was flat, so the pattern from earlier periods \u2014 onDiem the only brand losing ground \u2014 no longer "
           "holds.<br><br>"
           "<b>Perplexity is the engine that moved.</b> 30.0 to 11.4 over four weeks while ChatGPT held flat at 32.9. One "
           "engine is dropping onDiem specifically.<br><br>"
           "<b>The owned citation rate is the one moving the right way.</b> onDiem's own domain went 6.0 to 6.6 and sits third "
           "of eight. Brand mention rate did not move: 8.8% against GoTu at 24.1%.<br><br>"
           "<b>hub.ondiem.com is 30.4% of onDiem's AI citations</b> \u2014 151 across 15 pages, behind the homepage at 44.8%. "
           "The Darby hub page is the second strongest asset after the homepage. The paid search plan retires hub behind a "
           "redirect. Preserving those URLs matters here as much as it does in search.<br><br>"
           "A fifth week beginning Aug 16 reads 44.0 for onDiem, but on under a third of the usual sample, so it is excluded. "
           "It becomes a complete data point next period."))

# ============ SECTION 6: SOCIAL ============
s6_tiles = tiles([
    ("366","LinkedIn clicks",PINK,"from 1 post published"),
    ("3","Posts published",MUTED,"one per platform, all Aug 13"),
    ("0","Net new followers",RED,"IG and LinkedIn"),
    ("0.99","Instagram engagement",TEAL,"30d \u00b7 top of tracked set"),
])

s6_li = pivot([
    ("Posts published", 1, 4, 7, I),
    ("Clicks on all content viewed", 366, 629, 674, I),
    ("Impressions on all content viewed", 908, 1471, 2127, I),
    ("Impressions from posts published", 113, 1119, 1867, I),
], note_html="\u201cContent viewed\u201d counts every post earning attention in the window, whenever it was published. "
             "\u201cPosts published\u201d counts only posts created inside the window.")

s6_ig = pivot([
    ("Posts published", 1, 4, 7, I),
    ("Views on posts published", 84, 3401, 10900, I),
    ("Interactions", 1, 10, 58, I),
    ("Engagement rate", 2.17, 0.37, 0.99, F2),
])

s6_compet = table(
    ["Instagram account","Followers","Posts","Reels","Engagement"],
    [["Princess Dental Staffing","10,439","2","37","0.23"],
     ["Teero","3,609","7","\u2014","0.11"],
     ["onDiem","3,107","7","0","0.99"],
     ["Kwikly Dental Staffing","2,470","3","1","0.53"]],
    aligns=["left","right","right","right","right"], hi_cols=[4])

s6_stories = table(
    ["Instagram story","Impressions","Reach","Forward taps","Exits"],
    [["Aug 17","44","43","25","8"],
     ["Aug 18","41","41","23","3"],
     ["Aug 13 feed post (comparison)","\u2014","46","\u2014","\u2014"]],
    aligns=["left","right","right","right","right"])

s6 = section("social","Social",PINK,
    'Format, not <span class="hl" style="background:'+PINK+'33">frequency</span>',
    "One post published per platform this week and 366 LinkedIn clicks recorded. Almost all of them came from documents published the week before.",
    cc("LinkedIn: published against viewed","Two different things, and the gap between them is the point.",s6_li)
    + cc("Instagram","Views, interactions and engagement across the three windows.",s6_ig)
    + '<div class="grid2">'
    + cc("Instagram against competitors","30-day window. onDiem is top of the tracked set on engagement.",s6_compet)
    + cc("Stories outperformed the feed","Instagram stories resumed Aug 17\u201318.",s6_stories)
    + '</div>'
    + note("<b>One LinkedIn post published this week earned 113 impressions and 2 clicks. The account recorded 366 clicks.</b> "
           "The other 364 came from documents published Aug 7\u201311, still working. Those documents earned more in their "
           "second week (366) than their first (263). Document posts keep going for a fortnight. The image post did nothing on "
           "the day it ran.<br><br>"
           "<b>Followers did not move.</b> Instagram 3,107 and LinkedIn 2,171, both flat. Facebook 3,603, one gained and none "
           "lost. Instagram is \u22123 across fourteen days. Reach fell with publishing volume, from 10.9K views over thirty "
           "days to 84 on the single post this week.<br><br>"
           "<b>Instagram is top of the tracked set on engagement</b> at 0.99 against Princess at 0.23, Kwikly 0.53 and Teero "
           "0.11, on a third of Princess's audience. Princess published 37 reels in thirty days. onDiem published none.<br><br>"
           "<b>Feed publishing stopped after Aug 13. Stories did not.</b> Two Instagram stories on Aug 17\u201318 reached 43 "
           "and 41 against the Aug 13 feed post's 46, with 25 and 23 forward taps.<br><br>"
           "<b>No LinkedIn referral sessions show up in either GA4 property</b> despite 366 recorded clicks. The audience is "
           "also technology and engineering by industry, at 10,000+ employee companies. Not the dental practices the content "
           "is written for."))

# ============ SECTION 7: LINK TRACKING ============
s7_tiles = tiles([
    ("42","Human clicks",GREEN,"Aug 12\u201318"),
    ("445","Human clicks",TEAL,"Jul 21\u2013Aug 18"),
    ("294","Top path: /ada-email",BLUE,"66% of 30-day clicks"),
    ("8","Paths tracked",MUTED,"across the ondiem.io domain"),
])

s7_paths = hbars([
    ("/ada-email",294,GREEN),("/* (catch-all)",68,MUTED),("/ada-website",43,TEAL),
    ("/ (root)",35,MUTED),("/onDiem-youtube",11,MUTED),("/website",6,MUTED),
    ("/ada-member-advantage",5,MUTED),("/darby-ondiem-ada",1,PINK),
], unit=" clicks")

s7 = section("links","Link tracking",GREEN,
    'Where the <span class="hl" style="background:'+GREEN+'33">clicks land</span>',
    "Human clicks only. Automated traffic is filtered out before anything here is counted.",
    s7_tiles
    + cc("Clicks by path","Human clicks, Jul 21 \u2013 Aug 18.",s7_paths)
    + note("<b>/ada-email is 294 of 445 clicks, and 257 of those landed on Jul 24.</b> One ADA send three weeks before this "
           "period accounts for most of the thirty-day total. It falls outside both the 7-day and 14-day windows, which is "
           "why the weekly number reads 42.<br><br>"
           "<b>The Darby short link recorded one click in thirty days.</b> Widget traffic comes through the embed, not the "
           "short link, so this is not the measurement path for the partnership.<br><br>"
           "Short.io exports on windows anchored to the export moment rather than fixed dates. These figures were rebuilt "
           "from the daily series to match the spine. The series starts Jul 21, so the 30-day figure is missing Jul 20."))

# ============ TAKEAWAYS ============
take = callout("Wins, and what is on deck",[
    "<b>The promo converted.</b> 23 filled shifts, 10 worked and approved, $500 issued. Redemption is the number that "
    "matters here, not opens or clicks, and it is the number to run this campaign on.",

    "<b>The Darby widget is live and being used.</b> 97 Darby-referred users in its first week, filtering at 14.4% against "
    "7.9% for everyone else on the property. Over thirty days that gap is 18.5% against 7.0%.",

    "<b>The review automation is running on its own.</b> Nine reviews and nearly a full star since early July, off a "
    "workflow nobody has to remember to run. It is the only third-party signal in this report moving up, and it counts for "
    "AI answers as much as for search.",

    "<b>The indexing fix landed.</b> /practices went 121 to 253 and /shifts 46 to 123. Organic search is now 51.8% of site "
    "views and the site has risen three weeks running.",

    "<b>Discovery steadied.</b> onDiem's four-week decline is now matched by three of five tracked competitors, and the "
    "owned citation rate rose from 6.0 to 6.6. Schema on the core pages should show up here next.",

    "<b>On deck: the signup event.</b> Once it ships, paid search can record a conversion for the first time and the $1,536 "
    "becomes measurable. The widget's \u2018show more\u2019 events need the same treatment before we can report modal "
    "engagement.",

    "<b>Also on deck:</b> the promo runs to Aug 31 with a second reminder still to go, and the partial AI visibility week "
    "beginning Aug 16 becomes a complete data point next period.",
], kicker="Aug 12\u201318, 2026")

# ============ ASSEMBLE ============
nav=('<nav class="toc"><a href="#updates">Updates</a><a href="#wow">Week over week</a><a href="#campaigns">Campaigns</a><a href="#marketplace">Marketplace</a><a href="#website">Website</a>'
     '<a href="#aeo">AI visibility</a><a href="#social">Social</a>'
     '<a href="#links">Links</a><a href="#paid">Paid</a></nav>')

header=(f'<header class="masthead"><div class="mh-top"><span class="brand">'
        f'<span class="brand-mark">&#9681;</span> onDiem</span><span class="period">AUG 12 &ndash; 18, 2026</span></div>'
        f'<h1 class="title">Marketing Performance <span class="hl" style="background:{TEAL}44">Report</span></h1>'
        f'<p class="subtitle">Aug 12&ndash;18, 2026, with 14-day and 30-day views alongside. Aug 12 also appeared in the prior report. Paid search and AI visibility run on their own ranges, labeled in each section. Prepared by Figment Creative.</p>'
        f'{nav}</header>')

body=(header+s0+
      f'<section class="hero"><div class="sec-head">{eyebrow("At a glance", NAVY)}'
      f'<h2 class="sec-title">The period in six numbers</h2></div>{hero_tiles}</section>'+
      s_wow+s1+s2+s3+s5+s6+s7+s4+
      f'<section>{take}</section>'+
      f'<footer class="foot">onDiem Marketing Performance Report &middot; Spine window Aug 12 &ndash; 18, 2026 &middot; 14-day Aug 5 &ndash; 18 &middot; 30-day Jul 20 &ndash; Aug 18 &middot; Paid search Jul 21 &ndash; Aug 19 &middot; AI visibility four complete weeks to Aug 9 &middot; Owned citations Jul 23 &ndash; Aug 20 &middot; Google reviews captured Aug 20 &middot; Profile completion not reported this period &middot; Sources: GA4, Metricool, Google Ads, Short.io, HubSpot &middot; Internal use</footer>')

CSS=f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:{CREAM};color:{INK};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1120px;margin:0 auto;padding:40px 26px 80px}}
h1,h2,h3,.t-num,.dnum{{font-family:Georgia,'Times New Roman',serif}}
.masthead{{margin-bottom:34px}}
.mh-top{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:22px}}
.brand{{font-family:Georgia,serif;font-size:22px;font-weight:700;color:{NAVY};letter-spacing:.5px}}
.brand-mark{{color:{TEAL}}}
.period{{font-size:11px;font-weight:700;letter-spacing:1.5px;color:{MUTED}}}
.title{{font-size:44px;line-height:1.08;color:{NAVY};font-weight:700;letter-spacing:-.5px}}
.hl{{border-radius:6px;padding:0 10px}}
.subtitle{{margin-top:14px;color:{MUTED};font-size:15px;max-width:760px}}
.toc{{display:flex;flex-wrap:wrap;gap:8px;margin-top:24px;border-top:1px solid {LINE};padding-top:20px}}
.toc a{{font-size:12px;font-weight:600;color:{NAVY};text-decoration:none;background:#fff;border:1px solid {LINE};padding:6px 13px;border-radius:20px}}
.toc a:hover{{background:{NAVY};color:#fff}}
section{{margin-top:52px}}
.sec-head{{margin-bottom:20px}}
.eyebrow{{display:inline-block;font-size:11px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;padding:4px 11px;border-radius:5px;margin-bottom:12px}}
.sec-title{{font-size:30px;color:{NAVY};font-weight:700;letter-spacing:-.3px}}
.lede{{margin-top:9px;color:{MUTED};font-size:15px;max-width:820px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-bottom:18px}}
.tile{{background:#fff;border:1px solid {LINE};border-radius:13px;padding:16px 16px 15px}}
.t-num{{font-size:30px;font-weight:700;color:{NAVY};line-height:1.05}}
.t-lab{{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:{INK};margin-top:6px}}
.t-sub{{font-size:11.5px;color:{MUTED};margin-top:3px}}
.card{{background:#fff;border:1px solid {LINE};border-radius:15px;padding:20px 22px;margin-bottom:16px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.ctitle{{font-size:17px;color:{NAVY};font-weight:700;margin-bottom:3px}}
.csub,.lede{{font-size:13.5px}}
.csub{{color:{MUTED};margin-bottom:12px}}
.chart{{width:100%;height:auto;display:block;margin-top:6px}}
.bl{{font-size:12.5px;fill:{INK};font-weight:500}}
.bv{{font-size:12.5px;fill:{NAVY};font-weight:700}}
.ax{{font-size:11px;fill:{MUTED}}}
.ax2{{font-size:11px;fill:{MUTED}}}
.donutwrap{{display:flex;gap:18px;align-items:center;flex-wrap:wrap}}
.donut{{width:190px;height:190px;flex:0 0 auto}}
.dnum{{font-size:30px;font-weight:700;fill:{NAVY}}}
.dlab{{font-size:11px;fill:{MUTED};text-transform:uppercase;letter-spacing:.5px}}
.legend{{flex:1;min-width:180px}}
.lg{{display:flex;align-items:center;gap:8px;padding:4px 0;font-size:13px}}
.dot{{width:11px;height:11px;border-radius:3px;flex:0 0 auto}}
.lgl{{flex:1;color:{INK}}}
.lgv{{color:{MUTED};font-weight:600;font-size:12.5px}}
.ilegend{{display:flex;gap:16px;flex-wrap:wrap;margin-top:10px}}
.il{{display:flex;align-items:center;gap:6px;font-size:12.5px;color:{MUTED}}}
.tbl{{width:100%;border-collapse:collapse;margin-top:6px;font-size:13px}}
.tbl th{{background:{NAVY};color:#fff;padding:9px 11px;font-size:11px;text-transform:uppercase;letter-spacing:.5px;font-weight:700}}
.tbl th:first-child{{border-radius:7px 0 0 0}} .tbl th:last-child{{border-radius:0 7px 0 0}}
.tbl td{{padding:9px 11px;border-bottom:1px solid {LINE};color:{INK}}}
.tbl tbody tr:nth-child(even){{background:{CREAM}}}
.twocol{{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:8px}}
.fhead{{font-size:11px;font-weight:800;letter-spacing:1px;margin-bottom:10px}}
.funnel{{display:flex;flex-direction:column;gap:5px}}
.fstep{{background:{CREAM};border-radius:0 8px 8px 0;padding:9px 14px}}
.fval{{font-size:20px;font-weight:700;color:{NAVY};font-family:Georgia,serif}}
.flab{{font-size:12px;color:{MUTED}}}
.farr{{text-align:center;color:{LINE};font-size:11px;line-height:1}}
.stepper{{display:flex;align-items:center;flex-wrap:wrap;gap:8px;margin-top:10px}}
.step{{display:flex;align-items:center;gap:8px;background:{CREAM};border:1px solid {LINE};border-radius:22px;padding:6px 13px 6px 6px}}
.stepn{{width:22px;height:22px;border-radius:50%;background:{PURPLE};color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;flex:0 0 auto}}
.steptxt{{font-size:12.5px;font-weight:600;color:{INK}}}
.steparr{{color:{MUTED}}}
.tags{{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}}
.tag{{background:{CREAM};border:1px solid {LINE};border-radius:20px;padding:6px 13px;font-size:12.5px;font-weight:600;color:{NAVY}}}
.callout{{background:{NAVY};color:#eef2f6;border-radius:16px;padding:28px 30px}}
.co-kick{{font-size:11px;font-weight:800;letter-spacing:1.5px;color:{YELLOW};margin-bottom:8px}}
.co-title{{font-size:24px;color:#fff;font-weight:700;margin-bottom:14px}}
.co-list{{list-style:none;display:flex;flex-direction:column;gap:11px}}
.co-list li{{padding-left:22px;position:relative;font-size:14px;color:#dfe6ee}}
.co-list li:before{{content:'';position:absolute;left:0;top:8px;width:8px;height:8px;border-radius:50%;background:{TEAL}}}
.co-list b{{color:#fff}}
.fnote{{margin-top:14px;padding-top:12px;border-top:1px solid {LINE};font-size:12px;color:{MUTED};line-height:1.5}}
.fnote b{{color:{INK}}} .fnote code{{background:{CREAM};border:1px solid {LINE};border-radius:4px;padding:1px 5px;font-size:11px;color:{NAVY}}}
.inflight{{display:flex;gap:14px;align-items:flex-start;background:{YELLOW}14;border:1px dashed {YELLOW};border-radius:12px;padding:14px 16px;margin-top:16px;font-size:13.5px;color:{INK}}}
.if-tag{{flex:0 0 auto;background:{YELLOW};color:{NAVY};font-size:10px;font-weight:800;letter-spacing:1px;padding:4px 9px;border-radius:5px;margin-top:1px}}
.inflight b{{color:{NAVY}}}
.updgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}}
.upd{{background:#fff;border:1px solid {LINE};border-radius:14px;padding:20px}}
.upd-tag{{display:inline-block;font-size:10px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;padding:4px 10px;border-radius:5px;margin-bottom:11px}}
.upd-title{{font-size:18px;color:{NAVY};font-weight:700;margin-bottom:8px}}
.upd-body{{font-size:13.5px;color:{MUTED};line-height:1.6}}
.upd-body b{{color:{INK}}}
.wowrow{{display:grid;grid-template-columns:1.5fr 1fr .7fr .6fr;gap:14px;align-items:center;padding:13px 0;border-bottom:1px solid {LINE}}}
.wowrow:last-child{{border-bottom:none}}
.wowhead{{font-size:10.5px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:{MUTED};padding-bottom:9px}}
.wow-lab{{font-size:13.5px;font-weight:600;color:{NAVY}}}
.wow-cav{{font-size:11px;font-weight:400;color:{MUTED};margin-top:3px;line-height:1.4}}
.spark{{width:100%;max-width:150px;height:44px;display:block}}
.wow-cur{{font-family:Georgia,serif;font-size:20px;font-weight:700;color:{NAVY};text-align:right}}
.wow-d{{font-size:13px;font-weight:700;text-align:right}}
@media(max-width:600px){{.wowrow{{grid-template-columns:1fr .6fr .5fr}}.wow-spark{{display:none}}.wowhead .wow-spark{{display:none}}}}
.foot{{margin-top:44px;padding-top:18px;border-top:1px solid {LINE};font-size:11.5px;color:{MUTED};text-align:center}}
.widemod{{padding:24px 26px 22px}}
.wm-title{{font-size:21px;color:{NAVY};font-weight:700;margin-bottom:6px}}
.wm-lead{{font-size:14px;color:{MUTED};max-width:820px;margin-bottom:6px}}
.wm-lead b{{color:{INK}}}
.pvt{{width:100%;border-collapse:collapse;margin-top:8px;font-size:13px}}
.pvt th{{background:#fff;color:{MUTED};padding:8px 10px;font-size:11px;text-transform:uppercase;letter-spacing:.5px;font-weight:800;text-align:right;border-bottom:2px solid {LINE}}}
.pvt th:first-child{{text-align:left}}
.pvt th span{{display:block;font-size:10px;font-weight:600;letter-spacing:.2px;text-transform:none;color:{MUTED};margin-top:2px}}
.pvt th.pv-spine-h{{color:{NAVY};border-bottom-color:{TEAL}}}
.pvt td{{padding:9px 10px;border-bottom:1px solid {LINE}}}
.pvt tbody tr:last-child td{{border-bottom:none}}
.pv-lab{{color:{INK};font-weight:600}}
.pv-v{{text-align:right;font-variant-numeric:tabular-nums;color:{MUTED}}}
.pv-spine{{font-weight:800;color:{NAVY}}}
@media(max-width:600px){{.pvt th span{{display:none}}}}
@media(max-width:720px){{.grid2,.twocol{{grid-template-columns:1fr}}.title{{font-size:32px}}.donut{{width:160px;height:160px}}}}

/* ---- desktop reading size ----
   The report is typeset in fixed px. Rather than raise every size individually,
   the document renders at 125% on desktop and the content column is narrowed so
   the scaled layout still fits a 1280px viewport. Charts use viewBox and scale
   with it. Below 1180px the layout returns to 100% and the existing responsive
   rules take over. */
@media(min-width:1180px){{
  body{{zoom:1.25}}
  .wrap{{max-width:960px}}
}}
"""

htmlout=f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>onDiem — Weekly Performance Report</title><style>{CSS}</style></head>
<body><div class="wrap">{body}</div></body></html>"""

with open("/home/claude/onDiem_Weekly_Report.html","w") as f:
    f.write(htmlout)
print("written", len(htmlout), "bytes")
