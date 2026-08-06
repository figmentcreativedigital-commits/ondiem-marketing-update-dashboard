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

# ================= BUILD =================
P=[]

# ---- daily platform active users (Jul 7 - Aug 5) ----
plat_days=[890,799,844,580,263,345,3852,1067,929,873,593,250,281,4123,1211,
           956,913,581,267,347,3877,928,837,914,560,289,297,3722,997,957]
day_labels=["Jul 7","","","Jul 10","","","Jul 13","","","Jul 16","","","Jul 19","","",
            "Jul 22","","","Jul 25","","","Jul 28","","","Jul 31","","","Aug 3","","Aug 5"]
mondays=[6,13,20,27]

# ---- marketing site daily views ----
site_days=[613,513,511,404,240,341,633,600,526,531,386,231,280,624,660,
           626,576,387,270,355,617,555,506,559,380,247,290,596,578,559]

# ---- paid search daily clicks ----
paid_days=[99,62,51,43,20,25,90,73,76,66,27,17,23,84,85,
           80,51,40,27,36,89,68,51,68,36,24,16,79,77,84]

# ---- Short.io daily clicks (Jul 7 - Aug 5) ----
short_days=[3,9,12,41,7,8,5,1,5,12,8,3,16,25,14,0,0,257,15,13,5,4,12,4,3,5,7,3,2,3]
_HR=512/949   # domain-level human-click rate for the export period
short_human=[round(v*_HR) for v in short_days]

# ============ HERO ============
hero_tiles=tiles([
    ("24,936","Platform active users",TEAL,"app.ondiem.com · 30 days"),
    ("15","Shifts booked on promo",GREEN,"gift-card mailer, confirmed"),
    ("591","New pros registered",PINK,"signup completed"),
    ("14,657","Marketing site views",BLUE,"ondiem.com"),
    ("15.6K","Instagram views",PURPLE,"81% from non-followers"),
    ("$1,555","Paid search spend",ORANGE,"Google Ads, brand only"),
])

# ============ SECTION 0: UPDATES ============
u1=updatecard("Live",TEAL,"Partner site widget",
    "Logan and Darya shipped the partner availability widget. It detects any non-ondiem.com domain and renders "
    "<b>&ldquo;Find staff ready to work, powered by onDiem.&rdquo;</b> Scope was kept narrow to ship quickly; messaging can expand later. "
    "Live after the window closed, so there is no performance data this period.")
u2=updatecard("In market",ORANGE,"August $50 gift-card promo",
    "Six city-targeted sends went out Aug 5 to <b>701 practices</b> in Portland, Minneapolis, Chicago, Atlanta, Houston and Miami. "
    "Practices earn a $50 gift card per shift posted and worked through Aug 31. "
    "The offer redeems on a promo code entered at shift creation, so clicks understate response — redemption is the measure.")
u3=updatecard("Working",GREEN,"Google review automation",
    "A happy CSAT response now triggers an automated review request. Reviews moved from <b>9 at 3.7</b> to <b>16 at 4.3</b> in about two months, "
    "after roughly a year with none. The request has been extended from live chat to email tickets. "
    "The app store listing sits separately at 5 reviews and 1.8.")
s0=section("updates","What shipped",NAVY,
    'Updates <span class="hl" style="background:'+NAVY+'22">this period</span>',
    "Three items landed at or just after the close of the window. None carry performance data yet; each is noted here so next period&rsquo;s numbers have context.",
    '<div class="updgrid">'+u1+u2+u3+'</div>')

# ============ SECTION 1: MARKETPLACE ============
s1_tiles=tiles([
    ("24,936","Active users",TEAL,"4 Mondays this window"),
    ("285K","Page views",NAVY),
    ("2,815","Pros signed in",PINK),
    ("1,415","Practices signed in",BLUE),
    ("15","Shifts booked on promo",GREEN,"confirmed timecards"),
])
plat_area=chart_card("Daily active users — the Monday cycle holds",
    area(plat_days, day_labels, color=TEAL, hi_idx=mondays),
    "Every Monday clears 3,700 (marked) against a 250–1,200 baseline. The marketplace still runs on a weekly shift-posting rhythm. "
    "This window contains four Mondays; the previous window contained five, which accounts for part of the period-over-period change in active users.")
