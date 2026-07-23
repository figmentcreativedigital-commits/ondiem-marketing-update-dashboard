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

# ================= BUILD =================
P=[]

# ---- daily platform active users (Time_series4) ----
plat_days=[5158,988,1040,991,699,249,412,4020,834,802,845,411,191,331,4012,890,799,844,580,263,345,3852,1067,929,873,593,250,281,4123,1203]
day_labels=["Jun 22","","","Jun 25","","","Jun 28","","","Jul 1","","","Jul 4","","","Jul 7","","","Jul 10","","","Jul 13","","","Jul 16","","","Jul 19","","Jul 21"]
mondays=[0,7,14,21,28]

# ---- marketing site daily totals ----
site_days=[578,613,502,503,448,202,313,596,481,469,364,261,158,288,508,418,390,423,256,199,306,489,384,381,395,287,169,197,401,427]

# ---- Short.io daily clicks (Jun 23 - Jul 23) ----
short_days=[22,700,50,8,11,51,46,9,365,34,6,13,6,10,3,9,12,41,7,8,5,1,5,12,8,3,16,25,14,3,0]
_sd=[("Jun",d) for d in range(23,31)]+[("Jul",d) for d in range(1,24)]
short_labels=[f"{m} {d}" for m,d in _sd]

# ============ HERO ============
hero_tiles=tiles([
    ("29,862","Platform active users",TEAL,"app.ondiem.com · 30 days"),
    ("1,294","Shift confirmations",GREEN,"confirmation events (GA4)"),
    ("567","New pros signed up",PINK,"registration completed"),
    ("15,288","Marketing site views",BLUE,"ondiem.com"),
    ("8,872","Total social followers",PURPLE,"IG + FB + LinkedIn"),
    ("$1,523","Paid search spend",ORANGE,"Google Ads, brand"),
])

# ============ SECTION 1: MARKETPLACE ============
s1_tiles=tiles([
    ("29,862","Active users",TEAL),
    ("290K","Page views",NAVY),
    ("2,844","Pros signed in",PINK),
    ("1,406","Practices signed in",BLUE),
    ("1,294","Shift confirmations",GREEN,"GA4 events"),
])
plat_area=chart_card("Daily active users — the weekly Monday spike",
    area(plat_days, day_labels, color=TEAL, hi_idx=mondays),
    "Active users surge to 3,800–5,200 every Monday (▲ marked), then fall midweek and into the weekend (Jul 4 low = 191). The marketplace runs on a weekly shift-posting cycle.")
plat_practice=funnel([
    ("Listings created — by 627 practices","2,641",TEAL),
    ("Shift-creation flows started","1,721",TEAL),
    ("Shift offers sent to pros (largely automated)","142,674",TEAL),
    ("Shift confirmations (GA4 event)","1,294",GREEN),
])
plat_pro=funnel([
    ("Job searches — by 3,153 pros","9,643",PINK),
    ("Shifts viewed — by 6,692 pros","15,979",PINK),
    ("Shift requests submitted — by 370 pros","2,766",PINK),
])
plat_funnels=card(
    '<h3 class="ctitle">Two-sided marketplace funnel</h3>'
    '<div class="twocol">'
    f'<div><div class="fhead" style="color:{TEAL}">PRACTICE SIDE — posting &amp; booking</div>{plat_practice}</div>'
    f'<div><div class="fhead" style="color:{PINK}">PROFESSIONAL SIDE — finding work</div>{plat_pro}</div>'
    '</div>'
    '<p class="fnote">Figures are GA4 <b>event counts</b>, not verified database bookings. '
    '‘Shift confirmations’ (<code>temp_shift_confirmed</code>) fired 1,294× from just 32 accounts, and shift offers from 64 — '
    'both are driven by a small number of practice-admin or automated senders, so they indicate activity volume rather than unique completed shifts.</p>')
plat_device=chart_card("Device — desktop-first",
    donut([("Desktop",22257,NAVY),("Mobile",7549,PINK),("Tablet",56,YELLOW)],"75%","desktop"),
    "The opposite of the marketing site: practice staff and admins work at the front desk on Windows/desktop.")
