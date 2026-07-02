# Job: unmack-fish-page

> Convert the book *"Rainbowfishes: their care & keeping in captivity"* (Adrian Tappin,
> 2011 PDF, ~200 MB) into a new static **Home of the Rainbowfish** website that
> incorporates **all** the book's content — not just the fish species accounts.
> Requested by Peter; owned by Arthur.

## Goal
Produce a series of vanilla HTML/CSS pages, organised under 12 top-level headings,
that reproduce the full content of the PDF book. The result replaces/extends the
existing site at <https://rainbowfish.angfa.org.au/>, which today only carries the
individual species accounts. The new pages will be hosted on Digital Pacific as
plain static HTML (no Joomla/CMS).

## Source materials
| Material | Location | Status |
|----------|----------|--------|
| Book PDF (~200 MB) | mediafire: `http://www.mediafire.com/download/g7qzn85uqde8v8o/Rainbowfishes.2011.pdf` | ⛔ **needed locally** — see Dependencies |
| Table of contents | Excel, two columns (top-level heading → items under it) | ⛔ **not yet supplied** |
| Existing live site | <https://rainbowfish.angfa.org.au/> (standard HTML, hosted Digital Pacific) | ✅ reachable |
| Banner image (content pages) | `https://rainbowfish.angfa.org.au/rainbow_2a.jpg` | ✅ |
| Home logo image | `Rainbow_home.png` (used on existing top page) | ✅ |

## Deliverables
1. **Home / top page** (`index.html`) — reuse the existing top page, with edits:
   - **Remove** the "Kangaroo Tour" link/text (was `Welcome.htm`).
   - "Contents" link → points to the **new** contents generated from the PDF.
   - **Retain** "Rainbowfish Book" (`Book.htm`) and "About" (`about.htm`) links and
     the pages they point to (carry those pages over).
2. **Contents page** — index into all 12 sections (target of the "Contents" link).
3. **One page per top-level heading** (12 total), except the two species categories,
   which are index pages listing their species.
4. **One page per species** under *Rainbowfish Species* and *Blue Eye Species*,
   following the species-page template (breadcrumbs, title + author citation,
   image block, parameter table, prose sections).
5. **Shared stylesheet** (`style.css`) driving all typography/layout/colours.
6. **Left-hand vertical menu** listing the 12 top-level headings, present on every
   content page, defined once so a change propagates everywhere.
7. All **unique images** from the PDF and the live site, placed in each section's
   directory.

## Top-level headings (order as specified — note: reordered vs. the book;
"Background" = all PDF material before the Introduction)
1. Background
2. Introduction
3. Rainbowfish Species
4. Blue Eye Species
5. History of Rainbowfishes in Captivity
6. Distribution & Habitat
7. Collecting & Shipping
8. Keeping & Caring
9. Breeding & Raising
10. Foods & Feeding
11. Disease Prevention & Control
12. Sources of Information

## Directory & file naming
- One directory per top-level heading; each section's page(s) and images live inside
  its directory.
- Names: **all lower case**, **spaces → underscores**.
- **Assumption (needs confirmation):** ampersand `&` → `and`. So *Distribution &
  Habitat* → `distribution_and_habitat/`. (Alternative literal form would be
  `distribution_&_habitat` — less URL-friendly.)
- Species pages named from the species name, e.g. `rhadinocentrus_ornatus.html`.

```
/
  index.html                 (home / top page)
  contents.html              (Contents link target)
  style.css                  (shared)
  Book.htm  about.htm        (carried over from live site)
  background/
  introduction/
  rainbowfish_species/       (index + one page per species + images)
  blue_eye_species/          (index + one page per species + images)
  history_of_rainbowfishes_in_captivity/
  distribution_and_habitat/
  collecting_and_shipping/
  keeping_and_caring/
  breeding_and_raising/
  foods_and_feeding/
  disease_prevention_and_control/
  sources_of_information/
```

## Design system
Match the **true** design of the live fish-profile pages: pure white background,
black headings/text, clean blue links. Peter supplied a CSS block + two page
templates (a general one and a full species-page template) authored by Google's AI.

Palette (from supplied CSS):
- `--bg-main:#FFFFFF` · `--color-heading:#000000` · `--color-text:#111111`
- `--color-link:#002B66` · `--color-link-hover:#0056B3` · `--border-muted:#E2E8F0`
- Fonts (supplied guess): heading `Merriweather, Georgia, serif`; body `Source Sans 3, sans-serif`.

