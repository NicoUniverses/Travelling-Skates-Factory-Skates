#!/usr/bin/env python3
"""Generate the static Travelling Skates site from the page data (raw.json)."""
import json, os, re, html, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = json.load(open(os.path.join(HERE, 'data', 'raw.json')))
OUT = sys.argv[1] if len(sys.argv) > 1 else 'site'
IMG_BASE = sys.argv[2] if len(sys.argv) > 2 else 'assets/img/'
SKIP = {'b', 'blog', 'single-post'}
SITE_NAME = 'TRAVELLING SKATES S.A.'
HOME_TITLE = 'TRAVELLING SKATES S.A. - FABRICANTE DE PRODUCTOS PARA EL PATINAJE'
HOME_DESC = 'Patinaje artístico, hockey sobre ruedas, roller derby. Ruedas, planchas, suspenciones , frenos. '

MASTER = RAW['_master']['json']
THEME = MASTER['data']['theme_data']['THEME_DATA']
COLORS = THEME['color']
FONTS = THEME['font']

PAGES = {}
for k, v in RAW.items():
    if k == '_master' or k in SKIP:
        continue
    PAGES[v['meta']['id']] = 'index.html' if k == 'home' else k + '.html'

IMAGES = {}


def img_name(uri):
    base, ext = os.path.splitext(uri)
    name = base.replace('~', '_') + ('.jpg' if ext.lower() in ('.jpeg', '.jpg') else ext.lower())
    IMAGES[uri] = name
    return name


def img_url(uri):
    return IMG_BASE + img_name(uri)


def color(v, alpha=1):
    if v is None:
        return 'transparent'
    v = str(v)
    m = re.match(r'\{?color_(\d+)\}?', v)
    if m:
        v = COLORS[int(m.group(1))]
    if alpha != 1 and v.startswith('#') and len(v) == 7:
        r, g, b = int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16)
        return f'rgba({r},{g},{b},{alpha})'
    return v


FONT_MAP = {
    'din-next-w01-light': "'Barlow', 'DIN Next', 'Helvetica Neue', Arial, sans-serif",
    'raleway': "'Raleway', sans-serif",
    'georgia': "Georgia, 'Times New Roman', serif",
    'arial': 'Arial, Helvetica, sans-serif',
}


def font_css(spec):
    if spec.startswith('font_'):
        spec = FONTS[int(spec[5:])]
    col = None
    m = re.search(r'\{(color_\d+)\}', spec)
    if m:
        col = color(m.group(1))
        spec = spec[:m.start()].strip()
    parts = spec.split()
    style, variant, weight, size = parts[0], parts[1], parts[2], parts[3]
    fam = ' '.join(parts[4:])
    fam = FONT_MAP.get(fam.lower(), f"'{fam}', sans-serif")
    w = {'normal': '300' if 'Barlow' in fam else '400', 'bold': '700'}.get(weight, weight)
    css = f'font:{style} normal {w} {size} {fam};'
    if col:
        css += f'color:{col};'
    return css


class Ctx:
    def __init__(self, page_json):
        self.dd = page_json['data']['document_data']
        self.th = dict(page_json['data'].get('theme_data', {}))
        self.cp = page_json['data'].get('component_properties', {})
        self.md = MASTER['data']['document_data']

    def ref(self, q, src=None):
        if not q or not isinstance(q, str):
            return None
        k = q.lstrip('#')
        return (src or self.dd).get(k) or self.md.get(k)

    def style(self, sid):
        s = self.th.get(sid) or MASTER['data']['theme_data'].get(sid) or {}
        return s.get('style', {}).get('properties', {})

    def props(self, c):
        return self.cp.get(str(c.get('propertyQuery', '')).lstrip('#')) or MASTER['data'].get('component_properties', {}).get(str(c.get('propertyQuery', '')).lstrip('#')) or {}

    def link(self, q):
        L = self.ref(q)
        if not L:
            return None
        t = L.get('type')
        if t == 'PageLink':
            return PAGES.get(str(L.get('pageId')).lstrip('#'))
        if t == 'ExternalLink':
            return L.get('url')
        if t == 'EmailLink':
            return 'mailto:' + L.get('recipient', '')
        return None