plat_sources=chart_card("How users reach the platform",
    hbars([("Direct (logged-in)",63.0,NAVY),("Google — paid (CPC)",14.8,ORANGE),("Internal navigation",11.6,TEAL),("Google — organic",4.0,GREEN),("Email + SMS re-engagement",2.5,PINK)],
          maxv=70, unit="%", fmt=lambda v:f"{v:g}"),
    "63% is returning logged-in traffic. Paid search matters far more here than on the marketing site.")
plat_pages=chart_card("Most-used pages",
    hbars([("/login",20779,NAVY),("/results",17332,PINK),("/search",13889,TEAL),("/my-jobs",12285,BLUE),
           ("/timesheets",8244,GREEN),("/dashboard",8142,PURPLE),("/employee-portal",6263,ORANGE),("/registration",4129,MAUVE)],
          fmt=lambda v:f"{v:,}"),
    "Job discovery (results/search), My-Jobs, Timesheets and per-practice booking calendars carry the volume.")
s1=section("marketplace","The core product",TEAL,
    'Marketplace — <span class="hl" style="background:'+TEAL+'33">app.ondiem.com</span>',
    "Where practices post shifts and professionals get booked. Desktop-first, sticky (1–13% bounce on logged-in pages), and driven by a strong weekly rhythm.",
    s1_tiles+plat_area+plat_funnels+'<div class="grid2">'+plat_device+plat_sources+'</div>'+plat_pages)

# ============ SECTION 2: MARKETING SITE ============
s2_tiles=tiles([
    ("15,288","Page views",BLUE),
    ("96%","Organic + direct",NAVY),
    ("52","Views from social",RED,"the weak link"),
    ("90–165","Availability views / day",TEAL),
])
site_channels=chart_card("Traffic by channel",
    hbars([("Organic Search",8379,GREEN),("Direct",6208,NAVY),("Referral",446,TEAL),("Paid Search",179,ORANGE),
           ("Organic Social",52,PINK),("Email",12,PURPLE),("AI Assistant (ChatGPT)",7,BLUE)]),
    "SEO and brand/direct carry 96% of traffic. The active social + email programs send almost no one to the site.")
site_pages=chart_card("Top pages",
    hbars([("Home /",9686,NAVY),("/professionals",3123,PINK),("/practices",516,TEAL),("/ondiem-darby",317,GREEN),
           ("/ada",304,PURPLE),("/contact-us",252,ORANGE)]),
    "Home and the professional (job-seeker) page are ~84% of views; /practices is smaller but far more engaged (~148s sessions).")
site_trend=chart_card("Daily traffic",
    area(site_days, day_labels, color=BLUE),
    "Clean weekday pattern with weekend / holiday dips (Jul 4 lowest).")
site_mobile=chart_card("Mobile vs desktop by page",
    vbars([("Home\nmobile",5624,PINK),("Home\ndesktop",4007,BLUE),("Pros\nmobile",2690,PINK),("Pros\ndesktop",394,BLUE)],
          fmt=lambda v:f"{v:,}"),
    "Professionals are overwhelmingly mobile (~7:1); practices skew desktop.")
site_partners=card('<h3 class="ctitle">Referral traffic = partnerships</h3><p class="csub">The referral channel is almost entirely dental partners and associations.</p>'
    '<div class="tags">'+''.join(f'<span class="tag">{esc(t)}</span>' for t in
    ["Darby Dental","CDHA","ADA Business","AADOM","BroadcastMed","MDA Programs","RDH UOR"])+'</div>')
s2=section("website","Brand & acquisition",BLUE,
    'Marketing site — <span class="hl" style="background:'+BLUE+'33">ondiem.com</span>',
    "The public-facing site. Mobile-first and built for the professional audience, powered by search and brand — not by social or email.",
    s2_tiles+'<div class="grid2">'+site_channels+site_pages+'</div>'+'<div class="grid2">'+site_trend+site_mobile+'</div>'+site_partners)

