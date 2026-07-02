#!/usr/bin/env python
"""
Home of the Rainbowfish — static site generator (first draft).

Reads the converted book text/images (assets/converted) plus the preserved live-site
HTML (assets/reference/live_site) and stamps a complete static site into src/.

The left-hand menu and page chrome are defined ONCE here (SECTIONS + render_page)
and stamped into every page, so a change here propagates to the whole site.
"""
import os, re, shutil, html, io, json
import fitz, openpyxl
from PIL import Image

JOB   = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC   = os.path.join(JOB, "src")
CONV  = os.path.join(JOB, "assets", "converted")
PAGES = os.path.join(CONV, "pages")
IMGS  = os.path.join(CONV, "images")
SITE  = os.path.join(JOB, "assets", "site_assets")
REF   = os.path.join(JOB, "assets", "reference", "live_site")
PDF   = os.path.join(JOB, "assets", "source", "Rainbowfishes.2011.pdf")
XLSX  = os.path.join(JOB, "HotRF.headings.xlsx")

# --- CrossRef enrichment: map a reference's text signature -> DOI (title kept as-is
#     because the book's printed titles are cleaner than most CrossRef records) ------
def _ref_sig(text):
    """Robust key from a reference string: author+year+title-start, punctuation-free."""
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"<[^>]+>", "", text)              # strip span/italic markup
    return re.sub(r"[^a-z0-9]", "", text.lower())[:50]

_REF_DOI = None
def _load_ref_doi():
    global _REF_DOI
    if _REF_DOI is not None:
        return _REF_DOI
    _REF_DOI = {}
    raw_p = os.path.join(JOB, "assets", "references_raw.json")
    xref_p = os.path.join(JOB, "assets", "references_crossref.json")
    if os.path.exists(raw_p) and os.path.exists(xref_p):
        raw = json.load(open(raw_p, encoding="utf-8"))
        xref = json.load(open(xref_p, encoding="utf-8"))
        for i, ref in enumerate(raw):
            v = xref.get(str(i), {})
            if v.get("doi"):
                _REF_DOI[_ref_sig(ref)] = v["doi"]
    return _REF_DOI

def _enrich_reference(p_html):
    """Append a DOI link to a reference <p> when CrossRef confidently matched it."""
    plain = re.sub(r"<[^>]+>", "", p_html)
    doi = _load_ref_doi().get(_ref_sig(plain))
    if not doi:
        return p_html
    link = ('<a class="doi" href="https://doi.org/%s">https://doi.org/%s</a>'
            % (html.escape(doi, quote=True), html.escape(doi)))
    return p_html.rsplit("</p>", 1)[0].rstrip() + " " + link + "</p>"

# printed page + PDF_OFFSET = PDF (1-based) page
PDF_OFFSET = 16

# Species accounts we have located page ranges for (PDF pages, 1-based).
# Extend this map to build more accounts verbatim.
ACCOUNTS = {
    ("Rhadinocentrus", "ornatus"): list(range(432, 441)),   # printed 416–424
}

# ---------------------------------------------------------------- sections ----
# (title, slug, one-line description for the Contents page)
SECTIONS = [
    ("Background", "background",
     "Front matter, foreword and context from the opening of the book."),
    ("Introduction", "introduction",
     "What rainbowfishes and blue-eyes are, and why they matter."),
    ("Rainbowfish Species", "rainbowfish_species",
     "Illustrated species accounts for the family Melanotaeniidae."),
    ("Blue Eye Species", "blue_eye_species",
     "Illustrated species accounts for the family Pseudomugilidae."),
    ("History of Rainbowfishes in Captivity", "history_of_rainbowfishes_in_captivity",
     "How these fishes entered and shaped the aquarium hobby."),
    ("Distribution & Habitat", "distribution_and_habitat",
     "Where rainbowfishes live across Australia and New Guinea."),
    ("Collecting & Shipping", "collecting_and_shipping",
     "Field collection and moving fish safely."),
    ("Keeping & Caring", "keeping_and_caring",
     "Aquarium set-up, water quality and day-to-day husbandry."),
    ("Breeding & Raising", "breeding_and_raising",
     "Spawning, incubation and rearing fry."),
    ("Foods & Feeding", "foods_and_feeding",
     "Diets, live foods and feeding programs."),
    ("Disease Prevention & Control", "disease_prevention_and_control",
     "Recognising, preventing and treating disease."),
    ("Sources of Information", "sources_of_information",
     "References and further reading."),
]
SLUGS = {t: s for t, s, _ in SECTIONS}

# Lead-content source pages (PDF page indices). printed page + 16 = PDF page.
LEAD_PAGES = {
    "background": [7, 8, 9],
    "distribution_and_habitat": [23, 24],
    "collecting_and_shipping": [51, 52],
    "keeping_and_caring": [65, 66],
    "breeding_and_raising": [109, 110],
    "foods_and_feeding": [131, 132],
    "rainbowfish_species": [181, 182],
    "blue_eye_species": [441, 442],
    "disease_prevention_and_control": [491, 492],
    "sources_of_information": [555, 556],
}

# ------------------------------------------------------------- text cleaning --
def page_text(n):
    with open(os.path.join(PAGES, f"page_{n:04d}.txt"), encoding="utf-8") as f:
        return f.read()

def clean_paragraphs(page_nums):
    """Turn wrapped PDF lines into clean paragraphs; drop page furniture."""
    paras, cur = [], []
    def flush():
        if cur:
            paras.append(" ".join(cur).strip()); cur.clear()
    for n in page_nums:
        for ln in page_text(n).split("\n"):
            s = ln.strip()
            if not s:
                flush(); continue
            if re.fullmatch(r"\d+", s):                       # page number
                continue
            if s.startswith("Rainbowfishes—Their Care"):  # running header
                continue
            cur.append(s)
        flush()
    # drop short trailing fragments (running-footer titles, photo credits)
    return [p for p in paras if len(p) > 60 or p.rstrip().endswith(".")]

def paras_to_html(paras, limit=6):
    return "\n".join(f"      <p>{html.escape(p)}</p>" for p in paras[:limit])

# ---------------------------------------------------- spreadsheet TOC parse ---
def parse_toc():
    """Peter's authoritative TOC -> ordered [(heading, [subheadings])]."""
    ws = openpyxl.load_workbook(XLSX, data_only=True).worksheets[0]
    sections, cur, seen = [], None, set()
    for a, b in ws.iter_rows(values_only=True):
        a = (a or "").strip(); b = (b or "").strip()
        if a:
            if a in seen:            # bottom-of-sheet heading recap: stop collecting
                cur = None; continue
            seen.add(a); cur = (a, []); sections.append(cur)
        elif b and cur is not None:
            cur[1].append(b)
    return sections

BINOMIAL = re.compile(r"^[A-Z][a-z]+ [a-z]")

def toc_species(sections):
    """Return {'Rainbowfish Species': [(genus, species, sub)...], 'Blue Eye Species': [...]}."""
    out = {}
    for heading, subs in sections:
        if heading in ("Rainbowfish Species", "Blue Eye Species"):
            sp = []
            for s in subs:
                if BINOMIAL.match(s):
                    g, rest = s.split(" ", 1)
                    sp.append((g, rest, s))
                elif s.startswith("Rainbowfishes ("):     # "(undetermined)" placeholder
                    sp.append((None, None, s))
            out[heading] = sp
    return out

# -------------------------------------------------- verbatim account extract --
_LOCALITY = re.compile(r"(Queensland|New South Wales|Northern Territory|Western Australia"
                       r"|Victoria|Tasmania|New Guinea|Papua|Indonesia|Irian|Australia|Island)")

def _reflow(t):
    return re.sub(r"\s+", " ", t.replace("-\n", "").replace("\n", " ")).strip()

def _italic_span(s):
    return ("Italic" in s.get("font", "")) or bool(s.get("flags", 0) & 2)