def rich_text(ctx, text):
    def repl(m):
        href = ctx.link(m.group(1))
        if not href:
            return ''
        ext = href.startswith('http')
        return f'href="{html.escape(href)}"' + (' target="_blank" rel="noopener"' if ext else '')
    return re.sub(r'dataquery="([^"]+)"', repl, text)


def esc(s):
    return html.escape(s or '')


def box(x, y, w, h, extra=''):
    return f'left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}'


def full_width_box(y, h):
    return f'left:calc(490px - 50vw);top:{y}px;width:100vw;height:{h}px;'


def items_of(ctx, D):
    out = []
    for i in D.get('items', []):
        I = ctx.ref(i)
        if not I or not I.get('uri'):
            continue
        out.append({
            'src': img_url(I['uri']), 'w': I.get('width') or 1, 'h': I.get('height') or 1,
            'title': I.get('title') or '', 'desc': I.get('description') or '',
            'link': ctx.link(I.get('link')),
        })
    return out


def lb_attrs(it, group):
    return (f'data-lb="{group}" data-src="{esc(it["src"])}" data-title="{esc(it["title"])}" '
            f'data-desc="{esc(it["desc"])}"')


def nl2br(s):
    return esc(s).replace(chr(10), '<br>')


def render_masonry(ctx, c, x, y, w, D, props, st):
    items = items_of(ctx, D)
    cols = props.get('numCols', 3)
    margin = props.get('margin', 25)
    colw = (w - margin * (cols - 1)) / cols
    heights = [0] * cols
    parts = []
    show_text = props.get('textMode', 'titleAndDescription') != 'noText'
    for it in items:
        ci = heights.index(min(heights))
        ih = colw * it['h'] / it['w']
        th = 0
        cap = ''
        if show_text and (it['title'] or it['desc']):
            lines = sum(max(1, -(-len(p) // 42)) for p in it['desc'].split(chr(10))) if it['desc'] else 0
            th = 50 + lines * 17
            cap = ('<div class="m-txt"><div class="g-t">' + esc(it['title']) + '</div>'
                   + ('<div class="g-d">' + nl2br(it['desc']) + '</div>' if it['desc'] else '') + '</div>')
        ix, iy = ci * (colw + margin), heights[ci]
        heights[ci] += ih + th + margin
        inner = f'<div class="m-img" style="aspect-ratio:{it["w"]}/{it["h"]}"><img src="{it["src"]}" alt="{esc(it["title"])}" loading="lazy"></div>' + cap
        sty = f'left:{ix:.1f}px;top:{iy:.1f}px;width:{colw:.1f}px'
        if it['link']:
            parts.append(f'<a class="m-item" href="{it["link"]}" style="{sty}">' + inner + '</a>')
        else:
            parts.append(f'<div class="m-item" style="{sty}" {lb_attrs(it, c["id"])}>' + inner + '</div>')
    h = max(heights) - margin if items else 10
    return (f'<div class="comp masonry" data-cols="{cols}" data-gap="{margin}" style="{box(x, y, w, round(h))}">'
            + ''.join(parts) + '</div>'), h


def render_thumbnails(ctx, c, x, y, w, h, D, props, st, full=False):
    items = items_of(ctx, D)
    thumbs_h = max(40, round(h * 0.105))
    stage_h = h - thumbs_h - props.get('margin', 5)
    fit = 'contain' if props.get('cropAndFitStage') == 'fit' else 'cover'
    slides = []
    for n, it in enumerate(items):
        cap = ''
        if (it['title'] or it['desc']) and props.get('textMode', 'titleAndDescription') != 'noText':
            cap = '<div class="t-cap"><div class="g-t">' + esc(it['title']) + '</div><div class="g-d">' + nl2br(it['desc']) + '</div></div>'
        img = f'<img src="{it["src"]}" alt="{esc(it["title"])}" style="object-fit:{fit}"' + (' loading="lazy"' if n else '') + '>'
        if it['link']:
            img = f'<a href="{it["link"]}">{img}</a>'
        slides.append('<div class="t-slide' + (' on' if n == 0 else '') + '">' + img + cap + '</div>')
    th = ''.join('<button class="t-th' + (' on' if n == 0 else '') + '" style="background-image:url(' + chr(39) + it['src'] + chr(39) + ')" aria-label="' + str(n + 1) + '"></button>'
                 for n, it in enumerate(items))
    arrows = '<button class="t-prev" aria-label="Anterior">&#10094;</button><button class="t-next" aria-label="Siguiente">&#10095;</button>' if len(items) > 1 else ''
    pos = full_width_box(y, h) if full else box(x, y, w, h)
    bg = 'background:#fff;' if not full else 'background:rgba(255,255,255,.5);'
    auto = props.get('autoplayInterval', 5) if props.get('autoplay') else 0
    return (f'<div class="comp thumbs" data-auto="{auto}" style="{pos}{bg}">'
            f'<div class="t-stage" style="height:{stage_h}px">' + ''.join(slides) + arrows + '</div>'
            f'<div class="t-strip" style="height:{thumbs_h}px">' + th + '</div></div>')


def render_strip_slideshow(ctx, c, y, h, D, props):
    items = items_of(ctx, D)
    slides = ''.join(
        '<div class="ss-slide' + (' on' if n == 0 else '') + '" style="background-image:url(' + chr(39) + it['src'] + chr(39) + ')">'
        + ('<div class="ss-cap"><div class="g-t">' + esc(it['title']) + '</div><div class="g-d">' + esc(it['desc']) + '</div></div>' if it['title'] else '')
        + '</div>' for n, it in enumerate(items))
    dots = ''.join('<button class="ss-dot' + (' on' if n == 0 else '') + '" aria-label="' + str(n + 1) + '"></button>' for n in range(len(items)))
    auto = props.get('autoplayInterval', 3) if props.get('autoplay', True) else 0
    return (f'<div class="comp strip-ss" data-auto="{auto}" style="{full_width_box(y, h)}">' + slides +
            '<button class="ss-prev" aria-label="Anterior">&#10094;</button><button class="ss-next" aria-label="Siguiente">&#10095;</button>'
            '<div class="ss-dots">' + dots + '</div></div>')


def render_matrix(ctx, c, x, y, w, D, props, st, skin):
    items = items_of(ctx, D)
    cols = props.get('numCols', 3)
    margin = props.get('margin', 15)
    rows = -(-len(items) // cols)
    item_h = props.get('itemHeight', 150)
    colw = (w - margin * (cols - 1)) / cols
    parts = []
    separate = 'SeparateTextBox' in skin
    q = chr(39)
    for n, it in enumerate(items):
        r, cidx = divmod(n, cols)
        ix, iy = cidx * (colw + margin), r * (item_h + margin)
        if separate:
            tb = int(st.get('imgHeightDiff', 41))
            inner = (f'<div class="mx-img" style="height:{item_h - tb - 4}px;background-image:url({q}{it["src"]}{q})"></div>'
                     f'<div class="mx-box" style="height:{tb}px;background:{color(st.get("boxbg", "#2F2E2E"))};color:{color(st.get("ttl2", "#FFFFFF"))}">' + esc(it['title']) + '</div>')
            cls = 'mx-item sep'
        else:
            bw = st.get('brw', '0px')
            inner = (f'<div class="mx-img" style="height:100%;background-image:url({q}{it["src"]}{q});'
                     f'border:{bw} solid {color(st.get("brdTrans", "#2F2E2E"))}"></div>'
                     '<div class="mx-text" style="color:' + color(st.get('ttlTrans', '#2F2E2E')) + '"><div class="g-t">' + esc(it['title'])
                     + '</div><div class="g-d">' + nl2br(it['desc']) + '</div></div>')
            cls = 'mx-item trans'
        parts.append(f'<div class="{cls}" style="left:{ix:.1f}px;top:{iy}px;width:{colw:.1f}px;height:{item_h}px" {lb_attrs(it, c["id"])}>' + inner + '</div>')
    h = rows * item_h + (rows - 1) * margin
    return f'<div class="comp matrix" style="{box(x, y, w, h)}">' + ''.join(parts) + '</div>', h


def button_html(ctx, c, x, y, w, h, D):
    st = ctx.style(c.get('styleId'))
    skin = (c.get('skin') or '').split('.')[-1]
    href = ctx.link(D.get('link')) or '#'
    fnt = font_css(st.get('fnt', 'font_8'))
    txt = color(st.get('txt', 'color_11'))
    bg = color(st.get('bg', 'color_18'), float(st.get('alpha-bg', 1)))
    bgh = color(st.get('bgh', st.get('bg', 'color_18')), float(st.get('alpha-bgh', 1)))
    shd = ''
    if st.get('boxShadowToggleOn-shd') == 'true':
        shd = 'box-shadow:' + st.get('shd', '0 1px 4px rgba(0,0,0,.6)').rstrip(';') + ';'
    brd = ''
    if st.get('brw') and st.get('brw') not in ('0', '0px'):
        brd = f'border:{st["brw"]} solid {color(st.get("brd"))};'
    rd = st.get('rd', '0')
    rd = rd if rd.endswith('px') else rd + 'px'
    cls = {'ButtonArrow': 'btn arrow-r', 'ButtonArrowLeft': 'btn arrow-l', 'ButtonLiftedShadow': 'btn lifted'}.get(skin, 'btn')
    return (f'<a class="comp {cls}" href="{href}" style="{box(x, y, w, h)}{fnt}color:{txt};--bg:{bg};--bgh:{bgh};'
            f'border-radius:{rd};{shd}{brd}"><span>' + esc(D.get('label')) + '</span></a>')


def render(ctx, comps):
    out, bottom = [], 0
    for c in comps:
        ct = (c.get('componentType') or '').split('.')[-1]
        L = c.get('layout', {})
        x, y, w, h = L.get('x', 0), L.get('y', 0), L.get('width', 0), L.get('height', 0)
        D = ctx.ref(c.get('dataQuery')) or {}
        props = ctx.props(c)
        st = ctx.style(c.get('styleId'))
        skin = c.get('skin') or ''
        piece = ''
        if ct == 'WRichText':
            piece = f'<div class="comp txt" style="left:{x}px;top:{y}px;width:{w}px;min-height:{h}px">' + rich_text(ctx, D.get('text', '')) + '</div>'
        elif ct == 'WPhoto':
            if D.get('uri'):
                img = f'<img src="{img_url(D["uri"])}" alt="{esc(D.get("alt") or D.get("title"))}" loading="lazy">'
                href = ctx.link(D.get('link'))
                if href:
                    tgt = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
                    piece = f'<a class="comp photo" href="{href}"{tgt} style="{box(x, y, w, h)}">{img}</a>'
                else:
                    piece = f'<div class="comp photo" style="{box(x, y, w, h)}">{img}</div>'
        elif ct == 'SiteButton':
            piece = button_html(ctx, c, x, y, w, h, D)
        elif ct == 'Masonry':
            piece, h = render_masonry(ctx, c, x, y, w, D, props, st)
        elif ct == 'Thumbnails':
            piece = render_thumbnails(ctx, c, x, y, w, h, D, props, st)
        elif ct == 'StripShowcase':
            piece = render_thumbnails(ctx, c, x, y, w, h, D, dict(props, cropAndFitStage='fit', textMode='noText'), st, full=True)
        elif ct == 'StripSlideshow':
            piece = render_strip_slideshow(ctx, c, y, h, D, props)
        elif ct == 'MatrixGallery':
            piece, h = render_matrix(ctx, c, x, y, w, D, props, st, skin)
        elif ct == 'Video' and D.get('videoType') == 'YOUTUBE':
            piece = (f'<div class="comp video" style="{box(x, y, w, h)}"><iframe src="https://www.youtube-nocookie.com/embed/{D["videoId"]}" '
                     'title="Video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>')
        elif ct == 'Video' and D.get('videoType') == 'VIMEO':
            piece = f'<div class="comp video" style="{box(x, y, w, h)}"><iframe src="https://player.vimeo.com/video/{D["videoId"]}" allowfullscreen loading="lazy"></iframe></div>'
        elif ct == 'VectorImage':
            p = os.path.join(HERE, 'svg', D.get('svgId', ''))
            svg = open(p).read() if D.get('svgId') and os.path.exists(p) else ''
            href = ctx.link(D.get('link'))
            inner = svg.replace('<svg ', '<svg preserveAspectRatio="xMidYMid meet" width="100%" height="100%" ', 1)
            tag = 'a' if href else 'div'
            hattr = f' href="{href}"' if href else ''
            piece = f'<{tag} class="comp vec"{hattr} style="{box(x, y, w, h)}">{inner}</{tag}>'
        elif ct == 'FiveGridLine':
            lc = color(st.get('clr', 'color_15')) if st else '#2F2E2E'
            piece = f'<div class="comp" style="{box(x, y, w, 0)}border-top:{st.get("lnw", "1px")} solid {lc}"></div>'
        elif ct == 'FacebookLikeBox' and c.get('id') == 'comp-ilmc4wi5':
            piece = home_videos_html(x, y, w, h)
        elif ct == 'FacebookLikeBox':
            pg = D.get('facebookPageId', '')
            fw = min(w, 500)
            src = ('https://www.facebook.com/plugins/page.php?href=https%3A%2F%2Fwww.facebook.com%2F' + pg +
                   f'&tabs=timeline&width={fw}&height={h}&small_header=false&adapt_container_width=true&hide_cover=false&show_facepile=true')
            piece = f'<div class="comp fb" style="{box(x, y, w, h)}"><iframe src="{src}" width="{fw}" height="{h}" style="border:none;overflow:hidden" scrolling="no" allowfullscreen loading="lazy" title="Facebook"></iframe></div>'
        elif ct == 'FacebookShare':
            piece = (f'<a class="comp fbshare" href="#" data-fbshare style="{box(x, y, w, h)}">'
                     '<span class="fbf">f</span>' + esc(D.get('label', 'Compartir')) + '</a>')
        elif ct == 'TPAWidget' and c.get('id') == 'comp-ilmbbwb4':
            piece = teaser_html(x, y, w, h)
        elif ct == 'AppWidget':
            piece = render_form(ctx, c, x, y, w, h)
        elif ct in ('Container', 'Group', 'BoxSlideShow'):
            inner, _ = render(ctx, c.get('components', []))
            piece = f'<div class="comp" style="{box(x, y, w, h)}">{inner}</div>'
        if piece:
            out.append(piece)
            bottom = max(bottom, y + h)
    return '\n'.join(out), bottom


def home_videos_html(x, y, w, h):
    vids = [('ze6OEQH6xF0', 'Travelling Skates en "Valor Agregado" &middot; Programa Encuentro'),
            ('gU8ZA5r5Bow', 'Quantum Pro &middot; Quantum Dance &middot; Quantum Derby')]
    out = [f'<div class="comp homevids" style="{box(x, y, w, h)}"><span class="teaser-k">TRAVELLING SKATES EN VIDEO</span>']
    for vid, t in vids:
        out.append(f'<button class="yt-lite" data-yt="{vid}" aria-label="Reproducir video" '
                   f'style="background-image:url(https://i.ytimg.com/vi/{vid}/hqdefault.jpg)"><span class="yt-play"></span></button>'
                   f'<span class="homevids-t">{t}</span>')
    out.append('</div>')
    return ''.join(out)


def teaser_html(x, y, w, h):
    return (f'<a class="comp teaser" href="historia.html" style="{box(x, y, w, h)}">'
            '<span class="teaser-img" style="background-image:url(' + chr(39) + 'assets/historia/planchas-doradas-produccion.jpg' + chr(39) + ')"></span>'
            '<span class="teaser-txt"><span class="teaser-k">NUESTRA HISTORIA</span>'
            '<span class="teaser-h">De una idea a la marca de patín artístico l&iacute;der en Latinoam&eacute;rica.</span>'
            '<span class="teaser-p">Ingenier&iacute;a, matricer&iacute;a e inyecci&oacute;n propias: c&oacute;mo nacieron las ruedas Quantum y nuestras planchas.</span>'
            '<span class="teaser-b">Conoc&eacute; la historia &rarr;</span></span></a>')


def render_form(ctx, c, x, y, w, h):
    def find(cc, t):
        if (cc.get('componentType') or '').endswith(t):
            return cc
        for ch in cc.get('components', []):
            r = find(ch, t)
            if r:
                return r
    state = find(c, 'StateBoxFormState') or {}
    parts = []
    for ch in state.get('components', []):
        ct = (ch.get('componentType') or '').split('.')[-1]
        L = ch['layout']
        D = ctx.ref(ch.get('dataQuery')) or {}
        if ct == 'WRichText':
            parts.append(f'<div class="comp txt" style="left:{L["x"]}px;top:{L["y"]}px;width:{L["width"]}px">' + rich_text(ctx, D.get('text', '')) + '</div>')
        elif ct == 'TextInput':
            parts.append(f'<input class="comp inp" type="email" name="email" required placeholder="{esc(D.get("placeholder"))}" style="{box(L["x"], L["y"], L["width"], L["height"])}">')
        elif ct == 'SiteButton':
            st = ctx.style(ch.get('styleId'))
            parts.append(f'<button class="comp btn sub" type="submit" style="{box(L["x"], L["y"], L["width"], L["height"])}{font_css(st.get("fnt", "font_8"))}'
                         f'color:{color(st.get("txt", "color_11"))};--bg:{color(st.get("bg", "color_18"))};--bgh:{color(st.get("bgh", "color_18"))}"><span>' + esc(D.get('label')) + '</span></button>')
    return (f'<form class="comp form" action="mailto:info@travellingskates.com" method="post" enctype="text/plain" '
            f'style="{box(x, y, w, h)}">' + ''.join(parts) + '</form>')


def menu_html(ctx, current_file):
    md = MASTER['data']['document_data']
    menu = next(v for v in md.values() if v.get('type') == 'CustomMenu')

    def item(i):
        v = md[i.lstrip('#')]
        if not v.get('isVisible', True):
            return ''
        href = ctx.link(v.get('link'))
        kids = ''.join(item(k) for k in v.get('items', []))
        on = ' sel' if href and href == current_file else ''
        if kids and any(md[k.lstrip('#')].get('link') and ctx.link(md[k.lstrip('#')]['link']) == current_file for k in v.get('items', [])):
            on = ' sel'
        a = f'<a href="{href}">' + esc(v['label']) + '</a>' if href else '<span>' + esc(v['label']) + '</span>'
        if kids:
            return f'<li class="has-sub{on}">{a}<ul class="sub">{kids}</ul></li>'
        return f'<li class="{on.strip()}">{a}</li>'
    items = [item(i) for i in menu['items']]
    items = [x for x in items if x]
    hist = '<li class="' + ('sel' if current_file == 'historia.html' else '') + '"><a href="historia.html">HISTORIA</a></li>'
    items.insert(1, hist)
    return '<ul class="menu">' + ''.join(items) + '</ul>'


def header_footer(current_file):
    ctx = Ctx(MASTER)
    st = MASTER['structure']
    header = next(c for c in st['children'] if c['id'] == 'SITE_HEADER')
    footer = next(c for c in st['children'] if c['id'] == 'SITE_FOOTER')
    hparts = []
    for c in header['components']:
        ct = c['componentType'].split('.')[-1]
        L = c['layout']
        if ct == 'DropDownMenu':
            hparts.append(f'<nav class="comp ddm" style="left:{L["x"]}px;top:{L["y"]}px;height:{L["height"]}px">' + menu_html(ctx, current_file) + '</nav>')
        else:
            if ct == 'SiteButton':
                c = dict(c, layout=dict(c['layout'], x=470))
            hh, _ = render(ctx, [c])
            hparts.append(hh)
    fh, _ = render(ctx, footer['components'])
    hs = ctx.style('hc3')
    return ('<header id="hdr" style="background:' + color(hs.get('bg', 'color_14')) + '"><div class="stage" style="height:48px">'
            + ''.join(hparts) + '</div></header>',
            f'<footer id="ftr"><div class="stage" style="height:{footer["layout"]["height"]}px">' + fh + '</div></footer>')


def css():
    f = []
    for i, spec in enumerate(FONTS):
        f.append('.font_%d{%s}' % (i, font_css(spec)))
    for i, c in enumerate(COLORS):
        f.append('.color_%d{color:%s}' % (i, c))
    return open(os.path.join(HERE, 'base.css')).read() + '\n' + '\n'.join(f)


def page_html(title, desc, body, page_h, current_file, flow=False):
    hdr, ftr = header_footer(current_file)
    og = IMG_BASE + img_name('22781b_d271d225e5ae4e93b0259a63378980a1.jpg')
    ico = IMG_BASE + img_name('22781b_3f817ae20dc84f4f8ef4906a1d19da3a.png')
    return ('<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=1000">\n'
            f'<title>{esc(title)}</title>\n<meta name="description" content="{esc(desc)}">\n'
            f'<meta property="og:title" content="{esc(title)}">\n<meta property="og:description" content="{esc(desc)}">\n'
            f'<meta property="og:image" content="{og}">\n<link rel="icon" type="image/png" href="{ico}">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,300;0,400;0,700;1,300&family=Raleway:wght@400;700&display=swap" rel="stylesheet">\n'
            '<link rel="stylesheet" href="assets/site.css">\n</head>\n<body>\n'
            + hdr + ('\n<main id="pg" class="flowpage">\n' if flow else f'\n<main id="pg"><div class="stage" style="height:{page_h}px">\n') + body + ('\n</main>\n' if flow else '\n</div></main>\n') + ftr +
            '\n<div id="lb" hidden><button class="lb-x" aria-label="Cerrar">&times;</button><button class="lb-p" aria-label="Anterior">&#10094;</button>'
            '<figure><img alt=""><figcaption><div class="g-t"></div><div class="g-d"></div></figcaption></figure><button class="lb-n" aria-label="Siguiente">&#10095;</button></div>\n'
            '<script src="assets/site.js"></script>\n</body>\n</html>')


def main():
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    for key, v in RAW.items():
        if key == '_master' or key in SKIP:
            continue
        j = v['json']
        ctx = Ctx(j)
        body, bottom = render(ctx, j['structure'].get('components', []))
        page_h = max(bottom, 500)
        pdata = ctx.ref(j['structure'].get('dataQuery')) or {}
        fname = PAGES[v['meta']['id']]
        if key == 'home':
            title, desc = HOME_TITLE, HOME_DESC
        else:
            title = (pdata.get('pageTitleSEO') or v['meta']['title']).strip() + ' | ' + SITE_NAME
            desc = pdata.get('descriptionSEO') or HOME_DESC
        open(os.path.join(OUT, fname), 'w').write(page_html(title, desc, body, page_h, fname))
    import historia
    open(os.path.join(OUT, 'historia.html'), 'w').write(page_html(historia.TITLE + ' | ' + SITE_NAME, historia.DESC, historia.body(), 0, 'historia.html', flow=True))
    open(os.path.join(OUT, 'assets', 'site.css'), 'w').write(css())
    open(os.path.join(OUT, 'assets', 'site.js'), 'w').write(open(os.path.join(HERE, 'site.js')).read())
    dims = {}
    for k, v in RAW.items():
        for it in list(v['json']['data']['document_data'].values()) + list(v['json']['data'].get('design_data', {}).values()):
            if it.get('type') == 'Image' and it.get('uri'):
                dims[it['uri']] = (it.get('width') or 1200, it.get('height') or 1200)
    lst = []
    for uri, name in sorted(IMAGES.items()):
        w, h = dims.get(uri, (1200, 1200))
        if w > 1200:
            h, w = round(h * 1200 / w), 1200
        q = 90 if uri.lower().endswith('.png') else 82
        lst.append([name, f'https://static.wixstatic.com/media/{uri}/v1/fit/w_{w},h_{h},q_{q}/{uri}'])
    json.dump(lst, open(os.path.join(OUT, 'images.json'), 'w'))
    print('pages', len(PAGES), 'images', len(IMAGES))


if __name__ == '__main__':
    main()
