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

def hbars(items, maxv=None, unit="", height_per=34, fmt=None):
    # items: list of (label, value, color)
    if maxv is None: maxv=max(v for _,v,_ in items) or 1
    if fmt is None: fmt=lambda v: f"{v:,}"
    W=680; labw=190; barw=W-labw-70; H=len(items)*height_per+8
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
    W=680; labw=150; barw=W-labw-120; hp=42; H=len(items)*hp+10
    rows=[]
    for i,(lab,a,b,col) in enumerate(items):
        y=i*hp+8
        wa=max(2,(a/maxv)*barw); wb=max(2,(b/maxv)*barw)
        rows.append(f'<text x="{labw-10}" y="{y+21}" text-anchor="end" class="bl">{esc(lab)}</text>')
        rows.append(f'<rect x="{labw}" y="{y+2}" width="{wa:.1f}" height="13" rx="4" fill="{col}" opacity="0.32"/>')
        rows.append(f'<rect x="{labw}" y="{y+18}" width="{wb:.1f}" height="13" rx="4" fill="{col}"/>')
        arrow="▲" if b>a else ("▼" if b<a else "—")
        acol=GREEN if b>a else (RED if b<a else MUTED)
        rows.append(f'<text x="{labw+max(wa,wb)+9:.1f}" y="{y+21}" class="bv">{esc(fmt(a))}{esc(unit)} → {esc(fmt(b))}{esc(unit)}</text>')
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
          'Jul 9 &middot; Jul 16 &middot; Jul 23 &middot; Jul 30 &middot; Aug 6</div>'
          '<div class="wow-cur">This week</div><div class="wow-d">WoW</div></div>')
    ft=f'<p class="fnote">{foot}</p>' if foot else ""
    return card(f'<h3 class="ctitle">{esc(title)}</h3><p class="csub">{esc(sub)}</p>{head}{"".join(rows)}{ft}')

# ================= BUILD =================
day_labels=["Aug 6","Aug 7","Aug 8","Aug 9","Aug 10","Aug 11","Aug 12"]

plat_days=[939,606,257,280,2956,1119,950]
site_days=[596,403,262,283,694,663,639]
paid_days=[68,35,11,26,80,93,72]

# ============ HERO ============
hero_tiles=tiles([
    ("20","Shifts filled on promo codes",GREEN,"August gift-card campaign"),
    ("60","Offers accepted by pros",TEAL,"+36% week over week"),
    ("5,879","Platform active users",BLUE,"app.ondiem.com · −10.4%"),
    ("3,638","Marketing site views",PURPLE,"ondiem.com · +9.8%"),
    ("26.7","AI visibility score",RED,"new low, from 38.1"),
    ("$363","Paid search spend",ORANGE,"brand only · 0 conversions"),
])

# ============ SECTION W: WEEK OVER WEEK ============
wow_rows=[
    wowrow("Platform active users",[7880,8287,7750,7740,7107],TEAL,
           caveat="Sum of daily actives — counts a pro active on three days three times."),
    wowrow("Marketing site views",[3255,3338,3266,3230,3540],BLUE,
           caveat="Weeks through Jul 29 come from the prior 30-day export and differ slightly in page coverage."),
    wowrow("Paid search clicks",[378,382,362,384,385],ORANGE),
    wowrow("AI visibility score",[36.7,41.0,31.4,38.1,26.7],PURPLE,fmt=lambda v:f"{v:.1f}",
           caveat="Weekly snapshots dated Jul 12, 19, 26, Aug 2 and Aug 9."),
]
s_wow=section("wow","Momentum",NAVY,
    'Week over <span class="hl" style="background:'+NAVY+'22">week</span>',
    "Five trailing weeks for the metrics captured as daily series. The lighter bars are prior weeks; the solid bar is the week ending Aug 12.",
    wowcard("Trailing five weeks","Weeks beginning Jul 9, Jul 16, Jul 23, Jul 30 and Aug 6.",wow_rows,
        foot="Platform traffic fell while the marketing site rose and paid held flat. AI visibility dropped 29.9% to a new low. "
             "<b>Read the platform figure alongside the funnel section rather than on its own</b> — sessions rose 2.9% over the same week "
             "and every core marketplace action increased, so the decline is in visitors rather than activity.<br><br>"
             "<b>Not shown:</b> Short.io leaves this panel because the export only produces calendar-month windows this cycle. "
             "Funnel events, social, email and profile completion arrive as period totals and are compared against the prior seven days in their own sections."))