def _wrap_italics(text, phrases):
    esc = html.escape(text)
    mapping = {}
    for i, ph in enumerate(sorted((p for p in phrases if len(p) > 1), key=len, reverse=True)):
        eph = html.escape(ph)
        if eph and eph in esc:
            key = "%d" % i
            esc = esc.replace(eph, key)
            mapping[key] = '<span class="scientific-name">%s</span>' % eph
    for k, v in mapping.items():
        esc = esc.replace(k, v)
    return esc

def _split_numbered(text):
    if not re.match(r"^1\.\s", text) or not re.search(r"(?:^|\s)2\.\s", text):
        return None
    parts = re.split(r"(?:^|\s)(\d{1,2})\.\s+", text)
    nums, segs = parts[1::2], parts[2::2]
    if len(nums) < 2 or nums != [str(i + 1) for i in range(len(nums))]:
        return None
    return [s.strip() for s in segs if s.strip()]

def _para_render(lines):
    """Full paragraph element: <p>, or <ol> for a numbered list. Linnean names use
    the PDF's own italic runs."""
    raw = " ".join("".join(sp["text"] for sp in ln["spans"]) for ln in lines)
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", raw)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^[^0-9A-Za-z\"'(]+", "", text).strip()
    phrases, cur = set(), ""
    for ln in lines:
        for sp in ln["spans"]:
            if _italic_span(sp):
                cur += sp["text"]
            else:
                if cur.strip():
                    phrases.add(re.sub(r"\s+", " ", cur).strip())
                cur = ""
        if cur:
            cur += " "
    if cur.strip():
        phrases.add(re.sub(r"\s+", " ", cur).strip())
    listitems = _split_numbered(text)
    if listitems:
        lis = "".join("<li>%s</li>" % _wrap_italics(it, phrases) for it in listitems)
        return '<ol class="book-list">%s</ol>' % lis
    return "<p>%s</p>" % _wrap_italics(text, phrases)

def _section_caption(text, credit):
    text = re.sub(r"\s+", " ", text or "").strip()
    m = re.match(r"(?:Photo|Image|Illustration|Photograph)s?\s*[:\-]\s*(.+)$", text)
    if m and not credit:
        credit, text = m.group(1).strip(), ""
    bits = []
    if text:
        bits.append(html.escape(text))
    if credit:
        bits.append("photo &copy; " + html.escape(credit))
    return " &mdash; ".join(bits)

def _parse_header_lines(header_lines):
    """Line-based header parse (one synonym per line) for accounts whose synonym names
    are roman rather than italic (e.g. Pseudomugil signifer)."""
    lines_ = []
    for ln in header_lines:
        t = re.sub(r"\s+", " ", "".join(s["text"] for s in ln["spans"])).strip()
        if t:
            lines_.append(t)
    attribution, common, syns = "", "", []
    i = 0
    if i < len(lines_) and re.search(r",\s*\d{4}[a-z]?\)?\.?$", lines_[i]) \
            and not re.match(r"^[A-Z][a-z]+ [a-z]{2,}", lines_[i]):
        attribution = lines_[i].strip("."); i += 1
    while i < len(lines_) and not re.search(r"\d{4}", lines_[i]):
        common = (common + " " + lines_[i]).strip() if common else lines_[i]
        i += 1
    for sl in lines_[i:]:
        m = re.match(r"^(.*?)\s+(\(?[A-Z][A-Za-z.&'\- ]*,\s*\d{4}[a-z]?\)?)\.?$", sl)
        if m and m.group(1).strip():
            syns.append((m.group(1).strip(), m.group(2).strip()))
        elif sl:
            syns.append((sl.strip(), ""))
    return attribution, common, syns

def _fig_caption(binom, loc, credit):
    bits = []
    if binom:
        bits.append('<span class="scientific-name">%s</span>' % html.escape(binom))
    if loc:
        bits.append(html.escape(loc))
    cap = " &mdash; ".join(bits)
    if credit:
        cap = (cap + " &mdash; " if cap else "") + "photo &copy; " + html.escape(credit)
    return cap

def _fig_adjacent(a, b, t=3):
    """True if bboxes are tiles of one image (same width & vertically touching, or
    same height & horizontally touching)."""
    same_x = abs(a[0] - b[0]) < t and abs(a[2] - b[2]) < t
    same_y = abs(a[1] - b[1]) < t and abs(a[3] - b[3]) < t
    v_touch = abs(a[3] - b[1]) < t or abs(b[3] - a[1]) < t
    h_touch = abs(a[2] - b[0]) < t or abs(b[2] - a[0]) < t
    return (same_x and v_touch) or (same_y and h_touch)

def _group_tiles(places):
    groups, used = [], [False] * len(places)
    for i in range(len(places)):
        if used[i]:
            continue
        grp = [i]; used[i] = True; changed = True
        while changed:
            changed = False
            for j in range(len(places)):
                if used[j]:
                    continue
                if any(_fig_adjacent(places[k]["bbox"], places[j]["bbox"]) for k in grp):
                    grp.append(j); used[j] = True; changed = True
        groups.append([places[k] for k in grp])
    return groups

def _save_figure(doc, parts, vertical, out_dir, base):
    """Write one figure. Multi-tile figures are stitched back into a single image so
    integrity is preserved; single images keep their original bytes."""
    infos = [doc.extract_image(x) for x in parts]
    if len(infos) == 1:
        d = infos[0]
        im = Image.open(io.BytesIO(d["image"]))
        if im.mode not in ("CMYK", "YCCK", "P"):
            fn = base + "." + d["ext"]
            with open(os.path.join(out_dir, fn), "wb") as fh:
                fh.write(d["image"])
            return fn
        combined = im.convert("RGB")
    else:
        imgs = []
        for d in infos:
            im = Image.open(io.BytesIO(d["image"]))
            imgs.append(im.convert("RGB") if im.mode != "RGB" else im)
        if vertical:
            w = max(i.width for i in imgs)
            imgs = [i if i.width == w else i.resize((w, round(i.height * w / i.width))) for i in imgs]
            combined = Image.new("RGB", (w, sum(i.height for i in imgs)), "white")
            y = 0
            for i in imgs:
                combined.paste(i, (0, y)); y += i.height
        else:
            h = max(i.height for i in imgs)
            imgs = [i if i.height == h else i.resize((round(i.width * h / i.height), h)) for i in imgs]
            combined = Image.new("RGB", (sum(i.width for i in imgs), h), "white")
            x = 0
            for i in imgs:
                combined.paste(i, (x, 0)); x += i.width
    fn = base + ".jpg"
    combined.save(os.path.join(out_dir, fn), "JPEG", quality=90)
    return fn