plat_practice=funnel([
    ("Listings created — by 649 practices","2,723",TEAL),
    ("Shift-creation flows started","1,766",TEAL),
    ("Shift offers sent to pros (largely automated)","175,371",TEAL),
    ("Shift confirmations (GA4 event)","1,362",GREEN),
])
plat_pro=funnel([
    ("Job searches — by 3,046 pros","9,424",PINK),
    ("Shifts viewed — by 6,180 pros","15,601",PINK),
    ("Shift requests submitted — by 365 pros","2,960",PINK),
    ("Offers accepted — by 143 pros","300",GREEN),
])
plat_funnels=card(
    '<h3 class="ctitle">Two-sided marketplace funnel</h3>'
    '<div class="twocol">'
    f'<div><div class="fhead" style="color:{TEAL}">PRACTICE SIDE — posting &amp; booking</div>{plat_practice}</div>'
    f'<div><div class="fhead" style="color:{PINK}">PROFESSIONAL SIDE — finding work</div>{plat_pro}</div>'
    '</div>'
    '<p class="fnote">These are GA4 <b>event counts</b>, not verified bookings. <code>temp_shift_confirmed</code> fired 1,362&times; from '
    '<b>22 accounts</b> and <code>temp_shift_offered</code> 175,371&times; from <b>56</b> — both driven by a small number of practice-admin or automated '
    'senders. <code>professional_accepted_offer</code> (300 events, 143 distinct pros) is the closest GA4 signal to a pro actually taking work.</p>')

promo_tbl=table(
    ["Market","Practices in log","Shifts booked"],
    [["Portland / Oregon metro","6","10"],
     ["Minneapolis / Twin Cities","2","5"],
     ["Total","8","15"]],
    hi_cols=[2], hi_color=GREEN)
promo=card('<h3 class="ctitle">The one closed loop: spend to filled shift</h3>'
    '<p class="csub">The May/June physical gift-card mailer produced 15 confirmed shifts, tracked from promo code through approved timecard. '
    'It is the only place in this report where marketing spend connects to a filled shift.</p>'
    +promo_tbl+
    '<p class="fnote">Volume came from <b>repeat behaviour, not new practices</b>. Roughly eight practices produced all fifteen shifts — '
    'Metro Dentalcare appears five times, Weber and South Hillsboro three each. On the pro side one hygienist worked four of them. '
    'These practices already had accounts; the incentive moved them from registered to posting, and once posting they continued. '
    'Three further shifts await timecard approval and one fell outside the July cutoff.</p>')

plat_device=chart_card("Device — still desktop-first, but less so",
    donut([("Desktop",17462,NAVY),("Mobile",7424,PINK),("Tablet",50,YELLOW)],"70%","desktop"),
    "Desktop fell from 75% to 70% and mobile rose to 29.8%. Practice staff still work at the front desk, but more of the traffic now arrives on a phone.")
plat_sources=chart_card("How users reach the platform",
    hbars([("Direct (logged-in)",57.2,NAVY),("Google — paid (CPC)",16.5,ORANGE),("Internal navigation",13.9,TEAL),
           ("Google — organic",4.2,GREEN),("Email + SMS re-engagement",2.0,PINK)],
          maxv=65, unit="%", fmt=lambda v:f"{v:g}"),
    "Direct traffic fell from 63% to 57.2%. Paid rose to 16.5% — but see the note below on how that share is counted.")