# ============ SECTION 0: UPDATES ============
u1=updatecard("Converting",GREEN,"August $50 gift-card promo",
    "Seven sends reached <b>837 practices</b> across six cities and one all-cities list. The offer redeems on a promo code entered at shift creation, "
    "and the codes have now produced <b>20 filled shifts</b>. The campaign runs through Aug 31 and the second reminder email has not yet gone out, "
    "so this result is not final.")
u2=updatecard("In progress",YELLOW,"Partner site widget",
    "Logan and Darya&rsquo;s partner availability widget detects any non-ondiem.com domain and renders "
    "<b>&ldquo;Find staff ready to work, powered by onDiem.&rdquo;</b> Still no tagged traffic in this window. "
    "Until the widget CTAs carry UTM parameters, its sessions cannot be separated from existing referral traffic.")
u3=updatecard("Launched",BLUE,"DOMA 2026",
    "A six-email practice sequence launched Aug 6 and runs to Sep 29 — follow-up, fast signup, staffing network, ADA member, reliable coverage and pro calendar. "
    "All assets are built. <b>44 sends and 7 opens</b> so far, which is too little volume to read. First real measurement next period.")
s0=section("updates","What shipped",NAVY,
    'Updates <span class="hl" style="background:'+NAVY+'22">this period</span>',
    "Three items in flight. One of them produced the clearest conversion result in this report.",
    '<div class="updgrid">'+u1+u2+u3+'</div>')

# ============ SECTION 1: CAMPAIGNS ============
s1_tiles=tiles([
    ("20","Shifts filled",GREEN,"from 26 code redemptions"),
    ("5","Email clicks",RED,"across 837 delivered"),
    ("2.4%","Delivered → filled shift",TEAL,"campaign conversion rate"),
    ("48","Shifts from the spring mailer",PURPLE,"final — previously reported as 15"),
])
promo_funnel=card('<h3 class="ctitle">Where clicks stop being the measure</h3>'
    '<p class="csub">The August promo, end to end. The funnel breaks at clicks and recovers at redemption.</p>'
    +funnel([("Practices emailed","837",BLUE),
             ("Opened","117",BLUE),
             ("Clicked the email","5",RED),
             ("Entered a promo code at shift creation","26",TEAL),
             ("Filled a shift","20",GREEN)])+
    '<p class="fnote"><b>Redemption ran four times the click count.</b> A practice can enter a code without ever opening the link, so click rate '
    'measures the email rather than the offer. Against 837 delivered, 20 filled shifts is a <b>2.4% conversion rate</b> — higher than any '
    'other handoff measured in this report by an order of magnitude.</p>'
    '<p class="fnote">The promo code is distributed by email only, so this result is attributable to the campaign. '
    'Of the 20 filled shifts, <b>13 went to hygienists and 7 to dental assistants</b>.</p>')
code_tbl=chart_card("Promo code performance",
    table(["Code","Used","Filled","Still open","Cancelled"],
          [["Starbucks","15","10","3","2"],
           ["Target","6","5","1","0"],
           ["DoorDash","5","5","0","0"],
           ["Amazon","0","0","0","0"],
           ["Total","26","20","4","2"]],
          hi_cols=[2], hi_color=GREEN),
    "Amazon drew nothing across 26 redemptions, which is worth checking against how the four options were presented.")
promo_email=chart_card("The seven sends",
    table(["Send","Delivered","Opens","Open rate","Clicks"],
          [["All cities","136","29","21.3%","2"],
           ["Portland","268","40","14.9%","3"],
           ["Atlanta","60","9","15.0%","0"],
           ["Chicago","151","19","12.6%","0"],
           ["Houston","40","5","12.5%","0"],
           ["Miami","16","2","12.5%","0"],
           ["Minneapolis","166","13","7.8%","0"],
           ["Total","837","117","14.0%","5"]],
          hi_cols=[3], hi_color=PINK),
    "The untargeted all-cities send outperformed every city-specific version on both open and click rate.")
mailer_corr=card('<h3 class="ctitle" style="color:'+PURPLE+'">Correction: the spring mailer produced 48 shifts, not 15</h3>'
    '<p class="csub">Last period&rsquo;s figure was recorded while timecards were still clearing.</p>'
    +table(["Code","Used","Booked","Cancelled","Expired"],
           [["EARN50PDX (Portland)","54","38","12","4"],
            ["EARN50MPLS (Minneapolis)","15","10","3","1"],
            ["Atlanta / Miami / Houston / Chicago","0","0","0","0"],
            ["Total","69","48","15","5"]],
           hi_cols=[2], hi_color=PURPLE)+
    '<p class="fnote">The physical mailer has now fully settled at <b>69 redemptions and 48 booked shifts</b>. Portland and Minneapolis account for '
    'all of it; the four cities where geo paid spend went to zero produced nothing. '
    'This is a restatement rather than new activity, and it means gift-card results need roughly two months before they can be read as final.</p>')