# ============ SECTION 2B: SHORT.IO LINK TRACKING ============
sh_tiles=tiles([
    ("2,202","Total link clicks",GREEN,"down 16% vs prior 30d"),
    ("1,521","Human clicks",TEAL,"down 21% · ~31% are bots"),
    ("1,083","ADA email link clicks",PINK,"49% of all clicks"),
    ("0","New short links created",NAVY),
])
sh_links=chart_card("Top branded links",
    hbars([("/ada-email",1083,PINK),("/* (other)",254,MAUVE),("/ (root)",86,BLUE),("/ada-website",49,TEAL),
           ("/website",12,GREEN),("/ada-member-advantage",10,PURPLE),("/onDiem-youtube",8,ORANGE)]),
    "The ADA partnership email link (campaign ada_partnership_2025) is ~half of all clicks. These links point to varied destinations — ADA, partner pages, YouTube — not only ondiem.com.")
sh_daily=chart_card("Daily clicks",
    area(short_days, short_labels, color=GREEN, hi_idx=[1,8]),
    "Two email-driven spikes — Jun 24 (700) and Jul 1 (365) — then a long tail, with no new links created in the window.")
sh_quality=chart_card("Human vs. automated clicks",
    donut([("Human clicks",1521,GREEN),("Bots / scanners",681,MUTED)],"69%","human"),
    "~31% of clicks are non-human. The top ‘city’ is Ashburn, VA (628 — an AWS data-center hub) and clicks appear from China, the Netherlands and Singapore — typical email security-scanner traffic. Read the human-click figure, not the raw total.")
s_short=section("links","Link tracking",TEAL,
    'Branded links — <span class="hl" style="background:'+GREEN+'33">Short.io (ondiem.co)</span>',
    "Click performance on onDiem's branded short links — mostly campaign, email and partnership links. Window Jun 23 – Jul 24, 2026.",
    sh_tiles+'<div class="grid2">'+sh_links+sh_daily+'</div>'+sh_quality)

# ============ SECTION 3: PAID SEARCH ============
s3_tiles=tiles([
    ("$1,523","Ad spend",ORANGE),
    ("1,529","Clicks",PINK),
    ("49.3%","Click-through rate",GREEN),
    ("~$1.00","Cost per click",TEAL),
    ("0","Conversions tracked",RED,"measurement gap"),
])
paid_kw=chart_card("Spend is 100% brand defense",
    hbars([('"ondiem"',1147.86,ORANGE),('"on diem"',375.52,YELLOW),
           ("Generic keywords (staffing, hire RDH…)",0,MUTED)],
          maxv=1200, unit="", fmt=lambda v:f"${v:,.0f}"),
    "All spend went to navigational brand searches. The generic acquisition keywords are enabled but not serving, and the geo web-traffic campaigns (Atlanta/Houston/Chicago/Miami, ~$1,300 last month) are now at $0.")
paid_dow=chart_card("Demand by day of week",
    vbars([("Sun",238,MUTED),("Mon",775,ORANGE),("Tue",771,ORANGE),("Wed",501,YELLOW),("Thu",421,YELLOW),("Fri",239,MUTED),("Sat",157,MUTED)],
          fmt=lambda v:f"{v:,}"),
    "Impressions peak Monday–Tuesday and in the 7–10 AM window — the same rhythm as the marketplace.")
paid_auction=chart_card("Auction insights — competitors bid on your brand",
    table(["Advertiser","Impr. share","Outranks onDiem","Top of page"],
        [["onDiem (You)","61.4%","—","87.4%"],
         ["teero.com","48.6%","55.7%","93.0%"],
         ["clouddentistry.com","23.7%","58.6%","87.5%"],
         ["gotu.com","19.6%","59.8%","83.5%"],
         ["princessdentalstaffing.com","<10%","60.9%","80.2%"],
         ["directdental.com","<10%","60.8%","59.6%"]],
        aligns=["left","right","right","right"], hi_cols=[2], hi_color=RED),
    "Teero shows alongside onDiem 53% of the time and outranks it in 55.7% of shared auctions — active brand-term competition.")
paid_device=chart_card("Paid clicks by device",
    donut([("Mobile phones",873,PINK),("Computers",641,NAVY),("Tablets",15,YELLOW)],"57%","mobile"),
    "Mobile takes the larger share of paid spend and clicks; audience is 85% female, ages 25–54.")