plat_pages=chart_card("Most-used pages",
    hbars([("/login",21561,NAVY),("/results",17361,PINK),("/search",13719,TEAL),("/my-jobs",13064,BLUE),
           ("/timesheets",9590,GREEN),("/dashboard",8523,PURPLE),("/employee-portal",6350,ORANGE),("/registration",4212,MAUVE)],
          fmt=lambda v:f"{v:,}"),
    "Job discovery, My Jobs and Timesheets carry the volume. Internal admin pages are excluded — /administrator drew 4,611 views from 24 staff accounts.")
s1=section("marketplace","The core product",TEAL,
    'Marketplace — <span class="hl" style="background:'+TEAL+'33">app.ondiem.com</span>',
    "Where practices post shifts and professionals get booked. The weekly rhythm is unchanged. What moved this period is the device mix and where the traffic is credited.",
    s1_tiles+plat_area+plat_funnels+promo+'<div class="grid2">'+plat_device+plat_sources+'</div>'+plat_pages)

# ============ SECTION 2: MARKETING SITE ============
s2_tiles=tiles([
    ("14,657","Page views",BLUE),
    ("94.7%","Organic + direct",NAVY),
    ("46","Views from social",RED,"from 51 posts"),
    ("5","Form submissions",RED,"from 230 starts"),
])
site_channels=chart_card("Traffic by channel",
    hbars([("Organic Search",8017,GREEN),("Direct",5868,NAVY),("Referral",521,TEAL),("Paid Search",183,ORANGE),
           ("Organic Social",46,PINK),("Email",12,PURPLE),("AI Assistant",7,BLUE)]),
    "Search and direct carry 94.7% of traffic. Paid is small here because the ads point at hub.ondiem.com, not this site.")
site_pages=chart_card("Top pages",
    hbars([("Home /",9590,NAVY),("/professionals",3070,PINK),("/practices",501,TEAL),("/ondiem-darby",381,GREEN),
           ("/contact-us",232,ORANGE),("/ada",162,PURPLE)]),
    "Home and the professional page are 86% of views. /practices is far smaller but far more engaged.")
site_trend=chart_card("Daily traffic",
    area(site_days, day_labels, color=BLUE),
    "A clean weekday pattern with weekend dips. Absolute daily values are not comparable to last period — that export captured roughly 75% of pages per day against 97% here.")
site_mobile=chart_card("Mobile vs desktop by page",
    vbars([("Home\nmobile",5607,PINK),("Home\ndesktop",3944,BLUE),("Pros\nmobile",2617,PINK),("Pros\ndesktop",428,BLUE)],
          fmt=lambda v:f"{v:,}"),
    "Professionals arrive on mobile at roughly 6:1. The site is 60.7% mobile — the mirror image of the platform.")

form_call=card('<h3 class="ctitle" style="color:'+RED+'">230 form starts. 5 submissions.</h3>'
    '<p class="csub">The site&rsquo;s only direct conversion action completes at roughly 2%.</p>'
    +funnel([("Began a form on ondiem.com","230",BLUE),("Completed and submitted","5",RED)])+
    '<p class="fnote">This is a known defect, not a new finding. Form errors on ondiem.com and ondiem.com/darby have been an open item in the '
    'Figment&ndash;onDiem working notes since July; the pro app currently takes engineering priority and the fix is logged in Jira for later pickup. '
    'For context, <code>pro_availability_view</code> drew <b>2,510 users</b> across the same period. The site engages people. The handoff is where it stops.</p>')

site_partners=card('<h3 class="ctitle">Referral traffic = partnerships</h3><p class="csub">The referral channel is almost entirely dental partners and associations.</p>'
    '<div class="tags">'+''.join(f'<span class="tag">{esc(t)}</span>' for t in
    ["Darby Dental","CDHA","ADA Business","AADOM","BroadcastMed","MDA Programs","Sonrava Health"])+'</div>')
s2=section("website","Brand & acquisition",BLUE,
    'Marketing site — <span class="hl" style="background:'+BLUE+'33">ondiem.com</span>',
    "The public-facing site, powered by search and brand. Traffic held steady. The conversion path did not.",
    s2_tiles+'<div class="grid2">'+site_channels+site_pages+'</div>'+form_call+'<div class="grid2">'+site_trend+site_mobile+'</div>'+site_partners)