Structural rules (from Peter):
1. Page content wrapped in `<div class="content-wrapper">` (standardised — the
   supplied `species-container` class is superseded by `content-wrapper`).
2. Every scientific name → `<span class="scientific-name">` (italic serif).
3. Tank-care / parameter data → `<table class="parameter-table">`.

**Design fidelity:** sample the *real* live fish-profile pages and match their
actual fonts/palette/layout (the supplied Merriweather/Source Sans values are an AI
guess and the `@import url('https://googleapis.com')` line is a broken placeholder —
replace with a proper Google Fonts URL once the real typefaces are confirmed).

**Menu sharing:** the left-hand menu is single-sourced via the harness's
**generation step** — defined once and stamped into every page when pages are
(re)generated — not duplicated by hand.

**Content style:** reproduce the book faithfully but **lightly edit for web
readability**, applying the **biomatix `clear-writing` skill** (see Dependencies).

Supplied species template also uses: `.breadcrumbs`, `.author-citation`,
`.image-block` + `.image-caption`, `h1/h2` serif headings.

## Image sourcing & attribution policy
Priority order for every image needed on a page:
1. **Prefer images from the book** (`assets/converted/images/`, 673 extracted).
2. **Carry the book's attribution.** Where the book credits an image (photographer,
   source, collector, locality credit — usually in the caption text near the image),
   capture that credit and **display it with the image** on the web page (e.g. in the
   `.image-caption`). Build a `image_credits` map during the build so nothing is
   published uncredited when the book supplied a credit.
3. **If an image is needed but not in the book**, source it only from **government
   departments, museums, or fish-hobbyist websites**, and **include appropriate
   attribution** (credit + source link) shown with the image. Prefer clearly
   reusable/licensed images; record the source URL for each.
- Every displayed image ends up in one of two buckets: *from the book* (with the
  book's own credit if any) or *externally sourced* (with source + attribution).
  No uncredited third-party images.

## Constraints
- **Vanilla HTML + CSS only** (no frameworks, no CMS). Static hosting.
- Responsive (templates include the mobile viewport meta).
- Shared CSS so global style changes are made in one place.

## Dependencies / blockers (must resolve before build)
1. ~~**The PDF file.**~~ ✅ Supplied and converted 2026-07-02. Source at
   `assets/source/Rainbowfishes.2011.pdf` (194 MB, 576 pages, real text layer).
   Converted working assets in `assets/converted/`: per-page text (`pages/`),
   full-text `book.txt`, 673 extracted images (`images/`) + `images_manifest.csv`.
   See `assets/converted/README.md`.
2. **The Excel TOC** (heading → items mapping). → **Please supply the file**; it is
   the authoritative map of what goes under each heading and which species exist.
3. **Rights/permissions.** The book/site is © Adrian R. Tappin, "All Rights
   Reserved". Proceeding on the assumption that ANGFA is authorised to republish this
   content on their own site. → **Confirm with client at the 12:00 meeting.**
4. ~~**biomatix `clear-writing` skill.**~~ ✅ Installed 2026-07-02 from
   <https://github.com/biomatix/biomatix-tools/tree/main/plugins/clear-writing> into
   `.claude/skills/clear-writing/`.

## Decisions (confirmed by Arthur, 2026-07-02)
- Q1 `&` → `and` in directory/file names. **Yes.**
- Q2 Container class → **`content-wrapper`** (supersedes `species-container`).
- Q3 Fonts/palette → **sample the real live pages and match them** (then wire a
  proper Google Fonts URL).
- Q4 Shared menu → **generation step** (single-source template stamped into pages).
- Q5 Content fidelity → **lightly edit for web readability**, using the biomatix
  `clear-writing` skill.
- Q6 Home page → (still open) rebuild-to-match vs. copy-and-edit — decide at build time.

## APPROACH CHANGE (2026-07-02): VERBATIM
Direction changed from lightly-edited summaries to **faithful, verbatim reproduction**
of the book. Each section must reproduce the book's text; each species account must be
verbatim; **every figure** must be included, placed in order, with its caption
(locality) and photographer credit. The clear-writing skill is therefore *not* applied
to body text under this approach (verbatim wins over light editing).

Authoritative TOC/order/species now come from **`HotRF.headings.xlsx`** (Peter's
spreadsheet): 12 headings in order, each with sub-headings, and the book's 2011 species
list (79 rainbowfishes + 18 blue-eyes, incl. subspecies and "undetermined").

### Verbatim pipeline (in `generator/build.py`)
- `extract_account(pdf_pages, ...)` — per page: pulls every figure (excludes footer
  strips), sorts top-to-bottom, extracts caption (locality, ▲/▼ markers) + photographer
  credit, and reflows verbatim body text via blank-line paragraphs (sentences no longer
  break across blocks). Caption/credit lines are filtered out of body text.
- `build_species_account(...)` — renders title + citation + common name, then interleaves
  each page's figures (captioned) and verbatim paragraphs, with in-account subheadings
  (Species Summary, Distribution & Habitat, Keeping & Caring, Breeding…) as `<h2>`.
- Page-range map `ACCOUNTS`: currently just `Rhadinocentrus ornatus` (PDF 432–440),
  built and verified as the acceptance example (all 14 figures across 9 pages, correct
  localities Eprapah/Teewah/Searys/Carland/Evans Head/Woolii + credits).

### Next steps to scale verbatim
1. Auto-locate each species' PDF page range (find binomial heading + citation line;
   range = [start, next_start-1]) to populate `ACCOUNTS` for all 97 species.