s3=section("paid","Paid media",ORANGE,
    'Paid search — <span class="hl" style="background:'+ORANGE+'33">Google Ads</span>',
    "A lean, brand-protective account. Efficient on brand terms, but pulled back from prospecting and unable to measure conversions.",
    s3_tiles+paid_kw+'<div class="grid2">'+paid_dow+paid_device+'</div>'+paid_auction)

# ============ SECTION 4: SOCIAL ============
s4_tiles=tiles([
    ("8,872","Total followers",PURPLE),
    ("3,099","Instagram ▲25",PINK),
    ("3,608","Facebook ▼3",BLUE),
    ("2,165","LinkedIn ▲5",TEAL),
])
soc_ct=chart_card("Instagram views by content type — reels dominate",
    hbars([("Reels",3483,PINK),("Posts",1016,MAUVE),("Carousels",774,GREEN),("Stories",769,BLUE),("Ads",4,ORANGE)]),
    "4 reels out-viewed 6 feed posts and drove the majority of interactions. Reel engagement (5.35%) beats feed posts (3.97%).")
soc_eng=chart_card("Engagement rate by channel & format",
    hbars([("LinkedIn (link posts)",25.1,TEAL),("Instagram reels",5.35,PINK),("Instagram posts",3.97,MAUVE),("Facebook posts",1.8,BLUE)],
          maxv=27, unit="%", fmt=lambda v:f"{v:g}"),
    "LinkedIn is the click engine — 6 posts produced 155 clicks; Instagram is the reach engine; Facebook lags.")
soc_top=chart_card("Top posts across platforms",
    table(["Post","Platform","Reach / Impr.","Result"],
        [["“We're officially at RDH…” reel (Jul 17)","Instagram","333","452 views · 10.2% eng"],
         ["“Hm… what could it be?” pin teaser (Jul 9)","Facebook","205","397 views"],
         ["“Summer means vacation…” doc (Jun 25)","LinkedIn","98","71 clicks · 74% eng"],
         ["“Got questions?” doc carousel (Jun 26)","LinkedIn","123","70 clicks · 59% eng"],
         ["“Got questions?” carousel (Jun 26)","Instagram","124","305 views"]],
        aligns=["left","left","right","right"], hi_cols=[3], hi_color=PINK),
    "The RDH Under One Roof event drove the top-reaching content on both Meta platforms; LinkedIn documents drove the clicks.")
soc_comp=chart_card("Instagram vs. competitors (followers)",
    hbars([("Princess Dental Staffing",8368,MUTED),("Teero",3159,MUTED),("onDiem",3099,PINK),("Kwikly",2431,MUTED)]),
    "onDiem sits mid-pack — ahead of Teero and Kwikly, behind Princess (which leans heavily on reels).")
soc_aud=card('<h3 class="ctitle">Audience — consistent across platforms</h3>'
    '<p class="csub">Predominantly female, ages 25–44, in US dental metros — matching the dental-hygienist ICP. LinkedIn adds a professional overlay.</p>'
    '<div class="tags">'+''.join(f'<span class="tag">{esc(t)}</span>' for t in
    ["84% female","Ages 25–44","NYC","LA / SF Bay","Dallas–Ft. Worth","Phoenix","Portland","Entry + Senior (LI)","IT · BizDev · Sales (LI)"])+'</div>')
s4=section("social","Owned social",PINK,
    'Social — <span class="hl" style="background:'+PINK+'33">Instagram · Facebook · LinkedIn</span>',
    "The RDH Under One Roof conference powered the period. Each platform plays a distinct role: Instagram for reach, LinkedIn for clicks, Facebook fading.",
    s4_tiles+'<div class="grid2">'+soc_ct+soc_eng+'</div>'+soc_top+'<div class="grid2">'+soc_comp+soc_aud+'</div>')

# ============ SECTION 5: EMAIL & SURVEY ============
s5_tiles=tiles([
    ("1,050","Emails delivered",BLUE),
    ("18.6%","Open rate",TEAL,"excl. bots"),
    ("28","Unique clicks",PINK),
    ("14","Survey responses",GREEN,"39% completion"),
])
em_funnel=chart_card("Email funnel — Practice First Shift Survey",
    hbars([("Delivered",1050,NAVY),("Unique opens",195,TEAL),("Unique clicks",28,PINK),("Replies",0,MUTED)]),
    "Clean deliverability (0 spam, 3 unsubscribes) but a narrow open→click step.")