# ============ SECTION 3: PAID SEARCH ============
s3_tiles=tiles([
    ("$1,555","Spend",ORANGE),
    ("1,667","Clicks",NAVY),
    ("50.2%","CTR",TEAL),
    ("$0.93","Avg. CPC",GREEN),
    ("0.02","Conversions tracked",RED),
])
paid_trend=chart_card("Daily clicks — demand peaks Monday and Tuesday",
    area(paid_days, day_labels, color=ORANGE),
    "The paid curve tracks the marketplace curve. Mondays run 79–90 clicks against 16–27 on Sundays.")
paid_device=chart_card("Clicks by device",
    donut([("Mobile",946,PINK),("Desktop",705,NAVY),("Tablet",16,YELLOW)],"57%","mobile"),
    "Mobile carries the majority of paid clicks and runs a +49% bid adjustment.")
auction=chart_card("Auction insights — impression share on brand terms",
    hbars([("onDiem",64.71,TEAL),("Teero",40.63,PINK),("Cloud Dentistry",32.57,PURPLE),("GoTu",16.91,BLUE),
           ("Direct Dental",10.0,MUTED),("Princess Dental",10.0,MUTED),("Job Medley",10.0,MUTED)],
          maxv=70, unit="%", fmt=lambda v:f"{v:.1f}"),
    "onDiem holds 64.7% impression share and 77.2% absolute top-of-page on its own name. Bars marked 10% are reported by Google as “< 10%”.")
paid_note=card('<h3 class="ctitle">Two corrections worth carrying forward</h3>'
    '<p class="fnote"><b>Auction insights were read inverted last period.</b> In Google Ads, <i>outranking share</i> on a competitor row means how often '
    '<b>onDiem</b> ranked above <b>them</b>. onDiem outranks Teero 59.4% of the time and Teero appears above onDiem 18.9% of the time when both show. '
    'The brand position is strong, not under pressure. The competitor set has however doubled from three to six.</p>'
    '<p class="fnote"><b>Paid&rsquo;s share of platform traffic is overstated.</b> Platform GA4 credits google/cpc with 7,321 sessions; Google Ads recorded 1,667 clicks — '
    'a factor of 4.4. GA4 sessions carry their original source across return visits, so much of that 16.5% is returning users who first arrived via an ad. '
    'Separately, 1,567 of 1,615 attributed clicks land on <b>hub.ondiem.com</b>, which sits outside both GA4 properties in this report.</p>')
s3=section("paid","Paid media",ORANGE,
    'Paid search — <span class="hl" style="background:'+ORANGE+'33">brand defence</span>',
    "One campaign, $50 a day, two phrase-match keywords on the brand name. The geo campaigns are not paused — they no longer exist in the account.",
    s3_tiles+'<div class="grid2">'+paid_trend+paid_device+'</div>'+auction+paid_note)

# ============ SECTION 4: AI VISIBILITY ============
s4_tiles=tiles([
    ("15%","Share of voice",PURPLE,"4th of six brands"),
    ("36.0","Visibility score",RED,"from 43.3"),
    ("5.6%","Citations from owned pages",TEAL),
    ("16","Google reviews",GREEN,"from 9 · rating 4.3"),
])
sov=chart_card("Share of voice across AI answers",
    hbars([("GoTu",21,BLUE),("Cloud Dentistry",19,PURPLE),("Kwikly",17,MAUVE),("onDiem",15,TEAL),
           ("Toothio",13,ORANGE),("Stynt",6,MUTED)], maxv=24, unit="%", fmt=lambda v:f"{v:g}"),
    "onDiem sits fourth of six brands tracked.")