rdh=chart_card("RDH Under One Roof — nurture status",
    funnel([("Contacts enrolled in the workflow","361",PURPLE),
            ("Emails delivered","1,480",PURPLE),
            ("Opened","321",BLUE),
            ("Clicked","12",RED),
            ("Still enrolled","237",TEAL)]),
    "Marked complete, but 237 contacts remain in the sequence.")
rdh_note=card('<p class="fnote"><b>The conversion figure for this campaign is not available this period.</b> 124 contacts have exited the workflow, '
    'and an exit can mean a sign-up, an unsubscribe or a completed sequence — those point in opposite directions. '
    'Last period the nurture had produced 4 sign-ups against 451 event leads. The current count and the exit-reason breakdown are one pull and would settle it.</p>'
    '<p class="fnote">Open rate on this list is <b>21.7%</b>, which is healthy for a cold audience captured at an event. '
    'Reach is not the constraint here; the handoff is.</p>')
s1=section("campaigns","Lifecycle",GREEN,
    'Campaigns — <span class="hl" style="background:'+GREEN+'33">the promo converted</span>',
    "Four campaigns ran in or across this window. One of them connects spend to a filled shift, which nothing else in this report does.",
    s1_tiles+promo_funnel+'<div class="grid2">'+code_tbl+promo_email+'</div>'+mailer_corr+rdh+rdh_note)

# ============ SECTION 2: MARKETPLACE ============
s2_tiles=tiles([
    ("60","Offers accepted",GREEN,"from 44 · +36.4%"),
    ("10,292","Sessions",TEAL,"+2.9%"),
    ("5,879","Active users",RED,"−10.4%"),
    ("3.02","Listings per posting practice",ORANGE,"from 2.51"),
])
plat_area=chart_card("Daily active users",
    area(plat_days, day_labels, color=TEAL, hi_idx=[4]),
    "The Monday cycle holds. Aug 10 drew 2,956 against 3,722 the previous Monday.")
plat_funnel=chart_card("Core marketplace actions, week over week",
    pairbars([("Offers accepted",44,60,GREEN),
              ("Shift creation started",424,503,TEAL),
              ("Job searches",2157,2393,BLUE),
              ("Listings created",640,676,PURPLE),
              ("Pro registrations started",162,188,PINK),
              ("Shift requests",835,717,RED)],
             fmt=lambda v:f"{v:,.0f}"),
    "Five of six core actions rose. professional_accepted_offer is the most reliable booking proxy in the platform data.")
plat_users=chart_card("Where the decline actually sits",
    pairbars([("Desktop users",4423,3531,BLUE),
              ("Mobile users",2124,2332,PINK),
              ("First visits",5138,4422,MUTED)],
             fmt=lambda v:f"{v:,.0f}"),
    "Desktop fell 20.2% while mobile rose 9.8%. Mobile share moved from 32.4% to 39.6% in a single week.")
plat_sources=chart_card("Traffic sources",
    hbars([("Direct",5032,NAVY),("Google paid",1640,ORANGE),("Internal (ondiem)",1199,TEAL),
           ("Unattributed",1156,RED),("Google organic",497,GREEN),("Internal (ondiem_pro)",113,MAUVE),
           ("HubSpot email",87,PURPLE)]),
    "10,292 sessions in total.")
plat_note=card('<h3 class="ctitle">Fewer people, doing more</h3>'
    '<p class="fnote">Active users fell 10.4% while sessions rose 2.9% and every core action except shift requests increased. '
    'The 36.4% rise in accepted offers sits in the same week the gift-card promo filled 20 shifts. The two numbers are consistent, '
    'though the platform data cannot confirm the connection directly.</p>'
    '<p class="fnote"><b>Concentration tightened again.</b> Listings rose 5.6% while the practices creating them fell from 255 to 224 — '
    'from 2.51 listings each to 3.02. The pro side moved the other way: shift requests fell 14.1% while the pros making them rose from 97 to 120.</p>'
    '<p class="fnote"><b>Two data notes.</b> A <code>(not set)</code> source accounted for 1,156 sessions — 11.2% of platform traffic — '
    'with no counterpart in the prior week. That is new and large enough to distort the source mix; worth confirming whether a tag changed. '
    'And GA4 credits google/cpc with 1,640 sessions against 385 recorded ad clicks, a factor of 4.3 that matches the 4.4 seen last period. '
    'Sessions carry their original source across return visits, so paid&rsquo;s apparent share remains overstated.</p>')