2. Generate all species accounts verbatim.
3. Convert the 12 section pages from summaries to verbatim book text, following the
   spreadsheet sub-headings, with all figures.
4. CMYK→sRGB for the 12 CMYK images; residual glyph artifacts (°, ′) cleanup.

## VERBATIM RULES (refined 2026-07-02, per Peter/Arthur)
- **Spreadsheet is used ONLY for the order of the 12 major headings.**
- **Sub-headings and their heading levels come from the PDF itself** — detected by
  font size (title 16pt Georgia-Bold → h1; sub-headings 12pt Arial → h2; body 10pt).
  No hardcoded sub-heading list.
- **Figures stay in book reading order** relative to the text (two-column aware;
  full-width plates split the page into zones; column figures placed by column+y).
  Images are not moved or grouped.
- **Figure captions come only from text sitting over/inside the figure** — locality
  is the horizontal line inside the image; the photographer credit is the *vertical
  (rotated) text* in the margin. Captions are assigned per figure (fish vs habitat
  get their own photographer). Body text never enters a caption.
- **All Linnean names are italicised using the PDF's own italic font runs**
  (`TimesNewRoman,Italic`), so italics match the book exactly (incl. abbreviations
  like *R. ornatus* and *et al.*).

## STATUS: SPECIES ACCOUNTS ROLLED OUT (2026-07-02)
All species accounts generated verbatim by `generator/build.py` via `locate_accounts()`
(finds each account by its title font size, gives each a fresh page range to the next).
- **93 species accounts built** (75 Melanotaeniidae + 18 Pseudomugilidae), all linked
  from the two species-index pages; each on its own page. ~608 files, ~144 MB.
- Applied this round: numbered lists render as `<ol>` (not run-on sentences); italic
  Linnean names inherit the body font so their **size matches** the surrounding text;
  footer reads **"Original content from"**; each account starts on a fresh page.
- **Subspecies + undetermined now split out** (2026-07-02): the 4
  `Melanotaenia splendida` subspecies (*inornata*, *rubrostriata*, *splendida*, *tatei*)
  each have their own page (PDF 361–369 / 370–371 / 372–383 / 384–386); the parent
  `M. splendida` page is clipped to 358–360; `Pelangia mbutaensis` clipped to 414 so it
  no longer absorbs the undetermined section. The **"Undetermined Species"** section
  (PDF 416–430) is its own page `rainbowfishes_undetermined.html` with each
  *Melanotaenia sp. (locality)* form as a heading. All linked from the index.
- Minor: on some accounts the common-name line sits below the lead image rather than in
  the citation line (book layout); cosmetic.