vis_trend=chart_card("Visibility over six weekly snapshots",
    mline([("onDiem",[43.3,43.8,36.2,41.0,31.4,36.0],TEAL),
           ("GoTu",[50.0,50.5,50.0,59.0,51.4,52.0],BLUE),
           ("Cloud Dentistry",[40.0,43.8,48.1,46.7,46.7,47.0],PURPLE),
           ("Kwikly",[46.7,41.4,39.5,47.6,41.9,48.0],MAUVE),
           ("Princess Dental",[3.3,11.0,10.0,12.4,16.7,22.0],PINK)],
          ["Jun 28","Jul 5","Jul 12","Jul 19","Jul 26","Aug 2"], maxv=65, hi="onDiem"),
    "onDiem is the only brand in the top four trending down. Princess Dental Staffing rose from 3.3 to 22 over the same six weeks.")
engines=chart_card("Visibility by engine",
    pairbars([("ChatGPT",60.0,33.3,PINK),("Gemini",50.0,50.0,TEAL),("Perplexity",20.0,20.0,BLUE)],
             unit="%"),
    "The decline is concentrated in ChatGPT, which roughly halved. Gemini is the strongest engine and is holding. Perplexity is the weakest and flat.")
cite_mix=chart_card("Where AI answers source their citations",
    pairbars([("Peer / directory",51.8,37.5,BLUE),("Competitor-owned",22.5,32.4,PINK),("Earned",12.9,12.6,GREEN),
              ("Review sites",4.0,6.8,YELLOW),("Owned",3.6,5.6,TEAL),("UGC",5.2,5.1,MAUVE)],
             unit="%"),
    "Neutral directory sources fell while competitor-owned pages rose by ten points. Answers are increasingly sourced from pages competitors wrote about themselves.")
owned=chart_card("Most-cited onDiem pages",
    hbars([("ondiem.com",231,TEAL),("hub / ondiem-darby",45,GREEN),("hub.ondiem.com",29,BLUE),
           ("ondiem.com/ada",25,PURPLE),("hub / ba_practice",18,MAUVE),("hub / care-benefits-adha",16,PINK)]),
    "Partnership content is the strongest asset here. ada.org itself contributes a further 134 earned citations.")
aeo_note=card('<h3 class="ctitle">Reviews are moving. Visibility is not — yet.</h3>'
    '<p class="fnote">The automated review request has taken Google from <b>9 reviews at 3.7</b> to <b>16 at 4.3</b> after roughly a year of none, and review sites '
    'account for 6.8% of citations. Those two facts sit next to each other but should not yet be joined: onDiem&rsquo;s visibility <i>fell</i> from 43.3 to 36.0 over the '
    'same weeks. Two months of review activity cannot move a citation base this quickly. Treat reviews as a position being rebuilt, not as a lever already pulled.</p>'
    '<p class="fnote">Two open items affect this section directly. The app store listing sits at <b>5 reviews and 1.8</b> and the automation does not currently point at it. '
    'And two Google Business accounts remain unmerged, which splits the review count.</p>')
s4=section("aeo","Discovery",PURPLE,
    'Visibility in <span class="hl" style="background:'+PURPLE+'33">AI answers</span>',
    "How often onDiem appears when the AI engines answer questions about dental staffing, and which sources they draw on. Measured Jun 29 &ndash; Aug 6, so slightly wider than the rest of this report.",
    s4_tiles+'<div class="grid2">'+sov+engines+'</div>'+vis_trend+'<div class="grid2">'+cite_mix+owned+'</div>'+aeo_note)

# ============ SECTION 5: SOCIAL ============
s5_tiles=tiles([
    ("8,881","Total followers",PURPLE,"IG + FB + LinkedIn"),
    ("15.6K","Instagram views",PINK,"up from ~6K"),
    ("81%","Views from non-followers",BLUE),
    ("46","Site visits from social",RED,"from 51 posts"),
])
ig_type=chart_card("Instagram views by content type",
    hbars([("Carousel",8148,GREEN),("Reel",5846,PINK),("Post",985,PURPLE),("Story",793,BLUE)]),
    "Account-level views, which include back-catalogue content still circulating. Carousel took the top slot on the strength of a single Jul 30 post that drew 6,292 views on hashtag distribution.")