s2=section("marketplace","The core product",TEAL,
    'Marketplace — <span class="hl" style="background:'+TEAL+'33">app.ondiem.com</span>',
    "Traffic thinned while the funnel converted better. This is the first week in this report where those two move in opposite directions.",
    s2_tiles+plat_area+plat_funnel+'<div class="grid2">'+plat_users+plat_sources+'</div>'+plat_note)

# ============ SECTION 3: MARKETING SITE ============
s3_tiles=tiles([
    ("3,638","Page views",BLUE,"+9.8%"),
    ("63","Form starts",ORANGE,"from 36"),
    ("1","Form submission",RED,"from 2"),
    ("710","Availability views",TEAL,"+8.2%"),
])
site_area=chart_card("Daily page views",
    area(site_days, day_labels, color=BLUE),
    "A clean weekday pattern. Every weekday in this window ran ahead of the same day the week before.")
site_channels=chart_card("Traffic by channel",
    hbars([("Organic Search",2006,GREEN),("Direct",1381,NAVY),("Referral",173,TEAL),
           ("Paid Search",44,ORANGE),("Organic Social",22,PINK),("Cross-network",5,MAUVE),
           ("AI Assistant",3,BLUE)]),
    "Search and direct carry 93.1%. Paid is small here because the ads point at hub.ondiem.com.")
site_pages=chart_card("Top pages",
    hbars([("Home /",2355,NAVY),("/professionals",770,PINK),("/practices",121,TEAL),
           ("/contact-us",97,ORANGE),("/ondiem-darby",68,GREEN),("/shifts",46,PURPLE),("/ada",26,MAUVE)]),
    "Home and the professionals page are 86% of views, unchanged in shape from last period.")
site_device=chart_card("Device split",
    donut([("Mobile",2164,PINK),("Desktop",1455,BLUE),("Tablet",19,MUTED)],"59.5%","mobile"),
    "The mirror image of the platform, which runs desktop-heavy.")
form_call=card('<h3 class="ctitle" style="color:'+RED+'">Form starts nearly doubled. Submissions went down.</h3>'
    '<p class="csub">63 users began a form against 36 the week before. One completed.</p>'
    +funnel([("Began a form on ondiem.com","63",BLUE),("Completed and submitted","1",RED)])+
    '<p class="fnote">Across the two weeks that is <b>99 starts and 3 submissions</b>, consistent with the 230-to-5 recorded last period. '
    'The defect is known, logged in Jira, and currently behind the pro app in engineering priority.</p>'
    '<p class="fnote"><b>The loss is growing even though the rate is flat.</b> <code>/contact-us</code> views rose 62% to 97, so more practices and pros '
    'are actively trying to reach onDiem through the site and failing at the last step. A stable 2–3% completion rate on a rising denominator '
    'is a widening gap, not a steady one.</p>'
    '<p class="fnote"><b>AI Assistant sent 3 views.</b> Visibility in AI answers continues to produce effectively no traffic — relevant to the section below.</p>')
s3=section("website","Brand &amp; acquisition",BLUE,
    'Marketing site — <span class="hl" style="background:'+BLUE+'33">ondiem.com</span>',
    "Traffic rose across every channel. The one conversion action on the site went the other way.",
    s3_tiles+site_area+'<div class="grid2">'+site_channels+site_pages+'</div>'+'<div class="grid2">'+site_device+form_call+'</div>')

# ============ SECTION 4: PAID SEARCH ============
s4_tiles=tiles([
    ("$363","Spend",ORANGE,"+0.8%"),
    ("385","Clicks",NAVY,"+0.3%"),
    ("68.8%","Impression share",GREEN,"from 65.3%"),
    ("0","Tracked conversions",RED,"fourth period running"),
])
paid_area=chart_card("Daily clicks",
    area(paid_days, day_labels, color=ORANGE),
    "Demand still peaks Monday through Thursday and collapses at the weekend.")
paid_device=chart_card("Spend by device",
    donut([("Mobile",237,PINK),("Desktop",124,BLUE),("Tablet",2,MUTED)],"65%","mobile"),
    "Mobile now takes roughly two thirds of the budget at a higher cost per click.")
auction=chart_card("Auction insights",
    table(["Advertiser","Impression share","onDiem outranks them","They appear above onDiem"],
          [["onDiem","68.75%","—","—"],
           ["teero.com","37.84%","64.32%","16.05%"],
           ["clouddentistry.com","33.64%","63.30%","24.24%"],
           ["gotu.com","19.32%","66.70%","14.06%"],
           ["dentalmatch.ai","13.52%","67.50%","10.68%"],
           ["job-medley.com","< 10%","68.30%","13.33%"]],
          hi_cols=[1], hi_color=GREEN),
    "onDiem holds 86.12% absolute top of page and outranks every competitor in the auction.")