### Account header restructure (2026-07-02, per review)
Each species account now renders in a fixed order: **lead image → species name (italic
h1) → attribution (author, year) → common name → Synonymy (if any) → Species Summary →
body**. The header text is never interleaved with images (first image always precedes
the name). **Synonymies render as a list** (`<ul class="synonymy">`), one synonym per
line (italic name + author/year), split on the PDF's own italic runs — not a run-on
sentence. Header components are parsed from the pre-"Species Summary" block via
`_parse_header()`; `extract_account` returns `(items, header_lines)`.

### Image integrity (2026-07-02, per review)
Large images in the PDF are stored as **multiple vertically-stacked tiles** (e.g. the
*M. splendida* distribution map = two 1360×~555 halves; the Evans Head fish = two
1360×509 halves). The generator now **detects adjacent same-width/height tiles and
stitches them back into one image** (`_group_tiles` + `_save_figure`), so no image is
split with text between its halves, and the map shows in full. Figures that overlap in
y are ordered **full-width first, column-width second** — fixed in the zone logic so a
full-width image counts as "above" an overlapping column image (previously a column
image whose top overlapped a full-width image's lower edge was emitted first, which put
e.g. the *M. goldiei* habitat above its fish portrait; now the full-width fish leads).
Multi-tile figures are re-composited via PIL (also gives clean RGB); single images keep
their original bytes.

### Section pages — multi-page model (2026-07-02, per review)
Sections are driven by the **Excel major + subsidiary headings only** (not the finer
PDF font headings). Each section = a **divider-style landing page** (water-drop hero
image → "Rainbowfishes" → section title → credited photo → hyperlinked contents) +
**one page per subsidiary heading**, each with a "Next →" link and a "↑ contents"
link; the last page links back to the start. Built by `build_section_multipage()`:
locates each subsidiary heading in the PDF (in Excel order, with a token fallback for
variants like Green-water), extracts verbatim content between headings, and stamps the
pages. **Foods & Feeding is the working proof** (landing + 29 subsidiary pages).

### Section rollout complete (2026-07-02)
All non-species sections built via `build_section_multipage()` + a `SECTION_BUILD`
config in `main()`. Three shapes handled:
- **Divider + subsidiaries** (landing + one page per sub, next/back nav): Distribution
  & Habitat (5), Collecting & Shipping (2), Keeping & Caring (23), Breeding & Raising
  (9), Foods & Feeding (29), Disease Prevention & Control (36). All subsidiary headings
  matched (0 misses).
- **No divider, no subsidiaries** (single page): Introduction, History, Sources of
  Information.
- Slug-collision fix: when a subsidiary equals the section title (e.g. "Keeping &
  Caring", "Disease Prevention & Control"), its page slug gets an `_overview` suffix so
  it doesn't overwrite the landing page.

### Background + Introduction conformed (2026-07-02)
- **Shared hero**: sections without a book divider (Introduction, History, Sources)
  get the same hero — shared `assets/water_drop.png` + "Rainbowfishes" + title + the
  section's own lead photo. `build_section_multipage` always renders a hero.
- **Background is real TEXT now** (not page images). The front matter is in a
  shift-broken subset font (AdobeHeitiStd): `_decoded_items()` reads chars via
  `get_text("rawdict")` and decodes Heiti chars with **+31** (except char 32, which is
  a real justification space) — recovers full text with digits and spaces.
  `build_background()` builds landing + text sub-pages: Copyright (p5–6), Aims (p7),
  About the Author (p8), Foreword (p9–10), Photographic Contributors (p11–12).
  Page→heading mapping is a best guess — worth a client check.
- **Front-matter formatting (2026-07-02)**: `_decoded_items` now groups lines into real
  paragraphs by vertical gap (single-spaced blocks, not line-per-paragraph), preserves
  italic runs (`<em>` — e.g. the Aims quote), and uses the line's LEFT edge for column
  detection (so justified last-lines stay single-column; the contributors page's two
  columns still split). Per page: Copyright shows the title as the document name
  (`.doc-name`, italic) not as headings; Aims is justified (`.justify`); Photographic
  Contributors is a single-spaced list (`.contributors`). Minor: a stray char on the
  copyright line ("Editioni") and the Aims signature renders as an `<h2>`.
- **Navigation** (refined): each sub-page has a "↑ &lt;Section&gt; contents" link back to
  its section landing; **Next** links stay **within the section** (no cross-section
  links); the **last page of a section has no Next**; **single-document sections**
  (Introduction, History, Sources) have **no bottom nav** at all. `_page_nav()` returns
  `[]` when there's nothing to show. Main Contents is still reachable via the breadcrumb.
- **Rogue heading fixed**: `_render_items(skip_title=...)` drops the section-title
  running label that was leaking in as an `<h2>` (e.g. the stray "Introduction").

### Remaining
1. CMYK→sRGB for the 12 CMYK images (single-image CMYK still pending; multi-tile
   composites are already RGB).
2. A spawning-data **table** in Foods & Feeding renders as text, not a real table.
3. Misc per-section polish the client flagged ("a few issues" — to revisit).

## (earlier) VERBATIM ORNATUS REVISED — reviewed & approved
The <span>Rhadinocentrus ornatus</span> account was rebuilt under the rules above:
all 14 figures in book order, per-figure locality+photographer captions, verbatim
text with PDF headings and italic Linnean names. Ready for review at
`src/rainbowfish_species/rhadinocentrus_ornatus.html`. Once approved, scale to all
97 species + convert the 12 sections to verbatim the same way.
### (earlier) VERBATIM PROOF BUILT (ornatus) / FIRST DRAFT BUILT
Cleared to build at the meeting. TOC taken from the book's own contents (PDF pages
13–15; Introduction = printed p1 = PDF p17; printed→PDF offset = +16). Rights confirmed.