em_mobile=chart_card("The mobile drop-off",
    vbars([("Mobile\nopens",39,PINK),("Mobile\nclicks",17,PINK),("Desktop\nopens",28,BLUE),("Desktop\nclicks",83,BLUE)],
          maxv=90, unit="%", fmt=lambda v:f"{v:g}%"),
    "Mobile drives 39% of opens but only 17% of clicks; desktop is the reverse. CTA/mobile friction is losing earned clicks.")
em_survey=card('<h3 class="ctitle">What practices told the survey</h3>'
    '<p class="csub">36 views → 14 responses (39%). Sentiment by topic:</p>'+
    table(["Topic","Practice sentiment"],
        [["Creating a shift","Easy to very easy"],
         ["Finding coverage","Softest area — limited local candidates, slow response"],
         ["Approving timecards","Mostly easy"],
         ["Cancellation policy","Polarizing — several strongly negative"],
         ["Overall satisfaction","Mid-scale — room to move to advocates"]],
        aligns=["left","left"]))
inflight=('<div class="inflight"><span class="if-tag">IN FLIGHT</span>'
    '<div><b>2nd follow-up sent Jul 22 — results pending.</b> A resend to non-responders '
    '(“What would make onDiem work better for you?”) that applies this report’s recommendations: '
    'benefit-led subject, a stated “2-minute” ask, and previewed questions. Open / click / response '
    'performance will appear in next period’s report.</div></div>')
s5=section("email","Lifecycle",GREEN,
    'Email &amp; survey — <span class="hl" style="background:'+GREEN+'33">Practice First Shift Survey</span>',
    "A single send to 1,053 practices, plus the resulting survey. Solid deliverability, but a mobile CTA gap and a clear message on where practices feel friction.",
    s5_tiles+'<div class="grid2">'+em_funnel+em_mobile+'</div>'+em_survey+inflight)

# ============ SECTION 5B: PROFESSIONAL FIRST-SHIFT FEEDBACK ============
vp_tiles=tiles([
    ("663","Pro responses",PINK,"cumulative, Oct '24–Jul '26"),
    ("91.6%","Shift went as expected",GREEN,"607 of 663"),
    ("39%","Haven't set availability",RED,"supply-activation gap"),
    ("GoTu","Top other platform pros use",ORANGE,"22.8% also on it"),
])
vp_exp=chart_card("Did the first shift go as expected?",
    donut([("Yes",607,GREEN),("No",50,RED)],"92%","said yes"),
    "A strong first-shift satisfaction signal — the marketplace largely delivers on the booking.")
vp_platforms=chart_card("Pros multi-home — other platforms they use",
    hbars([("GoTu",151,ORANGE),("Kwikly",68,MAUVE),("Cloud Dentistry",63,BLUE),("Princess Dental",31,PURPLE),("Tooth.io",25,TEAL)]),
    "Nearly half also list ‘other/none’, but GoTu is the clear rival — the same names that bid on onDiem's brand in Google Ads.")
vp_why=chart_card("When a shift wasn't as expected — why",
    hbars([("Didn't know their system/software",47,RED),("Shift shorter than booked",29,ORANGE),
           ("Shift longer than booked",19,YELLOW),("Work wasn't what I signed up for",6,MAUVE),("Lacked expected credentials",3,PURPLE)],
          maxv=50),
    "Unfamiliar practice software is the leading cause — an onboarding/prep opportunity.")
vp_q=chart_card("What pros ask about most",
    hbars([("Pay — when & how I get paid",25,PINK),("Scheduling / setting availability",19,TEAL),
           ("Getting more shifts / going full-time",17,GREEN),("Timecard approval & corrections",10,BLUE),
           ("App usability / confusion",9,PURPLE),("Onboarding (routing #, I-9)",6,ORANGE)]),
    "Pay is the #1 question by a wide margin — ‘when will I be paid?’, ‘is there same-day cash-out?’ — followed by how to set availability.")