paid_note=card('<h3 class="ctitle">Position improved. Nothing downstream is measured.</h3>'
    '<p class="fnote">One campaign, $50 a day, two phrase-match keywords on the brand name. The four geo campaigns remain enabled at <b>$0</b> — '
    'they exist in the account but carry no budget.</p>'
    '<p class="fnote"><b>The competitor set shifted again.</b> <code>dentalmatch.ai</code> entered at 13.52% impression share, the first AI-native '
    'competitor to appear in this auction. Cloud Dentistry moved from 26.98% to 33.64% and GoTu from 11.45% to 19.32% — both bidding harder on '
    'onDiem&rsquo;s own name. Princess Dental Staffing and Direct Dental dropped out.</p>'
    '<p class="fnote">Search terms are entirely brand and navigational. <code>ondiem customer service number</code> and <code>ondiem phone number</code> '
    'together drew 9 clicks at $16.58 — support queries the account is paying for.</p>'
    '<p class="fnote"><b>Zero tracked conversions for a fourth consecutive period.</b> 1,567 of the attributed clicks land on <b>hub.ondiem.com</b>, '
    'which sits outside both GA4 properties in this report. This is a measurement gap rather than a performance result.</p>')
s4=section("paid","Paid media",ORANGE,
    'Paid search — <span class="hl" style="background:'+ORANGE+'33">brand defence</span>',
    "Flat spend, flat volume, stronger auction position, and still nothing measured after the click.",
    s4_tiles+'<div class="grid2">'+paid_area+paid_device+'</div>'+auction+paid_note)

# ============ SECTION 5: AI VISIBILITY ============
s5_tiles=tiles([
    ("26.7","Visibility score",RED,"new low, from 38.1"),
    ("14%","Share of voice",ORANGE,"5th of eight brands"),
    ("37.5%","Citations from competitor pages",PINK,"from 27.4%"),
    ("6.0%","Citations from owned pages",TEAL,"flat"),
])
sov=chart_card("Share of voice across AI answers",
    hbars([("GoTu",21,BLUE),("Cloud Dentistry",19,PURPLE),("Kwikly",18,MAUVE),("onDiem",14,TEAL),
           ("Toothio",14,ORANGE),("Princess Dental",7,PINK),("Stynt",4,MUTED),("TempStars",3,MUTED)],
          maxv=24, unit="%", fmt=lambda v:f"{v:g}"),
    "onDiem is now tied with Toothio for fourth. Measured Jul 16 – Aug 13.")
vis_trend=chart_card("Visibility over five weekly snapshots",
    mline([("onDiem",[36.7,41.0,31.4,38.1,26.7],TEAL),
           ("GoTu",[50.0,59.0,51.4,50.5,49.2],BLUE),
           ("Cloud Dentistry",[47.5,46.7,46.7,48.6,46.7],PURPLE),
           ("Kwikly",[40.0,47.6,41.9,43.3,42.5],MAUVE),
           ("Toothio",[30.0,39.0,34.3,32.4,29.2],ORANGE),
           ("Princess Dental",[13.3,12.4,16.7,17.1,22.5],PINK)],
          ["Jul 12","Jul 19","Jul 26","Aug 2","Aug 9"], maxv=65, hi="onDiem"),
    "onDiem is the only brand in the set that has lost ground, and now sits below Toothio. Princess Dental has closed to within 4.2 points.")
engines=chart_card("Visibility by engine",
    pairbars([("ChatGPT",34.3,32.5,PINK),("Gemini",50.0,35.0,TEAL),("Perplexity",30.0,12.5,BLUE)],
             unit="%"),
    "The decline moved. Last period it was ChatGPT halving; this period ChatGPT held and Gemini, the strongest engine, dropped 15 points.")
cite_mix=chart_card("Where AI answers source their citations",
    pairbars([("Peer / directory",49.6,39.5,BLUE),("Competitor-owned",27.4,37.5,PINK),
              ("Earned",8.6,11.3,GREEN),("Owned",5.4,6.0,TEAL),
              ("Review sites",4.3,4.2,YELLOW),("UGC",4.6,1.6,MAUVE)],
             unit="%"),
    "Neutral directory sources and competitor-owned pages crossed trajectories over the six weeks.")
sentiment=chart_card("Sentiment by engine",
    pairbars([("ChatGPT",61.3,46.9,PINK),("Gemini",68.6,77.1,TEAL),("Perplexity",42.9,28.0,BLUE)],
             unit=""),
    "Gemini cites onDiem less often but speaks more favourably when it does.")