ig_int=chart_card("Instagram interactions by content type",
    hbars([("Reel",186,PINK),("Post",137,PURPLE),("Story",36,BLUE)]),
    "Reels lead on interactions despite lower view volume. The Jul 30 carousel engaged at 0.91% — the lowest of any content this period.")
li_tbl=table(
    ["LinkedIn post","Format","Impressions","Clicks","Eng."],
    [["Better days in dentistry","Document","97","22","24.7%"],
     ["Staff retention","Multi-image","278","3","4.3%"],
     ["Booth 1014 preview","Video","147","5","6.8%"],
     ["Keep your eyes peeled","Image","142","5","4.9%"],
     ["Dental Assistant Palooza","Multi-image","130","2","3.1%"],
     ["RDH enamel pin tease","Image","97","2","4.1%"]],
    hi_cols=[3], hi_color=GREEN)
li=card('<h3 class="ctitle">LinkedIn: the document format leads again</h3>'
    '<p class="csub">One post produced 22 of the 39 post-level clicks from a third of the impressions of the next-largest post.</p>'
    +li_tbl+
    '<p class="fnote">This is the second consecutive period in which document and carousel formats out-converted every other format on LinkedIn. '
    'Two periods with the same result makes it a pattern worth building on rather than an outlier. Account-level clicks nonetheless fell from 155 to 118 across the same six-post cadence.</p>')
comp=chart_card("Instagram followers vs competitors",
    pairbars([("Princess Dental",8370,9738,PINK),("Teero",3160,3392,BLUE),("onDiem",3099,3109,TEAL),("Kwikly",2430,2450,MAUVE)],
             fmt=lambda v:f"{v:,.0f}"),
    "Princess Dental Staffing grew roughly 16% in a month. onDiem grew 0.3%. Windows overlap, so treat the magnitudes loosely and the direction seriously.")
fb=card('<h3 class="ctitle">Facebook</h3>'
    '<p class="fnote">3,604 followers, with <b>2 acquired against 7 lost</b> — a third consecutive period of decline on a page receiving the same creative as Instagram. '
    'Three posts, two reels and fourteen stories produced 733 and 737 views respectively, 27 reactions and 21 clicks.</p>')
social_note=card('<h3 class="ctitle">Reach roughly tripled. Followers grew by 37.</h3>'
    '<p class="fnote">Instagram views went from about 6,000 to 15.56K, and <b>12.75K of those views came from non-followers</b> against 2,965 from followers — 81%, up from '
    'roughly 57% last period. Hashtag distribution is putting the brand in front of two and a half times more people. '
    'Across 51 pieces of content on three platforms, organic social sent <b>46 visits</b> to ondiem.com.</p>')
s5=section("social","Owned social",PINK,
    'Social — <span class="hl" style="background:'+PINK+'33">reach without handoff</span>',
    "Instagram, Facebook and LinkedIn. Distribution improved sharply. What follows distribution did not.",
    s5_tiles+'<div class="grid2">'+ig_type+ig_int+'</div>'+social_note+li+'<div class="grid2">'+comp+fb+'</div>')

# ============ SECTION 6: LINK TRACKING ============
s6_tiles=tiles([
    ("502","Short.io clicks",TEAL,"Jul 7 – Aug 5"),
    ("257","On Jul 24 alone",ORANGE,"ADA email send"),
    ("54%","Human clicks",RED,"from 69%"),
    ("296","ADA email link",PURPLE,"largest path"),
])
short_chart=chart_card("Daily short-link clicks",
    area(short_days, day_labels, color=TEAL, hi_idx=[17]),
    "Jul 22 and 23 recorded nothing, then Jul 24 produced 257 clicks — over half the window in one day, almost certainly the monthly ADA email. Excluding it, the median day is 5 clicks.")