def extract_account(pdf_pages, out_dir, slug, binom, citation, common, keep_big=False, below_caption=False, special_header=False):
    """Ordered items faithful to book layout:
       ('fig', filename, caption_html) | ('head', level, text) | ('para', html)
    Heading levels come from PDF font sizes; captions are text sitting over a figure;
    figures keep reading-order position (by column and vertical position)."""
    from collections import Counter, defaultdict
    doc = fitz.open(PDF)
    items, fig_no = [], 0
    header_lines, hdr_done = [], {"v": False}
    first_pno = pdf_pages[0]
    for pno in pdf_pages:
        p = doc[pno - 1]
        pw, mid = p.rect.width, p.rect.width / 2
        places = [dict(bbox=list(im["bbox"]), xref=im["xref"])
                  for im in p.get_image_info(xrefs=True)
                  if (im["bbox"][3] - im["bbox"][1]) >= 130]
        figs = []
        for grp in _group_tiles(places):
            x0 = min(g["bbox"][0] for g in grp); y0 = min(g["bbox"][1] for g in grp)
            x1 = max(g["bbox"][2] for g in grp); y1 = max(g["bbox"][3] for g in grp)
            vertical = len(grp) == 1 or all(abs(g["bbox"][0] - grp[0]["bbox"][0]) < 3 for g in grp)
            grp.sort(key=lambda g: g["bbox"][1] if vertical else g["bbox"][0])
            figs.append(dict(bbox=[x0, y0, x1, y1],
                             parts=[g["xref"] for g in grp], vertical=vertical))
        # when figures overlap in y, emit the full-width one before a column one
        figs.sort(key=lambda f: (f["bbox"][1], -(f["bbox"][2] - f["bbox"][0])))
        lines = []
        for blk in p.get_text("dict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk["lines"]:
                txt = "".join(s["text"] for s in ln["spans"])
                if not txt.strip():
                    continue
                lines.append(dict(bbox=ln["bbox"], spans=ln["spans"], text=txt,
                                  size=max(s["size"] for s in ln["spans"])))
        def vertical(lb):
            return (lb[2] - lb[0]) < (lb[3] - lb[1]) * 0.6      # rotated = photographer credit
        def overlaps(lb, fb, m=8):
            oy = min(lb[3], fb[3] + m) - max(lb[1], fb[1] - m)
            ox = min(lb[2], fb[2] + m) - max(lb[0], fb[0] - m)
            return oy > (lb[3] - lb[1]) * 0.4 and ox > 0
        below_caps = {}
        def below_fig(lb, sz):
            if sz > 9:                                          # captions are ~8pt, body 10pt
                return None
            for f in figs:
                fb = f["bbox"]
                if fb[3] <= lb[1] <= fb[3] + 26 and lb[0] >= fb[0] - 25 and lb[2] <= fb[2] + 25:
                    return f
            return None
        credit_lines, loc_lines, page_marker, content = [], [], "", []
        for ln in lines:
            lb, t = ln["bbox"], ln["text"].strip()
            if re.fullmatch(r"\d+", t) or ("Their Care" in t and "Keeping" in t):
                continue
            if ln["size"] >= 30:
                continue
            if ln["size"] >= 14 and not keep_big:
                continue
            if pno == first_pno and not keep_big and re.sub(r"\s+", " ", t) == binom:
                continue                                        # sub-14pt title leak (e.g. Cairnsichthys, 13.98pt)
            if vertical(lb):                                    # photographer credit (vertical)
                credit_lines.append((t, lb)); continue
            if "(" in t and _LOCALITY.search(t) and len(t) < 80                     and any(overlaps(lb, f["bbox"]) for f in figs):
                loc = re.sub(r"[▲▼]", "", t).strip()
                loc_lines.append((loc, lb))
                if ("▲" in t) or ("▼" in t):
                    page_marker = loc
                continue
            if len(t) < 70 and any(overlaps(lb, f["bbox"]) for f in figs):
                continue                                         # other in-figure label
            if below_caption:
                bf = below_fig(lb, ln["size"])
                if bf is not None:
                    below_caps.setdefault(id(bf), []).append((lb[1], t)); continue
            content.append(ln)
        def _yc(b):
            return (b[1] + b[3]) / 2
        for f in figs:
            fb = f["bbox"]
            creds = [t for (t, b) in credit_lines if fb[1] - 8 <= _yc(b) <= fb[3] + 8]
            credit = " / ".join(dict.fromkeys(creds))
            if below_caption:
                bc = " ".join(t for _, t in sorted(below_caps.get(id(f), [])))
                f["cap"] = _section_caption(bc, credit)
            else:
                locs = [t for (t, b) in loc_lines if overlaps(b, fb)]
                loc = locs[0] if locs else page_marker
                f["cap"] = _fig_caption(binom, loc, credit)
        sizes = Counter(round(ln["size"]) for ln in content)
        body_size = sizes.most_common(1)[0][0] if sizes else 10
        head_sizes = sorted({round(ln["size"]) for ln in content
                             if round(ln["size"]) > body_size}, reverse=True)
        def level_of(sz):
            sz = round(sz)
            return head_sizes.index(sz) + 2 if sz in head_sizes else None
        fw = [f for f in figs if (f["bbox"][2] - f["bbox"][0]) > 0.6 * pw]
        def zone(y0):
            # a full-width image counts as "above" an item once the item's top reaches
            # the image's top, so a column image overlapping it is emitted AFTER it
            return sum(1 for f in fw if f["bbox"][1] <= y0 + 2)
        seq = []
        for ln in content:
            xc = (ln["bbox"][0] + ln["bbox"][2]) / 2
            seq.append((zone(ln["bbox"][1]), 0 if xc < mid else 1, ln["bbox"][1], "line", ln))
        for f in figs:
            if f in fw:
                continue
            xc = (f["bbox"][0] + f["bbox"][2]) / 2
            seq.append((zone(f["bbox"][1]), 0 if xc < mid else 1, f["bbox"][1], "fig", f))
        byzone = defaultdict(list)
        for it in seq:
            byzone[it[0]].append(it)

        def emit_fig(f):
            nonlocal fig_no
            fn = _save_figure(doc, f["parts"], f["vertical"], out_dir,
                              "%s_p%d_%d" % (slug, pno, fig_no))
            fig_no += 1
            items.append(("fig", fn, f["cap"]))

        def emit_zone(zitems):
            buf = []
            def flush():
                if buf:
                    items.append(("para", _para_render(list(buf))))
                    del buf[:]
            for _z, _col, _y, kind, obj in sorted(zitems, key=lambda t: (t[1], t[2])):
                if kind == "fig":
                    flush(); emit_fig(obj); continue
                ln = obj
                lvl = level_of(ln["size"])
                if lvl is not None and len(ln["text"].strip()) < 60:
                    flush()
                    items.append(("head", lvl, ln["text"].strip()))
                    hdr_done["v"] = True
                    continue
                if pno == first_pno and not hdr_done["v"] and not keep_big:
                    if special_header and any("Times" in sp.get("font", "") for sp in ln["spans"]):
                        hdr_done["v"] = True          # scoped fix (e.g. Pseudomugil signifer)
                    else:
                        header_lines.append(ln); continue
                if buf:
                    last = buf[-1]
                    gap = ln["bbox"][1] - last["bbox"][1]
                    lh = last["bbox"][3] - last["bbox"][1]
                    same_col = ((last["bbox"][0] + last["bbox"][2]) / 2 < mid) == \
                               ((ln["bbox"][0] + ln["bbox"][2]) / 2 < mid)
                    if same_col and gap > lh * 1.7:
                        flush()
                    elif (not same_col) and last["text"].strip()[-1:] in ".!?:”\"":
                        flush()
                buf.append(ln)
            flush()

        for z in range(len(fw) + 1):
            emit_zone(byzone.get(z, []))
            if z < len(fw):
                emit_fig(fw[z])
    return items, header_lines

def species_slug(genus, species):
    return ("%s_%s" % (genus, species)).lower().replace(" ", "_")

def _parse_header(header_lines):
    """Header block -> (attribution, common_name, [(syn_name, syn_author), ...]).
    Synonyms are split on the PDF's italic runs (each name is italic)."""
    segs = []
    for ln in header_lines:
        for sp in ln["spans"]:
            if sp["text"]:
                segs.append((sp["text"], _italic_span(sp)))
    i, lead = 0, ""
    while i < len(segs) and not segs[i][1]:          # leading roman = attribution + common
        lead += segs[i][0]; i += 1
    lead = re.sub(r"\s+", " ", lead).strip()
    m = re.match(r"^(\(?[^()]*?\d{4}\)?)\s*(.*)$", lead)
    attribution = m.group(1).strip() if m else ""
    common = (m.group(2) if m else lead).strip()
    syns, name, rest = [], "", ""
    while i < len(segs):
        txt, ital = segs[i]
        if ital:
            if name and rest.strip():
                syns.append((name, rest)); name, rest = "", ""
            name += txt
        else:
            rest += txt
        i += 1
    if name.strip():
        syns.append((name, rest))
    syns = [(re.sub(r"\s+", " ", n).strip(), re.sub(r"\s+", " ", a).strip()) for n, a in syns]
    return attribution, common, syns

def build_species_account(genus, species, pdf_pages, section_slug, citation=""):
    """Render a faithful, verbatim species account with all figures in book order."""
    out_dir = os.path.join(SRC, section_slug)
    os.makedirs(out_dir, exist_ok=True)
    binom = "%s %s" % (genus, species)
    raw0 = fitz.open(PDF)[pdf_pages[0] - 1].get_text("text")
    common = ""
    m = re.search(re.escape(binom) + r"\s*\n\s*(.+?,\s*\d{4})\s*\n\s*([A-Z][A-Za-z '\-]+?)\s*\n", raw0)
    if m:
        citation = citation or m.group(1).strip()
        common = m.group(2).strip()
    is_special = (genus, species) == ("Pseudomugil", "signifer")
    items, header_lines = extract_account(pdf_pages, out_dir, species_slug(genus, species),
                                          binom, citation, common, special_header=is_special)
    has_head = any(it[0] == "head" for it in items)
    if is_special:
        attribution, common_h, syns = _parse_header_lines(header_lines)
    else:
        attribution, common_h, syns = _parse_header(header_lines) if has_head else ("", "", [])
    citation = attribution or citation
    common = common_h or common

    def render_fig(it):
        _, fn, cap = it
        return ('      <div class="image-block"><img src="%s" alt="%s">'
                '<div class="image-caption">%s</div></div>' % (fn, html.escape(binom), cap))

    lead_idx = next((k for k, it in enumerate(items) if it[0] == "fig"), None)
    parts = []
    if lead_idx is not None:                        # first image comes before any text
        parts.append(render_fig(items[lead_idx]))
    parts.append('      <h1><span class="scientific-name">%s</span></h1>' % html.escape(binom))
    if citation:
        parts.append('      <p class="author-citation">%s</p>' % html.escape(citation))
    if common:
        parts.append('      <p class="common-name">%s</p>' % html.escape(common))
    if syns:
        lis = "".join('<li><span class="scientific-name">%s</span> %s</li>'
                      % (html.escape(n), html.escape(a)) for n, a in syns)
        parts.append('      <h2>Synonymy</h2>')
        parts.append('      <ul class="synonymy">%s</ul>' % lis)
    elif not has_head and header_lines:
        parts.append("      " + _para_render(header_lines))
    seen_head, inserted_ss = False, False
    for k, it in enumerate(items):
        if k == lead_idx:
            continue
        if it[0] == "fig":
            parts.append(render_fig(it))
        elif it[0] == "head":
            seen_head = True
            _, lvl, text = it
            parts.append("      <h%d>%s</h%d>" % (lvl, html.escape(text), lvl))
        else:
            if is_special and not seen_head and not inserted_ss:
                parts.append("      <h2>Species Summary</h2>"); inserted_ss = True
            parts.append("      " + it[1])

    fname = species_slug(genus, species) + ".html"
    label = "Rainbowfish Species" if section_slug == "rainbowfish_species" else "Blue Eye Species"
    page = render_page(binom, "\n".join(parts), active_slug=section_slug, prefix="../",
                       breadcrumb=['<a href="%s.html">%s</a>' % (section_slug, label),
                                   '<span class="scientific-name">%s</span>' % html.escape(binom)])
    write(os.path.join(out_dir, fname), page)
    return fname


# --------------------------------------------------------------- contents -----
# ---------------------------------------------------------- restored chrome ---
def menu_html(active_slug, prefix):
    rows = []
    for title, slug, _ in SECTIONS:
        cls = ' class="active"' if slug == active_slug else ""
        rows.append('      <li%s><a href="%s%s/%s.html">%s</a></li>'
                    % (cls, prefix, slug, slug, html.escape(title)))
    return '<ul class="menu">\n' + "\n".join(rows) + "\n    </ul>"

def render_page(title, body_html, active_slug=None, prefix="", breadcrumb=None):
    css = prefix + "style.css"
    banner = prefix + "assets/rainbow_2a.jpg"
    home = prefix + "index.html"
    contents = prefix + "contents.html"
    crumb = ""
    if breadcrumb:
        crumb_parts = ['<a href="%s">Home</a>' % home,
                       '<a href="%s">Contents</a>' % contents] + breadcrumb
        crumb = '\n      <div class="breadcrumbs">' + " &raquo; ".join(crumb_parts) + "</div>"
    return (
'<!DOCTYPE html>\n'
'<html lang="en">\n'
'<head>\n'
'  <meta charset="UTF-8">\n'
'  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
'  <title>' + html.escape(title) + ' — Home of the Rainbowfish</title>\n'
'  <link rel="stylesheet" href="' + css + '">\n'
'</head>\n'
'<body>\n'
'  <header class="site-banner">\n'
'    <a href="' + home + '"><img src="' + banner + '" alt="Home of the Rainbowfish" width="780" height="100"></a>\n'
'  </header>\n'
'  <div class="layout">\n'
'    <nav class="side-menu">\n'
'      ' + menu_html(active_slug, prefix) + '\n'
'    </nav>\n'
'    <main class="content-wrapper">' + crumb + '\n'
+ body_html + '\n'
'    </main>\n'
'  </div>\n'
'  <footer class="site-footer">\n'
'    <p>Original content from <em>Rainbowfishes &mdash; Their Care &amp; Keeping in Captivity</em>\n'
'    (Adrian R. Tappin, 2011). &copy; Adrian R. Tappin. Republished by ANGFA.</p>\n'
'  </footer>\n'
'</body>\n'
'</html>\n')

DRAFT_NOTE = ('      <p class="draft-note">First-draft extract &mdash; section pages are '
              'pending conversion to full verbatim text.</p>')

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def section_dir(slug):
    return os.path.join(SRC, slug, slug + ".html")

def parse_species():
    with open(os.path.join(REF, "contents.html"), encoding="utf-8") as f:
        h = f.read()
    order, cur_fam = [], None
    token = re.compile(
        r'<strong>(Melanotaeniidae|Pseudomugilidae)</strong>'
        r'|<strong><em>([A-Z][a-z]+)</em></strong>'
        r'|<li>\s*<em>([a-z][A-Za-z]+)</em>([^<]*)', re.S)
    for m in token.finditer(h):
        fam, genus, sp, cit = m.groups()
        if fam:
            cur_fam = fam; order.append((fam, []))
        elif genus and cur_fam:
            order[-1][1].append((genus, []))
        elif sp and cur_fam and order and order[-1][1]:
            order[-1][1][-1][1].append((sp, html.unescape(cit.strip())))
    return order

def citations_map():
    cmap = {}
    for _fam, genera in parse_species():
        for genus, species in genera:
            for sp, cit in species:
                cmap["%s %s" % (genus, sp)] = cit
    return cmap

def species_index_html(species_list, intro_html, family, common, citations, linked):
    parts = [intro_html, '      <h2>Species list</h2>',
             '      <h3>%s <span style="font-weight:400">&mdash; %s</span></h3>' % (family, common),
             '      <ul class="species-list">']
    state = {"cur": None, "open": False}
    def close():
        if state["open"]:
            parts.append('          </ul>'); parts.append('        </li>'); state["open"] = False
    for genus, epithet, full in species_list:
        if genus is None:
            close(); state["cur"] = None
            href = linked.get(("__undetermined__", full))
            if href:
                parts.append('        <li><a href="%s">%s</a></li>' % (href, html.escape(full)))
            else:
                parts.append('        <li>%s</li>' % html.escape(full))
            continue
        if genus != state["cur"]:
            close()
            parts.append('        <li><span class="scientific-name">%s</span>' % genus)
            parts.append('          <ul>'); state["cur"] = genus; state["open"] = True
        binom = "%s %s" % (genus, epithet)
        cit = html.escape(citations.get(binom, ""))
        label = '<span class="scientific-name">%s</span>' % html.escape(binom) + ((" " + cit) if cit else "")
        if (genus, epithet) in linked:
            parts.append('            <li><a href="%s">%s</a></li>' % (linked[(genus, epithet)], label))
        else:
            parts.append('            <li>%s</li>' % label)
    close()
    parts.append('      </ul>')
    return "\n".join(parts)

RF_INTRO = ('      <p>The family Melanotaeniidae &mdash; the rainbowfishes &mdash; is the larger '
            'of the two families in the book. Each species below links to its full illustrated '
            'account, reproduced verbatim from the book with all figures. (The four '
            '<span class="scientific-name">Melanotaenia splendida</span> subspecies are covered '
            'within the <span class="scientific-name">M. splendida</span> account.)</p>')

BE_INTRO = ('      <p>The family Pseudomugilidae &mdash; the blue-eyes &mdash; is a small group of '
            'mostly diminutive, often vividly coloured fishes closely related to the rainbowfishes. '
            'Each species below links to its full illustrated account, reproduced verbatim from the '
            'book with all figures.</p>')

SECTION_LEAD = {"background": [7, 8, 9], "introduction": [17, 18, 19],
                "history_of_rainbowfishes_in_captivity": [20, 21, 22]}

def build_sections(spset, citations, linked):
    for title, slug, _ in SECTIONS:
        if slug == "rainbowfish_species":
            body = '      <h1>%s</h1>\n' % html.escape(title) + species_index_html(
                spset["Rainbowfish Species"], RF_INTRO, "Melanotaeniidae", "Rainbowfishes", citations, linked)
        elif slug == "blue_eye_species":
            body = '      <h1>%s</h1>\n' % html.escape(title) + species_index_html(
                spset["Blue Eye Species"], BE_INTRO, "Pseudomugilidae", "Blue-eyes", citations, linked)
        else:
            pages = LEAD_PAGES.get(slug) or SECTION_LEAD.get(slug, [])
            paras = clean_paragraphs(pages) if pages else []
            body = '      <h1>%s</h1>\n' % html.escape(title) + DRAFT_NOTE + "\n" + paras_to_html(paras, 8)
        page = render_page(title, body, active_slug=slug, prefix="../",
                           breadcrumb=['<span>%s</span>' % html.escape(title)])
        write(section_dir(slug), page)

def build_undetermined(pdf_pages, section_slug):
    """The book's 'Undetermined Species' section as one page; Melanotaenia sp.
    forms become headings."""
    out_dir = os.path.join(SRC, section_slug)
    slug = "rainbowfishes_undetermined"
    items, _ = extract_account(pdf_pages, out_dir, slug, "", "", "", keep_big=True)
    parts = ["      <h1>Rainbowfishes &mdash; Undetermined Species</h1>",
             '      <p class="author-citation">Undescribed and provisionally identified rainbowfishes.</p>']
    i = 0
    while i < len(items):
        it = items[i]
        if it[0] == "fig":
            _, fn, cap = it
            img = '<img src="%s" alt="Undetermined rainbowfish">' % fn
            parts.append('      <div class="image-block">%s<div class="image-caption">%s</div></div>' % (img, cap))
        elif it[0] == "head":
            _, lvl, text = it
            if i + 1 < len(items) and items[i + 1][0] == "head" and items[i + 1][2].startswith("("):
                text = text + " " + items[i + 1][2]; i += 1
            disp = re.sub(r"^([A-Z][a-z]+) (sp\.)",
                          r'<span class="scientific-name">\1 \2</span>', html.escape(text))
            parts.append("      <h%d>%s</h%d>" % (lvl, disp, lvl))
        else:
            parts.append("      " + it[1])
        i += 1
    page = render_page("Undetermined Species", chr(10).join(parts),
                       active_slug=section_slug, prefix="../",
                       breadcrumb=['<a href="%s.html">Rainbowfish Species</a>' % section_slug,
                                   "<span>Undetermined Species</span>"])
    write(os.path.join(out_dir, slug + ".html"), page)
    return slug + ".html"

def _slugify(t):
    return re.sub(r"[^a-z0-9]+", "_", t.lower().replace("&", "and")).strip("_")

def _hnorm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))