vp_callout=callout("Two quick wins from the pro voice",[
    "<b>Make pay crystal-clear.</b> Payment timing and cash-out is the single most-asked question — a visible ‘when you'll be paid’ explainer at booking and in the app would deflect the most common friction.",
    "<b>Activate the 39% with no availability set.</b> Four in ten pros haven't marked their calendar, so practices can't find them — a targeted nudge directly grows bookable supply.",
], kicker="ACTIONABLE")
s5b=section("profeedback","Voice of the pro",PINK,
    'Professional first-shift feedback — <span class="hl" style="background:'+PINK+'33">663 responses</span>',
    "Cumulative feedback from professionals after their first onDiem shift (Oct 2024–Jul 2026). High satisfaction, clear friction points, and a direct read on what pros want.",
    vp_tiles+'<div class="grid2">'+vp_exp+vp_platforms+'</div>'+'<div class="grid2">'+vp_why+vp_q+'</div>'+vp_callout)

# ============ SECTION 6: CONVERSION ============
s6_tiles=tiles([
    ("451","Event leads",PURPLE),
    ("89","Already on onDiem",TEAL,"19.7%"),
    ("362","Opportunity to convert",PINK,"80.3%"),
    ("99.1%","Dental Hygienists",NAVY),
])
conv_donut=chart_card("Conversion opportunity",
    donut([("Opportunity to convert",362,PINK),("Already have an account",89,TEAL)],"362","to convert"),
    "4 in 5 professionals met at RDH Under One Roof don't yet have an onDiem account.")
conv_states=chart_card("Where the opportunity concentrates (unconverted pros by state)",
    hbars([("Maryland",61,PINK),("Virginia",47,PINK),("Pennsylvania",42,PINK),("Michigan",21,PURPLE),
           ("Texas",15,PURPLE),("Ohio",12,PURPLE),("Missouri",12,PURPLE),("Florida",11,PURPLE)]),
    "MD, VA and PA alone are 40%+ of the 362 unconverted professionals.")
conv_nurture=card('<h3 class="ctitle">Automated HubSpot nurture (drops anyone who converts)</h3>'+
    stepper(["SMS (Mon)","Email (Mon)","Call (+2d)","Email","Email","Email","SMS + 2 closing emails"]))
s6=section("conversion","Events & growth",PURPLE,
    'Event conversion — <span class="hl" style="background:'+PURPLE+'33">RDH Under One Roof 2026</span>',
    "The post-event contact list turned into a conversion pipeline. 451 clean leads, overwhelmingly hygienists, with a big untapped pool.",
    s6_tiles+'<div class="grid2">'+conv_donut+conv_states+'</div>'+conv_nurture)

# ============ SECTION 7: PROFILE COMPLETION ============
s7_tiles=tiles([
    ("765","Pros tracked",TEAL),
    ("15.6%","Fully complete",GREEN,"up from 13.7%"),
    ("65.8%","Missing a bio",PINK,"biggest gap"),
    ("2.79","Avg sections missing",NAVY,"was 2.88"),
])
pc_sms=chart_card("Profile-completion SMS funnel",
    hbars([("Received the SMS",528,NAVY),("Clicked the link",83,TEAL),("Completed ≥1 section",41,PINK)]),
    "83 clicked (15.7% CTR) but only 41 finished a section (72 sections total) — the click-to-completion gap is the thing to close. Profile Photo was the easiest win (23).")
pc_gaps=chart_card("Where the gaps live (% of pros missing)",
    vbars([("Photo",57,PINK),("Bio",65,NAVY),("Work\nExp",61,TEAL),("Educ.",55,GREEN),("Software",16,YELLOW),("Special.",20,PURPLE)],
          maxv=100, unit="%", fmt=lambda v:f"{v:g}%"),
    "Personal Bio, Work Experience and Profile Photo are the most-incomplete sections.")
pc_depth=chart_card("How many sections are pros missing?",
    vbars([("0\n(done)",119,GREEN),("1",110,YELLOW),("2",107,ORANGE),("3",85,ORANGE),("4",212,PINK),("5",70,PURPLE),("6",55,PURPLE)],
          maxv=230, fmt=lambda v:f"{v:,}"),
    "212 pros (~1 in 3) are still missing 4 of the 6 sections — the target for a dedicated ‘finish your profile’ nudge.")