short_note=card('<h3 class="ctitle">Bot traffic is rising</h3>'
    '<p class="fnote">Human clicks fell to <b>54.0%</b> of total from 69.1% last period. The geography explains it: Ashburn 165, Columbus 51, Singapore 40, '
    'the Netherlands 33, China 31 — datacentre and scanner traffic rather than dental practices. Per-day human figures on this chart are extrapolated from the '
    'domain-level rate, as Short.io reports the human/bot split only at domain level.</p>'
    '<p class="fnote">The <code>/ada-email</code> path carries 296 of the 502 clicks and the <code>ada_partnership_2025</code> campaign 293. '
    'The previous export showed a comparable spike on Jun 24. Two points is not a cadence, but a third would make it one.</p>')
s6=section("links","Partnerships",GREEN,
    'Link tracking — <span class="hl" style="background:'+GREEN+'33">Short.io</span>',
    "Tracked short links, almost entirely the ADA partnership programme.",
    s6_tiles+short_chart+short_note)

# ============ SECTION 7: EMAIL, SURVEY & EVENT ============
s7_tiles=tiles([
    ("701","Practices emailed",GREEN,"six cities, Aug 5"),
    ("10.8%","Open rate",NAVY,"24 hours after send"),
    ("22","Survey responses",TEAL,"of 1,050 · from 14"),
    ("4","RDH event sign-ups",RED,"1.12% of leads"),
])
promo_tbl2=table(
    ["City","Delivered","Unique opens","Open rate","Clicks"],
    [["Portland","268","32","11.9%","2"],
     ["Minneapolis","166","11","6.6%","0"],
     ["Chicago","151","19","12.6%","0"],
     ["Atlanta","60","8","13.3%","0"],
     ["Houston","40","5","12.5%","0"],
     ["Miami","16","1","6.3%","0"],
     ["Total","701","76","10.8%","2"]],
    hi_cols=[4], hi_color=PINK)
promo_card=card('<h3 class="ctitle">August gift-card promo — first 24 hours</h3>'
    '<p class="csub">One creative, city name swapped, sent Aug 5 — the last day of the window.</p>'
    +promo_tbl2+
    '<p class="fnote">These numbers will move and should not be read as final. More importantly, <b>clicks are the wrong measure here</b>: the offer redeems on a promo '
    'code entered at shift creation, so a practice can convert without ever clicking. The May/June mailer took until August for its last timecards to clear, '
    'so this campaign&rsquo;s real result lands two reports from now.</p>'
    '<p class="fnote">Two setup notes for the next batch. The promo codes are identical across all six cities, so a booked shift cannot be traced back to a market — '
    'city-suffixed codes would answer whether the digital send reproduces the physical mailer&rsquo;s Portland and Minneapolis pattern. '
    'And the UTM medium was written four different ways across the six sends, which will split the campaign in GA4.</p>')
event=card('<h3 class="ctitle">RDH Under One Roof — nurture result</h3>'
    +funnel([("Unique pros captured at the event","451",PURPLE),
             ("Without an onDiem account — the opportunity","362",PURPLE),
             ("Signed up after the nurture sequence","4",RED)])+
    '<p class="fnote">Four sign-ups, 1.12%, with two arriving after the third and fourth emails. One SMS and two emails remain in the workflow. '
    'Against 451 leads from a single event, this is the clearest evidence in the report that lead volume is not the constraint.</p>'
    '<p class="fnote">The practice survey now stands at <b>22 responses from 1,050</b>, up from 14 after the second send.</p>')
s7=section("email","Lifecycle",GREEN,
    'Email, survey &amp; <span class="hl" style="background:'+GREEN+'33">event conversion</span>',
    "Direct outreach to practices and professionals, and what the RDH Under One Roof nurture ultimately produced.",
    s7_tiles+promo_card+event)