def toc_subs(sections, heading):
    for h, subs in sections:
        if h == heading:
            return subs
    return []

def _match_subs(subs, items):
    """Align Excel subsidiary headings to head items, in order. Returns [(sub, idx|None)]."""
    heads = [(k, it[2]) for k, it in enumerate(items) if it[0] == "head"]
    out, pos = [], 0
    for s in subs:
        ns, found = _hnorm(s), None
        for jj in range(pos, len(heads)):
            nh = _hnorm(heads[jj][1])
            if nh == ns or nh.startswith(ns) or ns.startswith(nh):
                found = jj; break
        if found is None:                                   # token fallback (e.g. Green-water)
            toks = re.findall(r"[a-z]{5,}", s.lower().replace("&", "and"))
            tok = max(toks, key=len) if toks else ""
            if tok:
                for jj in range(pos, len(heads)):
                    if tok in _hnorm(heads[jj][1]):
                        found = jj; break
        if found is not None:
            out.append((s, heads[found][0])); pos = found + 1
        else:
            out.append((s, None))
    return out

def _render_items(chunk, skip_title=None):
    st = _hnorm(skip_title) if skip_title else None
    def _is_title(t):
        h = _hnorm(t)
        return st is not None and (h == st or (len(st) > 8 and h.replace("s", "") == st.replace("s", "")))
    parts = []
    for it in chunk:
        if it[0] == "fig":
            _, fn, cap = it
            parts.append('      <div class="image-block"><img src="%s" alt="">'
                         '<div class="image-caption">%s</div></div>' % (fn, cap))
        elif it[0] == "head":
            if _is_title(it[2]):
                continue
            parts.append("      <h2>%s</h2>" % html.escape(it[2]))
        else:
            parts.append("      " + it[1])
    return parts