aeo_note=card('<h3 class="ctitle">Presence is falling, and it was not converting</h3>'
    '<p class="fnote">onDiem&rsquo;s score fell to <b>26.7</b>, below the 31.4 that was previously the floor. It is the only brand in the tracked set '
    'moving down, and Princess Dental Staffing is the only one moving up — from 13.3 to 22.5 over five weeks, the fifth signal from that '
    'competitor in this report.</p>'
    '<p class="fnote"><b>Competitor-owned pages are now the largest single citation source</b> at 37.5%, having passed peer and directory sources. '
    'Owned pages supply 6.0%. AI answers are increasingly assembled from pages competitors wrote about themselves.</p>'
    '<p class="fnote">Set against that: AI Assistant referrals sent <b>3 views</b> to ondiem.com this week. '
    'This is a position worth defending rather than a channel to attribute.</p>')
s5=section("aeo","Discovery",PURPLE,
    'AI visibility — <span class="hl" style="background:'+PURPLE+'33">a new low</span>',
    "Measured Jul 12 – Aug 13, which does not match the reporting window and is labelled accordingly.",
    s5_tiles+sov+vis_trend+'<div class="grid2">'+engines+sentiment+'</div>'+cite_mix+aeo_note)

# ============ SECTION 6: SOCIAL ============
s6_tiles=tiles([
    ("3,340","Instagram views",PINK,"7 pieces of content"),
    ("84.4%","From non-followers",TEAL,"reach still working"),
    ("409","LinkedIn clicks",GREEN,"from 589 impressions"),
    ("+441","Princess Dental followers",RED,"in one week"),
])
ig_ctx=card('<h3 class="ctitle">Read this against two weeks, not one</h3>'
    '<p class="csub">Instagram views fell 52.7%. That number is an artefact of a single post.</p>'
    +table(["","Aug 6–12","Jul 30–Aug 5"],
           [["Views","3,340","7,067"],
            ["Content published","7","3"],
            ["Avg. reach per day","333","466"],
            ["Accounts engaged","14","34"]])+
    '<p class="fnote">The prior week&rsquo;s total came almost entirely from one post: the <b>Dental Assistant Palooza</b> announcement on Jul 30 drew '
    '<b>6,892 views and 26 interactions</b> on its own. It named a date, a city and a person hosting a Q&amp;A. Nothing else that week came close.</p>'
    '<p class="fnote">This week ran three feed carousels totalling 2,467 views across seven pieces of content. '
    'The honest read is not that Instagram declined by half — it is that <b>one event post outperformed a full week of brand content by roughly 3x</b>, '
    'and reach reverted to baseline when it left the window.</p>')
ig_type=chart_card("Instagram views by content type",
    hbars([("Carousel",2995,TEAL),("Story",102,PURPLE),("Reel",90,PINK),("Post",8,MUTED)]),
    "Carousels carry the account. Reels drew 90 views across the week.")
li=chart_card("LinkedIn — identical creative, different outcome",
    table(["Post","Impressions","Clicks","Engagement"],
          [["Is the hygienist shortage only about hygienists?","189","154","83.6%"],
           ["Your career has options","350","226","64.9%"],
           ["One call-off can impact more than the schedule","50","29","68.0%"],
           ["Total","589","409","—"]],
          hi_cols=[2], hi_color=GREEN),
    "All three are document posts. The same three pieces drew 9 interactions on Instagram and 7 clicks on Facebook.")
comp=chart_card("Competitor follower growth",
    table(["Account","Followers","Change","Reels this week"],
          [["Princess Dental Staffing","10,179","+441","11"],
           ["Teero","3,450","+58","—"],
           ["Kwikly Dental Staffing","2,459","+9","—"]],
          hi_cols=[2], hi_color=RED),
    "Princess crossed 10,000 followers on a reels-led strategy.")
social_note=card('<h3 class="ctitle">The pattern is format, not volume</h3>'
    '<p class="fnote"><b>LinkedIn has a fifth of Instagram&rsquo;s reach and forty-five times the clicks.</b> 589 impressions produced 409 clicks on document posts. '
    'That relationship has held in every period measured so far.</p>'
    '<p class="fnote">Facebook remains negligible: four posts, 268 impressions, 195 reach, 7 clicks and 1 reaction.</p>'
    '<p class="fnote">The two things that worked this fortnight — the Palooza event post and the LinkedIn documents — were both specific and '
    'useful rather than brand-general. That is a more actionable read than the view count.</p>')