### Built (in `src/`, generated by `generator/build.py`)
- Shared `style.css` (Peter's clean palette + Merriweather/Source Sans via Google
  Fonts) and single-source left menu stamped into every page.
- Home `index.html` (dark landing carried over; Kangaroo Tour removed; Contents →
  new contents; Book/About retained), `contents.html`, carried-over `book.html` /
  `about.html` with local images and repointed nav.
- All **12 section pages** under lowercase/underscore directories.
  - Introduction & History: hand-edited clean prose (clear-writing style).
  - Rainbowfish/Blue Eye Species: hand-written intros + full species lists
    (110 rainbowfishes, 19 blue-eyes) parsed from the live Contents page, grouped
    by family/genus with author citations.
  - Other 8 sections: real book text auto-extracted + cleaned, marked with a
    first-draft banner pending the clear-writing pass.
- Exemplar species page **`rhadinocentrus_ornatus.html`** with book photo
  (© Gunther Schmida), parameter table, and lightly-edited account.
- Verified by headless-Chrome screenshots at desktop width.

### Known first-draft gaps / next steps
1. Individual species accounts: only *R. ornatus* built; ~128 others are listed but
   not yet their own pages. Need per-species text + images + credits from the book.
2. Clear-writing editorial pass on the 8 auto-extracted sections (currently the
   book's raw lead paragraphs).
3. Deeper section content: only each section's lead is shown; sub-sections (from the
   TOC) not yet built out.
4. Text glyph artifacts: a few special characters (°, ′, ä) extracted as `�`; the
   Rainbowfish/Blue Eye family-overview pages (181–182) are in the subset font and
   were bypassed in favour of hand intros. Species-name decoding uses +31 offset.
5. CMYK images (12) still need sRGB conversion before use.
6. Species list is from the live 2018 index (superset) — reconcile against the book's
   2011 list.
7. Q6 resolved: home page = **copy-and-edit** the existing dark top page.

## Definition of done
- [ ] All 12 sections present with content extracted from the PDF.
- [ ] Every species has its own page under the correct category.
- [ ] Left-hand menu on every content page; editable in one place.
- [ ] Shared `style.css`; matches the real live-site look.
- [ ] All unique images placed in the correct section directories.
- [ ] Book images preferred; every image carries its credit (book credit, or
      external source + attribution) shown where it's displayed.
- [ ] Home/Contents/Rainbowfish Book/About navigation works; Kangaroo Tour removed.
- [ ] Renders correctly at mobile + desktop widths; no console errors.
- [ ] Naming/directory conventions followed throughout.

## Notes / references
Supplied CSS block and both page templates are preserved verbatim in
`assets/reference/` (to be added). Live nav confirmed 2026-07-02:
`Kangaroo Tour (Welcome.htm) | Contents (Melano.htm) | Rainbowfish Book (Book.htm) | About (about.htm)`.
Home page header image is `Rainbow_home.png`; content-page banner is `rainbow_2a.jpg`.