def _page_nav(up_href, up_label, next_href, next_label):
    """Bottom nav: always a link up to the main Contents, an optional link up to the
    section landing, and an optional link to the next page / next section."""
    if not up_href and not next_href:
        return []
    left = ('<a href="%s">&uarr; %s</a>' % (up_href, up_label)) if up_href else ""
    right = ('<a href="%s">%s &rarr;</a>' % (next_href, next_label)) if next_href else ""
    return ['      <div class="section-nav">',
            '        <span>%s</span>' % left,
            '        <span>%s</span>' % right,
            '      </div>']

def _decoded_items(pdf_pages, out_dir, slug, list_mode=False):
    """Front-matter items (subset font decoded with +31 via rawdict). Groups lines into
    real paragraphs by vertical gap, preserves italic runs, and (list_mode) renders a
    single-spaced two-column list (used for Photographic Contributors)."""
    doc = fitz.open(PDF)
    items, fig_no = [], 0
    for pno in pdf_pages:
        p = doc[pno - 1]
        figpieces = []
        for im in p.get_image_info(xrefs=True):
            b = im["bbox"]
            if (b[3] - b[1]) < 100:
                continue
            d = doc.extract_image(im["xref"])
            fn = "%s_p%d_%d.%s" % (slug, pno, fig_no, d["ext"]); fig_no += 1
            with open(os.path.join(out_dir, fn), "wb") as fh:
                fh.write(d["image"])
            figpieces.append(fn)
        lines_ = []
        for blk in p.get_text("rawdict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk["lines"]:
                segs = []
                for sp in ln["spans"]:
                    it = ("Italic" in sp.get("font", "")) or bool(sp.get("flags", 0) & 2)
                    heiti = "Heiti" in sp.get("font", "")
                    t = "".join(chr(ord(c["c"]) + 31)
                                if (heiti and 1 <= ord(c["c"]) <= 95 and ord(c["c"]) != 32)
                                else c["c"] for c in sp["chars"])
                    if not t:
                        continue
                    if segs and segs[-1][1] == it:
                        segs[-1] = (segs[-1][0] + t, it)
                    else:
                        segs.append((t, it))
                plain = "".join(t for t, _ in segs)
                if not plain.strip():
                    continue
                lhtml = "".join(("<em>%s</em>" % html.escape(t)) if i else html.escape(t)
                                for t, i in segs)
                b = ln["bbox"]
                col = 0 if b[0] < p.rect.width / 2 else 1   # use LEFT edge (short justified last-lines are single-column)
                lines_.append((col, b[1], lhtml, plain, max(sp["size"] for sp in ln["spans"])))
        lines_.sort(key=lambda l: (l[0], l[1]))

        if list_mode:
            names = [l[2] for l in lines_ if l[4] < 16]
            if names:
                items.append(("para", '<p class="contributors">%s</p>' % "<br>".join(names)))
            for fn in figpieces:
                items.append(("fig", fn, ""))
            continue

        cur, prev = None, None
        def flush():
            nonlocal cur
            if cur:
                items.append(("para", "<p>%s</p>" % cur.strip())); cur = None
        for l in lines_:
            col, y, lhtml, plain, sz = l
            if round(sz) >= 16:
                flush(); items.append(("head", 2, plain)); prev = None; continue
            gap = (y - prev[1]) if (prev and prev[0] == col) else 999
            if cur and gap < 30 and abs(sz - prev[4]) < 2:
                cur += " " + lhtml
            else:
                flush(); cur = lhtml
            prev = l
        flush()
        for fn in figpieces:
            items.append(("fig", fn, ""))
    return items

def build_section_multipage(title, slug, divider_page, content_pages, subs, next_section=None,
                            enrich_refs=False):
    """Landing (divider hero + hyperlinked contents) + one page per subsidiary heading,
    with within-section next / up nav. No-subsidiary sections render as one page."""
    out_dir = os.path.join(SRC, slug)
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(PDF)
    drop_fn = photo_fn = None
    credit = ""
    if divider_page:
        dp = doc[divider_page - 1]
        dimgs = [dict(bbox=im["bbox"], xref=im["xref"]) for im in dp.get_image_info(xrefs=True)
                 if (im["bbox"][3] - im["bbox"][1]) >= 100]
        dimgs.sort(key=lambda i: i["bbox"][1])
        if dimgs:
            d = doc.extract_image(dimgs[0]["xref"]); drop_fn = "%s_hero_drop.%s" % (slug, d["ext"])
            open(os.path.join(out_dir, drop_fn), "wb").write(d["image"])
        if len(dimgs) > 1:
            big = max(dimgs[1:], key=lambda i: (i["bbox"][2]-i["bbox"][0])*(i["bbox"][3]-i["bbox"][1]))
            d = doc.extract_image(big["xref"]); photo_fn = "%s_hero_photo.%s" % (slug, d["ext"])
            open(os.path.join(out_dir, photo_fn), "wb").write(d["image"])
        for blk in dp.get_text("dict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk["lines"]:
                m = re.match(r"Photo:\s*(.+)", " ".join(s["text"] for s in ln["spans"]).strip())
                if m:
                    credit = m.group(1).strip()

    items, _ = extract_account(content_pages, out_dir, slug, "", "", "", keep_big=True,
                               below_caption=True)

    if photo_fn:
        cap = ("photo &copy; " + html.escape(credit)) if credit else ""
        hero_photo = ('      <div class="image-block"><img src="%s" alt="">'
                      '<div class="image-caption">%s</div></div>' % (photo_fn, cap))
    else:
        hero_photo = ""
        for k, it in enumerate(items):
            if it[0] == "fig":
                hero_photo = ('      <div class="image-block"><img src="%s" alt="">'
                              '<div class="image-caption">%s</div></div>' % (it[1], it[2]))
                del items[k]; break

    drop_src = drop_fn if drop_fn else "../assets/water_drop.png"
    hero = ['      <div class="divider-hero">',
            '        <img class="drop" src="%s" alt="">' % drop_src,
            '        <span class="rf">Rainbowfishes</span>',
            '        <h1>%s</h1>' % html.escape(title),
            '      </div>']
    if hero_photo:
        hero.append(hero_photo)

    if subs:
        idxs = [(s, i) for s, i in _match_subs(subs, items) if i is not None]
        sslug, used = {}, {slug}
        for s in subs:
            base = _slugify(s)
            if base == slug:
                base = slug + "_overview"
            ss, k = base, 2
            while ss in used:
                ss = "%s_%d" % (base, k); k += 1
            used.add(ss); sslug[s] = ss
        toc = hero + ['      <h2>Contents</h2>', '      <ol class="section-toc">']
        for s in subs:
            toc.append('        <li><a href="%s.html">%s</a></li>' % (sslug[s], html.escape(s)))
        toc.append('      </ol>')
        start = (sslug[idxs[0][0]] + ".html", "Next: " + idxs[0][0]) if idxs else (None, None)
        toc += _page_nav(None, None, start[0], start[1])
        write(os.path.join(out_dir, slug + ".html"),
              render_page(title, chr(10).join(toc), active_slug=slug, prefix="../",
                          breadcrumb=["<span>%s</span>" % html.escape(title)]))
        for n, (s, i) in enumerate(idxs):
            end = idxs[n + 1][1] if n + 1 < len(idxs) else len(items)
            parts = ["      <h1>%s</h1>" % html.escape(s)] + _render_items(items[i + 1:end], skip_title=title)
            if n + 1 < len(idxs):
                nh, nl = sslug[idxs[n + 1][0]] + ".html", "Next: " + idxs[n + 1][0]
            else:
                nh, nl = None, None
            parts += _page_nav(slug + ".html", title + " contents", nh, nl)
            write(os.path.join(out_dir, sslug[s] + ".html"),
                  render_page(title + " — " + s, chr(10).join(parts),
                              active_slug=slug, prefix="../",
                              breadcrumb=['<a href="%s.html">%s</a>' % (slug, html.escape(title)),
                                          "<span>%s</span>" % html.escape(s)]))
        return len(idxs)

    content = items
    if content and content[0][0] == "head" and _hnorm(content[0][2]) == _hnorm(title):
        content = content[1:]
    rendered = _render_items(content, skip_title=title)
    if enrich_refs:
        rendered = [_enrich_reference(x) if x.lstrip().startswith("<p>") else x
                    for x in rendered]
    body = hero + rendered
    write(os.path.join(out_dir, slug + ".html"),
          render_page(title, chr(10).join(body), active_slug=slug, prefix="../",
                      breadcrumb=["<span>%s</span>" % html.escape(title)]))
    return 0

def build_background(next_section=None):
    title, slug = "Background", "background"
    out_dir = os.path.join(SRC, slug)
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(PDF)
    cover = "%s_cover.png" % slug
    doc[0].get_pixmap(dpi=110).save(os.path.join(out_dir, cover))
    BG = [("Copyright", [5, 6], "copyright"), ("Aims", [7], "aims"),
          ("About the Author", [8], ""), ("Foreword", [9, 10], ""),
          ("Photographic Contributors", [11, 12], "list")]
    sslug = {n: _slugify(n) for n, _, _ in BG}

    hero = ['      <div class="divider-hero">',
            '        <img class="drop" src="../assets/water_drop.png" alt="">',
            '        <span class="rf">Rainbowfishes</span>',
            '        <h1>Background</h1>',
            '      </div>',
            '      <div class="image-block"><img src="%s" alt="Book cover">'
            '<div class="image-caption">Rainbowfishes &mdash; Their Care &amp; Keeping in '
            'Captivity (Adrian R. Tappin, 2011)</div></div>' % cover,
            '      <h2>Contents</h2>', '      <ol class="section-toc">']
    for n, _, _ in BG:
        hero.append('        <li><a href="%s.html">%s</a></li>' % (sslug[n], html.escape(n)))
    hero.append('      </ol>')
    hero += _page_nav(None, None, sslug[BG[0][0]] + ".html", "Next: " + BG[0][0])
    write(os.path.join(out_dir, slug + ".html"),
          render_page(title, chr(10).join(hero), active_slug=slug, prefix="../",
                      breadcrumb=["<span>Background</span>"]))

    for i, (name, pages, mode) in enumerate(BG):
        items = _decoded_items(pages, out_dir, slug, list_mode=(mode == "list"))
        parts = ["      <h1>%s</h1>" % html.escape(name)]
        if mode == "copyright":
            heads = [it[2].strip() for it in items if it[0] == "head"]
            body = [it for it in items if it[0] != "head"]
            if len(heads) >= 3:
                parts.append('      <p class="doc-name"><em>%s: %s</em> by %s</p>'
                             % (html.escape(heads[0]), html.escape(heads[1]), html.escape(heads[2])))
            parts += _render_items(body)
        elif mode == "aims":
            parts.append('      <div class="justify">')
            parts += _render_items(items, skip_title=name)
            parts.append('      </div>')
        else:
            parts += _render_items(items, skip_title=name)
        if i + 1 < len(BG):
            nh, nl = sslug[BG[i + 1][0]] + ".html", "Next: " + BG[i + 1][0]
        else:
            nh, nl = None, None
        parts += _page_nav(slug + ".html", "Background contents", nh, nl)
        write(os.path.join(out_dir, sslug[name] + ".html"),
              render_page("Background — " + name, chr(10).join(parts),
                          active_slug=slug, prefix="../",
                          breadcrumb=['<a href="%s.html">Background</a>' % slug,
                                      "<span>%s</span>" % html.escape(name)]))


def build_contents():
    cards = []
    for title, slug, desc in SECTIONS:
        cards.append(
            f'        <li><a href="{slug}/{slug}.html"><strong>{html.escape(title)}</strong></a>'
            f'<br><span class="muted">{html.escape(desc)}</span></li>')
    body = f"""      <h1>Contents</h1>
      <p>This site presents the complete text of <em>Rainbowfishes &mdash; Their Care
      &amp; Keeping in Captivity</em> (Adrian R. Tappin, 2011), reorganised into the
      sections below. Use the menu on the left on any page, or start here.</p>
      <ul class="contents-list">
{chr(10).join(cards)}
      </ul>"""
    page = render_page("Contents", body, active_slug=None, prefix="",
                       breadcrumb=None)
    write(os.path.join(SRC, "contents.html"), page)

# ------------------------------------------------------- carried-over pages ---
def build_home():
    with open(os.path.join(REF, "home.html"), encoding="utf-8") as f:
        h = f.read()
    # remove Kangaroo Tour link, repoint nav to the new static structure
    h = re.sub(r'<a href="Welcome.htm">Kangaroo Tour</a>\s*\|\s*', "", h)
    h = h.replace('href="Melano.htm"', 'href="contents.html"')
    h = h.replace('href="Book.htm"', 'href="book.html"')
    h = h.replace('href="about.htm"', 'href="about.html"')
    h = h.replace('src="Rainbow_home.png"', 'src="assets/Rainbow_home.png"')
    h = h.replace('src="nla_logo_white.gif"', 'src="assets/nla_logo_white.gif"')
    h = h.replace('href="favicon.ico"', 'href="assets/favicon.ico"')
    write(os.path.join(SRC, "index.html"), h)

def build_carryover(name_in, name_out):
    with open(os.path.join(REF, name_in), encoding="utf-8") as f:
        h = f.read()
    h = re.sub(r'<a href="Welcome.htm">Kangaroo Tour</a>\s*\|?\s*', "", h)
    h = h.replace('href="Melano.htm"', 'href="contents.html"')
    h = h.replace('href="Book.htm"', 'href="book.html"')
    h = h.replace('href="about.htm"', 'href="about.html"')
    h = h.replace('href="index.html"', 'href="index.html"')
    # localise any image/icon references to assets/
    h = re.sub(r'(src|href)="([\w.\-]+\.(?:png|jpg|jpeg|gif|ico))"',
               r'\1="assets/\2"', h)
    write(os.path.join(SRC, name_out), h)

# ------------------------------------------------------------------ assets ----
def copy_assets():
    dst = os.path.join(SRC, "assets")
    os.makedirs(dst, exist_ok=True)
    for fn in os.listdir(SITE):
        shutil.copyfile(os.path.join(SITE, fn), os.path.join(dst, fn))
    ims = [i for i in fitz.open(PDF)[130].get_image_info(xrefs=True)
           if (i["bbox"][3] - i["bbox"][1]) >= 100]           # shared water-drop hero
    if ims:
        d = fitz.open(PDF).extract_image(min(ims, key=lambda i: i["bbox"][1])["xref"])
        Image.open(io.BytesIO(d["image"])).convert("RGB").save(os.path.join(dst, "water_drop.png"))

# --------------------------------------------------------------------- css ----
CSS = """/* Home of the Rainbowfish — shared stylesheet (first draft) */
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap');

:root{
  --bg-main:#FFFFFF; --color-heading:#000000; --color-text:#111111;
  --color-link:#002B66; --color-link-hover:#0056B3; --border-muted:#E2E8F0;
  --muted:#64748B;
  --font-heading:'Merriweather',Georgia,serif;
  --font-body:'Source Sans 3',Arial,sans-serif;
}
*{box-sizing:border-box}
body{background:var(--bg-main);color:var(--color-text);font-family:var(--font-body);
  line-height:1.7;margin:0;padding:0}
a{color:var(--color-link);text-decoration:underline}
a:hover{color:var(--color-link-hover)}

.site-banner{text-align:center;padding:18px 10px 0}
.site-banner img{max-width:100%;height:auto}

.layout{display:flex;gap:32px;max-width:1140px;margin:0 auto;padding:20px}
.side-menu{flex:0 0 220px}
.menu{list-style:none;margin:0;padding:0;border-top:2px solid var(--color-heading);
  position:sticky;top:16px}
.menu li{border-bottom:1px solid var(--border-muted)}
.menu li a{display:block;padding:9px 8px;text-decoration:none;font-weight:600;
  font-size:.95rem}
.menu li.active a{color:var(--color-heading);border-left:3px solid var(--color-link);
  padding-left:10px}
.menu li a:hover{background:#F1F5F9}

.content-wrapper{flex:1;min-width:0;max-width:820px}
.breadcrumbs{font-size:.9rem;color:var(--muted);margin-bottom:18px}
.breadcrumbs a{color:var(--color-link);text-decoration:none}
.breadcrumbs a:hover{text-decoration:underline}

h1{font-family:var(--font-heading);color:var(--color-heading);font-weight:700;
  font-size:2.2rem;line-height:1.2;margin:0 0 18px}
h2,h3{font-family:var(--font-heading);color:var(--color-heading);font-weight:700;
  margin-top:34px;border-bottom:1px solid var(--border-muted);padding-bottom:6px}
h3{font-size:1.15rem;border-bottom:none;margin-top:22px}
p{margin:0 0 18px;font-size:1.05rem}
.author-citation{color:#4A5568;font-size:1.05rem;margin-top:-8px}
.muted{color:var(--muted)}
.draft-note{background:#FFF7ED;border:1px solid #FED7AA;color:#9A3412;
  padding:8px 12px;border-radius:4px;font-size:.9rem}

.scientific-name{font-style:italic;font-family:inherit;font-size:inherit;font-weight:inherit}
.book-list{margin:0 0 18px 1.6em;padding:0}
.book-list li{margin:0 0 8px;font-size:1.05rem}
.common-name{color:#334155;font-size:1.05rem;font-weight:600;margin:-6px 0 14px}
.synonymy{list-style:none;padding-left:0;color:#475569;font-size:.95rem;margin:0 0 18px}
.synonymy li{padding:1px 0}
.divider-hero{text-align:center;margin-bottom:6px}
.divider-hero .drop{max-width:320px;height:auto;display:block;margin:0 auto 2px}
.divider-hero .rf{font-family:var(--font-heading);color:var(--color-link);font-size:1.7rem;display:block}
.divider-hero h1{border:none;margin:2px 0 12px}
.section-toc{line-height:1.85}
.page-image{border:1px solid var(--border-muted);margin:14px 0;background:#fff}
.page-image img{max-width:100%;height:auto;display:block;margin:0 auto}
.doc-name{font-size:1.1rem;margin:0 0 18px;color:#334155}
.justify p{text-align:justify}
.contributors{line-height:1.6}
.section-nav{display:flex;justify-content:space-between;gap:16px;margin-top:36px;padding-top:14px;border-top:1px solid var(--border-muted);font-weight:600}
a.doi{font-size:.9rem;word-break:break-all}

.image-block{background:#F8FAFC;border:1px solid var(--border-muted);border-radius:4px;
  padding:10px;margin:22px 0;text-align:center}
.image-block img{max-width:100%;height:auto;display:block;margin:0 auto}
.image-caption{font-size:.9rem;color:var(--muted);font-style:italic;margin-top:8px}

.parameter-table{width:100%;border-collapse:collapse;margin:22px 0}
.parameter-table td{padding:12px 10px;border-bottom:1px solid var(--border-muted);
  vertical-align:top}
.parameter-table tr td:first-child{font-weight:600;color:#334155;width:32%}

.contents-list,.species-list{list-style:none;padding-left:0}
.contents-list li{padding:10px 0;border-bottom:1px solid var(--border-muted)}
.species-list ul{list-style:none}
.species-list>li{margin:8px 0;font-weight:600}
.species-list ul li{font-weight:400;padding:2px 0}

.site-footer{max-width:1140px;margin:0 auto;padding:24px 20px;color:var(--muted);
  font-size:.85rem;border-top:1px solid var(--border-muted)}

@media(max-width:760px){
  .layout{flex-direction:column;gap:16px}
  .side-menu{flex:none}
  .menu{position:static}
}
"""

# ------------------------------------------------------------------- main -----
def locate_accounts():
    """Find each species account by its title (>=14pt binomial/trinomial line) in the
    species region, and give each a fresh page range up to the next account."""
    RF_START, RF_END, BE_END = 181, 440, 490   # PDF pages; Blue-Eye divider at 441
    doc = fitz.open(PDF)
    titles = []
    for pno in range(RF_START, BE_END + 1):
        if RF_END < pno < 442:
            continue
        big = []
        for blk in doc[pno - 1].get_text("dict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk["lines"]:
                if max(s["size"] for s in ln["spans"]) >= 13:   # titles 14-16pt; headings are 12
                    big.append((ln["bbox"][1], " ".join(s["text"] for s in ln["spans"]).strip()))
        big.sort()
        found, j = [], 0
        while j < len(big):
            t = big[j][1]
            if re.fullmatch(r"[A-Z][a-z]+ [a-z]+( [a-z]+)?", t):
                found.append((big[j][0], t)); j += 1
            elif re.fullmatch(r"[A-Z][a-z]{4,}", t) and j + 1 < len(big)                     and re.fullmatch(r"[a-z]{4,}", big[j + 1][1]):   # title wrapped to 2 lines
                found.append((big[j][0], t + " " + big[j + 1][1])); j += 2
            else:
                j += 1
        if found:
            titles.append((pno, found[0][1]))
    seen = {}
    for pno, name in titles:
        seen.setdefault(name, pno)
    ordered = sorted(seen.items(), key=lambda kv: kv[1])
    out = []
    for i, (name, pno) in enumerate(ordered):
        fam_end = RF_END if pno <= RF_END else BE_END
        nxt = ordered[i + 1][1] if i + 1 < len(ordered) else fam_end + 1
        end = min(nxt - 1, fam_end)
        parts = name.split()
        fam = "rainbowfish_species" if pno <= RF_END else "blue_eye_species"
        out.append((name, parts[0], " ".join(parts[1:]), fam, list(range(pno, end + 1))))
    return out

def main():
    if os.path.isdir(SRC):
        for entry in os.listdir(SRC):
            if entry == ".gitkeep": continue
            p = os.path.join(SRC, entry)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(SRC, exist_ok=True)
    write(os.path.join(SRC, "style.css"), CSS)
    copy_assets()

    sections = parse_toc()
    spset = toc_species(sections)                 # authoritative species list (book 2011)
    citations = citations_map()                   # author/year from live Contents (best-effort)

    # Which section each species belongs to.
    where = {}
    for heading in ("Rainbowfish Species", "Blue Eye Species"):
        slug = SLUGS[heading]
        for g, ep, _full in spset[heading]:
            if g:
                where[(g, ep)] = slug

    # Build every species account located in the PDF (verbatim + all figures).
    linked = {}
    accounts = []
    for name, genus, epithet, fam_slug, pdf_pages in locate_accounts():
        if name == "Melanotaenia splendida":
            pdf_pages = list(range(358, 361))
        elif name == "Pelangia mbutaensis":
            pdf_pages = [414]
        accounts.append((name, genus, epithet, fam_slug, pdf_pages))
    for ep, pr in [("splendida inornata", range(361, 370)),
                   ("splendida rubrostriata", range(370, 372)),
                   ("splendida splendida", range(372, 384)),
                   ("splendida tatei", range(384, 387))]:
        accounts.append(("Melanotaenia " + ep, "Melanotaenia", ep, "rainbowfish_species", list(pr)))
    for name, genus, epithet, fam_slug, pdf_pages in accounts:
        fname = build_species_account(genus, epithet, pdf_pages, fam_slug, citations.get(name, ""))
        linked[(genus, epithet)] = fname
    undet = build_undetermined(list(range(416, 431)), "rainbowfish_species")
    linked[("__undetermined__", "Rainbowfishes (undetermined)")] = undet

    # New-species accounts compiled from Fishes of Sahul papers (not in the 2011 book).
    # Figures are rendered from the source PDFs (pixmap clip = correct orientation).
    import runpy
    for _m in ("extract_figs", "make_garylangei", "make_jakora"):
        runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), _m + ".py"))

    build_sections(spset, citations, linked)
    SECTION_BUILD = [
        ("Introduction", "introduction", None, range(17, 20)),
        ("History of Rainbowfishes in Captivity", "history_of_rainbowfishes_in_captivity", None, range(20, 23)),
        ("Distribution & Habitat", "distribution_and_habitat", 23, range(24, 51)),
        ("Collecting & Shipping", "collecting_and_shipping", 51, range(52, 65)),
        ("Keeping & Caring", "keeping_and_caring", 65, range(66, 109)),
        ("Breeding & Raising", "breeding_and_raising", 109, range(110, 131)),
        ("Foods & Feeding", "foods_and_feeding", 131, range(132, 181)),
        ("Disease Prevention & Control", "disease_prevention_and_control", 491, range(492, 555)),
        ("Sources of Information", "sources_of_information", None, range(555, 577)),
    ]
    next_of = {s: ((SECTIONS[i + 1][0], SECTIONS[i + 1][1]) if i + 1 < len(SECTIONS) else None)
               for i, (_t2, s, _d2) in enumerate(SECTIONS)}
    for _t, _s, _dp, _rng in SECTION_BUILD:
        build_section_multipage(_t, _s, _dp, list(_rng), toc_subs(sections, _t),
                                next_section=next_of.get(_s),
                                enrich_refs=(_s == "sources_of_information"))
    build_background(next_section=next_of.get("background"))
    build_contents()
    build_home()
    build_carryover("book.html", "book.html")
    build_carryover("about.html", "about.html")

    rf = sum(1 for g, _, _ in spset["Rainbowfish Species"] if g)
    be = sum(1 for g, _, _ in spset["Blue Eye Species"] if g)
    print(f"Species (from spreadsheet): {rf} rainbowfishes, {be} blue-eyes")
    print(f"Verbatim accounts built: {len(linked)} -> {sorted(linked.values())}")
    n = sum(len(files) for _, _, files in os.walk(SRC))
    print(f"Wrote {n} files into src/")

if __name__ == "__main__":
    main()