s6=section("social","Owned social",PINK,
    'Social — <span class="hl" style="background:'+PINK+'33">format over volume</span>',
    "Instagram, Facebook and LinkedIn. Two formats performed; the headline number reflects neither.",
    s6_tiles+ig_ctx+'<div class="grid2">'+ig_type+li+'</div>'+comp+social_note)

# ============ SECTION 7: LINK TRACKING ============
s7_tiles=tiles([
    ("4","Clicks on the ADA email link",RED,"from 679 in July"),
    ("7.3%","Human clicks",RED,"from 63.0%"),
    ("79","Human clicks total",MUTED,"Aug 1 – 13"),
    ("~6","Human clicks per day",NAVY,"without the ADA send"),
])
short_tbl=chart_card("Clicks by path",
    table(["Path","Aug 1–13","Jul 1–31"],
          [["/ada-email","4","679"],
           ["/*","32","103"],
           ["/ada-website","17","49"],
           ["/","10","73"],
           ["/onDiem-youtube","7","7"],
           ["/ada-member-advantage","4","8"],
           ["/website","2","13"]],
          hi_cols=[1], hi_color=RED),
    "Windows are calendar months and do not match the reporting period.")
short_note=card('<h3 class="ctitle">The ADA email did not send in August</h3>'
    '<p class="fnote">That single fact explains the section. <code>/ada-email</code> carried <b>679 clicks in July and 4 in August</b>, and the medium '
    'breakdown confirms it — email fell from 679 clicks to 4 while unattributed traffic now accounts for 72 of 76 clicks. '
    'Worth confirming whether the August send is scheduled or skipped; three sends across June and July had started to look like a cadence.</p>'
    '<p class="fnote"><b>Bot traffic is now 93% of the domain.</b> Human share fell from 63.0% to 7.3%. Non-human clicks rose to roughly 78 a day from '
    '18 in July while human clicks fell away. July&rsquo;s top cities were Ashburn (418) and Columbus (144); August&rsquo;s are unidentified. '
    'This is scanner load against a quiet domain, and it means the raw click count is not usable without the human split.</p>'
    '<p class="fnote">Short.io only produces calendar-month windows in the current export, so this section is labelled Aug 1–13 against Jul 1–31 '
    'and is excluded from the week-over-week panel. A Click Stream export would restore daily granularity.</p>')
s7=section("links","Partnerships",MAUVE,
    'Link tracking — <span class="hl" style="background:'+MAUVE+'33">Short.io</span>',
    "Tracked short links, almost entirely the ADA partnership programme. Measured Aug 1 – 13 against Jul 1 – 31.",
    s7_tiles+short_tbl+short_note)

# ============ SECTION 8: PROFILE COMPLETION ============
s8_tiles=tiles([
    ("555","Pros tracked",NAVY,"new cohort — see note"),
    ("15.7%","Fully complete",TEAL,"from 12.8% at baseline"),
    ("11","Pros acted in 2.5 weeks",RED,"no SMS was sent"),
    ("63.4%","Missing a personal bio",PINK,"largest gap"),
])
prof_roles=chart_card("Completion by role",
    table(["Role","Pros","Profile photo","Personal bio","Work experience","Education"],
          [["Office Staff","16","87.5%","93.8%","93.8%","87.5%"],
           ["Dentist","17","70.6%","76.5%","70.6%","52.9%"],
           ["Dental Assistant","255","55.3%","62.0%","57.6%","59.6%"],
           ["Dental Hygienist","267","50.9%","62.2%","61.8%","43.4%"]],
          hi_cols=[5], hi_color=RED),
    "Hygienists and assistants are the largest cohorts and the least complete. Education is the weakest field for hygienists.")
prof_note=card('<h3 class="ctitle">Completion is prompt-dependent</h3>'
    '<p class="fnote"><b>No SMS went out between Jul 20 and this pull</b>, so the 2.5-week window measures organic behaviour with no nudge. '
    '<b>Eleven pros completed a section</b>, against 45 cumulatively since the baseline. When the prompt stops, movement stops. '
    'That is the same decay seen in the email drip and argues for cadence rather than better copy.</p>'
    '<p class="fnote"><b>The tracked cohort changed.</b> This report covers the 555 pros present in all three pulls (Jul 13, Jul 20, Aug 6). '
    'The previous report tracked 765 on a different definition, so the two counts are not comparable. '
    'Profile Photo remains the strongest converter at 28 cumulative completions; Personal Bio is the largest gap and barely moves.</p>'
    '<p class="fnote"><b>137 pros are missing four of six sections.</b> That group has not responded to any outreach so far and likely needs a different '
    'channel rather than another message. Oregon (132) and Minnesota (60) lead by volume — the same two markets where the gift-card promo worked. '
    'New York and Virginia show the highest incompletion rates.</p>'
    '<p class="fnote">Round-one and round-two SMS clicks recorded last period (152 and 89) still have no completion counts attached.</p>')