pc_role=card('<h3 class="ctitle">Gap rate by role (% missing each section)</h3>'+
    table(["Role","Pros","Photo","Bio","Work Exp","Educ.","Software","Special."],
        [["Dental Assistant","363","59.5%","64.7%","60.3%","62.0%","15.7%","9.1%"],
         ["Dental Hygienist","344","52.9%","63.7%","62.2%","44.8%","12.8%","29.4%"],
         ["Dentist","28","75%","75%","64.3%","53.6%","32.1%","25%"],
         ["Office Staff","30","90%","93.3%","96.7%","93.3%","56.7%","50%"]],
        aligns=["left","right","right","right","right","right","right","right"], hi_cols=[2,3]))
s7=section("profiles","Supply quality",TEAL,
    'Pro profile completion — <span class="hl" style="background:'+TEAL+'33">765 professionals</span>',
    "Profile completeness before and after a nudge SMS. Completeness ticked up, but most pros still have real gaps — especially bios.",
    s7_tiles+'<div class="grid2">'+pc_sms+pc_gaps+'</div>'+'<div class="grid2">'+pc_depth+pc_role+'</div>')

# ============ TAKEAWAYS ============
take=callout("What this means for next week",[
    "<b>Time everything to Monday.</b> The marketplace and paid demand both peak Sunday-night into Monday–Tuesday mornings — schedule shift-supply pushes, emails and ad budget there.",
    "<b>Lean into reels and LinkedIn documents.</b> Reels drove 58% of Instagram views from a fraction of the posts, and LinkedIn document/carousel posts converted at 25%+ into clicks. That's the content mix to scale.",
    "<b>Close the social/email → site gap.</b> A large social effort produced just 52 website visits and email 12. The mobile email CTA and social link-in-bio paths are leaking the traffic they earn.",
    "<b>Coverage is the recurring pain.</b> ‘Finding coverage’ is practices' softest survey area and the supply answer is more hygienists — exactly the 362 warm RDH leads (MD/VA/PA) and the 212 incomplete pro profiles worth activating.",
    "<b>Protect the brand in paid search.</b> Teero outranks onDiem in 55.7% of shared brand auctions — and the same rivals (GoTu, Cloud) are the platforms pros multi-home on — while 0 conversions are tracked. Fix conversion measurement before reopening prospecting.",
    "<b>Answer ‘when do I get paid?’.</b> Pay is the #1 question in 663 first-shift responses despite 91.6% satisfaction — a visible pay-timing explainer is a cheap retention win.",
], kicker="WEEKLY TAKEAWAYS")

# ============ ASSEMBLE ============
nav=('<nav class="toc"><a href="#marketplace">Marketplace</a><a href="#website">Website</a>'
     '<a href="#links">Links</a><a href="#paid">Paid</a><a href="#social">Social</a><a href="#email">Email</a>'
     '<a href="#profeedback">Pro feedback</a><a href="#conversion">Conversion</a><a href="#profiles">Profiles</a></nav>')

header=(f'<header class="masthead"><div class="mh-top"><span class="brand">'
        f'<span class="brand-mark">◑</span> onDiem</span><span class="period">30-DAY VIEW · JUN 22 – JUL 21, 2026</span></div>'
        f'<h1 class="title">Weekly Performance <span class="hl" style="background:{TEAL}44">Report</span></h1>'
        f'<p class="subtitle">A single view across the marketplace, marketing site, paid search, social, email, event conversion and profile quality. Prepared by Figment Creative.</p>'
        f'{nav}</header>')

body=(header+
      f'<section class="hero"><div class="sec-head">{eyebrow("At a glance", NAVY)}'
      f'<h2 class="sec-title">The week in six numbers</h2></div>{hero_tiles}</section>'+
      s1+s2+s_short+s3+s4+s5+s5b+s6+s7+
      f'<section>{take}</section>'+
      f'<footer class="foot">onDiem Weekly Performance Report · Reporting window Jun 22 – Jul 21, 2026 (email &amp; profile reports as of Jul 20) · Sources: GA4, Metricool, Google Ads, HubSpot · Internal use</footer>')

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