# ============ SECTION 8: PROFILE COMPLETION ============
s8=section("profiles","Supply quality",TEAL,
    'Profile <span class="hl" style="background:'+TEAL+'33">completion</span>',
    "Professional profile completeness across the marketplace.",
    tiles([("152","Clicks — round one",TEAL),("89","Clicks — round two",TEAL),
           ("765","Pros tracked",NAVY,"carried forward"),("15.6%","Fully complete",PINK,"carried forward")])+
    card('<p class="fnote">Completion figures for this round are pending. The baseline above is carried forward from the previous report, where 765 professionals were '
         'tracked at 15.6% fully complete, with Personal Bio missing for 65.8%. '
         'Round-two clicks fell 41% against round one, which may reflect a smaller remaining pool rather than fatigue — the completion counts will distinguish the two. '
         'Last period the gap between 83 clicks and 41 completions was the finding, not the click count, and the same will apply here.</p>'))

# ============ TAKEAWAYS ============
take=callout("What this means for next period",[
    "<b>Reach improved almost everywhere. Every handoff held flat or leaked.</b> Instagram views roughly tripled with 81% from non-followers, "
    "onDiem appears across three AI engines, and paid holds 64.7% impression share on its own name. Against that: 230 form starts produced 5 submissions, "
    "51 social posts produced 46 site visits, AI visibility produced 7, and a 451-lead event produced 4 sign-ups.",
    "<b>The one thing that converted was the gift-card mailer.</b> 15 confirmed shifts from roughly eight practices, all in Portland and Minneapolis, "
    "driven by repeat posting from accounts that already existed. The August digital version targets those two markets among six.",
    "<b>Fix the forms before adding more traffic to them.</b> The 2% completion rate is a known defect already logged behind the pro app. "
    "Every channel in this report routes to a site whose only conversion action is broken.",
    "<b>Give the August promo a measurable outcome.</b> City-suffixed promo codes and a single UTM medium would let the next report attribute booked shifts to a market. "
    "Neither change costs anything and both must happen before the next send.",
    "<b>Close the measurement gap at hub.ondiem.com.</b> It receives the paid traffic and the AI citations and sits outside both GA4 properties. "
    "Platform GA4 also credits paid with 4.4&times; the sessions Google Ads recorded.",
    "<b>Watch Princess Dental Staffing.</b> Three separate appearances this period — 16% Instagram growth, new to the brand-term auction, "
    "and AI visibility from 3.3 to 22.",
], kicker="TAKEAWAYS")


# ============ ASSEMBLE ============
nav=('<nav class="toc"><a href="#updates">Updates</a><a href="#marketplace">Marketplace</a><a href="#website">Website</a>'
     '<a href="#paid">Paid</a><a href="#aeo">AI visibility</a><a href="#social">Social</a>'
     '<a href="#links">Links</a><a href="#email">Email</a><a href="#profiles">Profiles</a></nav>')

header=(f'<header class="masthead"><div class="mh-top"><span class="brand">'
        f'<span class="brand-mark">&#9681;</span> onDiem</span><span class="period">30-DAY VIEW &middot; JUL 7 &ndash; AUG 5, 2026</span></div>'
        f'<h1 class="title">Marketing Performance <span class="hl" style="background:{TEAL}44">Report</span></h1>'
        f'<p class="subtitle">A single view across the marketplace, marketing site, paid search, AI visibility, social, partnerships, email and profile quality. Prepared by Figment Creative.</p>'
        f'{nav}</header>')

body=(header+
      f'<section class="hero"><div class="sec-head">{eyebrow("At a glance", NAVY)}'
      f'<h2 class="sec-title">The period in six numbers</h2></div>{hero_tiles}</section>'+
      s0+s1+s2+s3+s4+s5+s6+s7+s8+
      f'<section>{take}</section>'+
      f'<footer class="foot">onDiem Marketing Performance Report &middot; Reporting window Jul 7 &ndash; Aug 5, 2026 &middot; AI visibility measured Jun 29 &ndash; Aug 6 &middot; Sources: GA4, Metricool, Google Ads, Short.io, HubSpot &middot; Internal use</footer>')

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