s8=section("profiles","Supply quality",TEAL,
    'Profile <span class="hl" style="background:'+TEAL+'33">completion</span>',
    "Profile completeness across recently active professionals, measured Aug 6 against a Jul 13 baseline.",
    s8_tiles+prof_roles+prof_note)

# ============ TAKEAWAYS ============
take=callout("What this means for next period",[
    "<b>The promo converted, and it is the only thing in this report that did.</b> 837 emails produced 5 clicks and 20 filled shifts. "
    "Redemption ran four times the click count, which settles the argument about which metric to run this campaign on. "
    "The spring mailer has also now fully settled at 48 booked shifts rather than the 15 reported while timecards were clearing.",

    "<b>The marketplace funnel improved while traffic thinned.</b> Active users fell 10.4% and first visits 13.9%, but sessions rose, "
    "accepted offers rose 36.4%, and five of six core actions increased. Read together with the promo, this is the first period where "
    "conversion moved in the right direction. It is also the first period where the top of the funnel did not.",

    "<b>Discovery is going the other way.</b> AI visibility hit a new low at 26.7, onDiem is the only tracked brand losing ground, and "
    "competitor-owned pages are now the largest source of citations at 37.5%. Princess Dental Staffing appears in five separate places in this "
    "report — Instagram growth, AEO climb, share of voice, follower base and, last period, the brand-term auction.",

    "<b>The site still leaks at the same point.</b> Form starts nearly doubled to 63 and produced one submission. "
    "The rate is unchanged; the loss is larger because more people are trying. /contact-us views rose 62% over the same week.",

    "<b>Three measurement items are unchanged from last period.</b> Paid has recorded zero tracked conversions for a fourth consecutive period and "
    "lands on hub.ondiem.com, outside both GA4 properties. The partner widget still has no UTM tags, so its traffic cannot be separated. "
    "And 11.2% of platform sessions arrived unattributed this week, which is new.",

    "<b>Two things to settle before the next report.</b> Whether the August ADA email is scheduled or skipped, since its absence accounts for the "
    "entire link-tracking decline. And the RDH sign-up count, since 237 contacts remain in a workflow marked complete.",
], kicker="Aug 6 – 12, 2026")

# ============ ASSEMBLE ============
nav=('<nav class="toc"><a href="#wow">Week over week</a><a href="#updates">Updates</a><a href="#campaigns">Campaigns</a><a href="#marketplace">Marketplace</a><a href="#website">Website</a>'
     '<a href="#paid">Paid</a><a href="#aeo">AI visibility</a><a href="#social">Social</a>'
     '<a href="#links">Links</a><a href="#profiles">Profiles</a></nav>')

header=(f'<header class="masthead"><div class="mh-top"><span class="brand">'
        f'<span class="brand-mark">&#9681;</span> onDiem</span><span class="period">7-DAY VIEW &middot; AUG 6 &ndash; 12, 2026</span></div>'
        f'<h1 class="title">Marketing Performance <span class="hl" style="background:{TEAL}44">Report</span></h1>'
        f'<p class="subtitle">A single view across the marketplace, marketing site, paid search, AI visibility, social, partnerships, email and profile quality. Prepared by Figment Creative.</p>'
        f'{nav}</header>')

body=(header+
      f'<section class="hero"><div class="sec-head">{eyebrow("At a glance", NAVY)}'
      f'<h2 class="sec-title">The week in six numbers</h2></div>{hero_tiles}</section>'+
      s_wow+s0+s1+s2+s3+s4+s5+s6+s7+s8+
      f'<section>{take}</section>'+
      f'<footer class="foot">onDiem Marketing Performance Report &middot; Reporting window Aug 6 &ndash; 12, 2026 &middot; prior week Jul 30 &ndash; Aug 5 &middot; AI visibility measured Jul 12 &ndash; Aug 13 &middot; Short.io measured Aug 1 &ndash; 13 &middot; Sources: GA4, Metricool, Google Ads, Short.io, HubSpot &middot; Internal use</footer>')

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
@media(max-width:720px){{.grid2,.twocol{{grid-template-columns:1fr}}.title{{font-size:32px}}.donut{{width:160px;height:160px}}}}
"""

htmlout=f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>onDiem — Weekly Performance Report</title><style>{CSS}</style></head>
<body><div class="wrap">{body}</div></body></html>"""

with open("/home/claude/onDiem_Weekly_Report.html","w") as f:
    f.write(htmlout)
print("written", len(htmlout), "bytes")
